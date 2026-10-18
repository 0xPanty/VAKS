---
type: library_review
record_kind: architecture_review
status: draft
knowledge_status: candidate
processing_tier: heavy
library_name: Xinghongia/Kova
repo_url: https://github.com/Xinghongia/Kova
source_url: https://github.com/Xinghongia/Kova
source_ref: raw/repos/2026-06-13-Xinghongia-Kova-source.md
checked_commit: 8c440483cc5af9f1915fc8d4e2fcd82c3edc9a05
commit_time: 2026-06-08T10:43:25Z
source_status: active
reviewed_at: 2026-06-13
domain: local_first_ai_note_client
related_projects:
  - VAKS
current_branch:
  - source-intake
  - agent-gateway
  - capture-ux
  - dev-context
extracted_patterns:
  - hotkey-cursor-quick-capture
  - visible-ai-tool-operation-stream
  - local-sidecar-sqlite-state
  - zip-backup-restore-for-local-client
  - openai-compatible-note-tool-schema
extracted_risks:
  - direct-ai-mutation-without-review-gate
  - sqlite-as-truth-source-confusion
  - plaintext-api-key-config
  - broad-tauri-file-command-surface
fusion_decision: adapt
confidence: medium
evidence_count: 18
cross_validated_with:
  - SOURCE_INTAKE.md
  - REFERENCE_REVIEW_PROTOCOL.md
  - DEV_CONTEXT.md
negative_evidence:
  - no observed tests
  - app not run locally
  - license metadata ambiguity
  - no source provenance or evidence-aware review layer
extension_potential: medium
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
relations: []
tags:
  - library-review
  - architecture-review
  - kova
  - local-first-notes
  - quick-capture
  - ai-tool-layer
  - agent-gateway
  - risk-boundary
  - candidate-only
---

# 库分析：Xinghongia/Kova

## 一句话结论

Kova 值得看，但不是因为它比 VAKS 更懂知识管理。它强在“本地 AI 笔记工具的手感”：热键捕获、桌面弹窗、AI 工具调用、SQLite 本地存、备份恢复。

对我们最有价值的不是照搬产品，而是提炼一个 VAKS sidecar 的雏形：

```text
快捕获
-> 候选写入
-> 可见工具调用
-> diff / approval
-> review queue
```

其中 Kova 已经做好前半段；VAKS 必须补上后半段。

## 它解决什么问题

Kova 解决的是个人在桌面上快速记录和整理笔记的问题，并把 AI 放进笔记操作流里：

- 灵感来了能快速记一笔。
- 笔记和文件夹都存在本地。
- AI 可以直接创建、搜索、移动、更新、删除、导出笔记。
- 用户可以备份恢复自己的本地数据。

它不是证据系统、review system、知识校准系统，也不是 Obsidian vault 编译器。

## 核心设计

```text
Tauri desktop shell
-> React UI
-> Rust commands
-> SQLite local DB
-> quick note window
-> AI chat panel
-> OpenAI-compatible tool calling
-> backup / restore / import / export
```

Kova 的设计取舍很明确：让本地笔记体验轻、快、AI 可操作。

VAKS 的取舍不同：让强资料、关键结论、行动依据有来源、候选、校准、review、关系、反馈边界。

