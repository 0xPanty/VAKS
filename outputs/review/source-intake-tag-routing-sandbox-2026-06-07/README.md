---
type: sandbox_package
status: candidate_only
created_at: 2026-06-07
scope: source intake metadata, tags, classification, knowledge-point routing, retrieval lanes
truth_boundary: sandbox only; not reviewed knowledge; not architecture decision; not action basis
---

# Source Intake Tag / Routing Sandbox

## Purpose

This sandbox absorbs the Pro research recommendations into a candidate
mainline design for VAKS source intake metadata, tags, classification,
knowledge-point routing, and retrieval filtering.

It does not directly edit the mainline files.

Mainline files to patch later, only after review:

```text
SOURCE_INTAKE.md
templates/source-record.md
templates/video-source.md
templates/candidate-distillation.md
templates/query-run.md
wiki/indexes/knowledge-graph-index.md
00_handoff/
```

Truth layer remains out of scope:

```text
SCHEMA.md
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
wiki/claims
wiki/decisions
wiki/patterns
```

## One Sentence

Use tags for recall, fields for filtering, candidate points for knowledge,
overlays for project borrowing, and reviewed/action gates for authority.

## Candidate Rule

```text
filter by identity / authority first
rank by topic / entity / lexical / vector signals second
ground action-facing support only in raw or reviewed anchors
```

## Package Map

```text
00_PRO_REQUIREMENT_MAP.md
01_MAINLINE_CANDIDATE_DELTA.md
02_FIELD_CONTRACT.md
03_QUERY_PIPELINE_AND_RETRIEVAL_LANES.md
04_SUGGESTED_CONFIRMED_FORBIDDEN.md
05_TOPIC_ENTITY_KP_DESIGN.md
06_RETRIEVAL_MVP_LANE_CLASSIFIER.md
07_TOPIC_REGISTRY_CANDIDATE.md
08_ENTITY_ALIAS_CANDIDATE.md
09_KP_ID_LINT_CONTRACT.md
10_OTHER_ROLE_CLASSIFIER.md
11_VAULT_DISTILLATION_BORROWINGS.md
12_ARTIFACT_REGISTRY_CANDIDATE.md
13_CONTEXT_PACK_BUILDER_V0_CONTRACT.md
14_OBSIDIAN_WORKBENCH_ENTRYPOINTS.md
15_INTAKE_METADATA_PREFILL_OPTIMIZATION.md
16_SOURCE_CARD_VS_CANDIDATE_METADATA_SPLIT.md
17_TOPIC_RETRIEVAL_PACK_MVP.md
18_SOURCE_INTAKE_ROUTING_WORKBENCH_LANDING.md
19_SOURCE_INTAKE_ROUTING_WORKBENCH_HARDENING.md
fixtures/
checks/
workbench/
```

## Current Sandbox Addition

This package now includes a minimal retrieval workbench prototype:

```text
query pattern
-> lane-filtered retrieval MVP
-> topic/context pack candidate
-> explicit excluded/not-default noise list
-> context pack lint
```

It is not an answer generator, not a production builder, and not a mainline
schema change.

## GitHub Scout Addition

The first workbench-focused external scout has been added for:

```text
source-intake-routing
```

It checked 5 high-star, recently active GitHub repositories:

```text
langgenius/dify
infiniflow/ragflow
Mintplex-Labs/anything-llm
run-llama/llama_index
deepset-ai/haystack
```

The scout output stays candidate-only:

```text
raw repo source cards
candidate distillation
VAKS project overlay
sandbox check
```

It does not promote any repo, pattern, decision, or truth-layer object.

## Workbench Landing Addition

The scout has now been wired into a minimal workbench implementation:

```text
fixtures/source-intake-route-map.json
workbench/source-intake-routing.md
checks/source-intake-routing-workbench-pack-research-generated.md
checks/source-intake-routing-workbench-pack-source-inspection-generated.md
checks/source-intake-routing-workbench-pack-action-generated.md
```

The implementation keeps the borrowed ideas small:

```text
route front door
metadata/router/trace display
parser/connector route hints
citation/clickback as drilldown
action_readiness:not_ready until evidence support check
```

It does not add a vector DB, platform clone, Obsidian plugin, new schema, or
truth-layer mutation.

## Workbench Hardening Addition

The first workbench landing has been hardened into v0.1:

```text
natural question
-> query-intent-router
-> workbench mode
-> lane-filtered retrieval
-> lane-internal ranking
-> selector/snippet navigation
-> action anchor_queue only
```

Added pieces:

```text
fixtures/query-intent-router-v0.json
tools/vaks-query-intent-router-v0.ps1
19_SOURCE_INTAKE_ROUTING_WORKBENCH_HARDENING.md
checks/source-intake-routing-workbench-hardening-v0-1-test.md
checks/source-intake-routing-workbench-pack-query-*.md
```

Guard:

```text
selector/snippet = navigation only
selection_priority = navigation priority only
action anchor_queue = possible anchors to open/check, not final support
```

## Evidence Support Reference Distillation Addition

The next step has been researched but not implemented:

```text
20_EVIDENCE_SUPPORT_CHECK_REFERENCE_DISTILLATION.md
```

It distills high-quality papers, repos, and official docs for:

```text
anchor_queue
-> evidence-support-check
-> answer-ready context pack
```

Borrowed direction:

```text
claim/sentence-level support
source selector + warrant
coverage overview
known omissions
failure origin diagnostics
```

Guard:

```text
answer-ready = ready to draft a source-aware sandbox answer
answer-ready != action basis
evidence-support-check != truth layer
metrics / scores / citation markers remain diagnostic only
```

## Evidence Support v0 Landing Addition

The reference distillation has now been landed as a small sandbox prototype:

```text
21_EVIDENCE_SUPPORT_CHECK_V0_LANDING.md
fixtures/evidence-support-check-v0-source-intake.json
tools/vaks-evidence-support-check-v0.ps1
checks/evidence-support-check-v0-source-intake-generated.md
checks/answer-ready-context-pack-v0-source-intake-generated.md
checks/evidence-support-check-v0-test.md
```

Test result:

```text
anchor_queue_total=29
claims_checked=4
supported=4
missing_evidence=0
answer_readiness=ready_for_answer_draft
action_basis_allowed=false
```

## Evidence Support Negative Pressure Test Addition

The v0 checker has now been pressure-tested with deliberately unsupported and
scope-mismatched answer claims:

```text
fixtures/evidence-support-check-v0-negative-source-intake.json
checks/evidence-support-check-v0-negative-generated.md
checks/answer-ready-context-pack-v0-negative-generated.md
checks/evidence-support-check-v0-negative-pressure-test.md
```

The pressure test first exposed a false positive where non-goal / negated text
was treated as support. The tool now skips excluded support context such as:

```text
Supported does not mean
Non-Goals
must not become
forbidden use
```

Final pressure result:

```text
positive fixture: supported=4 missing_evidence=0 ready_for_answer_draft
negative fixture: supported=0 missing_evidence=4 not_ready
action_basis_allowed=false
citation_faithfulness_checked=false
```

## Evidence Support Mixed Pressure Test Addition

The v0 checker has also been tested on a mixed answer candidate:

```text
fixtures/evidence-support-check-v0-mixed-source-intake.json
checks/evidence-support-check-v0-mixed-generated.md
checks/answer-ready-context-pack-v0-mixed-generated.md
checks/evidence-support-check-v0-mixed-pressure-test.md
```

Result:

```text
mixed fixture: supported=2 missing_evidence=2 not_ready
supported claims keep source_refs/selectors
missing claims expose failure_origin
answer_ready_context_pack prints failure_origin per claim
action_basis_allowed=false
```

Practical effect:

```text
the workbench can keep good anchored claims while blocking the whole answer
until unsupported or scope-overclaimed claims are removed, rewritten, or reviewed
```

## Evidence Support Revised Flip Test Addition

The v0 checker has now been tested on a revised answer candidate:

```text
fixtures/evidence-support-check-v0-revised-source-intake.json
checks/evidence-support-check-v0-revised-generated.md
checks/answer-ready-context-pack-v0-revised-generated.md
checks/evidence-support-check-v0-revised-flip-test.md
```

Result:

```text
mixed fixture: supported=2 missing_evidence=2 not_ready
revised fixture: supported=4 missing_evidence=0 ready_for_answer_draft
action_basis_allowed=false
citation_faithfulness_checked=false
```

Practical effect:

```text
the workbench can guide a blocked mixed answer back to draft readiness when the
unsupported or overclaimed parts are removed or rewritten into supported
boundary claims
```

## Evidence Support E2E Repair Loop Addition

The v0 checker has now been tested through the natural-question workbench path:

```text
natural question
-> query-intent-router
-> context pack builder
-> action anchor_queue
-> evidence-support-check
-> mixed blocked
-> revised draft-ready
```

Added files:

```text
checks/source-intake-routing-workbench-pack-query-e2e-action-generated.md
fixtures/evidence-support-check-v0-e2e-mixed-source-intake.json
fixtures/evidence-support-check-v0-e2e-revised-source-intake.json
checks/evidence-support-check-v0-e2e-mixed-generated.md
checks/answer-ready-context-pack-v0-e2e-mixed-generated.md
checks/evidence-support-check-v0-e2e-revised-generated.md
checks/answer-ready-context-pack-v0-e2e-revised-generated.md
checks/evidence-support-check-v0-e2e-repair-loop-test.md
```

Result:

```text
router: selected_mode=action confidence=high
e2e action pack: anchor_queue_total=21
e2e mixed: supported=2 missing_evidence=2 not_ready
e2e revised: supported=4 missing_evidence=0 ready_for_answer_draft
action_basis_allowed=false
citation_faithfulness_checked=false
```

The e2e fixtures intentionally point their first claim at the newly generated
natural-question pack, and the final outputs confirm
`support_channel=context_pack_metadata`.

## Evidence Support Pack Containment Addition

The v0 checker now distinguishes current-pack support from fixture-supplied
external support:

```text
fixtures/evidence-support-check-v0-pack-containment-source-intake.json
checks/evidence-support-check-v0-pack-containment-generated.md
checks/answer-ready-context-pack-v0-pack-containment-generated.md
checks/evidence-support-check-v0-pack-containment-test.md
```

Result:

```text
pack containment: supported=2 weakly_supported=1 missing_evidence=0 not_ready
weak support reason: matched_outside_required_support_channel
action_basis_allowed=false
citation_faithfulness_checked=false
```

Practical effect:

```text
external fixture refs can stay visible as supplemental anchors, but they no
longer silently count as current-pack coverage when a claim requires
pack-contained support
```

## Evidence Support Pack Repair Addition

The pack-containment failure now has a minimal repair-loop test:

```text
checks/source-intake-routing-workbench-pack-query-e2e-action-repaired-generated.md
fixtures/evidence-support-check-v0-pack-repair-source-intake.json
checks/evidence-support-check-v0-pack-repair-generated.md
checks/answer-ready-context-pack-v0-pack-repair-generated.md
checks/evidence-support-check-v0-pack-repair-test.md
```

Result:

```text
containment before: supported=2 weakly_supported=1 missing_evidence=0 not_ready
repair after: supported=3 weakly_supported=0 missing_evidence=0 ready_for_answer_draft
action_basis_allowed=false
citation_faithfulness_checked=false
```

Practical effect:

```text
the workbench can now expose weak pack-contained support, add the missing
anchor into a repaired pack, and rerun to answer-draft readiness without
turning the pack into action basis
```

## Answer Draft Skeleton Addition

The answer-ready pack now has a thin draft-skeleton handoff:

```text
tools/vaks-answer-draft-skeleton-v0.ps1
checks/answer-draft-skeleton-v0-pack-repair-generated.md
checks/answer-draft-skeleton-v0-e2e-mixed-blocked-generated.md
checks/answer-draft-skeleton-v0-test.md
```

Result:

```text
ready input: claims_seen=3 draft_claims_emitted=3 ready_for_human_draft
not-ready input: claims_seen=4 draft_claims_emitted=0 blocked_not_ready
source_refs_policy=claim_evidence_map_only
action_basis_allowed=false
truth_mutation_allowed=false
```

Practical effect:

```text
ready_for_answer_draft can now produce a human-readable answer spine, while
not_ready packs are blocked before any answer claim is emitted
```

## Answer Draft Smoke Addition

The skeleton now has a human-readable smoke draft and lint check:

```text
tools/vaks-answer-draft-smoke-lint-v0.ps1
checks/answer-draft-smoke-v0-pack-repair-generated.md
checks/answer-draft-smoke-v0-e2e-mixed-blocked-generated.md
checks/answer-draft-smoke-v0-pack-repair-lint-generated.md
checks/answer-draft-smoke-v0-e2e-mixed-blocked-lint-generated.md
checks/answer-draft-smoke-v0-test.md
22_ANSWER_DRAFT_SMOKE_V0_OPUS_REVIEW_BRIEF.md
```

Result:

```text
ready smoke lint: pass / 3 tagged draft lines / claim_refs pr1,pr2,pr3
blocked smoke lint: pass / 0 draft lines / 0 claim_refs
empty claim_refs: expected fail / actual fail
paragraph blocked answer: expected fail / actual fail
fenced heading blocked answer: expected fail / actual fail
mismatched ref: expected pass known limitation
omitted claim: expected pass known limitation
source_refs_policy=claim_evidence_map_only
action_basis_allowed=false
truth_mutation_allowed=false
```

Practical effect:

```text
the workbench can now show a readable answer draft while checking that every
answer line has a non-empty existing claim_ref handle, and it refuses to emit
answer text from a not-ready skeleton
```

Trust boundary:

```text
smoke lint assumes skeleton readiness is correct upstream; it checks shape and
reference-handle existence only, not semantic support, citation faithfulness,
coverage, or omissions
```

## Real Local Pressure And Blind Review Addition

The answer-draft smoke chain was also pressure-tested on local sandbox files,
not only on synthetic `pr1/pr2/pr3` fixtures:

```text
checks/real-local-question-pack-smoke-boundary-generated.md
checks/real-local-question-pack-action-basis-generated.md
fixtures/evidence-support-check-v0-real-local-smoke-boundary.json
fixtures/evidence-support-check-v0-real-local-action-basis-negative.json
checks/real-local-answer-draft-smoke-pressure-test.md
23_REAL_LOCAL_PRESSURE_AND_BLIND_REVIEW_PACKET.md
23A_AUTHOR_RECORDED_RESULTS_AFTER_BLIND_RUN.md
24_BLIND_OPUS_REVIEW_ABSORPTION.md
```

Result:

```text
real-local ready sample: 5 checked / 5 supported / ready_for_answer_draft
real-local ready smoke: pass / 5 draft lines / 0 unknown refs
real-local negative sample: 4 checked / 0 supported / 4 missing / not_ready
real-local negative smoke: pass / 0 draft lines emitted from blocked skeleton
```

Blind review status:

```text
first blind review found a procedural leak: expected results were present in
the packet before commands
repair: 23 now contains protocol and commands only
author-recorded results moved to 23A for after-run comparison
blind Opus findings absorbed in 24 as sandbox-only limitations
```

Important correction:

```text
real-local positive support is not independent evidence maturity; it is partly
self-referential author-document support
negative real-local support proves no support fabrication, not robust semantic
overclaim detection
```

## Review Question

Does this sandbox preserve the current Source Intake Control Flow while adding
the Pro recommendations without creating a heavy ontology, authority tags, or a
new truth layer?

Follow-up review question:

```text
Do existing VAKS / Obsidian candidate distillations justify adding a usage-layer
workbench: artifact registry, progressive context pack, query-run receipts, and
topic entry pages?
```

Follow-up UX question:

```text
Can source-intake-routing become an Obsidian "front door" where a user starts
from current rules, then opens raw/candidate/overlay/audit lanes only when the
question needs them?
```
