---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: heavy
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
project_id: verified-action-knowledge-system
target_ref: raw/repos/2026-06-07-crosstalk-solutions-project-nomad-source.md
target_selector: checked_commit:d5f7c3f615c92c07b798b6512b2483fd9d64a89d
target_hint: "Use as a VAKS offline-content, ingestion-state, RAG-warning, and operator-surface reference, not as truth architecture."
tagging_decision: tagged
tag_level: medium-borrow
tag_level_reason: "Useful VAKS references exist, but the project is an offline appliance with security assumptions VAKS should not inherit."
project_borrow_scope:
  - tiered offline content manifest with version, URL, size, recommended, and includesTier
  - source package / local library status as activation and coverage hints
  - KB ingestion state separated from vector-store chunk presence
  - zero-chunk, partial-stall, unknown-estimate, and failed-check warning surfaces
  - job health and operator cockpit for long-running local tasks
  - RAG retrieval as activation/context preparation only
project_non_borrow_scope:
  - content package inclusion as source reliability
  - Qdrant chunks or RAG scores as evidence support
  - benchmark score as action readiness
  - unauthenticated LAN control surface
  - Docker socket, host filesystem mount, or updater sidecar posture as VAKS default
  - full offline appliance dashboard in VAKS core
project_reopen_trigger:
  - "VAKS starts an offline source package or curated source bundle lane."
  - "VAKS adds ingestion-state tracking beyond simple raw/candidate files."
  - "VAKS builds maintenance lint for extraction/indexing failure."
  - "VAKS builds a local operator dashboard for video intake, source sync, context-pack generation, or agent/tool runs."
  - "VAKS threat-models future local agent/tool control surfaces."
confirmation_basis:
  - user explicitly requested strong distillation and conditional tagging
  - source card, snapshot, candidate distillation, architecture review, and project overlay created
  - source/code anchors inspected from checked repository snapshot
  - no runtime execution; no promotion to reviewed knowledge
last_checked_at: 2026-06-07
expires_at: 2026-07-07
borrow_value: medium
borrow_order:
  - "P1: tiered content manifest and local source package status"
  - "P1: ingestion state row separate from vector chunks"
  - "P1: maintenance warnings for silent extraction/indexing failures"
  - "P2: job health and operator status model"
  - "P2: RAG activation with budget/rerank/diversity, not evidence support"
  - "P3: full local appliance stack as cold reference only"
avoid:
  - "Do not promote this overlay into reviewed knowledge."
  - "Do not use RAG score, installed package state, benchmark score, or collection tier as action basis."
  - "Do not inherit no-auth, Docker socket, host mount, or sidecar update privileges."
  - "Do not make VAKS a full Project N.O.M.A.D.-style appliance unless a later product decision asks for it."
tags:
  - VAKS
  - project-overlay
  - project-nomad
  - medium-borrow
  - offline-knowledge-appliance
  - local-first
  - curated-content-manifest
  - kiwix-zim
  - rag-ingest-guardrails
  - operator-cockpit
  - maintenance-diagnostics
  - activation-only
  - security-risk
  - candidate-only
---

# VAKS Project Overlay: Project N.O.M.A.D.

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: raw/repos/2026-06-07-crosstalk-solutions-project-nomad-source.md
target_selector: checked_commit:d5f7c3f615c92c07b798b6512b2483fd9d64a89d
target_hint: offline-content-package / ingestion-state / maintenance-diagnostics / operator-cockpit
```

## 标签等级

```yaml
tagging_decision: tagged
tag_level: medium-borrow
```

人话：

```text
有帮助，所以打。
但不强打，因为它不是 VAKS 的真值系统，而且安全边界不能照搬。
```

## Project Borrow Scope

VAKS 当前值得借：

1. **离线内容包 manifest**：资源要有 id、version、URL、size、description、tier、recommended、includesTier。
2. **安装/下载/本地可用状态**：package status 可以作为 activation/coverage hint。
3. **摄取状态独立于向量库**：state row 比“Qdrant 里有没有 chunk”更适合作为 process authority。
4. **摄取失败显性化**：zero chunks、partial stall、unknown estimates、检查失败都应该被看见。
5. **operator cockpit**：长任务需要 health、queue、warning、retry、update status。
6. **RAG 只作 activation**：query rewrite、rerank、source diversity、context budget 可以借；truth support 不能借。

## Project Non-Borrow Scope

VAKS 当前不要误借：

- 不要把 package tier / recommended / installed state 当成 source reliability。
- 不要把 Qdrant chunks、RAG score、Context rank 当成 evidence support。
- 不要把 benchmark score 当成 action readiness。
- 不要把 no-auth LAN UI 作为 VAKS 默认。
- 不要把 Docker socket、host filesystem mount、updater sidecar 作为 VAKS 默认权限模型。
- 不要为了这个源把 VAKS 核心做成完整 appliance dashboard。

## Reopen Trigger

重新打开这条 overlay 的条件：

- VAKS 要做离线 source package / curated source bundle。
- VAKS 要做 ingestion state registry。
- VAKS 要做 extraction/indexing maintenance lint。
- VAKS 要做本地 operator dashboard。
- VAKS 要给 agent/tool control surface 做 threat model。

## Confirmation

```yaml
confirmation_basis:
  - user_requested: "强蒸馏 有对vaks帮助的就打 没有就不打"
  - checked_commit: d5f7c3f615c92c07b798b6512b2483fd9d64a89d
  - artifact_paths:
      - raw/repos/2026-06-07-crosstalk-solutions-project-nomad-source.md
      - outputs/review/2026-06-07-crosstalk-solutions-project-nomad-candidate-distillation.md
      - wiki/summaries/2026-06-07-crosstalk-solutions-project-nomad-architecture-review.md
      - outputs/review/project_overlays/VAKS-project-nomad-2026-06-07.md
      - raw/repos/_snapshots/Crosstalk-Solutions-project-nomad-d5f7c3f615c92c07b798b6512b2483fd9d64a89d.zip
  - runtime_executed: false
last_checked_at: 2026-06-07
expires_at: 2026-07-07
```

## 人话结论

打标签，等级是 `medium-borrow`。

最值得 VAKS 记住的是：

```text
离线知识包要有 manifest 和版本。
摄取状态要和向量库状态分开。
大文件零 chunk 这种假成功要报警。
RAG 是激活材料，不是证据。
本地操作面板有用，但权限边界要比 NOMAD 更严。
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
security approval
strong-borrow
```

