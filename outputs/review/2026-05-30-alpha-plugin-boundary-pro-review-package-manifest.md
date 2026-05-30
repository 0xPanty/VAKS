---
type: review-package-manifest
status: draft
created: 2026-05-30
project: verified-action-knowledge-system
package_purpose: Pro review of v0.3 alpha detail mining and plugin-boundary correction
latest_local_commit: f187be0
---

# v0.3 Alpha Detail Mining + Plugin Boundary Pro Review Package

## Purpose

This package is for a Pro reviewer to check whether this research window kept the Verified Action Knowledge System on its intended path.

Primary question:

```text
Which frontier ideas should become main-framework rules,
which should only become interface contracts,
and which should remain external plugins / workbenches?
```

Important correction:

```text
Do not read every "alpha" as a main-framework addition.
Many are better treated as replaceable plugins whose outputs enter the vault only as candidate signals.
```

## Baseline Architecture

Public story:

```text
Capture -> Understand -> Review -> Connect -> Act and Learn
```

Internal loop:

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

Key boundary:

```text
retrieval, dashboards, graph rank, agent memory, source metadata, and feedback are not truth authority.
```

## Files To Read First

Read in this order:

```text
01_focus/2026-05-30-external-alpha-plugin-boundary-audit.md
01_focus/2026-05-30-alpha-plugin-boundary-pro-review-package-manifest.md
02_alpha_reviews/*.md
03_baseline_context/AGENTS.md
03_baseline_context/README.md
03_baseline_context/ARCHITECTURE_PRINCIPLES.md
03_baseline_context/FUSION_ARCHITECTURE_V0_2_DRAFT.md
03_baseline_context/SCHEMA.md
```

## Included Alpha Reviews

```text
PageIndexRAG-Web + GraphRAG-Example:
  source structure map, graph activation, candidate relation suggestion boundary.

ThirdSpace Vault Template:
  agent-facing vault operating protocol, progressive loading, Misa/Codex boundary.

ThirdSpace Dashboard:
  vault health / risk dashboard as view layer, not review authority.

ZLAgent:
  agent operation gate, permission tiers, write origin, sandboxed review.

langchain-miniopenclaw:
  skill-routed evidence locator and locator trace.

MemGAS:
  multi-granularity memory association as activation, not truth.

RAG-Anything:
  external multimodal / heavy-source extractor with source element manifest.
```

## Requested Pro Checks

Please check:

```text
1. Are the proposed main-framework residues still too heavy?
2. Did any plugin accidentally gain truth authority?
3. Should source_element_manifest and locator_trace be optional schema extensions?
4. Should agent_operation_gate be documented now or deferred until Misa writes exist?
5. Does the four-plugin consolidation prevent tool sprawl?
6. Are older review files misleading because `fusion_decision: adapt` should really mean plugin/interface?
7. Is the main framework still clean enough after this research window?
```

## Expected Review Output

Useful Pro output would be:

```text
keep / revise / reject classification for each alpha
recommended tiny mainline doc changes, if any
risks of overfitting to external repos
missing source-code anchors or unsupported claims
```

## Packaging Note

This package is evidence for review only.

No mainline architecture docs were rewritten by this package step.

