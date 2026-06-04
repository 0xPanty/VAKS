# External Source Priority And Final Judgment

Status: sandbox external-reading and engineering-judgment note. No main-vault
writeback, no `SCHEMA.md` change, and no operation-convention promotion.

## Source Discipline

For this topic, English primary sources are more valuable than Chinese
secondary summaries. Use the original specifications, official docs, or
original papers first. Secondary summaries may help orientation, but they must
not become design authority.

## Priority Sources

| priority | source | primary link | what VAKS should absorb |
| --- | --- | --- | --- |
| highest | W3C Web Annotation Data Model | https://www.w3.org/TR/annotation-model/ | `TextQuoteSelector`, `TextPositionSelector`, `State`, and `refinedBy`; this is the technical floor for anchor and jump-back design. |
| highest | W3C PROV-DM | https://www.w3.org/TR/prov-dm/ | Provenance as entities, activities, agents, and bundles; supports keeping a reversible truth ledger behind a light front face. |
| highest | W3C PROV Links | https://www.w3.org/TR/prov-links/ | Bundle links and `mention`; supports sparse front-face provenance pointers connected to fuller provenance packets. |
| high | GitHub PR conversation docs | https://docs.github.com/en/pull-requests/collaborating-with-pull-requests/reviewing-changes-in-pull-requests/commenting-on-a-pull-request | Resolved conversations collapse; unresolved / resolved / outdated conversations are review workflow state, not truth. |
| high | Sentry issue status docs | https://docs.sentry.io/product/issues/states-triage/ | Issue state, unresolved lists, escalating, and regressed reopen; use as product analogy for unresolved-first surface. |
| high | Sentry fingerprinting / grouping docs | https://docs.sentry.io/platforms/flutter/usage/sdk-fingerprinting/ | Fingerprint grouping routes repeated events into issues; grouping is triage compression, not proof strength. |
| high | OpenTelemetry sampling docs | https://opentelemetry.io/docs/concepts/sampling/ | Mature systems do not retain every full trace; richer retention should target high-value paths while ordinary paths keep sufficient trace stubs. |
| high | Schema.org ClaimReview | https://schema.org/ClaimReview | Compact claim-review summaries use minimal fields such as `claimReviewed`; metadata is summary surface, not the claim's truth proof. |
| high | SciFact original paper | https://aclanthology.org/2020.emnlp-main.609/ | Scientific claim + evidence-containing abstracts + rationales as a minimal reviewer unit. |
| high | AVeriTeC original paper | https://openreview.net/forum?noteId=fKzSz0oyaI | Real-world web evidence, question-answer decomposition, and justification flow for claim verification. |
| high | AmbiFC original paper | https://aclanthology.org/2024.tacl-1.1/ | Ambiguity, conflicting interpretations, annotator disagreement, and soft-label pressure. |
| high | FEVER original paper | https://aclanthology.org/N18-1074/ | Large ordinary-volume claim verification with supported / refuted / NEI pressure and sentence evidence. |

## Immediate Verification Work

Do not expand broad automated patching first. The most valuable immediate
checks are:

### 1. 12-24 Case Chinese Operator Preflight

Goal: not truth proof. The goal is to see whether Codex / Pro / reviewer agents
can:

- understand state;
- understand why a record escalated;
- avoid treating non-actionable records as actionable;
- jump back to source / record / evidence;
- avoid treating count, dashboard, lineage, source count, tests, lint, or
  feedback as authority.

This is already represented by:

```text
review_packet_risk_tiered_24/
review_packet_adversarial_12/
reports/CHINESE_REVIEWER_CARD_USABILITY_PREFLIGHT_PROTOCOL.md
```

### 2. Live Click-Back Authenticity Patch

The click-back authenticity patch should not create more wrapper snapshots. In
this sandbox, it has now raised the 24 representative full-anchor cases from
the earlier:

```text
4 live real snapshots
20 fallback wrappers
```

to:

```text
24 live / immutable snapshots
0 fallback wrappers
```

This is a real improvement over package-integrity-only proof. Product-stage
pilot cases should still be adjudicated as real source or immutable snapshot
click-back targets by the operator/reviewer flow. Wrapper-only targets must not
count as product click-back success.

Latest narrow adjudication and semantic landing audit added one stricter
boundary: 24 live / immutable snapshots are transport success, not
claim-relevant click-back success. The first semantic audit showed 7/24
selector success and 17/24 `body_window` / boilerplate landings. The current
package repairs this with exact evidence / exact claim / claim-keyword window
selection and now reports 24/24 automated semantic selector success. The next
target is human/product click-back adjudication, not a larger automatic sample.

## Open Questions And Limitations

- There is still no independent human oracle; `review_due` precision and
  `false-lite = 0` currently mean consistency with a machine-frozen overlay
  oracle, not human adjudication.
- Current click-back snapshot coverage for the representative 24-case subset is
  no longer wrapper-heavy, and automated semantic selector landing is now 24/24.
  It still does not prove final UI click-back usability or human adjudication.
- Recurrence side-arm benefits still rely on favorable structured grouping
  fields, not messy runtime extraction.
- Chinese operator-card candidate exists, but there is still no real human or
  real operator observation data.

## Final Engineering Judgment

Direction:

```text
continue
```

This solves a core system problem if it is understood as layer separation, not
as card beautification.

Current default core:

```text
shell_core + Chinese operator reviewer rendering
```

Recurrence / grouping:

```text
continue as conditional side arm; default off
```

Chinese reviewer-card:

```text
necessary operator surface, not ordinary user default front face
```

Next step:

```text
rerun narrow operator adjudication with the repaired selector landing proxy
then consider larger paired human pilot only if click-back semantics are credible
```

Do not ask Pro for another broad automatic review as the main next move.

## If Starting From Zero

Start from four layers:

1. truth ledger
2. escalation controller
3. reviewer cockpit / operator review surface
4. end-user answer surface

In that architecture, `card` is only a renderer inside the operator surface. It
is not the architecture center, not a truth layer, and not the ordinary user's
daily UI.
