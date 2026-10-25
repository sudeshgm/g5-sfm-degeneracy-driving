# G5 Block 1 — FAILURE REPORT (idea KILLED)

**Verdict:** killed under the pre-registered stop rules. Check (b) failed: the pose-log model cannot predict COLMAP failure (AUC 0.494, 95% CI [0.398, 0.588], threshold 0.75).

All numbers come from `results/per_clip.csv` and `results/results.md` (v2, produced by `analyze.py`; rerun on the final 200-clip v2 results reproduced them exactly).

## What was tested
Can simple numbers computed only from the ego-pose log (no reconstruction) predict whether COLMAP fails on a driving clip?
- Data: 200 randomly chosen Argoverse 2 Sensor clips (fixed seed, list in `clip_list.txt`), `ring_front_center` camera, ego poses, calibration, LiDAR. Stopped clips were **not** filtered out. Waymo was not added.
- Pose-log features: baseline-to-depth (LiDAR median depth), epipolar angle, rotation/translation ratio, stopped share (speed < 0.5 m/s), trajectory planarity, collinearity, parallax coverage.
- Shortcut baselines: stopped share, clip length (frames, metres driven), blur (Laplacian variance), mean brightness, night flag.
- COLMAP: one fixed setting for every clip (SIFT, sequential matching, incremental mapper, same frame cap/subsampling), recorded in `colmap_settings.txt`. No per-clip tuning.
- Failure = any label other than `ok` (labels: none / split / collapsed / drifted / plausible_wrong / ok, see the plan's data/NOTES.md).
- Predictor: logistic regression on pose-log features, 10× repeated 5-fold CV (out-of-fold scores), bootstrap 95% CI.

## v1 setup bug and v2 fix
- **v1 (invalid):** cameras were given to COLMAP as `PINHOLE`, ignoring AV2's strong front-camera lens distortion, and the focal length was refined during mapping. Under forward motion this broke reconstruction: many clips registered only about 2 of 60 frames, giving a spurious 65% "none" rate in the interim check. v1 results are archived in `results/v1_pinhole_refinefocal/` and are not used.
- **v2 (used here):** `FULL_OPENCV` camera built from the AV2 calibration (including distortion), with intrinsics frozen (no focal/distortion refinement). Same fixed setting for all 200 clips, all rerun from scratch.

## Results (v2, n = 200)

Labels: ok 49, plausible_wrong 60, none 58, drifted 30, split 3, collapsed 0 → failure rate 0.755 (151/200).

| Check | Result | Rule | Verdict |
|---|---|---|---|
| a) share of clips with >95% of frames registered | 0.700 (140/200) | dead if >0.90 | premise alive |
| b) pose-log LR AUC (CV, 95% CI) | **0.494 [0.398, 0.588]** | fail if <0.75 | **FAIL → killed** |
| c) any single shortcut AUC within/above pose-log CI? | all six are (best: blur, 0.579 orientation-free) | — | yes, but everything is at chance |
| d) failure rate, all vs stopped share ≤ 0.5 | 0.755 (n=200) vs 0.742 (n=186); relative drop 1.7% | drop ≥ 1/3? | no |

Random baseline at the same failure rate: AUC 0.499, 95% interval [0.401, 0.595].

Shortcut AUCs (check c):

| Feature | AUC | 95% CI | max(AUC, 1−AUC) |
|---|---|---|---|
| stopped share | 0.469 | [0.379, 0.555] | 0.531 |
| clip length, frames | 0.539 | [0.480, 0.597] | 0.539 |
| clip length, metres driven | 0.472 | [0.379, 0.560] | 0.528 |
| blur (−Laplacian variance) | 0.421 | [0.333, 0.515] | 0.579 |
| darkness (−mean brightness) | 0.490 | [0.391, 0.585] | 0.510 |
| night flag | 0.500 | [0.500, 0.500] | 0.500 |

Single pose features (raw AUC): baseline_to_depth 0.458, epipolar_angle 0.547, rot_trans_ratio 0.558, static_fraction 0.471, planarity 0.518, collinearity 0.532, parallax_coverage 0.473.

Stopped-share histogram: `results/stopped_share_hist.png` — 103 clips never stopped, 14 clips stopped more than half the time, median 0.000 (stopped clips were kept).

**In plain words:** the pose-log features, and every shortcut baseline, sit near chance (AUC ≈ 0.42–0.58, CIs overlapping the random baseline). Nothing we measured from poses or simple image statistics tells failing clips from working ones.

## Caveats
- The `drifted` / `plausible_wrong` labels use a fixed 2 m ATE limit (after similarity alignment), not a limit scaled to path length.
- 104 of the 148 clips with a computed ATE have error > 2% of their registered path length (verified from data).
- 60 clips are `plausible_wrong` (low reprojection error < 1 px but ATE > 2 m) — the largest failure class, and one that pose geometry may not be expected to predict.
- Only one camera rig (AV2 ring_front_center) and one dataset; one fixed COLMAP setting.

## Possible follow-up (note only)
COLMAP's "plausible but wrong" rate is about 30% on AV2 (60/200 clips: good reprojection error, wrong trajectory). That silent-failure rate could be a finding in its own right.

## References
- PoolNet, arXiv:2512.05362 — https://arxiv.org/abs/2512.05362
- ORBIT, arXiv:2608.22039 — https://arxiv.org/abs/2608.22039
- COLMAP issues on initialisation / sequential-trajectory failures:
  - colmap/colmap#1685 "Why is my start reconstruction step not working?" — https://github.com/colmap/colmap/issues/1685
  - colmap/colmap#1521 "reconstruction produces disjoint path" (single continuous trajectory) — https://github.com/colmap/colmap/issues/1521
