---
record_kind: sandbox_slice_plan
slice_id: 2026-06-15-p2-29-formal-vault-execution-plan-sandbox
status: built_pending_review
truth_boundary: sandbox_only
---

# Slice Plan

## Goal

Build a sandbox-only formal-vault execution plan shape after P2-28 preflight.

## This Slice Does

- Defines a non-executable plan contract.
- Carries P2-28 source and target bindings forward by hash.
- Provides positive fixtures for approved, denied, and revision scenarios.
- Provides failure cases for forbidden operations, target drift, source drift,
  executable steps, real-vault access, and authority confusion.
- Provides a static prototype for operator review.

## This Slice Does Not

- Does not collect real approval.
- Does not store real user text.
- Does not read, scan, hash, snapshot, write, or sync the formal vault.
- Does not emit commands.
- Does not create reviewed knowledge, evidence support, action basis, or
  mainline approval.
