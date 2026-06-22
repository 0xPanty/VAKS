---
type: candidate_distillation
record_kind: candidate_distillation
status: draft
title: "Phycat Typora 主题对 VAKS 的价值在发布外观，不在知识系统"
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
  - raw/repos/2026-06-08-sumruler-typora-theme-phycat-source.md
projects:
  - verified-action-knowledge-system
topics:
  - typora-theme
  - publishing
  - html-export
  - pdf-export
  - print-css
  - reader-facing-docs
  - visual-layer-boundary
borrow_value: low
borrow_order: P3
evidence_strength: medium
tags:
  - candidate-only
  - source-distillation
  - design-only
  - vaks-borrow-P3
provisional: true
---

# 候选蒸馏：Phycat Typora 主题对 VAKS 的价值在发布外观，不在知识系统

## 一句话

这条对 VAKS 是 `P3 / borrow_value: low`。

人话：

```text
它能帮 VAKS 的“成品长得更好看”；
不能帮 VAKS 的“知识更可信”。
```

它值得留，但只放在 future `products/` / publishing / HTML-PDF export 参考里。不要把它吸收到 raw、review、truth、action-basis core。

## Borrow Tag

```yaml
borrow_value: low
borrow_order: P3
borrow_scope:
  - publishing-theme
  - html-export-style
  - pdf-print-css
  - reader-facing-reports
  - theme-variable-split
  - visual-hierarchy
not_borrow_scope:
  - source intake
  - candidate extraction
  - reviewed knowledge
  - evidence support
  - truth confidence
  - reviewed relation
  - action basis
  - semantic status from color
```

## Candidate Point

VAKS 需要把两个东西分开：

```text
knowledge layer:
  raw / candidate / reviewed / decision / action basis
  目标是可追溯、可审查、边界清楚。

presentation layer:
  HTML / PDF / public report / product docs
  目标是好读、好看、好分享。
```

Phycat 只属于第二层。

## 可以借

- **结构样式和配色分离**：`phycat.light.css` / `phycat.dark.css` 是基础样式，单个主题 CSS 只 import base 并设置变量。
- **导出时仍保留导航**：HTML export sidebar / outline 的处理可参考。
- **打印 CSS**：A4、page-break、print-color-adjust、标题/代码/图片避免断裂，这些对 PDF 成品有用。
- **标题层级视觉化**：h1-h6、TOC、outline 统一处理，适合公开文档读者。
- **Theme Studio**：用小工具生成 CSS variables，适合作为未来产品主题生成器灵感。

## 不能借

- 不借 Typora-specific 主题作为 VAKS/Obsidian 主题。
- 不让颜色、alert、卡片、动画表达 review status。
- 不把 CSS 自动编号当 claim id / source id / evidence id。
- 不把漂亮导出当知识质量。
- 不让装饰风格影响审查文档的严肃性和可读锚点。

## 对 VAKS 的最小吸收

现在不改 schema，不改 vault 主题。

未来如果做 `products/`，可以开一个非常薄的发布层：

```text
source markdown:
  保持 VAKS 原始结构和边界。

export renderer:
  读取已允许发布的 summary / report。
  套一个 reader-facing CSS。
  明确显示 layer/status/provenance。
  不写回 reviewed knowledge。
```

如果要借 Phycat，最小只借这些原则：

```text
base-css + theme-variables
print-css
html-outline-sidebar
semantic labels before color
```

## VAKS 层级归位

```text
Capture:
  无直接价值，不影响 raw/source。

Understand:
  无直接价值，最多让说明文档更好读。

Review:
  不参与 review；视觉样式不能表达证据支持。

Connect:
  目录和 outline 是阅读导航，不是 reviewed relation。

Activation / Context Pack:
  可以作为导出 context pack/report 的视觉层参考。

Decision / Action:
  不可作为 action basis。

Use Ledger / Feedback:
  可记录用户是否觉得导出报告易读。

Publishing / Products:
  最相关。用于公开报告、产品文档、PDF/HTML 样式参考。
```

## Risk / Inhibition

```text
risk:
  好看的主题容易让候选材料显得更成熟。
  颜色和 alert 样式容易被误解成风险/置信度。
  自动编号可能和 VAKS id / claim id 混淆。
  Typora 导出依赖和 Obsidian/VAKS 工作流不一致。
  装饰性动画会降低审查场景的严肃感。

inhibition:
  只用于发布层。
  source/review/action 文件不套装饰主题。
  semantic status 必须用文字/字段表达，颜色只能辅助。
  导出层不写回 vault truth core。
```

## 融合判断

```text
fusion_decision: watch / design-only
borrow_value: low
borrow_order: P3
evidence_strength: medium
implementation_cost: low for visual prototype, medium for robust export pipeline
integration_fit: low-medium
reversibility: high
```

## 为什么是 P3

不是 P1/P2：

```text
它不解决 VAKS 的 source provenance、candidate/reviewed 边界、evidence support、point collision、action basis。
```

仍然值得留：

```text
VAKS 未来如果要输出给别人看，就需要一个“发布外观层”。
Phycat 在 HTML/PDF/print CSS/目录/主题变量上有可看的小模式。
```

## 后续行动

- 当前不安装 Typora 主题，不改 Obsidian vault theme。
- 当前不进入 `wiki/patterns` 或 `wiki/decisions`。
- 如果未来做 VAKS `products/` 或 public report，可重新打开本 source 做 export-theme review。
