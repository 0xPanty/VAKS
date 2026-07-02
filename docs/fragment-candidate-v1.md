# VAKS Fragment Candidate v1

`fragment_candidate` is the low-authority intake object for useful fragments
that do not yet have a source anchor.

It exists to preserve ideas, remembered claims, possible quotes, questions,
terms, and pattern hints without pretending that they are sourced evidence.

## Position

```text
Fragment Candidate
  -> source recovery succeeds
  -> Source Card / Source Capture / Source Annotation
  -> Candidate Distillation
  -> Review
  -> Reviewed Knowledge / Evidence Packet / Action Basis
```

Forbidden shortcut:

```text
Fragment Candidate
  -> Reviewed Knowledge / Evidence Packet / Action Basis
```

## Allowed Use

- orientation
- activation
- source recovery seed
- task or question routing
- pointer-only inclusion in a context pack

## Forbidden Use

- evidence support
- reviewed knowledge
- action basis
- exact quotation without recovered source
- Source Capture Store input
- Source Annotation target
- fake Source Card creation

## Core Fields

```yaml
schema: urn:vaks:schema:fragment-candidate:v1
record_kind: fragment_candidate
knowledge_status: candidate
candidate_class: fragment_only
processing_tier: light
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: missing_source_provenance
usage_policy:
  pack_content_allowed: false
  pack_pointer_allowed: true
  action_basis_allowed: false
  evidence_support_allowed: false
  reviewed_knowledge_allowed: false
```

`knowledge_status` remains `candidate` to preserve the current VAKS enum spine.
`candidate_class: fragment_only` prevents fragment records from being treated as
normal candidate distillations.

## Provenance Status

| Value | Meaning |
|---|---|
| `self_authored` | The fragment is explicitly the user's own idea. |
| `memory_trace` | The user remembers seeing it somewhere but cannot identify the source. |
| `source_hint_only` | A weak source hint exists, but no source identity or anchor exists. |
| `source_unknown` | No source hint exists. |

Weak hints are hints only. They must not create `source_id`, `source_ref`,
`capture_id`, or Source Annotation fields.

## Quote-Like Fragments

If `fragment.kind: quote_like` and no source has been recovered:

```yaml
quote_exactness: unverified
literal_quote_allowed: false
```

The fragment may remind the user to find the source, but it must not be rendered
as an exact quote.

## Merging

When `state.fragment_state: merged`, the record must identify the formal object
it merged into:

```yaml
state:
  fragment_state: merged
  merged_into:
    kind: source_card | source_annotation | candidate_distillation
    ref: ...
```

Merging into a candidate does not make the fragment evidence. The destination
candidate must still carry its own source pointer or explicitly remain
fragment-derived non-evidence.

Source recovery and merge state are bound:

- `source_recovery.status != found` requires `recovered_source_ref: null`.
- `source_recovery.status: found` requires a non-empty `recovered_source_ref`.
- `source_recovery.status: found` requires `fragment_state: merged`.
- `fragment_state != merged` requires `merged_into: null`.
- `fragment_state: merged` requires `merged_into.kind` and `merged_into.ref`.
- `provenance.status: source_unknown` cannot also declare
  `source_recovery.status: found`.

## Validation

Run:

```powershell
python tools/validate_fragment_candidate.py fragments
python tools/selftest_fragment_candidate.py
```

The validator checks:

- required fields and enum values
- exact field sets for named nested objects
- body content digest
- quote-like restrictions
- source hint consistency
- forbidden source/capture/evidence fields
- usage policy fail-closed flags
- merged target requirements

`source_recovery.attempts[]` is an exact-shape process log. Each item may only
use `method`, `query`, `outcome`, and `result_ref`. It must not carry formal
`recovered_source_ref`, `merged_into`, source/evidence/review/action short-name
fields, `*_ref` authority fields, URI/locator/citation/support fields, or
anchor fields. Formal pointers are allowed only on the canonical top-level state
machine paths where this contract explicitly defines them. Weak URL hints belong
only in `provenance.source_hint.possible_url`.
