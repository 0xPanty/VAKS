---
type: next_window_memory_alignment
status: minimal_mainline_rule_landed_with_candidate_validations
created_at: 2026-06-05
scope: v0.2.13-revised-make-action-support-visible
project: verified-action-knowledge-system
formalization_status: minimal mainline wording landed; validations remain candidate-only
truth_boundary: recovery alignment only; not reviewed knowledge; not release tag; not action basis
write_scope: outputs/review only
---

# v0.2.13 Revised Next Window Memory Alignment

## Current State

Current working version:

```text
VAKS v0.2.13 minimal mainline rule + Pro accept_minimal wording patch + pre-commit micro-test
```

Mainline architecture now includes the minimal action-support visibility wording in:

```text
FUSION_ARCHITECTURE_V0_2_DRAFT.md
ARCHITECTURE_PRINCIPLES.md
```

This is still not a full assurance-case system, schema change, template change, candidate pattern, or release tag.

Everything beyond the tiny rule remains candidate-only in `outputs/review`.

Project Lens update:

```text
Project Lens remains candidate-only, but the candidate sidecar has now passed high-intensity agent-maintenance testing after patches.
It added kp_ref, conceptual target status, and candidate snapshot trials.
It did not change SCHEMA.md, REVIEW_QUEUE.md, templates, or mainline architecture wording.
```

## Pro Review Outcome

Pro verdict:

```text
revise_candidate
```

Meaning:

```text
keep the direction
narrow the trigger
reduce the mandatory fields
make warrant non-circular
do not create a pattern file now
if promoted later, only as a sentence-level minimal rule plus guardrail
test no-upgrade and real promotion before expanding
```

Current status against that advice:

```text
minimal sentence-level rule: landed
companion guardrail: landed
Pro second review: accept_minimal
Pro wording patch: applied
pre-commit micro-test: pass_with_caveats
candidate pattern file: no
schema/template/directory expansion: no
no-upgrade validation: passed
dual-project reuse validation: passed
real promotion validation: passed for keeping the minimal rule only
```

## Revised v0.2.13 Rule

Use this as the current minimal mainline wording intent:

```text
For action_basis and significant promotion/decision use, when an answer or claim
will be relied on for action or risk-sensitive judgment, make the support visible:
state the action-facing claim, the point-specific anchored evidence, the non-circular
warrant connecting that evidence to the claim, the relevant scope/assumptions,
the known challenges or gaps, and the current residual review status.
Diagrams, notation, source counts, tool counts, vendor pages, and confidence labels
do not increase support, independence, or action readiness.
```

Short version:

```text
Evidence is not enough; show the non-circular warrant.
```

## Narrowed Triggers

Trigger only for:

- action_basis use.
- significant promotion.
- significant decision.
- risk-sensitive answer relied on for action.
- explicit "is this enough?" only when enough means enough for action/promotion/decision/risk-sensitive use.
- strong relation only when relation promotion or action-critical relation judgment is involved.

Do not trigger for:

- ordinary intake.
- ordinary source routing.
- ordinary search.
- simple summary.
- tool-directory triage.
- candidate-only scratch note.
- non-action-facing reviewer question.

## Core Fields

Core when triggered:

```text
action-facing claim
point-specific anchored evidence
non-circular warrant
scope / assumptions
known challenges / gaps
current residual review status
```

Guardrails when relevant, not mandatory fields:

```text
source-family duplicate warning
excluded non-support warning
tool/vendor/diagram/source-count/confidence-label lint
```

## Current Test Status

Revised manual boundary trial:

```text
passed
```

Pressure testing:

```text
manual adversarial pressure test: passed, no blocking design failure found
meta real action-basis trial: passed for candidate-only continuation
non-meta action-basis trials: passed for distinguishing candidate review from premature action
dual-project reuse validation: passed
no-upgrade validation: passed
real promotion validation: passed for keeping the minimal mainline rule only
```

Still true:

```text
long-run repeated-use evidence: not available
ordinary intake unaffected over time: intended and pressure-tested, not proven as a general fact
expansion readiness: no
candidate pattern readiness: no
stable workspace / directory migration readiness: no
```

## Files To Read First

Next window should read:

1. `AGENTS.md`
2. `git status --short --branch --untracked-files=all`
3. `00_handoff/2026-06-05-vaks-v0-2-13-action-support-visibility-handoff.md`
4. `outputs/review/2026-06-05-v0-2-13-pro-review-response-revise-candidate.md`
5. `outputs/review/2026-06-05-v0-2-13-structured-action-basis-envelope-revised-candidate-patch.md`
6. `outputs/review/2026-06-05-v0-2-13-structured-action-basis-envelope-revised-test.md`
7. `outputs/review/2026-06-05-v0-2-13-revised-pressure-test-suite.md`
8. `outputs/review/2026-06-05-v0-2-13-revised-real-action-basis-trial.md`
9. `outputs/review/2026-06-05-v0-2-13-revised-nonmeta-action-basis-trials.md`
10. `outputs/review/2026-06-05-v0-2-13-light-medium-heavy-alignment.md`
11. `outputs/review/2026-06-05-v0-2-13-dual-project-reuse-validation.md`
12. `outputs/review/2026-06-05-v0-2-13-no-upgrade-validation.md`
13. `outputs/review/2026-06-05-v0-2-13-real-promotion-validation.md`
14. `outputs/review/2026-06-05-v0-2-13-landed-rule-operational-test.md`
15. `outputs/review/2026-06-05-v0-2-13-pre-commit-micro-test.md`
16. `outputs/review/2026-06-05-v0-2-13-accept-minimal-closeout.md`
17. `outputs/review/2026-06-05-v0-2-13-development-borrowing-tags-knowledge-flywheel-note.md`
18. `outputs/review/2026-06-05-v0-2-13-development-borrowing-tags-pro-research-prompt.md`
19. `outputs/review/2026-06-05-v0-2-13-project-lens-pro-response-landing.md`
20. `outputs/review/project_lens_overlays/VAKS.md`
21. `outputs/review/project_borrowing_ledgers/VAKS.md`
22. `outputs/review/2026-06-05-v0-2-13-usage-guide.md`
23. `outputs/review/project-lens-mainline-sandbox-2026-06-05/HIGH_INTENSITY_GAUNTLET.md`
24. `outputs/review/project-lens-mainline-sandbox-2026-06-05/ANCHOR_AND_CHAIN_AUDIT.md`
25. `outputs/review/project-lens-mainline-sandbox-2026-06-05/SNAPSHOT_TRIALS.md`
26. `outputs/review/project-lens-mainline-sandbox-2026-06-05/PRESSURE_TEST_REPORT.md`
27. `outputs/review/project-lens-full-mainline-copy-test-2026-06-05/README.md`
28. `outputs/review/project-lens-full-mainline-copy-test-2026-06-05/FULL_MAINLINE_COPY_INSERTION_TEST_REPORT.md`
29. `outputs/review/project-lens-full-mainline-copy-test-2026-06-05/COMPLETION_AUDIT.md`
30. `outputs/review/2026-06-05-v0-2-13-main-architecture-obsidian-test.md`
31. `outputs/review/v0-2-13-expansion-sandbox-2026-06-05/00_README.md`
32. `outputs/review/v0-2-13-expansion-sandbox-2026-06-05/SANDBOX_TEST_REPORT.md`
33. `outputs/review/2026-06-05-v0-2-13-next-window-memory-alignment.md`
34. `outputs/review/2026-06-05-v0-2-12-gsn-assurance-case-cluster-deep-read.md`

Read older v0.2.12 files only if needed for comparison.

Do not proactively inventory all old intake files.

## Current Disposition After Pressure Testing

```text
minimal_mainline_rule: landed_and_keep_for_now
Pro_second_review: accept_minimal
Pro_wording_patch: applied
candidate_validation_history: keep
landed_rule_operational_test: passed
expansion_sandbox_test: completed
pre_commit_micro_test: pass_with_caveats
accept_minimal_closeout: ready_for_scoped_commit_if_requested
project_lens_candidate_sidecar: pass_after_patches
project_lens_high_intensity_gauntlet: completed
project_lens_blocking_issue_remaining: none_found_in_current_sandbox
project_lens_full_mainline_copy_insertion_test: pass_as_full_copy_sandbox
project_lens_mainline_merge_without_user_approval: no
revise_again_now: no
create_candidate_pattern: no
expand_to_schema_or_template: no
stable_workspace_migration: no
template_change: no
```

Expansion sandbox verdict:

```text
new schema: reject_for_now
new template: keep_sandboxed
formal development workspace directory: keep_sandboxed
new pattern: reject_for_now
GSN / SACM system: reject_for_now
tool adoption: reject_for_now
all intake heavier: reject_for_now
```

Pro package prepared:

```text
outputs/review/v0-2-13-mainline-and-expansion-pro-review-package-2026-06-05/
outputs/review/v0-2-13-mainline-and-expansion-pro-review-package-2026-06-05.zip
```

