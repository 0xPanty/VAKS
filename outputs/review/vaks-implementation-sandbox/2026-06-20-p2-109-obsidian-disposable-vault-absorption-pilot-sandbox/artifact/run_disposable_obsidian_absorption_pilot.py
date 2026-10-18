#!/usr/bin/env python3
"""Run a disposable Obsidian-vault absorption pilot for selected VAKS guards.

This runner creates a temporary Obsidian-style vault inside this sandbox slice,
runs the selected sandbox guards against positive and contaminated samples, then
deletes the temporary vault. It is not a mainline promotion tool.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from typing import Any


SLICE_ID = "2026-06-20-p2-109-obsidian-disposable-vault-absorption-pilot-sandbox"
HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
ARTIFACT_DIR = SLICE_DIR / "artifact"
RUNTIME_DIR = ARTIFACT_DIR / "_disposable_vault_runtime"
VAULT_DIR = RUNTIME_DIR / "Disposable-Obsidian-VAKS-Test-Vault"
REPORT_JSON = ARTIFACT_DIR / "obsidian_disposable_vault_absorption_pilot_report.json"
REPORT_MD = ARTIFACT_DIR / "obsidian_disposable_vault_absorption_pilot_report.md"
POSITIVE_ORACLE = SLICE_DIR / "fixtures" / "valid-disposable-vault-absorption-scenarios.json"
FAILURE_ORACLE = SLICE_DIR / "failure-cases" / "disposable-vault-contamination-failures.json"

GUARDS = {
    "body_hash": REPO_ROOT
    / "outputs/review/vaks-implementation-sandbox/2026-06-15-p0-03-body-hash-validator-sandbox/artifact/body_hash_validator_sandbox.py",
    "support_boundary": REPO_ROOT
    / "outputs/review/vaks-implementation-sandbox/2026-06-15-p0-04-support-boundary-validator-sandbox/artifact/support_boundary_validator_sandbox.py",
    "action_readiness": REPO_ROOT
    / "outputs/review/vaks-implementation-sandbox/2026-06-15-p0-05-action-readiness-validator-sandbox/artifact/action_readiness_validator_sandbox.py",
    "feedback": REPO_ROOT
    / "outputs/review/vaks-implementation-sandbox/2026-06-15-p0-06-feedback-validator-sandbox/artifact/feedback_validator_sandbox.py",
    "failure_matrix": REPO_ROOT
    / "outputs/review/vaks-implementation-sandbox/2026-06-15-p0-07-action-boundary-failure-matrix-sandbox/artifact/verify_failure_matrix_sandbox.py",
    "receipt": REPO_ROOT
    / "outputs/review/vaks-implementation-sandbox/2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox/artifact/receipt_validator_pilot.py",
    "runtime_exclusion": REPO_ROOT
    / "outputs/review/vaks-implementation-sandbox/2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox/artifact/runtime_artifact_exclusion_test.py",
}
SOURCE_MATRIX = REPO_ROOT / (
    "outputs/review/vaks-implementation-sandbox/"
    "2026-06-15-p0-07-action-boundary-failure-matrix-sandbox/"
    "artifact/action-boundary-failure-matrix.json"
)

FINAL_STATUSES = {
    "verification.md": "local_verification_passed",
    "reviewer-report.md": "review_pass_no_blocker",
    "boundary-audit.md": "pass_boundary",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_next_slice",
}


def canonical_body(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    while lines and lines[0].strip() == "":
        lines.pop(0)
    if lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    return "\n".join(lines).strip()


def sha256_body(text: str) -> str:
    return hashlib.sha256(canonical_body(text).encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_text(path: Path, text: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
    return path


def write_json(path: Path, payload: Any) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return path


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def run_command(args: list[str]) -> tuple[int, str, str]:
    env = os.environ.copy()
    env["PYTHONIOENCODING"] = "utf-8"
    proc = subprocess.run(
        args,
        cwd=REPO_ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        capture_output=True,
        env=env,
    )
    return proc.returncode, proc.stdout, proc.stderr


def parse_json_objects(stdout: str) -> list[dict[str, Any]]:
    objects: list[dict[str, Any]] = []
    for line in stdout.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        try:
            parsed = json.loads(stripped)
        except json.JSONDecodeError:
            continue
        if isinstance(parsed, dict):
            objects.append(parsed)
    return objects


def parse_single_json(stdout: str) -> dict[str, Any]:
    text = stdout.strip()
    if not text:
        return {}
    try:
        parsed = json.loads(text)
    except json.JSONDecodeError:
        objects = parse_json_objects(stdout)
        return objects[-1] if objects else {}
    return parsed if isinstance(parsed, dict) else {}


def payload_codes(payload: dict[str, Any]) -> list[str]:
    codes = payload.get("codes") or payload.get("issue_codes")
    if isinstance(codes, list):
        return [str(code) for code in codes]
    issues = payload.get("issues", [])
    if isinstance(issues, list):
        return [
            str(issue.get("code"))
            for issue in issues
            if isinstance(issue, dict) and issue.get("code")
        ]
    return []


def payload_matches_expected(payload: dict[str, Any], expected_result: str) -> bool:
    if expected_result == "valid_true":
        return payload.get("valid") is True
    if expected_result == "valid_false":
        return payload.get("valid") is False
    if expected_result == "status_pass":
        return payload.get("status") == "pass"
    if expected_result == "status_fail":
        return payload.get("status") == "fail"
    return False


def validate_oracles(case_results: list[dict[str, Any]], failures: list[str]) -> dict[str, Any]:
    positive_oracle = load_json(POSITIVE_ORACLE)
    failure_oracle = load_json(FAILURE_ORACLE)
    positive_cases = positive_oracle.get("positive_cases", [])
    failure_cases = failure_oracle.get("cases", [])
    by_id = {case["case_id"]: case for case in case_results}

    for expected in positive_cases:
        actual = by_id.get(expected["id"])
        if not actual:
            failures.append(f"positive_oracle_missing_case:{expected['id']}")
            continue
        if actual.get("guard") != expected.get("guard"):
            failures.append(
                f"positive_oracle_guard_mismatch:{expected['id']}:expected={expected.get('guard')}:actual={actual.get('guard')}"
            )
        if not payload_matches_expected(actual.get("payload", {}), expected.get("expected_result", "")):
            failures.append(f"positive_oracle_result_mismatch:{expected['id']}")
        if payload_codes(actual.get("payload", {})):
            failures.append(f"positive_oracle_unexpected_codes:{expected['id']}")

    for expected in failure_cases:
        actual = by_id.get(expected["id"])
        if not actual:
            failures.append(f"failure_oracle_missing_case:{expected['id']}")
            continue
        if actual.get("guard") != expected.get("guard"):
            failures.append(
                f"failure_oracle_guard_mismatch:{expected['id']}:expected={expected.get('guard')}:actual={actual.get('guard')}"
            )
        codes = payload_codes(actual.get("payload", {}))
        if not payload_matches_expected(actual.get("payload", {}), expected.get("expected_result", "")):
            failures.append(f"failure_oracle_result_mismatch:{expected['id']}")
        if expected.get("expected_code") not in codes:
            failures.append(f"failure_oracle_code_missing:{expected['id']}:{expected.get('expected_code')}")

    expected_ids = {case["id"] for case in positive_cases + failure_cases}
    actual_ids = set(by_id)
    if actual_ids != expected_ids:
        failures.append(f"oracle_case_set_mismatch:expected={sorted(expected_ids)}:actual={sorted(actual_ids)}")

    return {
        "fixture_oracle_used": True,
        "failure_oracle_used": True,
        "positive_oracle_case_count": len(positive_cases),
        "failure_oracle_case_count": len(failure_cases),
        "positive_oracle_sha256": sha256_file(POSITIVE_ORACLE),
        "failure_oracle_sha256": sha256_file(FAILURE_ORACLE),
    }


def create_vault_samples() -> dict[str, Path]:
    if RUNTIME_DIR.exists():
        shutil.rmtree(RUNTIME_DIR)
    VAULT_DIR.mkdir(parents=True)

    samples: dict[str, Path] = {}

    body_text = "# Candidate Body\n\nEvidence-aware review needs a checked body hash before approval reuse.\n"
    body_hash = sha256_body(body_text)
    samples["body_file"] = write_text(VAULT_DIR / "wiki/claims/bodies/body-hash-body.md", body_text)
    samples["body_hash_valid"] = write_text(
        VAULT_DIR / "wiki/claims/body-hash-valid.md",
        f"""---
