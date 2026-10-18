---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
derived_from:
  - raw/repos/2026-06-07-jc2255-log-collect-ai-analytics-source.md
  - raw/repos/_snapshots/jc2255-log-collect-ai-analytics-3a960f4e7aa23a2558df0b7eea813b656ecb3166.zip
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: yes
routing_hint:
  - query-run
  - feedback-ledger
  - use-ledger
  - observability
  - action-debug
  - tool-health
  - source-intake
possible_project_refs:
  - VAKS
point_anchor_refs:
  - source: raw/repos/2026-06-07-jc2255-log-collect-ai-analytics-source.md
    snapshot_ref: raw/repos/_snapshots/jc2255-log-collect-ai-analytics-3a960f4e7aa23a2558df0b7eea813b656ecb3166.zip
borrow_value: strong
borrow_order:
  - "P1: trace_id-centered event spine for query-run, source-intake, sync, review, action, and feedback flows."
  - "P1: raw trigger sample + AI diagnosis + root cause + resolution + category + history correlation in one diagnostic record."
  - "P1: deterministic rule/threshold prefilter before LLM diagnosis, with alert silence windows to prevent noise storms."
  - "P1: debug chain first: locate which stage failed before changing action or truth records."
  - "P2: connector/tool heartbeat and offline alerts for future agent/source health."
  - "P2: logstore/event-bucket scoping, retention, export, RBAC, and dashboard ergonomics."
  - "P3: Kafka/Elasticsearch/HA production stack and commercial product packaging."
avoid:
  - "Do not treat log volume, alert count, dashboard status, or AI diagnosis as truth confidence."
  - "Do not let feedback/use logs directly mutate reviewed knowledge or source reliability."
  - "Do not import Kafka/ES/HA stack before a lightweight event ledger is proven."
  - "Do not copy or fork commercial/proprietary code or binaries."
  - "Do not run AI-agent task execution without explicit tool-safety and user authorization."
  - "Do not store private logs without redaction, retention, and access policy."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing VAKS query-run observability, feedback/use ledger runtime, action-debug audit trail, source-sync monitoring, or tool/connector health."
  support_when: "Comparing event ingestion, alert history, AI diagnosis surfaces, trace IDs, dashboards, exports, or operational troubleshooting flows."
  risk_when: "Any proposal makes logs, alerts, LLM diagnoses, dashboard counts, or user feedback become reviewed truth, evidence support, source reliability, or action basis."
  cold_references:
    - raw/repos/2026-06-07-jc2255-log-collect-ai-analytics-source.md
    - raw/repos/_snapshots/jc2255-log-collect-ai-analytics-3a960f4e7aa23a2558df0b7eea813b656ecb3166.zip
tags:
  - candidate
  - provisional
  - repo-distillation
  - observability
  - query-run
  - feedback
  - log-analytics
  - ai-alerting
---

# Candidate Distillation: LCA as VAKS Observability and Use-Ledger Reference

## Boundary

This is a candidate knowledge point for `jc2255/log-collect-ai-analytics`.

It can route attention, compare ideas, or support a VAKS Project Overlay. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 人话总结

这个库最适合 VAKS 的地方，不是“日志系统本身”，而是它给了一个很完整的观察闭环：

```text
事件进来
-> 进入某个日志库 / topic / index
-> 带 trace_id 穿过每一段链路
-> 可以搜索原始日志
-> 规则先筛一遍
-> LLM 再做诊断
-> 告警历史保留原始样本、根因、修复步骤、分类和历史关联
-> 出问题时按 trace_id 查是哪一段坏了
```

对 VAKS 来说，最强借鉴是：

```text
把每次查询、入库、同步、review、action、feedback 都变成可追踪事件。
```

但边界必须钉死：

```text
日志不是知识。
告警不是证据。
AI 诊断不是 review。
dashboard 不是 truth。
```

最佳一句话借鉴：

```text
VAKS 需要一个轻量 observability/use-ledger，让系统知道自己怎么犯错，而不是让日志替系统判断什么是真的。
```

## Source

