---
record_kind: sandbox_enterprise_stress_report
status: complete
created_at: 2026-06-14
---

# Enterprise Stress Report

- Passed: True
- Good annotations: 5000
- Runtime: 3.8481s
- Records/sec: 1299.33
- Error count: 0
- Mutation caught: 29 / 29
- Bad context packs caught: 5 / 5
- Context pack: 60 items, 72583 bytes
- Context pack sources: 24
- Max items per source observed: 5

## View Counts

- ai_export_blocked: 309
- ai_export_ready: 4691
- annotation_inbox: 153
- cold_archive: 75
- locator_pool: 4538
- needs_anchor_repair: 167
- project_lens: 1642
- routing_queue: 297
- scale_debt: 3782
- source_drilldown: 4925
- stale_anchor_queue: 67
- support_checked_audit: 44

## Queue Accuracy

- active_bad_anchors: 167
- repair_missing: 0
- active_stale_anchors: 67
- stale_missing: 0
- ai_ready_contamination: 0

## Operator Load

- working_inbox: 153
- locator_pool: 4538
- scale_debt: 3782
- source_health_rows: 120
- source_digest_backlog: 9
- digest_backlog_p95_age_days: 14

## Top Dense Sources

- enterprise_stress/sources/source-005.md: active=426, repair=15, stale=6, scale_debt=426, digest=True
- enterprise_stress/sources/source-010.md: active=425, repair=15, stale=5, scale_debt=425, digest=True
- enterprise_stress/sources/source-002.md: active=424, repair=14, stale=6, scale_debt=424, digest=True
- enterprise_stress/sources/source-003.md: active=419, repair=16, stale=6, scale_debt=419, digest=True
- enterprise_stress/sources/source-001.md: active=418, repair=15, stale=6, scale_debt=418, digest=True
- enterprise_stress/sources/source-006.md: active=418, repair=14, stale=7, scale_debt=418, digest=True
- enterprise_stress/sources/source-009.md: active=418, repair=13, stale=5, scale_debt=418, digest=True
- enterprise_stress/sources/source-007.md: active=417, repair=13, stale=5, scale_debt=417, digest=True
- enterprise_stress/sources/source-011.md: active=417, repair=14, stale=5, scale_debt=417, digest=True
- enterprise_stress/sources/source-016.md: active=16, repair=3, stale=0, scale_debt=0, digest=False

## Errors

- none
