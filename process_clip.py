#!/usr/bin/env python3
"""G5 Block 1: process one AV2 sensor clip: download minimal data, pose-only features,
image-quality shortcuts, fixed-setting COLMAP, metrics, failure label. Writes results/clips/<id>.json
then deletes raw data."""
import sys, os, json, subprocess, shutil, glob
import numpy as np, pandas as pd, cv2
from scipy.spatial.transform import Rotation as R

BUCKET = "s3://argoverse/datasets/av2/sensor"
CAM = "ring_front_center"
NFRAMES = 60
LIDAR_SWEEPS = 16  # uniformly spaced sweeps for median depth
STATIC = 0.5
NIGHT_LUM = 50.0
TMP = "/workspace/g5/tmp"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results", "clips")

def sh(cmd, **kw):
    return subprocess.run(cmd, shell=True, check=True, capture_output=True, text=True, **kw)

def s5(args):
    return sh(f"s5cmd --no-sign-request {args}")

def quat_to_R(df):
    return R.from_quat(df[["qx", "qy", "qz", "qw"]].values).as_matrix()

def umeyama(src, dst):
    mu_s, mu_d = src.mean(0), dst.mean(0)
    xs, xd = src - mu_s, dst - mu_d
    var = (xs ** 2).sum() / len(src)
    U, D, Vt = np.linalg.svd(xd.T @ xs / len(src))
    S = np.eye(3)
    if np.linalg.det(U) * np.linalg.det(Vt) < 0: S[2, 2] = -1
    Rm = U @ S @ Vt
    s = np.trace(np.diag(D) @ S) / max(var, 1e-12)
    t = mu_d - s * Rm @ mu_s
    return s, Rm, t

def pose_features(C, Rc, ts, depth, K, W, H):
    f = {}
    steps = np.linalg.norm(np.diff(C, axis=0), axis=1)
    speed = steps / np.maximum(np.diff(ts), 1e-6)
    f["static_fraction"] = float((speed < STATIC).mean())
    f["baseline_to_depth"] = float(np.median(steps) / max(depth, 1e-6))
    f["baseline_to_depth_total"] = float(steps.sum() / max(depth, 1e-6))
    d = C[-1] - C[0]
    a = Rc[:, :, 2].mean(0); a /= np.linalg.norm(a)
    f["epipolar_angle_deg"] = float(np.degrees(np.arccos(np.clip(abs(d @ a) / np.linalg.norm(d), 0, 1)))) if np.linalg.norm(d) > 1e-3 else 0.0
    rel = [R.from_matrix(Rc[i].T @ Rc[i + 1]).magnitude() for i in range(len(C) - 1)]
    f["rot_trans_ratio"] = float(np.sum(rel) / (steps.sum() + 1e-3))  # rad per metre
    sv = np.linalg.svd(C - C.mean(0), compute_uv=False)
    f["traj_planarity"] = float(sv[2] / sv[0]) if sv[0] > 1e-3 else 0.0
    f["traj_collinearity"] = float(sv[1] / sv[0]) if sv[0] > 1e-3 else 0.0
    u, v = np.meshgrid(np.linspace(0, W, 32), np.linspace(0, H, 24))
    rays = np.linalg.inv(K) @ np.stack([u.ravel(), v.ravel(), np.ones(u.size)])
    rays /= np.linalg.norm(rays, axis=0)
    cov = []
    for i in range(len(C) - 1):
        X = C[i][:, None] + Rc[i] @ rays * depth
        a1 = X - C[i][:, None]; a2 = X - C[i + 1][:, None]
        c = (a1 * a2).sum(0) / (np.linalg.norm(a1, axis=0) * np.linalg.norm(a2, axis=0) + 1e-12)
        cov.append((np.degrees(np.arccos(np.clip(c, -1, 1))) > 1.0).mean())
    f["parallax_coverage"] = float(np.mean(cov))
    f["mean_speed_ms"] = float(speed.mean())
    return f

def read_images_txt(path):
    out = {}
    lines = [l for l in open(path) if not l.startswith("#")]
    for l in lines[0::2]:
        p = l.split()
        if len(p) < 10: continue
        q = list(map(float, p[1:5])); t = np.array(list(map(float, p[5:8])))
        Rw2c = R.from_quat([q[1], q[2], q[3], q[0]]).as_matrix()
        out[p[9]] = -Rw2c.T @ t
    return out

