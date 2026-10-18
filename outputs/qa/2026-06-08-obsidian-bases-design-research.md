---
type: qa
status: draft
created: 2026-06-08
topic: obsidian-bases-design-research
truth_boundary: research_summary_not_truth_layer
workspace: C:\Users\Administrator\Documents\资料库
formal_vault: H:\Obsidian\资料库
related_decisions:
  - wiki/decisions/2026-05-26-obsidian-bases-properties-primary-view-layer.md
related_patterns:
  - wiki/patterns/obsidian-bases-linked-workbench-views.md
  - wiki/patterns/property-driven-context-workbench.md
  - wiki/patterns/scope-dashboard-live-context-surface.md
related_sources:
  - raw/repos/2026-05-26-obsidian-base-hub-source.md
  - raw/repos/2026-05-27-kepano-obsidian-source.md
  - raw/repos/2026-05-27-dusk-obsidian-vault-source.md
external_sources:
  - https://obsidian.md/help/bases
  - https://obsidian.md/help/bases/create-base
  - https://obsidian.md/help/bases/views
  - https://obsidian.md/help/bases/syntax
  - https://obsidian.md/help/bases/functions
---

# Obsidian Bases Design Research

## AI-readable preamble

This is a research summary for the first VAKS Obsidian Bases rollout.

It is not a `.base` file, not a schema change, not a truth layer, not a promotion record, and not Obsidian sync.

Recommended direction:

```text
Start with sources.base + decisions.base after review.
Do not build patterns.base / claims.base / review-queue.base until the smallest property cleanup is approved.
Treat dev-context/scope dashboard Bases as a later workbench lane.
```

## 0. Current state checked

Repository:

```text
C:\Users\Administrator\Documents\资料库
```

Formal vault:

```text
H:\Obsidian\资料库
```

Current `.base` state:

```text
repo wiki/bases: no Base files after removing the prior trial files
formal vault: path exists, .base count = 0
```

No source, claim, pattern, decision, review-candidate, or Obsidian vault property was changed in this research pass.

## 1. Local material review

### 1.1 Bases primary-view-layer decision

File:

```text
wiki/decisions/2026-05-26-obsidian-bases-properties-primary-view-layer.md
```

Hard constraints:

- Obsidian Properties + Bases are accepted as first-stage view / lightweight database layer.
- Bases are not verification, RAG, graph database, compiler, or truth source.
- `.base` files are local YAML and can be versioned/diffed.
- The first suggested set is sources, claims, patterns, anti-patterns, decisions.
- Implementation timing is explicitly after core frontmatter fields stabilize.

Still valid:

- Markdown/YAML remains the system of record.
- Bases should improve human scan/review workflow only.

Needs refresh:

- The decision predates the current official 1.10-era documentation for list and map views. This does not invalidate the decision, but it means design should now acknowledge table/cards/list/map, with map gated by the Maps plugin.

### 1.2 Obsidian Bases linked workbench views

File:

```text
wiki/patterns/obsidian-bases-linked-workbench-views.md
```

Hard constraints:

- A Base filters one class of Markdown nodes and exposes a lightweight workbench.
- Avoid per-project/per-node Base duplication.
- Do not let Base view design define schema.
- Use a small global set:

```text
wiki/bases/sources.base
wiki/bases/claims.base
wiki/bases/patterns.base
wiki/bases/decisions.base
wiki/bases/review-queue.base
```

Raw/source alignment:

- Anchored by `raw/repos/2026-05-26-obsidian-base-hub-source.md`.
- The local snapshot exists:

```text
raw/repos/_snapshots/Obsidian-Base-Hub-ca4c927b42a74c63911aa5aa97d1d0694e6e126b.zip
```

- The snapshot contains real `.base` files:

```text
010 - Inbox/DDBB - Inbox.base
020 - Projects/999 - Demo Project/DDBB Demo Project.base
030 - Areas/999 - Demo Area/DDBB Demo Area.base
040 - Tasks/DDBB Tasks.base
050 - Daily/DDBB Daily.base
060 - Meetings/DDBB Meetings.base
070 - People/DDBB People.base
080 - Locations/DDBB Locations.base
```

Actual extracted Base Hub examples confirm:

- `file.inFolder(...)` filters.
- `projects.contains(link("Demo Project"))` for list/link filtering.
- `groupBy`, `sort`, `order`, `columnSize`, `cardSize`.
- `formulas`, e.g. counting backlinks.

Important negative evidence:

- The actual snapshot mixes property names such as `projects/proyectos`, `areas/áreas`, `rol/role`, `minutes/minutos`.
- This directly supports the warning that VAKS should stabilize field names before making rich grouped views.

