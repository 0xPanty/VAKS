# AGENTS.md

## Project

This workspace is the project-local entry guide for the Verified Action Knowledge System vault.

Current directory:

```text
C:\Users\Administrator\Documents\资料库
```

This file is intentionally a short router. It should help a new Codex window find the right source-of-truth files without turning the entry point into another long handoff.

## Start Here

Before architecture, review, or implementation work, read:

1. `00_handoff/2026-05-28-verified-action-knowledge-system-v0-2-handoff.md`
2. `README.md`
3. `FUSION_ARCHITECTURE_V0_2_DRAFT.md`
4. `SECOND_BRAIN_MODEL.md`

For schema, implementation, or source-review work, also read:

- `ARCHITECTURE_PRINCIPLES.md`
- `SCHEMA.md`
- `IMPLEMENTATION_BLUEPRINT.md`
- `SOURCE_INTAKE.md`
- `REFERENCE_REVIEW_PROTOCOL.md`
- `MEMORY_TIER.md`
- `DEV_CONTEXT.md`
- `REVIEW_QUEUE.md`
- `FEEDBACK.md`
- `wiki/indexes/knowledge-graph-index.md`
- `wiki/indexes/memory-tier-reference-index.md`
- `templates/architecture-review-window-prompt.md`

If a newer handoff exists, prefer the newest file in `00_handoff/`.

## Project Map

- `00_handoff/`: recovery handoffs and next-window state.
- `raw/articles/`: article source records.
- `raw/videos/`: video source records, transcripts, timestamp notes, and candidate-only video intake cards.
- `raw/repos/`: repository source records.
- `raw/repos/_snapshots/`: source snapshots and downloaded archives.
- `wiki/claims/`: reviewed or review-ready claim notes.
- `wiki/patterns/`: adopted or candidate design patterns.
- `wiki/anti-patterns/`: risks and rejected designs.
- `wiki/concepts/`: durable concept notes.
- `wiki/decisions/`: architecture decisions.
- `wiki/projects/`: focused project/research notes.
- `wiki/summaries/`: source and architecture review summaries.
- `wiki/indexes/`: index and recovery maps.
- `outputs/qa/`: analysis outputs and Q&A records.
- `outputs/review/`: review outputs.
- `outputs/feedback/`: feedback outputs.
- `templates/`: reusable record, review, feedback, and window templates.
- `products/`: future external publishing artifacts.

## Root Documents

- `README.md`: public five-layer story.
- `purpose.md`: vault mission and purpose layer.
- `ARCHITECTURE_PRINCIPLES.md`: architecture principles and boundaries.
- `FUSION_ARCHITECTURE_V0_2_DRAFT.md`: current v0.2 synthesis and Pro-review revision.
- `SECOND_BRAIN_MODEL.md`: second-brain explanation and design-check model, not an implementation module tree.
- `SCHEMA.md`: reviewed knowledge schema and MVP relation rules.
- `IMPLEMENTATION_BLUEPRINT.md`: implementation order and closed-loop path.
- `SOURCE_INTAKE.md`: light / medium / heavy source processing rules.
- `REFERENCE_REVIEW_PROTOCOL.md`: how to review external repositories, papers, and articles.
- `MEMORY_TIER.md`: activation tier rules; activation is not truth.
- `DEV_CONTEXT.md`: temporary project workbench context.
- `REVIEW_QUEUE.md`: candidate points, point collision, review, and promotion.
- `FEEDBACK.md`: Use Ledger and feedback boundaries.

## Project Review Templates

These two templates are for this project's architecture/repository/reference review work. They are not future user-facing note intake templates.

- `templates/architecture-review-window-prompt.md`: use this as the operating prompt when the user sends repositories, papers, articles, or architecture references for framework design. It defines the read-only/default boundaries, full-system lens, and the required comparison questions.
- `templates/library-review.md`: use this as the extraction shape when summarizing a repository, library, framework, or architecture source. It requires source/code anchors, current-branch value, whole-architecture value, risks, adoption judgment, and fusion fit.
- `templates/maintenance-manifest.md`: use this for lint-style maintenance reports. It may surface missing evidence, confidence-cap violations, stale dependencies, missing intent confirmation, missing outcome calibration, or test/benchmark interpretation risks, but it must not auto-repair reviewed knowledge or create truth/mainline readiness.

When reviewing a repo/library/article for this project, follow these templates before proposing writeback. Keep the analysis focused on design extraction and fusion quality. Do not confuse these project-development review templates with future light/medium/heavy intake templates for ordinary user notes.

## Source Intake Templates

- `templates/video-source.md`: use this for Bilibili, YouTube, course, lecture, interview, podcast-with-video, demo, or walkthrough source cards under `raw/videos/`. It records source metadata, transcript method, key-entity confidence, candidate points, and review routing, but it does not create reviewed knowledge.

## Source Set Already Considered

