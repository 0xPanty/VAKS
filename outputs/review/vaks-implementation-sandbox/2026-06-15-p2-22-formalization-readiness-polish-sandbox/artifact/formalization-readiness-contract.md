# Formalization Readiness Contract

## Input Contract

- P2-21 sandbox workbench reports and prototype.
- No formal vault content as an input.
- No runtime service, dependency install, sync, commit, push, or promotion.

## Output Contract

- A sandbox-only pilot pack under this slice.
- A decision matrix for the future real Obsidian workbench route.
- A first-run script, daily operator flow, receipt inspector, acceptance gates,
  boundary FAQ, reviewer packet, and rollout backlog.
- A receipt that records the source slice and confirms no forbidden operation.

## Product Surfaces

- `pilot_home`: Pilot Home - navigation is not authority
- `first_run_script`: First Run Script - trial does not mean adoption
- `daily_operator_flow`: Daily Operator Flow - triage is not review approval
- `receipt_inspector`: Receipt Inspector - receipt is not evidence support
- `triage_dirty_state_panel`: Triage and Dirty-State Panel - state grouping is not approval
- `formalization_decision_matrix`: Formalization Decision Matrix - decision matrix is not a merge approval
- `acceptance_gates`: Acceptance Gates - gate pass is not mainline approval
- `boundary_faq`: Boundary FAQ - FAQ prevents authority confusion
- `reviewer_packet`: Reviewer Packet - reviewer pass is not Product Acceptance
- `failure_messages`: Failure Messages - block reason is not a truth judgment
- `formalization_readiness_packet`: Formalization Readiness Packet - readiness packet is not permission to execute
- `rollout_backlog`: Rollout Backlog - backlog item is not approval to execute

## Formalization Options

- `static_html_cockpit`: Keep static HTML cockpit as inspection surface / boundary: inspection surface only
- `obsidian_native_markdown_bases`: Translate to Obsidian-native Markdown and Bases / boundary: not executed here
- `local_read_only_sidecar`: Build a local read-only sidecar / boundary: read-only only
- `hybrid_pilot_path`: Hybrid: native Markdown entry plus static inspector plus read-only validator / boundary: recommended candidate, not approval

## Product Promise

The user should be able to answer these without reading the full architecture:

- Where do I start?
- What is the current status?
- Which receipt or report proves the process trail?
- Which route is recommended next?
- What is still forbidden?

## Boundary Promise

This pack is sandbox only, not reviewed knowledge, not evidence support, not
action basis, and does not approve. It cannot merge, sync, commit, push, promote,
write the formal vault, create real Bases, or authorize an action.
