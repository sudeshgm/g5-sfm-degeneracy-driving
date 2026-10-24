# G5 Block 1 results (8 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: none 3, ok 3, plausible_wrong 2  -> failure rate 0.625 (5/8)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.625 (5/8) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.800 [0.283, 1.000] (per-repeat range 0.733-0.867) | PASS |
| c) any single shortcut AUC within/above pose-log CI? | best: clip length, frames AUC 0.800 | YES |
| d) failure rate all vs stopped<=50% clips | 0.625 (n=8) vs 0.625 (n=8); relative drop 0.0% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.505, 95% interval [0.067, 0.933]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.600 | [0.167, 0.917] | 0.600 | True |
| clip length, frames | 0.800 | [0.500, 1.000] | 0.800 | True |
| clip length, metres driven | 0.733 | [0.333, 1.000] | 0.733 | True |
| blur (-Laplacian variance) | 0.400 | [0.000, 0.833] | 0.600 | True |
| darkness (-mean brightness) | 0.733 | [0.286, 1.000] | 0.733 | True |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | True |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.867 |
| epipolar_angle_deg | 0.000 |
| rot_trans_ratio | 0.067 |
| static_fraction | 0.600 |
| traj_planarity | 0.267 |
| traj_collinearity | 0.000 |
| parallax_coverage | 0.800 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 0; = 0: 5; median 0.000.

Median over clips: reg share 1.000, models 1.0, reproj 0.685 px, track len 7.04, ATE 0.04 m, scale error |log s1/s2| 0.005
