# Project Tag / Priority Crosswalk

## Scope

This sandbox note answers the follow-up concern:

```text
Did the promotion pilot account for P1/P2-style borrowing priority and project
tags?
```

Short answer:

```text
The first promotion pilot looked mainly at evidence readiness.
It did not systematically list project tags / P-level borrowing signals.
This crosswalk adds that missing view.
```

This is not a new schema, lane, or vocabulary. It maps existing fields already
present in candidate files:

- `tags`
- `related_projects`
- `adoption_status`
- `source_family_ids`
- `project_fit_refs`
- Project Lens `stance`
- `routing_hint`
- `possible_project_refs`
- `reference_layer_tag`
- `borrow_order` with explicit `P1/P2/P3`

## Important Distinction

Project priority is not evidence sufficiency.

```text
P1 / adopt / partial = worth attention for this project
supported / sufficient = may support promotion
```

A P1 candidate can still be `not_ready` if the source anchor is only metadata,
abstract, transcript summary, candidate-bank routing, or project lens sidecar.

## Crosswalk

| ID | Candidate | Existing project tag / priority signal | What it means for VAKS | Does it change promotion judgment? |
|---|---|---|---|---|
| CI-01 | Self-contained review candidate record | `tags: verified-knowledge-system`; `adoption_status: adopt-now`; `tags: pattern/review`, `pattern/candidate` | Highest project fit among implementation candidates. This is directly about VAKS candidate review integrity. | Yes for ordering: keep in first promotion batch. Evidence sufficiency still comes from source/code anchors, not the tag. |
| CI-02 | Review-gated compile queue | `related_projects: verified-knowledge-system`; `adoption_status: adopt-soon`; `tags: pattern/review`, `pattern/llm-ingest` | Direct VAKS spine item: generated material waits for review before formal wiki writeback. | Yes for ordering: keep in first promotion batch. |
| CI-03 | Source hash registry and idempotent ingest | `related_projects: verified-knowledge-system`; `adoption_status: adopt`; `tags: pattern/ingest`, `source-state`, `idempotency` | Already a strong ingest hygiene fit. Useful for source lifecycle, duplicate prevention, and replay safety. | Yes for ordering: can be accepted as implementation pattern if scoped to source hygiene, not truth. |
| CI-04 | Decision outcome precondition before calibration | RKA review tags: `review-queue`, `decision-superseding`, `calibration`, `source-code-anchor`; index says RKA operational guardrails are absorbed for VAKS | Project signal is architectural absorption rather than a frontmatter project tag. The idea fits Use Ledger / decision calibration. | Yes for ordering: keep in first promotion batch as a narrow pattern. |
| CI-05 | Scope dashboard live context surface | `related_projects: verified-action-knowledge-system`; `adoption_status: adapt`; `tags: dev-context`, `dashboard`, `memory-tier`, `workbench` | Useful project workbench surface, but only as context selection / dev context, not truth. | No immediate promotion. Project fit is real, but evidence remains weak and single-source. |
| CI-06 | Context pack evidence envelope | `related_projects: verified-knowledge-system`, `misa-hermes`; `adoption_status: adopt-soon`; `tags: pattern/context-pack`, `pattern/agent-api` | Strong project/runtime fit for agent read boundaries and evidence packaging. | It raises priority, but this pilot did not select it only to avoid overloading one source family. It remains close. |
| CI-07 | Agent context pack budget guardrails | `adoption_status: adopt-soon`; `tags: pattern/context-pack`, `pattern/agent`, `pattern/budget` | Strong agent/context-pack implementation fit. | It raises priority for a future anchor pass; not enough by itself for promotion. |
| CI-08 | Claim-level provenance source ranges | `related_projects: verified-knowledge-system`; `adoption_status: adopt-soon`; `tags: pattern/provenance`, `pattern/evidence` | Core evidence discipline for VAKS. | It raises priority. Still needs targeted line/linter anchors before promotion if written as implementation pattern. |
| CI-09 | Source adapter ingest contract | `tags: verified-knowledge-system`, `pattern/ingest`, `pattern/source-adapter`; `adoption_status: adopt-soon` | Strong source-intake fit, especially for multiple source types and video/source card expansion. | It raises priority for anchor pass; do not freeze heavy adapter fields too early. |
| CI-10 | Static wiki health lint before auto rewrite | `related_projects: verified-knowledge-system`; `adoption_status: adopt-soon`; `tags: pattern/lint`, `pattern/health-check` | Strong boundary fit: visible diagnostics before repair, no background rewrite. | It raises priority for later promotion, but local lint scope/code anchors still need review. |
| CI-11 | Retrieval is activation, not truth | `source_family_ids: sf-rag-engineering`, `sf-memory-retrieval`, `sf-graph-ontology`; `project_fit_refs: VAKS`; Project Lens `stance: partial`; ledger says VAKS already adapts this boundary | Very high project relevance. It is already a main architecture boundary. | It changes wording: this is project-important but not necessarily a promotion target. Keep as boundary/pattern only if user wants a concise reviewed note. |
| CI-12 | Search to analysis before answer | `source_family_ids: sf-rag-engineering`; `project_fit_refs: VAKS`; Project Lens `stance: watch`; ledger says useful for high-impact answers only | Relevant to answer preparation and evidence envelopes, but scoped to high-impact / action-adjacent answers. | It should stay candidate/watch. Project tag increases review priority, not promotion readiness. |
| CI-13 | Source structure first for RAG | `source_family_ids: sf-rag-engineering`, `sf-obsidian-workflow`, `sf-graph-ontology`; `project_fit_refs: VAKS`; Project Lens `stance: partial`; ledger maps it to `SOURCE_INTAKE.md` | Strong source-intake / context-pack design pressure. | It should be considered before CI-12 if doing a RAG/source-intake anchor pass, but not promoted from candidate-bank summary alone. |
| CI-14 | Verified vault API for agent brain | `related_projects: 资料库`, `AI短剧`; `adoption_status: candidate`; `tags: pattern/knowledge-api`, `pattern/agent-context`, `pattern/gbrain` | Relevant runtime direction for agent access, especially read-only/context-pack API. | No immediate promotion as decision. Project fit is medium-high, but architecture says API/MCP remains parked/runtime until boundaries are stable. |
| CI-15 | PKM -> second brain -> personal AI companion | Explicit `possible_project_refs: verified-action-knowledge-system`; `routing_hint: second-brain`, `personal-ai-companion`, `activation-tier`, `context-pack-preparation`, `proactive-ai-boundary`, `privacy-autonomy-risk`, `ai-knowledge-graph`; `reference_layer_tag: ref/pkm-to-personal-ai-companion`; `borrow_order: P1/P1/P1/P2/P3` | This has the clearest P-level borrowing signal. P1 items are framing and guardrail priorities for VAKS: bounded companion story, active context suggestion, privacy/autonomy guardrail. | It changes review priority, not promotion result. Keep as candidate/framing until full-text or stronger independent anchors are available. |

## Revised Human Recommendation

If sorting by project priority plus evidence readiness:

```text
First promotion batch:
CI-01, CI-02, CI-03, CI-04
```

If sorting by project priority but still needing an anchor pass:

```text
Next anchor pass:
CI-06, CI-08, CI-10, CI-09, CI-07
```

If sorting by VAKS Project Lens value but not promotion-ready:

```text
Keep candidate / Project Lens:
CI-11, CI-13, CI-12, CI-05, CI-15
```

If sorting by future runtime direction:

```text
Park as runtime / decision candidate:
CI-14
```

## What This Corrects

The earlier pilot answer was right on evidence sufficiency, but incomplete on
project routing.

Corrected interpretation:

```text
CI-15 is not low-value.
It is high project-value / P1 framing, but low promotion-readiness.

CI-11 and CI-13 are not weak project-wise.
They are strong Project Lens items, but candidate-bank/project-lens support is
not enough for reviewed promotion.

CI-01 through CI-04 remain best first adoption targets because they have both
project fit and inspected anchors.
```
