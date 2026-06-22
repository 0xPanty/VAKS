---
type: source
record_kind: source_card
status: source-captured
title: Xinghongia/Kova
source_id: github-Xinghongia-Kova
source_uri: github:Xinghongia/Kova@8c440483cc5af9f1915fc8d4e2fcd82c3edc9a05
source_url: https://github.com/Xinghongia/Kova
source_type: github_repo
owner: Xinghongia
repo: Kova
author: Xinghongia
publisher: GitHub
published_at: 2026-06-02
updated_at: 2026-06-13
captured_at: 2026-06-13
captured_by: Codex
checked_commit: 8c440483cc5af9f1915fc8d4e2fcd82c3edc9a05
checked_branch: main
checked_tag: v0.1.0
version_or_commit: 8c440483cc5af9f1915fc8d4e2fcd82c3edc9a05
source_integrity:
  source_hash:
  snapshot_hash: 8256ABDA1F55736C758511ED2B164BA76056110BA342ACFDA41655E4671FEEC5
  ingest_state: new
adapter_ingest:
  adapter_name: manual-github-repo-review
  adapter_version: 2026-06-13
  capture_method: GitHub API metadata + source zip + local clone + rg/code inspection
  extraction_trace:
    - raw/repos/_snapshots/2026-06-13-Xinghongia-Kova-8c440483-source.zip
    - C:\Users\Administrator\.codex\repo-research\2026-06-13-Xinghongia-Kova-8c440483
  known_limits:
    - app not executed locally
    - tests/build not run
    - GitHub star/download counts are time-sensitive
source_status: active
raw_location: raw/repos/_snapshots/2026-06-13-Xinghongia-Kova-8c440483-source.zip
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
review_priority: normal
review_owner: Codex
formalization_status: raw-only
why_saved: User requested strong distillation of Xinghongia/Kova for VAKS architecture comparison and borrowable design extraction.
topics:
  - local-first-notes
  - tauri-desktop-client
  - ai-assisted-note-management
  - quick-capture
  - sqlite-local-storage
  - openai-compatible-tools
projects:
  - VAKS
source_family:
  - ai-note-client
  - local-first-pkm
upstream_sources: []
verification_status: code-inspected-not-run
evidence_granularity: table_or_code_anchor
candidate_relation_suggestions:
  - target: "[[agent-memory-quarantine]]"
    relation_type: risk_of
    relation_state: candidate
    why_suggested: "Kova lets AI tools directly mutate notes/folders, which is useful UX but unsafe for VAKS reviewed knowledge without a quarantine and approval gate."
    source_anchor: "src-tauri/src/services/ai.rs:614"
  - target: "[[operational-session-capture-loop]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "The cursor-position quick-note window and hotkey capture flow are concrete local-first capture UX anchors."
    source_anchor: "src-tauri/src/lib.rs:211"
tags:
  - source-card
  - github-repo
  - kova
  - local-first-notes
  - tauri
  - react
  - rust
  - sqlite
  - ai-tool-layer
  - quick-capture
  - candidate-only
---

# 来源记录：Xinghongia/Kova

## 为什么收录

用户要求对 `Xinghongia/Kova` 做强蒸馏，并按当前 VAKS 架构提取最大可借鉴点。

本卡只记录来源身份、快照、源码锚点和初步候选点。它不是采纳决策，不是 reviewed knowledge，也不能作为 action basis。

## 来源信息

- 仓库：`Xinghongia/Kova`
- 原始链接：https://github.com/Xinghongia/Kova
- 检查分支：`main`
- 检查 commit：`8c440483cc5af9f1915fc8d4e2fcd82c3edc9a05`
- GitHub 创建时间：2026-06-02T12:13:40Z
- GitHub 更新时间：2026-06-13T02:28:15Z
- GitHub pushed_at：2026-06-08T10:43:25Z
- Release/tag：`v0.1.0`，tag commit `d90010bcf080683f3900bfcd210290190ce23935`
- 快照：`raw/repos/_snapshots/2026-06-13-Xinghongia-Kova-8c440483-source.zip`
- 快照 SHA256：`8256ABDA1F55736C758511ED2B164BA76056110BA342ACFDA41655E4671FEEC5`
- 本地 scratch clone：`C:\Users\Administrator\.codex\repo-research\2026-06-13-Xinghongia-Kova-8c440483`
- 采集方式：GitHub API metadata、source zip、local clone、源码检索。

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

Source card 只提供来源身份和查验轨迹。它不能证明任何 VAKS 设计结论。

## Key Entity Confidence Check

| Entity | Check result | Confidence | Note |
|---|---|---:|---|
| Repo identity | GitHub API + local clone HEAD match `Xinghongia/Kova` | high | 当前检查到 main HEAD 为 `8c440483...`。 |
| Release identity | GitHub release API shows `v0.1.0` assets | high | Asset digests captured in review notes; counts are time-sensitive. |
| License | `Cargo.toml` says MIT; README badge says MIT; GitHub API license null and no `LICENSE` file seen | medium | 需要正式采用前复核许可文件。 |
| Package size claim | README says install package under 5 MB; release assets observed around 6.48 MB exe / 8.61 MB msi | medium | 可能口径不同，但不能直接引用为已证实事实。 |
| Runtime quality | Not run locally | low | 只做了源码级蒸馏。 |

## Source / Code Anchors

