---
type: source
status: source-captured
title: "sumruler/typora-theme-phycat"
source_id: github-sumruler-typora-theme-phycat
source_uri: https://github.com/sumruler/typora-theme-phycat
source_url: https://github.com/sumruler/typora-theme-phycat
source_type: repository
version_or_commit: b49f1fc6b193e333a3ebb186bbf1ae7f8fc21778
checked_commit: b49f1fc6b193e333a3ebb186bbf1ae7f8fc21778
checked_tag: v2.7.2
commit_time: "2026-03-01T15:58:23+08:00"
captured_at: "2026-06-08"
captured_by: Codex
raw_location: raw/repos/2026-06-08-sumruler-typora-theme-phycat-source.md
snapshot_location: raw/repos/_snapshots/2026-06-08-sumruler-typora-theme-phycat-b49f1fc-source.zip
snapshot_sha256: 5B7BB1D6A427771841AD6BE92D80BB61B52B5AA21A25F071965C564D3C58145C
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
  - typora
  - markdown-theme
  - publishing
  - html-export
  - print-css
  - css-variables
  - visual-design
projects:
  - verified-action-knowledge-system
source_family: markdown-publishing-style
upstream_sources: []
verification_status: primary-source-captured
candidate_relation_suggestions: []
tags:
  - raw-repo
  - github
  - candidate-only
---

# 仓库资料：sumruler/typora-theme-phycat

## 为什么收录

用户要求蒸馏这个 Typora 主题仓库，判断它对 VAKS 是否有帮助。

当前判断：它不是知识系统、不是 Obsidian 插件、不是 evidence/review 工具。它的价值主要在 Markdown 输出的视觉层：标题层级、目录、代码块、callout、任务列表、HTML 导出、打印 CSS、配色变量和主题生成器。

对 VAKS 来说，它只能作为 future `products/`、发布物、导出 HTML/PDF、读者友好样式的低强度参考；不能进入 VAKS core。

## Source Status

```text
Repository: sumruler/typora-theme-phycat
URL: https://github.com/sumruler/typora-theme-phycat
Description: 一款精心打磨过的多色多功能Typora主题
Default branch: main
Checked commit: b49f1fc6b193e333a3ebb186bbf1ae7f8fc21778
Checked tag: v2.7.2
Commit time: 2026-03-01T15:58:23+08:00
Commit subject: 修复选择器错误导致的一体化变白的问题#65
Stars at capture: 826
Forks at capture: 33
Open issues at capture: 16
License: MIT
Archived: false
Snapshot: raw/repos/_snapshots/2026-06-08-sumruler-typora-theme-phycat-b49f1fc-source.zip
Snapshot SHA256: 5B7BB1D6A427771841AD6BE92D80BB61B52B5AA21A25F071965C564D3C58145C
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
| `README.md:17-28` | Defines Phycat as Typora themes with clarity, simplicity, aesthetics, and vividness; light series uses bubbles/lines and dark series uses light/shadow/glassmorphism/neon | Source goal is writing/reading appearance, not knowledge processing | README is product/design claim only |
| `README.md:32-40` | Lists exported HTML demos for 8 light themes and 3 dark themes | Demonstrates output/export surface rather than source intake | Demo links are presentation artifacts |
| `README.md:44-51` | Links Phycat Theme Studio and dark studio for one-click color scheme generation | Theme variables can be productized into a simple customization UI | Online studio is not a VAKS runtime |
| `README.md:55-83` | Features include aesthetics, hierarchy, vividness, details, HTML export optimization, easy customization, feature toggles | Useful for publishing/presentation checklist | Not evidence/review logic |
| `README.md:117-155` | Installation requires copying `phycat` folder and CSS files into Typora theme folder; FAQ covers exported HTML sidebar, font includes, auto-numbering, background image | Typora-specific deployment and export knobs | Not directly compatible with Obsidian vault architecture |
| `phycat-cherry.css:1` | Color theme imports shared `phycat/phycat.light.css` | Separates base structural style from color variables | Good pattern for visual theme maintenance |
| `phycat-cherry.css:33-50` | Auto-numbering and max-width are toggled in color CSS variables/comments | Feature toggles are simple CSS-level switches | Manual toggles are fragile and not semantic state |
| `phycat-vampire.css:1` | Dark theme imports shared `phycat/phycat.dark.css` | Same base/color split for dark series | Visual-only pattern |
| `phycat-vampire.css:35-51` | Dark theme exposes auto-numbering and max-width variables | Shows parity between light/dark themes | Still Typora-specific |
| `phycat/phycat.light.css:17` | `#write` uses `max-width: var(--max-width)` and reading-oriented spacing | Constrained reading width is useful for published VAKS pages | Not schema or knowledge logic |
| `phycat/phycat.light.css:298-495` | CSS counters for h1-h6, outline, and toc auto-numbering | Heading hierarchy can be visually reinforced in exports | Auto numbering may conflict with plugins or document semantics |
| `phycat/phycat.light.css:560-651` | Task list checkbox styling and completion animation | Workbench outputs can visually mark task state | Animation is decorative, not Use Ledger truth |
| `phycat/phycat.light.css:1301-1444` | Styles Typora alert blocks for note/tip/warning/important/caution | Alert visual taxonomy can inspire published docs | VAKS risk/review labels must stay semantic, not just color |
| `phycat/phycat.light.css:1761-1963` | Export sidebar outline and responsive hiding on narrow screens | HTML export with outline is relevant for reader-facing pages | Export UI is not context-pack logic |
| `phycat/phycat.light.css:1974-2077` | Print media rules for A4, print-color-adjust, page-break behavior, avoid breaking headings/pre/figures | Strongest useful part for VAKS publishing/PDF products | Needs real print testing before adoption |
| `Phycat Theme Studio.html:467-614` | UI includes export CSS button, CSS output textarea, copy to clipboard | A small theme-customization workbench exists | Uses browser UI/CDN resources; not VAKS data model |
| `Phycat Theme Studio.html:839-1062` | Generates derived colors, builds CSS content, writes output and copies to clipboard | Color variable generation can be adapted for product theming | Theme generation should remain outside knowledge authority |

