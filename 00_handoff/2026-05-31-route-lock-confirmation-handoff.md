---
type: handoff
status: current
created: 2026-05-31
updated: 2026-06-04
project: verified-action-knowledge-system
scope:
  - route-lock
  - recovery-state
  - architecture-boundary
  - alpha-minimal-writeback
  - video-source-intake
mainline_change: review-boundary-tightening
---

# Route Lock Confirmation Handoff

## Purpose

This handoff records the current route lock so future windows do not reopen settled architecture questions.

This is a confirmation and recovery note, not a framework rewrite.

## Locked Route

The public architecture spine stays fixed:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

The internal loop stays fixed:

```text
source
-> candidate point
-> calibration / point collision
-> evidence-aware review
-> reviewed node / reviewed relation
-> context pack / action basis
-> action
-> use ledger / feedback / review_due
```

## Locked Items

1. Main spine does not change.

2. Internal verified-action loop does not change.

3. Intake uses light / medium / heavy.

```text
light:
  quick capture; no review; no truth creation

medium:
  reusable material; tags/workbench/candidate handling; still no truth creation

heavy:
  strong source or action-relevant material; evidence-aware review can create reviewed knowledge
```

Default rule:

```text
default light
upgrade only when triggered
```

4. Evidence discipline remains a lazy gate.

Strict checks appear for promotion, decision, action basis, strong relation, risk-sensitive answer, conflict, stale/contested claim, or explicit "can we trust this" use.

5. External plugins are not truth authority.

```text
plugin output != reviewed knowledge
retrieval != authority
dashboard != judge
draft != truth
agent memory != reviewed memory
```

6. Automatic compile is parked.

Do not turn AI-generated wiki compilation into reviewed truth or a mainline automation goal.

7. Do not create a new formal two-lane architecture.

`Karpathy-light / VAKS-strict` is allowed as a plain-language explanation only.

It is not a new module tree, folder structure, or replacement route.

## Final Wording

Use this wording when explaining the route:

```text
This is not a dual architecture.
It is one main route + graded intake + lazy evidence gates.
```

Chinese shorthand:

```text
不是双架构。
是一条主路 + 分级入口 + 懒证据闸门。
```

The simplest mental model:

```text
轻中重是门。
主脊椎是路。
证据纪律是关卡。
```

## Parked Topics

Keep these parked unless the user explicitly reopens them:

```text
automatic compile
formal Draft Wiki Lane / Reviewed Action Lane architecture
plugin registry
custom dashboard plugin
Misa write gateway
RAG / Graph runtime as core
agent OS / MCP runtime as core
```

## Recovery Note

The latest accepted mainline is v0.3 evidence discipline plus the minimal
review-boundary / reverse-audit guardrail tightening in commit `70f73b7`.

This handoff confirms route interpretation only.

Do not modify `SCHEMA.md`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md`, or `ARCHITECTURE_PRINCIPLES.md` from this note alone.

## 2026-06-03 Video Source Intake

This landing adds a video source entrance, not a downloader module and not a new truth layer.

Mainline files changed:

```text
SOURCE_INTAKE.md
REVIEW_QUEUE.md
README.md
AGENTS.md
wiki/indexes/knowledge-graph-index.md
templates/video-source.md
raw/videos/.gitkeep
raw/videos/2026-06-03-bilibili-omniget-source.md
.gitignore
```

What landed:

```text
raw/videos/:
  future home for video source records and transcript-backed source cards.

templates/video-source.md:
  Obsidian-ready video source card with source metadata, transcript method,
  media cleanup note, key-entity confidence, candidate points, borrow /
  do-not-borrow notes, and VAKS routing.

SOURCE_INTAKE.md:
  video light / medium / heavy handling.
  Direct conclusion allowed: "This video says X."
  Not allowed without review: "X is true", "we should adopt X",
  "X supports a reviewed claim", or "X changes confidence".

REVIEW_QUEUE.md:
  source trace source_type enum now includes video.

raw/videos/2026-06-03-bilibili-omniget-source.md:
  first real medium-level video source card, based on the OmniGet Bilibili test.
  It is raw-only / candidate-only and does not adopt OmniGet or create reviewed
  claims.

.gitignore:
  keeps local Obsidian UI config, trash, and OS metadata out of git.

2026-06-04 anti-omission follow-up:
  `SOURCE_INTAKE.md`, `templates/video-source.md`, and the OmniGet test card now
  require a second extraction pass for pain point, workflow, tools/plugins,
  information structure, judgment mechanism, UX, automation boundary, risk,
  fit for us, and challenge to us. A summary-only digest is incomplete.

