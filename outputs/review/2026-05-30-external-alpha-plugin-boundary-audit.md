---
type: architecture-audit
status: draft
created: 2026-05-30
project: verified-action-knowledge-system
scope:
  - external-alpha-review
  - plugin-boundary
  - framework-classification
review_mode: corrective synthesis
fusion_decision: classify
confidence: high
tags:
  - external-alpha
  - plugin-boundary
  - interface-contract
  - source-extraction
  - retrieval-activation
  - agent-gateway
  - vault-health
---

# External Alpha Plugin Boundary Audit

## One-Line Judgment

This round did not prove that the main framework should grow many new modules.

It proved that the framework needs a stricter adoption boundary:

```text
alpha detail != main framework change
external capability != truth layer
plugin output != reviewed knowledge
```

说人话：

```text
主框架是宪法。
外挂是工具。
接口契约是海关。

工具可以很强，但进库以后只能按我们的证据规则说话。
```

## Current Main Framework Is Not Off Track

The existing spine is still right:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

Internal verified-action loop is still right:

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

The problem discovered in this research window was not the main framework.

The problem was review language:

```text
some external systems were described as "absorbable alpha"
when they should be described as "external plugin plus thin interface contract".
```

## Adoption Classes

Future source reviews should classify every alpha into one of these buckets:

```yaml
adoption_layer:
  - core_rule
  - interface_contract
  - external_plugin
  - runtime_workbench
  - parked
  - rejected
```

Meaning:

```text
core_rule:
  A durable rule inside the verified-action framework.

interface_contract:
  A thin data shape by which outside tools hand outputs into the vault.

external_plugin:
  A replaceable capability outside the truth layer.

runtime_workbench:
  A UI, dashboard, agent shell, or operating surface.

parked:
  Interesting but not needed now.

rejected:
  Conflicts with the framework's evidence / review boundaries.
```

## Source Classification