```yaml
derived_from:
  - raw/repos/2026-06-07-jc2255-log-collect-ai-analytics-source.md
checked_commit: 3a960f4e7aa23a2558df0b7eea813b656ecb3166
snapshot_ref: raw/repos/_snapshots/jc2255-log-collect-ai-analytics-3a960f4e7aa23a2558df0b7eea813b656ecb3166.zip
key_anchors:
  - README.md:44-55
  - README.md:111-147
  - README.md:539-580
  - README.md:766-815
  - README.md:900-929
  - README.md:963-985
  - deploy/mysql/init.sql:50-64
  - deploy/mysql/init.sql:247-271
  - deploy/mysql/init.sql:454-472
  - deploy/nginx.conf:16-34
  - configs/syslog.yaml:1-22
```

## Candidate Points

### 1. `trace_id` is the strongest borrow

LCA pushes one `trace_id` through:

```text
HTTP request / response body / response header
-> apiserver logs
-> Kafka
-> logtransfer
-> Elasticsearch `_trace_id`
```

Its troubleshooting guide then uses that ID to ask:

```text
apiserver received?
Kafka wrote?
logtransfer consumed?
ES flushed?
ES searchable?
```

VAKS adaptation:

```yaml
vaks_trace_id:
  applies_to:
    - source_intake_run
    - candidate_distillation_run
    - review_run
    - query_run
    - context_pack_build
    - action_basis_prepare
    - action_attempt
    - feedback_event
    - obsidian_sync
  carried_in:
    - source_card
    - candidate_note
    - query-run
    - feedback-event
    - sync ledger
    - review package
  purpose:
    - debug_path
    - provenance_of_processing
    - replay_anchor
  forbidden:
    - truth_confidence
    - evidence_support
```

Why it matters:

```text
When VAKS gives a bad answer, we should not guess.
We should be able to trace: what source was activated, what candidate was included,
which overlay was suggested, what review boundary appeared, what was excluded,
what feedback came back.
```

### 2. Alert history is a good model for diagnostic records

The database has `alert_histories` fields for:

```text
content
status
rule_name
severity
store_name
raw_logs
root_cause
resolution
category
```

The UI exposes both "AI诊断报告" and "原始日志", plus same-category historical correlation.

VAKS adaptation:

```yaml
diagnostic_event:
  event_id:
  trace_id:
  event_kind: query_failure | sync_failure | weak_answer | wrong_scope | stale_activation | action_error
  severity:
  raw_trigger_sample:
  activated_context:
  ai_diagnosis:
    summary:
    possible_root_cause:
    suggested_fix:
    category:
  related_history:
  immediate_status: diagnostic_only
  review_pressure_effect:
  action_basis_allowed: false
```

This can make VAKS much more self-debuggable:

```text
不是只留下“这次回答不好”。
而是留下：触发样本是什么、AI 怎么解释、历史上有没有同类、下一次应该避开什么。
```

Boundary:

```text
diagnostic_event can create review pressure.
diagnostic_event cannot mutate truth.
```

### 3. Rule prefilter + LLM diagnosis is the right shape

LCA does not send everything to the LLM. It describes:

```text
ES rule pre-filtering
ERROR / FATAL count threshold
keyword hit threshold
silence period
OpenAI-compatible LLM deep analysis
multi-channel notification
```

VAKS adaptation:

```text
cheap deterministic trigger
-> candidate diagnostic packet
-> LLM explanation
-> human-visible report
-> review pressure / routing hint
```

Potential triggers:

- source anchor missing.
- candidate used as action basis.
- overlay default-retrieved without confirmation.
- answer includes unsupported claim.
- repeated wrong-scope feedback.
- Obsidian sync hash mismatch.
- stale source/version used in action-facing answer.
- tool/connector offline.

Do not send every event to the LLM. Use lazy gates:

```text
ordinary event: log only
warning event: group and summarize
high-impact event: LLM diagnostic + review pressure
action-facing event: evidence/debug packet
```

### 4. Use logs should become activation learning, not truth learning

The strongest VAKS mapping is to `FEEDBACK.md` and `templates/query-run.md`.

LCA's event flow can inspire a VAKS Use Ledger:

```yaml
use_event:
  trace_id:
  query_id:
  project:
  question_summary:
  activated_sources:
  activated_candidates:
  authority_bucket:
  excluded_candidates:
  answer_path:
  warnings:
  user_feedback:
  result:
  next_activation_hint:
```

Allowed effects:

```text
activation ranking
scope fit
usefulness
review_due
workflow debugging
```

Forbidden effects:

```text
truth confidence
verification status
source reliability
reviewed relation strength
decision outcome
```

This directly matches VAKS:

```text
feedback improves future activation.
feedback does not rewrite truth.
```

### 5. Agent heartbeat maps to VAKS connector/tool health

LCA has agents with heartbeat status and offline notification. For VAKS, a future equivalent could track:

- Obsidian sync connector health.
- source fetcher health.
- video transcription engine health.
- GitHub/source scout health.
- browser or local tool availability.
- scheduled intake monitor health.

Candidate record:

```yaml
connector_health_event:
  connector_id:
  last_seen:
  status: online | offline | degraded
  affected_flows:
  diagnostic_note:
  user_visible_warning:
  action_basis_allowed: false
```

This is P2 because VAKS does not yet run an always-on automation stack, but it becomes important once source scouting, sync, or scheduled jobs exist.

### 6. Event store buckets map to log stores, not knowledge stores

LCA has log stores with API keys, Kafka topics, retention, AI alert config, and storage lifecycle.

For VAKS:

```text
source cards live in the vault.
event logs live in an operational ledger.
```

Possible VAKS event buckets:

- `source_intake_events`
- `query_run_events`
- `feedback_events`
- `review_events`
- `sync_events`
- `tool_health_events`
- `action_debug_events`

Each bucket needs:

```yaml
retention_policy:
privacy_class:
redaction_required:
default_retrieval:
action_basis_allowed: false
```

This prevents a very common failure:

```text
because it is logged, it starts to look authoritative.
```

### 7. The heavy production stack is not the thing to borrow first

LCA uses MySQL, Redis, Kafka, Elasticsearch, Nginx, Docker Compose, HA mode, leader election, RBAC, snapshot backup, and commercial license activation.

For VAKS, this is mostly P3/P2:

```text
Good to know what mature production observability looks like.
Bad to copy before the lightweight event contract exists.
```

Smallest elegant VAKS adoption:

```text
Markdown/JSONL event ledger first.
Then query-run/feedback schema.
Then optional SQLite/FTS.
Only later consider ES/Kafka/dashboard.
```

## Open Questions

- Should VAKS `query-run` records get a mandatory `trace_id` now, or only when runtime tooling appears?
- Should Obsidian sync/hash mismatches create `diagnostic_event` records in `outputs/feedback/`?
- Can `feedback-event` and `query-run` templates share a `trace_id` / `parent_trace_id` field without overloading ordinary capture?
- What privacy class should source-intake and action-debug logs carry?
- When should repeated diagnostic events escalate from activation warning to review_due?
- How much of alert history should be visible in Obsidian versus hidden in a local operational store?

## Routing Hint

```yaml
good_for:
  - query-run observability
  - feedback/use ledger
  - tool and connector health
  - source intake runtime diagnostics
  - action debugging
  - sync/hash monitoring
  - dashboard/workbench design
not_good_for:
  - reviewed knowledge
  - evidence support
  - action basis
  - truth confidence
  - direct code reuse
  - immediate Kafka/ES deployment
```

## Borrow Gradient

```yaml
borrow_value: strong
P1:
  - trace_id event spine
  - raw sample plus AI diagnosis report
  - root cause / resolution / category fields
  - same-category history correlation
  - rule prefilter before LLM diagnosis
  - debug chain before changing action/truth records
P2:
  - connector heartbeat / offline alert
  - event buckets with retention
  - RBAC and privacy-aware workbench
  - exportable JSONL/CSV event evidence
P3:
  - Kafka / Elasticsearch / Nginx HA stack
  - commercial license machinery
  - production container topology
avoid:
  - logs as truth
  - AI diagnosis as review
  - dashboard count as authority
  - direct code/binary reuse
  - storing private logs without redaction
```

## Forbidden

```text
project_borrow_scope
project_non_borrow_scope
decision outcome
formal pattern
action basis
truth confidence
reviewed relation
```
