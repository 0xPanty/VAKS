---
record_kind: sandbox_validation_report
status: complete
created_at: 2026-06-14
---

# Source Annotation Sandbox Validation Report

- Passed: True
- Good annotations: 35
- Good errors: 0
- Warnings: 4
- Mutation annotations caught: 7 / 7
- Bad context pack caught: True

## View Counts

- ai_export_blocked: 3
- ai_export_ready: 30
- annotation_inbox: 30
- cold_archive: 1
- needs_anchor_repair: 3
- project_lens: 14
- routing_queue: 12
- scale_debt: 29
- source_drilldown: 34
- stale_anchor_queue: 1
- support_checked_audit: 1

## Errors

- none

## Warnings

- samples/sources/web-annotation-model.md: 17 active annotations; source digest route present
- selector duplicate pressure 7x: samples/sources/obsidian-workbench.md|TextQuoteSelector|A Base view is a surface for work.|159|193|None|None|None|None
- selector duplicate pressure 5x: samples/sources/rag-attribution-notes.md|TextQuoteSelector|Citation correctness is not the same as faithfulness.|102|155
- selector duplicate pressure 11x: samples/sources/web-annotation-model.md|TextQuoteSelector|A source annotation points to a source segment.|33|80|None|Non

## Mutation Results

- samples/mutations/ann-web-007.md: caught (1 errors)
- samples/mutations/mut-action-basis.md: caught (1 errors)
- samples/mutations/mut-broken-ready.md: caught (2 errors)
- samples/mutations/mut-missing-warning.md: caught (1 errors)
- samples/mutations/mut-project-borrow-scope.md: caught (1 errors)
- samples/mutations/mut-support-no-packet.md: caught (1 errors)
- samples/mutations/mut-truth-mutation.md: caught (1 errors)
