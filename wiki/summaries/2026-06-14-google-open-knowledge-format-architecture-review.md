---
type: architecture_review
record_kind: architecture_review
status: candidate
title: "Google Open Knowledge Format architecture review"
source_ref: raw/articles/2026-06-14-google-open-knowledge-format-source.md
distillation_ref: outputs/review/2026-06-14-google-open-knowledge-format-candidate-distillation.md
source_id: 2026-06-14-google-open-knowledge-format-source
source_url: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/?hl=en
checked_commit: main
commit_time:
reviewed_at: 2026-06-14
created_by: Codex
knowledge_status: candidate
processing_tier: medium
truth_status: not_reviewed
action_basis_allowed: false
truth_mutation_allowed: false
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
borrow_value: strong
fusion_decision: adapt
current_branch: vaks-architecture-upgrade-plan
project_fit:
  verified_action_knowledge_system: strong_interop_fit
  truth_layer: reject_direct
  review_layer: weak_direct_fit
  activation_layer: strong_fit
  context_pack_layer: strong_fit
  agent_access_layer: medium_fit
assessment:
  domain: agent-readable-knowledge-format
  maturity: draft
  complexity: low_medium
  problem_fit_vaks_interop: 5
  problem_fit_truth_review: 2
  reuse_value: 4
  implementation_cost: 2
  integration_fit: 4
  evidence_strength: 4
  reversibility: 5
tags:
  - architecture-review
  - candidate
  - google-cloud
  - open-knowledge-format
  - okf
  - markdown-yaml
  - llm-wiki
  - vaks/source-ingest
  - vaks/context-pack
  - vaks/export-import
  - risk/citation-as-support
  - risk/link-as-reviewed-relation
---

# Google Open Knowledge Format Architecture Review

## One-Line Judgment

Google OKF is a strong design-only / adapt reference for VAKS's portable Markdown/YAML bundle, source ingest, progressive disclosure, and future export/import story; it should not be used as VAKS's truth schema, review gate, or action-basis model.

## 它解决什么问题

OKF 解决的是组织内部知识碎片化和 agent context 难交换的问题。

它认为现代 AI agent 需要的不只是数据本身，还需要围绕数据和系统的 metadata、context、curated insight。OKF 用一个开放格式把这些知识表示成：

```text
directory of markdown files
+ YAML frontmatter
+ optional index.md
+ optional log.md
+ markdown links
+ citations
```

Google Cloud blog 的核心判断是：缺的不是另一个 knowledge service，而是一个 format。

## 核心设计

```text
Knowledge Bundle
-> directory tree
-> concept markdown files
-> YAML frontmatter
-> markdown body
-> index.md progressive disclosure
-> log.md update history
-> cross-links
-> citations
-> permissive conformance
```

OKF 的重心是互操作：

```text
producer and consumer can be independent
format is contract
tooling can be swapped
```

## Source / Code Anchors

| Anchor | What exists | Design extraction | Boundary |
|---|---|---|---|
| `okf/SPEC.md §1 Motivation` | Human-readable, agent-parseable, diffable, portable goals. | Supports VAKS file-first posture. | Goal statement is not implementation proof. |
| `okf/SPEC.md §3 Bundle Structure` | Directory tree with reserved `index.md` and `log.md`. | Strong fit for VAKS bundle/export/context loading. | Directory structure does not decide truth. |
| `okf/SPEC.md §4 Concept Documents` | UTF-8 Markdown + YAML frontmatter; required `type`. | Minimal interop surface. | Weaker than VAKS boundary fields. |
| `okf/SPEC.md §5 Cross-linking` | Markdown links as relationships; broken links tolerated. | Good activation/navigation graph. | Not reviewed relation. |
| `okf/SPEC.md §6 Index Files` | Progressive disclosure. | Strong fit for dev context/context pack loading. | Index is map, not evidence. |
| `okf/SPEC.md §7 Log Files` | Chronological history. | Useful for update/source/change logs. | Log is not approval. |
| `okf/SPEC.md §8 Citations` | External source links under citations. | Useful provenance convention. | Citation is not support. |
| `okf/SPEC.md §9 Conformance` | Parseable frontmatter + non-empty type; soft constraints. | Tolerant consumer model. | Too permissive for VAKS action/review. |
| Google Cloud Blog | Format not service; Markdown/YAML bundle; principles. | Strong architecture/product validation. | Blog is explanatory, not formal spec. |

