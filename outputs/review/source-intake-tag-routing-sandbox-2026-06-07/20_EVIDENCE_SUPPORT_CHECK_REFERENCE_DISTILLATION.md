---
record_kind: sandbox_reference_distillation_candidate
status: candidate_only
created_at: 2026-06-07
topic_id: source-intake-routing
scope: anchor_queue -> evidence-support-check -> answer-ready context pack
truth_boundary: sandbox research/design only; not reviewed knowledge; not architecture decision; not action basis
action_basis_allowed: false
truth_mutation_allowed: false
allowed_use:
  - sandbox_review
  - workbench_design
  - evidence_support_check_design
  - pro_review_packet
forbidden_use:
  - truth
  - reviewed_relation
  - action_basis
  - agent_execution
  - production_rag_evaluator
  - automatic_promotion
---

# Evidence Support Check Reference Distillation

## Plain Summary

Current workbench v0.1 stops at:

```text
question -> intent mode -> lane-filtered pack -> selector/snippet navigation
-> action anchor_queue only
```

The next sandbox step should not be an agent, executor, production RAG, or truth
checker. It should be a small review surface that opens the queued anchors and
asks:

```text
For each answer claim, which exact source anchor supports it, challenges it,
or leaves it missing?
```

In plain words:

```text
anchor_queue = things to open
evidence-support-check = claim-to-anchor checking
answer-ready context pack = a pack whose claims have visible support status
```

Even an answer-ready pack remains a context/action-prep artifact. It is not
reviewed knowledge, not truth confidence, and not final action basis unless a
later VAKS action-facing gate explicitly accepts it.

## Local Starting Point

Authoritative current sandbox files:

```text
README.md
MANIFEST.md
13_CONTEXT_PACK_BUILDER_V0_CONTRACT.md
18_SOURCE_INTAKE_ROUTING_WORKBENCH_LANDING.md
19_SOURCE_INTAKE_ROUTING_WORKBENCH_HARDENING.md
workbench/source-intake-routing.md
checks/source-intake-routing-workbench-hardening-v0-1-test.md
```

Current hard boundary:

```yaml
final_support.state: none
anchor_queue.note: navigation_queue_only_not_support
action_readiness.state: not_ready
required_next_step: evidence support check
```

## Reference Set

This pass uses primary papers, official repositories, and official docs. It
also checks existing VAKS source cards / candidate distillations where present.

| id | source | type | why high quality |
|---|---|---|---|
| R1 | ALCE: https://arxiv.org/abs/2305.14627 and https://github.com/princeton-nlp/ALCE | EMNLP paper + repo | benchmark and code for citation evaluation |
| R2 | Correctness is not Faithfulness in RAG Attributions: https://arxiv.org/abs/2412.18004 | paper | separates citation correctness from citation faithfulness |
| R3 | LongCite: https://arxiv.org/abs/2409.02897 and https://github.com/THUDM/LongCite | paper + repo | fine-grained sentence-level citations in long-context QA |
| R4 | RAGAS: https://arxiv.org/abs/2309.15217 and https://docs.ragas.io/en/stable/concepts/metrics/available_metrics/ | paper + official docs | reference-free RAG evaluation metrics |
| R5 | ARES: https://arxiv.org/abs/2311.09476 | paper | evaluates context relevance, answer faithfulness, answer relevance |
| R6 | RAGChecker: https://arxiv.org/abs/2408.08067 and https://github.com/amazon-science/RAGChecker | paper + repo | claim-level, retrieval/generation diagnostic framework |
| R7 | Summary of a Haystack / SummHay: https://arxiv.org/abs/2407.01370 | paper | evaluates coverage and citation jointly in long-context RAG |
| R8 | Google Check grounding with RAG: https://docs.cloud.google.com/generative-ai-app-builder/docs/check-grounding | official docs | claim-level grounding API shape and support outputs |
| R9 | PaperTrail: https://arxiv.org/abs/2602.21045 | paper | claim-evidence provenance interface with omissions |
| R10 | TruLens RAG Triad: https://www.trulens.org/getting_started/core_concepts/rag_triad/ | official docs | context relevance / groundedness / answer relevance split |

