---
type: source
status: source-captured
title: "Yaozhuwa/easy-typing-obsidian"
source_id: github-Yaozhuwa-easy-typing-obsidian
source_uri: https://github.com/Yaozhuwa/easy-typing-obsidian
source_url: https://github.com/Yaozhuwa/easy-typing-obsidian
source_type: repository
version_or_commit: 0fa3d1ad4058e0c900854741b40f8d30fb072d35
checked_commit: 0fa3d1ad4058e0c900854741b40f8d30fb072d35
commit_time: "2026-05-18T21:39:06+08:00"
captured_at: "2026-06-08"
captured_by: Codex
raw_location: raw/repos/2026-06-08-Yaozhuwa-easy-typing-obsidian-source.md
snapshot_location: raw/repos/_snapshots/2026-06-08-Yaozhuwa-easy-typing-obsidian-0fa3d1a-source.zip
snapshot_sha256: B553844B1F822259D91423595518432F18D45381B833817EC65D85105142D6DC
processing_mode: immediate
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
access_boundary: public
source_status: active
license: MIT
topics:
  - obsidian
  - typing-enhancement
  - markdown-editing
  - auto-formatting
  - rule-engine
  - cjk-writing
  - capture-ergonomics
projects:
  - verified-action-knowledge-system
source_family: obsidian-editing-ergonomics
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions: []
tags:
  - raw-repo
  - github
  - candidate-only
---

# 仓库资料：Yaozhuwa/easy-typing-obsidian

## 为什么收录

用户要求蒸馏这个 Obsidian 插件，判断它对 VAKS 是否有帮助。

当前判断：它不是 VAKS 的知识审查、证据支持或 action-basis 参考；它的价值在 Obsidian 写作体验和 capture ergonomics。它可以降低中英混排、符号输入、成对符号、代码/公式输入和粘贴时的摩擦，但也有自动改写 raw source 的风险。

## Source Status

```text
Repository: Yaozhuwa/easy-typing-obsidian
URL: https://github.com/Yaozhuwa/easy-typing-obsidian
Description: This is a plugin of obsidian for users writing in an easy way.
Default branch: master
Checked commit: 0fa3d1ad4058e0c900854741b40f8d30fb072d35
Commit time: 2026-05-18T21:39:06+08:00
Commit subject: 6.0.8
Manifest version: 6.0.8
License: MIT
Stars at capture: 731
Forks at capture: 22
Open issues at capture: 48
Archived: false
Snapshot: raw/repos/_snapshots/2026-06-08-Yaozhuwa-easy-typing-obsidian-0fa3d1a-source.zip
Snapshot SHA256: B553844B1F822259D91423595518432F18D45381B833817EC65D85105142D6DC
```

## Capture Boundary

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

Repository source records provide provenance, anchors, and candidate extraction
input. They do not create reviewed architecture decisions or action basis.

## Files / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:9-70` | README says the plugin improves Obsidian writing through automatic text formatting, smart editing enhancements, and a rule engine; quick-start lists auto-spacing, CJK punctuation, auto-pairing, inline code shortcut, Tabout, Smart Backspace | The project is an editor ergonomics plugin, not a knowledge architecture system | README is feature documentation, not a guarantee of safety in VAKS raw/source folders |
| `manifest.json:1-8` | Obsidian plugin id `easy-typing-obsidian`, version `6.0.8`, min app version `0.15.0`, desktop-only false | Confirms plugin identity, version, and mobile compatibility intent | Manifest metadata is not runtime validation |
| `src/main.ts:39-72` | `onload` loads settings, initializes `RuleManager`, defines tabout pairs, registers CodeMirror transaction filter, view update plugin, and tabstop field | Plugin integrates at editor transaction/update layer | Any similar VAKS capture helper would need hard file-scope exclusions |
| `src/main.ts:74-180` | Registers keymaps and commands: Tab, Enter, Backspace, Mod-A, format article/selection, delete blank lines, insert code block, toggle autoformat, toggle comment | Editing commands are thin affordances around Markdown writing | These are user-editing aids, not review gates |
| `src/rule_engine.ts:17-75` | Defines `RuleType` Input/Delete/SelectKey, `RuleTriggerMode`, `RuleScope`, `ConvertRule`, `TxContext`, `ApplyResult` | Clear rule model: type, trigger, scope, language, priority, replacement, match range | Good design pattern for UI-level transformations only |
| `src/rule_engine.ts:120-139` | Parses option flags into type, trigger mode, regex/function flags, and scope | Compact rule encoding with explicit execution scope | Option strings are convenient but need auditability if used for VAKS |
| `src/rule_engine.ts:232-250` | Function replacement compiles user-supplied JS with `new Function` when `F` flag is present | Powerful custom automation | Security / integrity risk; should not touch raw source, reviewed, or action layers |
| `src/rule_engine.ts:524-566` | `process` sorts and executes first matching enabled rule, checks type, trigger mode, scope, and code language | First-match priority and scope gating are reusable interaction ideas | Priority conflicts can still cause unexpected rewrites |
| `src/rule_processor.ts:9-49` | `triggerCvtRule` detects current rule scope, optionally respects user-defined regex blocks, runs the engine, dispatches one editor change with tabstop effects | Good local editor transaction boundary; transformations are visible and undoable | Still mutates text; provenance-sensitive text must be excluded |
| `src/cm_extensions.ts:28-122` | Transaction filter handles selected text replacement, code-block paste indentation, and list/quote smart paste | Shows a centralized edit interception pipeline | Edit interception is not suitable for VAKS truth/review mutation |
| `src/cm_extensions.ts:398-437` | Shared input pipeline triggers conversion rule, then auto-format, with file exclusion and line-type checks | Useful pattern: pipeline + exclusions + scope checks | Exclusions must be stricter for VAKS than for ordinary notes |
| `src/cm_extensions.ts:450-553` | View update listener clears tabstops, tracks IME compose, skips tables, ignores undo/redo/EasyTyping events, handles paste formatting | Mature handling of typing edge cases | Complexity is high; VAKS should not reimplement unless needed |
| `src/syntax.ts:208-225` | `detectRuleScope` maps position to formula, code with language, or text | Scope-aware rule execution avoids changing code/math unexpectedly | Raw source snippets may still be plain text and need path-based exclusion |
| `src/rule_manager.ts:52-90` | Initializes `builtin-rules.json` and `user-rules.json`, merges built-ins, stores rules in plugin directory or custom path | Rules are explicit files and can be imported/exported | Rule files become another mutable config surface |
| `src/default_rules.ts:12-149` | Built-in rules for CJK autopair, punctuation conversion, inline code/formula shortcuts, delete pairs, selected-text wrapping, quote handling | Practical Chinese Markdown input patterns | Some rules can rewrite evidence text; use only in authored notes |
| `src/settings/settings_types.ts:52-92` | Defaults enable Tabout, SmartPaste, BetterCodeEdit, BetterBackspace, AutoFormat, AutoFormatPaste; define language pairs and regex blocks for URLs/tags/callouts | Good defaults for general writing | VAKS raw/source folders need opt-out defaults |
| `Doc/CustomRules.md:237-249` | Docs explain function replacement runs JavaScript function body with match parameters | Confirms the power/risk of custom rules | This is the main safety reason not to treat the plugin as harmless infrastructure |
| `Doc/AutoFormatting.md:150-160` | Docs say auto-formatting excludes code blocks, math blocks, and frontmatter | Some built-in structural exclusions exist | VAKS still needs file/folder exclusions for raw transcripts, source cards, evidence snippets |