record_kind: review_candidate
fixture_kind: disposable_obsidian_positive
candidate_body_location: bodies/body-hash-body.md
review_status: approved
writeback_ready: false
body_hash: {body_hash}
approval_integrity:
  approved_by: disposable-reviewer
  checked_body_hash: {body_hash}
expected_result: pass
---

# Body Hash Valid

This note simulates a reviewed candidate note inside a disposable Obsidian vault.
""",
    )
    samples["body_hash_tampered"] = write_text(
        VAULT_DIR / "wiki/claims/body-hash-tampered.md",
        f"""---
record_kind: review_candidate
fixture_kind: disposable_obsidian_failure
candidate_body_location: bodies/body-hash-body.md
review_status: approved
writeback_ready: false
body_hash: 0000{body_hash[4:]}
approval_integrity:
  approved_by: disposable-reviewer
  checked_body_hash: {body_hash}
expected_result: fail
---

# Body Hash Tampered

The recorded body_hash is stale and must be blocked.
""",
    )

    samples["support_boundary_valid"] = write_text(
        VAULT_DIR / "wiki/claims/support-boundary-valid.md",
        """---
record_kind: support_boundary_check
fixture_kind: disposable_obsidian_positive
target_ref: wiki/claims/example-claim.md#claim
proposed_support_ref: raw/articles/example-source.md#L20-L28
proposed_support_record_kind: raw_source_span
proposed_support_authority_bucket: raw_anchor
pack_role: support
support_claimed: true
evidence_role: direct_support
independent_anchor_ref: raw/articles/example-source.md#L20-L28
anchor_type: raw_span
anchor_selector: L20-L28
url_only: false
rank_counted_as_support: false
score_counted_as_support: false
graph_rank_as_trust: false
retrieval_rank_as_trust: false
feedback_used_as_support: false
source_summary_self_support: false
claim_note_self_support: false
legacy_raw_metadata_used_as_support: false
expected_result: pass
---

