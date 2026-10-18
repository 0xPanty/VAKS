---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: heavy
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: review_due
derived_from:
  - raw/repos/2026-06-07-jiawei601-researchwiki-source.md
  - raw/repos/_snapshots/jiawei601-ResearchWiki-3f0705087fdd242514f1179bc53518b87a97f02c.zip
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: yes
routing_hint:
  - source-intake
  - paper-intake
  - zotero-workflow
  - research-synthesis
  - review-queue
  - dev-context
possible_project_refs:
  - VAKS
point_anchor_refs:
  - source: raw/repos/2026-06-07-jiawei601-researchwiki-source.md
    snapshot_ref: raw/repos/_snapshots/jiawei601-ResearchWiki-3f0705087fdd242514f1179bc53518b87a97f02c.zip
borrow_value: strong
borrow_order:
  - "P1: Zotero specified-collection -> import plan / manifest -> user confirmation -> single-paper PDF intake."
  - "P1: Paper card is not the endpoint: every paper should update topic, method, claim, gap, synthesis, index, and log."
  - "P1: Evidence and uncertainty discipline: source/page/section anchors, AI-inference labels, no summary-only output."
  - "P1: memory / agents / templates as explicit agent operating layer, with lint for tags, aliases, missing claim sources, and missing gap evidence."
  - "P2: Periodic synthesis / gap / review loop after several papers, not after every tiny intake."
  - "P2: Obsidian graph from real relations, not link count."
  - "P3: README/Quickstart/Obsidian setup as operator UX examples."
avoid:
  - "Do not borrow ResearchWiki wiki/claims as VAKS reviewed truth."
  - "Do not borrow memory/ as a truth layer."
  - "Do not let Zotero import become full-library scan or private storage crawl."
  - "Do not treat paper-card generation as enough learning."
  - "Do not treat graph links, tags, or aliases as evidence support."
  - "Do not promote AI-inferred gaps or claims without VAKS review."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Designing VAKS paper intake, Zotero/source connector workflow, academic research lanes, or paper-based synthesis/review queues."
  support_when: "Comparing source intake, candidate extraction, topic/method/claim/gap schemas, synthesis cadence, or operator-facing Obsidian workflow."
  risk_when: "Any proposal tries to make import plans, paper cards, graph links, memory files, or AI inferred gaps equal reviewed knowledge or action basis."
  cold_references:
    - raw/repos/2026-06-07-jiawei601-researchwiki-source.md
    - raw/repos/_snapshots/jiawei601-ResearchWiki-3f0705087fdd242514f1179bc53518b87a97f02c.zip
tags:
  - candidate
  - provisional
  - repo-distillation
  - research-wiki
  - paper-intake
  - zotero
  - source-intake
---

# Candidate Distillation: ResearchWiki as Paper Intake and Research Synthesis Spine

## Boundary

This is a candidate knowledge point for `jiawei601/ResearchWiki`.

It can route attention, compare ideas, or support a VAKS Project Overlay. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 人话总结

ResearchWiki 最值得压榨的不是“又一个 Obsidian 知识库模板”，而是它把论文学习拆成一条很清楚的链：

```text
Zotero 指定 collection
-> 候选导入清单和 manifest
-> 用户确认单篇论文
-> PDF 读取和 paper card
-> 同步更新 topic / method / claim / gap
-> 每 3-5 篇做 synthesis / gap / review
-> lint 检查重复、缺证据、标签混乱和不确定项
```

它和 VAKS 相似的地方是：

```text
导入不是知识。
摘要不是终点。
跨来源结构和证据锚才是长期价值。
```

但它比 VAKS 轻得多。ResearchWiki 的 `wiki/claims`、`memory`、graph links、lint pass 都不能直接等同于 VAKS 的 reviewed truth、reviewed relation 或 action basis。

最佳一句话借鉴：

```text
把论文摄入做成“候选资料 -> 结构节点 -> 周期综合”的循环，而不是把 PDF 摘要堆成收藏夹。
```

## Source