## 当前支线价值

Current branch:

```text
VAKS architecture upgrade plan / retrieval-context-action boundary hardening
```

Value:

- Supports VAKS's file-first architecture.
- Supports progressive context loading and bundle navigation.
- Supports future import/export compatibility without changing core schema.
- Supports product positioning: VAKS can be a verified-action layer over portable knowledge bundles.
- Reinforces that a format can be more important than a platform.

Risk:

- OKF minimal conformance is far weaker than VAKS reviewed/action requirements.
- OKF citations and links may look like support/relation if imported naively.
- Enrichment agents writing OKF concepts could be confused with reviewed writeback.

## 全貌架构价值

| Architecture Zone | Value / Finding | Adopt? |
|---|---|---|
| Karpathy spine | Strong: raw/wiki/index/log, Markdown bundle, git-friendly format. | adapt |
| Dusk workbench | Medium: index and visualizer can support workbench navigation. | adapt later |
| source ingest | Strong: concept files and frontmatter give interop target. | adapt |
| review queue | Weak direct: no review/promotion model. | reject direct |
| schema / reviewed knowledge | Medium as serialization inspiration, weak as authority model. | adapt cautiously |
| memory / dev context | Strong: progressive disclosure and portable context. | adapt |
| feedback | Low: no feedback ledger boundary. | watch |
| retrieval / cache | Strong: frontmatter, tags, links, index files help retrieval. | adapt |
| API / MCP / agent access | Medium: producer/consumer independence supports agent contracts. | adapt |
| viewer / workbench | Medium: static visualizer idea is useful. | watch |
| publishing | Strong: bundle export format. | adapt later |
| risk / anti-pattern | High: minimal format can be over-trusted. | record risk |

## 值得提炼的模式

### Format over platform

Borrow:

```text
VAKS can publish or exchange knowledge as files without requiring a service.
```

Boundary:

```text
Publishing/exchange format is not truth authority.
```

### Progressive disclosure through index files

Borrow:

```text
index.md helps agents inspect what exists before loading full documents.
```

Boundary:

```text
Index summaries are context, not evidence.
```

### Tolerant consumers, strict internal gates

Borrow:

```text
Consumers should tolerate unknown fields and partial bundles.
```

VAKS-specific refinement:

```text
Tolerate for reading.
Fail closed for authority/action.
```

### Citations as source pointers

Borrow:

```text
standard # Citations section improves traceability.
```

Boundary:

```text
Citation marker does not equal support.
```

### Link graph as activation

Borrow:

```text
markdown links can build navigation/activation graph.
```

Boundary:

```text
Link edge does not equal reviewed relation.
```

## 标签与量化

- domain: agent-readable-knowledge-format / metadata-as-code / llm-wiki
- problem: portable knowledge exchange and context assembly
- pattern: markdown-yaml-bundle / progressive-disclosure-index / producer-consumer-independence
- risk_pattern: citation-as-support / link-as-reviewed-relation / conformance-as-authority
- maturity: draft
- complexity: low-medium
- problem_fit: 5 for VAKS export/import/context, 2 for review/action
- reuse_value: 4
- implementation_cost: 2
- integration_fit: 4
- evidence_strength: 4
- reversibility: 5

## Knowledge Calibration / Point Collision

