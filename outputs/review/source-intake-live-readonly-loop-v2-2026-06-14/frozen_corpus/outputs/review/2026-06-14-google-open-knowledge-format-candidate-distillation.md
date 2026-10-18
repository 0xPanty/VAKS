---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
source_ref: raw/articles/2026-06-14-google-open-knowledge-format-source.md
derived_from:
  - https://github.com/GoogleCloudPlatform/knowledge-catalog/blob/main/okf/SPEC.md
  - https://cloud.google.com/blog/products/data-analytics/how-the-open-knowledge-format-can-improve-data-sharing/?hl=en
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
borrow_value: strong
borrow_order:
  - "P1: format-over-platform posture for VAKS external bundle/export design"
  - "P1: index.md progressive disclosure as agent context loading pattern"
  - "P1: Markdown/YAML concept document as interoperable source/candidate/review surface"
  - "P2: log.md change history for source/update/use-ledger inspired records"
  - "P2: producer/consumer independence as API/viewer/retrieval boundary"
  - "P3: OKF compatibility/export sandbox after VAKS P0/P1 gates stabilize"
avoid:
  - "Do not weaken VAKS schema to OKF's minimal `type`-only conformance."
  - "Do not treat OKF citations as VAKS evidence support."
  - "Do not treat OKF links as reviewed relations."
  - "Do not let enrichment agents write reviewed knowledge directly."
  - "Do not replace VAKS action_readiness / evidence_sufficiency with OKF bundle conformance."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "designing VAKS import/export, public bundle format, agent-readable documentation layer, or source/context-pack serialization"
  support_when: "discussing Markdown/YAML interoperability, LLM wiki portability, progressive disclosure, catalog metadata as code, or agent-readable knowledge exchange"
  risk_when: "minimal interop fields, citations, links, or agent-generated enrichment might be mistaken for reviewed evidence or action basis"
  cold_references:
    - raw/articles/2026-06-14-google-open-knowledge-format-source.md
routing_hint:
  - source_ingest
  - context_pack_preparation
  - agent_readable_bundle
  - markdown_yaml_interop
  - export_import_sandbox
  - retrieval_not_truth
possible_project_refs:
  - VAKS
point_anchor_refs:
  - raw/articles/2026-06-14-google-open-knowledge-format-source.md#source-anchors
tags:
  - candidate
  - provisional
  - google-cloud
  - open-knowledge-format
  - okf
  - llm-wiki
  - markdown-frontmatter
  - progressive-disclosure
  - metadata-as-code
  - candidate-only
---

# Candidate Distillation: Google Open Knowledge Format

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 说人话结论

Google OKF 对 VAKS 是一个很强的外部确认：

```text
知识交换不一定需要新服务、新 SDK、新数据库。
一个明确约定的 Markdown + YAML frontmatter 文件夹，就可以成为 human + agent 共用的知识 bundle。
```

这和 VAKS 的底层方向高度一致。

但 OKF 解决的是：

```text
portable knowledge format / catalog exchange / agent-readable bundles
```

VAKS 解决的是：

```text
candidate -> review -> evidence support -> sufficiency -> action readiness
```

所以最准确的融合判断是：

```text
OKF 可以成为 VAKS 的外部交换/导出/轻互操作参考。
不能替代 VAKS 的证据、审查、行动边界。
```

## Source

```yaml
source_ref: raw/articles/2026-06-14-google-open-knowledge-format-source.md
derived_from:
  - GoogleCloudPlatform/knowledge-catalog okf/SPEC.md
  - Google Cloud Blog: Introducing the Open Knowledge Format
```

## Candidate Points

### 1. Markdown + YAML frontmatter as an interoperability substrate is externally validated

OKF v0.1 defines a knowledge bundle as a directory of Markdown files with YAML frontmatter.

This supports VAKS's current posture:

```text
Markdown/YAML remains source of record.
Search, vector, graph, API, MCP, viewer, and agent outputs remain derived layers.
```

Borrow:

- bundle-as-directory;
- concept-as-markdown-file;
- frontmatter as machine routing surface;
- body as human/agent-readable prose;
- Git repo / archive / subdirectory as distribution options.

Do not borrow:

- minimal frontmatter as enough for VAKS truth or action.

