---
type: architecture-review-proposal
status: draft
created: 2026-05-30
project: verified-action-knowledge-system
review_source: Pro second-pass review
review_verdict: accept-with-tightening
closeout_verdict: research-only-guarded
scope:
  - plugin-boundary
  - external-alpha-classification
  - interface-contract-tightening
mainline_changed: false
mainline_adoption: not-approved
merge_instruction: do-not-merge-into-main-architecture
assessment_confidence: high
tags:
  - pro-review
  - plugin-boundary
  - interface-contract
  - no-mainline-change
  - guarded-closeout
  - alpha-detail-mining
---

# Pro-Tightened Plugin Boundary Proposal

## Purpose

This file is a standalone second-pass proposal and guarded closeout record.

It applies Pro's tightening comments to the alpha-plugin-boundary audit, without changing the main architecture docs.

Current status:

```text
research artifacts only
no mainline architecture change
no SCHEMA expansion
no implementation
no commit
not approved for mainline merge
```

## Closeout Guard

This file is not a mainline patch.

It must not be copied wholesale into:

```text
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
SCHEMA.md
SOURCE_INTAKE.md
README.md
```

It records research discipline only:

```text
external alpha review result
plugin-boundary guardrails
dangerous wording corrections
parked future interface ideas
```

Current closeout rule:

```text
Do not add this to the main architecture now.
Do not create plugin registry.
Do not expand SCHEMA.
Do not implement adapters.
Do not turn agent gateway into a project goal.
```

If this topic is reopened later, any mainline change must be proposed as a separate tiny patch and reviewed against the existing verified-action loop.

## One-Line Decision

The research direction is accepted, but compressed.

```text
accept with tightening
```

Meaning:

```text
Keep the main route.
Do not expand Truth Core.
Keep plugin capabilities outside.
Only define a few boundary rules and thin interface contracts.
```

## Main Route Stays Fixed

Do not replace the main framework with a general second-brain / PARA / RAG / agent-runtime flow.

The route remains:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

The internal verified-action loop remains:

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

Why:

```text
Review must stay before Connect.
External systems may help find, extract, route, display, or propose.
Only review decides what can support action.
```

## Core Discipline To Keep

The central rule from the previous audit stays:

```text
alpha detail != main framework change
external capability != truth layer
plugin output != reviewed knowledge
```

Pro tightening adds:

```text
All plugin outputs are typed as candidate, trace, signal, or maintenance pressure
unless reviewed inside the vault.
```

## Adoption Layer Rule

Future alpha reviews should not use bare `fusion_decision: adapt` as the main judgment.

Use:

```yaml
adoption_layer:
  - core_rule
  - interface_contract
  - external_plugin
  - runtime_workbench
  - parked
  - rejected
```

Recommended frontmatter pattern:

```yaml
fusion_decision: classify
adoption_layer: external_plugin
assessment_confidence: medium-high
```

Allowed meanings:

```text
core_rule:
  Durable rule inside the verified-action framework.

interface_contract:
  Thin data shape by which an outside tool hands outputs into the vault.

external_plugin:
  Replaceable capability outside the truth layer.

runtime_workbench:
  UI, dashboard, agent shell, or operating surface.

parked:
  Interesting but not needed now.

rejected:
  Conflicts with evidence / review boundaries.
```

## Proposed Core Rules

These rules are research guardrails.

They are not approved mainline additions in this closeout.

If reopened later, only boundary principles may be considered.

Guard for `core_rule`:

```text
core_rule may only preserve an existing verified-action boundary.
It cannot introduce a new module, schema family, runtime, plugin system, or authority surface.
```

### 1. External Tool Output Is Candidate-Only

External tools may locate, extract, retrieve, summarize, rank, route, visualize, or propose.

Their outputs may enter the vault only as:

```text
source processing output
candidate point
candidate relation suggestion
locator trace
activation trace
feedback event
maintenance signal
review_due_candidate
review_due_signal
```

They cannot create:

```text
reviewed truth
reviewed relation
truth confidence
evidence support judgment
evidence sufficiency judgment
action-ready basis
```

External tools cannot directly set an accepted vault `review_due` state.

They may only propose review pressure:

```text
review_due_candidate
review_due_signal
maintenance_signal
```

### 2. Interface Contract, Not Implementation

The framework may define thin contracts for external plugin outputs.

It must not import plugin runtimes into core.

Stay outside core:

```text
OCR stack
multimodal RAG runtime
vector store
graph database
PageRank / GMM / PPR / router algorithm
agent OS runtime
MCP installation system
dashboard app
Obsidian plugin implementation
```

### 3. Activation Is Not Authority

Retrieval or activation may decide:

```text
what to read early
```

It cannot decide:

```text
what is true
what supports a point
what deserves confidence
what can support action
```

### 4. Dashboard Is Health Surface

Dashboard / workbench views may show:

```text
review_due
evidence gaps
source hygiene risks
pending feedback
stale action basis
conflict pressure
```

They cannot decide:

```text
truth
confidence
review outcome
relation standing
promotion
```

Dashboard can read review state.

Dashboard cannot compute review state.

## Proposed Interface Contracts

These are optional contracts, not required schema expansions.

They should be introduced cautiously and only where needed.

### 1. Source Extraction Contract

Use only for heavy / multimodal / complex sources:

```text
PDF
image-heavy document
table-heavy document
figure / equation / code-heavy source
audio / video transcript
complex webpage
large repo documentation
```

Pro-tightened shape:

```yaml
source_element_manifest:
  source_id:
  extractor:
  elements:
    - element_id:
      modality: text | table | image | figure | equation | code | audio | video | mixed
      location:
      extracted_text:
      derived_description:
      source_anchor:
      extraction_quality_hint: high | medium | low | unknown
      hygiene_flags:
```

Rules:

```text
extraction_quality_hint means extraction quality, not truth confidence.
derived_description is model-generated description, not evidence.
VLM caption / OCR summary / table description cannot count as evidence support by itself.
```

### 2. Source Navigation Contract

Use only for long / high-impact sources:

```text
long paper
official manual
technical specification
large source package
legal / financial / policy report
complex repo docs
```

Pro-tightened shape:

```yaml
source_structure_map:
  source_id:
  structure_basis:
  structure_quality_hint: high | medium | low | unknown
  nodes:
    - node_id:
      title:
      parent:
      source_anchor:
      evidence_granularity:
      evidence_locator_hint:
      selection_note:
```

Rules:

```text
structure_quality_hint means map quality, not truth confidence.
evidence_locator_hint means where evidence may be found, not evidence strength.
This map helps choose where to read.
It does not prove a point.
```

### 3. Retrieval / Locator Contract

Use when retrieval decisions should be replayable:

```yaml
locator_trace:
  query:
  strategy:
  tools_used:
  candidate_anchors:
  locator_fit: high | medium | low | unknown
  reason_for_selection:
  rejected_or_low_fit_anchors:
  limitations:
  support_not_assessed: true
```

Rules:

```text
locator_trace can explain how candidate evidence was found.
locator_trace cannot say the evidence supports the point.
Do not use supports_candidate_point: likely.
Use locator_fit language only.
locator_fit is retrieval fit, not evidence support.
Support belongs to Evidence Support Check and Review.
```

### 4. Agent Gateway Contract

This belongs in agent / tool-safety boundaries, not Truth Core schema.

Closeout status:

```text
accepted as boundary concept
parked as interface contract
AGENTS / TOOL_SAFETY only if reopened later
not SCHEMA
not SOURCE_INTAKE
not main architecture
```

Pro-tightened shape:

```yaml
agent_operation_gate:
  actor:
  operation:
  permission: safe | confirm | forbidden
  allowed_outputs:
  forbidden_outputs:
  write_origin:
```

Near-term permissions:

```text
Misa:
  read context
  submit feedback
  propose candidate
  propose review_due_candidate

Misa cannot:
  write reviewed nodes
  write reviewed relations
  change truth confidence
  change schema
  change architecture
  promote knowledge

Codex local:
  may write review artifacts and approved patches under user instruction.

Reviewed core write:
  human-confirmed only.
```

Avoid this external-agent tier:

```text
reviewed-write
```

If this phrase is ever retained, it must mean:

