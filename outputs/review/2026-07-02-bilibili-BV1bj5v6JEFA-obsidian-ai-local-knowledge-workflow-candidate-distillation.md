---
type: candidate-distillation
record_kind: candidate_distillation
source_id: bilibili-BV1bj5v6JEFA
source_card: raw/videos/2026-07-02-bilibili-BV1bj5v6JEFA-obsidian-ai-local-knowledge-workflow-source.md
title: Obsidian + Claude Code + DeepSeek 的 AI 内容加工工作台
created: 2026-07-02
captured_by: Codex
processing_tier: medium
knowledge_status: candidate
overlay_state: none
review_pressure: none
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
---

# Obsidian + Claude Code + DeepSeek 的 AI 内容加工工作台

## 主要思路

说人话：这个视频的核心不是“搭一个可信知识系统”，而是“把 Obsidian 变成一个 AI 工作台”。它把 Claude Code 接上 DeepSeek API，再通过 Obsidian 插件把命令行 / Claude Code 对话嵌进 vault，最后用 Web Clipper、字幕抓取、翻译整理、Excalidraw 白板生成，形成一条从外部内容到 Obsidian 笔记/白板的加工流水线。

它的主线可以压成一句：

```text
外部内容进 Obsidian -> AI 按本库规则整理 -> 生成可读笔记或白板 -> 人再编辑/使用。
```

这个方法很适合“内容收集和整理效率”，但不解决“这些内容是否可靠、是否可作为行动依据”的问题。对 VAKS 来说，它是工作台参考，不是 truth core 参考。

## 视频结构

1. 安装 Claude Code，并通过第三方模型切换工具接入 DeepSeek API。
2. 用 Obsidian 插件把 AI 接入 vault：一种是内嵌终端，另一种是更像对话侧栏的 Claudian。
3. 用 Obsidian Web Clipper 保存网页 / 字幕内容，再让 AI 翻译、格式化、移动归档。
4. 用 Excalidraw + skill 让 AI 把整理后的内容生成手绘风格白板。

## 转录与可靠性

- 获取方式：Bilibili public metadata -> no public subtitle -> public audio -> local ASR。
- ASR：faster-whisper small / cuda。
- 可靠性：工作流主线清楚；英文工具名、插件名、命令、仓库地址需要画面或官方页面核验。
- 明显 ASR 问题：Claude Code -> Cloud Code；DeepSeek -> Deepseq / DeepSync；GitHub -> Gatehub；Excalidraw -> XCaliger / Excalator；skill -> SQL / Scale。
- 不使用：cookie、私有收藏、会员内容、云 API。

## 反漏提取检查

| 维度 | 提取 |
|---|---|
| Pain point | 内容进入 Obsidian 后仍需要手动翻译、总结、整理、改名、归档、做白板，流程碎片化。 |
| Workflow | Claude Code + DeepSeek 配置 -> Obsidian 插件接入 -> Web Clipper/字幕保存 -> AI 按规则整理 -> Excalidraw 生成白板。 |
| Tools / plugins | Claude Code、DeepSeek API、CCSwitch 类模型切换工具、Obsidian Terminal/Claudian、Obsidian Web Clipper、Excalidraw、Excalidraw Diagram skill。 |
| Information structure | 每个 vault / 项目用 `Claude.md` 一类规则文件约束 AI 输出、目录结构、翻译规范和归档路径。 |
| Judgment mechanism | 主要靠用户在 `Claude.md` 中写规则，以及 AI 按当前打开文档执行任务；不是证据审查机制。 |
| User experience | 优点是少切应用、整理速度快；缺点是依赖本地工具、API key、插件兼容和 AI 执行稳定性。 |
| Automation boundary | 自动化的是整理/翻译/归档/白板生成；可靠性判断和行动授权仍需人或后续审查。 |
| Risks | API key 暴露、插件权限、AI 误改 vault、ASR/网页剪藏误读、自动归档制造“看似整理好”的假权威。 |
| VAKS fit | 适合 UI/workbench、Capture、Understand、Activation；不适合直接进入 Review/Decision/Action。 |
| Challenge | 说明 VAKS 若只强调严格 review，可能缺一个顺手的前端工作台；但工作台不能越权成 truth。 |

## Candidate Points

### CP1: Obsidian 可以作为 AI 工作台，而不只是笔记仓库

- anchor: `raw/videos/2026-07-02-bilibili-BV1bj5v6JEFA-obsidian-ai-local-knowledge-workflow-source/segments.md` 00:00-00:41
- claim_type: workflow_pattern
- candidate_value: 把 Claude Code / DeepSeek、网页剪藏、字幕整理、白板生成统一放在 Obsidian 中执行。
- confidence: medium
- VAKS fit: UI/workbench + Capture/Understand 辅助。

### CP2: 内嵌终端让 Claude Code 在当前 vault 路径下工作

