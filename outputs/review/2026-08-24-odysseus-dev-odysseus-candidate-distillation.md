---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
source_ref: raw/repos/2026-08-24-odysseus-dev-odysseus-source.md
derived_from:
  - raw/repos/2026-08-24-odysseus-dev-odysseus-source.md
  - https://github.com/odysseus-dev/odysseus/tree/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c
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
  - source-intake-adapters
  - agent-tool-authority
  - risk-and-inhibition
  - operation-preflight
  - agent-memory-quarantine
  - self-hosted-ai-workbench
possible_project_refs:
  - verified-action-knowledge-system
source_annotation_refs:
  - outputs/review/source_annotations/2026-08-24-odysseus-dev-odysseus/odysseus-exact-action-binding-payload.md
  - outputs/review/source_annotations/2026-08-24-odysseus-dev-odysseus/odysseus-external-context-effect-gate.md
  - outputs/review/source_annotations/2026-08-24-odysseus-dev-odysseus/odysseus-auto-memory-direct-write-risk.md
point_anchor_refs:
  - snapshot_ref: https://github.com/odysseus-dev/odysseus/blob/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c/docs/agent-migration.md
    selector_type: line_range
    selector_value: "docs/agent-migration.md:14-26;166-181"
  - snapshot_ref: https://github.com/odysseus-dev/odysseus/blob/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c/src/prompt_security.py
    selector_type: line_range
    selector_value: "src/prompt_security.py:8-26;64-99"
  - snapshot_ref: https://github.com/odysseus-dev/odysseus/blob/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c/src/tool_capabilities.py
    selector_type: line_range
    selector_value: "src/tool_capabilities.py:586-662"
  - snapshot_ref: https://github.com/odysseus-dev/odysseus/blob/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c/src/tool_approvals.py
    selector_type: line_range
    selector_value: "src/tool_approvals.py:89-165;237-313;339-470"
  - snapshot_ref: https://github.com/odysseus-dev/odysseus/blob/b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c/services/memory/memory_extractor.py
    selector_type: line_range
    selector_value: "services/memory/memory_extractor.py:448-471"
borrow_value: medium
borrow_order:
  - "P1: exact-action binding and server-owned post-external-context capability gate"
  - "P1: source-neutral migration staging with archives separated from reviewable memory candidates"
  - "P2: tool visibility separated from execution authority"
  - "P3: integrated self-hosted AI workbench as a product reference only"
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "An approved task is specifically designing an agent/runtime action bridge, operation receipt, migration adapter, or memory-write quarantine."
  support_when: "Comparing agent tool gates, exact approvals, source migration, or self-hosted AI workbench boundaries."
  risk_when: "External content, model-selected tools, approval UI, auto memory, or runtime output is being treated as authority, reviewed knowledge, or action basis."
  cold_references:
    - raw/repos/2026-08-24-odysseus-dev-odysseus-source.md
avoid:
  - "Do not import auto-extracted facts directly into VAKS reviewed memory or truth-bearing notes."
  - "Do not treat an untrusted-content prompt wrapper as a deterministic security boundary by itself."
  - "Do not inherit chat-session-wide approval bypass as the default VAKS authorization scope."
  - "Do not copy the all-in-one runtime, vector rank, dashboard, or database as VAKS authority."
  - "Do not reuse or adapt AGPL-covered code without a separate license-compatibility review."
heavy_recommended: true
heavy_recommended_reason: "The repository is a large, privileged, fast-moving agent runtime whose approval, memory, security, and branch-drift questions exceed a medium static routing pass."
tags:
  - candidate
  - provisional
  - agent-runtime
  - exact-action-approval
  - memory-quarantine
  - source-intake
---

# 候选蒸馏：odysseus-dev/odysseus

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest a later Project Overlay. It is not reviewed knowledge, not a decision, not a formal pattern, not evidence support, and not action basis.

## 一句话结论

Odysseus 是一个功能很广、本机权限很高的自托管 AI 工作台。对 VAKS 最有候选价值的不是整体产品或 RAG/记忆库，而是三个可单独审视的边界机制：

