# Findings & Decisions

## Requirements

- Create a dedicated VAKS retrieval-layer design workspace.
- Use the recent `turbovec` distillation as an input.
- Do not finalize the custom VAKS retrieval design yet.
- First absorb mainstream and frontier retrieval/vector designs.
- Preserve VAKS's strong boundary governance while improving retrieval efficiency and accuracy.

## Initial Architecture Finding

The useful framing is:

```text
VAKS is not trying to become a normal RAG app.
VAKS is trying to build boundary-governed retrieval for action-capable knowledge.
```

So the target is not just:

```text
retrieve the most semantically similar chunks
```

The target is:

```text
retrieve the best allowed anchors for this task,
from the right authority bucket,
with enough context to expose support, challenge, risk, staleness, and gaps.
```

## What turbovec Adds

`turbovec` is useful as a candidate for:

```text
local compressed vector cache
allowlist dense rerank
stable external ID mapping
privacy-friendly / air-gapped retrieval
fast context-pack candidate retrieval
```

It should not be used as:

```text
truth store
reviewed relation engine
confidence scorer
action-basis generator
mainline dependency before pilot
```

Best VAKS-shaped usage:

```text
metadata / status / project / authority bucket filter
-> allowed chunk IDs
-> turbovec reranks inside allowlist
-> anchor queue
-> context pack
-> evidence/action gate if needed
```

## What Mnemosyne Adds

`mnemosyne` is useful as a candidate for:

```text
local-first SQLite-derived retrieval cache
sqlite-vec + FTS5 hybrid recall
polyphonic recall: vector / graph / fact / temporal voices
query cache for repeated context-pack retrieval
embedding lifecycle hygiene and stale-index cleanup
visible fallback when vector infrastructure is unavailable
```

It should not be used as:

```text
truth store
evidence support engine
review authority
agent memory authority
benchmark proof
mainline dependency before VAKS pilot
```

Best VAKS-shaped usage:

```text
query intent
-> scope / project filter
-> authority bucket filter
-> source hash / freshness filter
-> sqlite / FTS / vector / relation recall inside allowed buckets
-> bucket-local RRF or rerank
-> anchor queue
-> context pack
-> evidence/action gate if needed
```

Design distinction:

```text
turbovec = compact vector cache / rerank primitive
mnemosyne = local retrieval-layer composition pattern
```

The strongest borrow is not Mnemosyne's benchmark claim. The strongest borrow is its engineering shape: derived local cache, graceful fallback, multi-voice recall, query-cache surface, and stale embedding cleanup.

## What cBrain Official Mindmap Adds

The `cBrain官网` public mindmap is useful as a candidate for:

```text
structure-first retrieval entry
tree navigation before blank-box search
layered search: node title / note content / library content
node workbench that combines title, note, links, and action entry
knowledge-quantity style activation signals
learning moves that map to retrieval operations: down / up / left / center
```

It should not be used as:

```text
truth schema
reviewed relation model
evidence support model
action-basis model
kq-as-truth-confidence
public-share policy for VAKS raw/candidate material
```

Best VAKS-shaped usage:

```text
retrieval home / workbench
-> user chooses task or structure area
-> system derives allowed authority buckets
-> title/path/alias/BM25/vector retrieval runs inside allowed scope
-> result becomes anchor queue with visible layer/status/use limits
-> context pack or evidence/action gate happens downstream
```

Design distinction:

```text
turbovec = compact vector cache / rerank primitive
mnemosyne = local retrieval-layer composition pattern
cBrain official mindmap = retrieval workbench and structure-first UX pattern
```

The strongest borrow is the product shape: do not make retrieval start from a blank search box only. Give users a visible map of possible drawers, then let search operate inside the right drawer.

## What cBrain Offline Package Black-box Adds

The public `cBrain-1.3.2.zip` package is useful as a candidate for:

```text
local-first data package shape
graph.json nodes / links as a navigation index
Markdown note files as readable content bodies
domain object records linked to nodes: books / objectives / tasks / time / drawings / music
canvas JSON as a visual workbench layer
AI-friendly export modes: standard / full / graph-only / text-only
lazy migration instead of one-shot full migration
```

It should not be used as:

```text
private implementation source
truth schema
evidence support model
proof that local/offline results are trustworthy
reason to replace VAKS Markdown/YAML authority with an app package
```

Best VAKS-shaped usage:

```text
durable markdown store
-> anchor manifest
-> rebuildable relation / activation cache
-> domain object links
-> BM25 / sparse / vector indexes inside allowed buckets
-> exportable context pack modes with authority and allowed-use labels
```

Design distinction:

```text
cBrain public mindmap = workbench/navigation pattern
cBrain offline package = data-shape and export/migration pattern
```

The strongest borrow is not the app's private implementation. The strongest borrow is the visible data contract: graph for navigation, Markdown for content, domain objects for workflow, exports for human/AI reuse.

## P1 Knowledge Point: cBrain Quality Transparency Label

The cBrain/Kimi quality label example is useful as a P1 candidate for:

```text
human-readable quality transparency
personal model rigor labels
source / trust / consensus hints
scope-in and scope-out display
risk checks on macro theory / closed loops / abstraction / authority bias
last-checked and reviewer visibility
```

It should not be used as:

```text
truth confidence
evidence support
reviewed relation
action readiness
automatic promotion gate
```

Best VAKS-shaped usage:

```text
retrieval hit
-> anchor card
-> knowledge_status / allowed_use
-> transparency_label
-> scope_in / scope_out
-> risk_flags
-> context pack or review route
```

Design distinction:

```text
VAKS already has strict backend fields.
cBrain quality label adds a readable front-facing explanation layer.
```

The strongest borrow is "transparent rigor" for personal models: mark a method note as practice-based, niche, scoped, and risky where needed, without pretending it is an academic or reviewed claim.

## What Graphify Adds

`safishamsi/graphify` is useful as a P1 candidate for:

```text
derived code/document knowledge graph
AST-first source and symbol anchors
community-neighborhood activation
query/path/explain style agent orientation
MCP-style read-only graph tools
incremental graph/cache rebuild hygiene
graph-output safety guardrails
```

It should not be used as:

```text
truth store
reviewed relation engine
evidence support checker
action-basis generator
default forced hook system
mainline dependency before pilot
```

Best VAKS-shaped usage:

```text
query intent
-> authority / scope bucket filter
-> allowed node or chunk set
-> graph seed search + neighborhood expansion
-> community / bridge / risk hints
-> anchor queue with allowed-use labels
-> context pack
-> evidence / action gate when needed
```

Design distinction:

```text
turbovec = compact vector cache / rerank primitive
mnemosyne = local-first retrieval-layer composition pattern
cBrain official mindmap = retrieval workbench and structure-first UX pattern
cBrain offline package = data-shape and export/migration pattern
cBrain quality label = readable boundary/rigor display pattern
Graphify = structural graph retrieval and agent query surface
```

The strongest borrow is not Graphify's benchmark claim. The strongest borrow is its engineering shape: deterministic structure extraction before model interpretation, a rebuildable graph cache, and small graph-query tools that orient agents before they read raw source.

## What OneFeed Adds

`arXiv:2606.07972 OneFeed` is useful as a P2 candidate for:

```text
explicit query + implicit activation fusion
controlled query generation for candidate expansion
semantic-ID / query alignment as an intent-anchor bridge
candidate usefulness as a query-generation quality check
closed-loop feedback for activation and routing
leakage-prevention checklist for retrieval experiments
```

It should not be used as:

```text
benchmark evidence
truth store
action-basis support
feedback-driven truth update
generated-query authority
proof that search/recommendation fusion improves VAKS
```

Best VAKS-shaped usage:

```text
user query + active project context + feedback hints
-> controlled query variants
-> authority / scope bucket filter
-> lexical / vector / graph recall inside allowed buckets
-> anchor queue
-> context pack
-> feedback updates activation only
```

