# VAKS Audit Noise Reduction External Research Intake

This file captures the external research report in segments before VAKS-specific verification and design filtering.

Status:

```text
intake only
no main-vault change
no architecture conclusion yet
pending segment-by-segment verification
```

## Segment 1: Research Scope And Mature-System Patterns

### Scope / Judgment Standard

The report frames the core VAKS problem as:

```text
Keep strong auditability for high-risk / action-basis scenarios, while reducing excessive writing ritual for small claims, support/refine collisions, and ordinary scope-fit feedback.
```

External patterns should be judged by three criteria:

```text
default record can be thinner
escalation conditions are clear
raw anchors remain jump-backable
```

### Transparency Boundary

HCI transparency research is summarized as warning that transparency does not mean every detail should stay permanently visible.

Useful pattern:

```text
simple feedback first
drill down on demand
```

VAKS relevance:

```text
noise reduction should not remove traceability
traceability can be layered rather than always expanded
```

### Mature-System Pattern 1: Layered Records / Two Views

Examples cited:

```text
UK Algorithmic Transparency Recording Standard: Tier 1 public summary + Tier 2 professional detail
GRADE: Summary of Findings for decision makers + Evidence Profile for reviewers
```

Claim:

```text
compact cards and full audit records are not alternatives; they can be two views of the same object.
```

VAKS candidate implication:

```text
small claim / answer / feedback records can default to compact cards, with full audit packet available only when gates require it.
```

### Mature-System Pattern 2: Focus Main View On Unresolved Items

Examples cited:

```text
GitHub: resolved conversations are folded; conversations can be unresolved / resolved / outdated
GitLab: open threads can block merge; unresolved-only view; move thread to issue; outdated diff threads can be collapsed
Sentry: unresolved / for_review issues are separated from archived issues
```

Claim:

```text
review queues should center items that still need action, not keep resolved history in the main view.
```

VAKS candidate implication:

```text
review records and feedback logs may need unresolved/open/review_due-focused views, with resolved history folded or externalized.
```

### Mature-System Pattern 3: Group Repeated Events, Keep Representative Raw Traces

Examples cited:

```text
Sentry: fingerprint groups similar events into an issue; grouping information remains inspectable
Sentry breadcrumbs: configurable ring buffer, not unlimited event display
OpenTelemetry: tail sampling, IsRecording, event/link limits, span links, batching
```

Claim:

```text
systems reduce noise by grouping repeated events while preserving enough representative trace for diagnosis.
```

VAKS candidate implication:

```text
feedback events and repeated scope-fit failures could be grouped into issue-like clusters or compact recurrence records, with source/event anchors retained.
```

### Mature-System Pattern 4: Sparse Provenance Instead Of Fake Completeness

Examples cited:

```text
W3C PROV: starting point terms allow simple provenance first, then expansion
PROV-AQ / provRef: heavier provenance can be externalized and located/queried when needed
SLSA provenance: separates external parameters, internal parameters, resolved dependencies, and debug/event-response byproducts
Docker BuildKit attestation: mode=min and mode=max
```

Claim:

```text
importantness of an object and amount of retained detail should be separate switches.
```

VAKS candidate implication:

```text
review/action importance should not automatically mean every provenance detail is always displayed; detail level can be min/max or compact/full while keeping anchors.
```

### Mature-System Pattern 5: Prefer Explained Discrete States Over Fake Precise Numbers

Examples cited:

```text
GRADE: four certainty levels with downgrade/upgrade reasons instead of continuous confidence numbers
Sentry: new / ongoing / escalating / regressed / resolved / archived
ATRS examples: Low / Medium / High style risk categories
```

Claim:

```text
avoid pseudo-precise numbers when calibration is weak.
```

VAKS candidate implication:

```text
ordinary scope-fit feedback should use type + short reason + recurrence/status, not uncalibrated activation_delta-style numbers.
```

## Running Candidate Themes

```text
compact card + full audit view
unresolved-first review/feedback views
group repeated feedback/events
sparse provenance with jump-back anchors
discrete states instead of fake numeric deltas
```

## Segment 2: Candidate Mechanisms And Borrowable Parts

### Kubernetes Audit Policy

