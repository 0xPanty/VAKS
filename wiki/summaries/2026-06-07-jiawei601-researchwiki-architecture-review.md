---
type: library_review
status: candidate
library_name: ResearchWiki
repo_url: https://github.com/jiawei601/ResearchWiki
source_url: https://github.com/jiawei601/ResearchWiki
checked_commit: 3f0705087fdd242514f1179bc53518b87a97f02c
commit_time: 2026-06-03T12:47:46Z
source_status: active
reviewed_at: 2026-06-07
domain: paper-knowledge-base
related_projects:
  - VAKS
current_branch: source-intake / paper-intake / external-reference-borrowing
extracted_patterns:
  - zotero-candidate-import-plan
  - paper-card-not-endpoint
  - paper-topic-method-claim-gap-graph
  - synthesis-after-batch-import
  - memory-agents-templates-rule-layer
  - tag-alias-lint
fusion_decision: adapt
confidence: medium
evidence_count: 17
cross_validated_with:
  - README.md
  - AGENTS.md
  - agents/import_zotero.md
  - agents/pdf_read_agent.md
  - agents/synthesis_agent.md
  - agents/gap_agent.md
  - agents/lint_agent.md
  - templates/paper.md
  - memory/hard_memory.md
negative_evidence:
  - "No VAKS-style reviewed/action-basis separation."
  - "No authority-bucket retrieval policy."
  - "No formal evidence sufficiency gate."
  - "Narrow academic paper scope."
extension_potential: high for paper/Zotero intake; medium for whole VAKS architecture
relations: []
action_basis_allowed: false
truth_mutation_allowed: false
---

# 库分析：ResearchWiki

## 它解决什么问题

ResearchWiki solves a narrow but important problem:

```text
PDF / Zotero 条目很多，但很难变成长期可用的研究结构。
```

它不是传统文献管理器，也不是普通 RAG 问答工具。它更像一个 Obsidian + Agent 的论文研究工作台，把论文整理成 paper、topic、method、claim、gap、review、synthesis 等 Markdown 节点。

## 核心设计

```text
raw/
  original PDFs, Zotero records, attachments, notes

wiki/
  papers, topics, methods, datasets, metrics, claims, gaps, reviews

memory/ + agents/ + templates/
  local operating rules, task agents, and page templates

synthesis/
  literature map, open questions, research positioning, review outline
```

The core loop:

```text
Zotero collection or PDF
-> import plan / manifest
-> one confirmed paper
-> paper card
-> topic/method/claim/gap updates
-> synthesis/gap/review after a small batch
-> lint and error log
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `README.md:36-47` | Project positioning | Local AI paper knowledge base; user judges, agent organizes | Positioning only |
| `README.md:67-79` | Three-layer design | `raw` source, `wiki` structure, `memory/agents/templates` rules | Candidate architecture |
| `README.md:85-95` | Full flow diagram | Zotero -> import -> PDF -> paper/topic/method/claim/gap -> synthesis/review -> memory/log | Candidate workflow |
| `README.md:199-218` | Zotero ingestion boundary | specified collection only, no full library/storage scan, no Zotero mutation | Strong source-ingest guardrail |
| `README.md:238-245` | Synthesis cadence | after several papers, run synthesis/gap/lint | Candidate batch rule |
| `README.md:254-258` | Long-term decisions in memory/synthesis | rules and decisions should not live only in chat | Useful operating discipline |
| `AGENTS.md:18-25` | local layer split | raw/wiki/rule layer and no summary-only import | Candidate architecture |
| `AGENTS.md:121-127` | import_zotero handoff | import plan/manifest, single-paper read delegated | Strong P1 |
| `AGENTS.md:232-246` | operating rules | raw immutability, evidence anchors, uncertainty labels, tags/aliases | Strong guardrail |
| `AGENTS.md:270` | graph warning | graph value from real relations, not link quantity | Anti-pattern warning |
| `agents/import_zotero.md:22-37` | import scope | collection-only read; no DB/storage scan; no Zotero mutation | Strong P1 |
| `agents/import_zotero.md:104-162` | output plan/manifest and flow | candidate list and machine-readable manifest before ingestion | Strong P1 |
| `docs/zotero-workflow.md:5-11` | concise workflow | read collection, plan, check existing, user chooses, ingest one at a time | Strong P1 |
| `agents/pdf_read_agent.md:23-33` | single-paper scope | paper card plus topic/method/dataset/metric/claim/gap; no synthesis | Strong separation |
| `agents/pdf_read_agent.md:80-83` | evidence discipline | distinguish original paper, AI inference, pending checks; claim/gap support | Review input |
| `agents/synthesis_agent.md:60-72` | synthesis rules | read cross-paper nodes, mark weak evidence, write synthesis/review | Candidate consolidation |
| `agents/gap_agent.md:64-90` | gap extraction | extract from limitations/assumptions/metrics/conflicts, mark evidence strength | Candidate gap lane |
| `agents/lint_agent.md:23-25` | health checks | duplicate nodes, missing claim sources, missing gap evidence | Candidate maintenance |
| `memory/hard_memory.md:21-32` | persistent rules | raw/wiki/memory/agents/templates split and AI inference warning | Operating memory only |
| `memory/tag_taxonomy.md:14-18` | tag discipline | canonical tags, one main tag per concept, uncertain tags go inbox | Candidate lint |
| `memory/term_aliases.md:10-47` | alias discipline | prevent duplicate literature review/gap/claim/method pages | Candidate lint |

## 当前支线价值

当前支线：

```text
VAKS source intake / external-source borrowing / paper-scouting and automatic-learning paths
```

它对当前支线：

```text
refines
```

具体价值：

- Shows a concrete safe path from Zotero to candidate import plan.
- Gives an academic paper version of VAKS source/candidate/review separation.
- Adds a practical "paper card is not the endpoint" operator rule.
- Makes batch synthesis and lint a normal maintenance cadence.
- Gives simple user-facing vocabulary for topic/method/claim/gap extraction.

风险：

- It may tempt us to treat `wiki/claims` as reviewed support.
- It may tempt us to treat `memory/` as truth.
- It is narrower than VAKS and does not cover action basis, feedback, authority-bucket retrieval, or evidence sufficiency.

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Strong raw/wiki/index/log and LLM-maintained markdown spine | adapt |
| Dusk workbench | Light operator prompts and Quickstart, not a full dashboard | watch |
| source ingest | Strong specified Zotero collection -> import plan -> manifest -> single-paper gate | adapt P1 |
| review queue | Has `待核查`, evidence strength, lint, but no formal VAKS review queue | adapt with stronger gate |
| schema / reviewed knowledge | Paper/topic/method/claim/gap pages are useful candidate units | adapt, not reviewed |
| memory / dev context | Durable local rules via memory/agents/templates; context policy | adapt as operating layer |
| feedback | Error log and correction rules are useful but minimal | adapt lightly |
| retrieval / cache | Not a retrieval/cache system | no-clear-value |
| API / MCP / agent access | Mentions Codex/Zotero connector but no complete runtime | watch |
| viewer / workbench | Obsidian graph and pages; graph value depends on real relations | support with risk |
| publishing | Open-source hygiene and privacy docs | P2 |
| risk / anti-pattern | link count, AI inference, missing evidence, duplicate pages | adapt risk checks |

## 值得提炼的模式

### Pattern: specified-collection import gate

```text
external library
-> user-specified scope
-> candidate import plan
-> manifest
-> duplicate check
-> user confirms single item
-> source/paper intake
```

Why it matters:

```text
It prevents a connector from becoming a private-library crawler or direct knowledge writer.
```

### Pattern: paper card is not endpoint

```text
paper card
-> topic / method / dataset / metric
-> claim / gap
-> synthesis / review / positioning
```

Why it matters:

```text
It converts paper reading from isolated summaries into reusable cross-paper nodes.
```

### Pattern: operational memory as local rule layer

```text
memory/hard_memory
memory/context_policy
memory/tag_taxonomy
memory/term_aliases
memory/error_log
```

Why it matters:

```text
It gives the agent durable local instructions without relying on chat memory.
```

VAKS boundary:

```text
operational memory is not truth memory.
```

### Pattern: batch synthesis cadence

```text
after several related papers:
  run synthesis
  run gap analysis
  run review outline
  run lint
