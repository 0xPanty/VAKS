---
type: library_review
status: draft
library_name: geminese
repo_url: https://github.com/Momoyu404/geminese
source_url: https://github.com/Momoyu404/geminese
checked_commit: d8623d85d92dba5e4270b3246b5bc5f775dfb8a8
commit_time: "2026-03-29T12:15:31+11:00"
source_status: active
reviewed_at: "2026-06-08"
domain: obsidian-agent-workbench
related_projects:
  - verified-action-knowledge-system
current_branch: agent-gateway / workbench reference
extracted_patterns:
  - visible-permission-mode
  - command-mediated-agent-access
  - vault-local-workflow-config
  - mcp-context-saving
  - inline-edit-preview
fusion_decision: adapt
confidence: medium
evidence_count: 12
cross_validated_with:
  - README.md
  - ARCHITECTURE.md
  - package.json
  - manifest.json
negative_evidence:
  - no runtime validation
  - cloud path sends data to Gemini API
  - Bash validation is best-effort
extension_potential: high
relations: []
tags:
  - library-review
  - candidate-only
  - obsidian
  - agent-gateway
---

# 库分析：Geminese

## 它解决什么问题

Geminese 解决的是：如何把 Gemini CLI / 本地 Ollama agent 嵌进 Obsidian，让 vault 成为 agent 的工作台。它不是一个知识库 truth engine，而是一个 agent-facing UI 和工具边界系统。

## 核心设计

```text
Obsidian sidebar UI
-> chat / inline edit / context chips / model selector
-> Gemini CLI subprocess or Ollama local runtime
-> vault tools / path validation / permission mode / MCP / skills / agents
-> local .gemini storage
```

