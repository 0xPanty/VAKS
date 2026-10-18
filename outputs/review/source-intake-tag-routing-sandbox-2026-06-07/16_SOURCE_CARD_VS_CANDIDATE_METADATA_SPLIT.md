---
type: sandbox_design_note
status: candidate_only
created_at: 2026-06-07
scope: source-card vs candidate-distillation metadata split
truth_boundary: sandbox design note only; metadata routes work, it does not create authority
---

# Source Card vs Candidate Metadata Split

## Plain Rule

```text
Source card metadata helps find the source.
Candidate distillation metadata helps reason about extracted ideas.
Neither field set creates reviewed truth.
```

## Source Card Fields

Use source-card metadata for stable discovery facts visible at intake time.

Good source-card fields:

```yaml
source_id:
source_type:
source_url:
captured_at:
content_form:
language:
version_or_time_scope:
topics: []
entities: []
aliases: []
retrieval_policy:
  policy_kind: source_identity_only
  pack_allowed: drilldown_required
  action_basis_allowed: false
  warning_code: raw_is_provenance_only
```

Meaning:

```text
This record tells us what the source is, where it came from, and how to find it.
It does not tell us what VAKS should believe or adopt.
```

## Candidate Distillation Fields

Use candidate-distillation metadata for extracted ideas and review routing.

Good candidate fields:

```yaml
record_kind: candidate_distillation
knowledge_status: candidate
source_refs: []
extracted_topics: []
extracted_entities: []
candidate_points: []
review_pressure:
  - missing_evidence
  - contradiction
  - synthesis_needed
retrieval_policy:
  policy_kind: orientation_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: candidate_not_action_basis
```

Meaning:

```text
This record tells us what the source appears to suggest and what needs review.
It can orient research, but it cannot act as final support.
```

## Project Overlay Fields

Use project overlays only for project-scoped borrowing or non-borrowing notes.

Good overlay fields:

```yaml
record_kind: project_overlay
project_scope:
overlay_state: confirmed | archived
knowledge_status: candidate
source_ref:
borrowable_for_this_project: yes | no | maybe
non_borrow_scope:
retrieval_policy:
  policy_kind: project_context_only
  pack_allowed: activation_only
  action_basis_allowed: false
  warning_code: overlay_not_authority
```

Meaning:

```text
This project can use this source as orientation in this context.
The source card remains generic.
The generic knowledge point is not polluted by project preference.
```

## Field Ownership

| Question | Put it on source card? | Put it on candidate distillation? | Put it on project overlay? |
|---|---|---|---|
| What is this source? | yes | no | no |
| How do we find it later? | yes | sometimes | sometimes |
| What ideas were extracted? | no | yes | maybe, only project-scoped |
| Is it reviewed? | no, except `knowledge_status: raw` | no, candidate only | no, candidate only |
| Can it support action? | no | no | no |
| Is it useful for this project? | no | maybe as open question | yes |
| Should VAKS adopt it universally? | no | no | no |

## Retrieval Behavior

```text
source card:
  raw_drilldown
  useful when the user needs provenance, source identity, or raw anchor.

candidate distillation:
  candidate_orientation
  useful when the user is researching possible ideas.

project overlay:
  active_project_overlay
  useful only inside the active project scope.
```

## Pressure Cases

```text
If "DataChain" is on the source card:
  it helps find the raw source.

If "registry-before-recompute" is in candidate distillation:
  it helps find the extracted idea.

If "good for VAKS" appears:
  it belongs in a project overlay, not in generic source-card metadata.

If a candidate point is top-ranked:
  include it as orientation, then drill down to raw/reviewed anchors before action use.
```

## Sandbox Verdict

```text
Keep source-card metadata boring and source-facing.
Put interpretation pressure in candidate distillation.
Put project fit in overlays.
Let the context pack builder label the lane instead of trusting the tag.
```
