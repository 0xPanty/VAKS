---
type: recommendation_coverage_map
status: candidate_only
created_at: 2026-06-07
scope: Pro recommendation coverage for source intake metadata and retrieval
truth_boundary: sandbox coverage only; not reviewed knowledge
---

# Pro Requirement Map

## Coverage Summary

```text
requirements_total: 24
requirements_covered_in_sandbox: 24
known_open_questions: 3
mainline_writeback_status: not_started
```

## Requirements

| ID | Pro recommendation | Sandbox landing |
|---|---|---|
| P01 | Do not rely on one tag layer for everything. | `01_MAINLINE_CANDIDATE_DELTA.md`, `02_FIELD_CONTRACT.md` |
| P02 | Separate object/state fields, topics/facets, entity links, curated hubs, and query routing. | `02_FIELD_CONTRACT.md`, `03_QUERY_PIPELINE_AND_RETRIEVAL_LANES.md`, `05_TOPIC_ENTITY_KP_DESIGN.md` |
| P03 | Keep `processing_tier`, `knowledge_status`, `retrieval_policy`, and `promotion_gate` as hard fields. | `01_MAINLINE_CANDIDATE_DELTA.md`, fixtures |
| P04 | Add only limited controlled facets at intake: `topics`, `content_form`, `language`, `version_or_time_scope`. | `02_FIELD_CONTRACT.md`, source/video fixture |
| P05 | Use `entities`, `aliases`, and optional `entity_refs` for semantic anchors. | `02_FIELD_CONTRACT.md`, `05_TOPIC_ENTITY_KP_DESIGN.md`, fixtures |
| P06 | Keep optional open tags as low-authority recall only. | `02_FIELD_CONTRACT.md`, `04_SUGGESTED_CONFIRMED_FORBIDDEN.md` |
| P07 | Do not put project-specific borrowing into generic source-card tags. | `01_MAINLINE_CANDIDATE_DELTA.md`, project overlay fixture |
| P08 | Put project borrowing in overlay / sidecar only. | `01_MAINLINE_CANDIDATE_DELTA.md`, `fixtures/project-overlay-confirmed.md` |
| P09 | Source cards carry findability, filtering, provenance, and governance metadata only. | `02_FIELD_CONTRACT.md`, source/video fixture |
| P10 | Atomic knowledge points belong in candidate notes, not source tags. | `05_TOPIC_ENTITY_KP_DESIGN.md`, `fixtures/candidate-distillation-kp-refs.md` |
| P11 | Candidate points need stable `kp_ref` / bullet-level IDs or note-level refs. | `05_TOPIC_ENTITY_KP_DESIGN.md`, candidate fixture |
| P12 | Reviewed/adopted/action-basis language belongs only in reviewed/action layers. | `04_SUGGESTED_CONFIRMED_FORBIDDEN.md`, lint matrix |
| P13 | Suggested metadata should default to sidecar / UI / review diff, not persistent main note. | `04_SUGGESTED_CONFIRMED_FORBIDDEN.md`, suggestion-sidecar fixture |
| P14 | Auto-suggest only low-risk fields: topics, entities, content form, language, time/version hints, routing hints, query filters. | `04_SUGGESTED_CONFIRMED_FORBIDDEN.md` |
| P15 | Require confirmation for hard boundary fields, project overlay refs, candidate keep/drop, borrow/non-borrow, risk/anti-pattern, reviewed/adopted. | `04_SUGGESTED_CONFIRMED_FORBIDDEN.md` |
| P16 | Forbid authority tags such as reviewed, approved, adopted, use-this, best-practice, truth, safe, action-basis, decision. | `04_SUGGESTED_CONFIRMED_FORBIDDEN.md`, forbidden fixture |
| P17 | Retrieval must filter by authority/status/project boundary before tags/topics/entities/embeddings. | `03_QUERY_PIPELINE_AND_RETRIEVAL_LANES.md`, query fixtures |
| P18 | Query understanding extracts entities, time, source type, project scope, and action-facing state. | `03_QUERY_PIPELINE_AND_RETRIEVAL_LANES.md`, query fixture |
| P19 | Hybrid retrieval and rerank happen only inside the allowed slice or lane. | `03_QUERY_PIPELINE_AND_RETRIEVAL_LANES.md` |
| P20 | Links/entity refs/hub notes can expand context after hard filtering. | `03_QUERY_PIPELINE_AND_RETRIEVAL_LANES.md`, topic-pack fixture |
| P21 | Reviewed, candidate, raw, overlay, and audit evidence should display as separate lanes. | `03_QUERY_PIPELINE_AND_RETRIEVAL_LANES.md`, topic-pack fixture |
| P22 | Facets, retrieval scores, dashboard prominence, feedback clicks, graph centrality, and tag hits are diagnostics only. | `03_QUERY_PIPELINE_AND_RETRIEVAL_LANES.md`, lint matrix |
| P23 | Curated hub / MOC / topic pack should exist only for high-value topics and remain navigation, not truth. | `05_TOPIC_ENTITY_KP_DESIGN.md`, topic-pack fixture |
| P24 | Do not create a heavy ontology now; leave three open questions for empirical iteration. | `05_TOPIC_ENTITY_KP_DESIGN.md` |

## Open Questions Preserved

```text
1. How small should the controlled `topics` set be?
2. Should `entities` remain strings first, or move to alias + canonical refs?
3. What is the minimal stable candidate-point ID format that helps agents
   without making the main schema heavy?
```

## Coverage Verdict

```text
Pro recommendation coverage: complete in sandbox candidate design.
Mainline writeback: not yet applied.
Needs Pro / user review before formal merge.
```
