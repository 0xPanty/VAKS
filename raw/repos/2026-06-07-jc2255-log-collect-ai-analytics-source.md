---
type: source
status: source-captured
title: "LCA / log-collect-ai-analytics"
source_id: github:jc2255/log-collect-ai-analytics@3a960f4e7aa23a2558df0b7eea813b656ecb3166
source_uri: https://github.com/jc2255/log-collect-ai-analytics
source_url: https://github.com/jc2255/log-collect-ai-analytics
source_type: repo
author: jc2255
publisher: GitHub
published_at:
updated_at: 2026-06-05T10:41:25Z
captured_at: 2026-06-07
captured_by: Codex
version_or_commit: 3a960f4e7aa23a2558df0b7eea813b656ecb3166
source_status: active-commercial-reference
raw_location: raw/repos/_snapshots/jc2255-log-collect-ai-analytics-3a960f4e7aa23a2558df0b7eea813b656ecb3166.zip
snapshot_sha256: 05B72B98049CCF4B2908974F1EE4FE27DA8643EAFF2FD2F8BBF4188B5057BDB5
processing_mode: repository_review
processing_level: heavy
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
review_priority: high
review_owner: Codex
formalization_status: raw-only
topics:
  - log-analytics
  - observability
  - ai-alerting
  - feedback-ledger
  - query-run
projects:
  - VAKS
source_family:
  - external-reference
  - repo-reference
upstream_sources: []
verification_status: source-captured
candidate_relation_suggestions:
  - target: "query-run-and-feedback-observability"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The repo shows a concrete trace_id-centered logging and AI-diagnosis loop that may refine VAKS query-run, use-ledger, feedback, and action-debug observability."
    source_anchor: README.md:539-580; README.md:900-929; deploy/mysql/init.sql:50-64
tags:
  - source
  - repo
  - observability
  - log-analytics
  - ai-alerting
  - feedback
---

# 来源记录：jc2255/log-collect-ai-analytics

## 为什么收录

用户明确要求把 `github.com/jc2255/log-collect-ai-analytics` 压榨透，并判断它对 VAKS 很契合。

本记录只保存来源、快照、许可边界、source hygiene 和可追踪锚点。它不是采纳结论，不是 reviewed knowledge，不是 action basis。

## 来源信息

- 作者：`jc2255`
- 发布方：GitHub
- 原始链接：https://github.com/jc2255/log-collect-ai-analytics
- 仓库描述：`日志收集智能分析系统`
- 默认分支：`main`
- 检查 commit：`3a960f4e7aa23a2558df0b7eea813b656ecb3166`
- commit 时间：`2026-06-03T06:23:22Z`
- commit message：`feat: 修改readme`
- pushed_at：`2026-06-05T10:41:25Z`
- GitHub stars / forks at capture：59 / 0
- License：commercial / NOASSERTION; repository license says commercial license required
- 快照位置：`raw/repos/_snapshots/jc2255-log-collect-ai-analytics-3a960f4e7aa23a2558df0b7eea813b656ecb3166.zip`
- 快照 SHA256：`05B72B98049CCF4B2908974F1EE4FE27DA8643EAFF2FD2F8BBF4188B5057BDB5`
- 采集方式：GitHub public API metadata + GitHub zipball snapshot + local file inspection

## Intake Boundary

```yaml
processing_tier: heavy
knowledge_status: raw
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
promotion_gate: none
action_basis_allowed: false
truth_mutation_allowed: false
```

Source records provide provenance and findability. They must not carry adopt/reject verdicts, truth scores, project borrowing conclusions, or action basis.

## Source / Code Anchors