Pain points:

```text
P3 coverage_map too heavy
P4 runtime trace too heavy
indirectly helps P2 processing/access clarity
```

Key external mechanism:

```text
first-match rules assign audit levels:
None
Metadata
Request
RequestResponse

omitStages and omitManagedFields remove low-value intermediate stages or repeated bulky fields
```

Minimum VAKS borrow:

```text
default ordinary small claim, ordinary scope-fit feedback, and light query-run to metadata-level records
metadata-level record keeps only:
object
time
actor/reviewer/agent
source anchor
current status
jump-back pointer

upgrade only when:
action-basis
explicit challenge
conflict
regression
other strict gate trigger
```

Do not absorb:

```text
Kubernetes resource/request semantics
```

Schema-change tendency:

```text
no
better as operation convention first
may become runtime policy later if VAKS gets runtime support
```

Possible landing:

```text
operation convention
review-lite
future runtime
```

Main risk:

```text
wrong level rules may leave high-risk objects stuck at metadata level when they should be thickened
```

### UK Algorithmic Transparency Recording Standard

Pain points:

```text
P3 coverage/log heaviness
P4 trace/report burden
indirectly helps P2 clarity
```

Key external mechanism:

```text
Tier 1 high-level summary
Tier 2 professional detail
mandatory scope limited to tools with significant impact on public decisions
administrative burden reduction is an explicit design goal
```

Minimum VAKS borrow:

```text
for high-risk / action-basis output:
provide a one-screen summary face
put thicker evidence, scope, risk, and limitations in expansion/detail layer

small claims or ordinary design answers do not automatically enter heavy disclosure
```

Do not absorb:

```text
full public-sector compliance template
external-publication governance assumptions
```

Schema-change tendency:

```text
no
```

Possible landing:

```text
review-lite
action-basis card
operation convention
```

Main risk:

```text
if every internal object gets ATRS-style expansion, burden returns
if Tier 1 is too thin, key limitations may be hidden
```

### GRADE Evidence Profile And Summary Of Findings

Pain points:

```text
P3 coverage_map too heavy
P4 fake numeric precision in feedback / summary
```

Key external mechanism:

```text
same evidence body has two tables:
Evidence Profile for reviewers to inspect judgment process
Summary of Findings for decision makers

main table includes only important / critical outcomes
certainty uses four levels plus transparent downgrade/upgrade reasons
not fake continuous scores
```

Minimum VAKS borrow:

```text
split coverage_map into card front and expandable back

front includes only:
few points the answer actually depends on
rough order/shape of evidence sources
scope limit
risk note

back includes:
omitted gaps
counterevidence
support/refine details
review reasons
```

Do not absorb:

```text
medical effect-size machinery
baseline risk machinery
recommendation machinery
```

Schema-change tendency:

```text
no
```

Possible landing:

```text
review-lite
action-basis
anti-fake-precision
```

Main risk:

```text
if only summary front remains and review reasons are not jump-backable, users may overtrust the simplified table
```

### GitHub Pull Request Review Pattern

Pain points:

```text
P3 review noise / coverage-map surface heaviness
```

Key external mechanism:

```text
files can be marked Viewed and folded
progress bar exposes how much remains unseen
conversations split into unresolved / resolved / outdated
resolved conversations are folded
file view can filter by file/path/type/hide viewed
Markdown details blocks can fold long sections
```

Minimum VAKS borrow:

```text
small claim review, resolved support notes, and old scope-fit feedback default to folded
review queue gets a main view for only unresolved / newly regressed items
original trail remains expandable when needed
```

Do not absorb:

```text
code diff workflow assumptions
repo permissions assumptions
line-comment workflow assumptions
```

Schema-change tendency:

```text
no
view layer and record-view convention
```

Possible landing:

```text
review-lite
queue view
operation convention
```

Main risk:

```text
folding can make the system look clean while hiding high-risk details if upgrade signals are missing
```

### GitLab Merge Request Discussions And Issue Handoff

Pain points:

```text
P3 unresolved review noise
P4 long feedback / trace burden
```

Key external mechanism:

```text
open threads can block merge
resolved threads fold but can reopen
open threads can be moved into issues for follow-up without blocking the main line
unresolved-only queue/view
activity stream filters by relevant item
issue discussion can generate a separate summary view
```

Minimum VAKS borrow:

```text
turn support/refine collision and scope-correction feedback into a cluster/thread with unresolved gaps
move non-blocking items out of the main review queue as linked stubs
allow summary for long audit trail while preserving expandable raw text
```

Do not absorb:

```text
do not default evidence questions to automatically resolved just because a diff/source became outdated
do not treat LLM summaries as authority
```

Schema-change tendency:

```text
no
```

Possible landing:

```text
review-lite
unresolved-only queue
future runtime
```

Main risk:

```text
automatic stale/outdated closure works for diff noise but is unsafe for evidence problems that have not actually been resolved
```

### Sentry Issue Grouping, Breadcrumbs, And Issue States

Pain points:

```text
P4 feedback/runtime trace noise strongest
P3 review/log surface noise
```

Key external mechanism:

```text
events with the same fingerprint are grouped into one issue
issue detail can explain why events were grouped
breadcrumbs are structured, bounded ring buffers preserving recent diagnostic trail before a failure
noisy issues can be archived while events continue to be recorded
main workflow is organized around issue states, not every raw event:
unresolved
for_review
escalated
regressed
resolved / archived
```

Minimum VAKS borrow:

```text
group repeated query-runs, scope-fit feedback, repeated "too broad", repeated "missing evidence", or similar signals by fingerprint-like key

grouped work item keeps:
count
first seen
last seen
recent exemplar
necessary breadcrumbs / jump-back anchors
current state

archived item can float back to queue if it worsens or regresses
```

Do not absorb:

```text
exception stack model
SDK-specific grouping heuristics
AI grouping as epistemic authority
```

Schema-change tendency:

```text
no now
optional fingerprint field could be considered only if future automatic grouping exists
```

Possible landing:

```text
future runtime
review queue
feedback ledger
```

Main risk:

```text
over-grouping hides meaningful differences
under-grouping recreates noise
```

### OpenTelemetry Tracing

Pain points:

```text
P4 runtime trace too heavy
P3 coverage/log heaviness
indirectly helps P2 by separating what was recorded from what was processed
```

Key external mechanism:

```text
tail sampling can decide whether to retain after seeing a whole trace
IsRecording=false avoids expensive attributes/events/status capture
span processor triggers only when recording
span links associate cross-trace causality without expanding everything inline
event/link counts have limits
collector batch processor compresses output
```

Minimum VAKS borrow:

```text
future runtime defaults ordinary query-run to minimal trace

upgrade to full trace when:
error
regression
high-risk action-basis
explicit challenge
multi-source collision

ordinary runs can be linked rather than expanded into full chains
set event/link caps so one run cannot consume the whole log budget
```

Do not absorb:

```text
do not expose observability jargon directly as VAKS user-facing concepts
```

Schema-change tendency:

```text
no now
future runtime may need optional schema only after repeated evidence
```

Possible landing:

```text
future runtime
parked-now
```

Main risk:

```text
bad sampling policy can drop the exact abnormal run that mattered
```

### W3C PROV Family

Pain points:

```text
P1 source independence / lineage clarity strongest
P3 coverage/provenance display burden
P4 trace/log burden
```

Key external mechanism:

```text
PROV-O allows a small set of starting point terms for simple provenance first
heavier information can be added later:
derivation
quotation
primary source
qualified relation

PROV-AQ supports locating/querying external provenance records
provRef best practice supports linking to heavier provenance outside the current object
```

Minimum VAKS borrow:

```text
small claim / feedback / query-run keeps a sparse provenance tuple:
entity
activity
agent
source anchor
wasDerivedFrom
hadPrimarySource
pointer-to-full-record

audit can jump to external detailed evidence when needed
```

P1-specific value:

```text
record lineage and dependence instead of mistaking source count for independence
```

P1 boundary:

```text
lineage record is not independence review
provenance may come from multiple providers and may conflict
lineage can support review prompts but cannot prove source independence by itself
```

Do not absorb:

```text
RDF / OWL stack
triple-store expansion
ontology engineering
```

Schema-change tendency:

```text
no
start with naming convention and links
```

Possible landing:

```text
operation convention
anti-pattern documentation
future runtime
```

Main risk:

```text
if PROV becomes ontology engineering instead of lightweight relationship vocabulary, VAKS becomes heavy again
```

### SLSA Provenance As Backup Reference

Pain points:

```text
P1 source independence / dependency clarity
P2 processing/access distinction
future runtime disclosure depth
```

Key external mechanism:

```text
separates:
externalParameters
systemParameters
resolvedDependencies
byproducts

keeps external parameters simple
puts checkable digests in dependency fields
supports mode=min / mode=max disclosure depth
```

Minimum VAKS borrow:

```text
importantness / review intensity and actually-held evidence detail must be modeled separately
```

Current fit:

```text
future runtime / parked
not a direct replacement for the current small-claim template
```

Do not absorb:

```text
full software supply-chain attestation stack
build-specific semantics
```

Schema-change tendency:

```text
no now
future optional only if runtime needs mechanical provenance
```

Main risk:

```text
too mechanical for current Markdown-first VAKS if imported directly
```

## Segment 3: Integrated Answer To VAKS Key Questions

### Core Noise-Reduction Shape

The report's integrated recommendation:

```text
Do not merely shorten every template.
Wrap records in a layered, expandable audit shell.
```

Layering principle:

```text
default layer:
enough to locate, group, jump back, and reopen

expanded layer:
support reasons, scope limits, remaining gaps

heaviest layer:
only for action-basis, explicit challenge, conflict, regression, or high-impact objects
```

Plain summary:

```text
default light
conditionally thick
raw anchors always jump-backable
```

### Small Reviewed Claim

Recommended shape:

```text
compact evidence card
not a mini full packet
```

Card front answers only:

```text
what the claim says
where the source anchor is
current support judgment
scope limit / risk note
```

Card back / expansion contains when needed:

```text
counterevidence
omissions
full anchor
detailed review
```

External analogs:

```text
GRADE Summary of Findings / Evidence Profile
ATRS Tier 1 / Tier 2
GitHub collapsed details
```

VAKS candidate implication:

```text
replace "mini full packet" thinking with a true front/back evidence card for low-risk small claims
```

### Support / Refine Collision

Recommended shape:

```text
cluster / issue / thread
not one full long record for each repeated occurrence
```

Cluster should expose:

```text
what each source contributes
what unresolved gap remains
why it cannot upgrade yet
```

Main view should show:

```text
unresolved differences
not repeated material
```

External analogs:

```text
Sentry issue grouping
GitLab open threads / move-to-issue
GitHub unresolved conversations
```

VAKS candidate implication:

```text
support/refine convergence should be represented as a cluster with unresolved gap, exemplars, and source contributions
```

### Coverage Map And Query / Run Trace

Recommended shape:

```text
do not show full audit surface for every ordinary answer
```

Ordinary answer can explicitly cover:

```text
few points this answer actually depends on
uncovered/missing items
upgrade conditions
```

High-risk action-basis adds:

```text
full coverage rows
omission checks
full run trace
external provenance
```

External analogs:

```text
Kubernetes audit levels
OpenTelemetry trace detail / sampling / caps
SLSA / BuildKit min-max provenance
```

VAKS candidate implication:

```text
coverage detail level should depend on object/risk/gate, not on ordinary query existence
```

### Scope-Fit Feedback And Activation Change

Recommended shape:

```text
categorical state machine
short reason
recurrence logic
```

Avoid:

```text
manual continuous numeric deltas without calibration
activation_delta-like pseudo precision
scope_fit_delta-like pseudo precision
```

Small feedback should capture:

```text
problem type
what to activate next time
what to avoid next time
whether this is repeated / regressed
```

Future grouping:

```text
fingerprint / recurrence can group repeated feedback events
```

External analogs:

```text
Sentry unresolved / archived / regressed / escalating
GRADE four certainty levels plus reasons
ATRS discrete risk categories
```

VAKS candidate implication:

```text
feedback is better as type + reason + recurrence/status than as uncalibrated numeric deltas
```

### Integrated Research Answer

The report's overall answer:

```text
VAKS can preserve high-risk auditability and reduce low-risk burden through:
layered display
grouped storage
unresolved-first queues
sparse provenance
categorical feedback
risk-based escalation
```

Important boundary:

```text
high-risk / action-basis is not a separate system
it is the same main path with thicker layers opened by specific triggers
```

Lightweight cases should remain in:

```text
summary
card
cluster
stub
minimal trace
```

Cases that should thicken:

```text
action-basis
explicit challenge
conflict
regression
high-impact object
known omission / important gap
```

## Segment 4: VAKS Verification Table

The original report included a summary table with Deep Research internal citation markers. Those markers are not usable as durable local citations, so this intake preserves the mapping while converting it into a VAKS-specific verification table.

| Pain Point | External Reference | Borrowable Mechanism | VAKS Landing Candidate | Adoption Degree | Schema Change? | Now / Later | Main Risk |
| --- | --- | --- | --- | --- | --- | --- | --- |
| P3 / P4 / P2 | Kubernetes Audit Policy | Risk-based audit detail levels such as metadata vs request/detail, plus omission of low-value stages or large repeated fields. | Operation convention; review-lite; future runtime audit policy. | Medium | No now | Now for convention; later for runtime | Misclassified risk can leave high-risk objects too thin. |
| P3 / P4 / P2 | UK ATRS | Tier 1 summary plus Tier 2 professional detail; thicker disclosure only for high-impact decision contexts. | Action-basis card; review-lite; operation convention. | Medium | No | Now | Tier 1 too thin may hide limits; over-applying Tier 2 brings burden back. |
| P3 / P4 | GRADE Evidence Profile / Summary of Findings | Compact evidence summary plus detailed reviewer profile; discrete certainty with reasons. | Compact evidence card; compact coverage card; anti-fake-precision note. | Medium | No | Now | Summary without expandable reasons creates overtrust. |
| P3 | GitHub PR Review UX | Viewed folding, unresolved navigation, path/type filters, collapsible details. | Queue view convention; folded resolved notes; review-lite record view. | Small to medium | No | Now | Folding can hide high-risk details if escalation signals are weak. |
| P3 / P4 | GitLab MR Discussions | Unresolved-first threads, resolved folding/reopen, move-to-issue handoff, activity filtering, summary view. | Support/refine cluster; unresolved-only queue; linked stub for non-blocking follow-up. | Medium | No | Mostly now | Auto-outdated closure is unsafe for evidence issues. |
| P4 / P3 | Sentry Issues And Breadcrumbs | Event grouping, bounded recent-context breadcrumbs, archive noisy items while continuing to record, issue states. | Feedback grouping; recurrence/fingerprint convention; future runtime grouping. | Medium | No now | Partly now; fuller later | Over-grouping hides differences; under-grouping recreates noise. |
| P4 / P3 / P2 | OpenTelemetry Tracing | Sampling, IsRecording, span links, event/link caps, batching. | Future runtime minimal/full trace policy; parked-now design reference. | Medium to large | No now; optional later | Later | Bad sampling can drop the critical abnormal run. |
| P1 / P3 / P4 | W3C PROV Family | Sparse provenance tuple plus external detailed provenance; lineage/dependence record without pretending to prove independence. | Sparse provenance convention; anti-pattern note; future runtime provenance pointer. | Medium | No | Now for convention | PROV can balloon into ontology engineering; lineage can be mistaken for independence. |
| P1 / P2 / future runtime | SLSA Provenance | Separation of external parameters, system parameters, resolved dependencies, byproducts, and min/max disclosure. | Future runtime reference; processing/access clarification inspiration. | Small now; medium later | No now; optional later | Later / parked | Too mechanical for current Markdown-first VAKS if imported directly. |

Pain point legend:

```text
P1 = source independence / lineage clarity
P2 = processing_level vs source_access clarity
P3 = coverage_map / review surface too heavy
P4 = feedback / runtime trace / log noise too heavy
```

## Pending Verification Questions

```text
Verify cited external systems and exact mechanisms before adopting.
Check overlap with VAKS existing lazy gates and current templates.
Check whether each pattern can land as operating convention/template wording before SCHEMA.
Check whether ordinary capture/query remain light.
```