Gemini 路径尽量复用 Gemini CLI 原生能力；Ollama 路径自建结构化 JSON 工具协议。

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md` | 双模型、agent、Plan / Agent、MCP、skills、inline edit、privacy | 产品壳完整，适合 workbench 借鉴 | README 不是实现证明 |
| `manifest.json` | Obsidian plugin id/version/minAppVersion/Desktop only | 可作为插件成熟度锚点 | 不说明运行稳定性 |
| `package.json` | TS/Obsidian/esbuild/Jest/MCP SDK | 工程栈清楚，测试脚本完整 | 未在本次运行测试 |
| `ARCHITECTURE.md` | layer map、storage、CLI-first、TDD | repo 自身工程边界清楚 | 不等于 VAKS 适配完成 |
| `src/core/agent/ClaudianService.ts` | Gemini CLI process、session、Ollama path、approval callbacks | agent runtime coordinator | 代码名仍沿用 Claudian，语义需小心 |
| `src/core/agent/QueryOptionsBuilder.ts` | Gemini CLI args、system prompt file、approval mode、external dirs | CLI-first integration pattern | 依赖 Gemini CLI semantics |
| `src/core/prompts/mainAgent.ts` | Obsidian system prompt、path rules、tool guidance、Plan mode | agent prompt as UX contract | prompt 不能替代 hard gate |
| `src/core/prompts/ollamaAgent.ts` | 本地模型 JSON tool protocol | local model can be tool-using agent | 功能比 Gemini CLI path 更窄 |
| `src/core/agent/OllamaToolExecutor.ts` | Read/LS/Glob/Grep/Write/Edit/LoadSkill and path checks | command-mediated local tool layer | write is vault-only, but still needs mode clarity |
| `src/core/hooks/SecurityHooks.ts` | blocklist and vault restriction PreToolUse hooks | security hook layer | Bash parsing is not full sandbox |
| `src/utils/path.ts` | vault/context/export/none access types | external context vs export path distinction | path policy must be user-visible |
| `src/core/mcp/McpServerManager.ts` | context-saving MCP activation and disabled tools | MCP as on-demand context/tool layer | MCP output remains tool output |
| `src/utils/localSkills.ts` | `.gemini/skills` and global skills | skills as Markdown workflow modules | skill content is instruction, not truth |
| `src/core/storage/StorageService.ts` | `.gemini` split storage and migrations | operational config separated from notes | not a knowledge schema |
| `src/features/inline-edit/InlineEditService.ts` | read-only tool hook + replacement/insertion parse | safer edit preview workflow | generated text still needs user review |

## 当前支线价值

当前支线：

```text
VAKS Agent Gateway / Obsidian workbench / source intake UX
```

它对当前支线：

```text
supports / refines / risk_of
```

具体价值：

- 支持把 agent access 做成可见 UI，而不是隐藏在自动化脚本里。
- 支持把 Plan / Agent 权限、路径分类、MCP 激活、skills/slash/agents 分成不同层。
- 提醒 VAKS 需要比 “Obsidian vault + scripts” 更清楚的工作台入口。

风险：

- 默认 Agent mode 和 cloud Gemini 路径不适合直接照搬。
- external context read/write 和 export write-only 的差别容易被用户误解。
- Bash / MCP / tool execution 仍需更严格的 VAKS quarantine。

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | 可作为轻量 source/workflow entry，不是 truth engine | adapt |
| Dusk workbench | 侧栏、context chips、toolbar、history、settings 很有参考价值 | adapt |
| source ingest | 当前笔记、@file、selection、image、browser/canvas selection 是好入口 | adapt |
| review queue | Plan mode 可作为 review-before-write UX 启发 | adapt |
| schema / reviewed knowledge | 不提供 reviewed schema；不可直接吸收 | no |
| memory / dev context | `.gemini` settings/sessions/skills/agents 是 operational memory | adapt |
| feedback | session/history 可作为 use ledger 原料 | watch |
| retrieval / cache | file context cache、vault file cache 可参考 | watch |
| API / MCP / agent access | MCP context-saving、disabled tools、agent manager、tool executor 强相关 | adapt |
| viewer / workbench | Obsidian-native agent UI 是强参考 | adapt |
| publishing | 仅 export path 边界有间接启发 | watch |
| risk / anti-pattern | prompt/hook/blocklist 不等于完整安全沙箱 | keep as risk |

## 值得提炼的模式

- **Visible Permission Mode**：把 agent 权限显示成用户可切换模式。
- **Command-Mediated Vault Access**：模型只通过受控工具读写 vault。
- **Vault-Local Workflow Config**：commands、skills、agents、MCP、sessions 作为 operational layer。
- **Context Chips / Context Envelope**：当前笔记、选择区、图片、外部目录、MCP 都是可见上下文。
- **MCP Context Saving**：MCP server 可配置为被 mention 时才进入上下文。
- **Inline Edit Preview**：生成替换/插入内容，再由 UI 展示 diff。

## 标签与量化

- domain: obsidian-agent-workbench
- problem: agent access to vault with UI and permissions
- pattern: visible permission + tool gateway + local workflow config
- maturity: emerging
- complexity: high
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 4
- integration_fit: 4
- evidence_strength: 3
- reversibility: 3

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Agent Gateway needs visible permission mode | agent writes cannot directly mutate reviewed truth | refines | VAKS 是否需要 Plan / Candidate Write / Agent Action 三段？ |
| `.gemini` style storage is operational layer | activation tier is not truth tier | supports | VAKS 是否需要 `.vaks/` operational config，与 `wiki/` 分开？ |
| MCP should be on-demand | tool output is not reviewed support | supports | MCP activation 是否需要 context-saving / mention gate？ |
| Inline edit can lower write risk | candidate material not action basis | supports | VAKS source card edit 是否应走 diff preview？ |
| Cloud Gemini path is not local privacy | source provenance is not support | risk_of | VAKS 是否需要 cloud/local model disclosure chip？ |

## Support / Challenge Review

- What supports it: README, manifest, package, architecture docs, service/tool/security/storage source files.
- What challenges it: no live runtime test; no local Obsidian install; some safety is prompt/hook-based; Gemini path sends data to Google API; Bash parser is best-effort.
- Challenge severity: major but bounded.
- Scope limits: Agent Gateway / UI / workbench / operational config only.
- Known risks: authority confusion, cloud privacy misunderstanding, direct agent write, MCP overexposure, external context overreach.
- Review again when: designing VAKS agent gateway or installing/testing Geminese in a real Obsidian vault.
- Action readiness: not_ready.

## 融合判断

- 结论：adapt
- 理由：设计和代码锚点高度贴合 VAKS Agent Gateway，但不适合作为 core truth schema。
- 验证方式：未来做一个小型 VAKS workbench mock，复刻 permission mode、context chips、command-mediated candidate write。

## 直接判断

- Direct use: no
- Fork: no
- Design-only: yes
- Reject: no
- Current branch value: high
- Whole architecture value: medium-to-high
- Risk: medium-high if copied without quarantine
- Next action: keep as P1 reference for Agent Gateway / Workbench design.