```yaml
derived_from:
  - raw/repos/2026-06-07-jiawei601-researchwiki-source.md
checked_commit: 3f0705087fdd242514f1179bc53518b87a97f02c
snapshot_ref: raw/repos/_snapshots/jiawei601-ResearchWiki-3f0705087fdd242514f1179bc53518b87a97f02c.zip
key_anchors:
  - README.md:36-47
  - README.md:67-79
  - README.md:85-95
  - README.md:199-218
  - AGENTS.md:121-127
  - AGENTS.md:232-246
  - agents/import_zotero.md:22-37
  - agents/pdf_read_agent.md:23-33
  - agents/pdf_read_agent.md:80-83
  - agents/synthesis_agent.md:60-72
  - agents/gap_agent.md:64-90
  - agents/lint_agent.md:23-25
```

## Candidate Points

### 1. Zotero import plan should be a source-candidate gate

ResearchWiki does not jump from Zotero collection directly to knowledge pages. `import_zotero.md` first reads only the user-specified collection, identifies metadata and attachments, checks duplicates, writes an import plan plus `manifest.json`, and waits for user selection before handing one paper to `pdf_read_agent.md`.

VAKS 借鉴：

```text
Zotero / paper source lane should produce source candidates first.
Only confirmed candidates become source cards or paper-intake records.
No direct jump from external library to reviewed knowledge.
```

Candidate object shape:

```yaml
paper_source_candidate:
  source_system: zotero
  collection_name:
  item_key:
  attachment_key:
  title:
  authors:
  year:
  doi_or_arxiv:
  duplicate_check:
  recommended_status: candidate | duplicate | needs_check
  next_gate: user_confirm_single_paper
```

This is strong P1 for VAKS if we later build automatic or semi-automatic paper intake.

### 2. "Paper card is not the endpoint" is the core knowledge loop

ResearchWiki repeatedly says a paper page is not enough. A new paper should also update topic, method, dataset, metric, claim, gap, index, and log. That turns single-paper reading into graph growth.

For VAKS, the reusable pattern is:

```text
source/paper card = source-specific comprehension
topic/method/claim/gap nodes = cross-source reusable units
synthesis/review = periodic consolidation
```

This maps cleanly to our current boundary:

```text
Source Card -> Candidate Distillation -> Candidate Points -> Review Queue -> Reviewed Knowledge
```

ResearchWiki is useful because it gives a concrete academic version of the middle section:

```text
paper -> paper card
paper -> topic / method / claim / gap
topic / method / claim / gap -> synthesis / review / positioning
```

What VAKS must add:

```text
knowledge_status
retrieval_policy
review_pressure
promotion_gate
action_basis_allowed: false by default
```

### 3. Claim and gap extraction is evidence-aware but not VAKS-reviewed

The paper and claim/gap templates require evidence strength, source sections/pages, and explicit `AI 推断` or `待核查` labels. The PDF agent forbids summary-only output and requires important claims to have source support.

Good borrowing:

```text
For paper intake, require each important claim/gap to carry:
- source paper
- section/page/table/figure anchor when available
- evidence strength
- stated-by-authors vs AI-inferred distinction
- scope/limitations
```

Boundary:

```text
ResearchWiki evidence-aware extraction is review input.
It is not our Evidence Packet, not reviewed support, and not action readiness.
```

Best VAKS phrasing:

```text
Paper intake can pre-fill evidence packets, but cannot pass the review gate by itself.
```

### 4. Synthesis cadence solves the "收藏夹越堆越多" problem

ResearchWiki suggests doing synthesis, gap, and lint after several imported papers. Its synthesis/gap/review agents separate:

```text
synthesis_agent:
  compare papers, topics, methods, claims, gaps

gap_agent:
  extract research gaps and open questions from limitations, assumptions, metrics, conflicts

review_agent:
  organize related work / review outline / writing structure

lint_agent:
  check duplicates, missing sources, missing evidence strength, tag and alias drift
```

This is the most practical operational lesson:

```text
不要每来一篇都过度审稿。
也不要永远只入库不综合。
按批次做轻综合和健康检查。
```

VAKS adaptation:

```yaml
batch_synthesis_trigger:
  when:
    - "3-5 related papers imported"
    - "one project asks for research positioning"
    - "candidate queue accumulates duplicate claims/gaps"
    - "user asks for related work / open questions"
  output:
    - candidate literature map
    - candidate gap list
    - missing evidence list
    - review_queue suggestions
  forbidden:
    - reviewed relation
    - action basis
    - truth confidence upgrade
```

