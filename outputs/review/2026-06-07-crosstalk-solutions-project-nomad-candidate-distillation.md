---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
  - raw/repos/2026-06-07-crosstalk-solutions-project-nomad-source.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - offline-content-packaging
  - source-intake
  - retrieval-activation
  - operator-cockpit
  - maintenance-diagnostics
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/Crosstalk-Solutions-project-nomad-d5f7c3f615c92c07b798b6512b2483fd9d64a89d.zip
    selector_type: source_code
    selector_value: README.md:17-53
  - snapshot_ref: raw/repos/_snapshots/Crosstalk-Solutions-project-nomad-d5f7c3f615c92c07b798b6512b2483fd9d64a89d.zip
    selector_type: source_code
    selector_value: collections/kiwix-categories.json:1-75
  - snapshot_ref: raw/repos/_snapshots/Crosstalk-Solutions-project-nomad-d5f7c3f615c92c07b798b6512b2483fd9d64a89d.zip
    selector_type: source_code
    selector_value: admin/app/utils/kb_ingest_decision.ts:3-70
  - snapshot_ref: raw/repos/_snapshots/Crosstalk-Solutions-project-nomad-d5f7c3f615c92c07b798b6512b2483fd9d64a89d.zip
    selector_type: source_code
    selector_value: admin/app/utils/kb_warning_decision.ts:1-70
  - snapshot_ref: raw/repos/_snapshots/Crosstalk-Solutions-project-nomad-d5f7c3f615c92c07b798b6512b2483fd9d64a89d.zip
    selector_type: source_code
    selector_value: install/management_compose.yaml:11-117
tagging_decision: tagged
tag_level: medium-borrow
tag_level_reason: "Concrete offline-content, ingestion-state, warning, and operator-surface patterns help VAKS, but the project scope and security posture do not justify strong-borrow."
borrow_value: medium
borrow_order:
  - "P1: tiered offline content manifest with version, URL, size, recommended, and includesTier"
  - "P1: KB ingestion state row separate from vector-store chunk presence"
  - "P1: conditional ingestion warnings for zero chunks, partial stalls, and computation failure"
  - "P2: pre-ingest cost estimates and unknown-file disclosure"
  - "P2: local-first operator surface for health, update, queue, and service status"
  - "P2: RAG context injection with budget, reranking, and source diversity as activation support"
  - "P3: broader offline appliance stack as cold reference"
avoid:
  - "Do not treat Kiwix inclusion, package tier, or installed status as source reliability."
  - "Do not treat Qdrant chunks, RAG scores, or benchmark results as evidence support."
  - "Do not copy the unauthenticated LAN/Docker-socket posture into VAKS."
  - "Do not expose VAKS tool/agent surfaces directly to network without authentication and least privilege."
  - "Do not add a full appliance dashboard to VAKS core before an operator need exists."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "approved VAKS task implements offline source packages, ingestion-state monitoring, or operator health surfaces."
  support_when: "designing source intake cost estimates, retrieval activation, source package selectors, or maintenance lint."
  risk_when: "Docker socket access, host filesystem mounts, unauthenticated LAN exposure, updater sidecars, or RAG-as-truth confusion."
  cold_references:
    - raw/repos/2026-06-07-crosstalk-solutions-project-nomad-source.md
    - raw/repos/_snapshots/Crosstalk-Solutions-project-nomad-d5f7c3f615c92c07b798b6512b2483fd9d64a89d.zip
tags:
  - candidate
  - provisional
  - project-nomad
  - medium-borrow
  - offline-knowledge-appliance
  - local-first
  - curated-content-manifest
  - kiwix-zim
  - rag-ingest-guardrails
  - qdrant
  - operator-cockpit
  - maintenance-diagnostics
  - security-risk
  - candidate-only
---

# Project N.O.M.A.D. Candidate Distillation

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## Source

```yaml
derived_from:
  - raw/repos/2026-06-07-crosstalk-solutions-project-nomad-source.md
checked_commit: d5f7c3f615c92c07b798b6512b2483fd9d64a89d
snapshot: raw/repos/_snapshots/Crosstalk-Solutions-project-nomad-d5f7c3f615c92c07b798b6512b2483fd9d64a89d.zip
snapshot_sha256: A59965A0C7AA3D7CC3D4CC61212E657A1C270900F08F1395894103C864CD198E
```

## 人话压缩

Project N.O.M.A.D. 对 VAKS 有帮助，但不是“强采纳”。

```text
它强在离线知识包、摄取状态、RAG 摄取告警、操作面板。
它弱在安全边界：无认证、Docker socket、host mount、updater sidecar 都不能照搬。
```

所以标签等级：

```text
tag_level: medium-borrow
```

这表示：

```text
值得进入 VAKS 候选参考。
值得在 source intake / activation / maintenance lint 里反复回看。
不值得直接写进主干决策或 truth layer。
```

## Candidate Points

### 1. `tiered-offline-content-manifest`

候选结论：VAKS 如果未来支持离线资料包或可选 source bundle，不应只维护一串下载链接。更好的 shape 是给每个资源记录 id、version、title、description、url、size、tier、recommended、includesTier，并能计算 installed / downloading / missing 状态。