2026-06-04 project-local scope correction:
  video intake defaults are project-local to `C:\Users\Administrator\Documents\资料库`.
  The workflow belongs in this repository's `AGENTS.md`, `SOURCE_INTAKE.md`,
  `REVIEW_QUEUE.md`, `raw/videos/`, and `templates/video-source.md`; it should
  not become a global template for unrelated projects.

2026-06-04 artifact-location correction:
  medium / heavy video cards must not leave the only transcript, segment list,
  transcript metadata, or ledger under `.codex` scratch. Retained text artifacts
  should be copied into project-visible `raw/videos/<source-slug>/` paths or the
  formal Obsidian vault, and the source card should point there.

2026-06-04 source-card runner:
  `tools/new-video-source-card.ps1` is the project-local runner for the
  mechanical source-card draft: it can infer video identity, fetch public
  Bilibili metadata or public YouTube metadata through `yt-dlp` when available,
  copy retained transcript artifacts into `raw/videos/<source-slug>/`, generate
  frontmatter with project-visible artifact paths, and optionally invoke the
  finalization connector. It does not download media, transcribe, summarize,
  review claims, or promote knowledge.

2026-06-04 finalization connector:
  `tools/finalize-video-intake.ps1` is the project-local connector for medium /
  heavy video writeback finalization. It validates source-card artifact paths,
  syncs the source card and retained text artifacts to `H:\Obsidian\资料库`, checks
  SHA256 hashes, and can delete `.codex\video-research` temporary media. It uses
  `transcript_metadata_location` for subtitle or ASR metadata, with legacy
  `asr_metadata_location` accepted only as a compatibility alias. It is
  not a transcript engine, review engine, truth authority, or architecture
  promotion path.
```

Borrowed ideas are limited to workflow shape:

```text
batch links
platform-aware source identity
public subtitles first
local ASR when subtitles are missing
timestamped transcript / segment ledger
key-entity confidence
user visual check for unclear names / URLs / commands / numbers / UI text
delete downloaded media scratch after transcript by default
candidate-point routing before review
```

Do not infer from this landing:

```text
OmniGet adoption
video downloader product build
private/cookie/member-only scanning
automatic truth promotion
new schema/runtime/RAG/dashboard module
```

## 2026-05-31 Minimal Alpha Writeback

Commit:

```text
1eed9e2 Tighten review and maintenance boundaries
```

Mainline files changed:

```text
REVIEW_QUEUE.md
templates/maintenance-manifest.md
```

What landed:

```text
Approval integrity:
  LLM-assisted labels, prefilled review notes, high agreement, majority vote,
  or human "looks good" approval are review input / review pressure only.
  They do not create evidence review, truth confidence, reviewed relations,
  or automatic promotion.

Known omission check:
  Context-pack, action-basis, risk-sensitive, or explicit sufficiency reviews
  should expose known support, known counterevidence, known gaps, and known
  conflicts. This is review input, not action readiness.

Maintenance report discipline:
  Test, benchmark, fixture, and LLM-judge results are lint / diagnostic input.
  They do not create truth confidence, benchmark authority, runtime readiness,
  mainline readiness, or a new eval/test template family.
```

What stayed untouched:

```text
SCHEMA.md
README.md public five-layer spine
ARCHITECTURE_PRINCIPLES.md
runtime / API / MCP / dashboard
eval platform
agent toolchain
```

Post-writeback documentation sync:

```text
README.md, AGENTS.md, and wiki/indexes/knowledge-graph-index.md were later
updated to mention the accepted boundary tightening for recovery/discovery.
This did not change the public five-layer spine, schema, runtime, eval platform,
or agent toolchain.
```

Sandbox evidence:

```text
triage-compression-2026-05-31/mainline-placement-review/
  MAINLINE_PLACEMENT_REVIEW.md
  PLACEMENT_SCORE_MATRIX.md
  placement_test_report.md
  placement_results.json

triage-compression-2026-05-31/minimal-review-pressure-tests/
  report.md
  results.json
```

Post-writeback checks:

```text
placement test: 160 combinations, recommendation unchanged
pressure tests: 59 passed / 0 failed
git diff --check: passed, with Windows CRLF warnings only
```

## 2026-06-01 Reverse-Audit 2+1 Closeout

Final narrow writeback:

```text
REVIEW_QUEUE.md:
  prior chat memory / agent memory / model background cannot count as current
  source support unless tied to a current source span.

REVIEW_QUEUE.md:
  dynamic data evidence used for promotion or ready action basis needs
  query/filter/subset/as-of/result-set identity.

wiki/anti-patterns/transformed-evidence-as-original-source.md:
  OCR / translation / bbox / layout / table-derived evidence must not masquerade
  as original source support without a recoverable original anchor.
