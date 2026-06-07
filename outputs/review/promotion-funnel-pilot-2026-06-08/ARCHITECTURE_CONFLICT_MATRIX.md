# Architecture Conflict Matrix

## Scope

This sandbox note answers the follow-up question:

```text
Are the 15 inventory candidates already included in the main architecture, and
does any candidate conflict with it?
```

This file does not promote any claim, pattern, or decision. It is a
main-architecture comparison report only.

## Files Compared

Candidate side:

- `outputs/review/promotion-funnel-pilot-2026-06-08/CANDIDATE_INVENTORY.md`
- Candidate source notes under `wiki/patterns/` and
  `outputs/review/candidate_pattern_bank/`

Main architecture side:

- `AGENTS.md`
- `README.md`
- `SCHEMA.md`
- `FUSION_ARCHITECTURE_V0_2_DRAFT.md`
- `SOURCE_INTAKE.md`
- `REVIEW_QUEUE.md`
- `IMPLEMENTATION_BLUEPRINT.md`
- `DEV_CONTEXT.md`
- `MEMORY_TIER.md`
- `SECOND_BRAIN_MODEL.md`
- `wiki/indexes/knowledge-graph-index.md`

## Main Architecture Tests Used

The 15 candidates were compared against these architecture gates:

| Gate | Main architecture anchor | Meaning for this check |
|---|---|---|
| Thin truth core | `FUSION_ARCHITECTURE_V0_2_DRAFT.md:199`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md:2422`, `SCHEMA.md:37`, `SCHEMA.md:52` | No runtime, dashboard, retrieval, API, feedback, brief, or context pack may create truth directly. |
| Candidate before reviewed | `README.md:83-87`, `REVIEW_QUEUE.md:58`, `REVIEW_QUEUE.md:89-91`, `SCHEMA.md:516`, `SCHEMA.md:1637` | Raw/source and candidate material can be useful, but reviewed nodes require review/promotion. |
| Evidence support is source-span-to-target | `SCHEMA.md:121-123`, `SCHEMA.md:826-831`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md:1601`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md:1633-1639`, `REVIEW_QUEUE.md:273-283` | URL-only provenance, summary, retrieval hit, or background citation cannot count as support. |
| Evidence Sufficiency Gate is lazy | `SCHEMA.md:657`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md:993-1064`, `REVIEW_QUEUE.md:614-632`, `SOURCE_INTAKE.md:989-997` | Promotion/action use gets strict; ordinary capture/query should not become heavy. |
| Workbench and retrieval are not truth | `README.md:144-161`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md:765-815`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md:1251`, `SOURCE_INTAKE.md:992-1004`, `MEMORY_TIER.md:38-42` | Dashboards, graph rank, retrieval score, and activation tier are recall/workbench controls, not truth or support. |
| API/MCP/agent memory quarantine | `FUSION_ARCHITECTURE_V0_2_DRAFT.md:1281-1297`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md:3206`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md:3239`, `SCHEMA.md:1714-1736`, `AGENTS.md:255` | Agent/API surfaces can read or propose candidate material, but cannot bypass review and promotion. |
| Diagnostic evidence is not approval | `AGENTS.md:85`, `AGENTS.md:248`, `SCHEMA.md:153-155`, `SCHEMA.md:1789-1808`, `REVIEW_QUEUE.md:401-405` | Lint, tests, fixtures, LLM-judge output, and maintenance manifests are diagnostics or process evidence, not truth. |
| Source intake and answer support boundary | `SOURCE_INTAKE.md:675`, `SOURCE_INTAKE.md:983-1004`, `SOURCE_INTAKE.md:1008-1073` | Answer-bearing or action-adjacent support must return to an independent evidence/source anchor. |

## Short Answer

```text
All 15 were compared one by one against the main architecture.
No direct architecture conflict was found.
Most are already covered by the current architecture.
Several are implementation-level restatements of existing architecture rules.
The weak items are weak because their source anchors are not yet sufficient,
not because they contradict the architecture.
```

## One-by-One Comparison

