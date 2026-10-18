---
slice_id: 2026-06-19-p2-84-post-rehearsal-cockpit-mutation-hardening-sandbox
status: source_map_defined
---

# Source Map

## Inputs

- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox/artifact/post_rehearsal_goal_state_cockpit.json`
- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox/failure-cases/post-rehearsal-goal-state-cockpit-failures.json`
- `outputs/review/vaks-implementation-sandbox/2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox/product-acceptance-report.md`

## Output Contract

p2-84 is a mutation-hardening artifact only. It can copy p2-83 JSON into fixtures and mutate those copies inside this slice. It must not edit p2-83, old slices, main architecture docs, templates, tools, wiki truth layers, or Obsidian.

## Reuse Value

Future agents can use the p2-84 mutation report to distinguish:

- cockpit baseline passes
- all-done overclaim fails
- generic continuation as approval fails
- p2-82 rehearsal as write authority fails
- missing byte evidence fails
- stale pre-p2-82 cockpit fails
- mainline authority confusion fails
- Product Acceptance as user approval fails
- path boundary confusion fails
