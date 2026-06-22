---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
source_ref: raw/articles/2026-06-13-flexnote-docs-source.md
derived_from:
  - https://wiki.myflexnote.com/docs/intro
  - https://wiki.myflexnote.com/docs/tutorial-basics/card
  - https://wiki.myflexnote.com/docs/tutorial-basics/whiteboard
  - https://wiki.myflexnote.com/docs/tutorial-basics/tag
  - https://wiki.myflexnote.com/docs/tutorial-basics/Highlight
  - https://wiki.myflexnote.com/docs/tutorial-basics/reference
  - https://wiki.myflexnote.com/docs/cloud-sync
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
borrow_value: strong
borrow_order:
  - "P1: card as reusable information atom separated from visual/workspace contexts"
  - "P1: PDF/video/web annotations become source-location cards"
  - "P2: infinite whiteboard as project workbench or context-pack viewer"
  - "P2: tag database as review/dashboard UI, not truth schema"
  - "P3: journal/tabs/shortcuts/import-export/sync as usability references"
avoid:
  - "Do not treat visual arrows, backlinks, boards, or tags as reviewed relations."
  - "Do not let auto-generated annotation cards become reviewed knowledge."
  - "Do not replace VAKS Markdown/YAML schema with tag database fields."
  - "Do not make infinite canvas the core architecture."
  - "Do not treat third-party sync or export as provenance integrity."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "building VAKS visual workbench, source-annotation adapter, context-pack viewer, or review dashboard"
  support_when: "discussing card-based UI, source highlights, active project surfaces, review queue UX, or visual relation navigation"
  risk_when: "visual organization, tags, or links might be mistaken for reviewed knowledge or evidence support"
  cold_references:
    - raw/articles/2026-06-13-flexnote-docs-source.md
    - raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md
routing_hint:
  - visual_workbench
  - source_annotation_adapter
  - context_pack_viewer
  - review_dashboard
  - activation_not_truth
possible_project_refs:
  - VAKS
point_anchor_refs:
  - raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md
tags:
  - candidate
  - provisional
  - flexnote
  - visual-pkm
  - card-system
  - reusable-card
  - whiteboard-workbench
  - tag-database
  - annotation-to-card
  - source-anchor
  - candidate-only
---

# Candidate Distillation: FlexNote Docs

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 说人话结论

FlexNote 的核心思路可以提炼，而且挺适合我们借“外壳”。

它不是 VAKS 这种可信知识系统。它更像：

```text
卡片 = 知识原子
白板 = 多视角工作台
标签 = 小数据库
标注 = 从 PDF / 视频 / 网页里抽片段变卡片
链接/箭头 = 导航和可视化关系
本地优先 + 第三方同步 = 数据可控
```

对 VAKS 来说，FlexNote 最值得借的是视觉工作台和材料标注入口，不是知识可信逻辑。

## Source

```yaml
source_ref: raw/articles/2026-06-13-flexnote-docs-source.md
retained_notes: raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md
```

## Candidate Points

### 1. 卡片是统一信息原子

FlexNote 把笔记、PDF、视频、网页、图片、音频、附件、标注、脑图节点都统一成 card。

这个设计有一个很强的点：

```text
内容本体
!=
展示位置
```

同一张卡片可以出现在多个白板里，编辑一次，多处引用同步。

VAKS 可借：

```text
source card
candidate point
evidence packet
review queue item
feedback event
context pack item
```

都可以在 UI 上表现成“卡片”，但底层仍然是 Markdown/YAML 文件。

边界：

```text
card 是 UI 和操作单元，不是 truth 单元。
```

### 2. 白板是多视角工作台，不是知识图谱本体

FlexNote 的 whiteboard 是无限画布：拖卡片、嵌套、连线、缩放、导航、自动布局、导出。

这对 VAKS 很有启发：

```text
review board
source investigation board
project context board
decision comparison board
context pack board
```

但必须守住边界：

```text
白板连线 = 视觉导航 / 候选关系
reviewed relation = 另一个经过证据审查的对象
```

不能因为两个卡片在白板上被箭头连起来，就认为它们真的 supports / contradicts。

### 3. 标签数据库是好 UI，不是 VAKS schema

FlexNote 的 tags 不是普通标签，而是带字段、关系、视图、过滤和排序的小数据库。

VAKS 可借：

```text
review queue view
source intake dashboard
candidate status board
project material board
promotion readiness view
stale / review_due view
```

但不能借成：

```text
tag field = reviewed schema
tag relation = reviewed relation
kanban status = review result
```

最稳的融合方式：

```text
Markdown/YAML 仍是源数据
tag database / Bases / table / board 只是展示和操作层
```

