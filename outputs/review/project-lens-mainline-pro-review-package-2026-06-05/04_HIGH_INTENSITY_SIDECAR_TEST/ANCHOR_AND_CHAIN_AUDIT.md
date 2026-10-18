---
type: anchor_and_chain_audit
status: pass_after_patches
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-anchor-source-chain
truth_boundary: sandbox audit only; not reviewed knowledge; not mainline architecture
---

# Anchor And Chain Audit

## Purpose

Test whether Project Lens is actually useful for an agent that needs to move through the knowledge system without chat memory.

Target chain:

```text
Source Routing
-> Candidate Pattern
-> Project Lens
-> target_hint / outcome_ref
-> Snapshot when applicable
```

## Checks

### 1. Project Lens Entry Integrity

```text
lens_entries=10
missing_kp_ref=0
missing_kp_ref_file=0
bad_stance=0
bad_target_status=0
doc_targets=3
doc_missing=0
heading_missing=0
code_anchor_field=false
```

Result:

```text
pass
```

### 2. Candidate Pattern Source Chain

```text
candidate_pattern_files=10
derived_source_refs=42
missing_source_refs=0
```

Result:

```text
pass
```

### 3. Source Routing To Pattern Routes

Before patch:

```text
unique_routes=11
known_patterns=10
missing_routes=1
missing_route=agent-memory-quarantine
```

Patch:

```text
agent-memory-quarantine -> memory-granularity-and-quarantine
```

After patch:

```text
unique_routes=10
known_patterns=10
missing_routes=0
```

Result:

```text
pass_after_patch
```

### 4. Source Routing Raw Source Paths

```text
routing_sources=25
missing_sources=0
```

Result:

```text
pass
```

### 5. Candidate Pattern To Lens Coverage

```text
candidate_patterns=10
lens_entries=10
patterns_missing_lens=0
lens_missing_pattern=0
```

Result:

```text
pass
```

### 6. Outcome Ref Resolution

```text
lens_entries=10
outcome_refs=2
missing_outcome_refs=0
```

Linked outcome refs:

```text
retrieval-is-activation-not-truth -> snapshots/boundary/retrieval-score-is-not-support.md
graph-and-ontology-as-candidate-context -> snapshots/boundary/graph-lite-core-pollution.md
```

Result:

```text
pass
```

## Findings

### F1. `kp_id` Alone Was Too Weak

Without `kp_ref`, an agent had to infer or search for the candidate knowledge point file.

Patch:

```text
Add kp_ref to each Lens Entry.
```

### F2. `not_checked` Was Overloaded

`not_checked` mixed real unchecked anchors with conceptual workflow/module hints.

Patch:

```text
Add status: conceptual for module/workflow hints that are useful but not file-checkable.
```

### F3. Source Routing Had One Broken Pattern Route

`agent-memory-quarantine` was referenced but did not exist as a candidate pattern file.

Patch:

```text
Replace with memory-granularity-and-quarantine.
```

### F4. Repeated YAML Keys Are Patch-Risky

When editing repeated `outcome_ref` fields, a naive patch can hit the wrong Lens Entry.

Mitigation:

```text
Patch with `### Lens Entry: <id>` block context.
Validate outcome_ref resolution after every batch edit.
```

### F5. Regex Must Be Line-Bounded

Naive parsing like `outcome_ref:\s*(.*)` can consume the next line and misread `updated_at` as an outcome ref.

Mitigation:

```text
Use line-bounded parsing such as `^outcome_ref:[ \t]*([^\r\n]*)$`.
```

## Agent Experience Verdict

```yaml
chain_recoverability: high_after_kp_ref
anchor_semantics: high_after_conceptual_status
source_to_pattern_to_lens: pass_after_route_patch
snapshot_linkage: pass
automation_risk: manageable_with_block_context_and_line_bounded_parsing
blocking_issue_remaining: none_found_in_current_sandbox
```