## 人话判断

这是一个“让人写 Markdown 更顺手”的 Obsidian 插件，不是“让知识更可信”的插件。

它能帮 VAKS 的地方：

```text
少切输入法；
中英混排更干净；
输入代码、公式、双链、引用更快；
粘贴列表/代码块更不乱；
把常用输入动作做成规则。
```

它不能帮 VAKS 的地方：

```text
不能判断资料真假；
不能创建 reviewed relation；
不能提升 confidence；
不能作为 action basis；
不能保证 raw source 没被改写。
```

## 可抽取 Candidate Points

- VAKS 的正式知识系统不应该自动改写 raw source，但可以在用户写 candidate / summary / project notes 时提供轻量输入辅助。
- 如果 VAKS 未来做 Obsidian 编辑辅助，规则必须有 `scope`、`priority`、`file/path exclusion`、`undoable transaction`、`visible rule id` 和 `mutation ledger`。
- 中英混排、URL/tag/callout/inline code/formula 的格式卫生属于 capture ergonomics，不属于 evidence support。
- 自定义 Function Replacement 很强，但对 VAKS 是高风险能力；默认应禁用或隔离。

## 可借鉴

- Rule type：Input / Delete / SelectKey。
- Scope：Text / Formula / Code / All，加 code language。
- Priority：先匹配高优先级规则，first match wins。
- Tabstop：自动插入后让用户继续补字段。
- File exclusion：按路径排除自动格式化。
- User-defined regex blocks：保护 URL、tag、callout、模板表达式等不被打散。
- One transaction / undoable edit：自动改写必须可撤销。

## 不能直接借鉴

- 不让自动格式化进入 `raw/` source card、transcript、converted document、snapshot、evidence anchor。
- 不把输入美化当作资料清洗或证据规范化。
- 不让自定义 JS 规则接触 reviewed knowledge、decision、action basis。
- 不把插件安装本身当成 VAKS 架构升级。
- 不复制它的全部编辑行为；VAKS 只需要少量 guardrail-aware rules。

## 风险和不确定

- 本轮没有在 Obsidian 内实际安装运行，只做源码/文档审查。
- 开放 issues 数较多，具体兼容性和 bug 需要实测。
- 自定义 function replacement 使用 `new Function`，对普通插件是灵活性，对 VAKS 则是写入完整性风险。
- 自动格式化对 raw 引文、源码片段、ASR 转写和 evidence ranges 可能造成不可接受的细微变动。

## VAKS 归位

```text
Capture:
  可作为人工输入辅助，特别是中文 Markdown 笔记和 candidate notes。

Understand:
  可降低写 summary / candidate distillation 的摩擦。

Review:
  不参与 review；不能改变 support / challenge / confidence。

Connect:
  可以辅助双链、代码/公式输入，但 relation_state 仍由 VAKS review 决定。

Activation / Context Pack:
  可作为 workbench 编辑体验参考。

Decision / Action:
  不可作为 action basis；自动规则不能生成行动依据。

Use Ledger / Feedback:
  若未来自研编辑辅助，规则触发和用户撤销可作为 usefulness feedback，而不是 truth mutation。
```

## 融合判断

- Direct use: possible for personal authored notes only, after exclusion rules
- Fork: no
- Design-only: yes
- Current branch value: medium
- Whole architecture value: low-medium
- Borrow value: medium
- Borrow order: P2
- Evidence strength: medium for plugin design, low for VAKS safety without local runtime test
- Risk: automatic text mutation and custom JS rule execution
- Next action: 不安装、不启用自动化；先作为 P2 编辑体验参考。若要试用，先在非核心 vault 或测试文件里验证，并排除 VAKS raw/evidence 路径
