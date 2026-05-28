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

When reviewing a repo/library/article for this project, follow these templates before proposing writeback. Keep the analysis focused on design extraction and fusion quality. Do not confuse these project-development review templates with future light/medium/heavy intake templates for ordinary user notes.

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

For the full current graph of absorbed patterns, anti-patterns, decisions, source summaries, and index notes, read:

- `wiki/indexes/knowledge-graph-index.md`
- `wiki/indexes/memory-tier-reference-index.md`

## Operating Rules

- Answer in Chinese by default.
- Use files as source of truth. Do not rely on chat memory alone.
- If the user says read-only, analysis only, no edits, no implementation, no commit, or no push, obey that boundary.
- Do not overdesign. Prefer the smallest elegant architecture change that preserves the current spine.
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
-> Review / Consolidation
-> Association / Point Collision
-> Activation / Dev Context
-> Context Pack
-> Decision / Action
-> Use Ledger / Feedback
-> Cooling / Reactivation / Review Due
```

Boundaries:

- Feedback improves activation, usefulness, and scope fit; it does not directly change truth confidence.
- Proactive synthesis is candidate-only.
- Risk / Inhibition is cross-cutting.
- The second-brain model is an explanation and design-check layer, not the engineering module structure.