```

Explicitly not landed:

```text
oracle type taxonomy:
  parked / cut because AGENTS.md and templates/maintenance-manifest.md already
  say test, benchmark, fixture, and LLM-judge results are diagnostic lint only.
```

Untouched:

```text
SCHEMA.md
README.md public spine
runtime / API / MCP / dashboard
eval platform
agent toolchain
```

## 2026-06-01 Audit-Shell Noise-Reduction Sandbox

Status:

```text
sandbox/package only
not mainline
not schema
not product proof
```

Purpose:

```text
Test whether ordinary audit/log noise can be reduced without weakening the
existing evidence discipline. The candidate direction is audit shell v1:
default light, conditionally thick, raw anchors jump-backable.
```

External research and sandbox work tested these ideas:

```text
compact evidence card
compact coverage card
support/refine cluster
categorical feedback stub
unified audit shell v1
unresolved-first queue
resolved folding
regressed reopen
manual grouping guard
sparse provenance / jump-back pointer
```

Latest sandbox result:

```text
96-case adversarial fixture patch
96/96 pass
hard_gate_pass: true
false_lite: 0
review_due_precision: 1.0
review_due_recall: 1.0
jumpback_failures: 0
severe_over_grouping: 0
authority_leakage_incidents: 0
visible_front_reduction_pct: 58.7
grouped_reduction_pct: 50.0
```

Interpretation:

```text
This is stronger than the earlier 112-case pilot because gold labels, shell
output, comparison logic, and local anchor resolution are separated.

It is still fixture-based. It does not prove product readiness and does not
authorize main-vault operation convention writeback.
```

Current package locations:

```text
C:\Users\Administrator\Documents\VAKS_deep_research_context_2026-06-01.zip
C:\Users\Administrator\Documents\VAKS_pro_review_audit_shell_v1_2026-06-01_package.zip
C:\Users\Administrator\Documents\VAKS_alpha_noise_test_2026-06-01_package.zip
```

Recovery entry:

```text
00_READ_FIRST/NEXT_WINDOW_RECOVERY_FULL_GRAIN.md
```

Next decision:

```text
Send the package to Pro for review. If Pro accepts the adversarial patch, design
the 480 real-data paired pilot. At this June 1 stage, main-doc candidate
writeback was still on hold.
```

Superseded on 2026-06-04:

```text
The June 1 main-doc writeback hold belonged to the fixture/package stage.
It is superseded by the June 4 full ingest, pressure test, queue-first
prototype, Pro final gate, and main-vault candidate merge below.
```

Non-authority boundary:

```text
shell / grouping / dashboard / feedback / tests are routing and review aids.
They are not truth authority, source independence, evidence support, action
readiness, or mainline readiness.
```

## 2026-06-04 Audit Shell v1 / Queue-First Operator Cockpit Main-Vault Candidate Merge

Status changed after the June 4 full ingest simulation, pressure test, queue-first prototype, Pro review, final closeout, and final blocker confirmation.

Current status:

```text
operator-only candidate convention
pilot pending
not formal adoption
not schema guidance
not truth-layer guidance
not user-facing UI
not operator-usability validated
not product-grade click-back validated
```

Main candidate record:

```text
outputs/review/2026-06-04-audit-shell-v1-candidate-operation-convention.md
```

Final review and closeout:

```text
outputs/review/2026-06-04-audit-shell-v1-final-version-review.md
outputs/review/2026-06-04-audit-shell-v1-queue-cockpit-closeout.md
```

Full alpha lineage has been copied into the main vault without reduction:

```text
outputs/review/audit-shell-v1-full-alpha-lineage-2026-06-04/
outputs/review/audit-shell-v1-full-alpha-lineage-2026-06-04/ARTIFACT_MANIFEST.csv
```

This main-vault bundle includes:

```text
June 1 research / noise test / oracle / 480 / 800 lineage
June 4 full ingest simulation
June 4 pressure test
June 4 candidate Pro review package
June 4 queue-first cockpit prototype
June 4 Pro review package
June 4 final closeout package
intermediate and final zip snapshots
```

Final Pro gate:

```text
No merge blocker.
Can merge as main-vault candidate operation convention / operator-only candidate.
Do not present as formal adoption or completed product validation.
```

Hard rules now written into the candidate:

```text
deferred_review_unless_promoted requires promotion receipt / reopen before
action-basis, rule/convention basis, conflict handling, explicit challenge,
or high-risk answer support.

anchor-strength strip is only a front-face summary. Only selector-grade
jump-back can claim evidence landing.
```

Next step:

```text
Run the 80/60/60 operator pilot from:
outputs/review/audit-shell-v1-full-alpha-lineage-2026-06-04/directories/VAKS_queue_cockpit_CLOSEOUT_2026-06-04/NEXT_OPERATOR_PILOT_PROMPT.md
```
