---
record_kind: project_overlay
status: candidate
knowledge_status: candidate
processing_tier: medium
overlay_state: confirmed
review_pressure: none
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
target_ref: "raw/repos/2026-06-23-linxiv-dev-linXiv-source.md"
target_selector: "repo:linxiv-dev/linXiv@8085eeb61d03cadeb74eff2352afc148a3fa202c"
target_hint: "local-first academic paper manager; useful for VAKS paper/source adapter, source identity, runtime data root, and MCP permission boundary"
source_annotation_refs: "[ann-linxiv-001-namespaced-source-id, ann-linxiv-002-data-dir-source-of-truth, ann-linxiv-004-mcp-mutation-surface, ann-linxiv-005-case-collision]"
project_borrow_scope: "provider-prefixed source identity; runtime data root discipline; source adapter acquisition as raw/candidate intake; MCP read-only-first lesson; case-collision snapshot hygiene"
project_non_borrow_scope: "SQLite canonical memory; Obsidian export as reviewed knowledge; write/delete/import/restore MCP by default; React/Tauri/PyInstaller current-core dependency"
project_reopen_trigger: "paper/source-adapter sandbox; read-only VAKS MCP design; local cockpit or derived-cache runtime design; repo snapshot hygiene validator"
confirmation_basis: "User explicitly requested strong distillation in the VAKS workspace on 2026-06-23."
last_checked_at: "2026-06-23"
expires_at: null
---

# Project Overlay：linXiv -> VAKS

## Boundary

This is a project-scoped sidecar.

It does not rewrite the source card, candidate distillation, reviewed note,
decision, or pattern.

It can guide the active project, but it cannot act as reviewed knowledge or
action basis.

## Target

```yaml
target_ref: raw/repos/2026-06-23-linxiv-dev-linXiv-source.md
target_selector: repo:linxiv-dev/linXiv@8085eeb61d03cadeb74eff2352afc148a3fa202c
target_hint: paper/source intake and local runtime boundary reference
```

## Project Borrow Scope

For VAKS, this source may be borrowed as:

```text
1. Source identity reference:
   provider-prefixed IDs such as arxiv:, doi:, openalex:, local:.

2. Paper/source adapter reference:
   arXiv, DOI, CrossRef, OpenAlex, PDF metadata, BibTeX acquisition.

3. Runtime artifact hygiene:
   source tree and runtime data root must be separate.

4. MCP permission warning:
   read-only tools first; write/delete/import/restore tools require operation receipts.

5. Repo intake hygiene:
   case-colliding paths must be detected before trusting a Windows checkout.
```

## Project Non-Borrow Scope

For VAKS, do not currently borrow:

```text
1. linXiv SQLite app database as canonical memory.
   Reason: VAKS durable truth/source records stay Markdown/YAML and review-gated.

2. linXiv Obsidian export as reviewed knowledge.
   Reason: export is a convenience format, not candidate/review/action layering.

3. linXiv MCP write/destructive tool surface.
   Reason: VAKS needs explicit approval, operation receipts, permission tiers, and path scoping.

4. React/Tauri/PyInstaller sidecar app stack as current core.
   Reason: VAKS current priority is source -> candidate -> review -> action boundary, not product shell.

5. AI key/settings UI patterns.
   Reason: secret handling needs VAKS-specific policy and redaction checks.
```

## Reopen Trigger

Reconsider this overlay when:

```text
paper/source-adapter sandbox starts
read-only MCP for VAKS starts
local cockpit / derived cache runtime starts
repo snapshot hygiene validator starts
```

## Confirmation

```yaml
confirmation_basis: explicit user request for strong distillation
last_checked_at: 2026-06-23
expires_at:
```

## Operational Verdict

```text
borrow_value: medium
borrow_now: source identity + permission/risk lessons
borrow_later: paper adapter sandbox, read-only MCP contract, runtime data root
do_not_borrow_now: app DB, write-capable MCP, Tauri stack, Obsidian export as knowledge
```
