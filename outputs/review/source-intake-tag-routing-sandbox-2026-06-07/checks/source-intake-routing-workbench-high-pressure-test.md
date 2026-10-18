---
type: sandbox_check
status: pass
created_at: 2026-06-07
scope: source-intake-routing workbench landing high-pressure test
truth_boundary: sandbox test evidence only; not reviewed knowledge; not action basis
action_basis_allowed: false
truth_mutation_allowed: false
---

# Source Intake Routing Workbench High-Pressure Test

## Question

Did the GitHub scout become a usable workbench path without weakening VAKS
authority boundaries?

## What Was Tested

```text
route map loads
workbench entrypoint exists
research pack generates
source-inspection pack generates
action pack generates
5 GitHub scout source cards are pinned into source-inspection pack
action mode excludes candidate/overlay/support-review output from default action inclusion
generated packs have no unrendered PowerShell interpolation
context-pack lint catches bad pack fixture
usage-layer lint accepts the new workbench entrypoint
truth layer remains untouched
```

## Generated Pack Results

```text
research pack:
  selected_count=52
  selected_by_lane:
    mainline_current=5
    reviewed_support=8
    raw_drilldown=13
    candidate_orientation=9
    active_project_overlay=9
    support_review_output=8

source-inspection pack:
  selected_count=28
  selected_by_lane:
    mainline_current=5
    raw_drilldown=13
    candidate_orientation=9
    active_project_overlay=1

action pack:
  selected_count=29
  selected_by_lane:
    mainline_current=13
    reviewed_support=8
    raw_drilldown=8
  action_readiness=not_ready
```

## Pinned Scout Source Cards

All 5 GitHub scout source cards appear in the generated source-inspection pack:

```text
raw\repos\2026-06-07-langgenius-dify-source.md
raw\repos\2026-06-07-infiniflow-ragflow-source.md
raw\repos\2026-06-07-mintplex-labs-anything-llm-source.md
raw\repos\2026-06-07-run-llama-llama-index-source.md
raw\repos\2026-06-07-deepset-ai-haystack-source.md
```

## Direct Assertions

```text
source_ref_present:langgenius-dify=true
source_ref_present:infiniflow-ragflow=true
source_ref_present:anything-llm=true
source_ref_present:llama-index=true
source_ref_present:haystack=true
route_front_door_present=true
all_five_route_cards_present=true
action_pack_no_candidate_items=true
action_pack_no_overlay_items=true
action_pack_no_action_basis_true=true
action_readiness_not_ready=true
no_unrendered_powershell=true
```

## Action Retrieval Smoke

Pattern:

```text
source-intake-routing|Dify|RAGFlow|AnythingLLM|LlamaIndex|Haystack|metadata|router|citation|ingestion|source route|action basis
```

Mode:

```text
action
```

Result:

```text
active_project_overlay: 24 total / 0 included_by_default
candidate_orientation: 34 total / 0 included_by_default
mainline_current: 37 total / 37 included_by_default
raw_drilldown: 89 total / 89 included_by_default
reviewed_support: 43 total / 43 included_by_default
support_review_output: 93 total / 0 included_by_default
```

Interpretation:

```text
The action retrieval mode still excludes candidate, overlay, and support-review
output by default. Raw drilldown can be prepared as an anchor queue, but final
action-facing support still requires opening/checking the raw or reviewed anchor.
```

## Lint Matrix

```text
context-pack lint:
  files_checked=7
  pass=6
  expected_fail=1
  expected_fail_fixture=fixtures/usage-layer-bad-authority-leak.md

usage-layer lint:
  files_checked=67
  pass=66
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

## Regression Caught And Fixed

```text
1. Builder Markdown table previously leaked unrendered PowerShell interpolation.
   Fixed and lint now catches this regression class.

2. Retrieval MVP previously applied Limit before lane classification, allowing
   outputs/ package noise to crowd out raw/repos source cards.
   Fixed by classifying first, then sorting by lane order.

3. Workbench entrypoint frontmatter initially missed default exclusion fields.
   Fixed so usage-layer lint accepts it.

4. mainline-candidate candidate-distillation template had duplicate KP example.
   Fixed to keep KP lint focused on the intended bad fixture.
```

## Truth-Layer Check

```text
git status --short -- SCHEMA.md ARCHITECTURE_PRINCIPLES.md FUSION_ARCHITECTURE_V0_2_DRAFT.md wiki/claims wiki/decisions wiki/patterns
```

Result:

```text
no output
```

Latest commit remains:

```text
0cea747 docs: merge source intake control flow guardrails
```

## Verdict

```text
status=pass
landing_quality=usable_sandbox_workbench
action_basis_allowed=false
truth_mutation_allowed=false
mainline_changed=false
commit_created=false
```

The landing is strong enough for GPT Pro review as a sandbox implementation.
It is still not a production builder or mainline schema change.
