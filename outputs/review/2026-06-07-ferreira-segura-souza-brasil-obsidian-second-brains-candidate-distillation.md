---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from:
  - raw/papers/2026-06-07-ferreira-segura-souza-brasil-obsidian-second-brains-source.md
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - obsidian-workbench
  - empirical-vault-practices
  - retrieval-shapes-structure
  - context-sensitive-creation
  - templates-and-tags
  - dynamic-reorganization
  - ai-assisted-metadata
  - multi-vault-friction
possible_project_refs:
  - verified-action-knowledge-system
point_anchor_refs:
  - source_ref: raw/papers/2026-06-07-ferreira-segura-souza-brasil-obsidian-second-brains-source.md
    selector_type: arxiv_abs_lines
    selector_value: "arXiv lines 30-52: title, authors, abstract, submitted date, related DOI"
  - source_ref: raw/papers/2026-06-07-ferreira-segura-souza-brasil-obsidian-second-brains-source.md
    selector_type: pdf_method_lines
    selector_value: "PDF lines 70-106: case study, seven participants, interviews, observation tasks, content analysis"
  - source_ref: raw/papers/2026-06-07-ferreira-segura-souza-brasil-obsidian-second-brains-source.md
    selector_type: pdf_creation_organization_lines
    selector_value: "PDF lines 112-165: note creation context, folders, tags, templates, links, inbox"
  - source_ref: raw/papers/2026-06-07-ferreira-segura-souza-brasil-obsidian-second-brains-source.md
    selector_type: pdf_retrieval_lines
    selector_value: "PDF lines 166-206: search, tags, note links, sequential navigation, multi-vault confusion"
  - source_ref: raw/papers/2026-06-07-ferreira-segura-souza-brasil-obsidian-second-brains-source.md
    selector_type: pdf_design_implications_lines
    selector_value: "PDF lines 207-236: creation-to-retrieval design implications and dynamic organization"
reference_layer_tag: ref/obsidian-second-brain-empirical-study
reference_layer_label_zh: Obsidian 第二大脑实证研究
reference_layer_scope: "Obsidian vault practices / retrieval-driven structure / candidate design extraction only"
borrow_value: strong
borrow_order:
  - "P1: Retrieval strategy shapes vault structure and note-creation behavior; use this to design source cards, templates, tags, and context-pack retrieval together."
  - "P1: Context-sensitive creation matters: create notes in the right local context and use templates to preserve future retrieval paths."
  - "P1: Dynamic reorganization is normal; avoid a static taxonomy that punishes moving notes, changing tags, or refining inbox material."
  - "P2: Folders/tags/templates/links/inbox form an empirical feature map for Obsidian-style workbench design."
  - "P2: AI assistance is strongest as metadata, search, template, link, duplicate, and placement support, not as truth or review."
  - "P3: Multi-vault and multi-device friction should inform product/workbench risk, but not core VAKS truth schema."
avoid:
  - "Do not treat Obsidian tags, links, search hits, graph edges, or folder placement as reviewed relations or evidence support."
  - "Do not overstate the study as large-scale; the PDF reports seven Computer Science researchers in one Brazilian research-lab context."
  - "Do not auto-tag, auto-move, auto-link, or auto-merge notes without provenance, user control, and review routing."
  - "Do not impose a static pyramid taxonomy; the source supports changeable organization."
  - "Do not promote this candidate into wiki/claims, wiki/patterns, or wiki/decisions without a separate evidence-aware review."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing VAKS source-card UX, Obsidian workbench behavior, retrieval-aware templates, or vault organization rules."
  support_when: "Discussing PKM/second-brain practice, tags, links, inbox/refinement, dynamic reorganization, or AI-assisted metadata."
  risk_when: "Any retrieval label, tag, link, template output, AI suggestion, or vault graph starts being treated as reviewed knowledge or action basis."
  cold_references:
    - raw/papers/2026-06-07-ferreira-segura-souza-brasil-obsidian-second-brains-source.md
tags:
  - candidate
  - provisional
  - arxiv
  - interact-2025
  - obsidian
  - second-brain
  - pkm
  - empirical-study
  - retrieval-shapes-structure
  - graph-is-activation-not-truth
  - candidate-only
---

# Candidate Distillation: Obsidian Second Brains Empirical Study

## Boundary

This note is provisional orientation.

It distills an empirical Obsidian case study for VAKS design reference. It is
not reviewed knowledge, not a decision, not a formal pattern, and not action
basis.

Strongest safe use now:

```text
borrow empirical design pressure for Obsidian-style source intake and workbench UX
```

Unsafe use now:

```text
change VAKS truth schema
promote tags/links/search behavior into reviewed relations
claim universal PKM behavior from a small sample
```

## 一句话

这篇真正硬的点不是“Obsidian 很好”，而是：

```text
用户怎么找笔记，会反过来决定他们怎么写笔记、放笔记、打标签、做模板。
```

人话：

```text
资料库不能只问“这条知识该放哪”。
还要问“未来要怎么被找回来、在什么任务里被点亮、点亮时能不能分清候选/已审/行动依据”。
```

## 借用优先级

### P1: `retrieval_strategy_shapes_structure`

候选结论：

```text
检索策略会塑造 vault 结构和笔记创建方式。
```

来源支撑：

```text
arXiv 摘要明确说，参与者的知识检索策略影响他们构建和维护内容的方式。
PDF findings / retrieval section 展示了 search、tag、link、sequential navigation 等路径。
```

VAKS 可借：

```text
source card fields
tags
templates
indexes
context-pack preparation
activation routing
```