| Candidate Point | Local Reviewed / Core Boundary | Calibration Output | Review Question |
|---|---|---|---|
| OKF formalizes Markdown/YAML LLM-wiki pattern. | VAKS already uses Markdown/YAML as source-of-record. | supports / refines | Should VAKS define an OKF-compatible export profile? |
| `index.md` supports progressive disclosure. | VAKS dev context and context pack already use progressive loading. | supports | Which VAKS folders should expose index files first? |
| OKF citations point to sources. | VAKS Evidence Support Check requires span-target support. | scope_mismatch | How should imported citations be downgraded until checked? |
| OKF links imply relationships. | VAKS reviewed relation requires evidence for the edge. | risk_of | Should link import create candidate_relation only? |
| Enrichment agents can generate OKF concepts. | VAKS agent writes must be candidate/receipt gated. | risk_of | Should generated OKF concepts be marked candidate by default? |

## Support / Challenge Review

What supports the candidate value:

- SPEC is an official primary source from the GoogleCloudPlatform knowledge-catalog repository.
- Blog is an official Google Cloud announcement explaining motivation and design principles.
- The format closely matches VAKS's existing Markdown/YAML, index/log, agent-readable direction.
- It validates "format, not platform" as an industry-level posture.

What challenges it:

- OKF v0.1 is draft and deliberately minimal.
- SPEC was inspected on main branch, not immutable commit.
- OKF does not define evidence support, review state, action readiness, or feedback boundaries.
- Google Cloud Knowledge Catalog ingestion path is product-specific and should not be imported as VAKS core.

Challenge severity:

```text
minor for design-only adoption
major for direct schema replacement
```

Scope limits:

```text
Use OKF as export/import and interop reference.
Do not use OKF as VAKS review/action/truth model.
```

Action readiness:

```text
not_ready for implementation
ready only as candidate reference
```

## 对当前项目的适配点

Smallest elegant adoption:

```text
1. Keep VAKS internal boundaries.
2. Add future OKF compatibility sandbox after P0/P1 gates.
3. Map VAKS source/candidate/reviewed records to OKF concepts only for export/import.
4. Treat imported OKF citations as source pointers.
5. Treat imported OKF links as candidate/activation edges.
6. Keep VAKS action readiness completely outside OKF conformance.
```

## 复杂度和风险

Risks:

- Making OKF compatibility a premature core requirement.
- Weakening VAKS required fields to match OKF's minimal `type`.
- Letting unknown frontmatter fields bypass fail-closed authority checks.
- Treating OKF conformance as enough for reviewed knowledge.
- Letting enrichment agents write directly into reviewed memory.

## 不可行点 / 避坑

Do not:

- Replace VAKS schema with OKF.
- Rename VAKS records around OKF before practical need.
- Import OKF citations as support.
- Import OKF links as reviewed relations.
- Use Google Cloud Knowledge Catalog as VAKS runtime dependency.
- Treat OKF visualizer as evidence graph.

## 融合判断

- 结论：adapt as design-only candidate.
- 理由：OKF is a clean external validation of portable Markdown/YAML knowledge bundles, but lacks the verified-action gates that define VAKS.
- 验证方式：future OKF compatibility sandbox with boundary fixtures.

## 直接判断

- Direct use: no as core schema; yes as future export/import reference.
- Fork: no.
- Design-only: yes, strong.
- Reject: reject as truth/review/action model.
- Current branch value: strong for VAKS architecture upgrade and external positioning.
- Whole architecture value: strong for source ingest, context pack, retrieval, viewer/workbench, publishing/export; weak for review/action.
- Risk: citation-as-support, link-as-relation, conformance-as-authority.
- Next action: keep candidate-only; revisit during export/import or public bundle design.

## 后续行动

If VAKS later designs export/import:

1. Create `P2.5 OKF Compatibility Sandbox`.
2. Export one source card and one candidate distillation to OKF concept form.
3. Import one OKF concept back into candidate-only VAKS record.
4. Prove citations/links do not become support/reviewed relations.
5. Only then consider adding an OKF profile note to implementation docs.

