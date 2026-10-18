---
type: source_intake_minimum_fix_checklist
status: implementation_status_v2_13
created_at: 2026-06-13
scope: Pro minimum Source Intake hardening fixes
truth_boundary: implementation checklist only; not Source Intake P0 approval
---

# Minimum Fix Checklist

## Plain Verdict

The minimum static/contract hardening items are mostly landed in the sandbox
package. The remaining blockers are semantic debt and runtime evidence, not the
original static validator gaps.

This checklist does not claim Source Intake P0 passed.

## Status Table

| Priority | Fix item | Current status | Evidence / note |
|---|---|---|---|
| Highest | Move or exclude canonical-scope legacy `project_lens_overlay` | Done | 17 files moved to `outputs/review/_legacy_project_lens`; canonical lint excludes old path; tombstone retained. |
| Highest | Make canonical confirmed-overlay placeholders hard errors | Done | `confirmed_overlay_placeholder_value` is an error; current lint has 0 hard errors. |
| Highest | Clear raw top-level `relations` or move to candidate/legacy namespace | Done | Top-level raw `relations` is an error; existing items moved to `candidate_relation_suggestions` or out of top-level raw source frontmatter. |
| Highest | Clear raw top-level `confidence` or scope it under capture/extraction namespace | Done | Top-level raw `confidence` is an error; capture confidence is under `source_integrity.capture_confidence`. |
| High | Normalize `retrieval_policy.pack_allowed` to one string enum | Done | Registry uses `none`, `activation_only`, `review_input_only`, `drilldown_required`, `reviewed_support`; no boolean/string false dual encoding. |
| High | Remove `overlay_state: suggested` from canonical persisted overlay states | Done | Registry persistent `overlay_state` is `none`, `confirmed`, `archived`; `overlay_suggestion` is trace/inbox only and persisted use errors. |
| High | Add canonical validated surface count excluding legacy lens | Done | Current lint summary now records `canonical_validated_surfaces_excluding_legacy_lens` and `legacy_project_lens_excluded_count`. |
| Medium | Move `source_quality`, `relevance`, `freshness`, `cross_source_count` to `legacy_raw_metadata` or delete | Done | 11 files moved these soft authority-like fields to `legacy_raw_metadata`; compilers must ignore that subtree. |
| Medium | Cross-check `why_saved` placeholder against body `Why Captured` / `为什么收录` | Done | 118 defer-ok migration warnings; 4 missing-reason items surfaced as high-risk manual review. |
| Medium | Split `graph_neighbor` out of Source Intake core registry | Done | `record_kind` registry no longer includes `graph_neighbor`. |
| Medium | Split `promotion_gate: review_passed` into status/result layer | Done for intake registry | `promotion_gate` only allows `none` and `v0_2_13_required`; review result remains outside the gate enum. |
| Low | Add legacy migration changelog / deprecation note | Done as package evidence | `MIGRATION_REPORT.md`, non-isomorphic mapping policy, legacy compatibility report, and tombstone are included. |

## Remaining Non-Static Work

The following are not solved by this checklist:

- read-only answer-loop citation/support audit;
- index rebuild and receipt diff;
- graph/compiler sandbox proving no legacy/raw fields become formal edges;
- pack-builder replay proving candidates/overlays do not become support;
- dry-run writeback/forbidden-action tests.

Those are tracked in `RUNTIME_RISK_MATRIX.md`.
