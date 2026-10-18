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
project_id: verified-action-knowledge-system
target_ref: "raw/repos/2026-06-07-microsoft-markitdown-source.md"
target_selector: "repo:microsoft/markitdown@e144e0a2be95b34df17433bac904e635f2c5e551"
target_hint: "VAKS file distillation / source intake converter"
project_borrow_scope:
  - "Use MarkItDown as a candidate local file-to-Markdown adapter behind a VAKS wrapper."
  - "Borrow optional dependency discipline by file type."
  - "Borrow fixture matrix shape for file conversion tests."
  - "Borrow security warnings as explicit wrapper policy."
project_non_borrow_scope:
  - "Do not treat converted Markdown as reviewed knowledge, evidence support, or action basis."
  - "Do not expose broad URI/MCP conversion to agents by default."
  - "Do not enable plugins, OCR, Azure, or network fetching by default."
  - "Do not write conversion output directly into truth-layer wiki folders."
project_reopen_trigger:
  - "When implementing VAKS file-intake skill."
  - "When adding MCP/agent-access conversion."
  - "When processing scanned PDFs or image-heavy Office files."
confirmation_basis:
  - "GitHub live page and API checked on 2026-06-07."
  - "Snapshot `e144e0a2be95b34df17433bac904e635f2c5e551` inspected locally."
  - "Compared against SOURCE_INTAKE and REFERENCE_REVIEW_PROTOCOL."
last_checked_at: 2026-06-07
expires_at: 2026-07-07
borrow_value: strong
borrow_order:
  - "P1: file-to-Markdown adapter wrapper"
  - "P2: converter fixture matrix and metadata ledger"
  - "P3: MCP/OCR/cloud/plugin architecture as later references"
avoid:
  - "broad URI conversion"
  - "unauthenticated MCP access"
  - "default plugin/cloud/OCR"
  - "promotion without review"
---

# Project Overlay: VAKS x MarkItDown File Distillation

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note, decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or action basis.

## Target

```yaml
target_ref: raw/repos/2026-06-07-microsoft-markitdown-source.md
target_selector: repo:microsoft/markitdown@e144e0a2be95b34df17433bac904e635f2c5e551
target_hint: VAKS file distillation / source intake converter
```

## Project Borrow Scope

For VAKS, borrow this:

```text
1. Put MarkItDown before candidate distillation as a file-to-Markdown adapter.
2. Wrap it with VAKS policy: path allowlist, network off, plugins off, cloud off, output receipt.
3. Retain original source hash + converted markdown + conversion metadata.
4. Borrow the repo's multi-format test-vector style for VAKS fixtures.
5. Treat warnings/errors as workflow feedback or review pressure, not truth mutation.
```

Human shorthand:

```text
它帮我们把“文件内容”先变成可蒸馏文本。
它不帮我们判断真假。
```

## Project Non-Borrow Scope

For this project, do not currently borrow:

```text
1. Broad convert(uri) exposed directly to agents.
2. MCP server as a default local tool.
3. markitdown[all] as default dependency.
4. OCR / Azure / Content Understanding as default path.
5. ZIP recursion without a written recursion policy.
6. Any direct write from converter output into reviewed wiki folders.
```

Why:

```text
These routes widen permission, network, cost, or authority boundaries before VAKS has a wrapper contract.
```

## Reopen Trigger

Reconsider this overlay when:

- user asks to implement file distillation skill;
- real PDF/DOCX/XLSX/PPTX files need intake;
- scanned PDFs or embedded images become important;
- agent/MCP tool access is being designed;
- converted Markdown needs to support an action-facing answer.

## Confirmation

```yaml
confirmation_basis:
  - GitHub live metadata and source snapshot checked.
  - VAKS SOURCE_INTAKE and repo review protocol compared.
  - Existing OpenKB/long-document adapter notes checked for overlap.
last_checked_at: 2026-06-07
expires_at: 2026-07-07
```

## Forbidden

```text
decision outcome
review verdict
truth confidence
action basis
universal ban
```
