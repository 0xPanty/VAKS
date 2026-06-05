---
type: expansion_candidate_set
status: candidate-only
created_at: 2026-06-05
project: verified-action-knowledge-system
truth_boundary: shadow candidates only; not implementation
write_scope: outputs/review only
---

# v0.2.13 Expansion Candidates

## Candidate 1: New Schema

Shadow proposal:

```text
Add a formal action_support_envelope schema object.
```

Possible fields:

```text
claim
evidence_anchors
warrant
scope_assumptions
known_challenges
residual_review_status
excluded_non_support
source_family_context
```

Risk:

```text
It may turn a sentence-level guardrail into a mandatory object and make every
action-facing note feel like schema compliance.
```

## Candidate 2: New Template

Shadow proposal:

```text
Add a reusable action-basis-envelope template.
```

Possible sections:

```text
claim
evidence
warrant
scope
challenges
residual status
non-support shortcuts
```

Risk:

```text
Agents may start applying the template to ordinary source intake or simple review notes.
```

## Candidate 3: Formal Project Development Workspace Directory

Shadow proposal:

```text
Create a stable project_borrowing_workspace / development_area directory.
```

Possible use:

```text
Store project-local borrowing entries outside temporary outputs/review.
```

Risk:

```text
It may make pre-decision borrowing look like formal architecture decision or reviewed knowledge.
```

## Candidate 4: New Pattern

Shadow proposal:

```text
Create a candidate pattern such as structured-action-support-envelope.
```

Possible mechanism:

```text
Make action-facing support visible through claim, evidence, warrant, scope, challenges, status.
```

Risk:

```text
It may turn a final action-basis guardrail into a reusable pattern with a fancy name,
inviting overuse across light and medium layers.
```

## Candidate 5: GSN / SACM System

Shadow proposal:

```text
Adopt a lightweight GSN / SACM-inspired assurance-case subsystem.
```

Possible objects:

```text
claims
arguments
evidence artifacts
contexts
strategies
confidence annotations
diagram views
```

Risk:

```text
This would shift VAKS from evidence-aware action basis into a full assurance-case system.
```

## Candidate 6: Tool Adoption

Shadow proposal:

```text
Adopt or evaluate assurance-case tools such as ASCE, AdvoCATE, NOR-STA,
SafeTbox, Socrates, gsn2x, D-Case Editor, or Astah System Safety.
```

Possible use:

```text
Use tools to model claims, arguments, evidence, diagrams, baselines, and histories.
```

Risk:

```text
Tool catalogue / vendor pages may be mistaken for endorsement, conformance validation,
or VAKS architecture requirements.
```

## Candidate 7: Make All Intake Heavier

Shadow proposal:

```text
Require every source card, routing row, candidate point, or summary to include
a full claim/evidence/warrant packet.
```

Possible use:

```text
Increase rigor at every stage.
```

Risk:

```text
This would destroy light intake, encourage fake completeness, and make agents write
confident-looking warrants where there is not enough review yet.
```
