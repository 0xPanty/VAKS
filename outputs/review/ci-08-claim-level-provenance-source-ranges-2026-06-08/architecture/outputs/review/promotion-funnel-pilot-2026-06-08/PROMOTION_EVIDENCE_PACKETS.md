# Promotion Evidence Packets

## Review Rules Used

Source provenance is not support.

A claim or pattern note cannot prove itself.

Support must come from a source span, code anchor, transcript segment, stored
artifact, or other independent anchor.

`supported` does not mean truth or action-ready.

## EP-01: Self-Contained Review Candidate Record

Target:

```text
A review candidate should be a self-contained artifact with body, sources,
source-state / lint metadata, and stable identity, so review and approval refer
to the same object.
```

Promotion target: pattern.

Independent evidence/source anchors:

- `raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip`
- `llm-wiki-compiler-main/src/compiler/candidates.ts:1-12`
- `llm-wiki-compiler-main/src/compiler/candidates.ts:34-58`
- `llm-wiki-compiler-main/src/compiler/candidates.ts:84-101`
- `llm-wiki-compiler-main/src/commands/review-approve.ts:1-13`
- `llm-wiki-compiler-main/src/commands/review-approve.ts:47-64`

Anchor support:

- `candidates.ts:1-12` states generated pages go to standalone JSON candidates under `.llmwiki/candidates/`, not directly to `wiki/`, and that each candidate stores the full body.
- `candidates.ts:34-58` shows candidate draft fields for title, slug, summary, sources, body, sourceStates, schemaViolations, and provenanceViolations.
- `candidates.ts:84-101` writes those fields into a persisted candidate record.
- `review-approve.ts:47-64` re-reads the candidate, validates the stored body, writes that body, refreshes derived state, and clears the candidate.

Self-support loop check:

- Not a self-support loop. The pattern note is only a trace handle; support comes from the local repo snapshot code.

Support state:

```text
supported
```

Evidence sufficient for promotion?

```text
sufficient for a narrow reviewed pattern
```

Warrant:

The code directly implements the artifact boundary the target describes:
candidate records persist the body and review metadata, and approval writes the
stored candidate body rather than generating a new artifact.

Missing evidence:

- A local VAKS Markdown candidate example would strengthen implementation fit.
- A local lint script would strengthen operational readiness, but is not required to promote the pattern itself.

Counterevidence / risk / scope limit:

- Candidate directories can become a stale inbox if no review habit exists.
- The source implementation writes into `wiki/concepts/`; VAKS would adapt the pattern to claim/pattern/decision paths and stricter review gates.

Recommendation:

```text
promote_ready
```

Suggested minimal revision before actual writeback:

```text
Promote only the artifact-boundary pattern, not the source implementation's page-kind or runtime choices.
```

## EP-02: Review-Gated Compile Queue

Target:

```text
LLM-generated knowledge should enter a review queue first; only reviewed
candidates may move into formal wiki knowledge nodes.
```

Promotion target: pattern.

Independent evidence/source anchors:

- `raw/repos/_snapshots/llm-wiki-compiler-main-2026-05-26.zip`
- `llm-wiki-compiler-main/src/compiler/candidates.ts:1-12`
- `llm-wiki-compiler-main/src/compiler/candidates.ts:77-103`
- `llm-wiki-compiler-main/src/commands/review-approve.ts:1-13`
- `llm-wiki-compiler-main/src/commands/review-approve.ts:35-64`
- `REVIEW_QUEUE.md` section 7, "Promote"

Anchor support:

- `candidates.ts` shows generated pages routed to candidate JSON records for review instead of direct wiki writes.
- `review-approve.ts` shows approval as a separate command that validates, writes, refreshes indexes, and clears the candidate.
- `REVIEW_QUEUE.md` independently defines the local VAKS rule that promotion is allowed only when a cluster/candidate is reviewed.

Self-support loop check:

- Not a self-support loop. The source code supports the external implementation pattern; `REVIEW_QUEUE.md` supports local fit and boundary, not source behavior.

Support state:

```text
supported
```

Evidence sufficient for promotion?

```text
sufficient for pattern promotion under VAKS scope
```

Warrant:

The external code provides a concrete implementation of queue-before-write, and
the local `REVIEW_QUEUE.md` already defines the matching VAKS promotion boundary.
Together they support a reviewed pattern, not an automatic implementation decision.

Missing evidence:

- Local candidate folder convention and lint checks still need a concrete VAKS example if this becomes implementation work.

Counterevidence / risk / scope limit:

- Do not copy the source runtime wholesale.
- Do not treat approval mechanics, lint passes, or test passes as evidence review.
- This does not authorize `git add .`, Obsidian sync, or automatic promotion.

Recommendation:

```text
promote_ready
```

Suggested minimal revision before actual writeback:

```text
Scope the pattern to "candidate-before-wiki writeback"; leave implementation scripts for a separate decision.
```

## EP-03: Source Hash Registry And Idempotent Ingest

Target:

```text
Source ingest should keep a content-hash registry or derived index so repeated
source intake can skip duplicates or route replacement/recompile deliberately.
```

Promotion target: pattern.

Independent evidence/source anchors:

- `raw/repos/_snapshots/openkb-main-2026-05-27.zip`
- `OpenKB-main/openkb/state.py:8-25`
- `OpenKB-main/openkb/state.py:39-42`
- `OpenKB-main/openkb/state.py:80-87`
- `OpenKB-main/openkb/converter.py:36-61`
- `OpenKB-main/openkb/cli.py:348-361`
- `raw/repos/2026-05-27-openkb-source.md`

