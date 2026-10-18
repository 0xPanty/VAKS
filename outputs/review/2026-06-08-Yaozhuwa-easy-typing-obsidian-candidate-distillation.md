---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
title: "Easy Typing 对 VAKS 的价值是写入摩擦和格式卫生，不是 truth/review"
created_at: "2026-06-08"
created_by: Codex
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
derived_from:
  - raw/repos/2026-06-08-Yaozhuwa-easy-typing-obsidian-source.md
projects:
  - verified-action-knowledge-system
topics:
  - obsidian-editing
  - capture-ergonomics
  - input-rule-engine
  - markdown-formatting
  - mutation-boundary
  - source-integrity
borrow_value: medium
borrow_order: P2
evidence_strength: medium
tags:
  - candidate-only
  - source-distillation
  - design-only
  - vaks-borrow-P2
provisional: true
---

# 候选蒸馏：Easy Typing 对 VAKS 的价值是写入摩擦和格式卫生，不是 truth/review

## 一句话

这个仓库对 VAKS 有帮助，但不是核心帮助。借鉴等级：`P2 / medium`。

说人话：

```text
它不能让知识更可信；
但能让人写 VAKS 笔记更顺手。
```

它适合做“人工写作层”的参考：中英混排、符号输入、代码/公式/双链、粘贴缩进、Tab 跳出、选中文字包裹等。

它不适合进入 VAKS 的 raw/source、reviewed knowledge、decision/action 层，因为自动改写文字本身就可能破坏来源完整性。

## Borrow Tag

```yaml
borrow_value: medium
borrow_order: P2
borrow_scope:
  - authored-note-editing
  - candidate-distillation-writing
  - markdown-input-ergonomics
  - chinese-english-spacing
  - rule-engine-as-ui-helper
  - file-scope-exclusion
  - undoable-editor-mutation
not_borrow_scope:
  - raw source mutation
  - transcript cleanup as evidence
  - reviewed truth
  - reviewed relation
  - truth confidence
  - decision/action basis
  - automatic evidence normalization
  - unrestricted custom JS rules
```

## 它的核心逻辑

Easy Typing 的逻辑是：

```text
用户正在编辑 Markdown
-> 判断当前光标处于 text / formula / code 哪种作用域
-> 根据输入、删除、选中文字输入这三类事件匹配规则
-> 按优先级取第一条命中规则
-> 用一次可撤销的编辑 transaction 替换文本
-> 如果有 tabstop，就把光标放到下一个可填写位置
```

这个逻辑对 VAKS 很清楚：

```text
它是编辑层，不是知识层。
它处理“怎么写得更顺”，不处理“写的东西能不能信”。
```

## 对 VAKS 的帮助

### 1. 降低人写 candidate notes 的摩擦

VAKS 现在大量文件是 Markdown，人写中文和英文、命令、代码、链接、公式、引用块时，确实容易被输入细节打断。

这个插件的中英混排、inline code 快捷输入、选中文字包裹、Tab 跳出，对写候选蒸馏、项目笔记、设计记录有实际帮助。

### 2. 提供一个“规则引擎但不越权”的参考

它的规则结构值得借：

```text
rule_type:
  input
  delete
  selectKey

scope:
  text
  formula
  code
  all

control:
  priority
  enabled
  triggerMode
  file exclusion
  tabstop
```

如果未来 VAKS 做自己的 Obsidian capture helper，可以借这种结构，但要加更硬的 VAKS 边界。

### 3. 提醒我们“自动改写必须可见、可撤销、可排除”

自动格式化不是坏东西，问题是它必须有边界。

对 VAKS 来说，最低要求是：

```text
每次自动改写可 undo；
规则可开关；
raw/evidence 路径默认排除；
规则触发最好可记录；
用户能看懂哪条规则改了什么。
```

## 不能借进核心的原因

Easy Typing 有一个强能力：自定义规则可以用 Function Replacement，底层会把用户输入编译成 JavaScript 函数。