### 1.3 Property-driven context workbench

File:

```text
wiki/patterns/property-driven-context-workbench.md
```

Hard constraints:

- Use metadata and views to surface context instead of moving files.
- This is an activation/workbench pattern, not a truth-layer pattern.
- Strong fit for `MEMORY_TIER.md` and `DEV_CONTEXT.md`, not necessarily first-batch source/claim/pattern/decision management.

Raw/source alignment:

- Anchored by `raw/repos/2026-05-27-kepano-obsidian-source.md`.
- The source record has strong metadata: repo URL, checked commit, release/date observations, file counts, and inspected surfaces.
- The temp clone still exists:

```text
%TEMP%\codex-kepano-obsidian
```

Information density:

- Good enough for design alignment.
- It records `.obsidian/types.json`, `Templates/Bases/*.base`, `Categories/*.md`, and `Related.base` as source/code surfaces.

Design relevance:

- Useful for a later `dev-context.base` or related-context workbench.
- It should not drive the first `sources.base` / `decisions.base` design except as a general warning: keep fields reusable and avoid folder movement as the main state mechanism.

### 1.4 Scope dashboard live context surface

File:

```text
wiki/patterns/scope-dashboard-live-context-surface.md
```

Hard constraints:

- A scope dashboard suggests context; it is not evidence and not truth.
- It can gather core/support/risk/task/cold candidates before dev-context pack selection.
- It should not replace the dev context pack or review gate.

Raw/source alignment:

- Anchored by `raw/repos/2026-05-27-dusk-obsidian-vault-source.md`.
- The source record is unusually strong: it includes a source-anchor matrix for `template_area.md`, monthly notes, Mail Box, Vault Onboarding, and project README surfaces.
- The temp clone still exists:

```text
%TEMP%\codex-dusk-obsidian-vault
```

Design relevance:

- Strong for future `dev-context.base` / scope dashboard design.
- Weak for immediate `sources.base` and `decisions.base`.
- The source is plugin-heavy and explicitly legacy, so do not copy the runtime.

### 1.5 Existing Bases + Properties QA

File:

```text
outputs/qa/2026-05-26-obsidian-bases-properties-layer-check.md
```

Hard constraints:

- Bases + Properties are view/metadata layer, not verified truth layer.
- Dataview remains useful for complex queries and JS-style dashboards.
- Datacore remains a future/power-user option, not first-stage dependency.
- Do not turn Obsidian plugin ecosystem strength into verified architecture evidence.

Needs refresh:

- The broad judgment still holds.
- Current official docs now make list/map view details explicit. Map requires the Maps plugin and Obsidian 1.10.
- Board/Kanban is not a core Base layout in the official docs; do not use board as first-batch review-queue design.

## 2. Current official Bases syntax and limits

Official docs checked:

- `https://obsidian.md/help/bases`
- `https://obsidian.md/help/bases/create-base`
- `https://obsidian.md/help/bases/views`
- `https://obsidian.md/help/bases/syntax`
- `https://obsidian.md/help/bases/functions`

### 2.1 Data model

Official docs state that Bases is a core plugin for database-like views of files and their properties. Data stays in local Markdown files and properties; views are described by Bases syntax and can be saved as `.base` files or embedded in Markdown code blocks.

Implication for VAKS:

```text
Markdown/YAML still wins.
.base is only a rendering/query file.
```

### 2.2 File location

Official docs say a new base can be created in the active folder or selected folder, and embedded with `![[File.base]]` or `![[File.base#View]]`.

Implication:

```text
Keeping repo .base files under wiki/bases is Git-friendly.
They will only render in an Obsidian vault that contains those files.
```

This matches the current project boundary:

```text
repo = version/diff/design
H:\Obsidian\资料库 = render/use
```

### 2.3 Filters

Official syntax supports:

- Global base filters.
- Per-view filters.
- `and` / `or` / `not` filter groups.
- File properties such as `file.ext`, `file.folder`, `file.name`, `file.path`, `file.tags`, `file.links`.
- Note properties from YAML frontmatter, either by name or `note.property`.

Good VAKS filters:

```yaml
file.ext == "md"
file.inFolder("raw")
type == "source"
status == "source-captured"
```

Avoid for first batch:

```text
file.backlinks
```

Reason:

- Official docs mark `file.backlinks` as performance heavy and not automatically refreshed.

### 2.4 List fields

Official functions support list handling:

- `list(x)` to normalize a single value or list into a list.
- `contains`
- `containsAll`
- `containsAny`
- `filter`
- `join`
- `map`
- `reduce`
- `unique`
- `sort`

