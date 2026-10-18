---
type: sandbox_final_report
status: completed_with_external_blind_review_caveat
created_at: 2026-06-06
truth_boundary: sandbox report only; not reviewed knowledge; not architecture decision; not action basis
---

# Project Overlay Lightweight Landing Test

## One Sentence

Pro's recommendation has been landed in sandbox as a lightweight operating
pattern:

```text
one project borrowing list
minimal fields
no mainline expansion
no object model
action-facing use returns to v0.2.13
```

In plain Chinese:

```text
保留小便签，不再造新系统。
```

## What Changed Compared With The Prior Seven-Candidate Test

The earlier test used heavier candidate language:

```text
Project Lens
YAML-style entries
reason_1liner
manual target status
park
snapshot language
retrieval priority / precedence mechanism
```

This landing removes or downgrades those:

```text
Project Overlay / borrowing list
plain Markdown bullets
borrow_scope only
target_hint as raw navigation only
defer instead of park
candidate experience / boundary notes only when scoped
plain default read order sentence
```

## What Was Built

```text
outputs/review/project-overlay-lightweight-landing-test-2026-06-06/
```

Core files:

```text
protocol/PROJECT_OVERLAY_ONE_PAGE_PROTOCOL.md
project_overlays/MISA.md
project_overlays/VAKS.md
candidate_notes/experience/misa-runtime-memory-quarantine-no-effect-gate.md
candidate_notes/boundary/misa-retrieval-hints-not-control-authority.md
candidate_notes/boundary/misa-graph-carrier-not-controller.md
closeout/MISA-closeout-drain-note.md
checks/
```

## Quant Results

```text
Misa live overlay entries: 8
VAKS live overlay entries: 6
required field coverage: 100%
Misa target hints missing/weak: 0
strict live forbidden-language matches: 0
Misa tests passing: 25 / 25
mainline diff files: 0
staged files: 0
repeated full sandbox pass: pass
```

## Functional Verdict

The useful function survived:

- A project can see which reusable knowledge points are relevant.
- A project can see what to borrow and what not to mis-borrow.
- Codex can jump from `kp_ref` to project targets without tagging the knowledge
  point itself.
- Closeout can drain live entries.
- Archive/tombstone behavior stays out of default retrieval.
- Action-facing use still switches to v0.2.13.

The heavy system did not survive:

- No formal object model.
- No field contract.
- No lifecycle state machine.
- No formal workspace directory.
- No constant snapshot production.
- No retrieval authority mechanism.
- No schema, review queue, template, or mainline architecture expansion.

## Mainline Verdict

No new mainline change is needed now.

The current mainline already has the two minimum principles:

```text
generic project-scoped sidecar overlay boundary principle
v0.2.13 action-facing warrant gate
```

The lightweight overlay mode should stay in sandbox until a real blind
non-author pass shows low confusion risk.

## Remaining Caveat

The blind non-author pass in this package is simulated. It is useful as a
preflight, but it does not replace another model/window/person reading the
lightweight overlay without prior context.

This caveat does not block the sandbox landing. It blocks only future mainline
promotion.

## Next Best Test

Give another window or reviewer only:

```text
protocol/PROJECT_OVERLAY_ONE_PAGE_PROTOCOL.md
project_overlays/MISA.md
```

Ask whether it mistakes the overlay for truth, ADR, action basis, or project
approval. If confusion remains low, the light mode is stronger. If confusion is
high, keep reducing wording and fields.
