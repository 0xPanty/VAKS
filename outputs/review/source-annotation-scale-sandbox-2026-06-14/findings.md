---
record_kind: sandbox_findings
status: active
created_at: 2026-06-14
scope: source-annotation-scale-product-sandbox
truth_boundary: sandbox_research_not_adopted_architecture
---

# Findings

## Current VAKS Contract

Source Annotation Sidecar is already defined as:

```text
source-local locator / review input
not support
not truth
not Project Overlay verdict
not action basis
```

Canonical path:

```text
outputs/review/source_annotations/<source-slug>/<annotation-id>.md
```

The product problem now is not the boundary; it is scale:

```text
many annotations -> triage burden -> project confusion -> anchor rot -> AI context noise
```

## Open Research Questions

1. What does W3C Web Annotation give us for selectors and lifecycle without importing a heavy ontology?
2. How should Obsidian/Bases views be organized so hundreds of annotations remain usable?
3. What is the smallest lifecycle that supports inbox, use, repair, and archive?
4. How do we package selected annotations for AI without pretending they are evidence?
5. What tests prove that the design stays comfortable as annotation count grows?

## External Research Notes - Round 1

### W3C Web Annotation

Source:

- https://www.w3.org/TR/annotation-model/
- https://www.w3.org/TR/annotation-vocab/

Useful absorption:

- Model the annotation as `body -> target`, not as "tag on note".
- `target` can point to arbitrary resource segments, including timed media.
- Keep the simple common case simple; do not import the full Linked Data stack.
- Use Web Annotation selector ideas as compatibility inspiration:
  - `TextQuoteSelector`: exact quote plus prefix/suffix.
  - `TextPositionSelector`: start/end character offsets.
  - media-specific selectors can exist, but irrelevant selector/media combinations should be ignored.

Do not absorb:

- Full RDF/JSON-LD ontology as a daily writing requirement.
- Inferencing or graph queries as the annotation product core.

### Hypothesis Fuzzy Anchoring

Source:

- https://web.hypothes.is/blog/fuzzy-anchoring/

Useful absorption:

- Robust anchoring needs multiple selectors, not one magic locator.
- Exact DOM/XPath-style locators are fast when structure is stable but brittle after page changes.
- Text position handles structure changes when text is unchanged.
- Text quote with prefix/suffix supports fuzzy recovery when structure or content changes.
- Re-attachment should have statuses, not silent success.

Implication for VAKS:

```text
exact_verified -> safe to inspect
fuzzy_recovered -> human should confirm before evidence use
ambiguous -> repair queue
broken -> repair queue
source_changed -> review pressure
```

### Obsidian Bases

Source:

- https://obsidian.md/help/bases
- https://obsidian.md/help/bases/syntax

Useful absorption:

- Bases are a local Markdown-property view layer.
- A `.base` can contain global filters and per-view filters.
- Views can be tables/lists/cards/map, but the data still lives in Markdown files and properties.

Implication for VAKS:

```text
Bases = workbench view
Markdown/YAML source_annotation = canonical record
Base sorting/filtering != evidence/truth/review
```

### Obsidian Inline Footnotes

Source:

- https://obsidian.md/help/syntax
- https://obsidian.md/help/plugins

Useful absorption:

- Inline footnotes are ergonomic capture handles.
- Obsidian documents inline syntax `^[This is an inline footnote.]`.
- Official syntax note says inline footnotes work in Reading view, not Live Preview.
- Footnotes view is a core plugin for showing footnotes from the current note.

Implication for VAKS:

```text
inline footnote = optional entrance / working-copy handle
sidecar source_annotation = canonical data
```

### RAG Attribution Warning

Source:

- https://arxiv.org/abs/2412.18004

Useful absorption:

- Citation correctness and citation faithfulness are different.
- A cited source can appear to support a statement even when the model did not genuinely rely on it.

Implication for VAKS:

```text
annotation locator != evidence support
source span included in AI context != faithful or sufficient answer support
Evidence Packet / evidence_support remains the support gate
```

## Subagent Synthesis

### Workbench and Obsidian UX

Use Bases as the daily workbench and keep Markdown sidecars as canonical data.

Recommended views:

```text
Annotation inbox
Source drilldown
Project lens
Routing queue
Needs anchor repair
Support checked audit
AI export ready / blocked
Cold archive
Stale anchors
Scale debt / consolidation queue
```

Fields shown by default should stay human-sized:

```text
source, role, short note, anchor status, review pressure, route refs
```

Long selectors, hashes, evidence packet fields, and audit fields should live in
details or repair/audit views.

### Anchor Model

Absorb the W3C/Hypothesis selector skeleton:

```text
TextQuoteSelector exact/prefix/suffix
TextPositionSelector start/end
line / timestamp / page rect for non-web sources
source hash / snapshot ref for drift detection
```