### 2. `index.md` progressive disclosure is a strong VAKS context-loading pattern

OKF's `index.md` is for letting a human or agent see what exists before opening individual files.

This maps directly to VAKS:

```text
index first
-> inspect summaries/metadata
-> choose full reads
-> build context pack
```

Borrow into:

- context pack preparation;
- dev context briefing;
- source bundle navigation;
- export/import packages.

Boundary:

```text
index.md is a loading map, not evidence.
```

### 3. `log.md` is useful as lightweight change history

OKF reserves `log.md` as optional chronological update history.

VAKS can borrow the concept for:

- source update log;
- bundle ingestion log;
- context pack construction log;
- export/import changelog;
- agent operation receipt rollup.

Boundary:

```text
log entry is traceability.
It is not reviewed truth, confidence, or approval.
```

### 4. OKF producer/consumer independence reinforces VAKS derived-layer boundaries

OKF explicitly separates who writes the bundle from who consumes it.

VAKS equivalent:

```text
Markdown records = durable source of record
retrieval/API/viewer/MCP = consumers or derived layers
agents = producers only through candidate/receipt/review gates
```

This is strongly aligned with:

- plugin sandbox;
- retrieval receipt;
- operation receipt;
- no derived artifact as truth.

### 5. OKF links are good activation edges but not reviewed relations

OKF says concept documents can link to one another and consumers may treat links as directed edges.

For VAKS:

```text
markdown link = activation / navigation / candidate relation signal
reviewed_relation = separate evidence-aware object
```

Borrow:

- bundle-relative links;
- broken-link tolerance for not-yet-written knowledge;
- link graph as workbench/retrieval surface.

Do not borrow:

- untyped link graph as reviewed knowledge graph.

### 6. OKF citations are provenance aids, not enough for VAKS support

OKF conventionally lists external sources under a citations section.

For VAKS, that is useful but insufficient:

```text
citation link = where to inspect
evidence_support = span supports specific candidate point / reviewed node / relation / action basis
```

Borrow:

- `# Citations` as standard source pointer section;
- citations can point to URLs or bundle-local references.

Do not borrow:

- citation marker as direct support.

### 7. OKF conformance is intentionally permissive; VAKS authority checks must stay stricter

OKF conformance mainly requires parseable frontmatter and a non-empty `type` field for concept documents.

This is good for exchange, but too weak for VAKS:

```text
OKF conformance = can be consumed
VAKS promotion = can be trusted for reviewed/action-facing use
```

VAKS should keep:

- `knowledge_status`;
- `retrieval_policy`;
- `action_basis_allowed`;
- `truth_mutation_allowed`;
- `review_pressure`;
- `promotion_gate`;
- evidence/support/action gates.

## Relationship To Current VAKS Architecture

| VAKS layer | OKF value | Fit |
|---|---|---|
| Capture / Provenance | Source and concept files stay readable and portable | strong |
| Source Intake | Minimal required fields inspire interop subset | medium |
| Candidate Distillation | Concept documents can hold candidate material | strong if labeled candidate |
| Review Queue | OKF does not provide review/promotion gate | weak |
| Reviewed Knowledge | OKF can carry reviewed notes but does not decide review status | support only |
| Reviewed Relations | OKF links are untyped/prose-scoped | activation only |
| Retrieval / Activation | index.md, links, tags, frontmatter help routing | strong |
| Context Pack | progressive disclosure and concept files help pack building | strong |
| Decision / Action | OKF has no action readiness model | weak |
| Feedback | no feedback truth boundary | weak |
| Agent Gateway | producer/consumer independence supports sandboxing | medium |
| Workbench / Viewer | static visualizer and bundle graph idea are useful | watch |

## Knowledge Calibration / Point Collision

| Candidate Point | Local VAKS Boundary | Calibration Output | Review Question |
|---|---|---|---|
| Markdown/YAML bundles are enough for portable agent knowledge exchange. | VAKS already uses Markdown/YAML source-of-record. | supports / refines | Should VAKS expose an OKF-compatible export subset later? |
| `index.md` provides progressive disclosure. | VAKS uses index/dev context/context pack loading. | supports | Should VAKS standardize more index views before runtime retrieval? |
| OKF citations improve source traceability. | VAKS says provenance is not support. | scope_mismatch | How can VAKS import OKF citations without treating them as support? |
| OKF links can form a graph. | VAKS reviewed relations require evidence review. | risk_of | How to prevent OKF link graph from becoming reviewed relation graph? |
| Enrichment agents can write OKF concepts. | VAKS agent writes are candidate/receipt gated. | risk_of | Should enrichment-agent output be quarantined as candidate by default? |