所以它是入口层参考，不是主架构替代品。

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:23-27` | lightweight / AI operations / local storage / quick note / backup claims | product promise maps to capture + local-first UX | README only |
| `README.md:100-103` | SSE AI chat and 17 tools | AI-as-operator product direction | tool safety requires code review |
| `src-tauri/Cargo.toml:21-33` | Tauri, global shortcut, single instance, reqwest stream, zip, rusqlite | desktop sidecar stack | dependency stack not adoption proof |
| `src-tauri/src/services/ai.rs:203-207` | tool prompt says AI should actively manage notes/folders | AI command layer | direct mutation risk |
| `src-tauri/src/services/ai.rs:245` / `:412` | max 10 tool loops | bounded tool loop | not permission control |
| `src-tauri/src/services/ai.rs:356-377` | max context truncation + conversation summary | activation/context hygiene | not evidence support |
| `src-tauri/src/services/ai.rs:557-571` | emits `tool_call`, `tool_done`, `data_changed` | visible agent operation stream | event is not approval |
| `src-tauri/src/services/ai.rs:614-887` | executes create/update/move/delete/batch/export tools | concrete tool operation implementation | unsafe for VAKS reviewed layer |
| `src-tauri/src/services/ai.rs:904-1138` | OpenAI function definitions | reusable schema shape | adapt only behind quarantine |
| `src-tauri/src/lib.rs:211-234` | quick window near cursor, always on top, skip taskbar | capture UX alpha | capture-only |
| `src-tauri/src/lib.rs:402-461` | global shortcut register/update | hotkey intake shell | needs collision/error policy |
| `src-tauri/src/lib.rs:164-183` / `:579-585` | read/write/copy/download commands exposed | local app convenience | broad command surface risk |
| `src-tauri/src/services/db/mod.rs:47-84` | notes/folders/conversations/messages schema | local app state model | not VAKS truth source |
| `src-tauri/src/services/db/mod.rs:165-303` | backup/restore ZIP | resilience pattern | secrets/config may be included |
| `src-tauri/src/services/db/config.rs:5-35` | config JSON includes API key | implementation fact | plaintext secret risk |
| `src-tauri/src/services/db/io.rs:10-163` | md/html/txt import/export | interop pattern | simple HTML parsing risk |
| `src/quick.tsx:25-32` / `:150-162` | quick write/browse modes and save flow | high-value capture loop | no provenance/review |
| `src/App.tsx:102-131` | listens quick note and AI data changes | clean event bridge | not feedback ledger |

## 当前支线价值

当前支线：

```text
VAKS source intake / agent gateway / capture UX / dev context
```

它对当前支线：

```text
refines / risk_of
```

具体价值：

- 提供一个轻桌面入口的真实源码样本。
- 证明 quick capture 不必先做完整 vault app，也可以是一个小弹窗。
- 证明 AI 工具层可以用 OpenAI-compatible schema 做笔记操作。
- 提供 tool event 的 UI 刷新和操作可见性参考。
- 提供本地 sidecar 的 SQLite + backup/restore 参考。

风险：

- 如果直接借，会把 AI 工具成功误当成知识成功。
- 如果让 AI 直接写 Obsidian/vault reviewed 层，会破坏 VAKS 的候选/校准/review 边界。
- 如果把 SQLite 当真源，会和 Markdown vault source-of-truth 冲突。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | 不提供 raw/wiki/index/log 编译主线；但 quick capture 可作为 raw intake entry | adapt small |
| Dusk workbench | 桌面弹窗、tray、窗口状态、轻 UI 对 workbench 有启发 | adapt |
| source ingest | 文件导入导出有参考，但 provenance 不足 | adapt with provenance |
| review queue | 没有 review queue；AI 直接改 notes | reject direct |
| schema / reviewed knowledge | 只有 notes/folders/tags，不处理 claim/pattern/decision | no direct value |
| memory / dev context | conversation summary 和 max context 可作为 activation hygiene | adapt narrowly |
| feedback | `data_changed` 只是刷新，不是 use ledger | no direct value |
| retrieval / cache | 搜索是 app 内笔记搜索；无 authority bucket | weak |
| API / MCP / agent access | tool schema 和 event flow 很有价值；权限边界不足 | adapt with approval |
| viewer / workbench | Tauri shell、quick window、AI panel 可借 UI 思路 | adapt |
| publishing | export Markdown/HTML/TXT 是小参考 | low |
| risk / anti-pattern | direct AI mutation、plaintext key、broad file command surface 是高价值反面教材 | strong risk |

## 值得提炼的模式

### hotkey-cursor-quick-capture

用户不应该为了捕获一条想法被迫进入完整 app。Kova 的热键 + 鼠标附近弹窗，是很好的轻捕获手感。

VAKS 融合版：

```text
global hotkey
-> small capture window
-> raw/candidate file
-> source/provenance stub
-> review queue only when needed
```

### visible-ai-tool-operation-stream

AI 操作应该可见。Kova 的 `tool_call` / `tool_done` / `data_changed` 是一个好骨架。

VAKS 融合版：

```text
tool_intent
-> proposed diff
-> risk class
-> approval
-> execution
-> receipt
```

### openai-compatible-note-tool-schema

Kova 的 note/folder tools 能启发 VAKS 的 candidate-only tools。

VAKS 融合版：

```text
create_candidate_note
update_candidate_note
append_source_anchor
queue_review_candidate
never_write_reviewed_truth_directly
```

### local-sidecar-state

SQLite 适合存 UI 状态、队列、对话、缓存、索引，不适合成为 reviewed knowledge 主库。

VAKS 融合版：

```text
Markdown vault = authority
SQLite = derived cache / local app state
```

## 标签与量化

- domain: local_first_notes / ai_note_client / desktop_pkm
- problem: quick_capture / local_note_operation / ai_tooling_for_notes
- pattern: hotkey_capture_surface / visible_tool_stream / local_sidecar_db / zip_backup_restore
- anti_pattern: direct_ai_mutation_without_review / sqlite_truth_source_confusion / plaintext_secret_config
- maturity: experimental
- complexity: medium
- problem_fit: 4
- reuse_value: 4
- implementation_cost: 3
- integration_fit: 3
- evidence_strength: 3
- reversibility: 4

## 交叉验证

- 相似设计来源：之前蒸馏过的 llm_wiki / local API / Obsidian AI workflows 都强调 agent 入口，但 Kova 更偏桌面体验。
- 用户历史项目里的相似问题/影子：VAKS 需要强资料入库入口，但不想让普通 capture 变繁琐。
- 支持证据：源码中 quick window、global shortcut、AI tools、stream events、SQLite backup/restore 均有可查 anchors。
- 反例或失败边界：没有 review queue、没有 evidence support、没有 authority bucket、没有 approval gate。
- 最小验证方式：做一个只写 `raw/` 或 `outputs/review/` 的 quick capture prototype，不允许写 `wiki/claims` 或 `wiki/patterns`。

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Quick capture should be light and low-friction | Capture must stay easy; ordinary capture stays light | candidate_relation | Should VAKS add a local hotkey capture surface later? |
| AI tools can operate notes | Agent memory quarantine forbids direct reviewed truth writes | scope_mismatch / risk_of | What tool actions can be candidate-only without review? |
| SQLite is convenient local storage | Markdown vault remains source-of-truth | scope_mismatch | Which state may live in sidecar DB, and which must remain Markdown? |
| Stream events expose agent actions | Approval integrity is process evidence, not support | candidate_relation | What receipt fields are minimum for agent write transparency? |
| Conversation summary helps context | Activation Tier is not truth tier | candidate_relation | Should conversation summaries enter only activation/support? |

边界：

- 相似不是支持。
- 冲突不是自动推翻。
- 重复出现不是自动真理。
- 校准输出是 review input，不是 reviewed relation。

## Support / Challenge Review

- What supports it:
  - Source code shows actual quick window, global shortcut, AI tools, stream events, SQLite DB, backup/restore.
- What challenges it:
  - App was not run locally.
  - No tests observed.
  - Repo is very new.
  - Direct AI mutation conflicts with VAKS reviewed-knowledge boundary.
  - License metadata is ambiguous.
- Challenge severity: major for direct adoption; minor for design-only capture UX borrowing.
- Scope limits:
  - This review supports "Kova contains these mechanisms" and "these mechanisms are useful design references".
  - It does not support "Kova is production-safe" or "VAKS should adopt Kova code".
- Known risks:
  - Over-borrowing a convenience app into a verified-action system.
  - Turning AI tool success into truth confidence.
  - Letting sidecar state become authority.
- Review again when:
  - Kova adds permission/review gates, tests, a license file, or a mature release.
  - VAKS starts building a local capture client or agent gateway.
- Action readiness: not_ready.

## 关系边 / 关联强度

```yaml
relations:
  - target: "[[agent-memory-quarantine]]"
    type: risk_of
    relation_state: candidate
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-06-13-Xinghongia-Kova-source]]"
    rationale: "Kova's AI tools can directly mutate notes/folders, which is the boundary VAKS must quarantine."
    created: 2026-06-13
    last_verified: 2026-06-13
  - target: "[[operational-session-capture-loop]]"
    type: refines
    relation_state: candidate
    strength: 4
    confidence: medium
    evidence:
      - "[[2026-06-13-Xinghongia-Kova-source]]"
    rationale: "Kova's hotkey/cursor popup gives a concrete lightweight capture UI pattern."
    created: 2026-06-13
    last_verified: 2026-06-13
