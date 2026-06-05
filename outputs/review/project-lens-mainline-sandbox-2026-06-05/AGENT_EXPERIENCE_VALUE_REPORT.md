---
type: agent_experience_value_report
status: completed
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-agent-maintenance-experience
truth_boundary: sandbox experience report only; not reviewed knowledge; not mainline architecture
---

# Agent Experience Value Report

## What Got Better

### 1. Block Entries Are Better Than Tables

For me, this is clearly better.

Why:

```text
I can grep `Lens Entry`.
I can read one knowledge point without horizontal scanning.
I can patch one block without touching unrelated rows.
Long `reason_1liner` and target hints do not break table readability.
```

Value:

```text
high
```

### 2. Structured `target_hint` Is Better Than String Hints

For me, this is also better.

Why:

```text
type tells me how to inspect the target.
value gives the locator.
status tells me whether the locator has been checked.
anchor_version tells me why/when it was considered valid.
```

This is more useful than renaming the field to `code_anchor`, because not all targets are code.

Value:

```text
high
```

### 3. Core / Lens / Snapshot Language Helps Recovery

This is valuable as vocabulary.

Why:

```text
It tells me which file class I should trust for which job.
Core is not project fit.
Lens is not decision.
Snapshot is not a live hunch.
```

Value:

```text
high_as_language
low_as_folder_change_now
```

### 4. `kp_ref` Makes The Sidecar Operational

This was the biggest improvement from the high-intensity run.

Why:

```text
kp_id tells me the idea.
kp_ref tells me where to click/read next.
```

With `kp_ref`, the recovery chain becomes:

```text
Lens Entry -> Candidate Pattern -> Derived From Sources -> raw source
```

Value:

```text
very_high
```

### 5. `conceptual` Is Cleaner Than Overloaded `not_checked`

The previous `not_checked` value mixed real unchecked anchors with conceptual workflow/module hints.

After the patch:

```text
healthy = concrete file/heading target checked
conceptual = useful workflow/module locator, not file-checkable yet
not_checked = should still be checked later
```

Value:

```text
high
```

## What Still Feels Awkward

### 1. `module:` and `workflow:` Targets Are Still Conceptual

Problem:

```text
I can read them, but I cannot verify them automatically yet.
```

Current mitigation:

```text
status: conceptual
anchor_version: conceptual-module or workflow-name-only
```

Future improvement:

```text
Tiny registry only if repeated use proves module/workflow names drift.
```

### 2. Snapshot Layer Needed A Real Trial

Problem:

```text
Snapshot linkage was previously only described, not exercised.
```

Current mitigation now:

```text
Created 1 landed candidate and 3 boundary candidate snapshots in sandbox.
Linked 2 Lens entries through outcome_ref and validated the refs.
```

### 3. Knowledge Graph Lite Is Tempting But Dangerous

Problem:

```text
related_kp / depends_on / conflicts_with would be useful for navigation,
but if placed in Core it may look like reviewed relation.
```

Current mitigation:

```text
Use ordinary Markdown links in sandbox notes first.
No Core schema field now.
```

## My Current Preferred Design

```text
Main human/agent source:
  block-form Project Lens markdown sidecar

Optional future machine index:
  generated JSONL, not manually authored source of truth

Architecture vocabulary:
  Core / Lens / Snapshot

Agent-maintenance fields:
  kp_ref
  structured target_hint
  conceptual target status
  outcome_ref to candidate snapshots

Do not add yet:
  formal folders
  graph runtime
  pipeline templates
  governance automation
```

## Final Value Judgment

```yaml
grok_three_layer_model: keep_as_sandbox_vocabulary
grok_code_anchor: absorb_as_structured_target_hint
grok_graph_lite: defer
grok_warrant_pipeline: defer
grok_governance: defer
grok_integrations: defer
kp_ref: keep
conceptual_target_status: keep
snapshot_trial: pass
overall_value: very_high_if_kept_light
blocking_issue_remaining: none_found_in_current_sandbox
mainline_merge_without_user_approval: no
```
