# Retrieval Pilot Summary: full

## Corpus

- chunks indexed: 17869
- files indexed: 4132
- corpus hash: `d4352ff720b2adb7`

## Metrics

| Mode | hit@5 | hit@10 | candidate/raw top1 | warning when needed |
|---|---:|---:|---:|---:|
| T0_baseline_file_lexical | 6/12 | 7/12 | 9/12 | 0/10 |
| T1_yuxi_like_no_labels | 10/12 | 12/12 | 11/12 | 0/10 |
| T2_yuxi_like_boundary_labels | 10/12 | 12/12 | 11/12 | 10/10 |

## Provisional Interpretation

- Yuxi-like retrieval improved expected-source hit@5 over the baseline.
- Boundary-label mode emitted warnings for 10/10 warning-needed cases.
- This is a local simulation, not proof that Yuxi production deployment will behave identically.