These references have been discussed, reviewed, or partially absorbed. Use the existing source records, summaries, patterns, anti-patterns, and decisions before re-analyzing them from scratch.

- Karpathy LLM Wiki / LLM-maintained wiki workflow.
- `llm-wiki` and `llm-wiki-compiler`.
- `gbrain`.
- OpenKB.
- Obsidian Second Brain / AI-first vault patterns.
- Obsidian AI Orange Book.
- Obsidian Base Hub / Bases-style workbench.
- nano-NotebookLM.
- knowledge-base-server.
- Kepano Obsidian vault.
- PARA vault template.
- Kagantic vault structure.
- Dusk Obsidian vault.
- Obsidian + Claude / Vellum daily synthesis and second-brain articles.
- JARVIS / content-production vault article.
- ECC / AgentShield / Claude Code tool-safety article: discussed as future agent tool-safety inspiration; do not turn it into a core platform before agents can write or execute.
- Jon Doyle / Truth Maintenance System / Reason Maintenance: conceptual ancestor for Point Collision as knowledge calibration; absorb the idea of reasons, contradiction pressure, and review-triggering evidence, not an automatic truth machine.
- Dung / abstract argumentation framework: conceptual reference for Evidence-Aware Review; absorb the support/challenge/standing-check idea, not formal argumentation semantics or automatic debate resolution.
- W3C PROV / provenance model: conceptual reference for lightweight source provenance; absorb source identity, capture/extraction activity, and human/model/tool traceability, not the full ontology, graph stack, or source-node usage ledger.
- VERISCORE / verifiable-claim factuality evaluation: conceptual reference for candidate routing; absorb the distinction between verifiable and unverifiable content, not the metric or evaluator pipeline.
- PaperTrail / claim-evidence provenance interface: conceptual reference for context-pack coverage maps; absorb key point coverage and progressive disclosure, not the full UI or exhaustive omission scan.
- GraphFC / graph-based fact checking: conceptual reference for optional point graph fragments on complex candidate points; absorb entity-relation decomposition as a review aid, not the full pipeline or automatic graph truth.
- ProVe / RAG attribution faithfulness: conceptual references for Evidence Support Check; absorb source-span-to-point/relation support checking and the citation-correctness-vs-faithfulness warning, not automated ProVe, NLI/RTE, support scores, or causal citation faithfulness verification.
- Self-RAG / CRAG / A2RAG: conceptual references for Evidence Sufficiency Gate; absorb "escalate only when evidence is insufficient for the intended action", not automatic retrieval evaluators, web search, agentic retrievers, or correction pipelines.
- HippoRAG / hippocampal indexing inspired RAG: conceptual reference for Association Neighborhood Activation; absorb association retrieval for context activation, not graph traversal, Personalized PageRank, similarity, or association score as support, confidence, truth, or reviewed relation creation.
- GraphRAG / LightRAG: conceptual references for graph retrieval stratification; absorb low-level source/text-unit/claim/entity retrieval, high-level pattern/theme/community retrieval, and relation-neighborhood context activation, not community summary as truth, graph rank as trust, or auto-extracted relation as reviewed relation.
- Graphiti / Zep temporal knowledge graph: conceptual reference for Temporal Applicability Check; absorb validity windows, supersession, and episode/source traceability, not automatic graph construction, automatic invalidation, or graph database runtime as the Markdown source of truth.
- Reflexion / Reflective Memory Management: conceptual references for Feedback Ledger; absorb reflection-as-use-memory, prospective/backward-looking feedback, and cited-evidence retrieval refinement, not weight updates, hidden reinforcement learning, or feedback-driven truth changes.
- MemGPT / virtual context management: conceptual reference for Activation Tier; absorb fast/slow context management and explicit paging intuition, not an agent OS, autonomous memory manager, or truth-tier interpretation.
- RKA / research knowledge assistant: engineering and workflow reference for review queue taxonomy, decision superseding, intent confirmation, verbatim input preservation, maintenance manifests, confidence caps, and decision outcome calibration; absorb these as lazy gates and records, not its runtime, MCP, dashboard, SQLite truth source, or workflow actions as truth changes.

For the full current graph of absorbed patterns, anti-patterns, decisions, source summaries, and index notes, read:

- `wiki/indexes/knowledge-graph-index.md`
- `wiki/indexes/memory-tier-reference-index.md`

## Operating Rules

- Answer in Chinese by default.
- Use files as source of truth. Do not rely on chat memory alone.
- If the user says read-only, analysis only, no edits, no implementation, no commit, or no push, obey that boundary.
- Do not overdesign. Prefer the smallest elegant architecture change that preserves the current spine.
- Do not add a new formal lane structure; automatic compile is parked, and `Karpathy-light / VAKS-strict` is only a plain-language explanation layer.
- Do not treat dashboard, retrieval, metadata, brief, or feedback as reviewed knowledge.
- Do not start automation, scripts, API/MCP, viewer, publishing pipeline, dev context pack, query-run, feedback-event, or scheduled synthesis unless explicitly asked.
- Important architecture conclusions should be written back to the appropriate docs, handoff, and indexes after user confirmation.
- After meaningful file changes, run a sanity check, update handoff if recovery state changed, and commit when the user asks.

