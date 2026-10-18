---
type: source
record_kind: source_card
status: source-captured
title: "Momoyu404/geminese"
source_id: github-Momoyu404-geminese-d8623d8
source_uri: github:Momoyu404/geminese
source_url: https://github.com/Momoyu404/geminese
source_type: repository
author: Guangxing Lyu
publisher: GitHub
published_at: "2026-03-13T00:34:38Z"
updated_at: "2026-05-29T07:00:29Z"
captured_at: "2026-06-08 18:58:00 +08:00"
captured_by: Codex
version_or_commit: d8623d85d92dba5e4270b3246b5bc5f775dfb8a8
commit_time: "2026-03-29T12:15:31+11:00"
source_integrity:
  source_hash:
  snapshot_hash: sha256:7fb2dbaeb4806472c857271a4ed07834ae27ad2192842760ce04f7422ed57ba8
  ingest_state: captured_public_git
adapter_ingest:
  adapter_name: git-clone-and-archive
  adapter_version: manual-2026-06-08
  capture_method: public git clone depth 1 + git archive
  extraction_trace:
    - git clone https://github.com/Momoyu404/geminese.git
    - checked HEAD commit d8623d85d92dba5e4270b3246b5bc5f775dfb8a8
    - created source zip snapshot from HEAD
  known_limits:
    - no runtime execution
    - no Obsidian plugin install test
    - no Gemini CLI or Ollama live connection test
    - GitHub stars/issues are point-in-time metadata
source_status: active
raw_location: raw/repos/2026-06-08-Momoyu404-geminese-source.md
snapshot_location: raw/repos/_snapshots/2026-06-08-Momoyu404-geminese-d8623d8-source.zip
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
topics:
  - obsidian-plugin
  - gemini-cli
  - ollama
  - agent-in-vault
  - mcp
  - permission-boundary
  - slash-commands
  - local-skills
projects:
  - verified-action-knowledge-system
source_family: obsidian-agent-workbench
upstream_sources:
  - YishenTu/claudian
verification_status: unverified
candidate_relation_suggestions: []
tags:
  - raw-repo
  - github
  - obsidian
  - candidate-only
why_saved: see_body_or_legacy_record
---

# 来源记录：Momoyu404/geminese

## 为什么收录

`geminese` 是一个 Obsidian 插件，把 Gemini CLI 和本地 Ollama 模型接进 Obsidian vault。它对 VAKS 的价值不是“照搬插件”，而是展示了一个可运行的 agent-in-vault 外壳：聊天侧栏、当前笔记上下文、文件提及、图片、inline edit、slash commands、skills、subagents、MCP、Plan / Agent 权限模式、路径访问边界和本地模型工具协议。

它尤其适合 VAKS 未来的 Agent Gateway / Workbench / Source Intake UI 参考，但不能直接变成 VAKS reviewed knowledge 或 action basis。

## 来源信息

- 仓库：Momoyu404/geminese
- URL：https://github.com/Momoyu404/geminese
- 默认分支：main
- 检查 commit：`d8623d85d92dba5e4270b3246b5bc5f775dfb8a8`
- commit time：2026-03-29T12:15:31+11:00
- manifest version：0.9.1
- min Obsidian version：1.4.5
- license：MIT
- GitHub metadata captured at：2026-06-08
- stars / forks / open issues at capture：60 / 3 / 0
- 源码快照：raw/repos/_snapshots/2026-06-08-Momoyu404-geminese-d8623d8-source.zip
- 快照 SHA256：`7fb2dbaeb4806472c857271a4ed07834ae27ad2192842760ce04f7422ed57ba8`

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

Source records provide provenance and findability. They must not carry
adopt/reject verdicts, truth scores, project borrowing conclusions, or action
basis.

## 初步看点

- Obsidian 插件里直接运行 Gemini CLI：vault 是 CLI 工作目录，流式读取 `stream-json`。
- 同时支持 Gemini 云模型和 Ollama 本地模型，给本地 agent 设计了小型工具协议。
- Plan / Agent 模式：Plan 限定 read-only 工具，Agent 允许执行和编辑。
- 访问边界：vault read/write、external context read/write、export path write-only。
- 支持 MCP server 配置和按 `@mcp-server` 激活，带 context-saving 过滤。
- 支持 `.gemini/commands`、`.gemini/skills`、`.gemini/agents`、session、settings、MCP 配置的 vault-local 存储。
- Inline edit 单独使用 read-only hook 和结果 preview，降低直接修改风险。

## 明显疑点

- 默认 permission mode 是 Agent，安全性依赖 UI 提醒、权限模式和 hooks 是否稳定执行。
- Gemini 路径会把输入、文件、图片和 tool outputs 交给 Google Gemini API；隐私边界不等于本地。
- Ollama 本地 agent 的 JSON 工具协议是插件自建的，能力比 Gemini CLI 原生路径窄。
- Bash 路径检测是 best-effort，不等于完整 shell 安全模型。
- 外部上下文是 full read/write，导出路径是 write-only，用户需要非常清楚二者差别。

## 可抽取 Candidate Points

- Obsidian vault 可以成为 agent workbench，但必须先做路径、权限、模式和审计边界。
- Plan / Agent 这种显式权限模式值得成为 VAKS Agent Gateway 的基本交互。
- Local model 不应只是聊天后端；可通过受限工具协议执行 vault-native planning / edit。
- MCP 应按需激活和禁用工具，避免一次性把所有外部工具塞进上下文。
- Skills / slash commands / agents 作为 vault-local Markdown 配置，适合让用户逐步扩展工作流。

## 当前处理等级

```text
medium
```

升级到 heavy 的条件：

- 用户要设计 VAKS Agent Gateway / Obsidian workbench。
- 需要把 Plan / Agent / external context / export path 边界改造成 VAKS 正式权限模型。
- 需要对比 Claudian、Geminese、Obsidian Skills、Easy Typing 等插件形成主线设计。

## 下一步

进入候选蒸馏和架构 review 摘要；不进入 reviewed knowledge，不改 VAKS 主文档。
