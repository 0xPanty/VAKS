---
slice_id: 2026-06-20-p2-109-obsidian-disposable-vault-absorption-pilot-sandbox
status: local_verification_passed
---

# Verification

## Local Verifier

Command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-20-p2-109-obsidian-disposable-vault-absorption-pilot-sandbox\artifact\run_disposable_obsidian_absorption_pilot.py
```

Result:

```json
{
  "passed": true,
  "failures": [],
  "summary": {
    "guard_count": 7,
    "positive_case_count": 7,
    "positive_hits": 7,
    "failure_case_count": 6,
    "expected_failure_hits": 6,
    "fixture_oracle_used": true,
    "failure_oracle_used": true,
    "positive_oracle_case_count": 7,
    "failure_oracle_case_count": 6,
    "positive_oracle_sha256": "82896ef4604f4fdc652007d88eb2798bc5be7ac7b44ce1e4da668ccf85138280",
    "failure_oracle_sha256": "cb28f08c034fad7eb5b0d3b66b1ef12c7c988ce1b924d10ae4f112e4e1691af5",
    "disposable_vault_created": true,
    "disposable_vault_deleted": true,
    "runtime_samples_retained": false,
    "formal_obsidian_vault_touched": false,
    "mainline_files_touched": false,
    "tools_promoted": false,
    "templates_touched": false,
    "wiki_truth_layers_touched": false,
    "commit_push_sync": false,
    "mainline_ready": false,
    "action_basis_created": false,
    "reviewed_knowledge_created": false,
    "final_gate": false
  }
}
```

## What Was Proved

The seven candidate guards can run as sandbox-only lazy gates against Obsidian-style Markdown and JSON records.

The runner also reads the fixture and failure-case oracle files, checks that the executed case set matches those oracles, and records the oracle SHA256 hashes above. This prevents the manifest from drifting away from the actual executable samples.

Positive cases passed:

- body hash valid record
- support boundary direct raw anchor
- ordinary answer not claiming action readiness
- feedback event creating review pressure only
- action-boundary failure matrix
- retrieval receipt with direct raw anchor
- runtime artifact exclusion with pycache/log excluded

Contamination cases were blocked:

- body hash tampering -> `body_hash_mismatch`
- candidate summary claimed as support -> `candidate_as_support`
- destructive action without rollback -> `AR_DESTRUCTIVE_MISSING_ROLLBACK`
- feedback truth mutation -> `FB_TRUTH_CONFIDENCE_MUTATION`
- retrieval candidate as support -> `RV_CANDIDATE_OVERLAY_FEEDBACK_AS_SUPPORT`
- pycache selected into context -> `RA_RUNTIME_ARTIFACT_SELECTED`

The disposable test vault was deleted after the run. No formal Obsidian vault, mainline file, `tools/`, `templates/`, wiki truth layer, commit, push, or sync path was touched.

## Final Gate

Command:

```powershell
python -B .\outputs\review\vaks-implementation-sandbox\2026-06-20-p2-109-obsidian-disposable-vault-absorption-pilot-sandbox\artifact\run_disposable_obsidian_absorption_pilot.py --final-gate
```

Result:

```json
{
  "passed": true,
  "failures": [],
  "summary": {
    "guard_count": 7,
    "positive_case_count": 7,
    "positive_hits": 7,
    "failure_case_count": 6,
    "expected_failure_hits": 6,
    "fixture_oracle_used": true,
    "failure_oracle_used": true,
    "positive_oracle_case_count": 7,
    "failure_oracle_case_count": 6,
    "positive_oracle_sha256": "82896ef4604f4fdc652007d88eb2798bc5be7ac7b44ce1e4da668ccf85138280",
    "failure_oracle_sha256": "cb28f08c034fad7eb5b0d3b66b1ef12c7c988ce1b924d10ae4f112e4e1691af5",
    "disposable_vault_created": true,
    "disposable_vault_deleted": true,
    "runtime_samples_retained": false,
    "formal_obsidian_vault_touched": false,
    "mainline_files_touched": false,
    "tools_promoted": false,
    "templates_touched": false,
    "wiki_truth_layers_touched": false,
    "commit_push_sync": false,
    "mainline_ready": false,
    "action_basis_created": false,
    "reviewed_knowledge_created": false,
    "final_gate": true
  }
}
```