Design distinction:

```text
turbovec = compact vector cache / rerank primitive
mnemosyne = local-first retrieval-layer composition pattern
cBrain official mindmap = retrieval workbench and structure-first UX pattern
cBrain offline package = data-shape and export/migration pattern
cBrain quality label = readable boundary/rigor display pattern
Graphify = structural graph retrieval and agent query surface
OneFeed = query-generation-assisted candidate expansion and feedback routing
```

The strongest caution is as important as the borrow: this paper explicitly
labels its main tables as expected estimates and keeps full training/baselines/
ablations in a checklist, so it should not be treated as empirical support.

## Core Design Tension

Retrieval systems usually optimize:

```text
speed
recall
semantic similarity
developer convenience
```

VAKS additionally must optimize:

```text
authority separation
candidate vs reviewed boundary
source-anchor traceability
counterevidence visibility
action-basis quarantine
feedback not mutating truth
```

The custom design should treat those as first-class retrieval requirements, not extra paperwork.

## Early Hypothesis

The likely final shape is not one retrieval engine. It is a layered retrieval pipeline:

```text
1. query intent router
2. authority / scope bucket filter
3. lexical + vector + entity + tag recall inside allowed buckets
4. rerank inside each bucket
5. anchor queue with source/chunk spans
6. context pack roles: core / support / risk / cold
7. sufficiency and action-basis gate for high-stakes use
8. query-run feedback for future activation only
```

## Resources

- `outputs/review/2026-06-11-RyanCodrai-turbovec-candidate-distillation.md`
- `wiki/summaries/2026-06-11-RyanCodrai-turbovec-architecture-review.md`
- `outputs/review/project_lens_overlays/2026-06-11-turbovec-vector-retrieval-cache.md`
- `outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md`
- `wiki/summaries/2026-06-11-AxDSan-mnemosyne-architecture-review.md`
- `outputs/review/project_lens_overlays/2026-06-11-mnemosyne-vector-memory-layer.md`
- `outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/source-card.md`
- `outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/candidate-distillation.md`
- `outputs/review/vaks-retrieval-layer-design-2026-06-11/cbrain-official-mindmap-2026-06-11/offline-package-blackbox-notes.md`
- `outputs/review/vaks-retrieval-layer-design-2026-06-11/p1-cbrain-knowledge-quality-transparency-label.md`
- `raw/repos/2026-06-11-safishamsi-graphify-source.md`
- `outputs/review/2026-06-11-safishamsi-graphify-candidate-distillation.md`
- `wiki/summaries/2026-06-11-safishamsi-graphify-architecture-review.md`
- `outputs/review/project_lens_overlays/2026-06-11-graphify-graph-retrieval-layer.md`
- `outputs/review/vaks-retrieval-layer-design-2026-06-11/p1-graphify-code-graph-retrieval-layer.md`
- `raw/papers/2026-06-11-guoxun-onefeed-source.md`
- `outputs/review/2026-06-11-guoxun-onefeed-candidate-distillation.md`
- `wiki/summaries/2026-06-11-guoxun-onefeed-architecture-review.md`
- `outputs/review/project_lens_overlays/2026-06-11-onefeed-search-recommendation-fusion.md`
- `outputs/review/vaks-retrieval-layer-design-2026-06-11/p2-onefeed-feed-search-query-generation.md`
- `SOURCE_INTAKE.md`
- `SCHEMA.md`
- `FUSION_ARCHITECTURE_V0_2_DRAFT.md`
- `DEV_CONTEXT.md`
- `FEEDBACK.md`

## Open Research Need

The next research pass should compare at least these families:

```text
embedded vector index / quantization
vector database filtering and payload indexes
BM25 / SPLADE / sparse retrieval
hybrid retrieval and RRF
late-interaction rerankers
cross-encoder rerankers
GraphRAG / LightRAG / relation-neighborhood retrieval
chunking and semantic document layout
retrieval evaluation / attribution / sufficiency checks
local-first and privacy-preserving retrieval
```
