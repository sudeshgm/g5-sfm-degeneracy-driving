# G5 Block 1 results (17 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: ok 8, none 5, plausible_wrong 3, drifted 1  -> failure rate 0.529 (9/17)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.706 (12/17) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.722 [0.439, 0.971] (per-repeat range 0.625-0.792) | FAIL (<0.75) |
| c) any single shortcut AUC within/above pose-log CI? | best: clip length, metres driven AUC 0.653 | YES |
| d) failure rate all vs stopped<=50% clips | 0.529 (n=17) vs 0.529 (n=17); relative drop 0.0% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.498, 95% interval [0.222, 0.764]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.528 | [0.250, 0.795] | 0.528 | True |
| clip length, frames | 0.604 | [0.400, 0.792] | 0.604 | True |
| clip length, metres driven | 0.653 | [0.347, 0.939] | 0.653 | True |
| blur (-Laplacian variance) | 0.375 | [0.086, 0.686] | 0.625 | True |
| darkness (-mean brightness) | 0.583 | [0.278, 0.861] | 0.583 | True |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | True |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.764 |
| epipolar_angle_deg | 0.194 |
| rot_trans_ratio | 0.167 |
| static_fraction | 0.528 |
| traj_planarity | 0.333 |
| traj_collinearity | 0.167 |
| parallax_coverage | 0.681 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 0; = 0: 9; median 0.000.

Median over clips: reg share 1.000, models 1.0, reproj 0.729 px, track len 7.27, ATE 0.07 m, scale error |log s1/s2| 0.005
