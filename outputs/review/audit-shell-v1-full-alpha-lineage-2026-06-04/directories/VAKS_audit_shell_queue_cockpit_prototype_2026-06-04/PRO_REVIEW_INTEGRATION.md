# Pro Review Integration

## What Pro Changed

Pro did not reject audit shell v1.

Pro changed the landing target:

```text
from card-first audit shell
to queue-first risk-tiered review cockpit
```

## Keep

- `shell_core` five states.
- ordinary / for_review / blocking / resolved_folded / regressed semantics.
- internal landing class discipline.
- source / record / evidence / transcript / handoff jump-back.
- video / ASR / transcript / metadata split.
- authority lint as guardrail only.
- feedback strip as wording guardrail only.
- dashboard/test/lint/count/lineage as diagnostic only.

## Change

- Do not expose full landing taxonomy on every row.
- Use anchor-strength strip on the front face.
- Upgrade pointer design toward selector-grade anchors.
- Make queue-first cockpit the main operator surface.
- Split `for_review` into `review_now` and `deferred_review_unless_promoted`.
- Make card only a renderer/pane, not the primary unit.

## Remove From Default

- recurrence/grouping default-on.
- numeric support score.
- fake precision confidence.
- authority lint as semantic proof.

## Next Step

Run operator-only sandbox pilot:

```text
1. operator triage pilot over 80 rows
2. semantic click-back pilot over 60 rows
3. source-family independence trap over 60 rows
```

Only after this should VAKS consider moving beyond candidate convention.