### 4. PDF / 视频 / 网页标注自动变卡片，是最有价值的源材料入口

FlexNote 最值得 VAKS 借的点之一，是把 PDF highlight、video timestamp annotation、web clip 自动生成卡片。

VAKS 翻译版：

```text
PDF text highlight
-> source_anchor candidate
-> candidate point
-> evidence packet input

video timestamp note
-> transcript segment / frame anchor
-> candidate point
-> review queue item

web clip
-> raw source card
-> extracted passage
-> candidate distillation
```

这个比“把整篇文章总结一下”更高级，因为它保留了位置线索。

边界：

```text
highlight card = source anchor / candidate input
not reviewed evidence by itself
```

### 5. `@` 双链和视觉箭头适合作 activation，不适合作 support

FlexNote 通过 `@` 引用、backlinks、白板箭头建立知识网络。

VAKS 可借：

```text
related context discovery
association neighborhood activation
context pack navigation
source-to-candidate drilldown
```

但不能借成：

```text
link exists -> relation reviewed
arrow exists -> supports
backlink count high -> more true
```

这正好强化我们之前的边界：

```text
retrieval / graph / link = activation
reviewed relation = evidence-aware review 后才成立
```

### 6. Journal 和 Tabs 是 active workbench 的入口

FlexNote 的 Journal 是每天自动生成的日期卡片，Tabs 是当前打开材料的工作区。

VAKS 可借：

```text
daily capture
project session log
current review tabs
active context pack surface
reading / review / decision 工作区
```

这对体验很重要：VAKS 现在架构强，但入口偏硬。Journal/Tabs 这类东西能让用户自然进入系统。

边界：

```text
daily log / active tab = working context
not reviewed knowledge
not feedback truth mutation
```

### 7. Local-first + third-party sync 是好姿态，但要补完整性

FlexNote 文档强调本地优先、第三方云同步、导入导出。

VAKS 可借：

- local-first；
- 不绑定自家云；
- WebDAV/S3/Git-like sync 的思路；
- Markdown/PDF/HTML export；
- offline-friendly workflow。

但 VAKS 还要补：

- source hash；
- sync hash verification；
- conflict record；
- source identity；
- action receipt；
- reviewed-layer protection。

## 和 VAKS 的关系

| VAKS layer | FlexNote idea | Fit |
|---|---|---|
| Capture / Provenance | web/PDF/video import and highlights | strong if anchors retained |
| Candidate Comprehension | annotation cards and card reuse | useful as candidate point surface |
| Point Collision | visual boards can show conflicts | only UI; not logic |
| Review / Consolidation | tag views can show queues | missing review authority |
| Reviewed Relations | bidirectional links/arrows | must remain candidate/activation |
| Activation / Dev Context | tabs, journal, whiteboard, reusable cards | strong |
| Context Pack | board of relevant cards | strong viewer concept |
| Decision / Action | no action basis logic | weak |
| Feedback | no VAKS-style feedback ledger | weak |
| Risk | visual relation can create false authority | important warning |

## 标签与量化

- domain: visual_pkm / local_first_note_app / canvas_workspace
- problem: visual_knowledge_organization / source_annotation / multi_context_reuse
- pattern: reusable_card_atom / infinite_canvas_workbench / tag_database_views / annotation_to_card
- risk_pattern: visual_link_as_truth / tag_field_as_schema / auto_annotation_as_evidence
- maturity: emerging
- complexity: medium
- problem_fit: 4
- reuse_value: 4
- implementation_cost: 3
- integration_fit: 4
- evidence_strength: 2
- reversibility: 4

## Open Questions

- FlexNote 的底层数据格式是否开放、稳定、可导出为可审计 Markdown/YAML？
- 标注卡片是否保留足够 source anchor：页码、timestamp、文本范围、截图 hash、原文件 identity？
- 多设备同步冲突是否有可审计日志？
- 白板箭头是否有类型、说明、证据字段，还是纯视觉连接？
- tag database 字段是否能和外部 Markdown frontmatter 对齐？

## Routing Hint

这份材料适合进入：

- VAKS visual workbench 讨论；
- source annotation adapter 讨论；
- context pack viewer 讨论；
- review queue dashboard 讨论；
- active project workspace / tabs / daily capture 讨论；
- Obsidian Bases / canvas / whiteboard UI 借鉴。

不适合直接进入：

- reviewed relation；
- VAKS schema；
- action basis；
- formal pattern；
- sync safety decision。

## Forbidden

```text
project_borrow_scope
project_non_borrow_scope
decision outcome
formal pattern
action basis
truth confidence
```

项目借鉴范围写在单独的 project overlay，避免 candidate distillation 像项目决策。
