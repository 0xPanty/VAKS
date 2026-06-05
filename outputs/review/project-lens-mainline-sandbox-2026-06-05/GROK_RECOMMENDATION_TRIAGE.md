---
type: recommendation_triage
status: completed
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: grok-recommendations-agent-experience-triage
truth_boundary: sandbox triage only; not reviewed knowledge; not mainline architecture
---

# Grok Recommendation Triage

## My Operating Criterion

The user will not operate this knowledge system by hand.

So the deciding question is:

```text
Does this make future Codex/agent maintenance faster, safer, and less ambiguous?
```

Not:

```text
Does this look architecturally complete?
```

## Verdict Table

| Recommendation | Value For Agent Maintenance | Current Action | Reason |
|---|---|---|---|
| Core / Lens / Snapshot three-layer architecture | high | absorb into sandbox vocabulary now | It gives me a clean mental model: pure knowledge, project view, outcome record. |
| Knowledge Graph Lite | medium | keep as future extension | Related links are useful, but graph fields in Core can easily look like reviewed relations. |
| Warrant Gate as pluggable pipeline | medium-low now, high later | do not implement now | It would make v0.2.13 heavy again before repeated use proves the need. |
| `code_anchor` / structured target hints | high | absorb as structured `target_hint`, not rename to `code_anchor` | Typed target hints help me jump to files/modules. Keeping `target_hint` avoids false decision semantics. |
| Meta governance / ownership / annual review | low now, high later | defer | Too much ceremony before Project Lens has real usage load. |
| Future extension points | medium | record as non-blocking design reserve | Useful to avoid dead ends, but no automation/hooks now. |

## What I Would Keep If I Had To Maintain This Alone

Keep now:

```text
Core / Lens / Snapshot language
Project Lens sidecar
block-form entries
structured target_hint
anchor_health
boundary_snapshot seed shape
```

Keep only as future notes:

```text
Knowledge Graph Lite
pluggable Warrant Gate
owner / deprecation / annual review governance
Team Lens / Compliance Lens
GitHub/Jira/webhook integration
JSON export bundle
```

Do not add now:

```text
Core_KP / Lenses / Snapshots formal folders
related_kp fields in Core
pipeline checklist templates
database or graph runtime
CI checks for anchors
agent write automation
```

## Why Not Add Everything

The Project Lens design just survived pressure testing because it stayed small.

If all Grok suggestions are added now, the design risks turning into:

```text
schema + graph + governance + pipeline + automation
```

That is exactly the kind of system VAKS has been avoiding: it looks powerful, but it creates maintenance gravity before the workflow has repeated-use evidence.

## Current Recommendation

```yaml
absorb_now_in_sandbox:
  - Core / Lens / Snapshot vocabulary
  - structured target_hint
defer:
  - Knowledge Graph Lite
  - Warrant Gate pipeline
  - governance layer
  - external integrations
reject_now:
  - formal folders or databases as source of truth
  - Core schema changes
  - automatic AI confirmation of landed/boundary decisions
```
