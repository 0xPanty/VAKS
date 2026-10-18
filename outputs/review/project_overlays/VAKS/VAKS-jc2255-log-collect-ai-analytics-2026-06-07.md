---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: VAKS
target_ref: outputs/review/2026-06-07-jc2255-log-collect-ai-analytics-candidate-distillation.md
target_selector: "LCA as VAKS observability and use-ledger reference"
target_hint: "query-run / feedback-ledger / use-ledger / action-debug / tool-health / source-sync-monitoring"
project_borrow_scope:
  - "Borrow trace_id-centered event spine for query-run, source-intake, review, sync, action, and feedback."
  - "Borrow diagnostic history shape: raw trigger sample + AI diagnosis + root cause + resolution + category + related history."
  - "Borrow rule prefilter before LLM diagnosis, with silence/noise control."
  - "Borrow debug-chain discipline: locate which stage failed before changing knowledge/action records."
  - "Borrow connector heartbeat/offline alert as future source/tool health model."
  - "Borrow event buckets with retention/export/RBAC as workbench references, not truth structures."
project_non_borrow_scope:
  - "For VAKS, do not borrow logs, alert counts, LLM diagnosis, dashboard status, or exported samples as truth confidence or reviewed evidence."
  - "For VAKS, do not let feedback/use logs directly mutate reviewed knowledge, source reliability, or reviewed relations."
  - "For VAKS, do not copy or fork commercial/proprietary code or binaries."
  - "For VAKS, do not borrow Kafka/Elasticsearch/HA infrastructure before a lightweight event ledger proves useful."
  - "For VAKS, do not store private prompts, local paths, API keys, source text, or action logs without redaction and retention rules."
  - "For VAKS, do not enable AI-agent task execution without explicit tool-safety and user authorization."
project_reopen_trigger:
  - "Reopen when VAKS designs query-run traceability or runtime event ledger."
  - "Reopen when VAKS implements feedback/use-ledger automation."
  - "Reopen when VAKS adds source-sync/hash monitoring or tool/connector health."
  - "Reopen when VAKS builds a workbench dashboard for diagnostic events."
  - "Reopen when action-facing workflows need traceable debug logs."
confirmation_basis: "User explicitly requested deep distillation and said this repository is very compatible with VAKS."
last_checked_at: 2026-06-07
expires_at:
borrow_value: strong
borrow_order:
  - "P1: trace_id event spine"
  - "P1: raw sample + AI diagnosis + root cause + resolution + category"
  - "P1: rule prefilter before LLM diagnostic"
  - "P1: debug chain before action/truth changes"
  - "P2: connector heartbeat and offline alerts"
  - "P2: event buckets with retention/export/RBAC"
  - "P3: Kafka/ES/HA stack and commercial packaging"
avoid:
  - "logs as truth"
  - "AI diagnosis as review"
  - "dashboard counts as authority"
  - "direct code/binary reuse"
  - "unredacted private event storage"
  - "unsafe AI-agent task execution"
---

# Project Overlay: VAKS -> log-collect-ai-analytics

## Boundary

This is a VAKS-scoped borrowing sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern. It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-07-jc2255-log-collect-ai-analytics-candidate-distillation.md
source_ref: raw/repos/2026-06-07-jc2255-log-collect-ai-analytics-source.md
snapshot_ref: raw/repos/_snapshots/jc2255-log-collect-ai-analytics-3a960f4e7aa23a2558df0b7eea813b656ecb3166.zip
target_hint: query-run / feedback-ledger / use-ledger / action-debug / tool-health / source-sync-monitoring
```

## Project Borrow Scope

For VAKS, borrow this repository as an observability and use-ledger reference:

1. `trace_id_event_spine`: every important source/query/review/action/feedback run should be traceable.
2. `diagnostic_event_record`: keep raw trigger sample, AI diagnosis, root cause, resolution, category, severity, and related history together.
3. `rule_then_llm`: deterministic rules and thresholds first; LLM only diagnoses events that pass the trigger.
4. `debug_chain_first`: before changing knowledge/action records, identify which processing stage failed.
5. `connector_health`: future source fetchers, sync tools, transcription tools, and agents can report heartbeat/degraded/offline.
6. `event_bucket`: operational events can be scoped by event kind, project, privacy class, retention, and export policy.

Best one-line borrowing:

```text
给 VAKS 装一套轻量“黑匣子”：记录系统怎么用、哪里坏、为什么坏，但不让日志替我们判定真伪。
```

## Project Non-Borrow Scope

For VAKS, do not currently borrow:

- logs as truth confidence.
- AI diagnosis as reviewed knowledge or evidence support.
- alert severity as action readiness.
- dashboard counts as authority.
- user feedback as source reliability mutation.
- direct code/binary reuse due to commercial license and incomplete source.
- Kafka/Elasticsearch/HA stack as first implementation.
- unredacted event capture of private prompts, source text, local paths, API keys, or action outputs.
- AI-agent command/task execution without explicit tool-safety gate.

Plain-language warning:

```text
这个库能教我们怎么观察系统。
它不能替我们判断系统说的东西是真的。
```

## Reopen Trigger

Reopen this overlay when VAKS is working on:

- query-run `trace_id` fields.
- Feedback Ledger automation.
- Use Ledger / decision outcome calibration.
- source-intake runtime monitoring.
- Obsidian sync/hash mismatch diagnostics.
- tool/connector heartbeat and health status.
- action-facing debug trail.
- diagnostic workbench/dashboard.

## Confirmation

```yaml
confirmation_basis: "User explicitly requested deep distillation and said this repository is very compatible with VAKS."
last_checked_at: 2026-06-07
expires_at:
```

## Borrow Gradient

```yaml
borrow_value: strong
P1:
  - trace_id event spine
  - raw sample plus AI diagnosis history
  - root cause / resolution / category fields
  - rule prefilter before LLM
  - trace-based troubleshooting chain
P2:
  - connector heartbeat and offline events
  - event bucket retention and export
  - RBAC/privacy-aware diagnostic workbench
  - alert silence/noise control
P3:
  - Kafka/ES/Nginx HA production stack
  - commercial license machinery
  - release binary packaging
avoid:
  - logs as truth
  - AI diagnosis as review
  - dashboard count as authority
  - feedback as source reliability mutation
  - direct code/binary reuse
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
