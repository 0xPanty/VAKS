---
slice_id: 2026-06-19-p2-106-external-opus-dispatch-packet-sandbox
status: planned
---

# Slice Plan

## Goal

Create a sandbox-only dispatch packet that turns the p2-100 transfer ZIP, p2-101 operator kit, and p2-105 readiness cockpit into a single external Opus handoff surface.

## Scope

Write only under this slice path:

`outputs/review/vaks-implementation-sandbox/2026-06-19-p2-106-external-opus-dispatch-packet-sandbox/`

## Non-Scope

- No external Opus call is performed.
- No old slice, main architecture, README, wiki truth layer, template, tool, Obsidian, commit, push, or sync write is allowed.
- This slice is not an Opus result, user approval, mainline readiness, reviewed knowledge, evidence support, action basis, or goal completion.

## Acceptance

- Dispatch packet references the p2-100 ZIP and validates its SHA256.
- Dispatch message includes the required Opus task, allowed conclusion tokens, and boundary reminder.
- Checklist makes post-response intake route explicit.
- Verifier covers positive fixtures and negative authority/hash/freshness cases.
- Reviewer, Boundary Auditor, and GPT-5.5 extra-high Product Acceptance pass.