| ID | Candidate | Main architecture coverage | Conflict check | Judgment |
|---|---|---|---|---|
| CI-01 | Self-contained review candidate record | Covered. `REVIEW_QUEUE.md:58` defines the queue as the place where raw sources become reviewable candidate points before promotion. `REVIEW_QUEUE.md:89-91` says candidate points stay inspectable and promotion stays reviewed. `wiki/indexes/knowledge-graph-index.md:239` already records self-contained review candidate as an llm-wiki-compiler implementation extraction. | No conflict if the record remains a candidate/review artifact. Conflict would appear only if a self-contained candidate body were treated as a reviewed node without review, which is blocked by `REVIEW_QUEUE.md:704` and `SCHEMA.md:1637`. | Already included as implementation discipline. Promotion would tighten candidate artifact quality, not add a new lane. |
| CI-02 | Review-gated compile queue | Covered. The public flow is source -> candidate -> reviewed node/relation in `README.md:83-87`. `IMPLEMENTATION_BLUEPRINT.md:107` and `wiki/indexes/knowledge-graph-index.md:253` describe the narrow source -> candidate -> lint/review -> verified node loop. | No conflict if the queue blocks direct formal writeback. Conflict would appear if watch/compile became formal promotion, which Fusion explicitly rejects as `watch auto-recompile as formal promotion` at `FUSION_ARCHITECTURE_V0_2_DRAFT.md:1896` and `automatic promotion` at `FUSION_ARCHITECTURE_V0_2_DRAFT.md:2407`. | Core-aligned. It is the current funnel shape, not a new architecture block. |
| CI-03 | Source hash registry and idempotent ingest | Partly covered. `SOURCE_INTAKE.md:621-631` covers source identity and provenance; `SOURCE_INTAKE.md:939` requires snapshot/version/selector-style anchors when sources change. `wiki/indexes/knowledge-graph-index.md` already lists OpenKB-derived ingest/idempotence work as implementation-level source handling. | No conflict if hash registry is source hygiene, dedupe, or derived state. Conflict would appear if the hash registry became source reliability, truth confidence, or a replacement for Markdown/YAML system-of-record, which `SCHEMA.md:37` rejects. | Compatible implementation support. Needs a later implementation decision: Markdown source record remains primary; any JSON/hash registry should be derived or auditable. |
| CI-04 | Decision outcome precondition before calibration | Covered. `README.md:206` says decision outcome calibration improves future recommendation, not truth. `FUSION_ARCHITECTURE_V0_2_DRAFT.md:79` and `FUSION_ARCHITECTURE_V0_2_DRAFT.md:2185` define outcome calibration as future recommendation/risk calibration. `wiki/indexes/knowledge-graph-index.md:195` records the RKA exact-commit precondition: final decision_outcome needs recommendation plus user_choice or explicit override. | No conflict. It reinforces the current decision/use-ledger boundary. Conflict would appear only if outcomes directly mutated truth confidence or verification status, which `wiki/indexes/knowledge-graph-index.md:207` rejects. | Already in main architecture. Promotion can create a clearer implementation pattern but should not create a new decision schema. |
| CI-05 | Scope dashboard live context surface | Covered as workbench/runtime, not truth core. `FUSION_ARCHITECTURE_V0_2_DRAFT.md:766` says this belongs to runtime/workbench, not truth core. `SCHEMA.md:418` says dev context packs can activate core/support/risk/cold references without changing truth status. `DEV_CONTEXT.md:431` says workbench/lifecycle ideas do not replace dev context pack or review gate. | No conflict if kept as a scope dashboard or dev-context candidate surface. Conflict would appear if dashboard state became truth, evidence support, reviewed relation, or action basis; Fusion flags `dashboard state as truth` at `FUSION_ARCHITECTURE_V0_2_DRAFT.md:2401`. | Architecture-compatible but evidence-weak. Keep candidate or needs-more-evidence until exact Dusk/template anchors and local trial are stronger. |
| CI-06 | Context pack evidence envelope | Covered. `SCHEMA.md:1820` defines future context pack shape; `SCHEMA.md:1939-1965` requires coverage-aware context packs and evidence sufficiency before action-ready finalization. `FUSION_ARCHITECTURE_V0_2_DRAFT.md:835-895` defines coverage and evidence detail levels for context packs. | No conflict if context pack is an evidence-aware read/activation envelope. Conflict would appear if a context pack itself decided truth or support; `SCHEMA.md:52` blocks context pack from deciding truth, and `FUSION_ARCHITECTURE_V0_2_DRAFT.md:3202-3209` says citation/retrieval/generated wiki/MCP memory are not proof or truth. | Already covered. It can become a reviewed implementation pattern, but not a new truth layer. |
| CI-07 | Agent context pack budget guardrails | Covered as a context-pack implementation guardrail. `IMPLEMENTATION_BLUEPRINT.md:355-406` includes minimum context pack shape, warnings, budget, coverage and evidence sufficiency. `wiki/patterns/agent-context-pack-budget-guardrails.md:39-52` gives candidate implementation detail from llm-wiki-compiler. | No conflict if budget/warnings/gaps constrain agent reads. Conflict would appear if budget trimming hid known gaps while still calling the pack action-ready; `SCHEMA.md:1963-1965` requires insufficiency/gaps to remain visible for action-ready use. | Compatible. Needs exact source-code anchors before promotion, but architecture already has room for it. |
| CI-08 | Claim-level provenance source ranges | Covered strongly. `SCHEMA.md:203`, `SCHEMA.md:707-711`, `SCHEMA.md:826-831`, and `SOURCE_INTAKE.md:675-706` require source ranges/anchors and make provenance distinct from support. `wiki/indexes/knowledge-graph-index.md:186` records Evidence Support Check as source-span-to-target, not source-node-level support. | No conflict. This is one of the core evidence rules. Conflict would appear only if source ranges were treated as support without checking span_supports_target; `FUSION_ARCHITECTURE_V0_2_DRAFT.md:1610-1639` blocks that. | Already mainline. Promotion would give a concrete implementation pattern for an existing evidence rule. |
| CI-09 | Source adapter ingest contract | Partly covered. `SOURCE_INTAKE.md:621-631` defines source identity; `AGENTS.md:91-117` and `SOURCE_INTAKE.md:525-575` define project-local video/source cards and retained transcript/ledger routing; `IMPLEMENTATION_BLUEPRINT.md:558-567` lists source/output/feedback adapters as implementation extension points. | No conflict if adapter normalizes source identity/provenance while leaving review/promotion elsewhere. Conflict would appear if adapter fields froze a heavy schema too early or if adapter output became reviewed knowledge. `AGENTS.md:117` explicitly says the video connector is not truth authority or promotion path. | Compatible source-intake implementation direction. Do not freeze a heavy adapter schema yet; promote only after adapter anchors are inspected. |
| CI-10 | Static wiki health lint before auto rewrite | Covered. `SCHEMA.md:153-155` permits lint/schema validation/health reports but no background rewrite or automatic conflict resolution. `SCHEMA.md:1789-1808` says maintenance manifest is lint, not automatic repair. `AGENTS.md:85` says maintenance manifests must not auto-repair reviewed knowledge or create truth/mainline readiness. | No conflict if lint reports issues and humans/Codex later repair deliberately. Conflict would appear if lint/test/fixture became reviewer approval or auto-fix of reviewed truth, which `AGENTS.md:248` and `REVIEW_QUEUE.md:401-405` block. | Already covered. Promotion should preserve "lint reports; it does not auto-fix reviewed truth." |
| CI-11 | Retrieval is activation, not truth | Covered very strongly. `README.md:144-161`, `SCHEMA.md:398-491`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md:743-815`, `SOURCE_INTAKE.md:992-1004`, and `MEMORY_TIER.md:38-42` all repeat that retrieval, graph rank, association score, community report, and activation tier are not truth/support/trust. | No conflict. The candidate is a restatement of a main architecture boundary. Conflict would appear only if retrieval score/rerank/GraphRAG/community report counted as evidence support or reviewed relation; blocked by `REVIEW_QUEUE.md:338-344` and `FUSION_ARCHITECTURE_V0_2_DRAFT.md:3320`. | Already mainline. No urgent promotion needed unless the vault wants a concise pattern note for this boundary. |
| CI-12 | Search to analysis before answer | Partly covered. `SOURCE_INTAKE.md:1008-1073` defines Answer Preparation / Independent Support Boundary: gather candidate supports, check key answer claims against independent evidence/source anchors, and separate answer-ready from action-ready. Fusion also requires late-stage action-facing review at `FUSION_ARCHITECTURE_V0_2_DRAFT.md:44-55` and non-circular warrant at `FUSION_ARCHITECTURE_V0_2_DRAFT.md:1012-1020`. | No conflict if used for important answer preparation. Conflict would appear if ordinary query always becomes a heavy audit or if answer-ready is treated as action-ready; both are blocked by `SCHEMA.md:657` and `SOURCE_INTAKE.md:1022-1029`. | Compatible but scoped. Keep candidate until underlying source/transcript anchors are inspected. |
| CI-13 | Source structure first for RAG | Partly covered. `SOURCE_INTAKE.md:675`, `SOURCE_INTAKE.md:983-1004`, and `FUSION_ARCHITECTURE_V0_2_DRAFT.md:793-815` already require source anchors and warn that TextUnit anchors are provenance, community reports are briefings, and graph rank is not trust. `wiki/indexes/knowledge-graph-index.md:203-204` records retrieval stratification as context-pack preparation, not truth. | No conflict if "source structure first" means preserving anchors and source shape before retrieval. Conflict would appear if this turned into a full RAG runtime as core architecture or if graph/community outputs became truth; `FUSION_ARCHITECTURE_V0_2_DRAFT.md:2070-2072` rejects that. | Compatible. Not promotion-ready until raw source/transcript/code anchors are reviewed beyond candidate bank summary. |
| CI-14 | Verified vault API for agent brain | Covered as parked/runtime direction. `SCHEMA.md:39` says API/MCP/viewer are final implementation capabilities but governed by truth contract. `FUSION_ARCHITECTURE_V0_2_DRAFT.md:1281-1297` says API/MCP/agent access starts read-only and no MCP write tools before review/write boundaries are stable. `SCHEMA.md:1714-1736` keeps agent access at Level 1 read-only for Misa/gbrain. | No conflict if API is read-only/context-pack-first and agent outputs enter as candidates. Conflict would appear if API/MCP writes bypassed review or agent memory became reviewed memory; `FUSION_ARCHITECTURE_V0_2_DRAFT.md:3206`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md:3239`, and `AGENTS.md:255` block that. | Compatible runtime direction, not ready as a decision. Needs implementation target, read/write boundary, and independent anchors. |
| CI-15 | PKM -> second brain -> personal AI companion | Partly covered as story/framing. `FUSION_ARCHITECTURE_V0_2_DRAFT.md:96` frames the project as a verified second brain; `SECOND_BRAIN_MODEL.md:101` does the same. `README.md:46`, `README.md:198`, and `README.md:207` support bounded context preparation and action basis, not autonomous truth/action. The current source record says ACM PDF access was 403 at `raw/papers/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-source.md:50`. | No conflict as a bounded framing. Conflict would appear if "companion" meant private-data auto-ingest, auto-belief, autonomous action, or weakening review/action gates. The candidate distillation itself warns against that at `outputs/review/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-candidate-distillation.md:57-64` and `:277-288`. | Compatible as narrative/activation framing, but not promotion-ready. Current evidence is metadata/abstract-level, not full-text architecture support. |