应该一起设计，而不是先堆字段、后补搜索。

边界：

```text
retrieval design = activation support
not truth support
```

### P1: `context_sensitive_note_creation`

候选结论：

```text
笔记创建时所在的上下文，会影响后续组织和检索质量。
```

来源支撑：

```text
PDF 用 Obsidian 新建笔记示例说明：从错误位置新建会落到 root；
从目标 folder 的右键菜单新建，才更符合用户当前组织语境。
```

VAKS 可借：

```text
when creating source cards:
  infer or ask the source family
  place the source in the right raw lane
  apply a source-type template
  preserve review routing from the beginning
```

人话：

```text
不是写完再慢慢收拾；
入口就要帮用户少放错地方。
```

边界：

```text
context-sensitive creation can suggest location/template,
but should not silently promote or rewrite authority state.
```

### P1: `dynamic_reorganization_is_normal`

候选结论：

```text
好的第二大脑不是一次性设计好的静态金字塔，而是会随任务、项目、理解变化而重组。
```

VAKS 可借：

```text
candidate -> review -> connect -> activation
```

这条链路本来就支持变化：候选点可以改写、合并、降级、转路线；已审层才需要更严格。

设计含义：

```text
tags can change
folders can move
indexes can be regenerated
candidate routing can be revised
old decisions can be superseded
```

边界：

```text
dynamic organization is not dynamic truth.
Moving a note or retagging it must not change truth confidence.
```

### P2: `folders_tags_templates_links_inbox_feature_map`

候选结论：

```text
真实 Obsidian 用户常用 folders、tags、templates、links、inbox/refinement 来组合管理 vault。
```

VAKS 可借：

```text
raw lane = folder/context
frontmatter = stable metadata
tags = retrieval hint
links = navigation hint
templates = minimum viable capture structure
review queue = inbox/refinement pressure
```

不要借成：

```text
folder = truth layer
tag = reviewed status
link = reviewed relation
template completeness = evidence sufficiency
```

### P2: `ai_as_metadata_and_retrieval_assistant`

候选结论：

```text
AI 最适合先帮用户做标签、检索、模板、链接、去重、放置建议。
```

VAKS 可借：

```text
AI can suggest:
  candidate tags
  candidate source family
  missing template fields
  nearby notes
  possible duplicate points
  retrieval aliases
  context-pack candidates
```

必须保留：

```text
AI suggestion = candidate assistance
not reviewed knowledge
not evidence support
not action basis
```

### P3: `multi_vault_and_multi_device_friction`

候选结论：

```text
多 vault / 多设备会带来导航、同步、连续性摩擦。
```

VAKS 可借：

```text
repo vs formal Obsidian vault boundary must stay explicit
sync result must be hash-checked
future mobile/read-only surfaces should not imply source-of-truth mutation
```

边界：

```text
This is product/workbench risk,
not a reason to weaken review or provenance boundaries.
```

## 对用户摘要的校正

```text
High-value: yes.
Directly relevant to Obsidian/VAKS: yes.
INTERACT 2025 related: yes.
Large-scale: no.
Participant count in the arXiv PDF: seven Computer Science researchers.
```

所以它更准确的定位是：

```text
small but unusually direct qualitative Obsidian case study
```

不是：

```text
large-scale empirical benchmark
```

## VAKS 融合判断

### Should Borrow

```text
retrieval-aware capture
context-sensitive source creation
template-standardized minimum fields
inbox/refinement as light-to-medium processing
dynamic reorganization support
AI as metadata/retrieval assistant
explicit multi-vault sync status
```

### Should Not Borrow

```text
static taxonomy worship
tag/link/search as authority
silent AI auto-organization
automatic promotion from convenience metadata
multi-device convenience over provenance
```

## Candidate Points For Later Review

### CP-001: `retrieval_shapes_capture_schema`

Candidate:

```text
VAKS source-card schemas should be designed from future retrieval and context-pack needs, not only from archival completeness.
```

Review need:

```text
Compare current source-card fields against actual retrieval/context-pack workflows.
```

### CP-002: `tags_are_activation_hints`

Candidate:

```text
Tags should remain activation/retrieval hints unless separately reviewed.
```

Review need:

```text
Check whether any current VAKS workflow accidentally treats tags as evidence support or reviewed relation.
```

### CP-003: `templates_reduce_future_retrieval_friction`

Candidate:

```text
Templates can reduce retrieval friction by prompting source anchors, route labels, candidate status, and review boundaries at capture time.
```

Review need:

```text
Audit whether current templates have enough retrieval-critical fields without becoming heavy for ordinary capture.
```

### CP-004: `dynamic_reorganization_without_truth_mutation`

Candidate:

```text
VAKS should allow candidate routes, tags, and indexes to change while preventing those changes from mutating truth confidence.
```

Review need:

```text
Check current docs for any place where movement, dashboard status, or metadata update could imply authority upgrade.
```

### CP-005: `ai_metadata_assistant_gate`

Candidate:

```text
AI-assisted tagging, template filling, duplicate detection, and note-placement suggestions belong in candidate/support layers.
```

Review need:

```text
Define the minimum provenance trace for AI-assisted metadata changes before any future automation.
```

## Current Activation Use

Use this candidate note early when a task is about:

```text
Obsidian vault design
source-card template ergonomics
tag/link/index policy
retrieval-aware context packs
AI-assisted metadata
multi-vault sync friction
```

Do not use it as:

```text
reviewed proof
architecture decision
action-ready basis
universal user-behavior claim
```
