# Evidence Chain Checksum Freeze Contract

Slice: `2026-06-15-p2-48-sandbox-evidence-chain-freeze-checksum-bundle-sandbox`

This bundle freezes hashes for p2-44 through p2-47 key files. It is a drift detector only.
It does not copy source content, edit old slices, re-accept old work, certify runtime
behavior, promote artifacts, or approve action use.

## Drift Rule

- Matching hashes mean the tracked handoff/audit files still match this freeze bundle.
- Drift means stop and inspect the changed source slice before relying on the chain.
- Drift does not automatically reject prior Product Acceptance, and a match does not create new Product Acceptance.
- `--rebuild` is Builder-only. Reviewers and follow-up agents should use the default verifier so they do not refresh the freeze point by accident.
