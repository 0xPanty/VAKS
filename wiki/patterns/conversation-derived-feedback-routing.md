---
type: pattern
status: active
created: 2026-05-27
updated: 2026-05-27
source_libraries:
  - "local architecture discussion"
  - "gpt-5.5 xhigh subagent review"
sources:
  - "[[FEEDBACK]]"
  - "[[SCHEMA]]"
  - "[[IMPLEMENTATION_BLUEPRINT]]"
  - "https://www.microsoft.com/en-us/research/publication/unbiased-learning-rank-biased-feedback/"
  - "https://www.microsoft.com/en-us/research/publication/exploring-session-context-using-distributed-representations-of-queries-and-reformulations/"
  - "https://arxiv.org/abs/2307.14117"
  - "https://arxiv.org/abs/2407.00072"
  - "https://arxiv.org/abs/2405.14431"
related_concepts:
  - "[[semantic-relation-edge-schema]]"
related_projects:
  - verified-action-knowledge-system
adoption_status: adopted
verification_status: active
evidence_level: synthetic
evidence_count: 6
confidence: high
negative_evidence:
  - "Continuing a conversation can mean the previous answer was useful, but it can also mean the previous answer was incomplete or confusing."
  - "Implicit feedback is biased by what was shown, what was omitted, and the user's current phrasing."
  - "If implicit feedback changes truth confidence, the system will learn preference instead of evidence."
replaces:
superseded_by:
extension_points:
  - feedback adapters
  - context pack modes
  - query routing
  - retrieval indexes
last_verified: 2026-05-27
next_review: 2026-06-03
epistemic_type: take
gaps:
  - "No query-run recorder exists yet."
  - "No JSONL-to-SQLite aggregation script exists yet."
  - "No fixed eval set exists for checking whether feedback improves retrieval without hiding contradictions."
evidence_timeline:
  - date: 2026-05-27
    source: "architecture discussion"
    observation: "The user identified that follow-up questions, corrections, and narrowing turns can act as low-friction feedback."
    effect: supports
    confidence: high
  - date: 2026-05-27
    source: "gpt-5.5 xhigh subagent review"
    observation: "The subagent agreed with Markdown + JSONL + rebuildable SQLite, but warned that continuation is only a weak session-local signal."
    effect: refines
    confidence: high
relations:
  - target: "[[FEEDBACK]]"
    type: refines
    strength: 5
    confidence: high
    evidence:
      - "[[conversation-derived-feedback-routing]]"
    rationale: "This pattern adds implicit conversation signals to the feedback layer while preserving the truth/usefulness/scope-fit boundary."
    created: 2026-05-27
    last_verified: 2026-05-27
  - target: "[[accumulated-source-cross-validation]]"
    type: complements
    strength: 4
    confidence: high
    evidence:
      - "[[conversation-derived-feedback-routing]]"
    rationale: "Point collision strengthens stored knowledge over time; conversation-derived feedback strengthens query routes over time."
    created: 2026-05-27
    last_verified: 2026-05-27
tags:
  - pattern
  - feedback
  - implicit-feedback
  - query-routing
  - activation
---

# Conversation-Derived Feedback Routing

## AI-readable preamble

Conversation-derived feedback turns the user's next turn into a weak routing signal.

It can help future retrieval choose better keywords, routes, and scope. It must not rewrite truth, promote candidates, or hide contradictions.

The safest interpretation is:

```text
conversation behavior = routing preference signal
conversation behavior != truth signal
```

## Problem

Asking the user to mark every answer is too heavy.

But normal conversation already contains feedback:

```text
继续沿着同一条问
问得更具体
说跑偏
说漏了
说不是这个意思
换了一个方向
```

If the vault ignores these signals, it loses a natural learning path. If it trusts them too much, retrieval becomes biased and self-reinforcing.

## Pattern

Record important query runs, then classify the next user turn as a small feedback signal.

```text
query-run
-> activated points / relations / routes
-> answer
-> next user turn
-> conversation-derived feedback-event
-> session-local route adjustment
-> reviewed or aggregated persistent adjustment only when strong enough
```