Implication:

```text
List fields like sources, source_libraries, tags, decision_scope, projects can be displayed and filtered.
For mixed single/list fields, use list(field) in formulas or keep first Base views simple.
```

### 2.5 Formulas

Formulas can define derived columns in the `.base` file and can be used in filters/views.

Useful for VAKS:

```text
is_review_due = next_review <= today()
confidence_label = confidence.toString()
source_family_display = list(source_family).join(", ")
```

Boundary:

```text
Formula output is view metadata, not source-of-truth metadata.
Do not use formulas to silently redefine review status, truth confidence, or promotion readiness.
```

### 2.6 Views

Current official layouts:

```text
table
cards
list
map
```

Important limits:

- Map requires the Maps plugin and Obsidian 1.10.
- Additional layouts can come from community plugins.
- Official docs mention grouping by only one property.
- Sort behavior depends on property type.

Implication:

```text
First batch should use table views only.
Cards can wait.
Map is irrelevant.
Board/Kanban is not a core Base view and should not be used for review queue.
```

### 2.7 Mixed types

Official docs say sort options depend on property type: text sorts alphabetically, number sorts numerically, date sorts chronologically.

Inference for VAKS:

```text
Mixed numeric/string confidence values will make sorting/grouping brittle.
```

For a temporary view-only workaround, a formula can display `confidence.toString()`.

For a durable Base, the property should be normalized instead.

## 3. Current field health

Field counts from current repo frontmatter.

### 3.1 Sources

Scope:

```text
raw/**/*.md, excluding segments.md and image-index.md
```

Counts:

```text
files: 58
type: source 57, source_record 1
status: source-captured 56, processed 1, missing 1
verification_status: present 50, missing 8
source_status: present 39, missing 19
processing_tier: present 16
processing_level: present 40
knowledge_status: present 16
review_pressure: present 16
source_family: present 35
```

Diagnosis:

- `status` is good enough for `sources.base`.
- `processing_tier` vs `processing_level` is the biggest field-name conflict.
- `knowledge_status` and `review_pressure` only exist on newer intake records.
- `source_status` is not clean enough to be the main grouping field.

### 3.2 Claims

Scope:

```text
wiki/claims/*.md
```

Counts:

```text
files: 9
type: claim 9
status: cross-checked 6, accepted 2, verified 1
verification_status: cross-checked 7, source-reviewed 1, code-inspected 1
confidence: 4 x6, 5 x1, high x2
evidence_level: secondary 5, primary 3, primary-source 1
```

Diagnosis:

- Claims are small and mostly clean.
- `confidence` is mixed numeric/string and should be normalized before sorting/grouping.
- `sources` vs `source` differs between claim files, but display can tolerate this; filtering should avoid it in first version.

### 3.3 Patterns

Scope:

```text
wiki/patterns/*.md
```

Counts:

```text
files: 74
status: active 18, candidate 28, draft 19, pattern-candidate 9
adoption_status: 9 values
verification_status: present 26, missing 48
confidence: high 47, medium 26, medium_high 1
evidence_level: present 26, missing 48
next_review: present 26, missing 48
```

Diagnosis:

- Patterns need the most cleanup before a useful Base.
- `candidate` and `pattern-candidate` overlap.
- `adoption_status` has too many near-synonyms.
- `verification_status/evidence_level/next_review` are missing from most older records.
- `medium_high` should be normalized.

### 3.4 Decisions

Scope:

```text
wiki/decisions/*.md
```

Counts:

```text
files: 10
type: decision 10
status: active 9, accepted 1
outcome: adopted 7, missing 3
verification_status: active 7, missing 3
confidence: high 10
next_review: 2026-06-03 x7, missing 3
```

Diagnosis:

- Decisions are clean enough for a first Base.
- Missing `outcome/next_review` on 3 older decisions can be tolerated at first.

### 3.5 Review candidates / candidate distillations

Scope:

```text
outputs/review/**/*.md, excluding architecture/tests/directories/current_main_vault_records
```

Matched:

```text
strict review-candidate: record_type == review-candidate, 5
candidate_distillation: type == candidate_distillation, 13
type == review-candidate, 1
```

Diagnosis:

- There are two different objects:

```text
review-candidate = fixed review object for possible formal writeback
candidate_distillation = medium candidate comprehension/output
```

- Do not combine them into one authoritative `review-queue.base`.
- First view should either:

```text
review-candidates.base = strict fixed review objects only
candidate-distillations.base = candidate comprehension queue only
```

