---
type: candidate_patch_test
status: candidate
created_at: 2026-06-05
project: verified-action-knowledge-system
version_under_test: v0.2.13
patch_under_test: v0-2-13-structured-action-basis-envelope
test_method: manual_architecture_trial
source_basis:
  - outputs/review/2026-06-05-v0-2-13-structured-action-basis-envelope-candidate-patch.md
  - outputs/review/2026-06-05-v0-2-12-gsn-assurance-case-cluster-deep-read.md
  - outputs/review/2026-06-05-cross-project-borrowing-v0-2-12-delta-test.md
truth_boundary: test output only, not reviewed knowledge
write_scope: outputs/review only
---

# v0.2.13 Structured Action-Basis Envelope Test

## 测试结论

v0.2.13 candidate passes the first restraint test.

它比 v0.2.12 多抓住一个关键问题：重要行动依据不能只有 evidence list，还要有 evidence-to-claim warrant。

它没有把 VAKS 推成完整 assurance-case 系统：

- no mandatory GSN diagram.
- no mandatory SACM model.
- no assurance-case tool adoption.
- no source-count truth confidence.
- no tool-count adoption evidence.
- no vendor-claim conformance validation.
- no burden on ordinary intake.

Result:

```text
v0.2.13 candidate is stronger than v0.2.12 for action-basis clarity.
Keep candidate-only until Pro review or a real action-basis example.
```

## Test Matrix

| Test | Input Pressure | Expected v0.2.13 Behavior | Result |
| --- | --- | --- | --- |
| T1 | GSN / CAE cluster says claims need evidence, context, strategy/warrant | Create a candidate `structured-action-basis-envelope` patch, not a GSN system | PASS |
| T2 | SCSC Tools and vendor pages list many assurance-case tools | Classify as `discovery-only`, no adoption judgment | PASS |
| T3 | Several GSN pages repeat similar claim/evidence/context ideas | Group as `source_family`, no fake independent support count | PASS |
| T4 | Important action claim has sources but no warrant | Mark incomplete / insufficient rather than action-ready | PASS |
| T5 | Ordinary source routing or light intake | Do not trigger the envelope | PASS |
| T6 | Well-formed diagram or confidence notation appears | Treat as communication/notation, not truth confidence | PASS |
| T7 | Existing v0.2.12 cross-project borrowing flow | Preserve Raw Source -> Routing Overlay -> Candidate Pattern Bank -> Ledger -> Review -> Action Basis | PASS |

## T1: GSN / CAE Cluster

### Input

The GSN / CAE / assurance case cluster repeatedly separates:

```text
claim
evidence
argument / strategy / warrant
context / assumptions
challenge / review
```

### v0.2.12 likely behavior

v0.2.12 already says Evidence-Aware Review and Action Basis should not treat evidence as automatic truth.

But it may still leave the final action basis as:

```text
claim + evidence + risk notes
```

without forcing the middle warrant to be visible.

### v0.2.13 behavior

v0.2.13 adds:

```text
argument_or_warrant
```

between evidence anchors and action-facing claim.

### Judgment

PASS.

This is a real improvement and does not require GSN diagrams.

## T2: Tool Directory / Vendor Pages

### Input

SCSC Tools, ASCE, AdvoCATE, NOR-STA, SafeTbox, Socrates, gsn2x, D-Case Editor, Astah System Safety, and similar pages show a tool ecosystem.

### v0.2.13 expected behavior

```text
classification: discovery-only
pattern_support: no
adoption_evidence: no
truth_confidence: no
action_readiness: no
```

### Judgment

PASS.

v0.2.13 keeps tools as discovery-only. It does not treat tooling maturity as a reason to implement assurance-case tooling in VAKS.

## T3: Repeated GSN Family Pages

### Input

Several SCSC/GSN pages discuss similar concepts:

```text
goal / claim
solution / evidence
strategy
context
assumption
justification
```

### Failure mode to catch

Counting each page as independent evidence:

```text
GSN page count = stronger truth support
```

### v0.2.13 expected behavior

```text
source_family_id: sf-assurance-case-notation
independent_support_count: not_increased_by_same_family_repetition
```

### Judgment

PASS.

v0.2.13 preserves v0.2.12 source-family restraint.

## T4: Missing Warrant

### Input

Hypothetical action-basis draft:

```yaml
action_or_decision_claim: VAKS should promote structured action-basis envelope to mainline now.
evidence_items_with_anchors:
  - SCSC GSN overview
  - OMG SACM page
  - CAE overview
argument_or_warrant:
context_scope_assumptions:
  - important VAKS decisions need reviewable support
challenges_counterevidence_known_gaps:
  - no real VAKS action-basis example has been tried yet
```

### v0.2.12 likely behavior

v0.2.12 might say:

```text
evidence exists, but keep candidate-only
```

### v0.2.13 behavior

v0.2.13 should say:

```yaml
status: insufficient
reason: missing_argument_or_warrant
allowed_next_step: candidate patch/test only
blocked_next_step: mainline promotion
```

### Judgment

PASS.

This is the strongest added value: v0.2.13 catches a missing middle step.

## T5: Ordinary Intake Should Stay Light

### Input

A normal new article/repo/video arrives and needs only source routing:

```text
raw source -> routing overlay -> candidate comprehension
```

### Failure mode to catch

Forcing every source card to carry a full claim-argument-evidence envelope.

### v0.2.13 expected behavior

```text
trigger_envelope: no
reason: ordinary intake, no promotion/action-basis use yet
```

### Judgment

PASS.

v0.2.13 does not burden ordinary capture or ordinary query.

## T6: Diagram / Confidence Notation

### Input

A source shows a clean GSN diagram or a confidence label.

### Failure mode to catch

```text
well-formed diagram -> stronger truth confidence
confidence notation -> reviewed confidence
```

### v0.2.13 expected behavior

```text
diagram: communication aid
confidence_notation: source claim or notation
truth_confidence_delta: none
required_support: point-specific reviewed evidence
```

### Judgment

PASS.

v0.2.13 keeps notation separate from truth confidence.

## T7: Existing v0.2.12 Flow Compatibility

### Input

Existing candidate-only borrowing flow:

```text
Raw Source
-> Source Routing Overlay
-> Candidate Pattern Bank
-> Project Borrowing Ledger
-> Evidence-Aware Review / EtD-lite
-> Decision / Action Basis
```

### v0.2.13 expected behavior

Do not insert a mandatory new stage into all intake.

Only add the envelope inside the last area when action-basis triggers exist:

```text
Decision / Action Basis
-> Structured Action-Basis Envelope, only when triggered
```

### Judgment

PASS.

v0.2.13 is compatible with v0.2.12.

## Regression Checks

| Boundary | v0.2.13 Result |
| --- | --- |
| URL/source remains provenance | PASS |
| raw text remains source text | PASS |
| AI summary remains candidate comprehension | PASS |
| candidate point remains review unit | PASS |
| retrieval/context-pack remains activation/context preparation | PASS |
| feedback does not mutate truth | PASS |
| tool page remains discovery-only | PASS |
| source family repetition does not increase truth confidence | PASS |
| action basis requires evidence-aware review | PASS |
| missing warrant blocks action-ready status | PASS |

## Failure Found

No blocking failure found in the manual trial.

Residual caution:

```text
The patch is still unproven on a real VAKS action-basis example.
```

## Recommendation

Promote within candidate-only outputs:

```text
v0.2.13 candidate = accepted for further testing
```

Do not promote to mainline yet.

Next best test:

```text
Pick one real VAKS decision/action-basis example and force it through the envelope.
If the envelope improves clarity without creating process drag, consider Pro review.
```