| Anchor | What exists | Why it matters | Boundary |
|---|---|---|---|
| `README.md:23-27` | Claims lightweight, AI note operations, local storage, quick note, backup | Product-level promise | README promise only, not runtime proof |
| `README.md:100-103` | OpenAI-compatible SSE chat and 17 built-in tools | Confirms AI-native positioning | Tool safety must be checked in code |
| `src-tauri/Cargo.toml:2-8` | Rust package `kova`, version `0.1.0`, MIT field, Rust 1.77.2 | Build identity and license hint | License still ambiguous without repo license file |
| `src-tauri/Cargo.toml:21-33` | Tauri, global shortcut, single instance, reqwest stream, zip, rusqlite bundled | Desktop/local-first implementation stack | Dependency choice is not design validation |
| `src-tauri/src/services/ai.rs:203-207` | System tool prompt asks AI to actively manage notes/folders | Core AI-as-operator pattern | Unsafe for VAKS truth layer without approval |
| `src-tauri/src/services/ai.rs:245` and `src-tauri/src/services/ai.rs:412` | Tool loop capped at 10 iterations | Small guardrail against infinite tool loops | Not a review or permission gate |
| `src-tauri/src/services/ai.rs:356-377` | Context truncation and conversation summary injection | Lightweight context management | Summary is not evidence support |
| `src-tauri/src/services/ai.rs:557-571` | Stream emits tool call, tool done, data changed events | UI can expose agent actions and refresh state | Event visibility is not approval integrity |
| `src-tauri/src/services/ai.rs:614-887` | `execute_tool` mutates notes/folders and exports notes | Concrete operation layer | Direct mutation is the main VAKS anti-pattern |
| `src-tauri/src/services/ai.rs:904-1138` | Function definitions for note/folder CRUD, search, batch ops, export | Tool schema reference | Tool schema should be quarantined in VAKS |
| `src-tauri/src/lib.rs:211-234` | Quick-note window near cursor, always on top, skip taskbar | Strong quick-capture UX | Capture only; not review |
| `src-tauri/src/lib.rs:402-461` | User-configurable global shortcut registration | Concrete hotkey intake surface | Needs collision/error handling in any adaptation |
| `src-tauri/src/lib.rs:164-183` and `src-tauri/src/lib.rs:579-585` | Frontend-exposed file read/write/copy/download commands | Broad local file command surface | Security risk; do not copy blindly |
| `src-tauri/src/services/db/mod.rs:47-84` | SQLite tables for notes/folders/conversations/messages | Local data model | SQLite app DB is not VAKS source-of-truth |
| `src-tauri/src/services/db/mod.rs:165-303` | ZIP backup/restore of db/config/settings | Practical local-first resilience pattern | Backup may include config/API keys |
| `src-tauri/src/services/db/config.rs:5-35` | AI config and API key saved to `config.json` | Important privacy/security anchor | Plaintext key storage risk |
| `src-tauri/src/services/db/io.rs:10-163` | MD/HTML/TXT import/export | Interop value | HTML parser is simple and fragile |
| `src/quick.tsx:25-32` and `src/quick.tsx:150-162` | Quick note write/browse modes and note creation | End-user capture loop | No source provenance/review semantics |
| `src/App.tsx:102-131` | `quick-note-saved` and `ai-stream data_changed` refresh main state | Clean event bridge between capture/AI and UI | Refresh signal is not feedback ledger |

## 初步看点

- Kova 是一个 Tauri 2 + React + Rust + SQLite 的本地 AI 笔记客户端。
- 它把 AI 放在“操作层”：AI 不只是聊天，而是能调用工具创建、搜索、移动、删除、导出笔记和文件夹。
- 它的 quick note 体验很具体：全局热键、鼠标附近弹窗、always-on-top、写入后刷新主界面。
- 它有本地数据库、数据目录切换、ZIP 备份/恢复、Markdown/HTML/TXT 导入导出。
- 它有流式 AI、工具执行事件、停止/重试、上下文截断、对话摘要、thinking 开关等 AI 客户端机制。

## 明显疑点

- 仓库很新，未观察到测试套件；本次未运行 app。
- AI 工具可直接改笔记/文件夹，没有在已读源码中看到逐项人工审批门。
- API key/profile 保存在本地 `config.json`，需要当作敏感配置处理。
- Tauri command surface 暴露 `read_file` / `write_file` / `copy_file` / `download_font`，适合本地 app，但对 VAKS agent 权限设计是风险样本。
- README 的安装包大小描述和 release asset 尺寸存在口径差异。
- 许可字段不完全一致：代码配置写 MIT，但仓库 metadata 未识别 license，且未看到独立 `LICENSE` 文件。

## 可抽取 Candidate Points

1. 本地优先 AI 笔记客户端可以作为 VAKS 的轻入口层参考，但不能替代 Markdown vault 真源。
2. Quick capture 的热键、鼠标附近弹窗、always-on-top、快速保存，是值得借鉴的 Capture UX。
3. AI tool calling 可以作为候选层操作助手，但必须加 quarantine、diff preview、approval、action receipt。
4. Stream event 的 `tool_call` / `tool_done` / `data_changed` 机制适合做可见 agent 操作轨迹。
5. 对话摘要和 max context message 是 activation/context hygiene 参考，不是 evidence support。
6. SQLite + ZIP backup/restore 是本地 app resilience 参考，但不应成为 VAKS reviewed truth source。
7. Plaintext API key、宽文件命令、直接删除/批量删除，是 agent access 风险样本。

## 当前处理等级

```text
heavy source capture + candidate architecture review
```

已保留源码快照，并另写候选蒸馏和架构评审摘要。后续若要把其中某个点提升为 pattern / anti-pattern，需要走 evidence-aware review / promotion gate。

## 下一步

- 用 candidate distillation 做方向筛选。
- 用 architecture review 做全貌对照。
- 用 project overlay 记录 VAKS 当前可借和不可借范围。
- 不从 source card 直接创建 reviewed relation、reviewed pattern、decision 或 action basis。
