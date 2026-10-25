# G5 Block 1 results (149 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: ok 42, plausible_wrong 42, none 39, drifted 23, split 3  -> failure rate 0.718 (107/149)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.732 (109/149) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.464 [0.364, 0.568] (per-repeat range 0.406-0.530) | FAIL (<0.75) |
| c) any single shortcut AUC within/above pose-log CI? | best: blur (-Laplacian variance) AUC 0.588 | YES |
| d) failure rate all vs stopped<=50% clips | 0.718 (n=149) vs 0.701 (n=137); relative drop 2.4% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.500, 95% interval [0.397, 0.599]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.483 | [0.379, 0.577] | 0.517 | True |
| clip length, frames | 0.531 | [0.465, 0.594] | 0.531 | True |
| clip length, metres driven | 0.481 | [0.383, 0.580] | 0.519 | True |
| blur (-Laplacian variance) | 0.412 | [0.319, 0.514] | 0.588 | True |
| darkness (-mean brightness) | 0.451 | [0.339, 0.555] | 0.549 | True |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | True |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.474 |
| epipolar_angle_deg | 0.595 |
| rot_trans_ratio | 0.589 |
| static_fraction | 0.486 |
| traj_planarity | 0.523 |
| traj_collinearity | 0.561 |
| parallax_coverage | 0.475 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 12; = 0: 71; median 0.016.

Median over clips: reg share 1.000, models 1.0, reproj 0.920 px, track len 6.39, ATE 3.02 m, scale error |log s1/s2| 0.379
