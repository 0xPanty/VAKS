---
type: implementation-note
status: active
created: 2026-05-27
updated: 2026-05-28
project: verified-action-knowledge-system
related_decisions:
  - "[[2026-05-27-traceability-first-graduated-verification]]"
related_patterns:
  - "[[accumulated-source-cross-validation]]"
  - "[[conversation-derived-feedback-routing]]"
sources:
  - "[[REVIEW_QUEUE]]"
  - "[[2026-05-27-alpha-point-collision-validation-v0-1]]"
  - "[[2026-05-27-conversation-derived-feedback-routing-research]]"
verification_status: active
evidence_level: synthetic
confidence: high
validated_by:
  - "subagent architecture review"
  - "local architecture discussion"
rollback_path:
  - "If feedback starts reinforcing wrong answers, ignore feedback weights and fall back to reviewed relations plus source evidence."
last_verified: 2026-05-28
next_review: 2026-06-03
relations:
  - target: "[[REVIEW_QUEUE]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[FEEDBACK]]"
    rationale: "Feedback controls how reviewed points and relations are activated during future queries without changing truth directly."
    created: 2026-05-27
    last_verified: 2026-05-28
tags:
  - feedback
  - activation
  - scope-fit
  - query-learning
  - implicit-feedback
  - conversation-derived-feedback
---

# FEEDBACK.md v0.1

## AI-readable preamble

Feedback improves future retrieval and context activation.

In v0.2 language, this file is the Use Ledger contract.

Feedback must not directly rewrite truth. It can adjust usefulness, scope fit, and activation ranking. Formal truth changes still require review and promotion.

The goal is to make the vault less likely to repeat bad activation paths without hiding evidence or overfitting to user preference.

## 1. Core Rule

Separate three things:

```text
truth confidence:
  Is the point true or well-supported?

usefulness:
  Did this point help answer this kind of question?

scope fit:
  Does this point apply to this project, time, version, domain, or intent?
```

Feedback can adjust:

```text
usefulness
scope fit
activation ranking
```

Feedback cannot directly adjust:

```text
truth confidence
verification_status
source reliability
decision outcome
```

Those require review.

## 2. Feedback Record

Use this record for every meaningful correction:

```yaml
record_type: feedback-event
feedback_id:
created:
created_by:
feedback_source: explicit-user | conversation-derived | system-eval | action-result
query_id:
session_id:
turn_id:
parent_query_id:
derived_from_turn_id:
question:
query_intent: answer | decision | implementation | research | content | memory
query_scope:
  project:
  domain:
  version:
  time_range:
scope_key:
target_type: point | relation | cluster | claim | pattern | decision | context-pack | answer | route | keyword | channel
target_id:
feedback_type: useful | irrelevant | misleading | wrong_scope | stale | missing | contradicted | incomplete | too_weak | too_broad
signal_type: explicit_positive | same_line_followup | narrower_followup | correction | wrong_scope | missing | topic_shift | none
polarity: positive | negative | neutral
signal_strength: -2 | -1 | 0 | 1 | 2
signal_confidence: 0.0-1.0
severity: low | medium | high
reason:
evidence:
  - source_ref:
    note:
effect:
  activation_delta: -2 | -1 | 0 | 1 | 2
  usefulness_delta: -2 | -1 | 0 | 1 | 2
  scope_fit_delta: -2 | -1 | 0 | 1 | 2
  relation_strength_delta: -1 | 0 | 1
requires_review: true | false
review_status: pending | accepted | rejected
reviewed_by:
reviewed_at:
next_action:
```

## 3. Feedback Types

### useful

The activated point or relation helped answer the question.

Allowed effect:

```text
increase usefulness for similar query scope
increase activation ranking for similar query scope
```

Not allowed:

```text
increase truth confidence directly
```

### irrelevant

The point was related by words but not useful for this question.

Allowed effect:

```text
lower activation in this query scope
add near_miss signal
```

### misleading

The point led the answer in a wrong direction.

Allowed effect:

```text
lower activation
require review on relation
add warning to cluster
```

### wrong_scope

The point is valid somewhere else but not here.

Allowed effect:

```text
narrow scope
lower scope_fit for this project/domain/version
```

### stale

The point may be outdated.

Allowed effect:

```text
mark review due
lower activation until reviewed
```

Not allowed:

```text
delete or reject automatically
```

### missing

The answer missed an important point.

Allowed effect:

```text
create missing-point candidate
create missing-relation candidate
```

### contradicted

The answer ignored or mishandled a contradiction.

Allowed effect:

```text
raise contradiction priority
require context pack to include the contradiction next time
```

## 4. Conversation-Derived Feedback

Some feedback is explicit:

```text
this was useful
wrong direction
you missed X
not this scope
```

Some feedback is inferred from the next user turn:

```text
the user keeps asking along the same line
the user narrows the question
the user corrects the route
the user points out a missing piece
the user changes topic
```

This is called:

```text
conversation-derived feedback
```

It is weaker than explicit feedback.

### 4.1 Signal meanings

Use conservative meanings:

```text
explicit_positive:
  user directly says the answer or route is useful
  can persist as usefulness / route boost

same_line_followup:
  user continues along the same line
  session-local boost only by default
  do not treat as satisfaction

narrower_followup:
  user asks a more specific version
  create or strengthen route / keyword / channel
  do not permanently boost a point by default

correction:
  user says no, not this, misunderstood, or wrong
  lower route / scope fit for this query shape

wrong_scope:
  user says project, version, time, domain, or intent is wrong
  narrow scope fit

missing:
  user says a key point is missing
  create missing-point or missing-route candidate
  do not punish every activated point

topic_shift:
  user changes topic
  close the previous route
  do not write persistent feedback
```

### 4.2 Persistence rules

Do not persist weak implicit positive signals by default.

```text
same_line_followup:
  session-local only

narrower_followup:
  persistent only as route / keyword candidate

explicit correction:
  can persist as negative route / scope signal

missing:
  review candidate, not truth update
```

Only persist conversation-derived feedback when it is explicit, repeated across sessions, or attached to a high-value query run.

### 4.3 Storage

Use append-only JSONL as the event truth:

```text
outputs/feedback/query-runs/YYYY-MM-DD.jsonl
outputs/feedback/events/YYYY-MM-DD.jsonl
```

SQLite can be added later as a rebuildable cache:

```text
outputs/feedback/index.sqlite
```

If deleting SQLite loses knowledge, the design is wrong.

Derived SQLite tables can start as:

```text
query_runs(query_id, session_id, intent, scope_key, created)
candidate_exposures(query_id, target_id, rank, shown, included)
feedback_signals(feedback_id, target_id, signal_type, strength, confidence, scope_key)
activation_adjustments(target_id, scope_key, usefulness_adj, scope_fit_adj, updated_at)
```

### 4.4 Weight caps

Use explainable caps, not hidden learning:

```text
effective_delta =
  signal_strength
  * signal_confidence
  * recency_decay
  * exposure_weight
```

Limits:

```text
per_session_cap:
  each target can move at most +/-1 per session

persistent_cap:
  usefulness and scope-fit adjustment stay between -2 and +2

decay:
  old conversation-derived feedback fades unless repeated
```

## 5. Query Run Record

Feedback needs a query run to attach to.

Template:

```text
templates/query-run.md
```

```yaml
record_type: query-run
query_id:
session_id:
turn_id:
parent_query_id:
created:
question_summary:
query_intent:
query_scope:
scope_key:
inferred_keywords: []
seed_points: []
expansion_depth:
activated_points: []
activated_relations: []
activated_routes: []
included_sources: []
excluded_candidates: []
answer_path:
warnings: []
gaps: []
```

This can live under:

```text
outputs/qa/
outputs/review/query-runs/
outputs/feedback/query-runs/
```

v0.1 can store only important query runs, not every small chat.

## 6. Activation Scoring v0.1

Use simple explainable scoring.

```text
activation_score =
  query_relevance
  + relation_strength
  + reviewed_bonus
  + source_independence_bonus
  + usefulness_adjustment
  + scope_fit_adjustment
  + conversation_route_adjustment
  - stale_penalty
  - unresolved_contradiction_penalty
  - wrong_scope_penalty
```

Each part should be explainable in the context pack.

No hidden model-only score should decide what enters the final answer.

## 7. Feedback Safety Rules

Hard rules:

```text
Feedback does not change truth confidence directly.
Feedback does not delete contradictions.
Feedback does not hide negative evidence.
Feedback does not promote candidates.
Feedback does not lower source reliability from one bad answer.
Feedback does not make user preference equal truth.
Conversation-derived feedback does not become persistent by default.
Continuation does not equal satisfaction.
```

Feedback can create review work:

```text
relation needs review
point scope needs narrowing
claim may be stale
missing point should be extracted
context pack should include contradiction
```

## 8. L2 / L3 Expansion Rules

Default query expansion:

```text
L1:
  directly matched seed points and reviewed promoted nodes

L2:
  reviewed supports / contradicts / refines / risk_of / derived_from edges

L3:
  disabled by default
```

Allow L3 only when:

```text
the user asks for deep analysis
the edges are reviewed
the query budget allows it
or the system is building a decision context pack
```

This prevents graph explosion.

## 9. First Trial

Run after the first point-collision trial.

Procedure:

```text
1. Ask one real question against the 10-source trial set.
2. Record seed points and activated L2 points.
3. Produce an answer with supports, contradictions, gaps, and warnings.
4. User marks 2-5 activations as useful / irrelevant / wrong_scope / missing.
5. Write feedback-event records.
6. Ask a similar question and check whether activation improves.
7. Add one conversation-derived feedback trial:
   same_line_followup, narrower_followup, correction, wrong_scope, or missing.
```

Success condition:

```text
The second answer includes fewer irrelevant activations and does not hide contradiction.
```

Failure condition:

```text
Feedback makes the answer more agreeable but less evidence-aware.
```

## 10. Current Stop Point

v0.1 defines feedback as a record and ranking input.

It does not implement automatic learning, nightly rewrites, or hidden weight updates.
