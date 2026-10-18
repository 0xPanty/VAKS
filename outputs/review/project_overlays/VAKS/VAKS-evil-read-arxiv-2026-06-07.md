---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
overlay_scope: project_sidecar_only
overlay_storage: confirmed_persistent_project_bucket
retrieval_scope: active_project_only
default_retrieval: false
retrieval_policy:
  policy_kind: project_context_only
  default_scope: project_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
project_id: VAKS
target_ref: outputs/review/2026-06-07-juliye2025-evil-read-arxiv-candidate-distillation.md
target_selector: "evil-read-arxiv as Research Scout and Paper Intake Workbench"
target_hint: "source-intake / research-scouting / feedback-ledger / paper-workbench"
project_borrow_scope:
  - "Borrow Research Scout as a candidate-only source discovery lane."
  - "Borrow fresh + influential + venue search as complementary candidate discovery paths."
  - "Borrow triage workbench ergonomics: paper cards, images, focus search, feedback, favorites, cached runs."
  - "Borrow feedback as scouting preference pressure, not truth mutation."
  - "Borrow arXiv source figure extraction as a source artifact enhancer for medium/heavy paper intake."
project_non_borrow_scope:
  - "For VAKS, do not borrow recommendation score, citation count, LLM filter score, or user like as truth confidence or support."
  - "For VAKS, do not borrow automatic domain/keyword update as unreviewed main config mutation."
  - "For VAKS, do not borrow auto graph edges as reviewed relations."
  - "For VAKS, do not borrow direct vault writes without source card and candidate-review boundary."
  - "For VAKS, do not borrow shell exec web routes without hardening."
project_reopen_trigger:
  - "Reopen when VAKS designs an automatic source discovery or paper-scouting lane."
  - "Reopen when VAKS builds a source triage workbench UI."
  - "Reopen when VAKS adds feedback-driven search preference updates."
  - "Reopen when VAKS implements paper artifact extraction or arXiv figure intake."
confirmation_basis: "User explicitly requested strong distillation and framed this repository as a potential future automatic-learning / source-finding path for the VAKS vault."
last_checked_at: 2026-06-07
expires_at:
borrow_value: very_strong
borrow_order:
  - "P1: Research Scout candidate queue"
  - "P1: fresh + influence + venue search split"
  - "P1: triage workbench with feedback"
  - "P1: feedback as scouting preference pressure"
  - "P2: keyword autolink and graph hints as activation only"
  - "P3: direct vault write, shell bridge, and note graph implementations"
avoid:
  - "score as truth"
  - "citation as support"
  - "LLM summary as reviewed analysis"
  - "feedback as confidence"
  - "auto config mutation"
  - "auto graph relation"
  - "direct vault write"
---

# Project Overlay: VAKS -> evil-read-arxiv

## Boundary

This is a VAKS-scoped borrowing sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern. It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: outputs/review/2026-06-07-juliye2025-evil-read-arxiv-candidate-distillation.md
source_ref: raw/repos/2026-06-07-juliye2025-evil-read-arxiv-source.md
snapshot_ref: raw/repos/_snapshots/juliye2025-evil-read-arxiv-31bca2e56bfc2439e2d93384a238bd20502c2a77.zip
target_hint: source-intake / research-scouting / feedback-ledger / paper-workbench
```

## Project Borrow Scope

For VAKS, borrow this repository as a Research Scout reference:

1. `research_scout_config` for user interests, focus, source types, keywords, exclusions, and time windows.
2. `source_candidate_queue` before any source becomes source card or candidate distillation.
3. `fresh + anchor + venue` search split:
   - fresh: new arXiv / recent sources,
   - anchor: S2 high-impact or canonical sources,
   - venue: top conference DBLP/S2 lane.
4. `triage_workbench` so source candidates can be skimmed, opened, filtered, liked, disliked, and deferred.
5. `feedback_scouting_patch` so user feedback suggests future search changes.
6. `source_artifact_extraction` for arXiv figures and paper visual evidence artifacts.

Best one-line borrowing:

```text
先让系统自动侦察资料，再让资料进入候选队列；不要让侦察结果直接变成知识。
```

## Project Non-Borrow Scope

For VAKS, do not currently borrow:

- recommendation score as truth confidence, review status, or action readiness.
- citation count as evidence support.
- LLM summaries or title/abstract analysis as reviewed comprehension.
- keyword wikilinks as reviewed relations.
- automatic graph edges as reviewed relations.
- LLM-generated preference updates as direct mainline config mutation.
- direct vault note writing before source card.
- web `exec` command bridge without parameterized execution, input validation, timeout/resource limits, and tool-safety gate.

Plain-language warning:

```text
这个库强在会帮你找和筛。
它不负责证明、审稿、定论。
```

## Reopen Trigger

Reopen this overlay when VAKS is working on:

- automatic source discovery,
- paper-scouting sandbox,
- source candidate queue,
- triage UI,
- feedback-driven retrieval preference,
- arXiv / paper artifact extraction,
- external-source scouting config.

## Confirmation

```yaml
confirmation_basis: "User explicitly requested strong distillation and said the repository may become the future automatic-learning / source-finding path for VAKS."
last_checked_at: 2026-06-07
expires_at:
```

## Borrow Gradient

```yaml
borrow_value: very_strong
P1:
  - Research Scout candidate lane
  - fresh + influential + venue source discovery
  - candidate triage workbench
  - feedback as scouting preference pressure
  - arXiv source figure extraction
P2:
  - keyword autolink as activation hint
  - LLM semantic re-rank as candidate ranking
  - paper note template as candidate scaffold
  - graph JSON as possible-association workbench
P3:
  - old direct hunter script
  - direct graph updater
  - shell exec web bridge
  - API key storage pattern
avoid:
  - score as truth
  - citation as support
  - LLM summary as reviewed analysis
  - feedback as truth mutation
  - automatic config mutation
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
