---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p1-5-15-markdown-validation-search-sidecar-sandbox
status: pass_product_grade
truth_boundary: sandbox_plan_only
---

# Slice Plan

## Scope

Build a sandbox-only Markdown validation/search sidecar validator.

The slice proves that an mdvs-like reference can be used as a sidecar for:

- no-update Markdown/frontmatter validation;
- deterministic JSON lint output;
- path-scoped field contracts;
- manual review of inferred config;
- derived local search/cache;
- bucket-labeled activation/search hits;
- VAKS validator separation.

## Approved Write Path

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p1-5-15-markdown-validation-search-sidecar-sandbox/
```

## Non-Goals

- Do not install or run mdvs.
- Do not scan the real vault.
- Do not create or commit `.mdvs/`.
- Do not write Markdown source files.
- Do not write `raw/`, `wiki/`, `templates/`, `tools/`, mainline architecture,
  or the Obsidian vault.
- Do not start background indexers, MCP tools, hooks, or sync.
- Do not create reviewed knowledge, evidence support, reviewed relations, action
  basis, schema governance, promotion readiness, or mainline readiness.

## Artifacts

- `artifact/markdown_validation_search_sidecar_sandbox.py`
- `artifact/verify_markdown_validation_search_sidecar_sandbox.py`
- `artifact/markdown-validation-search-sidecar-contract.md`
- `artifact/failure-case-oracle.md`
- `fixtures/*.json`
- `failure-cases/*.json`

## Acceptance Criteria

- Positive fixtures cover no-update frontmatter validation, hybrid activation
  search, vault health lint, and manual-review config contract.
- Failure cases cover real vault scans, source mutation, protected paths,
  non-sandbox paths, missing required blocks, dependency installation, real
  runtime execution, background indexers/watch mode/hooks, MCP write tools,
  auto-update, non-deterministic output, missing path scopes, enum drift,
  forbidden frontmatter fields, validation pass as review pass, frontmatter as
  support, authority aliases, inferred config without review, config as schema
  governance, missing copied fixtures, symbolic cache path misuse, cache
  truth/database misuse, stale cache use, search modes, bucket filtering,
  cross-bucket fusion, hit refs, hit bucket membership, search rank as trust,
  search hit support/action misuse, sidecar replacing VAKS validators, truth
  mutation, and direct authority fields.
- Verification runs with `python -B` and leaves no `__pycache__` in the slice.
- Reviewer finds no blocker.
- Boundary Auditor finds no VAKS boundary violation.
- GPT-5.5 xhigh Product Acceptance returns `PASS_PRODUCT_GRADE`.

## Stop Conditions

Stop and ask the user if this slice needs:

- writes outside the approved sandbox path;
- protected-path edits;
- real mdvs/search runtime execution;
- dependency installation;
- real vault scan;
- Obsidian sync;
- MCP write tools;
- background service / hooks;
- commit or push;
- Product Acceptance returns `BLOCKED_NEEDS_USER`.