The first version should adjust only:

```text
usefulness
scope fit
activation ranking
route / keyword boost
```

It must not adjust:

```text
truth confidence
verification_status
source reliability
decision outcome
```

## Signal Map

Use conservative signal meanings.

```text
explicit_positive:
  user says useful, correct direction, keep going
  effect: usefulness + route boost
  persistence: can persist

same_line_followup:
  user continues along the same line
  effect: session-local route boost only
  persistence: not persistent by default

narrower_followup:
  user asks a more specific version
  effect: create or strengthen query keyword/channel
  persistence: route-level candidate, not point truth

correction:
  user says no, not this, wrong, misunderstood
  effect: lower route/scope fit for this query shape
  persistence: can persist when explicit

wrong_scope:
  user says version/project/domain/time is wrong
  effect: narrow scope fit
  persistence: can persist

missing:
  user says a key point is missing
  effect: create missing-point or missing-route candidate
  persistence: review queue, not automatic truth

topic_shift:
  user changes topic
  effect: close previous session route
  persistence: no feedback
```

## Storage Rule

Markdown remains the human-readable source of truth.

JSONL is the event truth for feedback:

```text
outputs/feedback/query-runs/YYYY-MM-DD.jsonl
outputs/feedback/events/YYYY-MM-DD.jsonl
```

SQLite may be added later as a rebuildable cache:

```text
outputs/feedback/index.sqlite
```

If deleting SQLite loses knowledge, the design is wrong. SQLite should only speed up aggregation and lookup.

## Minimal Event Fields

`query-run` should capture what was exposed:

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
inferred_keywords: []
activated_points: []
activated_relations: []
activated_routes: []
answer_path: []
warnings: []
gaps: []
```

`feedback-event` should capture how the next turn reacts:

```yaml
record_type: feedback-event
feedback_source: conversation-derived
feedback_id:
query_id:
session_id:
derived_from_turn_id:
target_type: point | relation | route | keyword | channel | answer
target_id:
signal_type: explicit_positive | same_line_followup | narrower_followup | correction | wrong_scope | missing | topic_shift
polarity: positive | negative | neutral
signal_strength: -2 | -1 | 0 | 1 | 2
signal_confidence: 0.0-1.0
scope_key:
reason:
effect:
  activation_delta:
  usefulness_delta:
  scope_fit_delta:
requires_review:
```

Do not store full private conversation when a summary, turn id, target id, and short reason are enough.

## Weight Rule

Use explainable caps instead of hidden learning.

```text
effective_delta =
  signal_strength
  * signal_confidence
  * recency_decay
  * exposure_weight
```

Limits:

```text
same_line_followup:
  session-local only by default

per_session_cap:
  each target can move at most +/-1 per session

persistent_cap:
  usefulness and scope-fit adjustment stay between -2 and +2

decay:
  old conversation-derived feedback fades unless repeated across sessions
```

## Why It Helps

This lets the vault learn the user's real working routes without forcing manual UI every time.

Example:

```text
User asks: feedback interaction feels dumb
System activates: explicit buttons, feedback-event, trace grading
User asks: can continuing the conversation itself count?
System records:
  narrower_followup on implicit feedback
  new inferred keyword: conversation-derived feedback
  route boost for future feedback-design questions
```

Next time the user asks about feedback design, the vault should retrieve both:

```text
structured feedback
conversation-derived feedback
```

## Failure Boundary

Do not over-read silence or continuation.

Bad interpretations:

```text
user kept asking = answer was correct
user asked a narrower question = previous point is true
user said thanks = permanent positive feedback
user stayed in same topic for an hour = global route boost
```

Correct interpretation:

```text
user kept asking = maybe useful, maybe incomplete
narrower question = route/keyword signal
explicit correction = scope/routing negative signal
missing point = review candidate
```

## Fit In This Vault

This pattern complements the existing alpha:

```text
point collision:
  improves stored knowledge by comparing traceable points

conversation-derived feedback:
  improves query routes by observing how the user continues
```

Both are useful only if review gates remain intact.