Do not absorb the full RDF, protocol, collection, rights, audience, or social
annotation stack.

The important split is:

```text
anchor_status = can we still find the span?
lifecycle_state = what are we doing with this record?
```

### Retrieval and AI Export

Authority bucket first:

```text
source_annotation -> review_input
raw source span -> inspectable context
Evidence Packet -> possible support after review
```

The AI pack must include original source windows and hard warnings. A selected
annotation cannot be packed as support.

### Red-Team Boundary

The main failure mode is not weak capture. It is over-trust:

```text
annotation becomes evidence
annotation becomes project verdict
annotation density becomes false consensus
fuzzy anchor becomes false precision
Base table order becomes truth ranking
```

The sandbox therefore tests action-basis denial, truth-mutation denial, project
scope pollution, evidence packet requirements, duplicate ID detection, stale
anchor separation, bad anchor separation, and bad context-pack support refs.

## Sandbox Test Findings

Current validation result:

```text
35 good annotations passed
7 mutation annotations caught
1 bad context pack caught
0 good-corpus errors
4 scale warnings surfaced
```

Workbench pressure results:

```text
AI export ready: 30
Needs anchor repair: 3
Stale anchors: 1
Scale debt: 29
Project lens: 14
Support checked audit: 1
Cold archive: 1
```

The warnings are useful. They show the product can surface density and duplicate
pressure instead of hiding it:

```text
one source over the active annotation budget but has a source digest route
three selector duplicate pressure groups visible for consolidation
```

Conclusion:

```text
The design is structurally ready as a sandbox candidate.
The remaining proof is lived Obsidian use: real Base ergonomics, real repair
friction, and real AI context quality over a larger vault sample.
```

## External Product Benchmark - World-Class Pass

### Zotero

Source:

- https://www.zotero.org/support/kb/annotations_in_database

Useful absorption:

- Zotero keeps annotations in its database rather than writing them directly
  into the PDF so sync, conflict handling, tags, filters, and export remain
  manageable.
- It still preserves portability by allowing annotated PDF export.

VAKS implication:

```text
canonical source_annotation sidecar is the right spine
raw/source file should stay clean
export is a derived action, not the canonical storage layer
```

### Readwise Reader

Sources:

- https://docs.readwise.io/reader/docs/faqs/adding-new-content
- https://docs.readwise.io/reader/llms.txt

Useful absorption:

- Reader separates manually saved Library items from automatic Feed items.
- It has Inbox / Later / Archive style locations for operating on reading
  queues.
- Browser capture is optimized for flow, including highlighting on the open web
  when the user does not want to break reading flow.
- It treats web highlighting as an exception handler because parsing cannot be
  perfect.
- AI features can be disabled, prompts are scoped, and AI receives only the
  relevant part of the document for some actions.
- It separates document tags and highlight tags; highlight views can jump back
  to original context.

VAKS implication:

```text
working inbox != locator pool
capture must not break reading flow
open-web/original-source capture is an exception path, not a truth path
AI export must be scoped and optional
document/project grouping must not inherit into each highlight as truth
```

### Hypothesis

Source:

- https://web.hypothes.is/blog/fuzzy-anchoring/

Useful absorption:

- Reliable annotation requires mapping between rendered DOM and plain text.
- Fuzzy anchoring is not trivial; whitespace, CSS-hidden text, DOM structure,
  and source changes create real failure modes.
- Anchor computation is expensive enough that mapping is built and reused.

VAKS implication:

```text
do not pretend exact quote is always enough
store multiple selectors and source snapshots
surface anchor health explicitly
cache/check lazily rather than recomputing everything on every ordinary use
```

### Obsidian Bases

Sources:

- https://obsidian.md/help/bases
- https://obsidian.md/help/bases/syntax

Useful absorption:

- Bases are views over local Markdown files and properties.
- A `.base` file can define multiple filtered views and formulas.
- Data remains in Markdown; views are a workbench surface.

VAKS implication:

```text
Base view order is not trust
Base filter is not schema
Base should show queues, counts, and routes
canonical source_annotation remains Markdown sidecar
```

## World-Class Criteria

The design should be judged by these product criteria, not by conceptual
cleverness:

| Criterion | Meaning | Gate |
|---|---|---|
| Flow | capture does not break reading | <= 5 human-facing capture fields |
| Calm scale | daily inbox stays small | p95 working inbox within operator capacity |
| Reversibility | source stays clean and exportable | sidecar canonical, raw source unpolluted |
| Repairability | bad anchors become visible work | 100% bad/stale queue coverage |
| Authority safety | AI cannot turn marks into proof | 0 support/action contamination |
| Progressive disclosure | details are available but hidden by default | default views hide long selectors/audit fields |
| Operator leverage | large pool is machine-queryable, human queue is small | locator pool separated from working inbox |
| Portability | nothing is locked in a UI | Markdown/YAML records and JSON/Markdown exports |