def analyze(model_dir):
    r = sh(f"colmap model_analyzer --path {model_dir}")
    txt = r.stdout + r.stderr
    def g(key):
        for l in txt.splitlines():
            if key in l:
                try: return float(l.split(":")[-1].strip().split()[0].replace("px", ""))
                except Exception: pass
        return float("nan")
    return dict(reg=g("Registered images"), points=g("Points"), track=g("Mean track length"),
                reproj=g("Mean reprojection error"))

def main(log):
    lid = log.split("/")[1]
    outp = os.path.join(OUT, lid + ".json")
    if os.path.exists(outp): return
    work = os.path.join(TMP, lid); shutil.rmtree(work, ignore_errors=True)
    os.makedirs(work + "/img"); os.makedirs(work + "/lidar")
    base = f"{BUCKET}/{log}"
    try:
        s5(f"cp '{base}/city_SE3_egovehicle.feather' {work}/"); s5(f"cp '{base}/calibration/*' {work}/")
        names = sorted(l.split()[-1] for l in s5(f"ls '{base}/sensors/cameras/{CAM}/*'").stdout.splitlines())
        tsall = np.array([int(n[:-4]) for n in names])
        idx = np.unique(np.round(np.linspace(0, len(names) - 1, min(NFRAMES, len(names)))).astype(int))
        sel = [names[i] for i in idx]
        lnames = sorted(l.split()[-1] for l in s5(f"ls '{base}/sensors/lidar/*'").stdout.splitlines())
        with open(work + "/cmds.txt", "w") as fh:
            for n in sel: fh.write(f"cp '{base}/sensors/cameras/{CAM}/{n}' {work}/img/\n")
            for i in np.unique(np.linspace(0, len(lnames) - 1, LIDAR_SWEEPS).astype(int)):
                fh.write(f"cp '{base}/sensors/lidar/{lnames[i]}' {work}/lidar/\n")
        s5(f"run {work}/cmds.txt")
        intr = pd.read_feather(f"{work}/intrinsics.feather").set_index("sensor_name").loc[CAM]
        ext = pd.read_feather(f"{work}/egovehicle_SE3_sensor.feather").set_index("sensor_name").loc[[CAM]]
        K = np.array([[intr.fx_px, 0, intr.cx_px], [0, intr.fy_px, intr.cy_px], [0, 0, 1]])
        W, H = int(intr.width_px), int(intr.height_px)
        R_ec = quat_to_R(ext)[0]; t_ec = ext[["tx_m", "ty_m", "tz_m"]].values[0]
        poses = pd.read_feather(f"{work}/city_SE3_egovehicle.feather").sort_values("timestamp_ns")
        pts = poses.timestamp_ns.values
        def cam_pose(ts):
            j = np.clip(np.searchsorted(pts, ts), 1, len(pts) - 1)
            j = np.where(np.abs(pts[j - 1] - ts) < np.abs(pts[j] - ts), j - 1, j)
            p = poses.iloc[j]
            Rw = quat_to_R(p); tw = p[["tx_m", "ty_m", "tz_m"]].values
            return np.einsum("nij,j->ni", Rw, t_ec) + tw, np.einsum("nij,jk->nik", Rw, R_ec)
        Call, _ = cam_pose(tsall)
        ts_sel = tsall[idx]; C, Rc = cam_pose(ts_sel)
        depths = []
        for lf in sorted(glob.glob(work + "/lidar/*.feather")):
            P = pd.read_feather(lf)[["x", "y", "z"]].values
            Pc = (P - t_ec) @ R_ec
            Pc = Pc[Pc[:, 2] > 1.0]
            uv = (K @ Pc.T).T; uv = uv[:, :2] / uv[:, 2:]
            m = (uv[:, 0] >= 0) & (uv[:, 0] < W) & (uv[:, 1] >= 0) & (uv[:, 1] < H)
            if m.any(): depths.append(np.median(Pc[m, 2]))
        depth = float(np.median(depths)) if depths else float("nan")
        rec = dict(log=log, log_id=lid, n_frames_total=len(names), n_frames_used=len(sel),
                   duration_s=float((tsall[-1] - tsall[0]) * 1e-9), lidar_median_depth_m=depth)
        steps_all = np.linalg.norm(np.diff(Call, axis=0), axis=1)
        sp_all = steps_all / np.maximum(np.diff(tsall) * 1e-9, 1e-6)
        rec["metres_driven"] = float(steps_all.sum())
        rec["static_fraction_fullrate"] = float((sp_all < STATIC).mean())
        rec.update(pose_features(C, Rc, ts_sel * 1e-9, depth, K, W, H))
        lap, lum = [], []
        for n in sel:
            g = cv2.imread(f"{work}/img/{n}", cv2.IMREAD_GRAYSCALE)
            g = cv2.resize(g, (W // 2, H // 2))
            lap.append(cv2.Laplacian(g, cv2.CV_64F).var()); lum.append(g.mean())
        rec["blur_laplacian_var"] = float(np.median(lap)); rec["mean_brightness"] = float(np.mean(lum))
        rec["night_flag"] = int(rec["mean_brightness"] < NIGHT_LUM)
        db = f"{work}/db.db"; sp = f"{work}/sparse"; os.makedirs(sp)
        cp = f"{intr.fx_px},{intr.fy_px},{intr.cx_px},{intr.cy_px}"
        sh(f"colmap feature_extractor --database_path {db} --image_path {work}/img --ImageReader.camera_model PINHOLE "
           f"--ImageReader.single_camera 1 --ImageReader.camera_params {cp} --SiftExtraction.use_gpu 0 "
           f"--SiftExtraction.max_image_size 1024 --SiftExtraction.max_num_features 4096 --SiftExtraction.num_threads 6")
        sh(f"colmap sequential_matcher --database_path {db} --SiftMatching.use_gpu 0 --SiftMatching.num_threads 6 "
           f"--SequentialMatching.overlap 10 --SequentialMatching.loop_detection 0")
        try:
            sh(f"colmap mapper --database_path {db} --image_path {work}/img --output_path {sp} --Mapper.num_threads 6", timeout=3600)
        except Exception as e:
            rec["mapper_error"] = str(getattr(e, "stderr", e))[-300:]
        models = sorted(d for d in glob.glob(sp + "/*") if os.path.isdir(d))
        stats = []
        for m in models:
            a = analyze(m); a["dir"] = m; stats.append(a)
        rec["n_models"] = len(models)
        n = len(sel)
        if stats:
            best = max(stats, key=lambda a: a["reg"])
            rec["reg_share_largest"] = best["reg"] / n
            rec["reg_share"] = min(1.0, sum(a["reg"] for a in stats) / n)
            rec["mean_reproj_px"] = best["reproj"]; rec["mean_track_len"] = best["track"]; rec["n_points"] = best["points"]
            sh(f"colmap model_converter --input_path {best['dir']} --output_path {work} --output_type TXT")
            est = read_images_txt(f"{work}/images.txt")
            name2i = {nm: i for i, nm in enumerate(sel)}
            keys = sorted(est, key=lambda k: name2i[k])
            E_ = np.array([est[k] for k in keys]); G = C[[name2i[k] for k in keys]]
            if len(keys) >= 3:
                s, Rm, t = umeyama(E_, G)
                A = (s * (Rm @ E_.T)).T + t
                rec["ate_m"] = float(np.sqrt(((A - G) ** 2).sum(1).mean()))
                gl = np.linalg.norm(np.diff(G, axis=0), axis=1).sum()
                al = np.linalg.norm(np.diff(A, axis=0), axis=1).sum()
                rec["gt_len_registered_m"] = float(gl); rec["traj_len_ratio"] = float(al / gl) if gl > 1e-3 else float("nan")
                h = len(keys) // 2
                L1 = np.linalg.norm(np.diff(G[:h], axis=0), axis=1).sum() if h >= 3 else 0
                L2 = np.linalg.norm(np.diff(G[h:], axis=0), axis=1).sum() if h >= 3 else 0
                if L1 > 0.5 and L2 > 0.5:
                    rec["scale_error"] = float(abs(np.log(umeyama(E_[:h], G[:h])[0] / umeyama(E_[h:], G[h:])[0])))
                else: rec["scale_error"] = float("nan")
        else:
            rec["reg_share"] = rec["reg_share_largest"] = 0.0
        rs = rec["reg_share"]
        ate = rec.get("ate_m", float("nan")); rp = rec.get("mean_reproj_px", float("nan")); lr = rec.get("traj_len_ratio", float("nan"))
        if rs < 0.5: lab = "none"
        elif rec["n_models"] > 1: lab = "split"
        elif lr == lr and lr < 0.2: lab = "collapsed"
        elif ate > 2.0 and rp < 1.0: lab = "plausible_wrong"
        elif ate > 2.0: lab = "drifted"
        else: lab = "ok"
        rec["label"] = lab; rec["failure"] = int(lab != "ok")
        os.makedirs(OUT, exist_ok=True)
        json.dump(rec, open(outp, "w"), indent=1, default=float)
        print(lid, lab, rs, rec.get("ate_m"), flush=True)
    finally:
        shutil.rmtree(work, ignore_errors=True)

if __name__ == "__main__":
    main(sys.argv[1])
