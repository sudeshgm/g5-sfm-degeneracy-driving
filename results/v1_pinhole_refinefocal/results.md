# G5 Block 1 results (176 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: none 92, ok 57, plausible_wrong 17, drifted 9, split 1  -> failure rate 0.676 (119/176)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.455 (80/176) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.797 [0.724, 0.865] (per-repeat range 0.787-0.804) | PASS |
| c) any single shortcut AUC within/above pose-log CI? | best: darkness (-mean brightness) AUC 0.597 | NO |
| d) failure rate all vs stopped<=50% clips | 0.676 (n=176) vs 0.671 (n=164); relative drop 0.8% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.499, 95% interval [0.403, 0.588]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.513 | [0.427, 0.600] | 0.513 | False |
| clip length, frames | 0.505 | [0.441, 0.567] | 0.505 | False |
| clip length, metres driven | 0.527 | [0.442, 0.618] | 0.527 | False |
| blur (-Laplacian variance) | 0.456 | [0.368, 0.551] | 0.544 | False |
| darkness (-mean brightness) | 0.403 | [0.314, 0.498] | 0.597 | False |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | False |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.530 |
| epipolar_angle_deg | 0.205 |
| rot_trans_ratio | 0.209 |
| static_fraction | 0.515 |
| traj_planarity | 0.352 |
| traj_collinearity | 0.206 |
| parallax_coverage | 0.521 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 12; = 0: 89; median 0.000.

Median over clips: reg share 0.200, models 1.0, reproj 0.616 px, track len 5.78, ATE 0.58 m, scale error |log s1/s2| 0.009