## 人话判断

这仓库对 VAKS 的帮助很窄：

```text
它能帮“怎么把 Markdown 导出去给人看”；
不能帮“怎么判断资料能不能信”。
```

如果以后 VAKS 要把某些 reviewed summary、产品说明、公开报告导出成 HTML/PDF，它有一点参考价值：标题层级、目录、打印分页、代码块、alert 样式、配色变量。

但如果问它对 VAKS core 有没有帮助，答案基本是：没有。

## 可抽取 Candidate Points

- VAKS 的发布层可以和知识层分离：Markdown truth core 不需要好看，reader-facing product 可以有主题。
- 视觉层可用 CSS variables 做低成本定制，但不能让颜色、卡片、动画、编号替代 semantic status。
- HTML/PDF 导出要单独考虑 print CSS、page break、outline sidebar、code/table/alert readability。
- 发布主题应该是 reversible skin，不应写回 raw/source/reviewed/action records。

## 可借鉴

- Base style + color theme split：结构样式和配色变量分离。
- 导出优化：HTML outline sidebar、print media、A4 page rule、page-break 防断裂。
- 标题层级视觉化：h1-h6、TOC、outline 有一致编号/样式。
- Theme Studio：用小工具生成 CSS variables，降低配色成本。
- Reader-facing docs 可以有 light/dark 多主题，而 VAKS 内核保持朴素。

## 不能直接借鉴

- 不把 Typora theme 当 VAKS vault theme 或 Obsidian 插件。
- 不把视觉状态当 review status、risk status、truth confidence。
- 不把自动编号当知识编号或 claim id。
- 不让背景、动画、毛玻璃、霓虹风格污染严肃审查页面。
- 不把在线 Theme Studio / CDN 字体作为 VAKS 发布默认依赖。
- 不在 raw/source/evidence 文件上应用会改变可读锚点的导出样式结论。

## 风险和不确定

- 本轮没有安装 Typora、没有真实导出 HTML/PDF 验证。
- 仓库是 Typora 主题，不是 Obsidian theme；直接迁移到 VAKS/Obsidian 不成立。
- 丰富装饰和动画可能让审查类文档显得过度包装。
- Auto-numbering 可能和已有编号插件或文档编号冲突，README FAQ 也提到编号插件冲突。
- Print CSS 看起来完整，但实际分页、字体、中文排版仍需样张测试。

## VAKS 归位

```text
Capture:
  无直接价值；不要影响 raw/source capture。

Understand:
  无直接价值；最多让手写说明更易读。

Review:
  不参与 review；颜色和 alert 样式不能成为 evidence/risk 判断。

Connect:
  无直接关系；目录/outline 只是阅读导航。

Activation / Context Pack:
  可作为 reader-facing context pack export 的外观参考。

Decision / Action:
  不可作为 action basis。

Use Ledger / Feedback:
  可记录导出样式是否被用户认为易读，但不改变 truth。

Publishing / Products:
  这是最相关的位置：HTML/PDF theme, print CSS, public report styling。
```

## 融合判断

- Direct use: no
- Fork: no
- Design-only: yes
- Current branch value: low
- Whole architecture value: low
- Borrow value: low
- Borrow order: P3
- Evidence strength: medium for theme structure, low for VAKS fit
- Risk: aesthetic layer confused with semantic/review layer
- Next action: 仅作为 future products / publishing theme 参考；当前不改 VAKS core
