# G5 Block 1 results (74 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: ok 25, plausible_wrong 21, none 18, drifted 9, split 1  -> failure rate 0.662 (49/74)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.757 (56/74) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.506 [0.369, 0.642] (per-repeat range 0.398-0.534) | FAIL (<0.75) |
| c) any single shortcut AUC within/above pose-log CI? | best: darkness (-mean brightness) AUC 0.637 | YES |
| d) failure rate all vs stopped<=50% clips | 0.662 (n=74) vs 0.632 (n=68); relative drop 4.5% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.500, 95% interval [0.359, 0.639]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.463 | [0.325, 0.597] | 0.537 | True |
| clip length, frames | 0.492 | [0.393, 0.589] | 0.508 | True |
| clip length, metres driven | 0.436 | [0.295, 0.575] | 0.564 | True |
| blur (-Laplacian variance) | 0.429 | [0.295, 0.565] | 0.571 | True |
| darkness (-mean brightness) | 0.363 | [0.224, 0.508] | 0.637 | True |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | True |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.447 |
| epipolar_angle_deg | 0.511 |
| rot_trans_ratio | 0.537 |
| static_fraction | 0.476 |
| traj_planarity | 0.487 |
| traj_collinearity | 0.479 |
| parallax_coverage | 0.451 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 6; = 0: 34; median 0.038.

Median over clips: reg share 1.000, models 1.0, reproj 0.916 px, track len 6.46, ATE 2.45 m, scale error |log s1/s2| 0.308
