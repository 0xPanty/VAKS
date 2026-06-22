# VAKS Routing Robustness & Shadow Assurance R0.7 Contract

This sandbox is a follow-up to the closeout R0.6 routing contract. It does not
modify R0.6 and does not create a new truth, review, action, or production
runtime layer.

## Scope

R0.7 checks three runtime-discipline concerns:

1. trusted policy signals are separated from user request and inferred text
   features;
2. paraphrased queries produce stable shadow route decisions under the same
   trusted policy context and the same structured `inferred_query_features`;
3. selective verification identifies which claims require later assessment by
   `assurance_profile`.

Every route decision is `shadow_only: true`, `applied_to_runtime: false`, and
`answer_policy: pending_evidence`.

## Signal Priority

```text
organization policy
> trusted caller metadata
> user request to increase assurance
> inferred query features
```

User text and query text cannot lower `assurance_floor`, cannot modify
`query_mode`, cannot change trusted `risk_level`, and cannot replace the
authority policy.

## Paraphrase Stability

For each paraphrase group, `query_mode`, `assurance_floor`,
`assurance_profile`, `retrieval_effort`, and `answer_policy` must remain stable
under the same trusted policy context and fixed structured inferred features.

This package does not evaluate natural-language feature extraction robustness
or real route regret, because the input features are fixtures and the runner
does not execute alternate Fast/Standard/Strict answer paths.

## Selective Verification

`verification_required` means a claim must be assessed later. It does not mean
the claim is supported, true, reviewed, approved, or action-ready.

- `light`: selects high-impact expressions such as numbers, dates, versions,
  policy claims, permissions, prohibitions, obligations, absolutes, and
  action-adjacent claims.
- `grounded`: selects all answer-material and externally verifiable claims,
  plus everything selected by `light`.
- `strict`: selects everything `grounded` selects and adds dimensions for
  scope, temporal, authority, conflict, and exception checks when flagged by
  structured claim features.
