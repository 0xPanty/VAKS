# Combined Rescreen For Review

## Scope

This sandbox file puts the promotion pilot and the development-area Project Lens
view together for a careful one-by-one review.

It combines:

- the original 15 promotion-funnel candidates;
- 7 additional VAKS Project Lens / candidate-pattern-bank points that were not
  in the first 15-candidate inventory.

This file does not promote anything. It does not change the main architecture.

## Boundary

Use this file as a review table, not as a truth source.

```text
Project tag / P1 / partial / watch = worth looking at for VAKS.
Source/code anchor + Evidence Packet = possible promotion support.
Project Lens / candidate bank = routing and borrowing pressure, not reviewed proof.
```

## Inputs Rechecked

Sandbox outputs:

- `CANDIDATE_INVENTORY.md`
- `PROMOTION_EVIDENCE_PACKETS.md`
- `PROMOTION_RECOMMENDATIONS.md`
- `ARCHITECTURE_CONFLICT_MATRIX.md`
- `PROJECT_TAG_PRIORITY_CROSSWALK.md`

Development-area project view:

- `outputs/review/project_lens_overlays/VAKS.md`
- `outputs/review/project_borrowing_ledgers/VAKS.md`
- `outputs/review/source_cards/2026-06-04-external-intake-source-routing-ledger.md`
- `outputs/review/candidate_pattern_bank/*.md`
- `outputs/review/2026-06-07-aal-ruller-pkm-second-brain-ai-companian-candidate-distillation.md`

Main architecture comparison anchors:

- `README.md`
- `SCHEMA.md`
- `FUSION_ARCHITECTURE_V0_2_DRAFT.md`
- `SOURCE_INTAKE.md`
- `REVIEW_QUEUE.md`
- `IMPLEMENTATION_BLUEPRINT.md`
- `DEV_CONTEXT.md`
- `MEMORY_TIER.md`
- `FEEDBACK.md`
- `SECOND_BRAIN_MODEL.md`
- `wiki/indexes/knowledge-graph-index.md`

## Total Count

```text
Original promotion-funnel candidates: 15
Extra development-area Project Lens points: 7
Combined review set: 22
Hard architecture conflicts found: 0
```

Fullness check:

```text
Current VAKS Project Lens primary overlay has 10 Lens Entry blocks.
Three overlap the original 15 candidates: CI-11, CI-12, CI-13.
Seven are extra Project Lens points: PL-01 through PL-07.
Aal/Ruller has the explicit P1/P2/P3 borrow_order and is counted as CI-15.
Older project-lens sandbox/test files were not counted as new reference points.
```

## Rescreen Buckets

| Bucket | Count | Items | Meaning |
|---|---:|---|---|
| Ready for formal promotion review | 4 | CI-01, CI-02, CI-03, CI-04 | Project fit and inspected evidence anchors are both strong enough for a narrow reviewed pattern proposal. |
| Next anchor pass | 5 | CI-06, CI-08, CI-10, CI-09, CI-07 | Architecture fit is strong, but exact source/code anchors or local scope decisions still need a pass. |
| Borrow as Project Lens / candidate only | 12 | CI-05, CI-11, CI-12, CI-13, CI-15, PL-01, PL-02, PL-03, PL-04, PL-05, PL-06, PL-07 | Useful for VAKS thinking, but not enough for reviewed promotion now. |
| Park as future runtime/decision direction | 1 | CI-14 | Compatible with architecture, but should not become a decision until read/write/API boundaries are concrete. |

## One-by-One Combined Table

