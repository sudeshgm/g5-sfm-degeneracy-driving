# G5 Block 1 results (180 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: plausible_wrong 52, none 51, ok 47, drifted 27, split 3  -> failure rate 0.739 (133/180)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.706 (127/180) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.483 [0.384, 0.585] (per-repeat range 0.433-0.528) | FAIL (<0.75) |
| c) any single shortcut AUC within/above pose-log CI? | best: blur (-Laplacian variance) AUC 0.585 | YES |
| d) failure rate all vs stopped<=50% clips | 0.739 (n=180) vs 0.725 (n=167); relative drop 1.9% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.500, 95% interval [0.405, 0.597]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.469 | [0.379, 0.559] | 0.531 | True |
| clip length, frames | 0.535 | [0.475, 0.593] | 0.535 | True |
| clip length, metres driven | 0.477 | [0.381, 0.570] | 0.523 | True |
| blur (-Laplacian variance) | 0.415 | [0.327, 0.508] | 0.585 | True |
| darkness (-mean brightness) | 0.476 | [0.377, 0.577] | 0.524 | True |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | True |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.457 |
| epipolar_angle_deg | 0.562 |
| rot_trans_ratio | 0.567 |
| static_fraction | 0.473 |
| traj_planarity | 0.511 |
| traj_collinearity | 0.540 |
| parallax_coverage | 0.474 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 13; = 0: 93; median 0.000.

Median over clips: reg share 1.000, models 1.0, reproj 0.918 px, track len 6.29, ATE 3.44 m, scale error |log s1/s2| 0.373
