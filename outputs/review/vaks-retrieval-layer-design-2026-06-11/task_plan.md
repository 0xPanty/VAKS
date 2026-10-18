# Task Plan: VAKS Retrieval Layer Design

## Goal

Create a candidate-only design workspace for the VAKS retrieval layer, absorb mainstream/frontier retrieval designs first, then propose a VAKS-specific retrieval architecture that keeps high recall/efficiency without losing boundary governance.

## Current Phase

Phase 2

## Phases

### Phase 1: Workspace Bootstrap

- [x] Create a dedicated candidate workspace.
- [x] Record the truth/action boundary.
- [x] Seed the initial design hypothesis.
- **Status:** complete

### Phase 2: Frontier Source Absorption

- [ ] Distill representative vector index / vector database / hybrid retrieval / reranking / graph retrieval / chunking / evaluation sources.
- [ ] Keep each source candidate-only.
- [ ] Add each source to `frontier-source-ledger.md`.
- **Status:** in progress
- **Current absorbed inputs:** `turbovec`, `mnemosyne`, `cBrain official mindmap`, `cBrain 1.3.2 offline package`, `cBrain quality transparency label`, `graphify`, `OneFeed`

### Phase 3: Comparison Matrix

- [ ] Compare sources by retrieval efficiency, recall, filtering model, update model, local-first fit, boundary risk, and VAKS fit.
- [ ] Separate engineering value from truth/action authority.
- **Status:** pending

### Phase 4: VAKS Custom Retrieval Architecture

- [ ] Draft the custom retrieval path.
- [ ] Define bucket filtering, hybrid recall, rerank, anchor queue, context-pack assembly, and evidence/action gate boundaries.
- [ ] Define what lives in rebuildable cache vs Markdown/YAML authority.
- **Status:** pending

### Phase 5: Pilot Design

- [ ] Create a small benchmark plan using real VAKS markdown chunks.
- [ ] Compare current retrieval, BM25, vector, hybrid, and bucket-filtered vector rerank.
- [ ] Measure recall, source-anchor correctness, and boundary violations.
- **Status:** pending

### Phase 6: Mainline Proposal Gate

- [ ] Only after the pilot, write a proposed minimal mainline patch or ADR draft.
- [ ] Keep the proposal separate from adoption.
- **Status:** pending

## Key Questions

1. How can VAKS improve semantic recall without letting vector similarity become authority?
2. How should raw / candidate / reviewed / overlay / feedback buckets be filtered before ranking?
3. Which retrieval signals should be allowed inside each authority bucket?
4. What is the minimum chunk/anchor model needed for accurate context packs?
5. What evidence is required before a retrieval result can become action-facing support?
6. Which parts should be local files, rebuildable cache, or future runtime service?

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Put this workspace under `outputs/review/` | It is candidate design material, not reviewed truth or architecture adoption. |
| Treat turbovec as P1 candidate for retrieval cache, not mainline dependency | It is useful for local compressed vector rerank, but still needs VAKS pilot evidence. |
| Treat mnemosyne as a P1 candidate for local-first hybrid retrieval-layer composition | It contributes SQLite-derived cache, sqlite-vec/FTS5 hybrid recall, polyphonic recall, query cache, and embedding lifecycle hygiene, but not truth or action authority. |
| Treat cBrain official mindmap as a P1 candidate for retrieval workbench/navigation, not retrieval authority | It contributes structure-first entry, layered search, node workbench, and activation signals, but its tree/kq/UI links cannot become evidence support or truth confidence. |
| Treat cBrain offline package as a P1 candidate for data-shape and export/migration design, not private implementation | It contributes graph + Markdown + domain-object layout, AI-friendly export modes, and lazy migration posture, but app code and local/offline data cannot become authority. |
| Treat cBrain quality transparency label as a P1 candidate for retrieval workbench display, not truth scoring | It contributes a readable rigor/source/trust/consensus/scope/risk label for personal models, but the label cannot replace evidence support, confidence review, or action readiness. |
| Treat Graphify as a P1 candidate for structural graph retrieval and agent orientation, not truth or action authority | It contributes AST-first anchors, derived graph cache, community activation, scoped graph query tools, MCP surface, and safety guardrails, but graph rank/community/confidence cannot become support. |
| Treat OneFeed as a P2 candidate for controlled query expansion and feedback routing, not empirical support | It contributes explicit/implicit intent fusion and query-generation-assisted recall, but the paper reports expected estimates and cannot support adoption claims. |
| Use bucket-first retrieval as the non-negotiable boundary | VAKS must not let relevance ranking collapse authority levels. |
| Delay custom final design until more frontier sources are absorbed | The user wants a stronger design after seeing the market/frontier space, not a premature local-only answer. |

## Errors Encountered

| Error | Attempt | Resolution |
|-------|---------|------------|
| None | 1 | N/A |

## Notes

- This workspace does not change `SCHEMA.md`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md`, or reviewed wiki files.
- Every source absorbed here remains candidate-only until later review.
- Strong retrieval performance is not enough; boundary-preserving retrieval is the actual design target.
