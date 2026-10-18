---
record_kind: sandbox_plan
status: active
created_at: 2026-06-14
scope: source-annotation-scale-product-sandbox
truth_boundary: sandbox_only_not_main_architecture
---

# Source Annotation Scale Sandbox Plan

## Goal

Design and test a product-level workflow for VAKS source annotations at scale.

The sandbox must answer:

```text
When annotations become numerous, how do we keep capture fast, review sane,
project filtering clean, broken anchors visible, and AI context packs precise?
```

## Hard Boundary

- Do not modify main architecture files in this phase.
- Do not edit raw sources, wiki truth layers, templates outside this sandbox, or current repo framework docs.
- Write only inside `outputs/review/source-annotation-scale-sandbox-2026-06-14/`.
- Everything here is candidate / sandbox / diagnostic only.

## Product-Level Requirements

1. Capture must stay low-friction.
2. Every annotation must resolve to a source span or explicitly show anchor risk.
3. The workbench must scale beyond a flat inbox.
4. Project-specific filtering must not pollute source-level truth.
5. AI context export must carry source span + note + boundary, not just a tag.
6. Broken / ambiguous / stale anchors must be triaged visibly.
7. Promotion routes must stay clear:
   - source span worth checking -> source annotation
   - candidate knowledge -> candidate distillation / review candidate
   - project borrow / non-borrow -> Project Overlay
   - evidence/action support -> Evidence Packet / evidence_support
8. The sandbox must include tests and measurable pass/fail criteria.

## Phases

| Phase | Status | Output |
|---|---|---|
| 0. Recover current contract and guardrails | complete | current docs inspected; sandbox boundary set |
| 1. External and local research | complete | findings on Web Annotation, Obsidian/Bases, annotation UX, anchor repair |
| 2. Product model v0 | complete | annotation lifecycle, fields, views, commands, failure modes |
| 3. Sample corpus and generated annotations | complete | mixed article/video/repo sample set |
| 4. Workbench prototype | complete | Bases-like views, project filters, repair queue, context export |
| 5. Validation harness | complete | schema/lifecycle/anchor/context-export checks |
| 6. Iteration rounds | complete | test -> adjust -> retest logs |
| 7. Product recommendation | complete | final sandbox report and adoption criteria |

## Current Design Hypothesis

Source Annotation should become a small product surface with four loops:

```text
Capture -> Triage -> Use -> Repair
```

The likely workbench split:

```text
Inbox
By Project
By Source
Candidate Seeds
Evidence Ready
Anchor Repair
Cold Archive
```

## Initial Metrics

| Metric | Target |
|---|---|
| Capture fields required | <= 8 human-facing fields |
| Workbench default views | 5-7 views, no giant flat table |
| Context export completeness | source_ref + selector + body_note + boundary + target route |
| Broken anchor visibility | every broken/ambiguous/source_changed item appears in repair queue |
| Project filtering | project refs never create project_borrow_scope by themselves |
| Evidence boundary | annotation never appears as support without evidence_packet_ref |

## Errors Encountered

| Time | Error | Resolution |
|---|---|---|
| 2026-06-14 | Subagent/read-only tooling left non-sandbox tool diffs and cache | Reverted tracked diff by patch and removed generated shared/cache files |

## Enterprise Stress Extension

User requested another round:

```text
high-pressure quantitative testing -> find problems -> optimize -> retest ->
enterprise-ready direct landing plan
```

Additional hard boundary:

```text
still sandbox only; do not touch main repo architecture files
```

Enterprise phases:

| Phase | Status | Output |
|---|---|---|
| E1. Quantitative gate design | complete | enterprise readiness metrics and pass/fail thresholds |
| E2. Large corpus fixture generation | complete | 5,000 and 10,000 file-backed source annotation runs |
| E3. Mutation and bad context-pack suite | complete | forbidden-field, support, project, anchor, stale, duplicate failures |
| E4. Performance and contamination tests | complete | runtime, queue accuracy, AI export safety, scale-debt visibility |
| E5. Optimization pass | complete | YAML/parser speed, lazy exact matching, working inbox split, support-on-bad-anchor gate |
| E6. Enterprise readiness report | complete | direct landing recommendation and residual risks |

Enterprise gates:

| Gate | Target |
|---|---|
| Large corpus size | >= 5,000 source annotation files |
| Good corpus schema errors | 0 |
| Mutation catch rate | 100% |
| Bad context-pack catch rate | 100% |
| AI export contamination | 0 bad / stale / archived anchors |
| Support contamination | 0 source_annotation as support |
| Project pollution | 0 project borrow verdict fields in annotations |
| Repair queue accuracy | 100% active bad anchors represented |
| Stale queue accuracy | 100% active stale anchors represented |
| Runtime | 5,000-file validation under 30 seconds on this machine |
| Context export size | <= 250 KB default pack |
| Operator load | default workbench has counts and separated queues, not one flat table |

Enterprise errors and optimizations:

| Time | Error | Resolution |
|---|---|---|
| 2026-06-14 | Archived + bad-anchor fixture conflicted between archive policy and repair lifecycle | Made archived lifecycle highest priority |
| 2026-06-14 | 5,000-file validation first failed runtime gate: 40.652s > 30s | Switched to C YAML loader/dumper when available and avoided unnecessary exact text counts; retest 5.143s |
| 2026-06-14 | 5,000-file inbox had 4,691 rows, too large for human operation | Split working inbox from locator pool; retest inbox 153, locator pool 4,538 |
| 2026-06-14 | 10,000-file stretch found support_checked overriding ambiguous anchor lifecycle | Added anchor repair beats support audit rule and hard validator check |
