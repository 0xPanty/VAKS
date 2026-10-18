---
type: project_overlay
record_kind: project_overlay
status: candidate
title: "Project lens: the-book-of-secret-knowledge for VAKS retrieval/source ingest"
created_at: "2026-06-11"
created_by: Codex
knowledge_status: candidate
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
action_basis_allowed: false
truth_mutation_allowed: false
derived_from:
  - raw/repos/2026-06-11-trimstray-the-book-of-secret-knowledge-source.md
  - outputs/review/2026-06-11-trimstray-the-book-of-secret-knowledge-candidate-distillation.md
project_ref: verified-action-knowledge-system
target_hint:
  - retrieval-layer
  - source-ingest
  - link-health
  - command-risk-gate
borrow_value: medium
borrow_order: P2
tags:
  - project-overlay
  - candidate-only
  - retrieval-layer
  - source-ingest
---

# Project Lens：the-book-of-secret-knowledge 对 VAKS 的局部借鉴

## 一句话

这个库对 VAKS 当前最有用的不是安全资源本身，而是一个产品/检索层模式：

```text
大规模外部资源，先做可浏览、可检索、可维护的候选索引。
不要一上来假装每条都 reviewed。
```

## Project Borrow Scope

```yaml
project_borrow_scope:
  - curated reference index for discovery
  - source hygiene fields for link rot and temporary unavailability
  - category/facet scaffold for retrieval workbench
  - RSS/Atom style freshness monitor
  - command-like-result warning and action gate
```

## Project Non-Borrow Scope

```yaml
project_non_borrow_scope:
  - giant README as main VAKS structure
  - GitHub stars as trust
  - awesome-list descriptions as evidence support
  - shell one-liners as executable recommendations
  - security tool listing as endorsement
```

## 对当前检索层开发区的意义

可以放进 `outputs/review/vaks-retrieval-layer-design-2026-06-11/` 的参考池，但不必现在改那边文件。

最小吸收方式：

```text
retrieval result card:
  if source_family == curated-resource-index:
    badge: DISCOVERY_ONLY
    warning: not evidence support

  if result_kind == command_or_one_liner:
    badge: COMMAND_CANDIDATE
    warning: requires environment/risk/rollback gate

  if link_status == temporary_unavailable:
    badge: LINK_UNSTABLE
    warning: source hygiene issue, not truth issue
```

## 未来可验证的小实验

- 建一个 sandbox curated index manifest，导入 20 条外部资源。
- 只做 category、source URL、短描述、link_status、risk_flag。
- 测试检索层能否把 discovery-only 和 evidence-support 结果分开显示。
- 测试 command-like 结果是否能被 action gateway 拦住。

## 边界

```text
overlay = active project context only
not reviewed knowledge
not source reliability judgment
not adoption decision
not action basis
```
