# VAKS 800 Pressure-Overlay Pilot Package

Status: sandbox-only. No main-vault writeback, no `SCHEMA.md` change, no commit.

## What This Package Is

This is the patched automated package after Pro's review of the first 800-case run.

Before reading headline metrics, start with:

```text
NEXT_REVIEW_READING_ORDER.md
```

That file lists the highest-priority reports, scripts, click-back manifest, and
human-packet summary to inspect before looking at automated pass/fail numbers.

Accurate label:

```text
800-case, four-arm, real-data-row-driven pressure-overlay pilot
+ frozen machine oracle
+ automated checking scaffold
+ stratified blank human review packets
```

It is not a completed independent human-oracle pilot. Human timing, dual review,
and click-back adjudication remain blank and must be filled by humans.

## Latest Convergence / Current Candidate Convention

Pro's latest convergence narrows the current candidate convention:

```text
default core = shell_core + Chinese AI/reviewer-operator rendering
recurrence / grouping = conditional side arm
authority lint + categorical feedback strip + forbidden-wording lint = background guardrails
```

This is still sandbox candidate work. It is not a main-vault operation
convention, not a `SCHEMA.md` change, and not a truth core.

Chinese reviewer-card rendering is the next required operator-facing alpha, not
cosmetic translation. The current blocker is operator clarity: Codex / Pro /
reviewer agents should be able to understand status, risk reason, anchor health,
recommended handling, and when to open the full audit without relying on raw
machine labels such as `missing_anchor`, `review_due`, `unresolved_gate`, or
`pointer_triad`.

This is not an ordinary user workflow. Ordinary vault use should stay light:
the user should only see short plain-language risk notices when a record affects
an answer or action.

Current role split:

- `shell_core` remains the only default-core candidate.
- `shell_core_plus_recurrence` remains a conditional side arm only.
- recurrence / grouping can route repeated ordinary open items, but count,
  group count, source count, and lineage do not prove support strength or
  independence.
- authority lint, categorical feedback strip, and forbidden-wording lint are
  guardrails. They do not prove semantic safety or truth.
- shell, reviewer-card, grouping, lint, tests, dashboards, and review packets
  are non-authority surfaces.

If work continues, the next narrow step should be:

1. Chinese AI/reviewer-operator patch for `shell_core`.
2. 12-24 case operator preflight with blank review fields.
3. Mandatory 12-case adversarial add-on focused on anti-self-proof traps.
4. Small render-integrity lint for card wording and forbidden authority claims.

Do not treat that as human timing, independent human oracle, product click-back
validation, mainline readiness, or a reason to expand broad automated testing.

Latest Pro review says this stage reached `pass with concerns`, then the narrow
operator adjudication draft found a real blocker: transport click-back is not
semantic click-back. This package now repairs the automatic selector landing
proxy with a conservative claim-keyword window after exact evidence/claim
matching. The next step is still not the 120-case main packet; rerun the narrow
operator adjudication and keep recurrence closed until human/product click-back
is checked.

Current sandbox update:

- `reports/EXTERNAL_ARCHITECTURE_REVIEW_SYNTHESIS.md` records the external
  review synthesis as sandbox input, not truth authority.
- `reports/EXTERNAL_SOURCE_PRIORITY_AND_FINAL_JUDGMENT.md` records the primary
  external sources to read first, the immediate verification work, and the
  final engineering judgment. It reinforces that the next real proof is
  operator preflight plus live/immutable click-back, not another broad
  automatic patch.
- `reports/RISK_TIERED_REVIEWER_UX_PATCH_SPEC.md` reframes the patch as
  risk-gated reviewer UX rather than card polish.
- `reports/AUDIT_SHELL_V1_STATE_AND_SLOT_CONVENTION.md` records the explicit
  state machine and required operator front-face slots. It makes the current
  convention precise: the card is only a renderer; the core is state machine
  plus slots.
- `reports/OPERATOR_RENDERER_SLOT_PATCH_REPORT.md` records the latest renderer
  patch: boundary reminders are now targeted, ordinary stable records no longer
  get per-card global disclaimers, and weak landing classes explicitly say they
  are not evidence landing.
