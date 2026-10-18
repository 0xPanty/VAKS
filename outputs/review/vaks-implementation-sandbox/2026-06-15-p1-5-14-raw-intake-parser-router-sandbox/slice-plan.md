---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p1-5-14-raw-intake-parser-router-sandbox
status: implemented_pending_review
truth_boundary: sandbox_plan_only
---

# Slice Plan

## Scope

Build a sandbox-only raw intake parser router / extraction bundle validator.

The slice proves that messy inputs can be routed by modality and wrapped in a
VAKS-owned extraction bundle while preserving:

- original source identity and SHA256 hash;
- parser adapter, version, runtime, config hash, model/locality/license limits;
- retained extraction outputs;
- source anchors;
- source-card / candidate routing boundaries;
- explicit non-authority flags.

## Approved Write Path

```text
outputs/review/vaks-implementation-sandbox/2026-06-15-p1-5-14-raw-intake-parser-router-sandbox/
```

## Non-Goals

- Do not run OmniParse, OCR, ASR, crawler, or any real parser runtime.
- Do not install dependencies.
- Do not write `raw/`, `wiki/`, `templates/`, `tools/`, mainline architecture,
  or the Obsidian vault.
- Do not start background services, MCP tools, hooks, or sync.
- Do not create reviewed knowledge, evidence support, reviewed relations, action
  basis, promotion readiness, or mainline readiness.

## Artifacts

- `artifact/raw_intake_parser_router_sandbox.py`
- `artifact/verify_raw_intake_parser_router_sandbox.py`
- `artifact/raw-intake-parser-router-contract.md`
- `artifact/failure-case-oracle.md`
- `fixtures/*.json`
- `failure-cases/*.json`

## Acceptance Criteria

- Positive fixtures cover document, image/OCR, video/transcript, and public web
  routing shapes.
- Failure cases cover missing hashes, weak hashes, route mismatch, non-lazy
  parsing, always-on heavy parsing, dependency install, full runtime import,
  license/locality review, retained output gaps, scratch-only output, protected
  paths, missing anchors, authority claims, private access, source-card
  authority fields, and candidate non-provisional status.
- Verification runs with `python -B` and leaves no `__pycache__` in the slice.
- Reviewer finds no blocker.
- Boundary Auditor finds no VAKS boundary violation.
- GPT-5.5 xhigh Product Acceptance returns `PASS_PRODUCT_GRADE`.

## Stop Conditions

Stop and ask the user if this slice needs:

- writes outside the approved sandbox path;
- protected-path edits;
- real parser execution;
- dependency installation;
- private/account crawling without explicit user authorization;
- Obsidian sync;
- MCP write tools;
- background service / hooks;
- commit or push;
- Product Acceptance returns `BLOCKED_NEEDS_USER`.
