---
type: review-candidate
status: pending-review
record_kind: candidate_distillation
provisional: true
knowledge_status: candidate
processing_tier: medium
lifecycle_state: candidate_provisional
overlay_state: confirmed
review_pressure: none
retrieval_policy: orientation_only
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
created: 2026-06-06
project: verified-action-knowledge-system
scope: x-article-obsidian-signal-density-cleanup-distillation
proposed_node_type: candidate-distillation
proposed_title: "Dami-Defi Obsidian Signal Density Cleanup Candidate Distillation"
proposed_by: Codex
sources:
  - raw/articles/2026-06-06-x-damidefi-obsidian-signal-density-cleanup-source.md
  - raw/articles/2026-06-06-x-damidefi-obsidian-signal-density-cleanup-source/pasted-text.txt
related_prior_distillation:
  - outputs/review/2026-06-06-x-damidefi-obsidian-claude-research-stack-candidate-distillation.md
  - outputs/review/2026-06-06-x-cyrilxbt-claude-obsidian-90-days-candidate-distillation.md
  - outputs/review/2026-06-06-x-hamza-obsidian-second-brain-candidate-distillation.md
  - outputs/review/2026-06-06-x-zaimiri-hermes-obsidian-vault-ai-brain-candidate-distillation.md
evidence_level: user-provided-x-article-self-report
verification_status: unverified
candidate_reliability_note: medium for signal-density workflow themes; low for deletion counts and performance claims
truth_boundary: "candidate comprehension only; not reviewed knowledge; not architecture decision; not action basis"
write_scope: outputs/review only
routing_labels:
  source_kind: practitioner_x_article
  processing_lane: medium_candidate_distillation
  truth_lane: candidate_only
  project_overlay_route: confirmed_sidecar_exists
  candidate_pattern_bank: no_new_entry
  v0_2_13_trigger: no
candidate_point_labels:
  - captured_information_is_not_knowledge
  - signal_density_limits_agent_synthesis
  - attention_budget_as_vault_constraint
  - own_thinking_compounds_more_than_clippings
  - unprocessed_captures_should_cool_or_archive
  - deletion_requires_reversible_quarantine
  - audit_prompt_suggests_not_deletes
  - irreplaceable_source_fact_minimal_retention
  - duplicate_thinking_should_consolidate
  - activation_selection_beats_raw_deletion_for_vaks
related_project_overlay:
  - outputs/review/project_overlays/VAKS/VAKS-damidefi-obsidian-signal-density-cleanup-2026-06-06.md
reviewer:
review_result:
---

# Dami-Defi Obsidian Signal Density Cleanup Candidate Distillation

## Boundary

This is a candidate distillation of a user-provided X article about deleting
low-signal Obsidian notes to improve AI-assisted vault synthesis.

It does not modify:

```text
wiki/
SCHEMA.md
REVIEW_QUEUE.md
templates/
ARCHITECTURE_PRINCIPLES.md
FUSION_ARCHITECTURE_V0_2_DRAFT.md
raw/
outputs/
```

It does not delete, archive, move, or classify any actual VAKS note.

## Plain-Language Takeaway

The useful part of this source is not "delete 90% of the vault."

The useful part is:

```text
AI-assisted vaults are attention systems;
too much unprocessed capture lowers signal density;
the user's own thinking matters more than clippings;
cleanup should be reversible and human-reviewed;
VAKS should prefer activation selection / cooling over raw-source deletion.
```

For VAKS, this reinforces a boundary:

```text
Raw sources may be retained for provenance and audit.
Activation packs should not pull everything.
Unprocessed captures can cool or be quarantined.
Review decides what becomes knowledge.
Deletion is not the default maintenance action.
```

## Source Comprehension

### What The Article Is Really About

The article argues that when an AI reads across a vault, the vault's signal to
noise ratio becomes a core quality constraint. A passive archive can survive
lots of unused material; an agent-readable vault suffers when the agent reasons
across too much low-value material.

The source distinguishes:

```text
information:
  collected articles, highlights, bookmarks, and raw captures

thinking:
  reactions, theses, analysis, questions, and processed takeaways
```

Its proposed cleanup mechanism is:

```text
classify notes as KEEP / DELETE / REVIEW
lean aggressive in suggestions
do not let the agent delete
move candidates to archive first
wait before permanent deletion
run the same daily brief after cleanup to observe quality changes
```

### What The Article Is Not

It is not:

```text
a verified vault-maintenance policy
a controlled retrieval-quality experiment
a source-retention policy for evidence systems
a VAKS deletion instruction
a reviewed architecture decision
a source of reviewed evidence for action basis
```

It is a useful practitioner provocation about signal density and cleanup.

## Candidate Points

### 1. captured_information_is_not_knowledge

Candidate point:

```text
Collected information is raw material; it becomes useful knowledge only after
the user extracts, reacts, analyzes, questions, or connects it.
```

Source anchor:

```text
raw/articles/2026-06-06-x-damidefi-obsidian-signal-density-cleanup-source.md
raw/articles/2026-06-06-x-damidefi-obsidian-signal-density-cleanup-source/pasted-text.txt
article sections: The Belief That Is Quietly Costing You; The Test for What Stays
```

VAKS fit:

```text
Strongly reinforces Capture vs Understand vs Review.
```

Boundary:

```text
VAKS still preserves source provenance when needed. A raw source is not
knowledge, but it may be necessary evidence material.
```

Route:

```text
candidate point
candidate pattern route: source-structure-first-rag
candidate pattern route: memory-granularity-and-quarantine
```

### 2. signal_density_limits_agent_synthesis

Candidate point:

```text
Agent synthesis quality can degrade when the vault contains too many low-signal
captures relative to processed thinking.
```

Source anchor:

```text
pasted text sections: The Mechanism Nobody Explains; What Changed After
```

VAKS fit:

```text
Supports Activation Tier and context-pack selection discipline.
```

Boundary:

```text
This does not prove that deleting raw files is the right fix for VAKS. The safer
VAKS fix is activation filtering, cooling, archive, and review routing.
```

Route:

```text
candidate point
possible future route: signal-density-vault-health
```

### 3. attention_budget_as_vault_constraint

Candidate point:

```text
A vault connected to an AI is constrained by attention budget, not storage
capacity; every included note competes with more relevant context.
```

Source anchor:

```text
pasted text section: The Mechanism Nobody Explains
```

VAKS fit:

```text
Supports context-pack budget guardrails and activation selection.
```

Boundary:

```text
Attention budget affects answer quality and context selection. It does not
change truth confidence.
```

Route:

```text
candidate point
possible support for agent-context-pack-budget-guardrails
```

### 4. own_thinking_compounds_more_than_clippings

Candidate point:

```text
The user's reactions, theses, active questions, and analyses compound more than
unprocessed saved articles or highlights.
```

Source anchor:

```text
pasted text section: The Two Objections and Why Both Are Wrong
```

VAKS fit:

```text
Supports candidate comprehension and own-words processing before promotion.
```

Boundary:

```text
This does not make personal reaction true. It only makes it a better candidate
unit for review and synthesis than unprocessed clipping.
```

Route:

```text
candidate point
possible route: own-words-before-knowledge
```

### 5. unprocessed_captures_should_cool_or_archive

Candidate point:

```text
Unprocessed captures that do not contain user thinking should cool, archive, or
leave activation paths instead of repeatedly entering synthesis.
```

Source anchor:

```text
pasted text sections: What I Actually Deleted; How to Run the Cleanup This Weekend
```

VAKS fit:

```text
Strong fit with Activation Tier, cooling, and archive-first lazy reactivation.
```

Boundary:

```text
Cooling or archive is not deletion. Raw sources may remain available for audit
while staying out of hot context.
```

Route:

```text
candidate point
candidate pattern route: archive-first-lazy-reactivation
candidate pattern route: memory-granularity-and-quarantine
```

### 6. deletion_requires_reversible_quarantine

Candidate point:

```text
Any cleanup that may delete notes should first move candidates into a reversible
archive or quarantine period.
```

Source anchor:

```text
pasted text section: How to Run the Cleanup This Weekend; Move before you delete
```

VAKS fit:

```text
Supports safe maintenance and anti-destructive agent operations.
```

Boundary:

```text
For VAKS, deletion is not an ordinary maintenance action. The useful mechanism
is reversible quarantine and owner review.
```

Route:

```text
candidate point
candidate pattern route: memory-granularity-and-quarantine
candidate pattern route: agent-tool-access-tiering
```

### 7. audit_prompt_suggests_not_deletes

Candidate point:

```text
An AI cleanup prompt should classify and explain candidates, not perform
destructive deletion.
```

Source anchor:

```text
pasted text section: The Prompt That Does the Audit For You
```

VAKS fit:

```text
Directly supports suggest-only agent access tiers and review-first maintenance.
```

Boundary:

```text
Even a useful classification can be wrong. It is a triage suggestion, not an
authority boundary or final action.
```

Route:

```text
candidate point
candidate pattern route: agent-tool-access-tiering
candidate pattern route: path-scoped-agent-output-writes
```

### 8. irreplaceable_source_fact_minimal_retention

Candidate point:

```text
If a source contains a hard-to-refind fact, retain the fact and provenance in a
minimal form rather than carrying a large low-signal wrapper into activation.
```

Source anchor:

```text
pasted text section: The Test for What Stays; exception for obscure or hard-to-refind data
```

VAKS fit:

```text
Useful for context-pack compression and source extraction, but must be handled
carefully because VAKS often needs source anchors.
```

Boundary:

```text
Do not discard source anchors needed for evidence-aware review. Minimal
retention is only safe when provenance and review needs remain satisfied.
```

Route:

```text
candidate point
possible route: source extraction / evidence packet compression
```