```text
human-confirmed / Codex-local only
never external agent
```

## Plugin Families

Do not create one plugin per admired repository.

Keep four replaceable capability families:

```text
1. Source Extraction Plugin
   RAG-Anything + PageIndexRAG style capabilities.

2. Retrieval / Activation Plugin
   MiniOpenClaw + GraphRAG + MemGAS style capabilities.

3. Agent Gateway Plugin
   ZLAgent + ThirdSpace Vault Template style capabilities.

4. Vault Health Plugin
   ThirdSpace Dashboard + Obsidian Bases / Dataview / Tasks / Kanban style capabilities.
```

Each plugin family may output only:

```text
candidate
trace
signal
maintenance pressure
```

unless reviewed inside the vault.

## Classification Of This Research Round

| Source | Final Classification | Keep | Do Not Import |
|---|---|---|---|
| RAG-Anything | external_plugin + interface_contract | source_element_manifest; source anchors; extraction quality hints | multimodal RAG runtime as core; VLM caption as support |
| PageIndexRAG-Web | external_plugin + interface_contract | source_structure_map; heavy-source navigation | structure rank as support; required PageIndex runtime |
| GraphRAG-Example | external_plugin | candidate relation suggestions; graph activation trace | graph edge as reviewed relation; graph rank as confidence |
| MiniOpenClaw | external_plugin + interface_contract | locator_trace; skill-routed evidence finding | support judgment by retriever; skill runtime as main chain |
| MemGAS | external_plugin | multi-granularity activation views | memory graph as truth; GMM/PPR as trust |
| ZLAgent | external_plugin + parked future boundary | agent_operation_gate concept; write origin; permission ideas | Agent OS core; MCP runtime; autonomous reviewed memory; mainline agent gateway |
| ThirdSpace Vault Template | runtime_workbench + future boundary | progressive loading; Misa/Codex boundary | vault template as main framework |
| ThirdSpace Dashboard | runtime_workbench | health/risk views | dashboard as review engine |

## Explicit Rejects

Reject:

```text
graph rank as confidence
retrieval score as support
dashboard as review engine
agent memory as reviewed memory
parser / OCR / VLM output as evidence support
LLM-extracted graph as reviewed knowledge graph
external agent reviewed-write
external plugin setting accepted review_due
```

## Parked Items

Park for later:

```text
custom dashboard plugin
Misa writable gateway
full RAG-Anything pipeline integration
multimodal extraction runtime
graph database / vector store implementation
source_structure_map as mandatory schema field
plugin registry file
agent_operation_gate as active mainline interface
```

## Mainline Status

Do not rewrite the architecture.

Do not apply a mainline patch from this file in this closeout.

```text
current decision:
  keep as outputs/review research artifact only
```

Future only if the user explicitly reopens this topic:

```text
1. Consider a tiny adoption_layer rule for review templates.
2. Consider a tiny External Plugin Boundary paragraph.
3. Consider optional heavy-source examples outside SCHEMA.
4. Consider AGENTS / TOOL_SAFETY agent boundary language.
```

Still forbidden in this closeout:

```text
large SCHEMA.md rewrite
plugin registry file
dashboard plugin
API / MCP runtime
Misa write gateway
copying this whole proposal into main docs
```

## Residual Questions If Reopened Later

If this topic is reopened, check:

```text
1. Are the four core rules still too broad?
2. Are the four interface contracts thin enough?
3. Should source_element_manifest / source_structure_map stay only in SOURCE_INTAKE, not SCHEMA?
4. Should agent_operation_gate be documented now, or parked until Misa write capability exists?
5. Is locator_fit safe enough, or should locator_trace avoid fit labels entirely?
6. Is "Dashboard can read review state but cannot compute review state" strict enough?
7. Should Plugin Capability Registry be removed from near-term mainline entirely and kept only as a future idea?
```

## Final Bottom Line

The strongest result of this research window is not a new module.

It is this discipline:

```text
The vault can borrow frontier capabilities without importing their authority model.
```

Current closeout:

```text
Do not merge now.
Keep as research artifact.
Use it as a guardrail if future plugin or agent work reopens.
```

Do not merge the external systems themselves.
