---
record_kind: sandbox_reviewer_report
slice_id: 2026-06-15-p1-5-14-raw-intake-parser-router-sandbox
status: review_pass_no_blocker
truth_boundary: reviewer_report_only
---

# Reviewer Report

## Reviewer Scope

Read-only review for:

- bugs;
- missing tests;
- overdesign;
- maintainability;
- fixture and failure-case coverage;
- whether local verification really exercises the contract.

## Current Conclusion

```text
REVIEW_PASS_NO_BLOCKER
```

## Initial Conclusion

```text
REVIEW_BLOCKERS_FOUND
```

## Initial Blocker

Reviewer found a direct-field authority bypass. The validator blocked claim
arrays and selected boolean fields, but these direct fields could pass:

- `retained_outputs[0].evidence_support: true`;
- `retained_outputs[0].reviewed_knowledge: true`;
- `retained_outputs[0].action_basis: true`;
- `retained_outputs[0].mainline_readiness: true`;
- `parser.truth_confidence: 0.91`;
- `router.truth_confidence: 0.91`;
- `source_card.evidence_support: true`;
- `candidate_distillation.reviewed_knowledge: true`;
- `anchors.page_refs[0].evidence_support: true`.

## Builder Repair

Builder repaired this inside the sandbox path by blocking direct authority field
names when they carry a truthy value or non-boolean value, while preserving
explicit negative boundary fields such as `promotion_ready: false`.

Added failure cases:

- `retained-output-direct-authority-field.json`;
- `parser-truth-confidence-direct-field.json`;
- `router-truth-confidence-direct-field.json`;
- `source-card-direct-evidence-support.json`;
- `candidate-direct-reviewed-knowledge.json`;
- `anchor-direct-evidence-support.json`.

Post-repair local verification:

```text
positive_fixtures: 4
failure_cases: 36
passed: true
failures: []
```

Reviewer must recheck this repair before Product Acceptance.

## Boundary Repair After Reviewer Recheck

Reviewer rechecked the direct-field repair and returned:

```text
REVIEW_PASS_NO_BLOCKER
```

Boundary Auditor later found that the direct field `promotion: true` was still
not covered. Builder added `promotion` to the direct authority denylist and added
`promotion-direct-authority-field.json`.

Post-boundary-repair local verification:

```text
positive_fixtures: 4
failure_cases: 37
passed: true
failures: []
```

Reviewer must recheck after this boundary repair before Product Acceptance.

## Final Recheck Evidence

Reviewer completed the final read-only recheck after the `promotion: true`
repair.

Observed verification:

```text
positive_fixtures: 4
failure_cases: 37
passed: true
failures: []
target __pycache__: 0
```

Reviewer confirmed:

- `promotion: true` is blocked by `RP_AUTHORITY_CLAIM_FORBIDDEN`;
- retained output direct authority fields are blocked;
- parser/router `truth_confidence` direct fields are blocked;
- source-card, candidate, and anchor direct authority fields are blocked;
- 4/4 positive fixtures remain valid.

No new blocker, missing key test, overdesign issue, or maintainability blocker
was found.
