---
type: candidate-artifact-bundle
status: main-vault-candidate-asset
created: 2026-06-04
project: verified-action-knowledge-system
subject: audit-shell-v1-full-alpha-lineage
scope: operator-only-candidate-convention
verification_status: packaged-for-main-vault-recovery
---

# Audit Shell v1 Full Alpha Lineage

## Plain Status

This directory is the full main-vault copy of the Audit Shell v1 / Queue-First Operator Cockpit alpha lineage.

It keeps the alpha materials intact inside the main vault.

This is not a reduced summary and not a deletion of the original sandbox folders.

## Merge Boundary

```text
operator-only candidate convention
pilot pending
not formal adoption
not truth-layer guidance
not schema guidance
not user-facing UI
not evidence that operator adjudication has passed
not evidence that product-grade click-back has passed
```

## What Is Inside

`directories/` contains full directory copies from the alpha lineage:

```text
VAKS_deep_research_context_2026-06-01
VAKS_pro_review_audit_shell_v1_2026-06-01_package
VAKS_alpha_noise_test_2026-06-01_package
VAKS_audit_shell_output_oracle_alpha_bakeoff_2026-06-01
VAKS_pro_review_output_oracle_alpha_bakeoff_2026-06-01_package
VAKS_audit_shell_independent_oracle_patch_2026-06-01
VAKS_pro_review_independent_oracle_patch_2026-06-01_package
VAKS_480_realdata_paired_pilot_2026-06-01
VAKS_800_independent_oracle_pilot_2026-06-01
VAKS_full_ingest_sim_2026-06-04
VAKS_audit_shell_pressure_test_2026-06-04
VAKS_audit_shell_v1_candidate_pro_review_2026-06-04
VAKS_audit_shell_queue_cockpit_prototype_2026-06-04
VAKS_queue_cockpit_PRO_REVIEW_PACKAGE_2026-06-04
VAKS_queue_cockpit_CLOSEOUT_2026-06-04
```

`zip_packages/` contains the matching packaged zip artifacts, including the intermediate 800-package snapshots and final closeout package.

`ARTIFACT_MANIFEST.csv` lists copied directories and zip packages with file counts, bytes, and main-vault paths.

## Current Accepted Candidate

The current candidate convention is:

```text
Audit Shell v1 / Queue-First Operator Cockpit
```

Current handoff:

```text
00_handoff/2026-06-04-audit-shell-v1-queue-cockpit-candidate-closeout.md
```

Main record:

```text
outputs/review/2026-06-04-audit-shell-v1-candidate-operation-convention.md
```

Final closeout:

```text
outputs/review/2026-06-04-audit-shell-v1-final-version-review.md
outputs/review/2026-06-04-audit-shell-v1-queue-cockpit-closeout.md
```

Main-framework integration validation:

```text
outputs/review/2026-06-04-audit-shell-v1-main-framework-integration-validation.md
```

## Why This Is In Main Vault

The design-review loop is closed.

Pro's final result:

```text
no merge blocker
can merge as operator-only candidate convention
not formal adoption
next step is 80/60/60 operator pilot
```

## Next Step

Run the pilot from:

```text
outputs/review/audit-shell-v1-full-alpha-lineage-2026-06-04/directories/VAKS_queue_cockpit_CLOSEOUT_2026-06-04/NEXT_OPERATOR_PILOT_PROMPT.md
```

Do not restart broad design review unless a pilot finds a real blocker.