Anchor support:

- `state.py` defines `HashRegistry`, lookup helpers, persistent add, and SHA-256 file hashing.
- `converter.py` computes the file hash before conversion and skips already-known files.
- `cli.py` registers the hash only after successful compilation.

Self-support loop check:

- Not a self-support loop. The pattern note points to OpenKB; support comes from the local OpenKB snapshot code.

Support state:

```text
supported
```

Evidence sufficient for promotion?

```text
sufficient for a narrow ingest-lifecycle pattern
```

Warrant:

The code shows a working mechanism for content-hash identity, duplicate
detection, and delayed registry commit after compilation. That directly
supports the VAKS pattern: dedupe/replacement should be source-lifecycle
infrastructure, not a truth claim.

Missing evidence:

- A VAKS-specific decision is still needed on whether Markdown source records or a derived JSON registry is the primary record.
- A local remove/recompile flow is not yet tested.

Counterevidence / risk / scope limit:

- Same content can arrive from different origins; hash dedupe must preserve origin/provenance when context matters.
- Hash registry is traceability infrastructure, not evidence support.

Recommendation:

```text
promote_ready
```

Suggested minimal revision before actual writeback:

```text
Promote as "derived registry from source records", with origin preservation as a required caveat.
```

## EP-04: Decision Outcome Precondition Before Calibration

Target:

```text
Decision outcome calibration should not record a final outcome unless the
recommendation and user choice, or an explicit override, are already recorded.
```

Promotion target: pattern.

Independent evidence/source anchors:

- `raw/repos/2026-05-29-rka-source.md`
- `outputs/review/2026-05-30-rka-source-code-anchor-review.md`
- `https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/models/decision_option.py#L121-L130`
- `https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/services/decision_options.py#L234-L280`
- `https://github.com/infinitywings/rka/blob/7bc2d76efba61b92db5b056220f7009763003a0d/rka/api/routes/decisions.py#L227-L243`

Anchor support:

- RKA's selection payload and service require either selected option or override rationale before recording PI selection.
- The route-level outcome guard rejects outcome recording when neither PI selected option nor override rationale exists.
- The local RKA source-code review already maps this to VAKS Use Ledger as a small hardening, not a runtime adoption.

Self-support loop check:

- Not a self-support loop if the exact commit code URLs are treated as the evidence anchors.
- The local source-code-review output is only the trace and mapping layer.

Support state:

```text
supported
```

Evidence sufficient for promotion?

```text
sufficient for a narrow review/use-ledger pattern
```

Warrant:

Without a recorded user choice or explicit override, an observed outcome cannot
show whether the recommendation itself worked. The RKA code enforces this
precondition at the service/API layer, and the VAKS boundary already says
decision outcome calibrates future recommendations, not truth.

Missing evidence:

- A concrete VAKS decision-outcome example would help before implementation.
- If promoted, the node should avoid implying that RKA's runtime or metrics should be adopted.

Counterevidence / risk / scope limit:

- RKA is a SQLite/API/MCP runtime; VAKS should not copy the runtime.
- Outcome calibration does not prove the underlying claim true.
- Sample-size metrics such as Brier/ECE remain parked.

Recommendation:

```text
promote_ready
```

Suggested minimal revision before actual writeback:

```text
Promote as a small pattern: "recommendation -> user choice/override -> outcome" chain.
```

## EP-05: Scope Dashboard Live Context Surface

Target:

```text
A project/area/scope dashboard can gather candidate core/support/risk/task
context before building a temporary dev context pack.
```

Promotion target: pattern.

Independent evidence/source anchors:

- `raw/repos/2026-05-27-dusk-obsidian-vault-source.md`
- Dusk source matrix anchors:
  - `template_area.md:13-38`
  - `template_area.md:40-66`
  - `Vault Onboarding Part 3:72-85`
- `wiki/patterns/scope-dashboard-live-context-surface.md`

Anchor support:

- The Dusk source record says the inspected area template gathers components, connected projects, documentation/workstation notes, meetings, ongoing tasks, and completed tasks.
- The onboarding anchor says an Area Family page can show connected components, projects, docs, workstation notes, meetings, and tasks.

Self-support loop check:

- Partial risk. The currently available independent evidence is the source record's inspected source matrix; this pilot did not reopen the original Dusk template files or zip entries.
- It is not pure self-support, but it is weaker than local code-snapshot anchors.

Support state:

```text
weak
```

Evidence sufficient for promotion?

```text
not sufficient yet for reviewed pattern promotion
```

Warrant:

The inspected source matrix supports the narrower claim that an Area dashboard
can gather live scope context. It does not yet prove that VAKS should promote
this as a reviewed pattern without a local dev-context trial.

Missing evidence:

- Reopen original Dusk template entries or retain a local template snapshot with exact anchors.
- Run one VAKS dev-context example showing that a scope dashboard helps select Core / Support / Risk / Cold references.
- Record failure cases: dashboard stale, plugin output treated as authority, task state polluting truth.

Counterevidence / risk / scope limit:

- Dusk repo is legacy and plugin-heavy.
- Dashboard output is a workbench surface, not source support, reviewed relation, or action basis.
- Single-source evidence is enough for a candidate, but weak for reviewed pattern adoption.

Recommendation:

```text
needs_more_evidence
```

Suggested minimal revision before actual writeback:

```text
Keep candidate. Promote only after exact template anchors and one local VAKS trial.
```