| Anchor | What exists | Why it matters | Boundary |
|---|---|---|---|
| `README.md:16` | Commercial-use warning | License and use boundary | Source hygiene |
| `LICENSE:1-34` | Commercial license, no copy/modify/distribute/reverse engineering without permission | Must not reuse code/binaries directly | Legal boundary |
| `README.md:44-55` | Feature table: collection, API push, Kafka/ES transport, KQL, AI alert, alert history, RBAC, backup, AI agent, license | Whole-system surface | Candidate architecture |
| `README.md:111-147` | Architecture: log sources -> logcollect/API -> apiserver -> Kafka -> logtransfer -> Elasticsearch -> admin/web -> AI Scanner | End-to-end event pipeline | Candidate observability reference |
| `README.md:210-222` | HA details: Redis, distributed lock, leader election, Casbin sync, Kafka, ES, Nginx, app horizontal scaling | Production operations shape | P2 reference |
| `README.md:523-535` | Collection tasks: agent binding, log store, glob path, parse mode, multiline merge, 60s task pull | Dynamic capture task pattern | Candidate operations reference |
| `README.md:539-580` | Direct log push API with optional/generated `X-Trace-Id`, batch logs, appended metadata | Traceable event ingress | Strong P1 |
| `README.md:766-804` | AI alert configuration: threshold, keywords, OpenAI-compatible LLM, silence period, notification channels | Rule prefilter + LLM diagnosis | Strong P1 with risk |
| `README.md:806-815` | Agent offline notification: 3-minute heartbeat timeout, alert history, email | Tool/source connector health pattern | P2 |
| `README.md:900-929` | Troubleshooting by `trace_id` through apiserver, Kafka/logtransfer, ES | Debuggability chain | Strong P1 |
| `README.md:963-985` | Changelog: trace_id, visible flush logs, HA, leader election, alert history, AI alerts | Confirms design evolution | Candidate evidence |
| `README.md:843-895` | Declared source tree with `cmd/`, `internal/`, `web/src` | Useful intended architecture | Caveat: directories absent in snapshot |
| `Makefile:11-38` | Build targets reference `./cmd/*` | Shows expected source layout | Caveat: source directories absent |
| zip listing | No `cmd/`, `internal/`, `pkg`, or `web/src` in extracted snapshot | Source code incomplete in public snapshot | Direct reuse blocked |
| `deploy/mysql/init.sql:50-64` | `alert_histories` stores content, raw logs, root cause, resolution, category | AI diagnosis plus raw sample history | Strong P1 |
| `deploy/mysql/init.sql:247-271` | `log_stores` includes API key, Kafka topic, retention/OSS fields, AI alert enabled/config | Logstore as scoped event bucket | Candidate schema reference |
| `deploy/mysql/init.sql:454-472` | `ai_conversations` and `ai_messages`, roles user/assistant/tool, tool calls, export data | AI-agent conversation/event trace | P2 with risk |
| `configs/admin-docker.yaml:59-65` | AI provider/API key/base URL/model/max_tokens/temperature | OpenAI-compatible provider config | Risk: secret handling |
| `configs/syslog.yaml:1-22` | Syslog to API server with route rules by match -> API key | Routing external log sources into stores | Candidate source routing |
| `deploy/nginx.conf:16-34` | exact `/api/v1/log/push` route separated from admin API | Ingress separation | P1 boundary pattern |
| `deploy/ha/nginx-ha.conf:31-55` | HA upstream for apiserver with retry/failover | Resilient ingestion | P2 |
| `exports/export_3_1779784623.jsonl` | Example exported log records with `_trace_id`, `_source_ip`, `_store_name`, raw message and parsed fields | Concrete traceable raw event shape | Candidate data shape |

## Source Hygiene Notes

- Public snapshot includes large release binaries and built frontend assets, but not the expected Go/Vue source directories named in README/Makefile.
- License is commercial/proprietary. Do not copy, modify, distribute, reverse engineer, or directly reuse code/binaries without authorization.
- Config examples include placeholder/default secrets such as `lca2024`, `sk-XXX`, and `lca-secret-key-change-in-production`; these are source-hygiene signals, not implementation recommendations.
- The AI diagnosis logic is not inspectable from source in this snapshot, so prompt quality and tool-safety cannot be verified.
- `AI智能体` is mentioned and database rows for AI conversations/messages exist, but agent execution boundaries are not auditable from public source.

## 初步看点

- It demonstrates an event/log observability loop, not a knowledge-review system.
- The strongest transferable pattern is traceable event ingress: `X-Trace-Id` moves through response body, headers, Kafka, and ES.
- Alert history keeps raw triggering logs plus AI diagnosis fields, which maps well to VAKS "AI output must remain drilldown-able to source material".
- Rule prefilter plus LLM deep analysis is a useful staged triage pattern, as long as LLM output stays diagnostic.
- Agent heartbeat/offline alerts suggest a future VAKS connector/tool health ledger.

## 明显疑点

- Source code is incomplete in the public snapshot.
- Commercial license blocks direct reuse.
- AI diagnosis can hallucinate root cause if not tied to raw events and deterministic checks.
- Logs may contain sensitive data; VAKS must treat event logs as privacy-sensitive operational records.
- Kafka/ES/HA stack is likely overkill for current VAKS; the borrow should be a lightweight event ledger first.

## 可抽取 Candidate Points

- `trace_id_as_query_run_event_spine`
- `raw_sample_plus_ai_diagnosis_history`
- `rule_prefilter_then_llm_triage`
- `event_log_not_truth`
- `connector_heartbeat_and_offline_alert`
- `event_store_scope_bucket`
- `debug_chain_before_action_change`

## 当前处理等级

```text
heavy
```

升级为主线设计或 action-facing 支持的条件：

- Must pass VAKS review gate for any schema/mainline change.
- Must keep logs, alerts, LLM diagnostics, dashboards, and metrics as diagnostic or review-input only.
- Must design privacy/redaction and retention boundaries before any real event capture.
- Must avoid direct code/binary reuse due to license and incomplete source.

## 下一步

- 已生成候选蒸馏：`outputs/review/2026-06-07-jc2255-log-collect-ai-analytics-candidate-distillation.md`
- 已生成架构复盘：`wiki/summaries/2026-06-07-jc2255-log-collect-ai-analytics-architecture-review.md`
- 已生成 VAKS 项目 overlay：`outputs/review/project_overlays/VAKS/VAKS-jc2255-log-collect-ai-analytics-2026-06-07.md`
