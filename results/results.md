# G5 Block 1 results (44 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: none 21, ok 17, plausible_wrong 4, drifted 2  -> failure rate 0.614 (27/44)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.523 (23/44) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.765 [0.595, 0.914] (per-repeat range 0.745-0.804) | PASS |
| c) any single shortcut AUC within/above pose-log CI? | best: blur (-Laplacian variance) AUC 0.634 | YES |
| d) failure rate all vs stopped<=50% clips | 0.614 (n=44) vs 0.619 (n=42); relative drop -0.9% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.502, 95% interval [0.322, 0.680]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.526 | [0.358, 0.689] | 0.526 | False |
| clip length, frames | 0.600 | [0.498, 0.700] | 0.600 | True |
| clip length, metres driven | 0.547 | [0.376, 0.722] | 0.547 | False |
| blur (-Laplacian variance) | 0.366 | [0.197, 0.549] | 0.634 | True |
| darkness (-mean brightness) | 0.401 | [0.219, 0.577] | 0.599 | True |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | False |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.606 |
| epipolar_angle_deg | 0.205 |
| rot_trans_ratio | 0.185 |
| static_fraction | 0.515 |
| traj_planarity | 0.331 |
| traj_collinearity | 0.179 |
| parallax_coverage | 0.529 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 2; = 0: 22; median 0.002.

Median over clips: reg share 1.000, models 1.0, reproj 0.626 px, track len 6.65, ATE 0.21 m, scale error |log s1/s2| 0.005
