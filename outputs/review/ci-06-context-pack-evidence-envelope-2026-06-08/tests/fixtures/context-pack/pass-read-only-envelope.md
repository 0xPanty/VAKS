---
fixture_id: ci06-pass-read-only-envelope
expected_result: PASS
context_pack:
  version: 1
  prompt: Should CI-06 be tested as a read-only envelope?
  budget:
    requested_tokens: 8000
    estimated_tokens: 1200
    truncated: false
    trimmed_sections: []
  project:
    root: null
    pages: 12
    pending_candidates: 1
    lint:
      warnings: 1
      errors: 0
      at: 2026-06-08T00:00:00Z
  primary:
    - id: context-pack-evidence-envelope
      title: Context Pack Evidence Envelope
      reasons:
        - title-match
      citations:
        - file: wiki/patterns/context-pack-evidence-envelope.md
      sourceWindows: []
  neighbors:
    - from: context-pack-evidence-envelope
      to: verified-vault-api-for-agent-brain
      reason: wikilink
  warnings:
    - code: pending-candidates
      message: One review candidate is pending approval.
  gaps:
    - code: missing-action-sufficiency
      message: Action basis readiness still needs evidence sufficiency.
  suggested_actions:
    - command: inspect evidence packet
      reason: Review anchors before promotion.
  source_windows: []
  read_only: true
  not_truth_layer: true
  not_action_basis: true
---

# PASS: Read-Only Envelope

This pack exposes context, warnings, gaps, and suggestions without writing wiki
or deciding truth.

