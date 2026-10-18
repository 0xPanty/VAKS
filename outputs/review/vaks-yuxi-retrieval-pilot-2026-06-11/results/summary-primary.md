# Retrieval Pilot Summary: primary

## Corpus

- chunks indexed: 3002
- files indexed: 268
- corpus hash: `8dee3606ca6f82e8`

## Metrics

| Mode | hit@5 | hit@10 | candidate/raw top1 | warning when needed |
|---|---:|---:|---:|---:|
| T0_baseline_file_lexical | 9/12 | 9/12 | 11/12 | 0/10 |
| T1_yuxi_like_no_labels | 11/12 | 12/12 | 9/12 | 0/10 |
| T2_yuxi_like_boundary_labels | 11/12 | 12/12 | 9/12 | 7/10 |

## Provisional Interpretation

- Yuxi-like retrieval improved expected-source hit@5 over the baseline.
- Boundary-label mode emitted warnings for 7/10 warning-needed cases.
- This is a local simulation, not proof that Yuxi production deployment will behave identically.
