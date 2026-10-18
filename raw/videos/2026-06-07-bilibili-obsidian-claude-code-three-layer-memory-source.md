---
type: source
status: source-captured
title: "我用Obsidian + Claude Code搭了三层记忆系统，彻底解决了AI跨会话失忆"
source_id: bilibili-BV1iwLn64EKL
source_uri: bilibili:BV1iwLn64EKL
source_url: https://www.bilibili.com/video/BV1iwLn64EKL/
source_type: video
platform: bilibili
platform_id: BV1iwLn64EKL
author: "嗯哌AI"
publisher: "嗯哌AI"
published_at: "2026-05-17 20:55:25 +08:00"
updated_at:
duration: 987s
captured_at: "2026-06-07 18:41:25 +08:00"
captured_by: Codex
raw_location: raw/videos/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-source.md
processing_mode: public-audio-local-asr
processing_level: medium
processing_tier: medium
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
access_boundary: public_no_cookies
transcript_method: local_asr
transcript_location: raw/videos/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-source/transcript.txt
segments_location: raw/videos/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-source/segments.md
transcript_metadata_location: raw/videos/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-source/transcript-meta.json
ledger_location: raw/videos/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-source/acquisition-ledger.json
source_metadata_location: raw/videos/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-source/source-metadata.json
media_retention: deleted
source_status: active
topics:
  - obsidian
  - claude-code
  - local-first-memory
  - session-memory
  - memory-router
  - second-brain
  - VAKS
projects:
  - verified-action-knowledge-system
source_family: bilibili-obsidian-claude-code-memory-system
upstream_sources: []
verification_status: unverified
candidate_relation_suggestions:
  - target: "[[2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-candidate-distillation]]"
    relation_type: derived_from
    relation_state: candidate
    why_suggested: "The video demonstrates a local three-layer memory scaffold: stable vault knowledge, session memory folder, and root memory router file."
reference_layer_tag: ref/three-layer-memory-router
tags:
  - raw-video
  - bilibili
  - local-asr
  - obsidian
  - claude-code
  - memory-router
  - candidate-only
---

# Bilibili Source Record: Obsidian + Claude Code Three-Layer Memory

## 为什么收录

用户要求蒸馏这个视频。它和 VAKS 的 `MEMORY_TIER`、`DEV_CONTEXT`、`AGENTS.md` / handoff 入口文件、候选工作台边界非常接近。

本卡只记录公开视频来源、公开元数据、本地 ASR 转写路径和候选理解。它不把视频观点直接写成 reviewed knowledge、architecture decision 或 action basis。

## 来源信息

- Platform: Bilibili
- BV: `BV1iwLn64EKL`
- URL: https://www.bilibili.com/video/BV1iwLn64EKL/
- Title: `我用Obsidian + Claude Code搭了三层记忆系统，彻底解决了AI跨会话失忆`
- Uploader: `嗯哌AI`
- Published: `2026-05-17 20:55:25 +08:00`
- Duration: `987s`
- Public description: explains a three-layer memory system using Obsidian + Claude Code.
- Public stats at capture: views `3289`, favorites `389`, replies `137`, likes `116`.
- Capture path: public Bilibili metadata API -> public subtitle check -> public audio -> local GPU ASR.

## Intake Boundary

