---
type: sandbox_check
status: pass
created_at: 2026-06-07
scope: source-intake-routing workbench hardening v0.1
truth_boundary: sandbox test evidence only; not reviewed knowledge; not action basis
action_basis_allowed: false
truth_mutation_allowed: false
---

# Source Intake Routing Workbench Hardening v0.1 Test

## Question

Did the workbench move from "findable" to a safer, more usable retrieval
operating surface?

## What Changed

```text
query intent router added
natural question -> mode routing added to context pack builder
lane-internal ranking added
selector/snippet v0 added
action mode renamed raw/reviewed/mainline results as anchor_queue roles
context-pack lint now catches empty selector and missing snippet boundary
```

## Router Test

```text
source-inspection query:
  expected=source-inspection
  actual=source-inspection
  pass=true

research query:
  expected=research
  actual=research
  pass=true

action query:
  expected=action
  actual=action
  pass=true

audit query:
  expected=audit
  actual=audit
  pass=true

project-exploration query:
  expected=project-exploration
  actual=project-exploration
  pass=true
```

Regression caught:

```text
"why are candidate and overlay excluded from action mode" initially routed to
action because it contained the word action. The router now gives audit intent
priority when why/excluded/guardrail/check/test language is present.
```

## Generated Pack Matrix

```text
source-intake-routing-workbench-pack-action-generated.md:
  mode=action
  selected=29
  empty_selector=0

source-intake-routing-workbench-pack-query-action-generated.md:
  mode=action
  selected=29
  empty_selector=0

source-intake-routing-workbench-pack-query-audit-generated.md:
  mode=audit
  selected=13
  empty_selector=0

source-intake-routing-workbench-pack-query-project-exploration-generated.md:
  mode=project-exploration
  selected=31
  empty_selector=0

source-intake-routing-workbench-pack-query-research-generated.md:
  mode=research
  selected=44
  empty_selector=0

source-intake-routing-workbench-pack-query-source-inspection-generated.md:
  mode=source-inspection
  selected=20
  empty_selector=0

source-intake-routing-workbench-pack-research-generated.md:
  mode=research
  selected=52
  empty_selector=0

source-intake-routing-workbench-pack-source-inspection-generated.md:
  mode=source-inspection
  selected=28
  empty_selector=0
```

## Action Pack Assertions

File:

```text
checks/source-intake-routing-workbench-pack-query-action-generated.md
```

Result:

```text
mode=action
items_candidate=false
items_overlay=false
action_basis_allowed_true=false
final_support_none=true
anchor_queue_present=true
mainline_anchor_roles=13
reviewed_anchor_roles=8
raw_anchor_roles=8
```

Interpretation:

```text
Action mode prepares a queue of possible anchors. It does not present raw,
reviewed, or mainline refs as final support. Candidate and overlay material are
not in default action items.
```

## Selector / Snippet Assertions

```text
all generated source-intake-routing packs:
  selector_or_offset_empty=0
  snippet_status=navigation_snippet_not_evidence present

meaning:
  selector/snippet helps navigation only
  selector/snippet is not evidence support
```

## Lint Matrix

```text
context-pack lint:
  files_checked=12
  pass=11
  expected_fail=1
  expected_fail_fixture=fixtures/usage-layer-bad-authority-leak.md

usage-layer lint:
  files_checked=73
  pass=72
  expected_fail=1
  expected_fail_fixture=fixtures/usage-layer-bad-authority-leak.md

intake-metadata lint:
  files_checked=10
  pass=7
  expected_fail=3
  expected_fail_fixtures:
    fixtures/intake-metadata-suggestion-bad-persistent.md
    fixtures/source-card-bad-prefill-authority.md
    fixtures/source-card-forbidden-authority-tags.md

kp lint:
  files_checked=3
  pass=2
  expected_fail=1
  expected_fail_fixture=fixtures/candidate-distillation-bad-kp.md
```

## Boundary Check

```text
truth_layer_changed=false
mainline_changed=false
commit_created=false
action_basis_allowed=false
truth_mutation_allowed=false
```

The latest mainline commit remains:

```text
0cea747 docs: merge source intake control flow guardrails
```

## Verdict

```text
status=pass
landing_quality=usable_retrieval_workbench_v0_1
mainline_changed=false
```

This is still sandbox-only. It is not a production retrieval engine, not an
automatic evidence checker, and not a schema promotion.

