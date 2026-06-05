---
type: sandbox_readme
status: active_test_sandbox
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-full-mainline-copy-insertion-test
truth_boundary: sandbox only; not reviewed knowledge; not mainline architecture; not schema; not template; not commit authority
---

# Project Lens Full Mainline Copy Test

## Purpose

This sandbox tests the exact question:

```text
What happens if complete copies of the main architecture docs receive a real Project Lens insertion?
```

It does not modify the real mainline documents.

## Files

Baseline full copies:

```text
baseline/FUSION_ARCHITECTURE_V0_2_DRAFT.md
baseline/ARCHITECTURE_PRINCIPLES.md
```

Full copies with Project Lens inserted:

```text
with-project-lens/FUSION_ARCHITECTURE_V0_2_DRAFT.md
with-project-lens/ARCHITECTURE_PRINCIPLES.md
```

Reports:

```text
FULL_MAINLINE_COPY_INSERTION_TEST_REPORT.md
COMPLETION_AUDIT.md
```

## Boundary

This is a sandbox integration test. It does not mean:

```text
Project Lens is now mainline.
SCHEMA.md changed.
REVIEW_QUEUE.md changed.
templates changed.
commit is authorized.
push is authorized.
```

## Current Verdict

```yaml
full_mainline_copy_created: yes
project_lens_inserted_into_copies: yes
root_mainline_modified_by_this_test: no
schema_review_queue_templates_modified: no
verdict: pass_as_full_copy_sandbox
mainline_merge_authorized: no
```
