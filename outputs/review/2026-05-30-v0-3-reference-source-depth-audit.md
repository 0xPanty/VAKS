---
type: source-depth-audit
status: completed
created: 2026-05-30
project: verified-action-knowledge-system
scope:
  - v0-3
  - reference-research
  - pro-review
tags:
  - source-depth
  - reference-audit
  - pro-review
---

# v0.3 Reference Source Depth Audit

## Purpose

This audit answers the Pro-review risk question:

```text
Are we using reference names as decoration, or do adopted mechanisms have enough source depth?
```

Short answer:

```text
We do not need to inspect every referenced library's source code.
We do need to inspect or source-anchor every reference that actually affects schema, review gates, action basis, or truth boundaries.
```

## Depth Rule

### Code / source inspection is required when:

```text
the framework borrows a concrete mechanism from a repository
the mechanism changes schema, templates, review flow, or action basis
the adoption depends on implementation behavior rather than a published concept
the reference is used to justify a hard boundary
```

### Paper / official documentation is enough when:

```text
the framework borrows only a concept or vocabulary
the source is a paper, standard, or official documentation
no runtime behavior is being adopted
the concept is compressed into a lazy review gate
```

### No deeper source inspection is needed now when:

```text
the source is watch / parked
the source is explicitly rejected for core architecture
the idea is only a future implementation option
the framework does not cite it as support for a current hard rule
```

## Current Source Depth Status

### A. Exact Source-Code Reviewed

#### RKA

```text
source: infinitywings/rka
checked commit: 7bc2d76efba61b92db5b056220f7009763003a0d
local review: outputs/review/2026-05-30-rka-source-code-anchor-review.md
```

What it supports:

```text
review queue as routing metadata
decision superseding as history-preserving review pressure
staleness versus validity split
decision outcome calibration
outcome_precondition: recommendation + user_choice / explicit override
maintenance hygiene as lint pressure
```

What it does not support:

```text
adopting RKA runtime
adopting MCP surface
adopting dashboard
using SQLite as this vault's truth source
using workflow actions as truth changes
```

Depth judgment:

```text
SUFFICIENT for current v0.3 adopted RKA ideas.
```

#### Graphiti / Zep Targeted Source-Code Anchor

```text
source: getzep/graphiti
checked commit: 34f56e65e0fe2096132c8d16f3a1a4ac9300a5f6
inspection mode: targeted code anchor only
runtime executed: false
```

Code/doc anchors checked:

```text
README.md lines 67-81:
context graph facts have validity windows and trace back to episodes.

README.md lines 127-153:
episodes/provenance, temporal context graph, validity windows, bi-temporal tracking.

graphiti_core/models/edges/edge_db_queries.py lines 88-100:
edge fields include episodes, expired_at, valid_at, invalid_at, reference_time.

graphiti_core/models/edges/edge_db_queries.py lines 196-220:
edge retrieval returns episodes, valid_at, invalid_at.

graphiti_core/models/nodes/node_db_queries.py lines 35-50:
episodic nodes store source_description, source, content, valid_at.
```

What it supports:

```text
Temporal Applicability Check:
truth is source-backed
applicability is time-, version-, and scope-bound
valid_from / valid_until style fields are reasonable
raw episode/source traceability is provenance
```

What it does not support:

```text
automatic graph construction as reviewed truth
automatic invalidation as this vault's truth update
Graphiti runtime as source of truth
graph database dependency
agent memory platform adoption
```

Depth judgment:

```text
SUFFICIENT for the narrow temporal-applicability principle.
NOT sufficient for adopting Graphiti runtime, which remains rejected.
```

### B. Primary Source Records Captured In The Main Vault

These sources already have local source records in the main vault and are included in this refreshed Pro package so the audit can be reviewed as a standalone ZIP:

```text
raw/papers/2026-05-29-truth-maintenance-system-source.md
raw/papers/2026-05-29-dung-argumentation-framework-source.md
raw/articles/2026-05-29-w3c-prov-source.md
raw/papers/2026-05-29-veriscore-source.md
raw/papers/2026-05-29-papertrail-source.md
raw/papers/2026-05-29-graphfc-source.md
raw/papers/2026-05-29-prove-provenance-verification-source.md
raw/papers/2026-05-29-rag-attribution-faithfulness-source.md
raw/papers/2026-05-29-self-rag-source.md
raw/papers/2026-05-29-crag-source.md
raw/papers/2026-05-29-a2rag-source.md
raw/papers/2026-05-29-hipporag-source.md
raw/repos/2026-05-29-graphrag-source.md
raw/papers/2026-05-29-lightrag-source.md
raw/articles/2026-05-29-graphiti-zep-temporal-validity-source.md
raw/papers/2026-05-29-reflexion-source.md
raw/papers/2026-05-29-rmm-reflective-memory-management-source.md
raw/papers/2026-05-29-memgpt-activation-tier-source.md
raw/repos/2026-05-29-rka-source.md
```

Depth judgment:

```text
SUFFICIENT for concept-level / principle-level absorption when reviewed together with the listed source records.
NOT sufficient to claim code-level behavior unless separately code-anchored.
```

### C. New Source Records Added For v0.3 Gaps

#### W3C Web Annotation Data Model

```text
local source record:
raw/articles/2026-05-30-w3c-web-annotation-source.md

official source:
https://www.w3.org/TR/annotation-model/#text-quote-selector
```

What it supports:

```text
source_anchor exact_quote + prefix + suffix as a stable source-span discipline.
```

Why code review is not needed:

```text
This is a standard/specification, not a library runtime adoption.
The framework borrows the selector concept only.
```

Depth judgment:

```text
SUFFICIENT for source_anchor mini-profile.
The source record now includes a readable context note in addition to short exact wording.
```

#### WiCER

```text
local source record:
raw/papers/2026-05-30-wicer-source.md

official source:
https://arxiv.org/abs/2605.07068
```

What it supports:

```text
omission_check:
generated or compiled wiki/digest output can fail by dropping critical facts.
```

Why code review is not needed:

```text
The framework adopts only the omission-check principle.
It does not adopt WiCER's algorithm, code, benchmark, or compile-refine runtime.
```

Depth judgment:

```text
SUFFICIENT for omission_check as a review principle.
NOT sufficient for implementing WiCER-style compile/evaluate/refine.
The source record now includes a readable context note in addition to short exact wording.
```

## v0.3 Ten Alpha Source-Depth Matrix

| Alpha | Current support | Depth required now | Status |
|---|---|---:|---|
| Evidence Packet | PaperTrail, ProVe/RAG attribution source records, local trials | paper/source records + local trial | sufficient |
| Warrant separation | TMS/reasons source record, Evidence-Aware Review rule, Pro-review compression | existing source record + local design trial | sufficient |
| Challenge taxonomy | Dung argumentation source record, Evidence-Aware Review rule, local integrated trial | existing source record + local trial | sufficient |
| Minimal revision needed | Point Collision / Knowledge Calibration rules, RKA decision superseding code anchor, local integrated trial | local architecture rule + RKA code anchor + trial | sufficient |
| Source anchor mini-profile | W3C Web Annotation Text Quote Selector | official spec source record | sufficient |
| Evidence granularity | ProVe/RAG attribution source records, RKA source-depth escalation, local trial | source records + local trial | sufficient |
| Omission check | WiCER source record + local heavy-digest trial | arXiv source record + local trial | sufficient |
| Context pack trace | W3C PROV, PaperTrail coverage, RAG attribution source records, local context trace | existing source records + local trial; platform source not required | sufficient |
| Agent memory quarantine | Reflexion/RMM source records, MemGPT activation source record, local boundary rule | concept/source records; no runtime adoption | sufficient for architecture, needs deeper review before MCP writes |
| Review due triggers | RKA code anchor, Graphiti targeted code anchor, Feedback Ledger source records | source/code mix | sufficient |