```text
外部内容影响状态
-> 工具 effect 分类
-> 高影响动作暂停
-> 精确载荷的用户授权
```

另一条同样重要的反向信号是：文档中的“archive 与 memory candidate 分层”不等于运行时所有记忆路径都经过审核；当前代码仍有自动抽取后直接写入的路径。

## Source Baseline

```yaml
repository: https://github.com/odysseus-dev/odysseus
branch: dev
commit: b4d12932a953b3cdfc745b3525c7ecd5dffd8b3c
commit_time: 2026-08-20T11:06:22Z
source_status: active
github_releases_observed: 0
github_tags_observed: 0
inspection: static_only
tests_or_runtime_executed: false
```

## Candidate Points

### 1. 产品形状：一体化 AI 工作台，不是知识权威系统

仓库把聊天、Agent、模型服务、工具/MCP、深度研究、文档、邮件、笔记、任务、日历和图像功能放在同一应用中。静态结构是：

```text
FastAPI app + routes/services
-> agent/model/tool orchestration
-> SQLite + JSON + ChromaDB
-> raw HTML/CSS/ES modules
-> SearXNG / ntfy / model-provider integrations
```

这个形状可以作为工作台与运行时边界的参考，但不应被解读为 VAKS 的知识分层、评审或 action-basis 架构。

### 2. Agent 迁移的两层暂存契约

`docs/agent-migration.md` 建议先将外部 Agent 数据转换为中立 manifest，再把长篇原始资料与短事实候选分开：

```text
archive documents / conversation context
-> 保留来源，供搜索、阅读和后续抽取

memory candidates
-> 短事实/偏好
-> 先 preview/review
-> 再进入正常 memory 路径
```

这与 VAKS 的 raw/candidate 分层有表面同构性。候选用法是把它视为 Source Capture Envelope / adapter ingest 的一个外部兼容样例，而不是另造平行 schema。

### 3. 外部内容的包装与 server-owned effect gate

`src/prompt_security.py` 将网页、邮件、检索文档、工具输出、保存记忆和 skill 文本视为数据，放入 `user` role 下的明确防注入包装。`src/tool_capabilities.py` 另外维护 server-owned 运行状态：一旦不可信外部内容已影响当前 run，涉及私有数据、写入、代码执行、网络出口、外部副作用、管理变更或破坏性的工具会被另行拦截。

候选可借的是两层结构：

```text
prompt wrapper = defense in depth
deterministic effect gate = dispatch boundary
```

不可借的错误等式是：

```text
内容已被标为 untrusted
!= 安全问题已解决
!= 源内容不会影响模型
!= 运行时已隔离
```

### 4. 精确动作封印比“审批按钮”更值得研究

`src/tool_approvals.py` 不从浏览器展示字段取回权威，而是由服务端把以下内容规范化并摘要绑定：

```text
owner
session
origin run
tool + exact content
workspace
document id/version/content digest
external-context state
selected tools + continuation query
effects + result integrity
```

待审批项有 TTL，使用时重算载荷，且精确动作只能 claim 一次。这是 VAKS 未来 operation receipt/action bridge 值得做强蒸馏比较的实现候选，但它不是当前 VAKS 审批语义的自动替代。

### 5. 文档契约与自动记忆实现之间存在需要保留的张力

`services/memory/memory_extractor.py:448-471` 显示一条静态路径：抽取出的事实可以 `source="auto"` 直接加入 memory，identity 类别还会被 pin，最后保存 JSON 并写入向量索引。

这不足以说明所有记忆都无审核——上游触发、设置、权限和 UI 仍未做完整调用链审计——但它足以构成一个风险定位器：

```text
文档中有 candidate/review 语言
!= 每一条 runtime 路径都不会直写 durable memory
```

对 VAKS，这个 annotation 应进入 Risk，不应被转化为自动记忆功能。

### 6. 工具检索/可见性不等于执行权