| Source | Correct Layer | Main-Framework Residue | Must Not Import |
|---|---|---|---|
| [YiTangMJ/PageIndexRag-Web](https://github.com/YiTangMJ/PageIndexRag-Web) | external_plugin + interface_contract | optional `source_structure_map`; heavy-source navigation before point mining | PageIndex runtime as required core; structure rank as evidence support |
| [YiTangMJ/GraphRAG-Example](https://github.com/YiTangMJ/GraphRAG-Example) | retrieval / activation plugin | graph-derived `candidate_relation_suggestion`; activation trace | graph edge as reviewed relation; graph rank as confidence |
| [zzyong24/thirdspace-vault-template](https://github.com/zzyong24/thirdspace-vault-template) | agent gateway / operating protocol | progressive loading; Misa read-only boundary; Codex write-gate boundary | template directory structure as main framework |
| [zzyong24/thirdspace-dashboard](https://github.com/zzyong24/thirdspace-dashboard) | runtime_workbench / vault health plugin | dashboard can surface `review_due`, evidence gaps, stale action basis, pending feedback | dashboard state as truth or review result |
| [Kkkirito-123/ZLAgent](https://github.com/Kkkirito-123/ZLAgent) | agent runtime / gateway plugin | `agent_operation_gate`; write origin; permission tiers | Agent OS as core; MCP/tool execution as reviewed knowledge |
| [lyxhnu/langchain-miniopenclaw](https://github.com/lyxhnu/langchain-miniopenclaw/tree/main) | retrieval / activation plugin | `locator_trace`; skill-routed evidence locator | retrieval score as support; skill runtime as main chain |
| [MemGAS paper](https://arxiv.org/pdf/2505.19549) | memory activation plugin | multi-granularity activation view selection | GMM/PPR memory graph as truth; summary/keyword as fact |
| [HKUDS/RAG-Anything](https://github.com/HKUDS/RAG-Anything) | external heavy-source extractor | `source_element_manifest`; modality-specific anchors; source hygiene flags | multimodal RAG runtime as core; VLM caption as evidence support |

## Four Plugin Consolidation Model

Do not create one plugin per admired repository.

Collapse this round's external capabilities into four replaceable plugin families:

```text
1. Source Extraction Plugin
   RAG-Anything + PageIndexRAG style capabilities.

2. Retrieval / Activation Plugin
   MiniOpenClaw + GraphRAG + MemGAS style capabilities.

3. Agent Gateway Plugin
   ZLAgent + ThirdSpace Vault Template style capabilities.

4. Vault Health Plugin
   ThirdSpace Dashboard + Obsidian Dataview / Tasks / Kanban / Bases style capabilities.
```

The main framework should only define the contracts they must obey.

It should not hard-code their implementations.

## What Can Enter The Main Framework

Only these small residues are appropriate for mainline absorption.

### 1. External Tool Output Is Candidate-Only

Any output from RAG, graph search, agent memory, OCR, VLM, dashboard, or agent runtime enters as:

```text
source processing output
candidate point
candidate relation suggestion
feedback event
maintenance signal
review_due trigger
```

It does not enter as:

```text
reviewed truth
reviewed relation
truth confidence
action-ready basis
```

### 2. Source Element Manifest

Heavy or multimodal sources may expose:

```yaml
source_element_manifest:
  source_id:
  parser:
  elements:
    - element_id:
      modality: text | table | image | figure | equation | code | audio | video | mixed
      location:
      extracted_text:
      derived_description:
      source_anchor:
      extraction_confidence:
      hygiene_flags:
```

This manifest helps locate evidence.

It is not evidence by itself.

### 3. Source Structure Map

Long documents may expose:

```yaml
source_structure_map:
  source_id:
  nodes:
    - section_id:
      title:
      parent:
      page_range:
      summary:
      evidence_density_hint:
      source_anchor:
```

This helps choose where to read.

It does not prove a point.

### 4. Locator Trace

Retrieval should leave a trace:

```yaml
locator_trace:
  query:
  strategy:
  tools_used:
  candidate_anchors:
  rejected_or_low_fit_anchors:
  reason_for_selection:
```

This makes answer preparation auditable.

It does not replace evidence-aware review.

### 5. Activation View Selection

Activation may choose among multiple views:

```text
source span
candidate point
summary
keyword
reviewed node
reviewed relation
decision trace
feedback event
```

But selected view means:

```text
read this early
```

It does not mean:

```text
believe this more
```

### 6. Agent Operation Gate

Misa / external agents should have explicit permission tiers:

```text
read-only
suggest-only
candidate-write
reviewed-write
confirm-external-action
```

Near-term rule:

```text
Misa can query.
Codex / human review controls writes.
External agent memory remains quarantined.
```

### 7. Dashboard Is Health Surface

Dashboards may show:

```text
review_due
evidence gaps
source hygiene risks
pending feedback
stale action basis
conflict pressure
```

Dashboards must not decide:

```text
truth
confidence
review outcome
relation standing
```

### 8. Plugin Capability Registry

The main framework may keep a light registry:

```yaml
plugin_capability:
  name:
  layer: source_extraction | retrieval_activation | agent_gateway | vault_health
  allowed_outputs:
  forbidden_outputs:
  review_authority: vault_only
```

Purpose:

```text
Keep plugins useful but unable to smuggle authority into the truth layer.
```

## What Should Stay Outside Main Framework

Do not absorb:

```text
OCR / parser stack
multimodal RAG runtime
vector store implementation
graph database implementation
PageRank / GMM / router algorithm
agent OS runtime
MCP installation system
dashboard app
Obsidian plugin implementation
```

These can be excellent external tools.

They should remain swappable.

## Reinterpret Existing Review Artifacts

Some files from this window say `fusion_decision: adapt`.

For Pro review, interpret them with this correction:

```text
adapt = adapt as plugin/interface unless explicitly marked core_rule
```

Specific correction:

```text
PageIndexRAG / GraphRAG artifact:
  read as source-extraction + retrieval plugin boundary,
  not a new core stage.

ThirdSpace Vault artifact:
  read as agent operating protocol,
  not a replacement vault framework.

ThirdSpace Dashboard artifact:
  read as vault health workbench,
  not a review engine.

ZLAgent artifact:
  read as agent gateway and permission inspiration,
  not Agent OS core.

MiniOpenClaw artifact:
  read as skill-routed evidence locator,
  not required retrieval architecture.

MemGAS artifact:
  read as memory activation idea,
  not truth memory layer.

RAG-Anything artifact:
  already correctly marked external-plugin-adapter.
```

## Pro Review Questions

Ask Pro to challenge these points:

```text
1. Are any proposed main-framework residues still too heavy?
2. Is any plugin capability accidentally being granted truth authority?
3. Is `source_element_manifest` narrow enough for multimodal/heavy sources?
4. Is `locator_trace` useful enough without becoming another burden?
5. Should `agent_operation_gate` live in main docs now, or wait until Misa write-capability exists?
6. Does the four-plugin consolidation avoid tool sprawl?
7. Are any reviewed artifacts misleading because their frontmatter says `adapt`?
```

## Recommended Next Move

Do not rewrite the framework yet.

Recommended next patch, if Pro agrees:

```text
1. Add a short adoption-layer rule to the architecture review template.
2. Add a small "External Plugin Boundary" section to ARCHITECTURE_PRINCIPLES.md.
3. Optionally add source_element_manifest / locator_trace as optional schema extensions.
4. Leave all implementations outside the main framework.
```

## Bottom Line

This research window's strongest result is not another module.

It is this boundary:

```text
The vault can borrow frontier capabilities without importing their authority model.
```

