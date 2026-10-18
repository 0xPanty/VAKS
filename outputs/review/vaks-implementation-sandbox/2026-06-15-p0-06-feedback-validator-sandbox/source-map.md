---
record_kind: sandbox_source_map
slice_id: 2026-06-15-p0-06-feedback-validator-sandbox
truth_boundary: source_map_for_sandbox_only
---

# Source Map

## Upgrade Plan

- `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md:629-639`
  defines the feedback validator: positive feedback is weak, negative feedback
  creates review pressure, explicit correction creates `review_due`, and
  feedback cannot change truth confidence, verification status, source
  reliability, or reviewed notes/relations directly.
- `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md:2232-2246`
  defines the P0-06 implementation sequence and must-block list.
- `outputs/review/vaks-architecture-upgrade-plan-2026-06-13.md:2258-2265`
  includes the failure matrix overlap: `AB-06 feedback modifies
  truth_confidence`.

## Feedback Rules

- `FEEDBACK.md:53-70` states that feedback may adjust usefulness, scope fit,
  and activation ranking, but formal truth changes require review and
  promotion.
- `FEEDBACK.md:88-120` lists allowed direct feedback effects and forbidden
  direct effects: usefulness, scope fit, activation ranking, and review_due are
  allowed; truth confidence, verification status, source reliability, and
  decision outcome are not.
- `FEEDBACK.md:125-178` gives the feedback-event record shape with `affects`
  and `never_affects_directly`.
- `FEEDBACK.md:194-198` states relation feedback can change relation-path
  activation but not reviewed relation strength.
- `FEEDBACK.md:301-310` states explicit correction must create `review_due`.
- `FEEDBACK.md:321-358` states action/decision outcomes can calibrate future
  usefulness/scope/risk framing and create review_due, but cannot turn outcomes
  into truth or directly change verification/source reliability.
- `FEEDBACK.md:604-645` states feedback does not lower source reliability from
  one bad answer, does not make user preference truth, agent memory can create
  feedback-event records but cannot write reviewed truth, and explicit
  correction creates review_due.

## Local Boundary Rules

- `SOURCE_INTAKE.md:168-180` defines feedback-event retrieval policy:
  `action_basis_allowed: false`, `warning_code: feedback_not_truth`,
  forbidden truth mutation fields absent, no reviewed-note mutation, and no
  source-reliability mutation.
- `SOURCE_INTAKE.md:285-292` forbids fields such as `truth_confidence`,
  `confidence_delta`, and `action_basis_allowed: true` in feedback records.
- `SOURCE_INTAKE.md:1301-1320` repeats feedback-event shape and says the cache
  can warn the project immediately, but does not mutate truth.
- `SOURCE_INTAKE.md:1332-1337` requires every feedback event to bind to
  `project_ref` or `observed_in_context`, and forbids global negative knowledge
  from a local feedback event.
- `SOURCE_INTAKE.md:1390-1394` lists feedback failure modes:
  repeated negative feedback must create review pressure, and feedback must not
  directly mutate reviewed truth.
- `SOURCE_INTAKE.md:1455-1459` states feedback is scoped and append-only; it can
  affect activation and review pressure, but not truth confidence or reviewed
  notes without review.
- `REVIEW_QUEUE.md:504-507` states process/approval signals can create review
  pressure but not truth confidence or reviewed relations.
- `REVIEW_QUEUE.md:871-897` states stale/action failure creates review pressure,
  not automatic invalidity or rejection.

## Prior Slice Dependency

- `outputs/review/vaks-implementation-sandbox/2026-06-15-p0-05-action-readiness-validator-sandbox/product-acceptance-report.md`
  records `PASS_PRODUCT_GRADE` for P0-05. This P0-06 slice builds after that
  accepted sandbox boundary but does not promote it to mainline.