- `reports/CHINESE_REVIEWER_CARD_USABILITY_PREFLIGHT_PROTOCOL.md` defines the
  small 24-case AI/reviewer-operator preflight metrics.
- `reports/NEGATIVE_CONTROL_AND_VALIDATION_TIMELINE.md` defines the required
  negative controls and the six-week validation timeline.
- `reports/QUALITY_GATES_AND_THRESHOLDS.md` defines the go / no-go gates. Here
  `go` means eligible for main-vault candidate operation-convention discussion,
  not adoption.
- `reports/CHINESE_FORBIDDEN_WORDING_LINT.md` records the exact banned Chinese
  wording and safe replacement phrases for the operator renderer.
- `reports/CODEX_OPERATOR_PREFLIGHT_DRY_RUN_REPORT.md` records the Codex
  operator dry-run over the 24 Chinese samples plus the 12 adversarial samples.
  This is useful operator evidence, but it is not independent human oracle,
  timed usability, or product click-back validation.
- `reports/PRO_REVIEW_PASS_WITH_CONCERNS_AND_NEXT_ROUTE.md` records the latest
  external verdict and the next route: truth ledger -> escalation controller ->
  operator review surface -> end-user answer surface, with card downgraded to a
  renderer.
- `reports/OPERATOR_ADJUDICATION_ROUND1_REVIEW_RESULT.md` records the imported
  narrow operator adjudication result: `pass with concerns`, wrong
  actionability 0/36, serious miss 0/36, authority misunderstanding 0/36, but
  core click-back only 16/24 and no 120-case packet yet. This imported result is
  not independent dual-human evidence.
- `reports/CLICKBACK_SEMANTIC_LANDING_EVAL.md` and
  `data/clickback_semantic_landing_eval.json` split transport fetch, local path
  resolution, and selector landing. Current automated semantic selector success
  is 24/24 after the keyword-window repair; `body_window` and boilerplate
  landing are 0/24. Landing class is split into evidence landing, claim landing,
  and weaker claim-relevant context landing. This is still a proxy, not
  human/product click-back adjudication.
- `reports/CODEX_LOCAL_REAL_OPERATOR_SELF_TEST_REPORT.md` records a 26-sample
  Codex self-test over local real-row/full-anchor cases. It supports the claim
  that the operator surface helps Codex triage, but it is not human
  adjudication or product readiness.
- `review_packet_operator_adjudication_narrow/` contains the blank double-review
  and adjudication packet that should be run next. It has no filled human
  results.
- `review_packet_risk_tiered_24/` contains the generated Chinese operator-facing
  samples and blank answer sheet. The current renderer adds a short Chinese
  handling gloss and shows source / record / evidence as operation entries with
  path handles, rather than using raw paths as the main UI text.
- `make_risk_tiered_reviewer_preflight_24.py` generated the packet from
  `shell_core` artifacts only.
- `review_packet_risk_tiered_24/render_integrity_lint.json` is a small wording
  lint only; it is not semantic safety proof.
- `review_packet_risk_tiered_24/forbidden_wording_lint_zh.json` checks the 24
  generated Chinese operator cards against `forbidden_wording_zh.json`; latest
  status is pass with 0 findings.
- `review_packet_adversarial_12/` contains hand-authored synthetic adversarial
  operator cases for ordinary-looking action-basis, buried challenge,
  anchor pseudo-success, wrapper-only click-back, review_due traps, grouping
  near-miss, serious folded traps, authority paraphrase, fake numeric precision,
  summary overwrite, source-count traps, and lineage traps.
- `make_adversarial_operator_cases_12.py` generated that packet. These cases are
  anti-self-proof pressure fixtures only; they are not real business logs,
  product click-back proof, or an independent human oracle.
- `quality_gates_v1.json` and `quality_gate_eval_800.json` separate available
  automated proxy gates from gates that still require human/product evidence.
  Current overall gate status is `not_go_yet`, because wrong actionability,
  authority misunderstanding, human timing/open-rate, and product click-back
  semantic landing are not passed yet.
- `data/clickback_snapshot_manifest.json` now records 24/24 representative
  full-anchor cases as live/immutable snapshots after urllib + PowerShell retry,
  with 0 fallback wrappers. This repairs transport/fallback, but
  `data/clickback_semantic_landing_eval.json` must be checked separately. It
  now reports 24/24 automated semantic selector success after the
  keyword-window repair; 24/24 live is still not human/product click-back
  success.