### 5. `memory / agents / templates` is a useful rule layer, but must not become truth

ResearchWiki uses:

```text
memory/hard_memory.md
memory/project_profile.md
memory/context_policy.md
memory/tag_taxonomy.md
memory/term_aliases.md
memory/error_log.md
agents/*.md
templates/*.md
```

This is a good operator pattern: make agent rules durable and local instead of relying on chat history.

VAKS should borrow the idea, not the authority model:

```text
memory files = operating instructions / preferences / aliases / error history
not source evidence
not reviewed truth
not relation support
```

The most useful sub-patterns:

- `term_aliases.md`: prevent duplicate topic/method/claim/gap pages.
- `tag_taxonomy.md`: keep tags canonical.
- `error_log.md`: user corrections become durable process repair.
- `context_policy.md`: decides what the agent reads for each task.

VAKS already has stronger boundaries, but ResearchWiki shows a simpler UX vocabulary that could make the rules easier for non-architect users.

### 6. Graph view only matters if relations are real

ResearchWiki explicitly warns that valuable graph view comes from real relations, not link quantity.

For VAKS this is a strong anti-pattern warning:

```text
Obsidian graph / backlinks / tags / auto wikilinks
can help activation,
but cannot create reviewed relations.
```

Useful adoption:

```yaml
relation_lint:
  check:
    - duplicated aliases
    - unanchored claim pages
    - gap pages without evidence strength
    - graph-heavy pages with weak source anchors
  output: maintenance_manifest
  forbidden: auto_reviewed_relation
```

### 7. It is a P1 reference for academic intake, not for the whole VAKS architecture

ResearchWiki is focused on a local paper knowledge base. That narrowness is a feature.

Borrow strongly for:

- Zotero collection gate.
- paper/PDF source intake.
- topic/method/claim/gap cross-paper structure.
- synthesis/gap/review cadence.
- tag/alias/lint discipline.
- operator-friendly README/Quickstart language.

Do not treat it as complete for:

- VAKS truth layer.
- action basis.
- project borrowing overlays.
- evidence sufficiency gate.
- retrieval authority buckets.
- feedback ledger.
- security/tooling beyond the Zotero no-scan/no-mutate boundary.

## Open Questions

- If VAKS adds Zotero, should import candidates live under `raw/papers/`, `raw/repos`, or a separate `raw/paper_sources/` lane?
- Should paper `claim/gap` extraction pre-fill Evidence Packet fields, or only create review-queue candidate points?
- How many related papers should trigger batch synthesis in VAKS: fixed `3-5`, user-scoped, or project-lane-specific?
- Should alias/tag lint become a generic maintenance manifest rule for all candidate points, not only papers?
- How to preserve Zotero privacy: connector-only, never local DB scan, explicit collection confirmation, no attachment mutation?

## Routing Hint

```yaml
good_for:
  - paper intake
  - Zotero source candidate queue
  - academic research synthesis
  - related work / literature map workflow
  - topic/method/claim/gap candidate extraction
  - lint and alias discipline
not_good_for:
  - reviewed truth
  - action basis
  - automatic claim promotion
  - graph relation authority
  - full VAKS replacement
```

## Borrow Gradient

```yaml
borrow_value: strong
P1:
  - Zotero specified-collection candidate gate
  - import_plan + manifest before ingestion
  - single-paper PDF read after user confirmation
  - paper card not endpoint
  - topic/method/claim/gap updates
  - claim/gap evidence and uncertainty marking
  - tag/alias/lint maintenance
P2:
  - batch synthesis after several papers
  - review-outline and research-positioning surfaces
  - Obsidian graph from real relations
  - operator-friendly Quickstart prompts
P3:
  - exact folder names
  - open-source README polish
  - Obsidian graph settings
avoid:
  - memory as truth
  - wiki/claims as reviewed support
  - graph/link count as evidence
  - full Zotero storage scan
  - automatic PDF import without user confirmation
```

## Forbidden

```text
project_borrow_scope
project_non_borrow_scope
decision outcome
formal pattern
action basis
truth confidence
reviewed relation
```
