# Promotion Recommendations

## Recommendation Table

| Packet | Target | Promote as | Support | Sufficiency for promotion | Recommendation | Minimal next step |
|---|---|---|---|---|---|---|
| EP-01 | Self-contained review candidate record | pattern | supported | sufficient | promote_ready | Write a narrow pattern note or update existing note after user approval |
| EP-02 | Review-gated compile queue | pattern | supported | sufficient | promote_ready | Promote only the queue-before-wiki boundary, not runtime implementation |
| EP-03 | Source hash registry and idempotent ingest | pattern | supported | sufficient | promote_ready | Preserve origin/provenance caveat before writeback |
| EP-04 | Decision outcome precondition before calibration | pattern | supported | sufficient | promote_ready | Promote as Use Ledger / decision-outcome chain pattern, not RKA runtime |
| EP-05 | Scope dashboard live context surface | pattern | weak | insufficient | needs_more_evidence | Reopen exact Dusk template anchors and run one local VAKS dev-context trial |

## Gap List

### G-01: Local VAKS Candidate Example

Applies to:

- EP-01
- EP-02

Need:

```text
One Markdown candidate record in `outputs/review/candidates/` or equivalent,
with body, source refs, violations/checks, review result, and archive behavior.
```

This is not needed for pattern promotion, but is needed before implementation.

### G-02: Local Lint / Review Check

Applies to:

- EP-01
- EP-02
- CI-08
- CI-10

Need:

```text
A tiny lint pass that catches missing source anchors, candidate self-support,
background_context-as-support, and pending-candidate promotion.
```

Do not create this in this sandbox unless the user asks.

### G-03: Registry Primary Record Choice

Applies to:

- EP-03

Need:

```text
Decide whether the Markdown source card is primary and JSON registry is derived,
or whether a small state file becomes an operational cache.
```

Recommended:

```text
Markdown source record primary; JSON registry derived and rebuildable.
```

### G-04: RKA Runtime Boundary

Applies to:

- EP-04

Need:

```text
If promoted, the pattern must explicitly reject RKA runtime / MCP / dashboard
adoption and limit itself to the decision-outcome precondition.
```

### G-05: Dusk Template And Local Trial

Applies to:

- EP-05

Need:

```text
Exact template anchors from the original Dusk source, plus one VAKS dev-context
trial showing dashboard -> briefing -> dev context pack selection.
```

### G-06: Candidate Pattern Bank Source Drilldown

Applies to:

- CI-11
- CI-12
- CI-13

Need:

```text
Do not promote candidate-pattern-bank files directly.
Reopen underlying raw video/repo/paper records and inspect transcript segments,
paper sections, source-code files, or stable artifacts.
```

### G-07: Abstract-Only Paper Limitation

Applies to:

- CI-15

Need:

```text
Authorized full text or another stable full-text source before any architecture
or implementation claim is promoted.
```

Current public abstract/metadata can support orientation only.

## User Decision Questions

1. Should the next writeback promote the four `promote_ready` items into `wiki/patterns/`, or should they stay as sandbox recommendations until a second pass?

2. If promoting, should the writeback update existing pattern files where they already exist, or create separate reviewed promotion notes first?

3. Should EP-05 receive a local VAKS dev-context trial now, or stay parked as `needs_more_evidence`?

4. Should the untracked Aal/Ruller paper intake be kept, committed later, or ignored for this promotion-funnel pilot?

## Commit Boundary

Only these sandbox files are this window's intended write output:

```text
outputs/review/promotion-funnel-pilot-2026-06-08/README.md
outputs/review/promotion-funnel-pilot-2026-06-08/CANDIDATE_INVENTORY.md
outputs/review/promotion-funnel-pilot-2026-06-08/PROMOTION_EVIDENCE_PACKETS.md
outputs/review/promotion-funnel-pilot-2026-06-08/PROMOTION_RECOMMENDATIONS.md
```

Do not commit without user approval.
