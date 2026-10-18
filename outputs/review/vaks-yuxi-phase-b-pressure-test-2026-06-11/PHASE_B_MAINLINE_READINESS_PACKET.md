---
record_kind: sandbox_mainline_readiness_packet
status: candidate
project_id: VAKS
created_at: 2026-06-11
truth_boundary: review_packet_not_mainline_adoption
action_basis_allowed: false
---

# Phase B Mainline-Readiness / Pro Review Packet

## Decision

Phase B is ready for a mainline-readiness review.

It is not approved for mainline edits yet.

Plain-language version:

```text
we can now ask: "if we wanted to preserve this Phase B value, what is the smallest safe doc integration?"
we cannot yet say: "merge this into VAKS core"
```

## Compared Against Previous Version

Previous version:

```text
integration readiness package
```

This packet adds:

```text
candidate mainline touch set
candidate insertion points
candidate snippet summaries
evidence map
remaining blockers
Pro review questions
```

This packet does not change:

```text
core docs
adapter behavior
ranking policy
contract validator
readiness validator
truth layer
write path
```

Readiness floor is preserved:

```text
readiness status: pass
readiness errors: 0
contract status: pass
contract errors: 0
```

## Candidate Mainline Touch Set

Minimal first patch, if later approved:

| Priority | File | Insertion point | Purpose |
|---:|---|---|---|
| 1 | `SOURCE_INTAKE.md` | `### Retrieval Bucket Policy` around line 429 | Define Phase B read-only retrieval adapter and bucket-local fusion boundary. |
| 2 | `IMPLEMENTATION_BLUEPRINT.md` | `## 9. Phase 5: Query Layer` around line 452 | Add Phase B as the next query-layer implementation step before runtime/tool expansion. |
| 3 | `DEV_CONTEXT.md` | `### Step 2: Context Pack` around line 254 | Allow retrieval receipts as context-pack candidates, not action basis. |
| 4 | `MEMORY_TIER.md` | `## 2. Core Rule` around line 83 or `## 8. What Not To Do` around line 409 | State that retrieval activation and Yuxi-like scores are not truth or confidence. |

Deferred unless Pro says necessary:

| File | Why deferred |
|---|---|
| `SCHEMA.md` | Only needed if VAKS formalizes `retrieval_receipt` or adapter manifest as a named schema object. |
| `REVIEW_QUEUE.md` | Only needed if adapter receipts are allowed to create review pressure or queue items. |
| `templates/architecture-review-window-prompt.md` | Only needed if Phase B becomes a standard external-runtime review prompt. |

## Candidate Snippet Summaries

These are review snippets, not applied patches.

### SOURCE_INTAKE.md

Candidate insertion under `### Retrieval Bucket Policy`:

```markdown
#### Phase B Read-Only Retrieval Adapter

VAKS may use a derived retrieval adapter for parser/chunk/metadata/vector-like
or graph-neighborhood recall, but VAKS authority buckets must be applied before
ranking or RRF fusion.

The adapter may emit chunk manifests, retrieval receipts, click-back anchors,
source hashes, chunk hashes, warning codes, and retrieval reasons.

The adapter must not promote raw/candidate/diagnostic/feedback material into
reviewed support, reviewed relation, truth confidence, or action basis.
```

### IMPLEMENTATION_BLUEPRINT.md

Candidate insertion under `## 9. Phase 5: Query Layer`:

```markdown
Phase B query-layer work starts as a read-only derived adapter:

1. build chunk manifest and retrieval receipt artifacts;
2. filter by VAKS authority bucket before ranking;
3. run bucket-local retrieval and rerank;
4. return context-pack candidates with click-back and warnings;
5. require pressure, contract, and readiness gates before any mainline adoption.

Do not attach Skills, MCP writes, subagents, or formal writeback in Phase B.
```

### DEV_CONTEXT.md

Candidate insertion under `### Step 2: Context Pack`:

```markdown
Retrieval receipts may help assemble a context-pack candidate.

They are not action basis by themselves. A context pack that uses adapter output
must still expose source click-back, authority badge, usage badge, warning code,
and any stale or scope warning before it can be used for action-facing review.
```

### MEMORY_TIER.md

Candidate insertion under `## 2. Core Rule` or `## 8. What Not To Do`:

```markdown
Retrieval activation is not truth.

Vector similarity, graph-neighborhood hits, rerank score, repeated retrieval,
and evaluation score may improve activation or review pressure. They must not
increase truth confidence, create reviewed relations, or approve action basis.
```

## Evidence Map

Use these sandbox artifacts for review:

| Claim | Evidence |
|---|---|
| Phase B retrieval improved over early baselines without leakage | `PHASE_B_PRESSURE_REPORT.md`, `KEEP_DECISION.md` |
| v1 and v1.1 avoided overfitting by adding holdout checks | `PHASE_B_V1_VS_LOCKED_BASELINE.md`, `PHASE_B_V11_VS_V1_DECISION.md` |
| Skeleton preserved v1.1 retrieval behavior while emitting artifacts | `PHASE_B_SKELETON_VS_V11_DECISION.md` |
| Contract defects were found and fixed, not hidden | `PHASE_B_CONTRACT_TEST_DECISION.md`, `results/phase_b_adapter_contract_test.json` |
| Integration package passed with zero readiness errors | `PHASE_B_INTEGRATION_READINESS_CHECK.md`, `results/phase_b_integration_readiness_check.json` |
| Mainline touch set remains sandbox-only | `git status --porcelain -- core docs` should show no core doc changes |

Current quantitative floor:

| Set | Corpus | hit@5 | hit@10 | MRR | Leakage |
|---|---|---:|---:|---:|---:|
| main | primary | 30/30 | 30/30 | 1.0000 | 0.0000 |
| main | full | 30/30 | 30/30 | 1.0000 | 0.0000 |
| holdout | primary | 12/15 | 13/15 | 0.7811 | 0.0000 |
| holdout | full | 13/15 | 13/15 | 0.7591 | 0.0000 |

## Remaining Blockers

These block mainline adoption:

```text
original Yuxi full-stack was not run locally because Docker was unavailable
holdout is positive but not perfect
production vector database behavior is not tested
index refresh and concurrency behavior are not tested
multi-user permission behavior is not tested
no real Obsidian/browser click-through UX has been validated
no C-lite runtime has been approved
no Skills, MCP writes, subagents, or formal writeback are approved
```

## Pro Review Questions

Ask Pro to review these points:

```text
1. Is the four-file minimal touch set enough for Phase B documentation?
2. Should SCHEMA.md define retrieval receipt now, or should it stay sandbox-only?
3. Does SOURCE_INTAKE.md remain the right home for bucket-local RRF rules?
4. Does DEV_CONTEXT.md need stronger action-facing language for adapter receipts?
5. Should a real Yuxi Docker/full-stack run be required before any mainline doc patch?
6. Are the remaining blockers acceptable for a documentation-only Phase B note?
7. Is there any hidden path where adapter output could become truth, reviewed relation, or action basis?
```

## Mainline Entry Gate

No core doc edit should happen until these are true:

```text
contract validator: pass / 0 errors
readiness validator: pass / 0 errors
mainline-readiness validator: pass / 0 errors
core docs currently clean
Pro or human review accepts the minimal touch set
patch is documentation-only
patch preserves "read-only derived adapter" language
patch explicitly rejects Skills, MCP writes, subagents, formal writeback, and production readiness
```

## Recommended Next Action

Send this packet to Pro or use it as the next local review prompt.

If approved, prepare a separate minimal documentation patch.

If rejected, keep all Phase B artifacts in sandbox and do not change the VAKS core docs.
