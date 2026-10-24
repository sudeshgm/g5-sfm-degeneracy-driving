# G5 Block 1 results (149 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: none 77, ok 49, plausible_wrong 16, drifted 6, split 1  -> failure rate 0.671 (100/149)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.463 (69/149) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.798 [0.710, 0.871] (per-repeat range 0.773-0.808) | PASS |
| c) any single shortcut AUC within/above pose-log CI? | best: darkness (-mean brightness) AUC 0.606 | NO |
| d) failure rate all vs stopped<=50% clips | 0.671 (n=149) vs 0.664 (n=137); relative drop 1.0% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.500, 95% interval [0.406, 0.599]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.522 | [0.437, 0.609] | 0.522 | False |
| clip length, frames | 0.514 | [0.451, 0.573] | 0.514 | False |
| clip length, metres driven | 0.521 | [0.423, 0.613] | 0.521 | False |
| blur (-Laplacian variance) | 0.441 | [0.339, 0.551] | 0.559 | False |
| darkness (-mean brightness) | 0.394 | [0.300, 0.494] | 0.606 | False |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | False |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.522 |
| epipolar_angle_deg | 0.190 |
| rot_trans_ratio | 0.214 |
| static_fraction | 0.525 |
| traj_planarity | 0.351 |
| traj_collinearity | 0.210 |
| parallax_coverage | 0.510 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 12; = 0: 75; median 0.000.

Median over clips: reg share 0.250, models 1.0, reproj 0.616 px, track len 5.88, ATE 0.67 m, scale error |log s1/s2| 0.009
