# Operator Adjudication Round 1 Review Result

Status: external narrow operator adjudication review imported from the user-provided Pro / ChatGPT review text. This is not independent dual-human evidence.

## Verdict

`pass with concerns`

The current `shell_core + Chinese operator/reviewer rendering` remains worth continuing as an operator maintenance surface. It should stay outside the truth core, outside the ordinary end-user UI, and outside any claim that evidence has become sufficient.

The correct abstraction remains:

```text
truth ledger -> escalation controller -> operator review surface -> end-user answer surface
```

`not_go_yet` remains the correct package status.

## Post-Fix Update

After this imported review, the package added a stricter semantic landing
evaluator and repaired the selector fallback:

```text
exact evidence substring
-> exact claim substring
-> claim-keyword window
-> body_window only as failure fallback
```

Current automated semantic selector success is now 24/24 with 0 `body_window`
and 0 boilerplate landings. This repairs the specific Archive-header failure
found in `FULLANCHOR-001` and `FULLANCHOR-002`, but it is split by landing
class. `claim_relevant_context_landing` is weaker than `evidence_landing` and
must not be described as direct evidence landing. This remains an automated
selector proxy, not independent human/product click-back adjudication.

## What This Round Passed

- State legibility is useful: ordinary / for_review / blocking / resolved_folded / regressed are easier for an operator to understand than raw machine labels.
- No wrong actionability was observed in the imported narrow run: `0/36`.
- No serious miss was observed in the imported narrow run: `0/36`.
- No authority misunderstanding was observed in the imported narrow run: `0/36`.
- Adversarial traps were useful as pressure cases, especially action-basis-looking ordinary text, pseudo-success anchors, wrapper-only click-back, authority paraphrase, fake numeric precision, source-count traps, and lineage traps.

## What Did Not Pass

The click-back gate did not pass.

Imported readout:

```text
core click-back success: 16/24
adversarial click-back success: 9/12
enter 120-case main packet: no
recurrence side packet: keep closed
```

The critical failure is semantic landing, not simple file opening. `FULLANCHOR-001` and `FULLANCHOR-002` opened live / immutable snapshots, but their selected quote landed on Wayback / Archive boilerplate such as capture metadata rather than claim-relevant evidence. Therefore `24/24 live snapshots` is transport success, not product click-back success.

The package must distinguish:

- transport fetch success
- source / record / evidence path resolution
- claim-relevant selector success

`body_window` must not count as product-grade click-back success.

## Ordinary + Warning Boundary

The imported review also flagged `RISK-UX-17` through `RISK-UX-20`.

These are ordinary records with warning strips. Their handling text should not say `open full audit or at least review risk strip`, because that makes the operator hesitate between save and review. The safer route is:

```text
light save + boundary reminder
only open full audit if the record becomes action-basis or hits a hard trigger
```

## Design Judgment

The route remains sound, but card is not the final product shape. The long-term surface should move toward a queue-first operator cockpit:

- unresolved-first queue
- risk strip
- anchor health
- handling suggestion
- source / record / evidence drilldown
- retained deep packet

Card is only the current renderer for that operator surface.

## Next Required Fixes

1. Treat `body_window` and boilerplate landing as semantic click-back failures.
2. Add a semantic click-back landing evaluator.
3. Update quality gates so live fetch does not masquerade as product click-back.
4. Tighten ordinary + warning handling text.
5. Keep recurrence / grouping closed.
6. Do not enter the 120-case main packet until the selector landing issue is repaired and rechecked.

## Evidence Boundary

This round was described as same-model double-pass operator adjudication draft. It is useful for finding overclaims and UI/selector failures, but it is not independent dual-human adjudication and must not be promoted to formal human evidence.