```

These are candidate relation suggestions only.

## 对当前项目的适配点

最小优雅吸收版：

```text
VAKS Quick Capture Sidecar

Allowed:
  create raw source stub
  append candidate note
  open review queue item
  show proposed tool action
  show diff
  log receipt

Forbidden:
  create reviewed claim directly
  edit reviewed pattern directly
  delete source or reviewed files without confirmation
  treat AI summary as support
```

## 可拓展性

- 是否适合作为插件/适配层：适合作为未来本地 sidecar / capture client 的设计参考。
- 是否会绑定核心结构：不应该绑定核心；核心仍是 Markdown vault + review gate。
- 未来替换成本：低到中。Quick capture 和 event stream 可单独借，不需要 fork 全 app。
- 可迁移路径：先做 candidate-only write adapter，再做 approval UI，再接 review queue。

## 复杂度和风险

- Tauri app 会增加桌面客户端维护成本。
- Agent tools 一旦接入真实 vault，就必须有权限和审批边界。
- SQLite sidecar 很容易变成第二套真源。
- API key / local file command / CSP 需要安全设计。

## 不可行点 / 避坑

- 不要 fork Kova 当 VAKS 主体。
- 不要把 Kova 的 SQLite schema 迁成 VAKS schema。
- 不要让 AI tool 直接写 `wiki/claims`、`wiki/patterns`、`wiki/decisions`。
- 不要把 quick capture 变成强制完整 source review。
- 不要让本地 app 的 stream event 替代 feedback ledger。

更稳的替代方案：

```text
candidate-only capture sidecar
-> path-scoped write tools
-> diff preview
-> approval gate
-> append-only receipt
-> later review queue
```

## 融合判断

- 结论：adapt。
- 理由：Kova 的 UX 和 tool-stream 很值得借，但它的 truth/review 边界不适合 VAKS。
- 验证方式：先做一个只写候选层的小捕获原型，验证是否真的减少 capture 摩擦，不碰 reviewed 层。

## 直接判断

- Direct use: no.
- Fork: no, unless later要做独立桌面客户端实验。
- Design-only: yes, strong.
- Reject: reject direct AI mutation and SQLite-as-truth-source direction.
- Current branch value: strong for capture UX / agent gateway risk.
- Whole architecture value: medium-high as sidecar/interface/risk reference.
- Risk: high if copied without quarantine.
- Next action: keep as candidate support + risk reference; only promote after a concrete VAKS local capture or agent gateway task appears.

## 后续行动

- 若用户后续要做 VAKS 桌面入口：从 Kova 抽 `quick capture + visible tool event + candidate-only write` 三件事。
- 若用户后续要做 agent gateway：把 Kova 的 direct mutation 作为反面压力测试。
- 若用户后续要做 reviewed pattern：拆成两个独立 candidate points，分别 review：
  - quick capture hotkey surface
  - visible tool operation stream with approval gate
