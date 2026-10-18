# Evidence Chain Freeze Guide

Status: sandbox checksum drift detector only.

Source slices: `4`

Tracked files: `31`

Missing files: `0`

Report status mismatches: `0`

Interpretation:

- Run this verifier before relying on the p2-44..p2-47 handoff/audit chain.
- If drift appears, stop and inspect the changed source slice.
- Do not use `--rebuild` during review; it refreshes the freeze point inside this sandbox.
- This freeze is not re-acceptance, runtime certification, release approval, promotion, reviewed knowledge, evidence support, or action basis.
