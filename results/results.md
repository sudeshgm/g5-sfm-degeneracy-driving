# G5 Block 1 results (200 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: plausible_wrong 60, none 58, ok 49, drifted 30, split 3  -> failure rate 0.755 (151/200)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.700 (140/200) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.494 [0.398, 0.588] (per-repeat range 0.449-0.550) | FAIL (<0.75) |
| c) any single shortcut AUC within/above pose-log CI? | best: blur (-Laplacian variance) AUC 0.579 | YES |
| d) failure rate all vs stopped<=50% clips | 0.755 (n=200) vs 0.742 (n=186); relative drop 1.7% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.499, 95% interval [0.401, 0.595]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.469 | [0.379, 0.555] | 0.531 | True |
| clip length, frames | 0.539 | [0.480, 0.597] | 0.539 | True |
| clip length, metres driven | 0.472 | [0.379, 0.560] | 0.528 | True |
| blur (-Laplacian variance) | 0.421 | [0.333, 0.515] | 0.579 | True |
| darkness (-mean brightness) | 0.490 | [0.391, 0.585] | 0.510 | True |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | True |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.458 |
| epipolar_angle_deg | 0.547 |
| rot_trans_ratio | 0.558 |
| static_fraction | 0.471 |
| traj_planarity | 0.518 |
| traj_collinearity | 0.532 |
| parallax_coverage | 0.473 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 14; = 0: 103; median 0.000.

Median over clips: reg share 1.000, models 1.0, reproj 0.918 px, track len 6.29, ATE 3.56 m, scale error |log s1/s2| 0.471