## Borrow Gradient

### P1 Borrow

- Format-over-platform posture.
- Markdown/YAML as durable portable bundle.
- `index.md` progressive disclosure.
- Concept files as one knowledge unit.
- Producer/consumer independence.

### P2 Borrow

- `log.md` update history.
- `# Citations` as source pointer convention.
- bundle-relative links for navigation.
- unknown field preservation / tolerant consumption.
- static viewer / graph view as workbench reference.

### P3 Watch

- OKF sample bundles and reference enrichment agent.
- Google Cloud Knowledge Catalog ingestion path.
- Future OKF versioning and extension conventions.
- Potential import/export compatibility with VAKS.

## Avoid

- Do not weaken VAKS schema to OKF's minimum `type` requirement.
- Do not treat OKF citations as evidence support.
- Do not treat OKF links as reviewed relations.
- Do not let enrichment-agent output bypass review.
- Do not make OKF conformance equal action readiness.
- Do not adopt Google-specific catalog/runtime as VAKS core.

## Minimal Elegant Adoption

The smallest useful VAKS adoption is:

```text
Keep VAKS internal schema strict.
Add a future OKF-compatible export/import adapter only after P0/P1 gates.
Map OKF concept files to VAKS source/candidate/reviewed layers with explicit boundary fields.
Treat imported OKF citations and links as provenance/activation until VAKS support/relation review checks them.
```

## Candidate Implementation Package

Future package name:

```text
P2.5 OKF Compatibility Sandbox
```

Artifacts:

- `outputs/review/okf-compatibility-sandbox-*/mapping.md`
- sample VAKS source card -> OKF concept export
- sample OKF concept -> VAKS candidate import
- citation import boundary fixture
- link graph import boundary fixture
- index/log export fixture

Acceptance cases:

```text
OKF-01 imported citation becomes source pointer, not support
OKF-02 imported link becomes candidate relation / activation edge, not reviewed relation
OKF-03 OKF concept with type only cannot become VAKS reviewed note
OKF-04 VAKS source card can export a minimal OKF concept without losing boundary fields
OKF-05 index.md can guide loading but cannot create action basis
OKF-06 log.md can show update history but cannot approve changes
OKF-07 enrichment-agent output enters candidate layer by default
```

## Open Questions

- Should VAKS eventually expose an OKF export profile, or only learn from OKF internally?
- What is the minimal frontmatter mapping between VAKS records and OKF concept documents?
- Should VAKS reserve `index.md` / `log.md` names in exported bundles?
- How should VAKS preserve OKF unknown fields without letting them become authority?
- Is `type` enough for external interop, while VAKS keeps `record_kind` and `knowledge_status` internally?

## Direct Judgment

- Direct use: no, not as VAKS core schema.
- Fork: no.
- Design-only: yes, strong.
- Adapt: yes, for export/import and progressive disclosure.
- Current branch value: strong for architecture upgrade plan, retrieval/context-pack preparation, product interoperability.
- Whole architecture value: strong for source ingest, context pack, viewer/workbench, publishing/export, agent-readable bundles.
- Risk: OKF's permissive conformance can be mistaken for VAKS authority; citations/links can be mistaken for support/reviewed relations.
- Next action: keep candidate-only; revisit after P0/P1 gates when designing export/import or public bundle format.

## Forbidden

```text
project_borrow_scope
project_non_borrow_scope
decision outcome
formal pattern
action basis
truth confidence
```

## Summary

OKF is one of the cleanest outside confirmations of VAKS's file-first instincts.

But VAKS should absorb it like this:

```text
OKF = portable knowledge exchange surface
VAKS = verified action knowledge control system
```

Use OKF to make VAKS easier to exchange with other tools.
Do not let OKF reduce VAKS's review/action discipline.