### 9. duplicate_thinking_should_consolidate

Candidate point:

```text
Repeated versions of the same idea can be consolidated into the sharpest version
instead of repeatedly entering retrieval and synthesis.
```

Source anchor:

```text
pasted text section: What I Actually Deleted; Duplicate thinking
```

VAKS fit:

```text
Supports point collision, consolidation, and duplicate candidate handling.
```

Boundary:

```text
Consolidation should preserve provenance and supersession trail when used for
reviewed knowledge.
```

Route:

```text
candidate point
possible support for Knowledge Calibration / Point Collision
```

### 10. activation_selection_beats_raw_deletion_for_vaks

Candidate point:

```text
For an evidence-oriented vault, the safer translation of signal-density cleanup
is activation selection and cooling, not deleting raw sources.
```

Source anchor:

```text
derived VAKS interpretation from article's signal-density argument and VAKS source-retention boundary
```

VAKS fit:

```text
Central project fit for this source.
```

Boundary:

```text
This is a project overlay interpretation, not a claim made directly by the
source. It must not be presented as the author's recommendation.
```

Route:

```text
candidate point
project overlay only
candidate pattern route: retrieval-is-activation-not-truth
candidate pattern route: memory-granularity-and-quarantine
```

## Candidate Pattern Bank Decision

Do not create a new Candidate Pattern Bank entry from this one article.

Reason:

```text
Most useful ideas already route to existing or known local patterns:
memory-granularity-and-quarantine
retrieval-is-activation-not-truth
source-structure-first-rag
simple-first-retrieval-baseline
archive-first-lazy-reactivation
agent-tool-access-tiering
path-scoped-agent-output-writes
```

Possible future patterns only if more sources repeat them:

```text
signal-density-vault-health
activation-selection-over-raw-deletion
cleanup-classifier-suggests-not-deletes
```

For now they stay candidate points.

## Candidate Routing Hints (Not Project Overlay)

The project-scoped borrowing list is written as a separate candidate sidecar:

```text
outputs/review/project_overlays/VAKS/VAKS-damidefi-obsidian-signal-density-cleanup-2026-06-06.md
```

It is not a schema, not a formal Project Lens object, and not an action basis.

## Candidate Routing Hints

Candidate routing hints:

```text
1. Treat vault signal density as an activation quality concern.
2. Keep unprocessed captures out of hot context.
3. Prefer the user's processed thinking over raw clipping for synthesis.
4. Let AI suggest cleanup candidates, never delete directly.
5. Use reversible archive / quarantine before destructive changes.
6. Consolidate duplicate thinking with provenance preserved.
7. Compress rare irreplaceable facts carefully while preserving source anchors.
```

## Candidate Boundary Notes

Candidate boundaries:

```text
1. Delete 90% as a rule.
2. Deleting raw source records from VAKS.
3. Assuming internet retrievability replaces provenance.
4. Letting Claude delete files.
5. Treating smaller vault as automatically more true.
6. Treating daily brief improvement as evidence of correctness.
7. Removing transcripts, ledgers, source cards, or review artifacts for cleanliness.
8. Conflating personal productivity cleanup with verified knowledge maintenance.
```

## Relation To The Current Five-Article Cluster

This is the fifth piece in the current Obsidian / Claude / agent-vault cluster:

```text
Hamza:
  storage without resurfacing fails.

Zaimiri:
  agent outputs need visible receipts and output zones.

CyrilXBT:
  long-running workflows reveal vault quality and over-automation risk.

Dami-Defi research stack:
  capture and source templates are the research system's critical path.

Dami-Defi signal density:
  unprocessed capture can degrade AI synthesis and should cool, archive, or be removed from activation.
```

Together they suggest a VAKS-safe reading:

```text
capture everything lightly enough to preserve provenance;
do not activate everything;
separate source retention from context selection;
review determines truth;
maintenance should be reversible before destructive.
```

## v0.2.13 Trigger Check

Does this source currently trigger v0.2.13?

```text
action_basis: no
significant promotion: no
significant decision: no
architecture absorption: no
risk-sensitive answer relied on for action: no
explicit "is this enough to act" question: no
```

Result:

```text
v0.2.13 not triggered
```

If a future window wants to use this source to justify deletion, archive policy,
activation policy, source retention changes, or vault health maintenance, then
v0.2.13 must run:

```text
claim
anchored evidence
non-circular warrant
scope / assumptions
known challenges / gaps
residual risk
```

## Suggested Next Step

Keep this as candidate-only.

If more vault-health or cleanup sources arrive, cluster them around:

```text
signal-density-vault-health
activation-selection-over-raw-deletion
unprocessed-capture-cooling
cleanup-classifier-suggests-not-deletes
duplicate-thinking-consolidation
source-retention-vs-context-selection
```

Then decide whether any one has enough repeated mechanism value to become a
Candidate Pattern Bank entry or reviewed architecture note.

