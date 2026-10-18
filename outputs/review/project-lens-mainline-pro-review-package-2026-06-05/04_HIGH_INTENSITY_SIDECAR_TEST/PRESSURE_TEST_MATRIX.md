---
type: pressure_test_matrix
status: active
created_at: 2026-06-05
project: verified-action-knowledge-system
scope: project-lens-mainline-integration-pressure-test
truth_boundary: test matrix only; not reviewed knowledge; not mainline architecture
---

# Pressure Test Matrix

## Test Dimensions

| ID | Dimension | Failure We Are Trying To Catch |
|---|---|---|
| T01 | Format scalability | Markdown wide table becomes unreadable or unparsable. |
| T02 | Source boundary | Source routing starts saying VAKS should adopt/reject. |
| T03 | Generic knowledge pollution | Project stance leaks into original knowledge point body/YAML. |
| T04 | Ledger drift | Derived view becomes primary authoring surface again. |
| T05 | ADR leakage | Project Lens sounds like context/decision/consequence. |
| T06 | Truth leakage | stance / route / reuse count becomes support strength. |
| T07 | Outcome confusion | landed/failure is stored as live status instead of snapshot. |
| T08 | v0.2.13 false trigger | Ordinary lens tagging becomes heavy action-basis workflow. |
| T09 | v0.2.13 missed trigger | Lens item used for action without non-circular warrant. |
| T10 | target_hint drift | A line/path hint becomes stale or implies a decision. |
| T11 | Candidate Pattern bloat | Pattern Bank becomes a pretty-name directory. |
| T12 | Obsidian isolation | Test files pollute root docs or ordinary notes. |
| T13 | Agent recovery | A fresh window can tell what is candidate vs mainline. |
| T14 | Negative knowledge | avoid/non-fit fails to become triggerable boundary knowledge. |
| T15 | AI authority | AI suggestions confirm adoption/rejection/landed by themselves. |
| T16 | Cross-project reuse | One project's stance contaminates another project. |
| T17 | Search/readability | Human and AI can find an entry quickly. |
| T18 | Mainline patch minimality | Candidate wording tries to create schema/template/system. |
| T19 | Obsidian readability | Block-form sidecar is legible in Obsidian markdown. |
| T20 | Commit scope | Future commit plan can stage only intended files. |
| T21 | Three-layer clarity | Core / Lens / Snapshot becomes a folder/schema migration instead of vocabulary. |
| T22 | Structured target hints | `target_hint` is too vague for agents or too strong like a code decision. |
| T23 | Graph-lite overreach | related/depends/conflicts fields create fake reviewed relations. |
| T24 | Pipeline overreach | Warrant Gate becomes a heavy workflow for ordinary use. |
| T25 | Governance overreach | ownership/deprecation/review policies create maintenance burden too early. |
| T26 | Future extension leakage | integrations/webhooks/agent writes imply automation authority. |
| T27 | Agent navigation chain | Lens entry cannot directly reach its candidate pattern or source refs. |
| T28 | Source routing integrity | Source routing names candidate patterns that do not exist. |
| T29 | Snapshot linkage | outcome_ref cannot link to landed/boundary snapshots without stance confusion. |
| T30 | Automation patch safety | Repeated YAML fields or naive regex parsing silently corrupt entries. |

## Method

Each test should record:

```text
setup
attack / pressure
expected behavior
observed behavior
verdict
patch if needed
retest result
```
