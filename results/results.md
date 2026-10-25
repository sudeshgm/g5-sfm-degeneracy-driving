# G5 Block 1 results (49 AV2 Sensor clips, ring_front_center, COLMAP fixed setting)

Failure labels: ok 16, plausible_wrong 16, none 10, drifted 6, split 1  -> failure rate 0.673 (33/49)

## Checks

| Check | Result | Verdict |
|---|---|---|
| a) clips with >95% frames registered | 0.796 (39/49) | premise alive (<=0.90) |
| b) pose-log LR AUC (10x5-fold CV OOF, bootstrap 95% CI) | 0.477 [0.314, 0.639] (per-repeat range 0.447-0.568) | FAIL (<0.75) |
| c) any single shortcut AUC within/above pose-log CI? | best: clip length, metres driven AUC 0.631 | YES |
| d) failure rate all vs stopped<=50% clips | 0.673 (n=49) vs 0.660 (n=47); relative drop 2.1% | does NOT drop by 1/3 |

Random baseline at same failure rate: AUC mean 0.500, 95% interval [0.328, 0.672]

## Single-feature AUCs (shortcuts; a-priori direction, plus orientation-free max(AUC,1-AUC))

| Feature | AUC | 95% CI | max(AUC,1-AUC) | within/above pose-log CI |
|---|---|---|---|---|
| stopped share (static_fraction_fullrate) | 0.504 | [0.333, 0.658] | 0.504 | True |
| clip length, frames | 0.497 | [0.374, 0.608] | 0.503 | True |
| clip length, metres driven | 0.369 | [0.213, 0.533] | 0.631 | True |
| blur (-Laplacian variance) | 0.479 | [0.305, 0.668] | 0.521 | True |
| darkness (-mean brightness) | 0.405 | [0.225, 0.583] | 0.595 | True |
| night flag | 0.500 | [0.500, 0.500] | 0.500 | True |

## Single pose features (raw AUC, higher value = failure)

| Feature | AUC |
|---|---|
| baseline_to_depth | 0.373 |
| epipolar_angle_deg | 0.570 |
| rot_trans_ratio | 0.616 |
| static_fraction | 0.523 |
| traj_planarity | 0.515 |
| traj_collinearity | 0.528 |
| parallax_coverage | 0.373 |

Stopped-share histogram: results/stopped_share_hist.png. Clips with stopped share > 0.5: 2; = 0: 26; median 0.000.

Median over clips: reg share 1.000, models 1.0, reproj 0.874 px, track len 6.45, ATE 2.53 m, scale error |log s1/s2| 0.280
