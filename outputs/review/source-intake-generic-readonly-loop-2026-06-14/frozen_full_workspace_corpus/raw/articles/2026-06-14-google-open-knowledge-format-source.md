---
type: source
record_kind: source_card
status: source-captured
title: "Google Open Knowledge Format v0.1 spec and launch blog"
source_id: 2026-06-14-google-open-knowledge-format-source
source_uri: github:GoogleCloudPlatform/knowledge-catalog/okf/SPEC.md@main
source_url: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/?hl=en
source_type: official-spec-and-official-blog
author: "Sam McVeety; Amir Hormati; Google Cloud Data Cloud team"
publisher: Google Cloud
published_at: 2026-06-13
updated_at:
captured_at: 2026-06-14
captured_by: Codex
extracted_by: Codex
extracted_at: 2026-06-14
extraction_tool: web
extraction_model: Codex
version_or_commit: "OKF v0.1 draft; GitHub main branch SPEC.md checked 2026-06-14"
source_integrity:
  source_hash:
  snapshot_hash:
  ingest_state: new
adapter_ingest:
  adapter_name: web
  adapter_version:
  capture_method: direct official URLs
  extraction_trace:
    - raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/main/okf/SPEC.md
    - cloud.google.com blog page
  known_limits:
    - "GitHub SPEC.md was inspected from main branch raw URL, not pinned to immutable commit."
    - "Blog was inspected as published web page; no archived copy stored in this intake."
source_status: active
raw_location:
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
why_saved: "User requested combined VAKS distillation of Google's OKF SPEC.md and launch blog; the two sources belong to one Open Knowledge Format knowledge point."
topics:
  - open-knowledge-format
  - llm-wiki
  - markdown-frontmatter
  - knowledge-exchange
  - agent-readable-knowledge
projects:
  - verified-action-knowledge-system
source_family: google-open-knowledge-format
upstream_sources:
  - title: "Open Knowledge Format (OKF) SPEC.md"
    url: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
    raw_url: https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/main/okf/SPEC.md
    source_kind: official-spec
  - title: "Introducing the Open Knowledge Format"
    url: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/?hl=en
    source_kind: official-blog
verification_status: primary-sources-captured
candidate_relation_suggestions:
  - target: "[[vaks-architecture-upgrade-plan-2026-06-13]]"
    relation_type: refines
    relation_state: candidate
    why_suggested: "OKF strengthens VAKS's Markdown/YAML bundle and portable knowledge exchange story, but remains retrieval/exchange infrastructure rather than reviewed truth."
    source_anchor: "SPEC.md sections 1-11; Google Cloud blog sections 'What's missing is a format, not another service' and 'Three principles behind the design'."
    evidence_support:
      span_supports_target: partial
      evidence_role: inferential_support
      reviewer_note: "Use only as architecture reference; not reviewed VAKS pattern yet."
    suggested_at: 2026-06-14
tags:
  - source-card
  - raw
  - google-cloud
  - open-knowledge-format
  - okf
  - llm-wiki
  - candidate-only
---

# 来源记录：Google Open Knowledge Format

## 为什么收录

用户要求把 Google 的 OKF SPEC 和 Google Cloud launch blog 一起蒸馏。两者属于同一知识点：

```text
Open Knowledge Format = 用 Markdown files + YAML frontmatter + index/log/citations
来表达人类和 agent 都能读写、可移植、可版本化的知识 bundle。
```

这对 VAKS 有强参考价值，因为它从官方云厂商角度验证了我们一直在走的方向：

```text
Markdown/YAML as portable knowledge substrate
index.md for progressive disclosure
log.md for change history
links as relation navigation
citations as source pointers
format over platform
```

但它不能直接替代 VAKS 的 reviewed knowledge、Evidence Support Check、Evidence Sufficiency Gate 或 action basis 规则。

## 来源信息

- SPEC: https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
- SPEC raw: https://raw.githubusercontent.com/GoogleCloudPlatform/knowledge-catalog/main/okf/SPEC.md
- Blog: https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/?hl=en
- Blog title: Introducing the Open Knowledge Format
- Blog date: 2026-06-13
- Authors: Sam McVeety, Amir Hormati
- Publisher: Google Cloud
- Captured at: 2026-06-14
- Capture method: official URLs via web inspection

## Source Anchors

| Anchor | What was checked | Why it matters |
|---|---|---|
| SPEC.md §1 Motivation | OKF motivation and goals | Confirms format-over-platform and human/agent readability goals |
| SPEC.md §3 Bundle Structure | Directory tree, optional `index.md`, `log.md` | Maps directly to VAKS raw/wiki/index/log spine |
| SPEC.md §4 Concept Documents | Markdown body + YAML frontmatter, required `type` | Useful as minimal interop surface |
| SPEC.md §5 Cross-linking | Markdown links as relationships, consumers tolerate broken links | Good for activation graph, not reviewed relations |
| SPEC.md §6 Index Files | Progressive disclosure | Strong fit with VAKS context loading |
| SPEC.md §7 Log Files | Change history | Useful for source/update logs |
| SPEC.md §8 Citations | External sources under `# Citations` | Useful, but VAKS must keep citation != support |
| SPEC.md §9 Conformance | Required frontmatter block and non-empty `type`, soft constraints | Useful interop posture, weaker than VAKS review rules |
| Blog lines around launch motivation | fragmented context landscape, format not service | Supports VAKS product/architecture framing |

## 初步看点

OKF is valuable because it formalizes the same family of design VAKS already values:

- common files over proprietary service;
- Markdown body for human reading;
- YAML frontmatter for agent routing;
- Git/version control as distribution and history;
- index files for progressive disclosure;
- log files for updates;
- links and citations for traversal and provenance;
- producer/consumer independence.

## 明显边界

OKF is intentionally minimal. VAKS needs stricter boundaries:

```text
OKF citation = source pointer
VAKS evidence_support = checked support for a specific point/relation/action

OKF link = relationship in prose/navigation
VAKS reviewed_relation = evidence-aware reviewed edge

OKF type = routing/presentation field
VAKS knowledge_status / action_readiness = authority boundary

OKF conformance = parseable bundle
VAKS promotion = reviewed/action-facing gate
```

## 可抽取 Candidate Points

1. A portable agent-readable knowledge bundle can be just Markdown files with YAML frontmatter when the format is explicit enough.
2. `index.md` as progressive disclosure is a strong fit for agent context loading and VAKS context pack preparation.
3. `log.md` as chronological update history is useful for source/update/change records.
4. Producer/consumer independence supports VAKS's separation between Markdown source of record and derived retrieval/API/viewer layers.
5. OKF citations improve provenance but are weaker than VAKS evidence support.
6. OKF cross-links are useful activation/navigation signals but must not become reviewed relations automatically.

## 当前处理等级

```text
medium
```

Upgrade to heavy if:

- VAKS starts designing export/import compatibility;
- VAKS adds a public bundle format;
- source/retrieval/context-pack templates need OKF-compatible serialization;
- Google OKF becomes a practical interoperability target.

## 下一步

- Use the candidate distillation as design reference.
- Do not promote to reviewed pattern without later evidence-aware review.
- If implementation starts, create a small VAKS-to-OKF compatibility sandbox rather than changing core schema first.

