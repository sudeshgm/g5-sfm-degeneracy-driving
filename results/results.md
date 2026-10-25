# G5 Block 1 results (121 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: ok 36, plausible_wrong 33, none 33, drifted 16, split 3  -> failure rate 0.702 (85/121)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.727 (88/121) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.457 [0.343, 0.570] (per-repeat range 0.376-0.542) | FAIL (<0.75) |
| c) any single shortcut AUC within/above pose-log CI? | best: darkness (-mean brightness) AUC 0.574 | YES |
| d) failure rate all vs stopped<=50% clips | 0.702 (n=121) vs 0.682 (n=110); relative drop 2.9% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.498, 95% interval [0.384, 0.607]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.472 | [0.361, 0.575] | 0.528 | True |
| clip length, frames | 0.519 | [0.447, 0.586] | 0.519 | True |
| clip length, metres driven | 0.484 | [0.372, 0.597] | 0.516 | True |
| blur (-Laplacian variance) | 0.437 | [0.328, 0.554] | 0.563 | True |
| darkness (-mean brightness) | 0.426 | [0.313, 0.546] | 0.574 | True |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | True |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.464 |
| epipolar_angle_deg | 0.575 |
| rot_trans_ratio | 0.581 |
| static_fraction | 0.476 |
| traj_planarity | 0.513 |
| traj_collinearity | 0.532 |
| parallax_coverage | 0.473 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 11; = 0: 57; median 0.022.

Median over clips: reg share 1.000, models 1.0, reproj 0.919 px, track len 6.40, ATE 2.75 m, scale error |log s1/s2| 0.400
