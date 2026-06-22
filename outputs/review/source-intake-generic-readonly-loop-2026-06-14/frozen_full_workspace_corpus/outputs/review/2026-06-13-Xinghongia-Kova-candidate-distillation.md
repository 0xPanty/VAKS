---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
source_ref: raw/repos/2026-06-13-Xinghongia-Kova-source.md
derived_from:
  - github:Xinghongia/Kova@8c440483cc5af9f1915fc8d4e2fcd82c3edc9a05
  - raw/repos/_snapshots/2026-06-13-Xinghongia-Kova-8c440483-source.zip
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
borrow_value: strong
borrow_order:
  - "P1: quick capture hotkey + cursor popup + always-on-top local intake surface"
  - "P1: visible AI tool operation stream with tool_call/tool_done/data_changed events"
  - "P2: OpenAI-compatible tool schema for candidate note operations, only behind quarantine and approval"
  - "P2: local SQLite plus backup/restore pattern for a future sidecar app, not as truth source"
  - "P3: conversation summary and max-context controls as activation hygiene inspiration"
avoid:
  - "Do not let AI tools directly mutate reviewed knowledge or relations."
  - "Do not replace Markdown/Obsidian vault source of truth with SQLite app state."
  - "Do not store API keys casually or expose broad file commands to agent paths."
  - "Do not treat stream events, summaries, or tool success as evidence support."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "building a VAKS local capture client, sidecar UI, or agent gateway approval flow"
  support_when: "discussing quick capture, local-first note UX, AI tool operation UI, backup/restore, or desktop shell patterns"
  risk_when: "an agent or plugin is allowed to write, move, delete, export, or rewrite vault content"
  cold_references:
    - raw/repos/2026-06-13-Xinghongia-Kova-source.md
    - raw/repos/_snapshots/2026-06-13-Xinghongia-Kova-8c440483-source.zip
routing_hint:
  - capture_provenance
  - agent_gateway
  - local_first_client
  - dev_context_support
  - risk_agent_write_boundary
possible_project_refs:
  - VAKS
point_anchor_refs:
  - raw/repos/2026-06-13-Xinghongia-Kova-source.md#source-code-anchors
tags:
  - candidate
  - provisional
  - kova
  - local-first-notes-client
  - quick-capture-hotkey
  - ai-tool-operation-layer
  - agent-gateway
  - tauri
  - sqlite
  - backup-restore
  - risk-direct-ai-mutation
  - candidate-only
---

# Candidate Distillation: Xinghongia/Kova

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 说人话结论

Kova 不是我们的同类“可信知识系统”。它更像一个本地 AI 笔记小客户端：热键快速记、SQLite 本地存、AI 可以直接帮你查/改/建/删笔记。

对 VAKS 来说，它最值得借的是入口体验和 agent 操作可视化，不是知识判断逻辑。

一句话：可以借它的“好用入口”和“AI 工具层界面”，不能借它的“AI 直接改库就是完成任务”。

## Source

```yaml
derived_from:
  - raw/repos/2026-06-13-Xinghongia-Kova-source.md
  - raw/repos/_snapshots/2026-06-13-Xinghongia-Kova-8c440483-source.zip
checked_commit: 8c440483cc5af9f1915fc8d4e2fcd82c3edc9a05
```

## Candidate Points

### 1. Quick Capture 可以比我们现在更顺手

Kova 的 quick note 不是普通编辑器页，而是一个全局热键触发、贴近鼠标位置、always-on-top、轻量保存的捕获面。

可借鉴点：

- `Ctrl+Shift+N` 或用户自定义快捷键。
- 鼠标附近弹出，不强制切换主窗口。
- 写入模式 / 浏览模式切换。
- `Ctrl+Enter` 快速保存，`Esc` 快速关闭。
- 保存后发事件刷新主界面。

VAKS 对应层：

```text
Capture / Provenance
-> Candidate Comprehension
```

边界：

```text
快速捕获只能进 raw/candidate，不直接进 reviewed truth。
```

### 2. AI 工具层能提高操作效率，但必须隔离

Kova 的 AI 不只是聊天，它有 `create_note`、`search_notes`、`update_note`、`delete_note`、`batch_create_notes` 等工具。

可借鉴点：

- AI 操作不是靠自然语言“建议”，而是有明确 tool schema。
- 工具执行有 `tool_call`、`tool_done`、`data_changed` 事件。
- UI 可以展示 AI 做了什么，并刷新数据。
- 工具循环有最大 10 次限制。

VAKS 对应层：

```text
Agent Gateway
-> Candidate write
-> Review Queue
-> Approval / action receipt
```

边界：

```text
Kova 的直接 mutation 对普通笔记 app 是爽点；
对 VAKS 是必须加闸的风险点。
```

### 3. Stream event 是 agent 操作可见性的好骨架