| ID | Point | Existing tag / dev signal | Main architecture coverage | Evidence state | Can borrow? | Can promote now? | Next review question |
|---|---|---|---|---|---|---|---|
| CI-01 | Self-contained review candidate record | `adoption_status: adopt-now`; `verified-knowledge-system`; pattern/review | Already covered by review queue: candidates must be inspectable before promotion. | Direct source/code anchors from llm-wiki-compiler candidate and approve flow. | Yes. Borrow as candidate artifact discipline. | Yes, as narrow reviewed pattern. | Do we update existing pattern file, or create a promotion receipt first? |
| CI-02 | Review-gated compile queue | `adoption_status: adopt-soon`; `verified-knowledge-system`; pattern/llm-ingest | Already covered by source -> candidate -> lint/review -> reviewed node flow. | Direct source/code anchors from compile `--review` and approve flow. | Yes. Borrow as the core funnel guard. | Yes, as narrow reviewed pattern. | Promote only queue-before-wiki, not automatic compile/runtime. |
| CI-03 | Source hash registry and idempotent ingest | `adoption_status: adopt`; source-state/idempotency | Covered as source identity/provenance and source hygiene; not truth. | Direct OpenKB code anchors; source lifecycle support. | Yes. Borrow as source hygiene. | Yes, if scoped to ingest hygiene. | Should hash registry be derived from Markdown source records, not a separate truth store? |
| CI-04 | Decision outcome precondition before calibration | RKA source-code review; decision/calibration/use-ledger | Covered by decision outcome calibration: future recommendation, not truth. | Exact RKA commit code anchors checked. | Yes. Borrow as Use Ledger hardening. | Yes, as narrow pattern. | How do we word the pattern without importing RKA runtime/dashboard/SQLite? |
| CI-05 | Scope dashboard live context surface | `adoption_status: adapt`; dev-context/dashboard/workbench | Covered as workbench/dev-context surface, not truth core. | Single-source Dusk/template evidence; no local trial yet. | Yes, as workbench idea. | No. | Should we run one local VAKS dev-context trial before promotion? |
| CI-06 | Context pack evidence envelope | `adoption_status: adopt-soon`; context-pack/agent-api; VAKS + Misa | Covered strongly by context pack/action basis evidence envelope. | Direct llm-wiki-compiler context pack anchors exist, but not selected in first packet. | Yes. | Not yet in this pilot; close. | Do an anchor pass and decide minimal VAKS context-pack shape. |
| CI-07 | Agent context pack budget guardrails | `adoption_status: adopt-soon`; context-pack/agent/budget | Covered as context pack budget/warnings/gaps/source-window safety. | Candidate note has implementation anchors, but exact local line anchors still needed. | Yes. | No, needs anchor pass. | Inspect `budget.ts`, `provenance.ts`, retrieval warning behavior. |
| CI-08 | Claim-level provenance source ranges | `adoption_status: adopt-soon`; provenance/evidence | Core architecture already requires source ranges/anchors and source-span-to-target support. | Strong concept fit; exact linter/citation anchors still need targeted pass. | Yes. | No, needs anchor pass. | Should this become the next reviewed evidence-pattern after CI-01..04? |
| CI-09 | Source adapter ingest contract | `adoption_status: adopt-soon`; source-adapter/ingest | Covered by Source Intake, video source cards, provenance, adapter extension points. | Candidate note cites source support; adapter line anchors not inspected in pilot. | Yes. | No, needs anchor pass. | Which adapter fields are stable enough, and which stay flexible? |
| CI-10 | Static wiki health lint before auto rewrite | `adoption_status: adopt-soon`; lint/health-check | Covered by lint/maintenance manifest as diagnostic, not auto-repair. | Good pattern evidence; local lint scope/code anchors still need check. | Yes. | No, needs anchor pass. | Which first lint rules are safe without creating auto-repair pressure? |
| CI-11 | Retrieval is activation, not truth | Project Lens `partial`; source families RAG/memory/graph | Already one of the strongest mainline boundaries. Retrieval/rank/community reports are not truth/support. | Candidate-bank and source-family routing; underlying sources not individually packet-reviewed here. | Yes, strongly as boundary wording. | Not necessary now; already mainline. | Do we want a concise reviewed pattern note, or is architecture text enough? |
| CI-12 | Search to analysis before answer | Project Lens `watch`; high-impact answer drafting | Covered by Answer Preparation / Independent Support Boundary and late-stage action-facing review. | Candidate-bank routing; raw video/source anchors not packet-reviewed. | Yes, only for important answers. | No. | Keep ordinary query light; when exactly does answer prep become mandatory? |
| CI-13 | Source structure first for RAG | Project Lens `partial`; maps to `SOURCE_INTAKE.md` | Covered by source anchors, source structure, GraphRAG/LightRAG retrieval stratification as context prep. | Candidate-bank routing; underlying source anchors need review. | Yes, as source-intake pressure. | No. | Should this be the first RAG/source-intake anchor pass item? |
| CI-14 | Verified vault API for agent brain | `adoption_status: candidate`; agent-context/gbrain/API | Covered as parked runtime direction: API/MCP read surface, no write tools before review boundaries. | Medium evidence and older pattern; no current implementation target. | Yes, as future runtime direction. | No. | What is the first read-only/context-pack API shape, and what stays forbidden? |
| CI-15 | PKM -> second brain -> personal AI companion | Explicit `P1/P1/P1/P2/P3`; `possible_project_refs: verified-action-knowledge-system` | Covered as verified second-brain / bounded activation framing, not autonomous truth/action. | Metadata/abstract only; ACM PDF access 403; full text not inspected. | Yes, as P1 framing and risk boundary. | No. | Can we get full text or independent anchors before turning any claim into reviewed knowledge? |
| PL-01 | File-first agent workbench | Project Lens `watch`; candidate bank; source families agent-workbench/Obsidian | Covered by Markdown/YAML system-of-record, workbench/runtime outside truth core, API/MCP read boundaries. | Candidate-bank routing; source-family evidence only. | Yes, as future workbench principle. | No. | Which files should be visible operation traces versus reviewed knowledge? |
| PL-02 | Adaptive retrieval depth | Project Lens `watch`; activation/context-pack budget | Covered by Activation Tier, lazy retrieval expansion, ordinary query stays simple. | Candidate-bank routing; source-family evidence only. | Yes, as activation-budget idea. | No. | What query types deserve slow/deep retrieval, and what remains ordinary? |
| PL-03 | Memory granularity and quarantine | Project Lens `watch`; memory/agent-workbench | Covered by feedback not truth, agent memory quarantine, review_due pressure, candidate/feedback-event writes. | Candidate-bank routing; source-family evidence only. | Yes, as future agent-memory boundary. | No. | How to avoid quarantine becoming a permanent junk drawer or hidden memory layer? |
| PL-04 | Graph and ontology as candidate context | Project Lens `watch`; graph/ontology/RAG | Covered by optional point graph fragments, candidate_relation, reviewed relation boundaries, graph rank not trust. | Candidate-bank routing; source-family evidence only. | Yes, as review aid/context organization. | No. | When does a graph fragment help review instead of making weak extraction look precise? |
| PL-05 | Visual workbench for retrieval diagnostics | Project Lens `partial/prototype`; RAG/workbench diagnostics | Covered by dashboard/workbench as runtime aid, not truth; diagnostics not approval. | Candidate-bank routing; source-family evidence only. | Yes, as future reviewer/operator surface. | No. | What minimal visual/diagnostic view helps without creating dashboard authority? |
| PL-06 | Skills and prompts as visible files | Project Lens `watch`; agent-workbench/tool-safety | Covered by future agent tool safety, visible files, MCP/hooks/skills caution, no agent self-approval. | Candidate-bank routing; source-family evidence only. | Yes, as future tool-safety/workbench idea. | No. | What permission/quarantine rules are needed before skill/prompt files can be edited? |
| PL-07 | Simple-first retrieval baseline | Project Lens `watch`; ordinary query/retrieval baseline | Covered by Karpathy-simple UX, start with simple local search, BM25/vector/cache as derived layers. | Candidate-bank routing; source-family evidence only. | Yes, as implementation heuristic. | No. | What small baseline should ordinary query use before adding heavier retrieval? |

## Human Reading Order For The Next Review

Recommended order for going one by one:

```text
1. CI-01
2. CI-02
3. CI-03
4. CI-04
5. CI-06
6. CI-08
7. CI-10
8. CI-09
9. CI-07
10. CI-11
11. CI-13
12. CI-12
13. CI-05
14. CI-15
15. CI-14
16. PL-01
17. PL-02
18. PL-03
19. PL-04
20. PL-05
21. PL-06
22. PL-07
```

Why this order:

```text
first = strongest evidence + direct funnel value
middle = strong architecture fit but needs anchors
later = Project Lens / runtime ideas that should remain candidate until scoped
```

## Plain-Language Result

```text
The first four I found are usable.
The development-area summaries are also useful and more detailed.
The current architecture already covers the direction of all 22 points.
No hard conflict was found.
The mistake would be treating Project Lens / P1 / watch / partial as promotion proof.
```

Best immediate action after user review:

```text
Discuss CI-01 through CI-04 one by one.
If approved, prepare reviewed-pattern writeback in a separate step.
Keep the other 18 as anchor-pass / Project Lens / runtime candidates.
```