## Conflict Summary

No hard architecture conflict was found among the 15 candidates.

The actual risks are boundary failures, not new architectural incompatibilities:

```text
candidate -> treated as reviewed
source summary -> treated as independent proof
retrieval score / graph rank -> treated as support or trust
dashboard / workbench -> treated as truth
context pack -> treated as truth layer
lint / test / fixture / LLM judge -> treated as reviewer approval
API / MCP / agent memory -> treated as write authority or reviewed memory
AI companion framing -> treated as permission for private-data auto-ingest or auto-action
```

Those risks are already named and blocked by the current architecture.

## Coverage Buckets

Already strongly covered by main architecture:

- CI-01 Self-contained review candidate record
- CI-02 Review-gated compile queue
- CI-04 Decision outcome precondition before calibration
- CI-06 Context pack evidence envelope
- CI-08 Claim-level provenance source ranges
- CI-10 Static wiki health lint before auto rewrite
- CI-11 Retrieval is activation, not truth

Covered as implementation/runtime direction:

- CI-03 Source hash registry and idempotent ingest
- CI-07 Agent context pack budget guardrails
- CI-09 Source adapter ingest contract
- CI-14 Verified vault API for agent brain

Covered as workbench/framing/search discipline but still weak for promotion:

- CI-05 Scope dashboard live context surface
- CI-12 Search to analysis before answer
- CI-13 Source structure first for RAG
- CI-15 PKM -> second brain -> personal AI companion

## Promotion Implication

The comparison does not justify adding a new architecture layer, schema, lane,
or vocabulary.

For the promotion funnel, the useful distinction is:

```text
architecture-compatible + source-code-backed -> possible reviewed pattern
architecture-compatible + weak anchor -> keep candidate / needs more evidence
already-mainline boundary -> no need to promote unless a clearer pattern note is desired
```

Current implication:

- Promote-ready candidates from the evidence-packet pass remain implementation
  patterns, not architecture changes.
- Weak candidates should not be promoted until their independent anchors are
  stronger.
- Nothing in the 15 requires reopening the frozen SCHEMA / FUSION architecture
  work.
