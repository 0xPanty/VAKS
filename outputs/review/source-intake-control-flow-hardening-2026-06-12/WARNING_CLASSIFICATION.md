---
type: source_intake_warning_classification
status: diagnostic
created_at: 2026-06-12
scope: current lint semantic warning triage
truth_boundary: diagnostic only; not Source Intake P0 approval
---

# Warning Classification

## Verdict

The current lint result should be read in two layers:

```text
structural intake contract: pass
semantic migration layer: debt_pending
canonical Source Intake P0: not passed
```

The warnings are not one flat class. They split into:

```text
migration_debt_defer_ok: 118
high_risk_manual_review: 4
hard_error_canonical_p0: 0 remaining in current lint
```

After v2.9, legacy Project Lens files are not part of canonical current lint.
They are tracked separately as a 17-file compatibility set under
`outputs/review/_legacy_project_lens/`, with downstream consumption disabled
and a tombstone retained for audit.

## Classification Rules

| Class | Current count | Rule | Recommended action |
|---|---:|---|---|
| `migration_debt_defer_ok` | 118 | Raw source `why_saved` placeholder while the record remains provenance/orientation only and the body contains a real capture/save reason. | Keep as visible migration debt; require drilldown before pack/support use. |
| `high_risk_manual_review` | 4 | Raw source `why_saved` placeholder without a real body capture/save reason. | Add a real save reason before canonical P0, or leave as explicit manual-review debt. |
| legacy compatibility set | 17 | Legacy Project Lens files moved out of canonical current lint. | Keep excluded, or manually migrate selected gold examples later. |
| `hard_error_canonical_p0` | 0 current | Confirmed overlay core placeholders, raw source top-level `confidence`, raw source top-level `relations`. | Must be fixed or excluded before structural pass. |

## Representative Matrix

| Example | File / field | Current class | Rule | Action |
|---|---|---|---|---|
| 1 | `raw/articles/2026-01-thinking-os-with-ai-vault-source.md` / `why_saved` | `migration_debt_defer_ok` | Source card remains raw provenance/orientation. | Keep warning; drilldown before pack/support. |
| 2 | `raw/articles/2026-04-04-karpathy-llm-wiki-source.md` / `why_saved` | `migration_debt_defer_ok` | Same raw source placeholder pattern. | Keep warning. |
| 3 | `raw/papers/2026-05-29-w3c-prov-source.md` / `why_saved` | `migration_debt_defer_ok` | Same raw source placeholder pattern. | Keep warning. |
| 4 | `raw/papers/2026-05-30-w3c-web-annotation-source.md` / `why_saved` | `migration_debt_defer_ok` | Same raw source placeholder pattern. | Keep warning. |
| 5 | `raw/repos/2026-06-11-awesome-obsidian-vault/giallozafferano-recipe-site-source.md` / `why_saved` | `migration_debt_defer_ok` | Frontmatter is placeholder; body/source record remains raw. | Keep warning. |
| 6 | `raw/videos/2026-06-03-bilibili-omniget-source.md` / `why_saved` | `migration_debt_defer_ok` | Same raw video source placeholder pattern. | Keep warning. |
| 7 | `outputs/review/_legacy_project_lens/2026-06-11-ai-reverse-toolkit-agent-workflow.md` / legacy marker | legacy compatibility set | Legacy project lens overlay can be mistaken for canonical overlay if left in canonical path. | Keep excluded or manually migrate as gold example. |
| 8 | `outputs/review/_legacy_project_lens/2026-06-11-cyrilxbt-n8n-obsidian-business-brain-overlay.md` / legacy marker | legacy compatibility set | Same legacy overlay risk. | Keep excluded or migrate manually. |
| 9 | `outputs/review/_legacy_project_lens/2026-06-11-the-book-of-secret-knowledge-curated-index-overlay.md` / legacy marker | legacy compatibility set | Same legacy overlay risk. | Keep excluded or migrate manually. |
| 10 | `outputs/review/_legacy_project_lens/VAKS.md` / legacy marker | legacy compatibility set | Legacy sandbox artifact; not canonical P0 proof. | Keep excluded or migrate manually. |
| 11 | raw source / `cross_source_count` | cleared from top-level current lint | Count can be misread as evidential strength. | Moved to `legacy_raw_metadata` where retained. |
| 12 | raw source / `freshness` | cleared from top-level current lint | Freshness is applicability/diagnostic metadata, not authority. | Moved to `legacy_raw_metadata` where retained. |
| 13 | raw source / `relevance` | cleared from top-level current lint | Relevance is query-dependent and should not be fixed raw authority. | Moved to `legacy_raw_metadata` where retained. |
| 14 | raw source / `source_quality` | cleared from top-level current lint | Quality labels look like trust/authority proxies. | Moved to `legacy_raw_metadata` where retained. |
| 14a | raw source / `why_saved` placeholder without body reason | `high_risk_manual_review` | Missing save reason is information debt, not defer-ok migration debt. | Add a real `Why Captured` / `为什么收录` section or fill `why_saved`. |
| 15 | confirmed overlay / `target_ref` placeholder | `hard_error_canonical_p0` | Confirmed overlay without real target has no reliable mount point. | Fill real target or exclude. |
| 16 | confirmed overlay / `project_borrow_scope` placeholder | `hard_error_canonical_p0` | Borrow scope is a core overlay semantic field. | Fill real project-local scope or exclude. |
| 17 | confirmed overlay / `project_non_borrow_scope` placeholder | `hard_error_canonical_p0` | Non-borrow boundary prevents universal-ban confusion. | Fill real project-local boundary or exclude. |
| 18 | confirmed overlay / `project_reopen_trigger` placeholder | `hard_error_canonical_p0` | Reopen trigger prevents stale project sidecars. | Fill real trigger or exclude. |
| 19 | raw source / top-level `confidence` | `hard_error_canonical_p0` | Top-level confidence can be read as trust/authority. | Delete or move to capture/extraction namespace. |
| 20 | raw source / top-level `relations` | `hard_error_canonical_p0` | Top-level relations can be read as reviewed graph edges. | Move to candidate relation suggestions or sidecar. |

## Boundary

This matrix classifies warnings and hard-error rules. It does not prove semantic
adequacy, runtime behavior, reviewed truth, or action readiness.

`author` and legacy `kp_ref` are intentionally not treated as P0 authority
fields. `author` may be unknown or omitted on raw source cards; if present it
must not be a fake specific placeholder. `kp_ref` can remain in excluded legacy
Project Lens material as a navigation pointer only, not as evidence support,
action basis, or proof of a canonical overlay.

`legacy_raw_metadata` is likewise audit/tombstone metadata only. It is not a
retrieval, graph, pack, or support signal. Current lint can block serialized
receipt/pack misuse, but runtime answer-loop behavior still needs separate
read-only trace validation.