## Distillation By Source

### R1. ALCE

Solves:

```text
Citation generation needs evaluation beyond answer text quality. ALCE separates
fluency, correctness, and citation quality, and requires systems to retrieve
supporting evidence and generate cited answers.
```

VAKS can borrow:

```text
citation_quality separate from answer_correctness
supporting_evidence required before a citation is meaningful
per-answer citation coverage as a visible check item
```

VAKS cannot borrow:

```text
ALCE metric scores as truth confidence
benchmark pass/fail as action readiness
the dataset/evaluator as mandatory VAKS infrastructure
```

Sandbox landing:

```yaml
answer_ready_check:
  answer_quality: not_scored
  citation_quality: checked_per_claim
  support_coverage:
    state: supported | weak | missing | challenged | out_of_scope
  warning: citation_quality_is_not_truth_confidence
```

### R2. Correctness Is Not Faithfulness In RAG Attributions

Solves:

```text
A cited document can support a statement, but the model may not have genuinely
used that citation when producing the answer. Citation correctness and citation
faithfulness are different.
```

VAKS can borrow:

```text
separate source-support checking from causal citation-faithfulness claims
make the MVP honest: it checks support/correctness, not model reliance
mark post-hoc citation risk explicitly
```

VAKS cannot borrow:

```text
full causal faithfulness verification
model-internal reliance tracking
any claim that VAKS proves the answer was generated from the cited source
```

Sandbox landing:

```yaml
evidence_support_check:
  support_kind: source_span_support
  citation_correctness_checked: true | false
  citation_faithfulness_checked: false
  faithfulness_scope_note: "MVP does not verify causal model reliance."
```

### R3. LongCite

Solves:

```text
Long-context answers need fine-grained citations. Document-level references are
too coarse for readers to verify specific answer sentences.
```

VAKS can borrow:

```text
sentence/claim-level citation binding
answer sentence -> source selector mapping
shorter, precise evidence anchors instead of whole-file links
```

VAKS cannot borrow:

```text
LongCite training, LongCite-45k, or fine-tuned citation models
generated citation markers as sufficient evidence support
```

Sandbox landing:

```yaml
claims:
  - claim_id: c1
    claim_text:
    claim_selector: answer.line:N
    supporting_anchors:
      - source_ref:
        selector_or_offset:
        snippet:
        support_status:
```

### R4. RAGAS

Solves:

```text
RAG evaluation needs separate lenses for retrieval/context and generation. RAGAS
names metrics such as faithfulness, context precision, context recall, and
response relevancy.
```

VAKS can borrow:

```text
diagnostic vocabulary for where failure happened
context precision/recall intuition for whether anchor_queue is noisy or missing
faithfulness as a warning label, not as an automatic authority label
```

VAKS cannot borrow:

```text
LLM judge scores as truth
single-number quality thresholds for action basis
reference-free evaluation as replacement for source-span inspection
```

Sandbox landing:

```yaml
diagnostics:
  retrieval_context:
    possible_noise: true | false
    possible_missing_context: true | false
  generation:
    possible_unsupported_claims: true | false
  metrics_policy: diagnostic_only_not_truth
```

### R5. ARES

Solves:

```text
ARES evaluates RAG along context relevance, answer faithfulness, and answer
relevance, using lightweight LM judges plus limited human annotation.
```

VAKS can borrow:

```text
three-axis review shape: context relevance, answer support, answer usefulness
small human-check calibration idea for future review trials
component-level separation instead of one final score
```

VAKS cannot borrow:

```text
finetuned judges
prediction-powered inference as VAKS gate
automated evaluator authority or promotion authority
```

Sandbox landing:

```yaml
review_axes:
  context_relevance: unchecked | pass | concern
  answer_support: unchecked | pass | concern
  answer_relevance: unchecked | pass | concern
  axis_status_is_review_input_not_truth: true
```

### R6. RAGChecker

Solves:

```text
RAGChecker diagnoses RAG at fine granularity, including retrieval and generation
modules, and uses claim-level entailment operations.
```

VAKS can borrow:

```text
claim-level unit of checking
failure attribution: retrieval gap vs generation unsupported vs mixed issue
diagnostic split between retriever-side and answer-side problems
```

VAKS cannot borrow:

```text
RAGChecker as a required dependency
benchmark dataset as VAKS quality bar
claim-level entailment score as final support
```

Sandbox landing:

```yaml
support_failure_origin:
  - retrieval_gap
  - anchor_too_coarse
  - generation_unsupported
  - source_conflict
  - scope_or_time_mismatch
  - not_verifiable
```

### R7. Summary Of A Haystack / SummHay

Solves:

```text
Long-context RAG answers can cite sources while still missing important insights.
SummHay evaluates coverage and citation together.
```

VAKS can borrow:

```text
answer-ready means coverage-aware, not just citation-present
known missing evidence / known omission fields in the pack
joint view: supported claims plus uncovered important points
```

VAKS cannot borrow:

```text
synthetic haystack benchmark as VAKS acceptance gate
coverage percentage as truth confidence
require exhaustive omission scans for ordinary questions
```

Sandbox landing:

```yaml
coverage_overview:
  supported_claims:
  weak_or_partial_claims:
  missing_evidence:
  known_omissions:
  challenged_or_conflicting:
  coverage_status_is_audit_surface_not_truth: true
```

### R8. Google Check Grounding With RAG

Solves:

```text
Given an answer candidate and facts, the API checks grounding, returns support
score, claim-level citations, cited chunks, and whether a claim requires
grounding.
```

VAKS can borrow:

```text
answer_candidate + facts input shape
claim-level support records
grounding_check_required for non-factual connective text
small fact chunks with metadata instead of one giant blob
```

VAKS cannot borrow:

```text
Google API dependency
support score threshold as action readiness
automatic filtering as truth or review promotion
```

Sandbox landing:

```yaml
evidence_support_check_input:
  answer_candidate_ref:
  facts:
    - source_ref:
      selector_or_offset:
      text:
      metadata:
claims:
  - claim_text:
    grounding_check_required: true | false
    support_status: supported | unsupported | partial | not_checked
```

### R9. PaperTrail

Solves:

```text
Source citations are too coarse for scholarly verification. PaperTrail maps
answer claims to source evidence and exposes unsupported claims and omissions.
```

VAKS can borrow:

```text
claim-evidence map as reader-facing review surface
unsupported and omitted information as first-class visibility
progressive disclosure: overview first, detail only for key claims
```

VAKS cannot borrow:

```text
full UI
full scholarly editing workflow
exhaustive source-document decomposition for ordinary queries
coverage status mutating truth confidence
```

Sandbox landing:

```yaml
answer_ready_context_pack:
  coverage_overview:
  claim_evidence_map:
  unsupported_claims:
  known_omissions:
  ui_policy: markdown_first_progressive_disclosure
```

### R10. TruLens RAG Triad

Solves:

```text
TruLens splits RAG quality into context relevance, groundedness, and answer
relevance.
```

VAKS can borrow:

```text
simple operator checklist
separate "did we retrieve the right things" from "did the answer stay grounded"
separate "grounded" from "useful answer"
```

VAKS cannot borrow:

```text
the phrase "hallucination free" as a VAKS guarantee
evaluator output as reviewed truth
runtime observability stack
```

Sandbox landing:

```yaml
operator_checklist:
  context_relevance_checked:
  groundedness_checked:
  answer_relevance_checked:
  checklist_is_review_aid_not_authority: true
```

## Minimal Sandbox Design

### Step 1. Anchor Queue Input

Start from current action pack output:

```yaml
anchor_queue:
  total:
  items:
    - item_id:
      action_role: anchor_queue_rule_or_template | anchor_queue_reviewed_or_review_ready | anchor_queue_raw_provenance
      source_ref:
      selector_or_offset:
      snippet:
      snippet_status: navigation_snippet_not_evidence
      selection_priority:
      selection_reason:
```

Still true:

```text
An anchor can be opened for checking.
An anchor is not support yet.
```

### Step 2. Evidence Support Check

Add a new sandbox artifact type:

```yaml
record_kind: evidence_support_check_candidate
status: candidate_only
truth_boundary: support_check_review_input_not_truth
action_basis_allowed: false
query_ref:
answer_candidate_ref:
anchor_queue_ref:
claim_unit: sentence_or_atomic_claim
claims:
  - claim_id:
    claim_text:
    grounding_check_required: true | false
    support_status: supported | weakly_supported | unsupported | challenged | out_of_scope | not_verifiable | not_checked
    support_kind: source_span_support
    citation_correctness_checked: true | false
    citation_faithfulness_checked: false
    supporting_anchors:
      - source_ref:
        selector_or_offset:
        snippet:
        warrant:
    challenge_anchors: []
    missing_or_omission_note:
    failure_origin:
      - retrieval_gap
      - anchor_too_coarse
      - generation_unsupported
      - source_conflict
      - scope_or_time_mismatch
      - not_verifiable
coverage_overview:
  supported:
  weakly_supported:
  unsupported:
  challenged:
  missing_evidence:
  out_of_scope:
  not_verifiable:
  known_omissions: []
answer_readiness:
  state: ready_for_answer_draft | not_ready | risky | needs_review
  reason:
warnings:
  - citation_faithfulness_not_checked
  - scores_are_diagnostic_only
```

### Step 3. Answer-Ready Context Pack

Only after Step 2 exists, create a context pack variant:

```yaml
record_kind: answer_ready_context_pack_candidate
status: candidate_only
truth_boundary: answer_preparation_not_truth
action_basis_allowed: false
source_pack_ref:
evidence_support_check_ref:
final_support:
  state: checked
  scope: answer_draft_only
  not_action_basis: true
claim_evidence_map:
  - claim_id:
    answer_sentence:
    support_status:
    source_refs:
    selectors:
    warrant:
coverage_overview:
  supported:
  weakly_supported:
  unsupported:
  challenged:
  missing_evidence:
  known_omissions:
answer_readiness:
  state: ready_for_answer_draft | not_ready | risky | needs_review
  required_next_step:
```

Important wording:

```text
answer-ready = enough to draft a source-aware answer in this sandbox.
answer-ready != action basis.
answer-ready != reviewed knowledge.
answer-ready != production guarantee.
```

## Design Rules To Carry Forward

1. Use claim/sentence as the checked unit; keep whole-file citations as
   navigation only.
2. Treat support as `source_span_support`, not causal citation faithfulness.
3. Preserve `citation_faithfulness_checked: false` until VAKS has a real causal
   attribution method, which is out of scope now.
4. Keep evaluator metrics, support scores, retrieval ranks, and citation markers
   diagnostic only.
5. Track coverage and known omissions; do not require exhaustive omission scans
   for ordinary queries.
6. Split failure origin so retrieval misses, coarse anchors, unsupported
   generation, conflicts, and scope/time mismatches are not collapsed into one
   "bad answer" label.
7. Keep this Markdown-first and sandbox-local. No vector DB, no plugin, no API
   dependency, no agent execution layer.

## Proposed Next Sandbox Artifacts

If this design is accepted, the next files should be:

```text
21_EVIDENCE_SUPPORT_CHECK_V0_CONTRACT.md
fixtures/evidence-support-check-v0-source-intake.md
checks/evidence-support-check-v0-manual-trial.md
checks/answer-ready-context-pack-v0-manual-trial.md
```

Do not create tools yet. First prove the shape manually on one existing action
pack:

```text
checks/source-intake-routing-workbench-pack-query-action-generated.md
```

## Non-Goals

This pass must not become:

```text
agent action
execution layer
production RAG
automatic evaluator
new truth layer
schema/mainline change
Obsidian plugin
full PaperTrail UI
LongCite training
RAGAS/ARES/RAGChecker dependency
Google grounding API dependency
```

## Verdict

The best next move is a manual, Markdown-first evidence-support-check sandbox
trial.

It should transform:

```text
anchor_queue item
```

into:

```text
claim -> source selector -> warrant -> support status -> coverage overview
```

That is the smallest useful bridge from current retrieval workbench to an
answer-ready context pack, while preserving VAKS's core boundary:

```text
retrieval and citation help review;
they do not create truth or action basis.
```