# Support Boundary Valid

Direct support comes from a raw anchored span.
""",
    )
    samples["candidate_claimed_as_support"] = write_text(
        VAULT_DIR / "wiki/claims/support-boundary-candidate-as-support.md",
        """---
record_kind: support_boundary_check
fixture_kind: disposable_obsidian_failure
target_ref: wiki/claims/example-claim.md#claim
proposed_support_ref: outputs/review/candidate-distillation.md
proposed_support_record_kind: candidate_summary
proposed_support_authority_bucket: candidate
pack_role: support
support_claimed: true
evidence_role: direct_support
independent_anchor_ref:
anchor_type: none
anchor_selector:
url_only: false
rank_counted_as_support: false
score_counted_as_support: false
graph_rank_as_trust: false
retrieval_rank_as_trust: false
feedback_used_as_support: false
source_summary_self_support: false
claim_note_self_support: false
legacy_raw_metadata_used_as_support: false
expected_result: fail
---

# Candidate Claimed As Support

Candidate material is being counted as support and must be blocked.
""",
    )

    samples["action_readiness_valid"] = write_text(
        VAULT_DIR / "actions/action-readiness-valid.md",
        """---
record_kind: action_readiness_check
action_id: AR-DISP-VALID
action_readiness: not_ready
action_basis_ready_claimed: false
action_mode: answer
operation_mode: read
significant_action: false
evidence_sufficiency: unchecked
evidence_support_status: not_checked
temporal_applicability: unchecked
replacement_basis_ref:
narrowed_scope_ref:
unresolved_risk: false
warnings_or_gaps_trimmed: false
missing_evidence_trimmed: false
intent_confirmation_required: false
intent_confirmed: false
success_criteria_present: false
basis_materials: [candidate, context_pack]
reviewed_write: false
target_bucket:
approved: false
checked_body_hash_present: false
rollback_required: false
rollback_plan_present: false
---