```

Why it matters:

```text
It avoids both extremes: over-reviewing every paper and never consolidating.
```

## 标签与量化

- domain: paper knowledge base / research wiki
- problem: scattered PDFs and Zotero records do not become reusable research structure
- pattern: candidate import, cross-paper graph nodes, batch synthesis, lint
- maturity: experimental
- complexity: medium
- problem_fit: 5
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 4
- evidence_strength: 3
- reversibility: 5

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed Knowledge | Calibration Output | Review Question |
|---|---|---|---|
| Zotero collection should produce import plan and manifest before paper intake | VAKS Source Card and Candidate Distillation boundaries | candidate_relation | Should VAKS add a `paper_source_candidate` lane before source card? |
| Paper card is not endpoint | VAKS candidate points and review queue | candidate_relation | Should paper intake pre-fill candidate points rather than only summary cards? |
| Claims/gaps need source anchors and AI-inference labels | Evidence Packet and Evidence Support Check boundaries | refines | Which fields can be pre-filled without creating reviewed support? |
| `memory/agents/templates` as local rule layer | VAKS AGENTS/manual/templates/dev context | candidate_relation with scope limit | How to keep rule memory out of truth memory? |
| Graph links require real relations | VAKS association is activation, not truth | supports boundary | Should relation lint flag graph-heavy but evidence-weak pages? |

Boundary:

- Similarity is not support.
- Repetition is not truth.
- Calibration output is review input, not reviewed relation.

## Support / Challenge Review

What supports the useful extraction:

- Multiple files repeat the same architecture: README, AGENTS, hard_memory, and task agents.
- The Zotero flow is documented both in `agents/import_zotero.md` and `docs/zotero-workflow.md`.
- Templates explicitly carry source page/section and evidence strength fields.
- Lint agent checks exactly the drift risks implied by the structure.

What challenges it:

- The repository is a template/spec-oriented vault, not a complete executable ingestion runtime.
- It does not have VAKS authority separation, reviewed support, or action-basis gates.
- Its `claim` pages may sound stronger than VAKS would allow before evidence-aware review.

Challenge severity:

```text
major for direct adoption
minor for design-only borrowing
```

Action readiness:

```text
not_ready
```

## 对当前项目的适配点

For VAKS, use ResearchWiki as:

```text
Support + Risk reference for paper/Zotero intake.
```

Potential future VAKS object:

```yaml
paper_source_candidate:
  source_system: zotero | arxiv | pdf | manual
  source_scope:
  source_item_id:
  candidate_status:
  duplicate_check:
  user_confirmation:
  source_card_created:
  candidate_points_created:
  review_queue_refs:
```

Potential future VAKS workflow:

```text
Source Scout / Zotero Import
-> Source Candidate Queue
-> Source Card
-> Paper Candidate Distillation
-> Candidate Points: topic / method / claim / gap
-> Batch Synthesis
-> Review Queue
-> Evidence-aware review only when promotion/action use is needed
```

## 可拓展性

- 是否适合作为插件/适配层：Yes, especially Zotero connector workflow.
- 是否会绑定核心结构：Should not; keep as paper-source lane.
- 未来替换成本：Low if implemented as source-candidate adapter.
- 可迁移路径：Start with import-plan markdown/JSON, not database runtime.

## 复杂度和风险

- Low-to-medium implementation cost if only creating source candidates and source cards.
- Higher cost if attempting full Zotero connector, PDF extraction, page anchors, and batch synthesis.
- Biggest risk is authority confusion: generated paper pages feel knowledge-like before VAKS review.

## 不可行点 / 避坑

- Do not clone its folder structure as VAKS main schema.
- Do not create `wiki/claims` as reviewed VAKS support without review.
- Do not let `memory/hard_memory.md` become truth confidence.
- Do not scan Zotero DB/storage or copy attachments without explicit scope and consent.
- Do not treat AI inferred research gaps as real gaps.
- Do not treat Obsidian graph density as relation quality.

## 融合判断

- 结论：adapt
- 理由：Very strong for paper intake and academic synthesis; insufficient for VAKS authority/truth/action model.
- 验证方式：future sandbox with 3-5 papers, checking whether source candidates, paper cards, candidate points, synthesis, and review queue remain separated.

## 直接判断

- Direct use: no
- Fork: no
- Design-only: yes
- Reject: no
- Current branch value: strong
- Whole architecture value: medium-high
- Risk: authority confusion around memory, claim pages, and graph links
- Next action: keep as support reference; reopen when VAKS designs Zotero/paper intake or academic research scout lane.

## 后续行动

- Keep this review in candidate/support context.
- Use the project overlay for active VAKS borrowing boundaries.
- Do not promote any pattern into `wiki/patterns`, `wiki/decisions`, or `wiki/claims` without a separate VAKS review gate.
