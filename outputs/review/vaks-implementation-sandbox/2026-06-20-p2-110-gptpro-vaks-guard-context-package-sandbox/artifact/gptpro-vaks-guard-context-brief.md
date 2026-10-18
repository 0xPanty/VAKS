---
slice_id: 2026-06-20-p2-110-gptpro-vaks-guard-context-package-sandbox
status: ready_for_gptpro_upload
artifact_kind: gptpro_context_brief
---

# VAKS Guard Context Brief For GPT Pro Review

## What This Is

This is a context packet for reviewing whether seven proven sandbox guard candidates should be absorbed into VAKS as a lightweight tool layer.

This is not a request to merge code, change the main architecture, write Obsidian content, promote reviewed knowledge, or approve action basis.

## VAKS In One Paragraph

VAKS means Verified Action Knowledge System. Its core distinction is not "find more context", but "decide what can safely become reviewed knowledge or action basis". The architecture separates raw source, candidate interpretation, review, evidence support, action readiness, feedback, and operational write authority. Retrieval, summaries, feedback, tests, and agent judgment are useful signals, but none of them automatically create truth, evidence support, reviewed relations, or permission to act.

## Current Decision

The seven guard candidates have passed sandbox validation in an Obsidian-style disposable vault pilot. The open question is not whether the sandbox can run. It can. The open question is:

```text
Should these seven capabilities become a lightweight VAKS Guard tool layer under the existing architecture, rather than becoming a new architecture layer or remaining only sandbox artifacts?
```

## Current Evidence

The p2-109 sandbox pilot proved:

- Seven guards were exercised: P0-03, P0-04, P0-05, P0-06, P0-07, P1-08, P1-10.
- Positive cases passed 7/7.
- Contamination cases were caught 6/6.
- Fixture and failure-case oracle files were read by the runner and recorded by SHA256.
- The disposable runtime vault was deleted after execution.
- Formal Obsidian vault, `tools/`, `templates/`, wiki truth layers, main architecture docs, commit, push, and sync were untouched.
- Reviewer returned `REVIEW_PASS_NO_BLOCKER`.
- Boundary Auditor returned `PASS_BOUNDARY`.
- GPT-5.5 extra-high Product Acceptance returned `PASS_PRODUCT_GRADE` for the sandbox-only goal.

Important boundary:

```text
p2-109 proves sandbox product grade only.
It does not mean the guards are already mainline, reviewed knowledge, evidence support, action basis, Opus approval, user approval, commit, push, or sync permission.
```

## Existing Architecture Already Has The Principles

These seven candidates are not invented from nowhere. The existing VAKS architecture already has the relevant principles:

- Review objects should be tied to `body_hash` / `checked_body_hash`.
- Evidence Support Check exists and is explicitly not a new truth engine.
- `action_readiness` is distinct from truth status.
- Feedback improves activation/usefulness/review pressure, not truth.
- Retrieval receipts exist as process/context-pack traces.
- Source-intake validators and failure matrices already exist as precedent.
- Runtime/cache/derived artifacts are not reviewed knowledge.

The gap is product execution:

```text
The original architecture has good rules.
The seven guards make those rules executable and harder to misuse.
```

## The Seven Guard Candidates

| Candidate | What It Protects | Existing VAKS Principle It Executes | Proposed Landing |
| --- | --- | --- | --- |
| P0-03 Body Hash Validator | Prevents approval drift after candidate body changes. | Reviewed object must be fixed to exact body content. | Tool checker. |
| P0-04 Support Boundary Validator | Prevents URL, summary, retrieval rank, candidate, or feedback from pretending to be direct support. | Retrieval/provenance/background are not evidence support by themselves. | Tool checker. |
| P0-05 Action Readiness Validator | Prevents insufficient, stale, risky, out-of-scope, or candidate-backed material from becoming action-ready. | Action readiness is stricter than having some evidence. | Tool checker. |
| P0-06 Feedback Validator | Prevents feedback from mutating truth confidence, verification status, source reliability, reviewed notes, or reviewed relations. | Feedback is use-memory/review pressure, not truth mutation. | Tool checker. |
| P0-07 Action-Boundary Failure Matrix | Keeps known dangerous authority-confusion cases as regression tests. | Boundary failures should be reproducible and rechecked. | Minimal regression matrix. |
| P1-08 Retrieval / Operation Receipt Validator | Ensures retrieval and operation records expose actor, basis, scope, authority bucket, and limits. | Receipts are process evidence, not review approval or action basis. | Tool checker plus small contract. |
| P1-10 Runtime Artifact Exclusion | Prevents caches, logs, temp vaults, `__pycache__`, and generated runtime artifacts from entering knowledge/context selection. | Derived runtime artifacts are not source/truth/reviewed knowledge. | Scan/check mode. |

