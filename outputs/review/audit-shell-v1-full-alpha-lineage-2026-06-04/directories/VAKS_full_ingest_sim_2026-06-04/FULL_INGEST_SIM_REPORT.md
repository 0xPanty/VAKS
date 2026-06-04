# VAKS Audit Shell v1 Full Ingest Simulation

Date: 2026-06-04

Sandbox: `C:\Users\Administrator\Documents\VAKS_full_ingest_sim_2026-06-04`

Main vault: `C:\Users\Administrator\Documents\资料库` read-only

Package read: `C:\Users\Administrator\Documents\VAKS_800_independent_oracle_pilot_2026-06-01`

## What Was Tested

This run did not re-review the architecture and did not change the main vault. It simulated how Codex, as the background operator, would handle real local VAKS material if those records were entering or updating the vault.

The audit shell was applied as:

- `ordinary`: light save unless it becomes action basis or hits a hard trigger.
- `for_review`: route to unresolved review; do not treat as action-ready.
- `blocking`: open full audit before action; fix anchor, conflict, or action-basis problem first.
- `resolved_folded`: keep historical or completed material out of the default unresolved surface.
- `regressed`: reopen a previously settled or packaged item when it becomes stale, misleading, or contradicted.

The operator front face was tested for status, one-line summary, risk reason, anchor health, handling suggestion, targeted boundary reminder, and source-first drilldown.

## Sample Set

46 real local samples were selected across:

- `raw/articles`
- `raw/videos`
- `raw/repos`
- `wiki/claims`
- `wiki/patterns`
- `wiki/anti-patterns`
- `wiki/concepts`
- `wiki/decisions`
- `outputs/review`
- `outputs/feedback`
- `00_handoff`
- `templates`

The sample was intentionally dirty: video transcripts, missing source URL, binary repo snapshot, stale handoff, stale package manifest, dashboard/review outputs, feedback wording, draft templates, accepted claims, and review_due patterns were all included.

## Result Counts

| State | Count | Meaning in this run |
|---|---:|---|
| `ordinary` | 24 | Light operator handling was enough. |
| `for_review` | 16 | Needs review before promotion, action, or strong answer use. |
| `blocking` | 2 | Cannot be used until anchor or evidence drilldown is fixed. |
| `resolved_folded` | 3 | Historical or completed item should stay folded by default. |
| `regressed` | 1 | Previously packaged/current-looking item became stale enough to reopen. |

Immediate full audit opened for 19 of 46 samples. That number is intentionally high because this was a pressure sample, not a clean ordinary intake sample.

Ordinary material was not dragged into full audit: all 24 `ordinary` rows kept a light save or light operator reminder unless they later become action basis.

## Layer Findings

| Layer | Samples | Main outcome |
|---|---:|---|
| Raw articles | 4 | Clean source records stayed light; missing URL or drift-prone docs went to review. |
| Raw videos | 5 | Source cards and ASR metadata stayed raw; transcript-only action claims were blocked or reviewed. |
| Raw repos | 5 | Source records were usable; binary snapshot alone was not enough as evidence. |
| Claims | 3 | Accepted claims could stay readable, but high-impact schema claims need full audit before action. |
| Patterns | 6 | Draft, stale `next_review`, dashboard, and source-count risks were caught. |
| Anti-patterns | 4 | Active guardrails stayed light; draft high-severity rules stayed for review. |
| Concepts | 2 | Concepts stayed light and explanatory. |
| Decisions | 4 | Current decisions stayed light; v0.1 historical decision folded. |
| Review outputs | 5 | Completed review output stayed folded or light; stale package manifest regressed. |
| Feedback | 1 | Feedback wording was flagged because event records can be mistaken for truth changes. |
| Handoffs | 2 | Current handoff stayed light; old handoff folded. |
| Templates | 5 | Templates stayed light but needed clear template-not-record reminders. |

## Risk Pressure Results

### Ordinary material stayed light

Simple source records, concepts, templates, and current handoff material did not force full audit. The operator surface only needed a short status, anchor note, and handling suggestion.

This means audit shell v1 does not have to slow ordinary capture if the renderer keeps targeted reminders and does not print global disclaimers on every stable record.

### Action-bearing material opened full audit

Items that could affect answers, schema, operation conventions, action basis, or promotion were escalated. Examples:

- `wiki/claims/semantic-relation-strength-should-be-core-schema-field.md`
- `wiki/patterns/context-pack-evidence-envelope.md`
- `outputs/review/2026-05-30-rka-evidence-packet-source-record-trial.md`
- `outputs/review/2026-05-30-thirdspace-dashboard-vault-health-panel-alpha.md`

The useful part is not the label. The useful part is that the operator sees the next action immediately: review, full audit, or do not use as action basis yet.

### Weak or missing anchors were caught

The shell caught three important anchor classes:

- Missing or weak source URL: `raw/articles/2026-05-27-automated-obsidian-daily-brief-source.md`
- Transcript-only without precise evidence use: `raw/videos/2026-06-04-youtube-hermes-obsidian-source/transcript.txt`
- Binary snapshot as direct evidence: `raw/repos/_snapshots/openkb-main-2026-05-27.zip`

This is one of the clearest wins. Without the operator surface, these can look like usable material because the files exist. With the shell, existence is separated from support.

### Video and ASR stayed out of reviewed knowledge

Video cards, transcript metadata, segments, and flat transcript text were treated as raw source artifacts. The simulation did not let ASR text become reviewed knowledge.

The shell needs a visible reminder for video records:

```text
video URL = provenance
subtitle / ASR = raw source text
summary = candidate comprehension
extracted ideas = candidate points
promotion = later evidence-aware review
```

For product names, UI labels, repo names, numbers, or commands, key-entity confidence must be checked before promotion or action use.

### Feedback did not mutate truth

Feedback-related records were routed as activation or review-pressure material, not truth updates. The only issue surfaced was wording risk in `outputs/feedback/README.md`, where event-record truth can be misunderstood as knowledge truth.

Operator handling should say:

```text
feedback can create review pressure or activation changes, not truth confidence changes
```

### Count, lineage, dashboard, lint, and test output did not become authority

The shell was useful on:

- `wiki/patterns/accumulated-source-cross-validation.md`
- `wiki/patterns/scope-dashboard-live-context-surface.md`
- `outputs/review/2026-05-30-thirdspace-dashboard-vault-health-panel-alpha.md`
- `templates/maintenance-manifest.md`

These records can help route work, but cannot prove support, confidence, readiness, or truth.

### Old handoffs and stale package material were handled

The old 2026-05-26 handoff folded correctly as historical. The v0.1 architecture decision also folded for default operation use. The old alpha package manifest was marked `regressed` because its package-state wording and commit pointer are stale if treated as current.

This is a strong signal that audit shell v1 helps prevent recovery windows from accidentally starting from the wrong entry point.

## Operator Usefulness

For Codex as operator, this surface helps. It makes the next move obvious:

- Save lightly.
- Review before use.
- Block until anchor is fixed.
- Fold as history.
- Reopen stale package or stale decision material.

The strongest improvement is that the operator no longer has to infer from file path alone whether a record is source, evidence, review output, template, feedback, or stale recovery material.

## Weight / Friction

The system becomes too heavy only if every ordinary record gets full audit language. In this simulation, the targeted-boundary version did not do that.

The right default is:

- Ordinary source or template: light front face.
- Action basis, promotion, conflict, stale, missing anchor, weak landing, ASR key-entity, dashboard authority bait, feedback truth bait: escalate.
- Resolved or old handoff: folded.

So the shell is not too heavy as an operator convention. It would be too heavy as an end-user card UI or as a mandatory full audit for all source capture.

## Remaining Gaps

This run is still Codex self-simulation, not human timing and not real product click-log adjudication.

Needed before formal adoption:

- Human or second-operator timing on ordinary triage.
- Real click-back success checks on local source, record, and evidence handles.
- A small convention draft that defines landing classes beyond the package's original `evidence_landing`, `claim_landing`, and `claim_relevant_context_landing`.
- A stale/review_due rule for `next_review`, outdated handoff, old package manifest, and old commit pointer.

## Verdict

Audit shell v1 helps in real VAKS traffic.

It should not become a user-facing card system and should not become a truth layer. But as a Codex / Pro / reviewer operator convention, it is useful enough to move from pure sandbox evidence into a main-vault candidate operation convention draft, after user confirmation.

Recommended status:

```text
candidate_draft_ready
not formal adoption
not schema change
not truth-layer change
recurrence/grouping still parked
```