Odysseus 可以先用向量/关键词/领域映射选择少量工具 schema 给模型，但实际调度时仍有 owner、当前请求策略、disabled tools、workspace 和 approval 约束。这个形状支持一个很小但重要的候选原则：

```text
retrieved/visible tool schema
!= authorized tool execution
```

对 VAKS 而言，这可以作为“retrieval score/routing 不产生 authority”的运行时类比，但不产生新的 truth layer。

## Candidate Routing

### P1 先看

- `exact-action-binding-payload`：精确动作、目标版本、工作区和 effect 的服务端绑定。
- `external-context-effect-gate`：外部信息影响如何从 prompt 层传到 dispatch 层。
- `agent-migration.v1`：archive 与 reviewable memory candidates 的分流。

### P2 按需展开

- 工具可见性与执行权分开。
- 审批 TTL、一次性消费、目标版本绑定。
- 默认快速分支与 curated 分支的版本/验证语义冲突。

### P3 仅作冷参考

- 一体化 AI 工作台。
- 向量工具检索、多模型适配、原生前端和 Docker 组合。
- GitHub 热度、功能表和 demo。

## Avoid / Risk

- 不把自动抽取结果直接写入 VAKS reviewed knowledge、truth confidence 或持久主记忆。
- 不把 prompt wrapper 当成 sandbox、证据支持或安全验证。
- 不默认吸收 chat-session 级广泛 bypass；未来 VAKS 优先 exact action 或严格 task scope，且在目标/载荷/作用域变化时重新授权。
- 不把工具 RAG、ChromaDB、SQLite、dashboard 或运行时状态当作 VAKS 权威层。
- 不在未做许可兼容评估时复制/改编 AGPL 代码。
- 不因官方 CI、大量测试文件或 GitHub 热度就宣称当前 commit 已在本环境中通过验证。

## Open Questions

- 精确动作摘要的字段集，如何与 VAKS 已有 operation receipt、checked body hash、intent confirmation 和 rollback 边界最小融合？
- VAKS 是否只需要借鉴“服务端精确绑定”语义，而不需要引入新的审批对象家族？
- Odysseus 的 auto-memory 路径在什么设置、权限、会话和 UI 条件下触发？是否有本次未覆盖的用户审核面？
- `dev` 与 `main` 当前已分叉，哪一个才是可用于安全/部署结论的正式基线？
- 当前 `THREAT_MODEL.md` 中的 known gaps 有多少已修复但文档未同步，有多少仍能通过其他路径触发？

## Heavy Recommendation

```yaml
heavy_recommended: true
reason:
  - privileged-agent-and-host-execution-surface
  - fast-moving-default-branch-without-tags-or-releases
  - high-value-action-gate-and-memory-boundary-candidates
  - security-and-architecture-document-drift
  - cross-module-call-chain-needed-for-safe-judgment
```

强蒸馏应聚焦：

```text
external source
-> untrusted wrapper
-> run integrity state
-> tool effect classification
-> exact approval creation/consume/claim
-> dispatch/result re-entry
```

其次才是全仓架构图、`dev`/`main` 差异和记忆完整调用链。即使后续强蒸馏，也不自动授权测试、部署或安全验证。

## Forbidden

```text
project_borrow_scope as adoption decision
source annotation as evidence support
reviewed knowledge
formal pattern
decision outcome
truth confidence
action basis
auto-memory writeback
runtime deployment inference
```

## Final Candidate Judgment

```yaml
direct_use: not_assessed_in_standard_intake
fork: not_assessed_in_standard_intake
design_only_candidate: yes
borrow_value: medium
best_use: exact-action authority, external-context tool gating, and migration-boundary comparison
not_best_use: VAKS truth architecture, default memory pipeline, or production deployment reference
```

说人话：

```text
这个仓库值得在候选层保留；整体迁移未评估，也不在本轮范围。
先留住“外部信息不授权 + 精确动作封印”，
同时把“自动记忆直写”当作 Risk 保留。
```
