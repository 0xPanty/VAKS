# Click-back Semantic Landing Evaluation

Status: sandbox diagnostic. This separates transport fetch, path resolution, and claim-relevant selector landing.

Current readout:

| metric | value |
| --- | --- |
| target | 24 |
| transport_fetch_success | 24 |
| source_path_resolves | 24 |
| record_path_resolves | 24 |
| evidence_path_resolves | 24 |
| semantic_selector_success | 24 |
| body_window_used | 0 |
| boilerplate_quote | 0 |
| landing_class_counts | {'evidence_landing': 1, 'claim_landing': 6, 'claim_relevant_context_landing': 17, 'selector_failure': 0} |
| semantic_selector_success_pct | 100.0 |

## Interpretation

- `transport_fetch_success` means a live / immutable snapshot was fetched.
- `source_path_resolves` means the local source handle opens.
- `semantic_selector_success` means the selected quote came from evidence, claim, or claim-keyword matching, not from a generic body window.
- `landing_class` separates evidence landing, claim landing, and weaker claim-relevant context landing.
- `body_window` and boilerplate quotes are not product-grade click-back success.

## Rows Needing Selector Repair

| case_id | quote_strategy | landing_class | boilerplate_quote | quote_preview |
| --- | --- | --- | --- | --- |
