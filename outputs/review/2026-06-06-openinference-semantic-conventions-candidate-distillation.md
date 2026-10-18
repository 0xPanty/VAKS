---
type: repo_candidate_distillation
status: candidate_only
record_kind: candidate_distillation
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: confirmed
review_pressure: none
retrieval_policy: orientation_only
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
created_at: 2026-06-06
source_record: raw/repos/2026-06-06-openinference-semantic-conventions-source.md
source_url: https://github.com/Arize-ai/openinference/blob/main/spec/semantic_conventions.md
raw_snapshot: raw/repos/2026-06-06-openinference-semantic-conventions-source/semantic_conventions.md
checked_commit: ece68f51f91c7ad26a33cb8417e87ea3d3c2a046
raw_sha256: 7DC950B0C3B37E2C3EED31FDA02209E8339C2FEE3D29E4F13E0A7B8AB6079A79
truth_boundary: candidate distillation only; not reviewed knowledge; not architecture decision; not action basis
review_priority: medium
projects:
  - verified-action-knowledge-system
tags:
  - openinference
  - semantic-conventions
  - tracing
  - ai-observability
  - agent-runtime-receipts
  - retrieval-diagnostics
  - tool-call-audit
  - activation-not-truth
routing_labels:
  source_kind: repository_spec_file
  processing_lane: medium_candidate_distillation
  truth_lane: candidate_only
  project_overlay_route: confirmed_sidecar_exists
  candidate_pattern_bank: no_new_entry
  v0_2_13_trigger: no
candidate_point_labels:
  - operation_trace_taxonomy_for_ai_systems
  - span_kind_required_for_trace_assembly
  - retrieval_document_attributes_are_provenance_not_support
  - reranker_and_document_scores_are_activation_signals
  - prompt_template_versioning_as_run_receipt
  - token_and_cost_fields_as_operational_accounting
  - tool_call_traces_need_access_policy_boundary
  - evaluator_and_guardrail_spans_are_diagnostics_not_review
  - session_user_metadata_tags_need_privacy_scope
  - flattened_attributes_enable_interoperable_trace_export
related_project_overlay:
  - outputs/review/project_overlays/VAKS/VAKS-openinference-semantic-conventions-2026-06-06.md
reviewer:
review_result:
---

# OpenInference Semantic Conventions Candidate Distillation

## Boundary

This is a candidate distillation of the OpenInference `semantic_conventions.md`
specification snapshot.

It does not adopt OpenInference, change VAKS schema, create a tracing runtime,
add OpenTelemetry requirements, or turn trace attributes into reviewed
knowledge.

## Plain-Language Takeaway

This source is much stronger than the recent X articles because it is a primary
technical spec, not a practitioner story.

The useful part is:

```text
AI systems need a stable vocabulary for recording what happened:
LLM call, retriever call, reranker call, tool call, agent block,
guardrail, evaluator, prompt rendering, input/output, prompt version,
retrieved documents, token/cost, session, user, tags, and metadata.
```

For VAKS, this belongs in the operational receipt / observability lane:

```text
good for recording runs
good for debugging retrieval
good for auditing tool calls
good for cost/session ledgers
bad as truth support
bad as automatic review
bad as action readiness
```

## Candidate Points

### 1. operation_trace_taxonomy_for_ai_systems

Candidate point:

```text
AI application work can be traced with operation-level span kinds such as LLM,
EMBEDDING, CHAIN, RETRIEVER, RERANKER, TOOL, AGENT, GUARDRAIL, EVALUATOR, and
PROMPT.
```

Source anchor:

```text
semantic_conventions.md:6-20
```

VAKS fit:

```text
Useful as a vocabulary for future query-run receipts, context-pack generation
receipts, source-intake automation receipts, and agent session capture.
```

Boundary:

```text
These are runtime operation types. They are not VAKS reviewed knowledge types.
```

### 2. span_kind_required_for_trace_assembly

Candidate point:

```text
OpenInference requires `openinference.span.kind` on all OpenInference spans so
the tracing backend can assemble the trace.
```

Source anchor:

```text
semantic_conventions.md:8
semantic_conventions.md:94
```

VAKS fit:

```text
Any future VAKS run receipt should label what kind of operation produced each
event, otherwise later review cannot tell whether a record came from retrieval,
LLM generation, tool execution, evaluator output, or prompt rendering.
```

Boundary:

```text
Span assembly is observability. It does not validate the output.
```

### 3. retrieval_document_attributes_are_provenance_not_support

Candidate point:

```text
Retrieved documents can be represented with document content, id, metadata, and
score attributes.
```

Source anchor:

```text
semantic_conventions.md:29-32
semantic_conventions.md:102
```

VAKS fit:

```text
This maps well to source/context-pack receipts: which document was activated,
what metadata followed it, and what the retrieval system scored it.
```

Boundary:

```text
A retrieved document record is provenance and activation evidence. It is not
evidence support unless the specific source span supports the specific claim or
relation under review.
```

### 4. reranker_and_document_scores_are_activation_signals

Candidate point:

```text
Reranker spans include input documents, output documents, query, top_k, model
name, and document scores.
```

Source anchor:

```text
semantic_conventions.md:97-102
```

VAKS fit:

```text
Good candidate vocabulary for retrieval diagnostics and "why did this context
surface" reports.
```

Boundary:

```text
Reranker output and document score remain activation signals. They cannot become
truth confidence, reviewed relation, citation support, or action readiness.
```

### 5. prompt_template_versioning_as_run_receipt

Candidate point:

```text
Prompt template, variables, and version can be recorded as span attributes.
```

Source anchor:

```text
semantic_conventions.md:55-57
```

VAKS fit:

```text
Useful for future prompt/skill/version receipts, especially when a candidate
distillation or context pack depends on a particular prompt template.
```

Boundary:

```text
Prompt version improves reproducibility. It does not prove correctness.
Prompt variables may contain sensitive or raw source content and need scope
control.
```

### 6. token_and_cost_fields_as_operational_accounting

Candidate point:

```text
Token counts and cost attributes can track prompt, completion, reasoning, audio,
cache read/write, total tokens, and USD cost.
```

Source anchor:

```text
semantic_conventions.md:58-76
semantic_conventions.md:168-188
```

VAKS fit:

```text
Useful for Use Ledger, run receipts, budget accounting, and knowing which tasks
were expensive enough to deserve cached artifacts or review.
```

Boundary:

```text
High cost, many tokens, or reasoning-token usage says nothing by itself about
quality, truth, or review status.
```

### 7. tool_call_traces_need_access_policy_boundary

Candidate point:

```text
Tool schemas, tool names, tool ids, tool call arguments, and tool call ids can
be represented in trace attributes.
```

Source anchor:

```text
semantic_conventions.md:77
semantic_conventions.md:105-113
semantic_conventions.md:277-284
```

VAKS fit:

```text
Strong fit for future agent-tool audit: what tools were advertised, what tool
was called, and with what arguments.
```

Boundary:

```text
Trace visibility is not tool permission. VAKS still needs separate access tiers,
path-scoped writes, user intent confirmation, and review gates before
action-facing tool use.
```

### 8. evaluator_and_guardrail_spans_are_diagnostics_not_review

Candidate point:

```text
OpenInference has span kinds for guardrail checks and evaluator calls.
```

Source anchor:

```text
semantic_conventions.md:19-20
```

VAKS fit:

```text
Useful for recording that a guardrail or evaluator was run during an operation.
```

Boundary:

```text
Evaluator and guardrail spans are diagnostics/process evidence. They are not
human review, evidence-aware review, truth confidence, or action basis.
```

### 9. session_user_metadata_tags_need_privacy_scope

Candidate point:

```text
Session id, user id, metadata, and tags can be attached to spans.
```

Source anchor:

```text
semantic_conventions.md:93
semantic_conventions.md:103-114
```

VAKS fit:

```text
Useful for threading run receipts, grouping related operations, and later
recovering what happened in a task.
```

Boundary:

```text
These fields are privacy-sensitive and scope-sensitive. They should not become
global memory by default, and should not be written into reviewed knowledge.
```

### 10. flattened_attributes_enable_interoperable_trace_export

Candidate point:

```text
OpenInference flattens lists of structured objects into indexed attribute names,
for messages, multimodal content, tool calls, and tools.
```

Source anchor:

```text
semantic_conventions.md:231-338
```

VAKS fit:

```text
Useful if VAKS ever exports operation receipts to OpenTelemetry-style traces or
needs a bridge between Markdown receipts and tracing backends.
```

Boundary:

```text
Flattening is an interoperability mechanism, not a reason to replace VAKS's
file-first reviewed knowledge model.
```

## Candidate Routing Hints

Candidate routing hints:

```text
span kind for operation category
input/output mime and values for run receipts
prompt template/version/variables for reproducibility
retrieved document id/content/metadata/score for context activation receipts
reranker input/output/query/top_k/model fields for retrieval diagnostics
tool schema/call/id/arguments for tool-call audit
token/cost/cache fields for Use Ledger accounting
session/user/tag/metadata fields for recovery and grouping, with privacy limits
```

Candidate boundaries:

```text
retrieval score != evidence support
evaluator span != evidence-aware review
guardrail span != risk review
tool call trace != tool authorization
prompt trace != correctness
token/cost accounting != quality
session metadata != reviewed memory
```

## VAKS Routing Decision

This source should stay in:

```text
raw/repos
outputs/review
outputs/review/project_overlays
```

It should not write into:

```text
wiki/claims
wiki/decisions
wiki/patterns as adopted pattern
SCHEMA.md
IMPLEMENTATION_BLUEPRINT.md
SOURCE_INTAKE.md
```

Reason:

```text
The source is high-quality and relevant, but current use is still candidate
comprehension. Actual adoption of tracing conventions would affect runtime
receipts, tool-call audit, privacy policy, and action-facing logs, so it would
need a later v0.2.13 review.
```

## v0.2.13 Trigger

Current trigger:

```text
no
```

Trigger later if we use this source to:

```text
change VAKS schema or templates
define an official run receipt format
instrument a tool or agent runtime
log user/session/tool/prompt data by default
use evaluator or guardrail traces as review evidence
support an action-facing answer
```

Required later review shape:

```text
claim + anchored evidence + non-circular warrant + scope + gaps + residual risk
```