Kova 的流式 AI 会把 thinking、内容 chunk、tool call、tool done、data changed 这类状态发回前端。

可借鉴点：

- agent 不应该黑箱改数据。
- 每次工具调用都应在 UI 和日志里可见。
- 数据变化事件可以触发局部刷新。

VAKS 最小融合版：

```text
tool_intent
-> diff_preview
-> user_approval
-> candidate_write
-> receipt/log
-> refresh
```

### 4. SQLite + backup/restore 适合 sidecar，不适合真源

Kova 用 SQLite 保存 notes/folders/conversations/messages，并支持 ZIP 备份恢复。

可借鉴点：

- 本地 app 的状态、UI 缓存、临时队列、对话消息、设置，适合 SQLite。
- ZIP backup/restore 是很现实的本地工具设计。
- 自定义数据目录对个人工具很友好。

VAKS 边界：

```text
Markdown vault = source of truth
SQLite/cache/index = derived sidecar
backup/restore = tool resilience, not truth authority
```

### 5. 对话摘要和 max context 是 activation hygiene，不是证据

Kova 支持 conversation summary、max_context_messages、enable_thinking。

可借鉴点：

- 控制上下文长度，避免无限聊天历史。
- 摘要可帮助继续对话。

VAKS 边界：

```text
summary = activation / orientation
not evidence support
not reviewed relation
not confidence
```

### 6. Import/export 是互操作入口，但不能省略 provenance

Kova 支持 Markdown/HTML/TXT 导入导出。

可借鉴点：

- 轻量文件导入和导出是个人知识工具必备。
- Markdown 导出可以让用户逃离锁定。

VAKS 边界：

```text
imported file needs source identity / capture trace
export is convenience, not review
HTML import should use robust parser / sanitizer
```

### 7. Kova 是强风险样本：agent 权限不要一上来放太大

已读源码里能看到：

- AI 工具能更新/删除/批量删除笔记。
- Tauri commands 暴露文件 read/write/copy/download。
- API key 存在本地 config JSON。
- Tauri config 里 CSP 为 null。

这不等于 Kova “不好”。它的定位是个人本地 app，很多设计换来的是轻便。

但对 VAKS，这些是很好的风险提示：

```text
agent write permissions must be path-scoped
destructive actions need confirmation
reviewed truth must not be directly writable
secrets need proper storage boundary
```

## 标签与量化

- domain: local_first_notes / ai_note_client / desktop_pkm
- problem: quick_capture / ai_operated_notes / local_storage / note_app_resilience
- pattern: hotkey_capture_surface / ai_tool_operation_stream / local_sidecar_db / zip_backup_restore
- risk_pattern: direct_ai_mutation / plaintext_secret_storage / broad_file_command_surface
- maturity: experimental
- complexity: medium
- problem_fit: 4
- reuse_value: 4
- implementation_cost: 3
- integration_fit: 3
- evidence_strength: 3
- reversibility: 4

## 与 VAKS 架构的对应

| VAKS layer | Kova gives | Fit |
|---|---|---|
| Capture / Provenance | hotkey quick note, cursor popup, file import | strong for capture UX; provenance missing |
| Candidate Comprehension | AI can draft/create/update notes | useful only as candidate write |
| Knowledge Calibration | no point collision or contradiction pressure | absent |
| Review / Consolidation | no evidence-aware review gate | absent |
| Association / Reviewed Relations | folders/tags/search only | weak; not reviewed relation |
| Activation / Dev Context | conversation summary and recent context | useful as activation intuition |
| Context Pack | no coverage-aware context pack | absent |
| Decision / Action | AI tools directly act | strong UX, high VAKS risk |
| Use Ledger / Feedback | UI refresh events, chat history | not feedback ledger |
| Risk / Inhibition | direct mutation and broad file commands expose boundary risk | strong negative lesson |

## Open Questions

- Kova 是否有隐藏的 runtime permission/confirmation 逻辑没有被本次源码扫到？
- Release 包和 README 的大小描述差异是口径问题还是文档过期？
- API key 是否应迁到 OS secret store？
- 如果我们借 quick capture，最小实现是 Obsidian 插件、Tauri sidecar，还是只做脚本/全局热键？
- 如果我们借 AI tool layer，审批粒度应该是每条工具调用、每批 diff，还是按风险等级？

## Routing Hint

这份材料适合进入：

- local capture client 设计讨论。
- agent gateway / write boundary 设计讨论。
- VAKS quick intake UX 候选。
- sidecar cache / local app shell 候选。
- agent permissions 风险样本。

不适合进入：

- reviewed claim。
- formal pattern。
- action basis。
- truth confidence 更新。

## Forbidden

```text
project_borrow_scope
project_non_borrow_scope
decision outcome
formal pattern
action basis
truth confidence
```

项目借鉴范围写在单独的 project overlay，避免 candidate distillation 像项目决策。