## Architecture Reminder

Public story:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

Internal loop:

```text
Capture / Provenance
-> Candidate Comprehension
-> Knowledge Calibration / Point Collision
-> Review / Consolidation
-> Association / Reviewed Relations
-> Activation / Dev Context
-> Context Pack
-> Decision / Action
-> Use Ledger / Feedback
-> Cooling / Reactivation / Review Due
```

Boundaries:

- Feedback improves activation, usefulness, and scope fit; it does not directly change truth confidence.
- Strict checks are lazy gates: ordinary capture stays light, ordinary query stays simple, promotion gets strict, and action basis gets auditable.
- Proactive synthesis is candidate-only.
- Risk / Inhibition is cross-cutting.
- Knowledge calibration output is review input, not truth.
- Evidence-aware review checks support, challenge, scope limits, and risk before a judgment is treated as standing; the full panel is a lazy gate for promotion, decisions, action basis, strong relations, explicit contradictions, or stale / contested claims.
- Source provenance uses a lightweight PROV-inspired vocabulary. Source records stay light; review, promotion, and context-pack use are recorded in their own layers.
- Verifiability routing happens before review: candidate points are atomic review units, not all claims; only verifiable claims receive truth confidence.
- Complex candidate points may use optional `point_graph_fragment`; extracted triplets are review aids, not truth or reviewed relations.
- Context packs are coverage-aware, but full `coverage_map` detail is only required for key judgments used in an answer or action basis; ordinary queries should not become full audit reports.
- The second-brain model is an explanation and design-check layer, not the engineering module structure.
- Evidence Support Check lives on evidence items, not Source nodes: URL-only citations are provenance, background citations cannot count as support, and evidence must support the specific point or relation.
- Evidence Packet is the v0.3 lightweight review input for important promotion or action use: point, source anchor, evidence item, warrant, scope/risk, challenge kind, omission check when needed, and minimal revision. It is not a truth layer, formal logic engine, or automatic truth engine.
- Evidence Sufficiency Gate appears only for promotion, decision, strong reviewed relation, context pack / action basis, risk_sensitive_answer, or an explicit "is this enough" question; it runs after a draft evidence/context envelope is assembled and before action-ready finalization. Ordinary capture and ordinary query stay light.
- Approval integrity is process evidence, not evidence support: LLM-assisted labels, prefilled review notes, high agreement, majority vote, or a human "looks good" confirmation can create review pressure, but not evidence review, truth confidence, reviewed relations, or automatic promotion.
- Known omission checks are review input, not action readiness: important sufficiency reviews should expose known support, known counterevidence, known gaps, and known conflicts without creating a global evidence pool, coverage score, automatic retrieve_more action, truth confidence, or ready action basis.
- Test, benchmark, fixture, and LLM-judge results are maintenance lint / diagnostic input, not truth confidence, benchmark authority, reviewer status, runtime readiness, mainline readiness, or a new eval/test template family.
- Association Neighborhood Activation is retrieval / activation, not truth: it may light up support, challenge, risk, decisions, scope notes, and source anchors for a query, but only reviewed evidence and reviewed relations can support action.
- Graph retrieval stratification is a context-pack preparation aid: low-level retrieval finds source/text-unit/claim/entity anchors, high-level retrieval finds pattern/theme/community briefings, and relation-neighborhood traversal finds nearby reviewed context. Community reports are not truth, graph rank is not trust, and auto-extracted relations are not reviewed relations.
- Temporal Applicability Check hardens scope fit: truth is source-backed, while applicability is time-, version-, project-, environment-, and scope-bound. A standing claim may still be out of scope, stale, or superseded for the current action.
- Feedback Ledger follows Reflexion/RMM-style reflection without truth mutation: positive feedback is weak, negative feedback creates review pressure, and explicit correction creates review_due.
- Review queue item taxonomy labels why attention is needed: low_confidence_claim, contradiction, missing_evidence, synthesis_needed, or decision_superseded. Decision superseding preserves the old decision, links the replacement, and marks affected downstream content review_due.
- RKA-inspired operational gates are lazy: intent confirmation / backbrief, verbatim user input, maintenance manifest, confidence cap without full text, and decision outcome calibration apply to significant actions, promotion, review, or action basis; they do not burden ordinary capture or ordinary query.
- Agent memory quarantine: future agent / MCP memory writes may create candidate or feedback-event records, but cannot directly write reviewed truth, change confidence, create reviewed relations, or promote knowledge.
- Activation Tier is the public name for hot / warm / cold. The vault has activation tiers, not truth tiers; hot means read early, not believe more.
