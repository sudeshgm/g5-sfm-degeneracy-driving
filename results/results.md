# G5 Block 1 results (24 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: ok 10, plausible_wrong 9, none 3, drifted 2  -> failure rate 0.583 (14/24)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.875 (21/24) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.479 [0.222, 0.721] (per-repeat range 0.414-0.579) | FAIL (<0.75) |
| c) any single shortcut AUC within/above pose-log CI? | best: darkness (-mean brightness) AUC 0.757 | YES |
| d) failure rate all vs stopped<=50% clips | 0.583 (n=24) vs 0.565 (n=23); relative drop 3.1% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.504, 95% interval [0.271, 0.750]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.407 | [0.189, 0.625] | 0.593 | True |
| clip length, frames | 0.386 | [0.219, 0.544] | 0.614 | True |
| clip length, metres driven | 0.486 | [0.237, 0.727] | 0.514 | True |
| blur (-Laplacian variance) | 0.557 | [0.296, 0.800] | 0.557 | True |
| darkness (-mean brightness) | 0.243 | [0.063, 0.471] | 0.757 | True |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | True |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.471 |
| epipolar_angle_deg | 0.586 |
| rot_trans_ratio | 0.643 |
| static_fraction | 0.450 |
| traj_planarity | 0.343 |
| traj_collinearity | 0.607 |
| parallax_coverage | 0.457 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 1; = 0: 13; median 0.000.

Median over clips: reg share 1.000, models 1.0, reproj 0.825 px, track len 6.89, ATE 1.79 m, scale error |log s1/s2| 0.154