普通写作插件里这是高级功能；但对 VAKS，这是风险能力：

```text
它能生成文本；
它能按匹配结果动态改写；
它可能悄悄改变引用、URL、证据片段、代码、命令、日期。
```

所以它不能直接接触：

```text
raw/videos transcripts
raw/articles snapshots
raw/repos source anchors
evidence packet source spans
reviewed claims
decisions
action-basis notes
```

## Candidate Point

VAKS 可以吸收一个轻量原则：

```text
Editing helpers are allowed to improve authored notes,
but forbidden to mutate provenance-bearing text.
```

对应到中文：

```text
人写的候选笔记可以被辅助；
来源文本、证据文本、审查结论不能被自动美化。
```

## 最小吸收方案

现在不建议改 VAKS core schema，也不建议直接安装到正式 vault。

如果以后试用，建议这样试：

```text
scope:
  只在手写 notes / outputs/review draft / wiki/projects draft 使用。

exclude:
  raw/
  raw/videos/
  raw/repos/
  raw/articles/
  converted documents
  transcripts
  source snapshots
  evidence packets
  reviewed claims
  decisions

disable_or_audit:
  Function Replacement
  imported user rules
  AutoFormatPaste on provenance-bearing files
```

如果未来做 VAKS 自研插件，最小功能应该是：

```text
1. 中英混排和 inline code 快捷输入。
2. source/raw 路径强制排除。
3. 每条自动改写记录 rule_id + before/after range。
4. 用户撤销或关闭规则时写入 usefulness feedback，而不是 truth。
```

## 与现有 VAKS 架构关系

```text
Capture:
  可帮助人工快速输入候选内容，但不能改 raw capture。

Understand:
  可帮助写 candidate distillation，更顺手。

Review:
  不参与 review，不能改变 support/challenge/scope/risk。

Connect:
  可以帮助输入 links，但链接是否为 reviewed relation 仍需 review。

Activation / Context Pack:
  可用于 workbench 编辑体验参考。

Decision / Action:
  不可作为 action basis；自动改写不能参与行动依据。

Use Ledger / Feedback:
  规则是否有用、是否被撤销，可以作为 usefulness feedback。
```

## Risk / Inhibition

```text
risk:
  自动格式化可能改变来源原文。
  自定义 JS 规则可能越权改写。
  粘贴时格式化可能让 source span / evidence range 失效。
  用户可能把“排版更干净”误认为“资料更可靠”。

inhibition:
  raw/source/evidence/reviewed/action 路径默认禁用。
  只允许 authored notes 使用。
  对规则导入和 Function Replacement 做显式确认。
  自动改写必须可撤销，最好可追踪。
```

## 融合判断

```text
fusion_decision: adapt-lightly / optional-use-with-guardrails
borrow_value: medium
borrow_order: P2
evidence_strength: medium
implementation_cost: low for user plugin trial, medium for VAKS-safe helper
integration_fit: medium
reversibility: high if only used on authored notes
```

## 为什么是 P2

不是 P1：

```text
它不解决 VAKS 最核心的 source provenance、evidence support、point collision、reviewed relation、action basis。
```

不是 P3：

```text
VAKS 是 Markdown/Obsidian-heavy 工作流；
人写候选笔记、蒸馏、设计记录时，输入摩擦是真问题。
这个插件提供了成熟的编辑层规则模型和很多中文写作细节。
```

所以它是 P2：值得保留为支持层参考，但必须带 guardrails。

## 直接判断

- Direct use: 可以在测试 vault 或非 raw 文件里试，不建议直接全 vault 启用。
- Fork: 暂不建议。
- Design-only: yes。
- Current branch value: medium。
- Whole architecture value: low-medium。
- Risk: 自动文本变异污染 provenance。
- Next action: 作为 VAKS authored-note editing helper 的 P2 参考；如要实际安装，先设计排除清单和测试样例。