```yaml
processing_tier: medium
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

Video source records provide provenance, transcript location, and findability.
They do not create reviewed evidence, project borrowing conclusions, or action
basis.

## 获取与转写

```yaml
subtitle_status: public subtitle list empty
transcript_method: local_asr
asr_engine: faster-whisper
asr_model: small
asr_device: cuda
language: zh
language_probability: 1
segment_count: 513
text_chars: 5456
transcript_quality: medium
media_retention: deleted
scratch_cleanup: audio deleted after ASR
project_visible_artifacts: yes
cookies_used: false
cloud_api_used: false
transcript_location: raw/videos/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-source/transcript.txt
segments_location: raw/videos/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-source/segments.md
transcript_metadata_location: raw/videos/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-source/transcript-meta.json
ledger_location: raw/videos/2026-06-07-bilibili-obsidian-claude-code-three-layer-memory-source/acquisition-ledger.json
```

说明：

```text
字幕 / ASR 是 raw/source text，不是 reviewed evidence。
AI 摘要是 candidate comprehension，不是 truth。
本视频 ASR 有明显同音错误，例如 Cloud/Claude、绘画/会话、Memory.MB/MEMORY.md。
关键实体优先按 Bilibili 标题、简介和项目上下文校正。
```

## 人话摘要

这个视频讲的是一个很简单但很管用的本地代理记忆脚手架：

```text
Layer 1: Obsidian 长期知识层
Layer 2: Claude_Memory 会话/工作记忆层
Layer 3: 根目录 MEMORY.md 路由/启动说明层
```

它的核心不是“Obsidian 文件夹怎么起名”，而是：

```text
让 AI 每次启动先读一个入口文件，知道你是谁、资料在哪里、规则是什么、上次做到哪里；
让当前会话产生的草稿和决策先进入隔离的会话记忆；
会话结束后再把有价值内容整理进长期知识层。
```

对 VAKS 来说，这条视频最像一个面向普通用户的 `AGENTS.md + 00_handoff + DEV_CONTEXT + session scratch` 简化版。

## 关键实体置信度

```text
confirmed:
  - Bilibili BV1iwLn64EKL
  - Title: 我用Obsidian + Claude Code搭了三层记忆系统，彻底解决了AI跨会话失忆
  - Uploader: 嗯哌AI
  - Published: 2026-05-17 20:55:25 +08:00
  - Duration: 987s
  - Tools named in title/description: Obsidian, Claude Code
  - Description names Layer 1, Layer 2, Layer 3, Claude_Memory, MEMORY.md
  - Public subtitle list was empty; transcript came from local ASR

likely:
  - The video mentions folder examples such as Context, Clippings, Script, Daily, Reading.
  - The video distinguishes a Claude/CLAUDE-style behavior file from a separate MEMORY.md route/index file.
  - The demo uses prompt templates for five workflows: read, analyze, write, connect, archive.

unclear:
  - Exact on-screen prompt text and commands.
  - Exact spelling of all folder names shown on screen.
  - Whether `Smart Connections` is only a next-episode topic or already part of the demonstrated setup.

needs user visual check:
  - Exact MEMORY.md template text if later copied into VAKS or another project.
  - Exact terminal/Obsidian plugin command if someone wants to reproduce the demo literally.
```

## 时间轴 / 分段

- `00:00-00:24`: pain point: AI cross-session memory loss; solution is local Obsidian + Claude Code memory scaffold.
- `00:24-03:34`: three-layer model: long-term knowledge, session/work memory, root memory router file.
- `03:34-05:00`: practical setup: create/open an Obsidian vault as a local knowledge repository.
- `05:00-06:40`: Layer 1 folder examples: Context, Clippings, Script, Daily, Reading.
- `06:40-09:05`: MEMORY.md template sections: basic info, Layer 1 map, Layer 2 rule, routing/core workflow, operating rules, quick commands.
- `09:05-10:44`: connect Claude Code to the vault and let it read the root route file.
- `10:45-13:46`: five workflows: read/summarize Context, synthesize Reading/Clippings, create script from style/history, connect related notes, end-session archive.
- `14:03-15:17`: why separate MEMORY.md from Claude/CLAUDE-style general behavior rules.
- `15:17-16:26`: closing claim: every inspiration/thought/revision should accumulate locally.

## 视频里直接说了什么

- Obsidian is the local storage surface for knowledge, scripts, preferences, and notes.
- Claude Code is positioned as the tool that reads and uses the vault.
- The proposed structure has three layers:
  - stable long-term knowledge folders;
  - a dedicated current-session memory folder;
  - one root memory/router file.
- Each session should start by reading the root memory file, then find long-term knowledge and prior session context.
- New outputs should first land in the session memory folder, then be archived or promoted into long-term folders after a session-end整理 step.
- The demo includes five prompt use cases: basic read test, knowledge summary, script creation, related-note discovery, and end-session archive.

## 我的理解 / 推断

这个视频真正有价值的不是三层命名，而是三个边界：

```text
stable memory != session scratch
router file != truth layer
session output != long-term knowledge until整理/迁移
```

这正好对应 VAKS 的核心边界：

```text
raw/candidate/reviewed 分离
activation != truth
handoff / DEV_CONTEXT 是入口和工作台，不是证据
候选输出必须经过 review gate 才能进入可行动知识
```

## 反漏提取检查

```text
pain point:
  - AI across sessions loses user/project context, style, prior decisions, and unfinished work.

workflow:
  - Obsidian vault -> long-term folders -> Claude_Memory session folder -> root MEMORY.md router -> Claude Code reads -> output -> write back -> session-end archive/promotion.