## Pro Result After Closeout

The user clarified that "开发区 / Project Borrowing Ledger" should be understood as a knowledge-flywheel mechanism, not a formal folder or decision ledger. Pro then reviewed the idea and returned:

```text
Verdict: accept_direction
Best name: Project Lens
Storage: project-scoped sidecar overlay
```

```text
external references
-> AI-distilled generic knowledge points
-> Project Lens sidecar beside relevant points
-> project validation / adoption / failure
-> project-end landed_snapshot / boundary_snapshot
-> stronger future reuse and warning signals
```

Plain version:

```text
Generic knowledge points stay independent and reusable.
The current project only adds a temporary sidecar lens:
- possible borrow scope
- non-borrow scope when needed
- target_hint
- reason_1liner
- stance: watch / partial / avoid / park
- outcome_ref only after real landed or boundary snapshot
```

This is not:

```text
reviewed knowledge
ADR
truth layer
action basis
schema
template
permanent project status
```

Relationship to v0.2.13:

```text
Project Lens helps select and digest reusable knowledge during development
v0.2.13 checks a lens item only when it is about to become action-facing use / decision / promotion
landed_snapshot may later become architecture pattern / experience guide
boundary_snapshot may later become negative knowledge / project boundary / warning rule
```

Candidate-only landing now present:

```text
outputs/review/2026-06-05-v0-2-13-project-lens-pro-response-landing.md
outputs/review/project_lens_overlays/VAKS.md
outputs/review/project_borrowing_ledgers/VAKS.md
outputs/review/project-lens-mainline-sandbox-2026-06-05/PRESSURE_TEST_REPORT.md
outputs/review/project-lens-mainline-sandbox-2026-06-05/REAL_CASE_TRIALS.md
outputs/review/project-lens-mainline-sandbox-2026-06-05/GROK_RECOMMENDATION_TRIAGE.md
outputs/review/project-lens-mainline-sandbox-2026-06-05/THREE_LAYER_ARCHITECTURE_CANDIDATE.md
outputs/review/project-lens-mainline-sandbox-2026-06-05/AGENT_EXPERIENCE_VALUE_REPORT.md
outputs/review/project-lens-mainline-sandbox-2026-06-05/HIGH_INTENSITY_GAUNTLET.md
outputs/review/project-lens-mainline-sandbox-2026-06-05/ANCHOR_AND_CHAIN_AUDIT.md
outputs/review/project-lens-mainline-sandbox-2026-06-05/SNAPSHOT_TRIALS.md
```

Sandbox verdict:

```text
Project Lens sidecar block format: pass
structured target_hint: pass
kp_ref: pass
conceptual target status: pass
Core / Lens / Snapshot vocabulary: useful but sandbox-only
Obsidian sandbox isolation: pass
mainline integration without user approval: blocked
overall: pass_after_patches
blocking issue remaining in candidate sidecar: none found in current sandbox
```

Read:

```text
outputs/review/2026-06-05-v0-2-13-development-borrowing-tags-knowledge-flywheel-note.md
outputs/review/2026-06-05-v0-2-13-development-borrowing-tags-pro-research-prompt.md
outputs/review/2026-06-05-v0-2-13-project-lens-pro-response-landing.md
outputs/review/project_lens_overlays/VAKS.md
```

The strongest remaining possible improvement is operational, not architectural:

```text
If future use is inconsistent, create a tiny warrant-quality checklist later.
Do not create it now.
```

## Next Required Work

Next useful work is not more abstract promotion. Pick one ordinary-to-medium example and one heavy example:

```text
ordinary source / routing item that should not upgrade
real VAKS action-basis / important promotion / risk-sensitive answer
```

Run the revised rule against it.

Pass condition:

```text
It makes claim, anchored evidence, non-circular warrant, scope, challenges,
and residual status clearer without pulling ordinary intake/routing into a
heavy workflow.
```

Fail condition:

```text
It becomes a new object/template/system,
or allows notation/tooling/source-count to stand in for support.
```

## Hard Boundaries

Do not:

- modify `SCHEMA.md`, `REVIEW_QUEUE.md`, or templates without explicit promotion work.
- expand `ARCHITECTURE_PRINCIPLES.md` beyond the already-landed minimal rule without explicit promotion work.
- create a candidate pattern file yet.
- call the wider workspace/directory/template plan accepted or validated.
- claim ordinary intake is proven unaffected.
- commit / push unless explicitly asked.
