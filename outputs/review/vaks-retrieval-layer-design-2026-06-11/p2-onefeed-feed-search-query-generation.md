---
record_kind: p2_candidate_point
status: candidate
knowledge_status: candidate
project_id: VAKS
created_at: 2026-06-11
created_by: Codex
source:
  - raw/papers/2026-06-11-guoxun-onefeed-source.md
  - outputs/review/2026-06-11-guoxun-onefeed-candidate-distillation.md
  - wiki/summaries/2026-06-11-guoxun-onefeed-architecture-review.md
processing_tier: heavy
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: p2_candidate_not_authority
promotion_gate: retrieval_layer_comparison_and_sandbox_required
action_basis_allowed: false
truth_mutation_allowed: false
borrow_value: medium
borrow_order: P2
target_layer:
  - retrieval-layer
  - query-intent-router
  - feedback-ledger
  - context-pack-preparation
tags:
  - p2
  - candidate-only
  - query-generation
  - retrieval-layer-design
---

# P2 Candidate: OneFeed Query-Generation-Assisted Retrieval

## 说人话

OneFeed 的可借鉴点不是“它证明了性能很好”。它还没证明。

可借的是这个想法：

```text
用户显式问什么
和用户最近隐式在做什么
应该一起决定检索怎么展开。
```

对 VAKS 来说，这可以变成“受控 query 扩展”。

## VAKS-safe Pipeline

```text
1. User query
2. Active project / recent context / feedback hints
3. Generate controlled query variants
4. Apply scope and authority bucket filters
5. Run lexical / vector / graph recall inside allowed buckets
6. Merge candidates into anchor queue
7. Context pack assembly
8. Evidence/action gate if needed
9. Feedback updates future activation, not truth
```

## Controlled Query Variant Shape

```yaml
query_variant:
  text:
  reason:
  derived_from:
    - user_query
    - active_project_context
    - retrieval_failure_trace
  allowed_buckets:
  forbidden_buckets:
  source_scope:
  time_scope:
  warning_code:
```

## Borrow

- Generate query variants to improve recall when the user's wording is narrow.
- Use active project context as activation hint.
- Align query intent with anchor types before retrieval.
- Evaluate query generation by whether it retrieves useful anchors, not by pretty wording.
- Feed negative retrieval outcomes into review pressure or routing adjustment.

## Do Not Borrow

- Expected performance tables as evidence.
- Feedback as truth confidence.
- Generated query as user intent certainty.
- Generated semantic ID as source authority.
- Query expansion across raw/candidate/reviewed/action buckets without policy checks.

## Fit With Existing Retrieval Inputs

```text
turbovec:
  rerank inside allowed vector candidate set

mnemosyne:
  local hybrid retrieval composition

Graphify:
  structure graph orientation

OneFeed:
  controlled query expansion from explicit + implicit context
```

## Pilot Test

Minimum useful pilot:

```text
take 20 VAKS real questions
create 2-5 controlled query variants each
run bucket-first retrieval
compare against no-variant baseline
measure:
  recall of useful anchors
  source-anchor correctness
  candidate/reviewed/action leakage
  number of noisy extra results
  user-perceived helpfulness
```

Pass condition:

```text
better anchor recall
manageable noise
zero action-basis leakage
no truth mutation from feedback
```

## Current Status

```text
P2 candidate.
Conceptual value: medium.
Empirical evidence: low.
Do not promote before sandbox.
```
