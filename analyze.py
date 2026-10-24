#!/usr/bin/env python3
"""Aggregate per-clip JSON -> per_clip.csv, AUCs, checks a-d, figures, results.md."""
import json, glob, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score

rng = np.random.default_rng(0)
df = pd.DataFrame([json.load(open(f)) for f in glob.glob("results/clips/*.json")])
order = [l.strip().split("/")[1] for l in open("clip_list.txt")]
df["order"] = df.log_id.map({k: i for i, k in enumerate(order)}); df = df.sort_values("order").drop(columns="order")
def relabel(r):
    # NOTES.md taxonomy; 'split' requires frames actually divided (largest model < 95% of frames),
    # because COLMAP 3.10 sometimes emits a redundant 2nd model whose images are all in the 1st.
    ate, rp, lr = r.get("ate_m", np.nan), r.get("mean_reproj_px", np.nan), r.get("traj_len_ratio", np.nan)
    if r.reg_share < 0.5: return "none"
    if r.n_models > 1 and r.reg_share_largest < 0.95: return "split"
    if lr == lr and lr < 0.2: return "collapsed"
    if ate > 2.0 and rp < 1.0: return "plausible_wrong"
    if ate > 2.0: return "drifted"
    return "ok"
df["label_raw"] = df.label; df["label"] = df.apply(relabel, axis=1); df["failure"] = (df.label != "ok").astype(int)
df.drop(columns=["mapper_error"], errors="ignore").to_csv("results/per_clip.csv", index=False)
y = df.failure.values; n = len(df)
POSE = ["baseline_to_depth", "epipolar_angle_deg", "rot_trans_ratio", "static_fraction",
        "traj_planarity", "traj_collinearity", "parallax_coverage"]
X = df[POSE].copy()
for c in ["baseline_to_depth", "rot_trans_ratio", "traj_planarity", "traj_collinearity"]:
    X[c] = np.log10(X[c] + 1e-4)  # heavy-tailed -> log
X = X.fillna(X.median()).values

def boot_ci(y, s, B=2000):
    a = []
    for _ in range(B):
        i = rng.integers(0, len(y), len(y))
        if y[i].min() != y[i].max(): a.append(roc_auc_score(y[i], s[i]))
    return np.percentile(a, [2.5, 97.5])

oof = np.zeros(n); reps = []
for r in range(10):  # 10x repeated 5-fold, OOF scores averaged
    o = np.zeros(n)
    for tr, te in StratifiedKFold(5, shuffle=True, random_state=r).split(X, y):
        m = make_pipeline(StandardScaler(), LogisticRegression(C=1.0, max_iter=2000)).fit(X[tr], y[tr])
        o[te] = m.predict_proba(X[te])[:, 1]
    reps.append(roc_auc_score(y, o)); oof += o / 10
auc = roc_auc_score(y, oof); lo, hi = boot_ci(y, oof)
# shortcuts with a-priori direction (higher score = predicted failure)
SC = {"stopped share (static_fraction_fullrate)": df.static_fraction_fullrate,
      "clip length, frames": df.n_frames_total, "clip length, metres driven": df.metres_driven,
      "blur (-Laplacian variance)": -df.blur_laplacian_var, "darkness (-mean brightness)": -df.mean_brightness,
      "night flag": df.night_flag}
rows = []
for k, s in SC.items():
    s = s.values.astype(float)
    a = roc_auc_score(y, s); c = boot_ci(y, s)
    rows.append((k, a, c[0], c[1], max(a, 1 - a), lo <= max(a, 1 - a) <= hi or max(a,1-a) > hi))
single_pose = {f: roc_auc_score(y, df[f].fillna(df[f].median())) for f in POSE}
rand = [roc_auc_score(y, rng.random(n)) for _ in range(2000)]
# checks
a_share = (df.reg_share > 0.95).mean()
sf = df.static_fraction_fullrate
fr_all = y.mean(); keep = sf <= 0.5; fr_keep = y[keep].mean()
drop = (fr_all - fr_keep) / fr_all if fr_all > 0 else np.nan
plt.figure(figsize=(6, 3.5)); plt.hist(sf, bins=np.linspace(0, 1, 21), edgecolor="k")
plt.xlabel("stopped share (fraction of frames, speed < 0.5 m/s)"); plt.ylabel("clips")
plt.title(f"AV2 Sensor, {n} random clips (none removed)"); plt.tight_layout(); plt.savefig("results/stopped_share_hist.png", dpi=120)
lab = df.label.value_counts()
L = []
L.append(f"# G5 Block 1 results ({n} AV2 Sensor clips, ring_front_center, COLMAP fixed setting)\n")
L.append(f"Failure labels: " + ", ".join(f"{k} {v}" for k, v in lab.items()) + f"  -> failure rate {fr_all:.3f} ({y.sum()}/{n})\n")
L.append("## Checks\n\n| Check | Result | Verdict |\n|---|---|---|")
L.append(f"| a) clips with >95% frames registered | {a_share:.3f} ({int((df.reg_share>0.95).sum())}/{n}) | premise {'DEAD (>0.90)' if a_share>0.9 else 'alive (<=0.90)'} |")
L.append(f"| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | {auc:.3f} [{lo:.3f}, {hi:.3f}] (per-repeat range {min(reps):.3f}-{max(reps):.3f}) | {'PASS' if auc>=0.75 else 'FAIL (<0.75)'} |")
best = max(rows, key=lambda r: r[4])
L.append(f"| c) any single shortcut AUC within/above pose-log CI? | best: {best[0]} AUC {best[4]:.3f} | {'YES' if any(r[5] for r in rows) else 'NO'} |")
L.append(f"| d) failure rate all vs stopped<=50% clips | {fr_all:.3f} (n={n}) vs {fr_keep:.3f} (n={keep.sum()}); relative drop {drop:.1%} | {'drops >= 1/3' if drop>=1/3 else 'does NOT drop by 1/3'} |")
L.append(f"\nRandom baseline at same failure rate: AUC mean {np.mean(rand):.3f}, 95% interval [{np.percentile(rand,2.5):.3f}, {np.percentile(rand,97.5):.3f}]\n")
L.append("## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))\n\n| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |\n|---|---|---|---|---|")
for r in rows: L.append(f"| {r[0]} | {r[1]:.3f} | [{r[2]:.3f}, {r[3]:.3f}] | {r[4]:.3f} | {r[5]} |")
L.append("\n## Single pose features (raw AUC, higher value = failure)\n\n| Feature | AUC |\n|---|---|")
for k, v in single_pose.items(): L.append(f"| {k} | {v:.3f} |")
L.append(f"\nStopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: {(sf>0.5).sum()}; = 0: {(sf==0).sum()}; median {sf.median():.3f}.")
L.append(f"\nMedian over clips: reg share {df.reg_share.median():.3f}, models {df.n_models.median()}, reproj {df.mean_reproj_px.median():.3f} px, track len {df.mean_track_len.median():.2f}, ATE {df.ate_m.median():.2f} m, scale error |log s1/s2| {df.scale_error.median():.3f}")
open("results/results.md", "w").write("\n".join(L) + "\n"); print("\n".join(L))
