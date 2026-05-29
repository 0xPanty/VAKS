---
type: handoff
status: active
created: 2026-05-29
project: verified-action-knowledge-system
scope:
  - architecture
  - pro-review
  - supplements-1-8
  - next-window
---

# Verified Action Knowledge System v0.2 - Pro 1-8 Handoff

## Working Directory

```text
C:\Users\Administrator\Documents\资料库
```

## Current State

Pro supplements 1-8 have been reviewed, absorbed, and written back into the architecture files.

The public spine remains:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

The internal loop remains:

```text
source
-> candidate point
-> calibration / point collision
-> review
-> reviewed node / reviewed relation
-> context pack / action basis
   with coverage_map / evidence_sufficiency when action-ready or high-impact
-> action
-> use ledger / feedback
```

Main controlling principle:

```text
Strict checks are lazy gates.

Capture stays light.
Ordinary query stays simple.
Promotion gets strict.
Action basis gets auditable.
Feedback improves activation, not truth.
```

Strict checks do not run for ordinary capture or ordinary query by default.
They open for promotion, decision, action basis, strong reviewed relation, high-impact / stale / contested / explicitly challenged points, or risk_sensitive_answer.

## Pro Supplements Landed

1. Knowledge Calibration / Point Collision
   - Raw source does not collide with the vault directly.
   - Candidate points collide with reviewed knowledge.
   - Calibration output is review input, not truth.

2. Evidence-Aware Review
   - Review is standing check, not source check.
   - Full support / challenge / qualification / risk panel is a lazy gate.

3. Lightweight Source Provenance
   - Source records capture identity and capture/extraction trace.
   - Provenance is not support, truth, confidence, or action readiness.

4. Verifiability Routing
   - Candidate point is atomic review unit, not necessarily claim.
   - Minimal fields: point_type, verifiability.state, review_route.

5. Claim / Point Coverage Map
   - Context packs are coverage-aware.
   - Full coverage_map is only for key judgments used in an answer or action basis.
   - Risk is shown through risk_flags / risk_refs / action_readiness, not coverage_status.

6. Optional Point Graph Fragment
   - Optional high-impact-only review aid.
   - Triplets are not truth, not support, and not reviewed relations.

7. Evidence Support Check
   - A source link is not evidence.
   - Evidence must support the specific point or relation.
   - evidence_support lives on evidence items / source_refs, not Source nodes.
   - Stable enum:

```yaml
evidence_support:
  span_supports_target: supported | partial | unsupported | unclear
  evidence_role: direct_support | inferential_support | background_context | counterexample
  reviewer_note:
```

8. Evidence Sufficiency Gate
   - Single evidence support does not mean the whole evidence set is sufficient.
   - Gate runs after a draft evidence/context envelope is assembled and before action-ready finalization.

```yaml
evidence_sufficiency:
  state: sufficient | weak | insufficient | out_of_scope | risky
  checked_for: context_pack | action_basis | decision | promotion | reviewed_relation | risk_sensitive_answer
  missing: []
  required_next_step: proceed | ask_user | retrieve_more | create_missing_point | narrow_scope | mark_not_actionable | needs_review
  reviewer_note:
```

## Files Updated

Core docs and contracts:

```text
AGENTS.md
README.md
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SCHEMA.md
SECOND_BRAIN_MODEL.md
SOURCE_INTAKE.md
REVIEW_QUEUE.md
IMPLEMENTATION_BLUEPRINT.md
00_handoff/2026-05-28-verified-action-knowledge-system-v0-2-handoff.md
wiki/indexes/knowledge-graph-index.md
```

Templates:

```text
templates/review-candidate.md
templates/claim-record.md
templates/dev-context-pack.md
templates/source-record.md
templates/design-pattern.md
templates/anti-pattern.md
templates/decision-record.md
templates/library-review.md
templates/architecture-review-window-prompt.md
```

New source records:

```text
raw/papers/2026-05-29-truth-maintenance-system-source.md
raw/papers/2026-05-29-dung-argumentation-framework-source.md
raw/articles/2026-05-29-w3c-prov-source.md
raw/papers/2026-05-29-veriscore-source.md
raw/papers/2026-05-29-papertrail-source.md
raw/papers/2026-05-29-graphfc-source.md
raw/papers/2026-05-29-prove-provenance-verification-source.md
raw/papers/2026-05-29-rag-attribution-faithfulness-source.md
raw/papers/2026-05-29-self-rag-source.md
raw/papers/2026-05-29-crag-source.md
raw/papers/2026-05-29-a2rag-source.md
```

Candidate-only research output:

```text
outputs/review/2026-05-29-framework-reference-research.md
```

## Validation Done

Ran:

```text
git diff --check
rg checks for old yes/no evidence_support enum
rg checks for old required_next_step without narrow_scope
rg checks for risky-as-coverage-status wording
rg checks for old replaces collision enum
rg trailing whitespace check on new raw source records
```

Result:

```text
No substantive check failures.
git diff --check reports only Windows LF/CRLF warnings.
Some older pre-existing QA/wiki files contain trailing spaces; they were not changed in this cleanup.
```

## Next Window

Continue with Pro supplement 9:

```text
HippoRAG-style association retrieval / association neighborhood.
```

Start read-only.

Read first:

```text
AGENTS.md
00_handoff/2026-05-29-verified-action-knowledge-system-v0-2-pro-1-8-handoff.md
README.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SCHEMA.md
REVIEW_QUEUE.md
SECOND_BRAIN_MODEL.md
templates/dev-context-pack.md
wiki/indexes/knowledge-graph-index.md
```

Expected discussion posture:

```text
Explain point 9 in plain Chinese first.
Discuss whether it is reasonable and how to absorb it minimally.
Do not edit files until the user confirms.
Do not turn HippoRAG into a truth module.
Do not let graph traversal, PageRank, or association retrieval decide truth.
Likely absorption, if accepted: association retrieval / context activation only.
```

Current likely positioning for point 9:

```text
The vault does not retrieve isolated chunks.
It activates an evidence-aware association neighborhood.

But:
association retrieval is activation, not truth;
graph traversal is recall, not support;
reviewed relations remain the only formal graph edges.
```

## Do Not Do By Default

```text
No automation.
No API/MCP/viewer implementation.
No dev context pack trial unless explicitly requested.
No commit/push except when explicitly requested.
No source record promotion without review.
```
