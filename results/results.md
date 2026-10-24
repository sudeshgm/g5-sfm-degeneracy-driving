# G5 Block 1 results (111 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: none 56, ok 39, plausible_wrong 11, drifted 5  -> failure rate 0.649 (72/111)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.477 (53/111) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.781 [0.681, 0.872] (per-repeat range 0.760-0.786) | PASS |
| c) any single shortcut AUC within/above pose-log CI? | best: darkness (-mean brightness) AUC 0.595 | NO |
| d) failure rate all vs stopped<=50% clips | 0.649 (n=111) vs 0.634 (n=101); relative drop 2.3% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.500, 95% interval [0.390, 0.616]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.549 | [0.447, 0.651] | 0.549 | False |
| clip length, frames | 0.553 | [0.484, 0.617] | 0.553 | False |
| clip length, metres driven | 0.500 | [0.388, 0.619] | 0.500 | False |
| blur (-Laplacian variance) | 0.429 | [0.319, 0.541] | 0.571 | False |
| darkness (-mean brightness) | 0.405 | [0.292, 0.522] | 0.595 | False |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | False |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.517 |
| epipolar_angle_deg | 0.207 |
| rot_trans_ratio | 0.224 |
| static_fraction | 0.552 |
| traj_planarity | 0.356 |
| traj_collinearity | 0.202 |
| parallax_coverage | 0.495 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 10; = 0: 52; median 0.022.

Median over clips: reg share 0.300, models 1.0, reproj 0.617 px, track len 6.04, ATE 0.26 m, scale error |log s1/s2| 0.009