- anchor: `raw/videos/2026-07-02-bilibili-BV1bj5v6JEFA-obsidian-ai-local-knowledge-workflow-source/segments.md` 01:54-03:14
- claim_type: integration_pattern
- candidate_value: 终端插件把命令行上下文放到当前知识库目录，便于读取文章、统计、写文案、安装 skill。
- confidence: medium
- risk: 这也扩大了误读/误写 vault 的风险，必须有权限和边界控制。

### CP3: Claudian 类插件提供更贴近笔记场景的 AI 对话侧栏

- anchor: `raw/videos/2026-07-02-bilibili-BV1bj5v6JEFA-obsidian-ai-local-knowledge-workflow-source/segments.md` 03:15-04:28
- claim_type: ux_pattern
- candidate_value: 相比纯终端，对话式插件更像 Obsidian 内部 AI 助手，并可默认使用当前打开文档。
- confidence: medium
- review_need: 插件名、能力、权限和当前可用性需以官方仓库/插件市场核验。

### CP4: `Claude.md` / 项目规则文件是工作台质量的关键

- anchor: `raw/videos/2026-07-02-bilibili-BV1bj5v6JEFA-obsidian-ai-local-knowledge-workflow-source/segments.md` 04:27-05:02
- claim_type: governance_hint
- candidate_value: 通过规则文件指定仓库定位、目录结构、输出规范、翻译规范，让 AI 在 vault 内按本地规则工作。
- confidence: medium
- VAKS fit: 和本项目 `AGENTS.md` / handoff / local manuals 的“入口约束”方向一致。

### CP5: Web Clipper + AI 整理把外部内容变成可读笔记

- anchor: `raw/videos/2026-07-02-bilibili-BV1bj5v6JEFA-obsidian-ai-local-knowledge-workflow-source/segments.md` 05:02-06:23
- claim_type: capture_to_understand_pattern
- candidate_value: 保存网页或字幕为 Markdown 后，让 AI 翻译、格式化、重命名、移动归档。
- confidence: medium
- risk: 这是 candidate comprehension，不是证据支持；自动整理会让未经核验内容显得更可信。

### CP6: AI 生成 Excalidraw 白板适合做可视化理解层

- anchor: `raw/videos/2026-07-02-bilibili-BV1bj5v6JEFA-obsidian-ai-local-knowledge-workflow-source/segments.md` 06:25-07:36
- claim_type: visualization_pattern
- candidate_value: 用 skill 让 AI 根据内容生成手绘风格画布，适合章节、对比、概念图。
- confidence: medium
- VAKS fit: 可作为 activation / explanation view，不作为 reviewed relation graph。

## VAKS 层级归位

- Capture：网页、字幕、视频内容进入 Obsidian。
- Understand：AI 翻译、格式化、总结、主题筛选。
- UI/workbench：Obsidian 侧栏、终端、白板统一操作。
- Activation：`Claude.md` 规则文件让 AI 读取当前 vault 结构和规范。
- Review：视频本身没有完整 review 机制，只能作为 review input 的前置整理。
- Decision / Action：不能直接作为 action basis。
- Use Ledger / Feedback：若未来采用，应记录 AI 改了哪些文件、用户是否满意、是否误归档。

## 可借鉴

- “AI 工作台”思路值得借：把获取、整理、可视化放在一个操作面里，降低切换成本。
- `Claude.md` / 项目规则文件是关键：这和 VAKS 的本地 manuals、handoff、边界文档同向。
- Web Clipper + AI 整理可作为轻量 capture/understand 流程，但必须保持 candidate-only。
- Excalidraw 白板可作为解释/激活视图，不要当成知识图谱或 reviewed relations。

## 不能借鉴

- 不能把自动翻译/格式化后的笔记当 reviewed knowledge。
- 不能让 AI 在正式 vault 中无边界写文件、移动文件、安装 skill。
- 不能把插件 UI、白板、对话历史当成 evidence support。
- 不能因为整合顺手，就跳过 source provenance、candidate/review/action 分层。

## Truth-Boundary 风险

这个视频最大的风险是“顺滑工作流制造假确定感”：网页、字幕、AI 总结、白板一旦整理得漂亮，就容易被误当作已经理解、已经验证、可以行动。VAKS 应该吸收它的工作台体验，但保留自己的边界：

```text
剪藏/字幕 = raw source
AI 整理 = candidate comprehension
白板 = explanation / activation view
reviewed knowledge = 后续 evidence-aware review
action basis = 后续 action-facing gate
```

## 最小吸收建议

暂不改 schema，不改正式流程。把它作为“Obsidian AI 工作台参考”进入候选层。后续如果要吸收，建议只做一个 disposable vault / sandbox 演示：限制 AI 只能读写指定文件夹，记录操作 ledger，测试 Web Clipper -> AI 整理 -> Excalidraw 画布的闭环。

## 是否建议进入 REVIEW_QUEUE

建议暂不进入 reviewed queue。只有当我们要实际引入 Obsidian 插件、Claude Code vault 写入、或 Excalidraw 自动画布生成时，再创建 review_due 项，重点审权限边界、可回滚性和操作 ledger。
