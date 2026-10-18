---
record_kind: sandbox_frozen_corpus_manifest
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: corpus_manifest_is_reproducibility_evidence_not_truth
action_basis_allowed: false
---

# Phase B Frozen Corpus Manifest

## What This Adds

```text
file-level frozen corpus manifest
sha256 hash snapshot for every markdown file used by primary/full corpora
corpus selection rules captured from the local harness
```

## Corpus Counts

```text
primary files: 409
primary bytes: 2655541
full files: 4384
full bytes: 13491041
primary/full overlap paths: 409
```

## Boundary

```text
This makes the local corpus identifiable and rerunnable in the original vault environment, but it is not yet a self-contained portable rerun bundle.
It does not validate original Yuxi runtime.
It does not approve C-lite, writeback, action basis, or core-doc strong conclusions.
```

## Artifacts

```text
results/phase_b_frozen_corpus_manifest.json
results/phase_b_frozen_corpus_manifest.csv
```