or defer both until the workflow name is settled.

## 4. Five Base design drafts

These are design drafts only. Do not implement until approved.

### 4.1 `sources.base`

Readiness:

```text
Can build now, but avoid overusing source_status.
```

Filter:

```text
file.ext == "md"
file.inFolder("raw")
type == "source" or type == "source_record"
```

Suggested columns:

```text
file.name
status
verification_status
processing_level
processing_tier
knowledge_status
review_pressure
source_family
last_verified
next_review
file.path
```

Views:

```text
All sources
Unverified or single-source
New intake missing boundary fields
By source_family
```

Sort/group:

```text
Sort: file.mtime desc or captured_at desc if available.
Group: verification_status or source_family.
```

Pre-cleanup required:

```text
No, but high-value cleanup is processing_level -> processing_tier.
```

### 4.2 `decisions.base`

Readiness:

```text
Can build now.
```

Filter:

```text
file.ext == "md"
file.inFolder("wiki/decisions")
type == "decision"
```

Suggested columns:

```text
file.name
status
outcome
decision_scope
confidence
verification_status
last_verified
next_review
replaces
superseded_by
file.path
```

Views:

```text
All decisions
Review due
Supersession / replacement
```

Sort/group:

```text
Group: status
Sort: next_review asc, then file.name
```

Pre-cleanup required:

```text
No. Missing outcome/next_review on 3 older files can be shown as blank.
```

### 4.3 `patterns.base`

Readiness:

```text
Do not build rich grouping yet.
Build only an ungrouped audit view if needed.
```

Filter:

```text
file.ext == "md"
file.inFolder("wiki/patterns")
type == "pattern"
```

Suggested columns:

```text
file.name
status
adoption_status
verification_status
evidence_level
confidence
source_libraries
last_verified
next_review
file.path
```

Views:

```text
All patterns
Adopted / active
Candidate / draft
Missing review metadata
```

Sort/group:

```text
Group: adoption_status only after normalization.
Sort: next_review asc after missing dates are understood.
```

Pre-cleanup required:

```text
Yes: status/adoption_status/confidence.
```

### 4.4 `claims.base`

Readiness:

```text
Can build a simple audit view after confidence normalization.
```

Filter:

```text
file.ext == "md"
file.inFolder("wiki/claims")
type == "claim"
```

Suggested columns:

```text
file.name
status
verification_status
evidence_level
confidence
sources
source
last_verified
next_review
file.path
```

Views:

```text
All claims
Cross-checked
Needs review date
High confidence
```

Sort/group:

```text
Group: verification_status
Sort: confidence only after normalization.
```

Pre-cleanup required:

```text
Recommended: confidence numeric/string normalization.
```

### 4.5 `review-queue.base`

Readiness:

```text
Defer or split.
```

Option A:

```text
review-candidates.base
filter: record_type == "review-candidate" or type == "review-candidate"
purpose: fixed review objects for possible writeback
```

Suggested columns:

```text
file.name
record_type
status
knowledge_status
review_status
promotion_target
candidate_body_location
body_hash
candidate_lint
approval_integrity
file.path
```

Option B:

```text
candidate-distillations.base
filter: type == "candidate_distillation"
purpose: medium candidate comprehension outputs
```

Suggested columns:

```text
file.name
status
knowledge_status
processing_tier
processing_level
review_pressure
source_ref / source
file.path
```

Do not use:

```text
board / Kanban
```

Reason:

- Board is not a core official Base layout.
- Review queue status transitions are governed by `REVIEW_QUEUE.md`, Evidence Packet, lint, approval integrity, and promotion gates, not by dragging cards in a view.

## 5. Minimum property cleanup, ranked

### P0: normalize processing field name

Issue:

```text
processing_level present 40 source records
processing_tier present 16 source records
some new records have both
```

Affected Base:

```text
sources.base
candidate-distillations.base
```

Impact:

```text
Without cleanup, filters and columns need both fields.
```

Recommended fix:

```text
Keep processing_tier as canonical because SOURCE_INTAKE now names processing_tier.
Either migrate processing_level -> processing_tier or create a temporary formula/display fallback in Base.
```

Preferred route:

```text
For first Base, display both.
For cleanup pass, migrate only raw/source cards after approval.
```

### P1: normalize confidence

Issue:

```text
claims: numeric 4/5 plus high
patterns: high/medium plus medium_high
sources: numeric 3/4 plus high/medium
outputs: medium-high and other one-off values
```

Affected Base:

```text
claims.base
patterns.base
sources.base if source confidence is shown
```

Impact:

```text
Mixed types make sorting/grouping brittle.
```

Recommended fix:

```text
Do not delete old meaning blindly.
Choose one canonical scale first.
For UI grouping, use low / medium / high strings.
If numeric granularity matters, preserve it in confidence_score or a note field.
```

Preferred route:

```text
First normalize claims + patterns only.
Do not touch raw source confidence until source schema cleanup is approved.
```

### P2: normalize pattern status

Issue:

```text
active 18
candidate 28
draft 19
pattern-candidate 9
```

Affected Base:

```text
patterns.base
```

Impact:

```text
candidate and pattern-candidate split the same conceptual bucket.
```

Recommended fix:

```text
Use status for lifecycle only:
draft | candidate | active | archived | rejected | superseded
Map pattern-candidate -> candidate.
```

### P3: normalize pattern adoption_status

Issue:

```text
adapt
adapt-later
adopt
adopt-candidate
adopt-lite
adopt-soon
adopted
candidate
watch
```

Affected Base:

```text
patterns.base
```

Impact:

```text
Grouping is noisy and hard to scan.
```

Recommended fix:

```text
Minimal value set:
watch | adapt | adopt-candidate | adopted | parked | rejected
```

Potential mapping:

```text
adopt -> adopt-candidate unless already formally adopted
adopt-soon -> adopt-candidate
adopt-lite -> adapt
adapt-later -> watch or parked
candidate -> adopt-candidate
```

Do not run this automatically; confirm mapping one value at a time.

### P4: verification_status compaction

Issue:

```text
Across outputs/review there are many one-off process values.
Core wiki sources/patterns/claims/decisions are less chaotic but still inconsistent.
```

Affected Base:

```text
patterns.base
review-candidates.base
candidate-distillations.base
```

Impact:

```text
Grouping gets fragmented.
```

Recommended fix:

```text
Do not globally rewrite outputs/review first.
For wiki nodes, prefer stable values:
unverified
single-source
primary-source
cross-checked
reviewed
active
superseded
rejected
```

Boundary:

```text
Process-only statuses should move to review_note, lint result, or closeout metadata only after a separate protocol decision.
```

### P5: old sources missing knowledge_status / review_pressure

Issue:

```text
knowledge_status present 16/58
review_pressure present 16/58
```

Affected Base:

```text
sources.base
```

Impact:

```text
New source cards are clean; old records show blank columns.
```

Recommended fix:

```text
Not required before first sources.base.
When approved, fill old raw source cards with:
knowledge_status: raw
review_pressure: none
```

## 6. Direct recommendation

### First implementation batch

Build only:

```text
wiki/bases/sources.base
wiki/bases/decisions.base
```

But keep them conservative:

```text
table views only
few columns
no formulas that imply review/truth
no board
no map
no Obsidian sync until approved
```

### Second batch

Before building:

```text
claims.base
patterns.base
```

Do:

```text
confidence cleanup
pattern status cleanup
pattern adoption_status cleanup
```

### Third batch

Split rather than combine:

```text
review-candidates.base
candidate-distillations.base
```

Do not create a generic `review-queue.base` until the queue object taxonomy is clearer.

### Later workbench lane

Use Kepano/Dusk evidence for:

```text
dev-context.base
scope dashboard
related context surface
closeout/cooling dashboard
```

Do not let this lane leak into first-batch truth/review views.

## 7. What is evidence vs inference

Evidence-backed:

- Base Hub snapshot has real `.base` files with filters, groupBy, sort, order, formulas, and list/link filtering.
- Base Hub also has field-name inconsistency, so schema-first is not theoretical.
- Kepano source record supports property-driven context workbench, but only for activation/dev-context.
- Dusk source record supports scope dashboard and closeout/cooling surfaces, but is plugin-heavy and legacy.
- Official docs support `.base` files, embedded Base code blocks, table/cards/list/map layouts, filters, formulas, functions, and one-property grouping.

Inference:

- Mixed numeric/string confidence will make durable sorting/grouping brittle. Official docs establish type-dependent sorting, but do not provide a VAKS-specific mixed-field failure case.
- `review-queue.base` should be split because current repo has both strict review-candidates and candidate_distillations with different meanings.
- `sources.base` can tolerate old blank fields better than `patterns.base`, because source status is already mostly `source-captured` and missing boundary fields can be visibly audited.

## 8. Stop rules for next step

Before implementation:

```text
Confirm whether to keep research-only or build first two Bases.
If building, do not sync to H:\Obsidian\资料库 unless explicitly approved.
If cleaning fields, do one field family at a time.
Do not commit unless explicitly requested.
```