# Action Readiness Valid

An ordinary answer is not claiming action-basis readiness.
""",
    )
    samples["destructive_action_without_rollback"] = write_text(
        VAULT_DIR / "actions/action-delete-without-rollback.md",
        """---
record_kind: action_readiness_check
action_id: AR-DISP-FAIL
action_readiness: ready
action_basis_ready_claimed: true
action_mode: delete
operation_mode: suggest
significant_action: true
evidence_sufficiency: sufficient
evidence_support_status: supported
temporal_applicability: current
replacement_basis_ref:
narrowed_scope_ref:
unresolved_risk: false
warnings_or_gaps_trimmed: false
missing_evidence_trimmed: false
intent_confirmation_required: true
intent_confirmed: true
success_criteria_present: true
basis_materials: [reviewed_support, evidence_packet]
reviewed_write: false
target_bucket:
approved: true
checked_body_hash_present: true
rollback_required: false
rollback_plan_present: false
---

# Destructive Action Without Rollback

Delete is claimed ready without a rollback plan.
""",
    )

    samples["feedback_valid"] = write_text(
        VAULT_DIR / "feedback/feedback-valid.md",
        """---
record_kind: feedback_event
feedback_id: FB-DISP-VALID
event_type: action_outcome
feedback_type: stale
polarity: negative
project_ref: vaks
observed_in_context: disposable-vault-action
review_pressure_effect: review_due
review_due: true
review_due_ref: review_due_candidate_FB_DISP_VALID
effect_affects: [usefulness, scope_fit, review_due, implementation_note_candidate]
direct_mutations: []
never_affects_directly: [truth_confidence, verification_status, source_reliability]
truth_confidence_delta:
confidence_delta:
truth_confidence:
verification_status_delta:
verification_status:
source_reliability_delta:
source_reliability:
source_reliability_mutation_allowed: false
reviewed_note_mutation_allowed: false
mutates_reviewed_note: false
mutates_reviewed_relation: false
reviewed_relation_strength_delta:
action_basis_allowed: false
warning_code: feedback_not_truth
global_negative_knowledge: false
review_completed: false
creates_reviewed_relation: false
promotes_reviewed_knowledge: false
---

# Feedback Valid

Feedback creates review pressure but not truth mutation.
""",
    )
    samples["feedback_truth_confidence_mutation"] = write_text(
        VAULT_DIR / "feedback/feedback-truth-confidence-mutation.md",
        """---
record_kind: feedback_event
feedback_id: FB-DISP-FAIL
event_type: answer_helpful
feedback_type: useful
polarity: positive
project_ref: vaks
observed_in_context: disposable-vault-answer
review_pressure_effect: none
review_due: false
effect_affects: [usefulness]
direct_mutations: [truth_confidence]
never_affects_directly: [truth_confidence, verification_status, source_reliability]
truth_confidence_delta: 0.2
confidence_delta:
truth_confidence:
verification_status_delta:
verification_status:
source_reliability_delta:
source_reliability:
source_reliability_mutation_allowed: false
reviewed_note_mutation_allowed: false
mutates_reviewed_note: false
mutates_reviewed_relation: false
reviewed_relation_strength_delta:
action_basis_allowed: false
warning_code: feedback_not_truth
global_negative_knowledge: false
review_completed: false
creates_reviewed_relation: false
promotes_reviewed_knowledge: false
---

# Feedback Truth Confidence Mutation

Feedback tries to modify truth confidence directly.
""",
    )

    samples["receipt_valid"] = write_text(
        VAULT_DIR / "receipts/retrieval-receipt-valid.md",
        """---