## External Inspiration Positioning

These ideas were inspired by systems and papers that mostly place similar capabilities in tool, pipeline, evaluator, controller, memory, or audit layers:

- GraphRAG / LightRAG: retrieval/indexing/query routes and TextUnit-style anchors.
- PaperTrail / ProVe / RAG attribution: claim-evidence coverage and support verification.
- Self-RAG / CRAG / A2RAG: adaptive retrieval/evidence sufficiency control.
- Reflexion / Reflective Memory Management: feedback as memory for future behavior, not direct truth updates.
- W3C PROV: entity/activity/agent traceability.
- RKA: review queue, intent confirmation, decision/outcome calibration, and maintenance guardrails.

The proposed VAKS interpretation is deliberately narrow:

```text
Borrow the useful execution/control boundary.
Do not import full runtimes, graph databases, dashboards, MCP write tools, automatic promotion, automatic truth scoring, or hidden agent memory authority.
```

## Recommended Architecture Placement

Do not add a new primary architecture layer.

Recommended placement:

```text
Main VAKS architecture = defines principles, boundaries, and authority rules.
VAKS Guard = read-only lazy-gate tool layer that executes those boundaries.
Smart Workbench = optional user experience layer that explains failures and suggests next steps.
Sandbox = proof space for artifacts before any mainline absorption.
```

One-line architecture expression:

```text
VAKS Guard is a read-only lazy-gate tool layer for enforcing review, evidence, action, feedback, receipt, and runtime-artifact boundaries before high-risk exits. It checks boundary conditions but is not a truth source, reviewer, promotion authority, action approval, or write authority.
```

## Proposed Lightweight Product Shape

Avoid seven separate systems.

Prefer:

```text
one VAKS Guard entry point
seven small pure checkers
one shared status format
one minimal regression set
no services
no background automation
no database
no dependency install
no Obsidian write
no promotion
```

Possible command shape:

```text
python tools/vaks_guard.py check <file-or-folder> --mode review
python tools/vaks_guard.py check <file-or-folder> --mode action
python tools/vaks_guard.py check <file-or-folder> --mode write
python tools/vaks_guard.py scan-runtime <folder>
```

Possible output shape:

```yaml
status: pass | warn | block
code: support_url_only
message: URL-only citation cannot be direct support.
next_step: Attach a raw/source anchor or evidence packet.
authority_boundary: This check does not create reviewed knowledge or action approval.
```

## What GPT Pro Should Review

Please review the following questions:

1. Is the proposed "VAKS Guard as lightweight tool layer" positioning correct, or should any of the seven candidates remain sandbox-only?
2. Does this avoid overbuilding the architecture?
3. Does this preserve the smart parts from external RAG/agent systems while preventing authority confusion?
4. Are any candidates wrongly classified as tool checks when they should be architecture principles only?
5. Are any candidates missing from the minimal guard set before mainline absorption?
6. Is the proposed command/API shape too heavy, too weak, or about right?
7. What should be the smallest mainline absorption path if this is approved later?
8. What must stay out of mainline even if the tool layer is accepted?

## Desired GPT Pro Output

Use this structure:

```text
Verdict:
PASS_TOOL_LAYER_DIRECTION / REVISE_BEFORE_MAINLINE / BLOCK_MAINLINE_ABSORPTION

Main reasoning:

Per-candidate review:
- P0-03:
- P0-04:
- P0-05:
- P0-06:
- P0-07:
- P1-08:
- P1-10:

Overbuild risks:

Missing guardrails:

Recommended minimal landing shape:

What must not be merged:

Questions for user/Codex:
```

## Non-Negotiable Boundaries

- Sandbox success is not reviewed knowledge.
- Validator pass is not reviewer approval.
- Retrieval found is not evidence support.
- Agent thinks useful is not action basis.
- Feedback does not mutate truth.
- Runtime artifacts are not knowledge.
- No mainline write without explicit user approval.
- No Obsidian formal vault write from this package.
- No commit, push, sync, hooks, background service, or dependency install.

