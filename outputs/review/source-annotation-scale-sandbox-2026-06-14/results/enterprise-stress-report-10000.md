---
record_kind: sandbox_enterprise_stress_report
status: complete
created_at: 2026-06-14
---

# Enterprise Stress Report

- Passed: True
- Good annotations: 10000
- Runtime: 8.3639s
- Records/sec: 1195.61
- Error count: 0
- Mutation caught: 29 / 29
- Bad context packs caught: 5 / 5
- Context pack: 60 items, 72703 bytes
- Context pack sources: 24
- Max items per source observed: 5

## View Counts

- ai_export_blocked: 609
- ai_export_ready: 9391
- annotation_inbox: 303
- cold_archive: 150
- locator_pool: 9088
- needs_anchor_repair: 329
- project_lens: 3284
- routing_queue: 580
- scale_debt: 7478
- source_drilldown: 9850
- stale_anchor_queue: 130
- support_checked_audit: 85

## Queue Accuracy

- active_bad_anchors: 329
- repair_missing: 0
- active_stale_anchors: 130
- stale_missing: 0
- ai_ready_contamination: 0

## Operator Load

- working_inbox: 303
- locator_pool: 9088
- scale_debt: 7478
- source_health_rows: 168
- source_digest_backlog: 9
- digest_backlog_p95_age_days: 14

## Top Dense Sources

- enterprise_stress/sources/source-001.md: active=837, repair=28, stale=11, scale_debt=837, digest=True
- enterprise_stress/sources/source-002.md: active=836, repair=28, stale=11, scale_debt=836, digest=True
- enterprise_stress/sources/source-005.md: active=836, repair=27, stale=11, scale_debt=836, digest=True
- enterprise_stress/sources/source-010.md: active=836, repair=29, stale=11, scale_debt=836, digest=True
- enterprise_stress/sources/source-007.md: active=835, repair=27, stale=9, scale_debt=835, digest=True
- enterprise_stress/sources/source-011.md: active=835, repair=25, stale=10, scale_debt=835, digest=True
- enterprise_stress/sources/source-003.md: active=822, repair=29, stale=12, scale_debt=822, digest=True
- enterprise_stress/sources/source-006.md: active=821, repair=28, stale=11, scale_debt=821, digest=True
- enterprise_stress/sources/source-009.md: active=820, repair=27, stale=11, scale_debt=820, digest=True
- enterprise_stress/sources/source-030.md: active=16, repair=1, stale=0, scale_debt=0, digest=False

## Errors

- none