## Patch Scope

The patch addresses the required pre-human-stage fixes:

- human review packet is now stratified across resolved, recurrence-capable,
  bad-anchor, authority-bait, over-grouping near-miss, and serious-folded
  samples.
- recurrence grouping measurement now counts folded members with visible
  `group_id`.
- resolved folding is measured as default unresolved-first surface behavior,
  not as a 95% line reduction after a resolved record is already opened.
- 24 representative click-back snapshot cases are materialized; after urllib
  retry plus PowerShell fallback retry, all 24 use live/immutable snapshots and
  0 use fallback source-wrapper snapshots.
- semantic click-back landing evaluation now separates transport success from
  claim-relevant selector success. `body_window` and Wayback / Archive
  boilerplate landing are counted as selector failure, not product click-back.
  Current automated semantic selector success is 24/24, but it still needs
  operator click-log adjudication.
- authority fuzz remains labeled as canned lint, not semantic authority safety.

## Arms

- `baseline_full`
- `shell_core`
- `shell_core_plus_recurrence`
- `leaky_or_unversioned_control`

The negative control fails, as required.

## Current Automated Readout

`shell_core`:

- safety hard gates pass
- serious false-lite: 0
- serious folded: 0
- source pointer exactness is no longer summarized as a blanket 0. Check
  `reports/PILOT_800_REPORT.md` and `reports/QUALITY_GATES_AND_THRESHOLDS.md`
  for current source-anchor exactness; record/evidence pointer checks remain
  separate.
- authority leakage: 0 on canned checks
- ordinary line reduction: 56.2%
- ordinary char reduction: 63.4%
- resolved default queue visible: 0
- resolved front line violations: 0
- threshold audit: pass

`shell_core_plus_recurrence`:

- safety hard gates pass
- serious folded: 0
- severe over-grouping: 0
- grouping recall: 8/8 multi-member groups
- predicted grouped members: 48
- grouped reduction: 83.3%
- recurrence line reduction: 49.1% and therefore below the >=50% continuation gate
- threshold audit: caution/fail on recurrence performance gate

`leaky_or_unversioned_control`:

- fails as expected
- serious false-lite: 376
- state mismatch: 376
- severe over-grouping: 12
- serious folded: 12
- authority leakage: 48

`authority_leaky_renderer`:

- fails as expected
- authority leakage: 692
- purpose: proves the harness catches rendered wording that treats dashboard or
  test pass as truth authority

`fake_precision_feedback_renderer`:

- fails as expected
- authority leakage: 692
- purpose: proves the harness catches fake numeric precision such as risk,
  feedback delta, and confidence percent when framed as actionability or truth

## Human Packet

Main packet:

- `review_packet/main_core_assignments.csv`
- compares `baseline_full` vs `shell_core`
- 120 stratified cases, 240 assignments
- covers resolved, recurrence-capable, bad-anchor, authority-bait,
  anchor-jumpback-failure, over-grouping near-miss, and serious-folded risks

Side packet:

- `review_packet/side_recurrence_assignments.csv`
- compares `shell_core` vs `shell_core_plus_recurrence`
- 60 recurrence-heavy cases, 120 assignments
- intended only for recurrence bundle value and misunderstanding risk

Timing and adjudication sheets are blank. No human results are fabricated.

## Important Limits

- Gold is hash-frozen, but still machine-derived from explicit overlays.
- Valid anchor checks prove selector/hash/offset/quote integrity inside the
  package; they do not prove final UI click-back usability.
- The previous wrapper-heavy click-back snapshot subset has been repaired to
  24 live/immutable representative snapshots and 0 fallback wrappers, but this
  is still not final UI click-back adjudication. Current automated semantic
  selector success is 24/24, split by landing class, so the next blocker is
  human/product click logs and adjudication, not transport or body-window
  boilerplate.
- Authority fuzz hit rate is a lint result, not a semantic firewall.
- `shell_core` remains the only default-core candidate.
- recurrence/grouping remains a conditional bundle.
- shell/grouping/pointers/feedback/tests/dashboard outputs remain non-authority.