record_kind: retrieval_receipt
expected_valid: true
expected_codes: []
receipt_id: rr-disp-valid-direct-anchor
query_id: q-disp-valid-direct-anchor
query_mode: review
requested_authority_bucket: raw_anchor
included_buckets: [raw_anchor]
rrf_scope: same_authority_bucket_only
cross_bucket_rrf_used: false
selected_item_authority_buckets: [raw_anchor]
selected_item_pack_roles: [support]
selected_item_action_basis_allowed: false
selected_by_claims_support: false
scores_are_support: false
graph_rank_claims_trust: false
legacy_raw_metadata_used: false
support_result: supported
support_evidence_role: direct_support
support_anchor_kind: excerpt_or_passage
independent_anchor_ref: raw/articles/example-source.md#L10-L18
receipt_claims: []
selected_by_is_not_support: true
same_bucket_rrf_only: true
cross_bucket_rank_not_authority: true
legacy_raw_metadata_excluded: true
candidate_overlay_feedback_not_support: true
url_only_not_direct_support: true
graph_rank_not_trust: true
receipt_not_review_approval: true
receipt_not_action_basis: true
receipt_not_reviewed_knowledge: true
---

# Retrieval Receipt Valid

The receipt has a raw anchor and does not claim action authority.
""",
    )
    samples["retrieval_candidate_as_support"] = write_text(
        VAULT_DIR / "receipts/retrieval-candidate-as-support.md",
        """---
record_kind: retrieval_receipt
expected_valid: false
expected_codes: [RV_CANDIDATE_OVERLAY_FEEDBACK_AS_SUPPORT]
receipt_id: rr-disp-fail-candidate-support
query_id: q-disp-fail-candidate-support
query_mode: action
requested_authority_bucket: candidate
included_buckets: [candidate]
rrf_scope: same_authority_bucket_only
selected_item_authority_buckets: [candidate]
selected_item_pack_roles: [support]
selected_item_action_basis_allowed: false
---

# Retrieval Candidate As Support

