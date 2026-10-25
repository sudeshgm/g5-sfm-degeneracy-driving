# G5 Block 1 results (97 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: ok 31, none 26, plausible_wrong 24, drifted 14, split 2  -> failure rate 0.680 (66/97)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.732 (71/97) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.485 [0.359, 0.610] (per-repeat range 0.385-0.544) | FAIL (<0.75) |
| c) any single shortcut AUC within/above pose-log CI? | best: darkness (-mean brightness) AUC 0.617 | YES |
| d) failure rate all vs stopped<=50% clips | 0.680 (n=97) vs 0.655 (n=87); relative drop 3.7% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.498, 95% interval [0.372, 0.621]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.450 | [0.336, 0.563] | 0.550 | True |
| clip length, frames | 0.510 | [0.429, 0.586] | 0.510 | True |
| clip length, metres driven | 0.461 | [0.332, 0.587] | 0.539 | True |
| blur (-Laplacian variance) | 0.470 | [0.343, 0.597] | 0.530 | True |
| darkness (-mean brightness) | 0.383 | [0.268, 0.509] | 0.617 | True |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | True |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.445 |
| epipolar_angle_deg | 0.525 |
| rot_trans_ratio | 0.558 |
| static_fraction | 0.459 |
| traj_planarity | 0.493 |
| traj_collinearity | 0.508 |
| parallax_coverage | 0.459 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 10; = 0: 45; median 0.035.

Median over clips: reg share 1.000, models 1.0, reproj 0.921 px, track len 6.45, ATE 2.62 m, scale error |log s1/s2| 0.344