锚点：

- `collections/wikipedia.json:1-51`
- `collections/kiwix-categories.json:1-75`
- `admin/app/services/collection_manifest_service.ts:27-91`
- `admin/app/services/collection_manifest_service.ts:193-245`

对 VAKS 的适配：

- 用作 `source-package manifest` 或 `offline context pack manifest` 的候选形状。
- `size_mb` 和 `version` 可用于下载成本、时效、适用范围提示。
- `recommended` 和 `includesTier` 只能表示选择/覆盖关系，不能表示可信度。

边界：

```text
included in package != reliable
recommended by manifest != reviewed
installed locally != evidence support
```

### 2. `kb-ingest-state-is-separate-from-vector-presence`

候选结论：VAKS 的摄取/索引状态应独立于向量库或检索库里“有没有 chunk”。Project N.O.M.A.D. 用 per-file state row 作为 authoritative process state，用 Qdrant chunk presence 作为 corroborating evidence，这个边界对 VAKS 很有用。

锚点：

- `admin/app/utils/kb_ingest_decision.ts:3-70`
- `admin/app/services/rag_service.ts:1513-1648`
- `admin/app/services/rag_service.ts:1076-1130`

对 VAKS 的适配：

- `raw captured`、`extracted`、`indexed`、`pending_decision`、`browse_only`、`failed`、`stalled` 这类状态应属于 processing layer。
- 向量索引存在只能说明“曾经进入检索层”，不能说明内容完整、可信或已审查。
- 手动模式可以把“看到文件”和“自动摄取”拆开，适合高风险 source。

边界：

```text
state row = process status
vector chunk = retrieval artifact
reviewed evidence = later review result
```

### 3. `silent-ingest-failure-warning-surface`

候选结论：VAKS 应该把摄取失败和半失败显性化，尤其是大文件零 chunk、低于预期 chunk、Qdrant/DB/FS 检查失败这些“看起来成功但实际不可用”的情况。

锚点：

- `admin/app/utils/kb_warning_decision.ts:1-70`
- `admin/app/utils/kb_ratio_lookup.ts:31-97`
- `admin/app/services/rag_service.ts:1159-1235`

对 VAKS 的适配：

- 对视频、ZIM、PDF、网页快照、repo 快照都可记录 `extraction_warning`。
- `ok: false` 的检查结果不能显示成“健康”，应显示成“无法确认”。
- 估算值可用于维护 lint 和 operator warning，不能用于 truth confidence。

边界：

```text
warning = maintenance input
warning != truth judgment
no warning != evidence sufficiency
```

### 4. `local-first-operator-cockpit-with-risk`

候选结论：VAKS 未来如果有本地 agent、同步、索引、视频 intake、Obsidian sync、context-pack build 等长任务，需要一个本地 operator cockpit 显示状态、队列、健康、失败和重试。但 Project N.O.M.A.D. 的安全姿态只能当风险样本，不能照搬。

锚点：

- `README.md:17-53`
- `README.md:105-115`
- `install/management_compose.yaml:11-69`
- `install/management_compose.yaml:98-117`
- `admin/app/utils/kb_job_health.ts:1-50`

对 VAKS 的适配：

- 借“任务状态可见、健康检查、失败显式化、更新状态显式化”。
- 不借“无认证 LAN UI + Docker socket + host mount”的默认姿态。
- VAKS agent/tool 面板需要认证、最小权限、写入隔离、dry-run/confirm 边界。

边界：

```text
operator visibility is useful
operator privilege is dangerous
local-first does not mean no-auth
```

### 5. `rag-as-activation-not-evidence`

候选结论：Project N.O.M.A.D. 的 RAG pipeline 对 VAKS 的价值在 activation/context preparation，不在 truth support。它提供 query rewrite、similarity search、reranking、source diversity、model-size context budget 等机制，但这些都只能帮助“找材料/组上下文”。

锚点：

- `admin/app/services/rag_service.ts:791-929`
- `admin/app/services/rag_service.ts:945-1053`
- `admin/app/controllers/ollama_controller.ts:74-130`
- `admin/app/controllers/ollama_controller.ts:366-445`

对 VAKS 的适配：

- 可作为 context pack / activation retrieval 的候选参考。
- `score`、`rank`、`top N`、`Context 1` 都不能成为 evidence support。
- Source diversity 只能减少单源占满上下文，不代表覆盖充分。

边界：

```text
retrieval result = activation
context injection = model input
evidence support = reviewed source-span match
```

## 打标签结论

```yaml
tagging_decision: tagged
tag_level: medium-borrow
main_tags:
  - offline-knowledge-appliance
  - curated-content-manifest
  - rag-ingest-guardrails
  - operator-cockpit
  - maintenance-diagnostics
  - security-risk
```

不打 `strong-borrow` 的原因：

- 这不是 VAKS 的主问题域。
- 它的 security posture 对 VAKS 不能直接接受。
- 它的 RAG/benchmark/collection 层很容易被误读成 truth layer。
- 值得借的是几组工程局部，不是整套架构。

## Forbidden

```text
reviewed relation
truth confidence
action basis
implementation decision
security approval
offline package as trust
rag score as evidence
```

