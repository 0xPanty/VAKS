---
record_type: review-candidate
status: pending
knowledge_status: candidate
promotion_gate: v0_2_13_required
action_basis_allowed: false
truth_mutation_allowed: false
candidate_id: CI-03-source-hash-registry-and-idempotent-ingest
source_candidate_points:
  - CI-03
promotion_target: pattern
proposed_title: Source Hash Registry And Idempotent Ingest
proposed_path: wiki/patterns/source-hash-registry-and-idempotent-ingest.md
review_object_state: fixed_for_review
candidate_body_location: "# Candidate Body"
body_hash: sha256:cdafe6e912ae5fc9799aab46d5021534b685262128bad1a27ee18bf85ccfd9b7
body_hash_algorithm: sha256_utf8_lf_trim_body_without_heading
evidence_packet_ref: outputs/review/promotion-funnel-pilot-2026-06-08/PROMOTION_EVIDENCE_PACKETS.md#EP-03
source_anchor_refs:
  - raw/repos/_snapshots/openkb-main-2026-05-27.zip::OpenKB-main/openkb/state.py:8-25
  - raw/repos/_snapshots/openkb-main-2026-05-27.zip::OpenKB-main/openkb/state.py:39-42
  - raw/repos/_snapshots/openkb-main-2026-05-27.zip::OpenKB-main/openkb/state.py:80-87
  - raw/repos/_snapshots/openkb-main-2026-05-27.zip::OpenKB-main/openkb/converter.py:36-61
  - raw/repos/_snapshots/openkb-main-2026-05-27.zip::OpenKB-main/openkb/cli.py:348-361
scope_limits:
  - Applies to source lifecycle hygiene, duplicate detection, and deliberate replacement routing.
  - Does not make source hash a truth-confidence signal.
risk_flags:
  - Same content can arrive from different origins, so provenance must be preserved.
  - A derived hash registry must not replace the Markdown source record as the system of record without a separate decision.
known_counterevidence: []
missing_evidence:
  - Local VAKS remove/recompile flow before implementation work.
approval_integrity:
  approved_by:
  approval_source:
  approved_at:
  llm_assisted: true
  checked_specific_evidence: false
  checked_body_hash:
---

# Candidate: Source Hash Registry And Idempotent Ingest

## Candidate Body

Source ingest should keep a content-hash registry or derived index so repeated
source intake can skip duplicates or route replacement and recompile
deliberately.

This pattern is source-lifecycle infrastructure. It helps with duplicate
detection, replay safety, and source hygiene. It does not prove that a source is
true, reliable, or sufficient for promotion.

## Evidence Packet Summary

Support comes from OpenKB source-code anchors.

- `state.py` defines a hash registry, lookup helpers, persistent add, and SHA-256 file hashing.
- `converter.py` computes the file hash before conversion and skips already-known files.
- `cli.py` registers the hash only after successful compilation.

## Self-Support Check

```text
self_support_loop: false
support_basis: independent local OpenKB source snapshot code anchors
support_state: supported
object_integrity_ready: true
approval_readiness: blocked_pending_approval
```

## Minimal Scope

Promote only this boundary:

```text
source record
-> derived content hash / registry
-> duplicate or replacement routing
-> source-lifecycle audit
```

Preserve origin/provenance even when content hash matches.

## Forbidden Interpretations

```text
hash = truth confidence
same hash = same provenance
registry = reviewed knowledge store
source hygiene = evidence support
```
