---
record_kind: candidate_distillation
status: candidate
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: none
review_pressure: none
derived_from: "raw/repos/2026-06-07-microsoft-markitdown-source.md"
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
v0_2_13_trigger: no
routing_hint:
  - source_ingest
  - file_distillation_skill
  - source_hygiene
possible_project_refs:
  - VAKS
point_anchor_refs:
  - "raw/repos/2026-06-07-microsoft-markitdown-source.md#Source / Code Anchors"
borrow_value: strong
borrow_order:
  - "P1: file-to-Markdown adapter before candidate distillation"
  - "P2: fixture matrix for file distillation skill"
  - "P3: plugin/MCP/OCR as later-stage optional references"
avoid:
  - "Do not let MarkItDown output become reviewed knowledge."
  - "Do not expose broad URI/MCP conversion without path and network policy."
  - "Do not install or enable cloud/OCR/plugins by default."
dev_context_hint:
  default_layer: support_with_required_risk
  core_only_when: "Implementing or testing a VAKS file-intake converter wrapper."
  support_when: "Designing document/source intake for PDF, Office docs, HTML, ZIP, image, or audio files."
  risk_when: "Agent-access, MCP, untrusted files, remote URIs, plugins, cloud analyzers, or action-facing source support is involved."
  cold_references:
    - "raw/repos/2026-06-07-microsoft-markitdown-source.md"
    - "raw/repos/_snapshots/microsoft-markitdown-e144e0a2be95b34df17433bac904e635f2c5e551.zip"
tags:
  - candidate
  - provisional
  - markitdown
  - source-intake
---

# Candidate Distillation: microsoft/markitdown

## Boundary

This note is provisional orientation.

It can help route attention, compare ideas, or suggest project overlays. It is not reviewed knowledge, not a decision, not a formal pattern, and not action basis.

## 人话判断

有帮助，而且是强帮助，但位置要放准。

它不是“蒸馏系统”，它是“蒸馏前的文件清洗 / 转 Markdown 入口”。对我们最有价值的是：

```text
各种文件 -> 结构尽量保住的 Markdown -> VAKS candidate distillation
```

也就是说，它可以帮 VAKS 少造一大堆 PDF/DOCX/XLSX/PPTX/HTML/ZIP 解析轮子。但它不能负责真假、证据、review、关系边、action basis。

## Source

```yaml
derived_from: raw/repos/2026-06-07-microsoft-markitdown-source.md
point_anchor_refs:
  - snapshot_ref: raw/repos/_snapshots/microsoft-markitdown-e144e0a2be95b34df17433bac904e635f2c5e551.zip
    selector_type: file_lines
    selector_value: README.md:8-12, README.md:342-348, packages/markitdown/src/markitdown/_markitdown.py:94-205
```

## Candidate Points

### 1. File distillation should separate conversion from comprehension

MarkItDown gives the conversion layer:

```text
binary/source file -> markdown-ish text
```

VAKS still owns:

```text
source card -> candidate points -> review queue -> evidence-aware review -> action basis gate
```

Borrow value: strong.

### 2. MarkItDown can be a default local adapter candidate, not the whole intake runtime

Best minimum wrapper:

```text
vaks-file-intake
-> verify input path is inside allowed source folder
-> hash original file
-> call narrow MarkItDown local/stream conversion
-> write retained raw markdown
-> write conversion metadata
-> write candidate distillation shell
-> never promote automatically
```

This aligns with VAKS because conversion output is raw/candidate material.

### 3. Preserve source identity and conversion metadata separately

MarkItDown result is useful, but VAKS needs extra metadata:

```yaml
source_file:
source_sha256:
converter: markitdown
converter_version:
checked_commit:
input_mode: local_path | stream
network_used: false
plugins_enabled: false
cloud_used: false
conversion_warnings:
retained_markdown_path:
raw_file_retention:
```

Without this, converted Markdown becomes too easy to mistake for source truth.

### 4. The test matrix is almost as valuable as the converter

MarkItDown tests cover docx/xlsx/pptx/pdf/zip and several input modes. For VAKS, we should borrow that idea as a fixture grid:

```text
format x input_mode x expected artifact x forbidden side effect
```

Minimum VAKS fixture set:

- `.pdf`: text PDF, table PDF, scanned PDF later
- `.docx`: headings, comments, embedded images later
- `.xlsx`: multi-sheet, table-like cells
- `.pptx`: slide text and notes if supported
- `.html`: local exported web page
- `.zip`: only if explicit recursive policy exists
- `.md/.txt`: passthrough baseline

### 5. Security warning should become a VAKS wrapper rule

The repo itself warns that it performs I/O with current process privileges and recommends narrow conversion APIs. For VAKS, that becomes a hard rule:

```text
No raw convert(uri) from arbitrary user/agent input.
No broad MCP exposure.
No private paths unless explicitly allowed.
No network fetch unless the intake card says network_used: true.
No plugin/cloud/OCR unless explicitly requested and recorded.
```

### 6. MCP is a useful warning, not a default route

The MCP package exposes `convert_to_markdown(uri)`. That is convenient, but for VAKS it is too broad unless wrapped by:

- path allowlist
- network allowlist
- max file size
- timeout
- plugin/cloud disabled by default
- read receipt
- output directory receipt
- no write to reviewed layers

For now: design-only / risk reference.

### 7. OCR and Azure paths are later-stage, not default

OCR plugin and Azure Content Understanding can improve scanned PDFs and structured field extraction, but they change the trust and cost profile.

Default VAKS stance:

```text
local deterministic conversion first
OCR only for explicit scanned/embedded-image need
cloud only with user approval and provenance
```

## Open Questions

- Does MarkItDown preserve enough locator information for VAKS source-span evidence, or do we need a sidecar locator layer?
- For PDFs, do we need PageIndex-style page windows alongside MarkItDown Markdown?
- Should file distillation keep original binary in repo, Obsidian, or only hash + user-owned path?
- How do we mark conversion confidence separately from claim confidence?
- Should ZIP conversion be disabled until recursion and path policy are written?

## Routing Hint

```yaml
route_to:
  - source_ingest
  - file_distillation_skill
  - tool_safety
  - fixture_matrix
do_not_route_to:
  - reviewed_truth
  - action_basis
  - architecture_decision
  - universal_agent_tool
```

## Borrow Gradient

- `borrow_value`: strong
- P1: use as local file-to-Markdown adapter candidate for VAKS file distillation.
- P2: borrow test matrix shape and optional dependency discipline.
- P3: keep MCP/OCR/Azure/plugin ideas as later-stage references.
- avoid: broad `convert(uri)` from arbitrary agent input, default `[all]` install, default cloud/OCR, treating output Markdown as evidence support.

## Forbidden

```text
project_borrow_scope
project_non_borrow_scope
decision outcome
formal pattern
action basis
truth confidence
```
