# Quality Gates And Thresholds

Status: sandbox gate report. `go` means eligible for main-vault candidate operation-convention discussion, not adoption.

Current verdict:

```text
not_go_yet
Not eligible yet for main-vault candidate operation-convention discussion because human/product click-back adjudication gates are not passed.
automated_proxy_status: available_automated_proxies_pass
```

Important: human/product gates that are not measured cannot be counted as pass.

| gate | threshold | nature | current status | current value | note |
| --- | --- | --- | --- | --- | --- |
| serious_false_lite | 0 | hard | automated_proxy_pass | 0 | Automated overlay proxy only; final truth requires reviewer/adjudicator. |
| serious_full_audit_recall | 100% | hard | automated_proxy_pass | 100.0 | Automated overlay proxy only. |
| serious_folded_count | 0 | hard | automated_proxy_pass | 0 | Automated overlay proxy only. |
| wrong_actionability | 0 | hard | not_measured_yet |  | wrong_actionability requires reviewer decision plus adjudication. |
| ordinary_false_positive_rate | <= 2% | hard | automated_proxy_pass | 0.0 | Automated overlay proxy only. |
| review_due_recall | >= 95% | hard | automated_proxy_pass | 100.0 | Machine-overlay diagnostic; final gate requires adjudication. |
| review_due_precision | >= 90% | strong | automated_proxy_pass | 100.0 | Machine-overlay diagnostic; final gate requires adjudication. |
| source_record_evidence_clickback_success | >= 95% live / immutable cases | hard | not_measured_yet | {"package_pointer_source_resolve_pct": 100.0, "package_record_pointer_resolve_pct": 100.0, "package_evidence_pointer_resolve_pct": 100.0, "live_fetch_success": 24, "fallback_used": 0, "target": 24, "semantic_selector_success": 24, "semantic_selector_success_pct": 100.0, "body_window_used": 0, "boilerplate_quote": 0, "landing_class_counts": {"evidence_landing": 1, "claim_landing": 6, "claim_relevant_context_landing": 17, "selector_failure": 0}} | Package pointer resolution, live fetch, and automated semantic landing are not product click-back. claim_relevant_context_landing is weaker than evidence_landing and needs operator adjudication. |
| anchor_problem_visibility | 100% | hard | automated_proxy_pass | 100.0 | Automated visibility proxy only; failures=0; final gate requires reviewer/adjudicator. |
| authority_misunderstanding | <= 2% | hard | not_measured_yet |  | authority misunderstanding requires observation prompts, notes, and adjudication. |
| ordinary_triage_time_reduction | >= 20% vs baseline_full | product | not_measured_yet |  | ordinary triage time reduction requires actual human timing. |
| ordinary_full_audit_open_rate_reduction | >= 30% vs baseline_full | product | not_measured_yet | {"artifact_proxy_reduction_pct": 100.0, "baseline_ordinary_full_open_artifacts": 424, "shell_core_ordinary_full_open_artifacts": 0} | Artifact full-open reduction is a diagnostic proxy, not actual reviewer operation rate. |
| ordinary_rendered_line_reduction | >= 55% | supporting | automated_proxy_pass | 56.2 | Supporting renderer metric only. |
| ordinary_rendered_char_reduction | >= 60% | supporting | automated_proxy_pass | 63.4 | Supporting renderer metric only. |
| resolved_default_queue_visible | 0 | hard | automated_proxy_pass | 0 | Automated queue-surface proxy only. |
| recurrence_grouped_reduction | >= 50% | conditional | automated_proxy_pass | 83.3 | Conditional side-arm diagnostic only. |
| recurrence_over_grouping_serious_mismatch | 0 | hard when recurrence is enabled | automated_proxy_pass | 0 | Automated side-arm proxy only. |
| recurrence_human_misunderstanding | <= 5% | conditional | not_measured_yet |  | recurrence human misunderstanding requires side-packet reviewer notes and adjudication. |
| recurrence_slice_triage_time_reduction | >= 10% | conditional product | not_measured_yet |  | recurrence slice triage-time reduction requires side-packet human timing. |

## Interpretation

- The available automated proxies for `shell_core` pass.
- The overall gate is still `not_go_yet` because wrong actionability, authority misunderstanding, human timing, operation open-rate, recurrence misunderstanding, and product click-back adjudication are not formally measured.
- Package pointer resolution, live fetch, and automated semantic selector landing are useful diagnostics, but they are not human/product click-back adjudication.
- `body_window` selector landing is treated as a semantic click-back failure; the current keyword-window repair must still be rechecked by operator click logs.
- `shell_core_plus_recurrence` can only be discussed as a side arm; its human misunderstanding and triage-time gates are still unmeasured.
