---
record_kind: window_handoff
created_at: 2026-06-08
topic_id: answer-prep-boundary-and-three-window-execution
truth_boundary: handoff_recovery_state_not_truth
status: active
---

# Handoff: Answer-Prep Boundary + Three-Window Execution

Purpose: let a fresh window pick up at project granularity without re-deriving
context. Files are source of truth. Do not rely on chat memory alone.

## 1. Read First (alignment)

- `AGENTS.md` (router + operating rules + boundaries)
- `SCHEMA.md`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md`, `ARCHITECTURE_PRINCIPLES.md` (frozen spine)
- `REVIEW_QUEUE.md`, `REFERENCE_REVIEW_PROTOCOL.md`, `SOURCE_INTAKE.md`
- Then run: `git log --oneline -8` and `git status --porcelain`

## 2. Verified Current State (as of 2026-06-08)

- HEAD = `4abb84a docs: add self-contained review candidate gate`
- Recent commits:
  - `4abb84a` self-contained review candidate gate (NOT yet reviewed by advisor)
  - `ea7339b` video intake source-card helpers
  - `4fe57a8` independent answer support boundaries (the answer-prep principle merge)
  - `0cea747` source intake control flow guardrails
- Working tree is DIRTY:
  - Modified: `REVIEW_QUEUE.md`, `wiki/indexes/knowledge-graph-index.md`, `wiki/patterns/review-gated-compile-queue.md`
  - Untracked: `outputs/review/ci-02..ci-09-*` (candidate improvement items), 2 candidate-distillations, new `raw/papers`, `raw/repos` (MrXujiang NO-CRM, Nocode-Wep) + snapshots, `raw/videos` xhs source
- Old sandbox `outputs/review/source-intake-tag-routing-sandbox-2026-06-07/` is DELETED.
- Promoted claims in `wiki/claims/`: 9.

## 2A. Verified Current State Addendum (2026-06-14)

- Source Annotation pilot workbench mainline merge was committed as
  `db7b6bb2 docs: land source annotation pilot workbench`.
- That commit intentionally contains only five files:
  `00_handoff/2026-06-08-answer-boundary-and-three-window-execution-handoff.md`,
  `SCHEMA.md`, `SOURCE_INTAKE.md`, `templates/source-annotation.md`, and
  `wiki/bases/source-annotations.base`.
- The scale sandbox `outputs/review/source-annotation-scale-sandbox-2026-06-14/`
  remains untracked sandbox evidence and was not included in the mainline merge.
- Validation after the merge: `python .\tools\validate_source_intake_contract.py`
  returned `0 warnings / 0 errors`; YAML parsing also passed for
  `templates/source-annotation.md` frontmatter and
  `wiki/bases/source-annotations.base`.
- The broader working tree remains dirty with unrelated historical intake,
  raw-source, project-overlay, and tool changes. Do not use `git add .`; future
  commits must continue to stage only their own explicit file territory.

## 3. Locked Route + Red Lines (do not violate)

- Spine FROZEN: do NOT edit `SCHEMA.md`, `ARCHITECTURE_PRINCIPLES.md`, `FUSION_*`.
- No new lane structure; automatic compile stays parked.
- Test / lint / benchmark / LLM-judge / blind review = diagnostic, NOT truth,
  NOT reviewer approval, NOT mainline readiness.
- Scripts/pipelines = tools/test-products, stay in sandbox, never become truth.
- Promotion is a strict gate: evidence first, final promotion needs user sign-off.
- Never `git add .`; commit only your own file territory; atomic commits.
- Commit evidence BEFORE cleanup (an earlier pilot's evidence was lost this way).
- Answer in Chinese by default.

## 4. What This Arc Concluded

- The answer-preparation evidence boundary was merged at the PRINCIPLE level
  (`4fe57a8`, 4 files: `SOURCE_INTAKE.md`, `REFERENCE_REVIEW_PROTOCOL.md`,
  `templates/query-run.md`, `templates/review-candidate.md`). Core rules:
  claim cannot self-support; independent anchor required; supported != truth;
  answer-ready != action-ready; claim_refs = trace handles; test/lint/blind = diagnostic.
- This principle was validated ONCE on real claims (n=1 true-claim pilot with
  cold blind review). Status: design/contract for this block ~90%; operationalized
  + habitual use still thin. The pilot run records were sandbox and were deleted;
  `4fe57a8` currently has NO audit breadcrumb.
- The "10-point supplement" (warrant / sufficiency / coverage_map / missing-context /
  temporal / granularity / source-transformation / trace / annotation / retrieval)
  was dedup-checked against the spine: 6 already canonical, 4 only clearer wording,
  ZERO new alpha. Conclusion: NOT a development track. Do not redefine or build
  parallel vocabularies; reference existing definitions only.
- Whole-architecture verdict: design-rich, use-poor (~40% overall). The scarce
  resource is real-use mileage and the review->promotion funnel, NOT more design.

## 5. Open / Unreviewed (confirm before trusting)

- `4abb84a` and the `ci-02..ci-09` items are NOT advisor-reviewed; a new window
  should read and judge them before merging anything further.
- Dirty tree mixes funnel edits + new intake; do not bundle unrelated files.

## 6. Three-Window Execution Plan (parallel, non-colliding)

Each window owns a separate file territory; they can run simultaneously safely.

- Window 1 — Review->Promotion Funnel (mainline priority)
  - Territory: `wiki/claims/`, `wiki/decisions/`, `REVIEW_QUEUE.md`, `wiki/indexes/`
  - Do: inventory review-ready candidates; build Evidence Packets; run Evidence
    Sufficiency Gate on 3-5; mark promotion-ready / missing / scope_limited.
    Add the `4fe57a8` validation breadcrumb in a commit message.
  - Promotion write needs user sign-off.
- Window 2 — True-Claim Pilots (mileage)
  - Territory: `outputs/review/<new-sandbox>/` only; reads `wiki/claims` read-only.
  - Do: run 2-3 real-question pilots; real claims as trace handles; support to
    independent anchors; differentiated results; each with a COLD blind review;
    summarize pain points (no new vocabulary).
  - Never write mainline; commit records before cleanup.
- Window 3 — Obsidian Use Surface (safest, zero repo collision)
  - Territory: `H:\Obsidian\资料库\` only.
  - Do: HOME/landing page; 2-3 Bases dashboards (e.g. promotion candidates,
    by-layer, recent intake); a light MOC to replace the long flat index.
  - Navigation/display only; dashboards != truth; do not touch repo mainline.

Coordination: Windows 1 and 2 share the git repo but different subdirs; each
commits ONLY its own territory, never `git add .`.

Single-window priority: open Window 1. Two windows: 1 + 3. Three: 1 + 2 + 3.

## 7. Pending Tasks

- Decide commit grouping for the current dirty tree (funnel edits vs new intake),
  atomic, no `git add .`.
- Add `4fe57a8` validation breadcrumb (handoff or next commit message).
- Review `4abb84a` + `ci-02..ci-09` before further mainline moves.
- Keep 10-point supplement closed (no redevelopment).

## 8. 2026-06-14 Source Annotation Replacement

- User explicitly asked to replace the old source-level tag/sticky-note idea with
  the Obsidian-footnote-inspired Source Annotation Sidecar design.
- New boundary: inline footnote / highlight is only the human-friendly entrance;
  canonical data is `record_kind: source_annotation` under
  `outputs/review/source_annotations/`.
- Source annotations are locators and review input only. They cannot become
  final support, confidence, reviewed relation, Project Overlay verdict, or
  action basis without Evidence Packet / evidence_support.
- Project Overlay remains project-level borrow / non-borrow / reopen scope. It
  may reference annotations, but annotations do not replace Overlay fields.
- New recovery files to inspect with the main framework:
  `SOURCE_INTAKE.md`, `SCHEMA.md`, `IMPLEMENTATION_BLUEPRINT.md`,
  `templates/source-annotation.md`, `wiki/bases/source-annotations.base`, and
  `tools/validate_source_intake_contract.py`.
- Post-review patch: added conditional `evidence_packet_ref`, a
  `source_annotation`-as-support failure-matrix case, a source-annotation
  processing-tier guard, and clarified that v2 live readonly harness remains
  sandbox evidence only because frozen replay can drift with generated runtime
  fixtures.
- Follow-up router / skill patch: `AGENTS.md` now routes future windows to
  Source Annotation Sidecar for source-level "useful / borrowable" spans, and
  local Codex skills `vaks-obsidian-distill` + `vaks-video-research-intake`
  were updated so future VAKS / Obsidian intake uses annotations for source
  spans, Project Overlay for project borrow / non-borrow scope, and Evidence
  Packet / evidence_support for support or action use.
- Product-gate closeout: an independent red-team pass judged the design
  `pass-with-conditions`: L4 product-grade pilot-ready, not L5
  production-operated. The safe mainline merge is intentionally small:
  `templates/source-annotation.md`, `wiki/bases/source-annotations.base`,
  `SOURCE_INTAKE.md`, and `SCHEMA.md` only absorbed the durable fields and
  workbench rules. The scale sandbox, 10k fixtures, reports, and stress scripts
  stay sandbox evidence and should not be bundled into mainline.
- Mainline enhancement now landed conceptually: source annotations carry anchor
  health (`anchor_checked_at`, `anchor_stale`, `anchor_match_count`), operator
  routing (`blocked_reason`, `next_action`), and source-level scale controls
  (`source_digest_required`, `source_digest_ref`). The Bases workbench should
  stay lightweight: working inbox, anchor repair, source drilldown, AI
  review-input gate, and source health.

## 9. Report Back Format

State which window, which files touched (paths), what concluded, and what is
left for user sign-off. Update the newest handoff if recovery state changes.
