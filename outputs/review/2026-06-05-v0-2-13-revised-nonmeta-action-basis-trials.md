---
type: real_action_basis_trial
status: candidate
created_at: 2026-06-05
project: verified-action-knowledge-system
version_under_test: v0.2.13 revised candidate
rule_under_test: v0-2-13-make-action-support-visible
trial_scope: non_meta_real_candidate_materials
truth_boundary: trial output only, not reviewed knowledge, not architecture decision
write_scope: outputs/review only
---

# v0.2.13 Revised Non-Meta Action-Basis Trials

## 说人话结论

这轮用两个真实候选材料试跑 v0.2.13 revised：

```text
Trial 1: retrieval-is-activation-not-truth
Trial 2: source-structure-first-rag
```

结果很有区分度：

```text
Trial 1 能放行到 candidate wording review，但不能自动进主线。
Trial 2 不能直接改模板，因为 required gates 缺失且有 ordinary capture 变重风险。
```

这说明规则不是只会“全拦”，也不是只会“全放”。它能根据 claim/evidence/warrant/scope/challenge 的完整程度做分层 disposition。

## Trial 1: Retrieval Is Activation, Not Truth

### Question

```text
Should VAKS prepare a future minimal wording review for the boundary
"retrieval is activation/context preparation, not truth/action basis"?
```

### Action-Facing Claim

```text
VAKS may prepare a future minimal wording review for the retrieval boundary,
but must not treat the candidate pattern or ledger row as automatic mainline promotion.
```

### Point-Specific Anchored Evidence

Evidence 1:

```text
outputs/review/candidate_pattern_bank/retrieval-is-activation-not-truth.md
```

Relevant support:

```text
The one-line pattern says retrieval, vector similarity, rerank, GraphRAG,
community summary, and agentic retrieval only bring material forward; they are
not truth confidence, reviewed relation, or action basis.
```

Evidence 2:

```text
outputs/review/project_borrowing_ledgers/VAKS.md
```

Relevant support:

```text
The VAKS ledger marks this pattern `adapt` and says it already aligns with
the main boundary, but still needs wording review before any template patch.
```

Evidence 3:

```text
outputs/review/2026-06-05-v0-2-13-structured-action-basis-envelope-revised-candidate-patch.md
```

Relevant support:

```text
The revised patch preserves retrieval/context pack as activation/context preparation,
not support or action readiness.
```

### Non-Circular Warrant

These anchors support the claim because they address the same boundary from three positions:

```text
candidate pattern states the boundary
VAKS ledger records project fit but blocks automatic promotion
v0.2.13 revised preserves the same boundary as a rule constraint
```

Therefore, the evidence supports preparing a minimal wording review. It does not support mainline promotion because all anchors remain candidate/project-fit/revised-candidate materials, not reviewed architecture decisions.

### Scope / Assumptions

Scope:

```text
retrieval / context-pack / activation boundary only
not all RAG quality work
not source intake templates
not reviewed relation creation
```

Assumptions:

```text
future wording review would be explicit and separate
no schema/template edit occurs in this trial
```

### Known Challenges / Gaps

```text
candidate pattern is active but not reviewed knowledge
ledger adapt is not ADR/action basis
no exact mainline wording has been reviewed
ordinary query should not become heavy evidence review
```

### Current Residual Review Status

```yaml
disposition: candidate_wording_review_allowed
mainline_promotion: blocked
template_change: blocked
residual_risk: low for candidate wording review, high for direct promotion
```

### Trial Judgment

PASS.

The v0.2.13 revised rule makes the right split:

```text
yes to future minimal wording review
no to automatic promotion
```

## Trial 2: Source Structure First For RAG

### Question

```text
Should VAKS change source intake templates now to require structure-preserving fields?
```

### Action-Facing Claim Being Tested

```text
VAKS should update source intake templates now to require source-structure preservation fields.
```

### Point-Specific Anchored Evidence

Evidence 1:

```text
outputs/review/candidate_pattern_bank/source-structure-first-rag.md
```

Relevant support:

```text
The candidate pattern says preserving titles, sections, tables, paragraphs,
page/time anchors, and file hierarchy before retrieval/chunking can prevent
downstream distortion.
```

Evidence 2:

```text
outputs/review/project_borrowing_ledgers/VAKS.md
```

Relevant support:

```text
The VAKS ledger marks this pattern `adapt` for future source intake,
context-pack preparation, and retrieval workbench.
```

### Warrant Being Tested

```text
The pattern is active and VAKS ledger says adapt, so source intake templates should change now.
```

### v0.2.13 Revised Evaluation

This warrant fails.

Reasons:

```text
candidate pattern status is not reviewed knowledge
ledger adapt is project posture, not architecture decision
required gates before promotion include direction review, source-card template update review,
and evidence-aware review if promoted to architecture principle
the pattern itself warns ordinary capture should not become too heavy
```

### Scope / Assumptions

The evidence supports:

```text
source-structure preservation as design pressure
future candidate review
possible lightweight guidance exploration
```

It does not support:

```text
template change now
mandatory fields for all sources
ordinary capture burden
mainline architecture principle
```

### Known Challenges / Gaps

```text
no template-specific review
no burden test for ordinary source cards
source structure extraction can itself be wrong
short/light capture may not need structure fields
```

### Current Residual Review Status

```yaml
disposition: blocked_for_template_change_now
allowed_next_step: candidate-only lightweight structure-guidance sketch or direction review
mainline_promotion: blocked
template_change: blocked
residual_risk: high if changed now, manageable if kept candidate-only
```

### Trial Judgment

PASS.

The v0.2.13 revised rule blocks the tempting but premature action:

```text
active pattern + adapt ledger != template update authority
```

## Cross-Trial Finding

The rule can distinguish:

```text
coherent candidate action-basis for next review
```

from:

```text
premature mainline/template action
```

That is exactly the behavior VAKS needs at the boundary between candidate borrowing and action basis.

## Remaining Issue

The only issue left is operational, not conceptual:

```text
Repeated real use may need a tiny warrant-quality checklist
so reviewers apply "non-circular warrant" consistently.
```

Do not add that checklist yet. First observe one or two more real trials.

## Final Trial Verdict

```text
v0.2.13 revised candidate survives non-meta action-basis trials.
```

Keep:

```text
candidate-only
no mainline patch
no candidate pattern file
no template edit
```

Next:

```text
Use the rule opportunistically on the next real action-basis or promotion decision.
```