Names from the broader research report such as FEVER / AVeriTeC / SciFact, ASPIC+, AGM, GRADE / Cochrane, TrustGraph, and RAG eval platforms are not being used as proof for the v0.3 rules unless they have an explicit local source record or code anchor elsewhere.
They remain vocabulary / watch references only.

## Watch / Parked References That Do Not Need Source-Code Review Now

These are valuable but not core proof sources for v0.3:

```text
RAGAS
TruLens
Phoenix
DeepEval
OpenInference
RAG observability stacks
C2PA
OriginTrail DKG
RO-Crate
OpenLineage
Flowcept
Semantic MediaWiki
Wikibase
SHACL runtimes
ArchiveBox
Webrecorder / Browsertrix
SingleFile
Mem0 / OpenMemory
LangMem
Basic Memory
Engram
AICTX Memory
agentmemory
PaperQA2
Elicit systematic review
OpenAlex
Semantic Scholar
scite
Argdown / Cytoscape
DeepWiki-Open
CodeWiki / RepoDoc / Codebase-Memory
Repowise
SwarmVault
Omnigraph
```

Why not source-code review now:

```text
They are not adopted as runtime.
They are not adopted as truth architecture.
They are not required for current schema correctness.
They may inform future implementation or UI, but v0.3 only needs the lightweight evidence discipline.
```

## References That Need Deeper Review Before Future Implementation

If future work tries to implement these capabilities, source-code / API / runtime review becomes required:

```text
agent memory write tools:
  Mem0 / OpenMemory
  LangMem
  Basic Memory
  Engram
  AICTX Memory
  MCP Security Best Practices
  OWASP Agent Memory Guard

RAG evaluation / observability:
  RAGAS
  TruLens
  Phoenix
  DeepEval
  OpenInference

repo-to-wiki / generated documentation:
  DeepWiki-Open
  CodeWiki
  RepoDoc
  Codebase-Memory
  Repowise

source preservation / archive runtime:
  ArchiveBox
  Browsertrix
  SingleFile
  Webrecorder

formal provenance / publishing:
  C2PA
  OriginTrail DKG
  RO-Crate
  OpenLineage
  Flowcept
```

Future deep-review trigger:

```text
When any of the above changes from watch/reference into implementation dependency, create a source record and inspect actual docs/code/API behavior before writing schema or runtime hooks.
```

## What Pro Could Ask, And The Answer

### Did you inspect every referenced library's source code?

```text
No, intentionally.
That would be scope creep and would turn v0.3 into a platform survey.
```

### Which references did you inspect at code level?

```text
RKA exact commit 7bc2d76 for adopted workflow mechanics.
Graphiti commit 34f56e65 for narrow temporal validity / episode provenance anchors.
```

### Which references got new source records because they support v0.3 rules?

```text
W3C Web Annotation Data Model for source_anchor.
WiCER for omission_check.
```

### Are any adopted v0.3 rules still backed only by loose library names?

```text
In this refreshed package, each current v0.3 alpha is backed by a package-visible source record, exact code-anchor review, official standard/paper record, or local trial.
```

### Are watch references being used as proof?

```text
No.
Watch / parked references are explicitly not proof for current truth architecture.
They are future implementation candidates only.
```

## Final Judgment

```text
The reference depth is sufficient for v0.3 Pro review in this refreshed package.

The framework is not pretending to have code-reviewed every library.
It code-reviewed the only repository whose concrete workflow mechanics were adopted deeply: RKA.
It added targeted Graphiti code anchors for temporal validity because that mechanism affects applicability.
It added W3C Web Annotation and WiCER source records for source_anchor and omission_check.

All other broad references remain watch/adapt/parked unless future implementation pulls them into schema or runtime.
```
