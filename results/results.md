# G5 Block 1 results (76 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: none 38, ok 26, plausible_wrong 8, drifted 4  -> failure rate 0.658 (50/76)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.487 (37/76) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.778 [0.650, 0.888] (per-repeat range 0.715-0.804) | PASS |
| c) any single shortcut AUC within/above pose-log CI? | best: clip length, frames AUC 0.601 | NO |
| d) failure rate all vs stopped<=50% clips | 0.658 (n=76) vs 0.638 (n=69); relative drop 3.1% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.501, 95% interval [0.362, 0.637]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.553 | [0.423, 0.677] | 0.553 | False |
| clip length, frames | 0.601 | [0.526, 0.670] | 0.601 | False |
| clip length, metres driven | 0.532 | [0.398, 0.664] | 0.532 | False |
| blur (-Laplacian variance) | 0.440 | [0.292, 0.587] | 0.560 | False |
| darkness (-mean brightness) | 0.458 | [0.320, 0.595] | 0.542 | False |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | False |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.546 |
| epipolar_angle_deg | 0.185 |
| rot_trans_ratio | 0.207 |
| static_fraction | 0.547 |
| traj_planarity | 0.349 |
| traj_collinearity | 0.190 |
| parallax_coverage | 0.513 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 7; = 0: 36; median 0.019.

Median over clips: reg share 0.592, models 1.0, reproj 0.626 px, track len 6.06, ATE 0.21 m, scale error |log s1/s2| 0.008