tools / plugins:
  - Obsidian, Claude Code Desktop/CLI, possible terminal plugin, possible CC Switch / third-party model switching, Smart Connections mentioned as next step.

information structure:
  - Layer 1 stable folders, Layer 2 session folder, Layer 3 root router file with maps/rules/prompts.

judgment mechanism:
  - The video relies on manual end-of-session整理 to decide what graduates from session memory to long-term memory.
  - It does not provide an evidence-aware truth review mechanism.

user experience:
  - Easier: user gets a simple, teachable setup for continuity.
  - Harder: long-term folder hygiene and session archive discipline become recurring chores.

automation boundary:
  - Starting context loading can be semi-automatic.
  - Promotion from session memory to long-term knowledge should stay explicit and reviewed.
  - Exact commands and prompt templates need visual verification before direct reuse.

risk:
  - Session scratch may pollute stable knowledge if auto-promoted.
  - Whole-vault scanning may leak private material or waste context.
  - MEMORY.md may be mistaken for truth, policy, or reviewed evidence.
  - Folder names may become copied as schema without proving fit.

fit for us:
  - Very strong as a user-facing explanation of VAKS activation and session-memory discipline.
  - Useful for AGENTS.md / handoff / DEV_CONTEXT as root-router analogies.
  - Useful for future session scratch, closeout, and promotion UX.

challenge to us:
  - VAKS may be too abstract for ordinary users unless we expose a simple three-file/folder operating surface.
  - Our review discipline is stronger, but the user-facing ritual should be as simple as this video.
```

## 可抽取 Candidate Points

- `three_layer_memory_scaffold`: stable vault knowledge, session scratch, and root router file should be distinct.
- `memory_router_file`: a root entry file can tell the agent who the user is, where data lives, what rules apply, and what to read first.
- `session_memory_quarantine`: current conversation outputs should land in a quarantined session folder before becoming durable knowledge.
- `end_session_promotion_ritual`: closeout/archive is the gate between session scratch and long-term vault.
- `five_prompt_smoke_tests`: read, analyze, write, connect, archive are practical tests for whether agent memory actually works.
- `claude_md_vs_memory_md_split`: separate general agent behavior/style rules from vault-specific routing and memory map.

## 可借鉴

- P1: root memory/router file as an activation gateway.
- P1: session scratch folder that prevents long-term knowledge pollution.
- P1: end-of-session整理/promotion ritual.
- P1: five smoke-test workflows for whether the memory scaffold works.
- P2: simple folder examples for creator workflows.
- P2: separate behavior file vs vault route/index file.
- P3: Smart Connections / semantic search as later activation enhancement, not truth engine.

## 不能直接借鉴

- Do not let Claude Code or any agent freely rewrite long-term knowledge.
- Do not treat MEMORY.md as reviewed knowledge, evidence, or action basis.
- Do not copy creator-oriented folders as VAKS schema.
- Do not assume whole-vault scan is safe or efficient for every task.
- Do not use session memory as truth confidence or source reliability.
- Do not merge session scratch into Layer 1 without candidate/review routing.

## 风险和不确定

- ASR quality is medium and has repeated proper-noun errors.
- The exact on-screen MEMORY.md template and prompts were not verified visually.
- The video is a tutorial/marketing-style demo, not an evaluated architecture.
- The source does not include formal evidence checks, conflict handling, provenance, or privacy policy.

## VAKS 归位

```text
Capture:
  - local-first Obsidian vault and source preservation.

Understand:
  - Claude Code reads Context/Reading/Script and synthesizes candidate outputs.

Review:
  - missing in the video; VAKS must add review gates before durable promotion.

Connect:
  - related-note discovery and knowledge-map summary are activation aids.

Activation / Context Pack:
  - MEMORY.md root router is the strongest analog.

Decision / Action:
  - not supported directly by this video.

Use Ledger / Feedback:
  - session memory and end-session archive can feed feedback, but cannot mutate truth.
```

## 处理等级

当前等级：medium。

升级到 heavy 的条件：

- VAKS decides to design an official agent-session scratch / closeout workflow.
- VAKS wants a user-facing `MEMORY.md` / `AGENTS.md` template for non-developer users.
- A future implementation would let agents write into the vault automatically.

## 下一步

Keep this as candidate/reference material and project overlay input. Do not promote to `wiki/claims`, `wiki/patterns`, or `wiki/decisions` without a later evidence-aware review.