A candidate distillation is being marked as final support.
""",
    )

    samples["runtime_artifact_exclusion_valid"] = write_json(
        VAULT_DIR / "runtime/runtime-exclusion-valid.json",
        {
            "record_kind": "runtime_artifact_exclusion_manifest",
            "scenario_id": "ra-disp-valid-mixed-corpus-runtime-excluded",
            "expected_valid": True,
            "expected_codes": [],
            "exclude_runtime_artifacts": True,
            "items": [
                {
                    "id": "reviewed_note_001",
                    "path": "wiki/summaries/example-reviewed-summary.md",
                    "artifact_kind": "reviewed_summary",
                    "runtime_artifact": False,
                    "seen_by_retrieval": True,
                    "selected": True,
                    "excluded": False,
                    "pack_role": "orientation",
                    "authority_bucket": "reviewed",
                },
                {
                    "id": "pycache_001",
                    "path": "outputs/review/example/artifact/__pycache__/runner.cpython-310.pyc",
                    "artifact_kind": "python_cache",
                    "runtime_artifact": True,
                    "seen_by_retrieval": True,
                    "selected": False,
                    "excluded": True,
                    "excluded_reason": "runtime_artifact_excluded",
                    "pack_role": "none",
                    "authority_bucket": "runtime_artifact",
                },
            ],
        },
    )
    samples["runtime_pycache_selected"] = write_json(
        VAULT_DIR / "runtime/runtime-pycache-selected.json",
        {
            "record_kind": "runtime_artifact_exclusion_manifest",
            "scenario_id": "ra-disp-fail-pycache-selected",
            "expected_valid": False,
            "expected_codes": ["RA_RUNTIME_ARTIFACT_SELECTED"],
            "exclude_runtime_artifacts": True,
            "items": [
                {
                    "id": "pycache_selected",
                    "path": "outputs/review/example/artifact/__pycache__/runner.cpython-310.pyc",
                    "artifact_kind": "python_cache",
                    "runtime_artifact": True,
                    "seen_by_retrieval": True,
                    "selected": True,
                    "excluded": True,
                    "excluded_reason": "runtime_artifact_excluded",
                    "pack_role": "orientation",
                    "authority_bucket": "runtime_artifact",
                }
            ],
        },
    )

    matrix_copy = VAULT_DIR / "matrices/action-boundary-failure-matrix.json"
    matrix_copy.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE_MATRIX, matrix_copy)
    samples["failure_matrix_valid"] = matrix_copy

    return samples


def summarize_command(case_id: str, guard: str, path: Path, rc: int, payload: dict[str, Any]) -> dict[str, Any]:
    rel = path.relative_to(VAULT_DIR).as_posix()
    return {
        "case_id": case_id,
        "guard": guard,
        "runtime_sample_path": rel,
        "runtime_sample_sha256": sha256_file(path),
        "return_code": rc,
        "payload": payload,
    }


def run_pilot() -> dict[str, Any]:
    failures: list[str] = []
    expected_failure_hits = 0
    positive_hits = 0
    case_results: list[dict[str, Any]] = []

    samples = create_vault_samples()
    try:
        for case_id, sample_key, expected_valid, expected_code in [
            ("body_hash_valid", "body_hash_valid", True, None),
            ("body_hash_tampered", "body_hash_tampered", False, "body_hash_mismatch"),
        ]:
            rc, stdout, stderr = run_command(
                [sys.executable, "-B", str(GUARDS["body_hash"]), "--json", str(samples[sample_key])]
            )
            objects = parse_json_objects(stdout)
            payload = objects[0] if objects else {}
            case_results.append(summarize_command(case_id, "p0-03", samples[sample_key], rc, payload))
            if expected_valid is True and rc == 0 and payload.get("valid") is True:
                positive_hits += 1
            elif expected_valid is False and rc != 0 and payload.get("valid") is False and expected_code in payload.get("codes", []):
                expected_failure_hits += 1
            else:
                failures.append(f"{case_id}_unexpected_result")

        for case_id, sample_key, expected_valid, expected_code in [
            ("support_boundary_valid", "support_boundary_valid", True, None),
            ("candidate_claimed_as_support", "candidate_claimed_as_support", False, "candidate_as_support"),
        ]:
            rc, stdout, stderr = run_command(
                [sys.executable, "-B", str(GUARDS["support_boundary"]), "--json", str(samples[sample_key])]
            )
            objects = parse_json_objects(stdout)
            payload = objects[0] if objects else {}
            case_results.append(summarize_command(case_id, "p0-04", samples[sample_key], rc, payload))
            if expected_valid is True and rc == 0 and payload.get("valid") is True:
                positive_hits += 1
            elif expected_valid is False and rc != 0 and payload.get("valid") is False and expected_code in payload.get("codes", []):
                expected_failure_hits += 1
            else:
                failures.append(f"{case_id}_unexpected_result")

        for case_id, sample_key, expected_status, expected_code in [
            ("action_readiness_valid", "action_readiness_valid", "pass", None),
            ("destructive_action_without_rollback", "destructive_action_without_rollback", "fail", "AR_DESTRUCTIVE_MISSING_ROLLBACK"),
        ]:
            rc, stdout, stderr = run_command(
                [sys.executable, "-B", str(GUARDS["action_readiness"]), "--json", str(samples[sample_key])]
            )
            payload = parse_single_json(stdout)
            case_results.append(summarize_command(case_id, "p0-05", samples[sample_key], rc, payload))
            if expected_status == "pass" and payload.get("status") == "pass":
                positive_hits += 1
            elif expected_status == "fail" and payload.get("status") == "fail" and expected_code in [
                issue.get("code") for issue in payload.get("issues", [])
            ]:
                expected_failure_hits += 1
            else:
                failures.append(f"{case_id}_unexpected_result")

        for case_id, sample_key, expected_status, expected_code in [
            ("feedback_valid", "feedback_valid", "pass", None),
            ("feedback_truth_confidence_mutation", "feedback_truth_confidence_mutation", "fail", "FB_TRUTH_CONFIDENCE_MUTATION"),
        ]:
            rc, stdout, stderr = run_command(
                [sys.executable, "-B", str(GUARDS["feedback"]), "--json", str(samples[sample_key])]
            )
            payload = parse_single_json(stdout)
            case_results.append(summarize_command(case_id, "p0-06", samples[sample_key], rc, payload))
            if expected_status == "pass" and payload.get("status") == "pass":
                positive_hits += 1
            elif expected_status == "fail" and payload.get("status") == "fail" and expected_code in [
                issue.get("code") for issue in payload.get("issues", [])
            ]:
                expected_failure_hits += 1
            else:
                failures.append(f"{case_id}_unexpected_result")

        rc, stdout, stderr = run_command(
            [sys.executable, "-B", str(GUARDS["failure_matrix"]), "--json", str(samples["failure_matrix_valid"])]
        )
        payload = parse_single_json(stdout)
        case_results.append(summarize_command("failure_matrix_valid", "p0-07", samples["failure_matrix_valid"], rc, payload))
        if rc == 0 and payload.get("status") == "pass":
            positive_hits += 1
        else:
            failures.append("failure_matrix_valid_failed")

        for case_id, sample_key, expected_valid, expected_code in [
            ("receipt_valid", "receipt_valid", True, None),
            ("retrieval_candidate_as_support", "retrieval_candidate_as_support", False, "RV_CANDIDATE_OVERLAY_FEEDBACK_AS_SUPPORT"),
        ]:
            rc, stdout, stderr = run_command(
                [sys.executable, "-B", str(GUARDS["receipt"]), str(samples[sample_key])]
            )
            payload = parse_single_json(stdout)
            case_results.append(summarize_command(case_id, "p1-08", samples[sample_key], rc, payload))
            if expected_valid is True and payload.get("valid") is True:
                positive_hits += 1
            elif expected_valid is False and payload.get("valid") is False and expected_code in payload.get("issue_codes", []):
                expected_failure_hits += 1
            else:
                failures.append(f"{case_id}_unexpected_result")

        for case_id, sample_key, expected_valid, expected_code in [
            ("runtime_artifact_exclusion_valid", "runtime_artifact_exclusion_valid", True, None),
            ("runtime_pycache_selected", "runtime_pycache_selected", False, "RA_RUNTIME_ARTIFACT_SELECTED"),
        ]:
            rc, stdout, stderr = run_command(
                [sys.executable, "-B", str(GUARDS["runtime_exclusion"]), str(samples[sample_key])]
            )
            payload = parse_single_json(stdout)
            case_results.append(summarize_command(case_id, "p1-10", samples[sample_key], rc, payload))
            if expected_valid is True and payload.get("valid") is True:
                positive_hits += 1
            elif expected_valid is False and payload.get("valid") is False and expected_code in payload.get("issue_codes", []):
                expected_failure_hits += 1
            else:
                failures.append(f"{case_id}_unexpected_result")

    finally:
        if RUNTIME_DIR.exists():
            shutil.rmtree(RUNTIME_DIR)

    runtime_exists_after_cleanup = RUNTIME_DIR.exists()
    if runtime_exists_after_cleanup:
        failures.append("disposable_vault_not_deleted")

    oracle_summary = validate_oracles(case_results, failures)

    report = {
        "slice_id": SLICE_ID,
        "passed": not failures,
        "failures": failures,
        "summary": {
            "guard_count": 7,
            "positive_case_count": 7,
            "positive_hits": positive_hits,
            "failure_case_count": 6,
            "expected_failure_hits": expected_failure_hits,
            **oracle_summary,
            "disposable_vault_created": True,
            "disposable_vault_deleted": not runtime_exists_after_cleanup,
            "runtime_samples_retained": runtime_exists_after_cleanup,
            "formal_obsidian_vault_touched": False,
            "mainline_files_touched": False,
            "tools_promoted": False,
            "templates_touched": False,
            "wiki_truth_layers_touched": False,
            "commit_push_sync": False,
            "mainline_ready": False,
            "action_basis_created": False,
            "reviewed_knowledge_created": False,
        },
        "case_results": case_results,
    }
    write_json(REPORT_JSON, report)
    write_text(REPORT_MD, render_markdown_report(report))
    return report


def render_markdown_report(report: dict[str, Any]) -> str:
    summary = report["summary"]
    lines = [
        "# Obsidian Disposable Vault Absorption Pilot Report",
        "",
        f"Passed: `{str(report['passed']).lower()}`",
        "",
        "## Summary",
        "",
        f"- Guards tested: {summary['guard_count']}",
        f"- Positive cases: {summary['positive_hits']} / {summary['positive_case_count']}",
        f"- Failure cases caught: {summary['expected_failure_hits']} / {summary['failure_case_count']}",
        f"- Positive oracle cases: {summary['positive_oracle_case_count']}",
        f"- Failure oracle cases: {summary['failure_oracle_case_count']}",
        f"- Fixture oracle used: {summary['fixture_oracle_used']}",
        f"- Failure oracle used: {summary['failure_oracle_used']}",
        f"- Disposable vault deleted: {summary['disposable_vault_deleted']}",
        f"- Runtime samples retained: {summary['runtime_samples_retained']}",
        f"- Formal Obsidian vault touched: {summary['formal_obsidian_vault_touched']}",
        f"- Mainline files touched: {summary['mainline_files_touched']}",
        f"- Tools promoted: {summary['tools_promoted']}",
        "",
        "## Interpretation",
        "",
        "The seven candidates can be exercised as sandbox-only lazy gates against Obsidian-style Markdown and JSON records.",
        "This proves absorption readiness, not mainline absorption.",
        "",
        "## Case Results",
        "",
        "| Case | Guard | Runtime sample deleted after run | Result | Codes |",
        "| --- | --- | --- | --- | --- |",
    ]
    for case in report["case_results"]:
        payload = case.get("payload", {})
        codes = payload_codes(payload)
        result = payload.get("valid")
        if result is None:
            result = payload.get("status")
        lines.append(
            f"| `{case['case_id']}` | `{case['guard']}` | yes | `{result}` | `{', '.join(codes)}` |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This report is sandbox evidence only. It is not a mainline merge, not reviewed knowledge, not evidence support, not action basis, not Opus approval, not user approval, not commit, not push, and not sync.",
        ]
    )
    return "\n".join(lines) + "\n"


def frontmatter_status(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return "missing_frontmatter"
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def final_gate_failures(report: dict[str, Any]) -> list[str]:
    failures: list[str] = []
    if not report.get("passed"):
        failures.append("pilot_report_not_passed")
    summary = report.get("summary", {})
    expected = {
        "guard_count": 7,
        "positive_case_count": 7,
        "positive_hits": 7,
        "failure_case_count": 6,
        "expected_failure_hits": 6,
        "fixture_oracle_used": True,
        "failure_oracle_used": True,
        "positive_oracle_case_count": 7,
        "failure_oracle_case_count": 6,
        "disposable_vault_deleted": True,
        "runtime_samples_retained": False,
        "formal_obsidian_vault_touched": False,
        "mainline_files_touched": False,
        "tools_promoted": False,
        "templates_touched": False,
        "wiki_truth_layers_touched": False,
        "commit_push_sync": False,
        "mainline_ready": False,
        "action_basis_created": False,
        "reviewed_knowledge_created": False,
    }
    for key, expected_value in expected.items():
        if summary.get(key) != expected_value:
            failures.append(f"summary_mismatch:{key}:expected={expected_value}:actual={summary.get(key)}")
    for filename, expected_status in FINAL_STATUSES.items():
        path = SLICE_DIR / filename
        if not path.exists():
            failures.append(f"missing_report:{filename}")
            continue
        actual = frontmatter_status(path)
        if actual != expected_status:
            failures.append(f"status_mismatch:{filename}:expected={expected_status}:actual={actual}")
    return failures


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(description="Run p2-109 disposable vault absorption pilot.")
    parser.add_argument("--final-gate", action="store_true", help="Also enforce final report statuses.")
    args = parser.parse_args(argv)

    report = run_pilot()
    gate_failures = final_gate_failures(report) if args.final_gate else []
    result = {
        "passed": report["passed"] and not gate_failures,
        "failures": report["failures"] + gate_failures,
        "summary": report["summary"] | {"final_gate": args.final_gate},
    }
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
