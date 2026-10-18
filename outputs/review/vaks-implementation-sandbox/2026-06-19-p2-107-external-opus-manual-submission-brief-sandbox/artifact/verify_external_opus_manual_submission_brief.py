import copy
import hashlib
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-19-p2-107-external-opus-manual-submission-brief-sandbox"
HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

PACKET_PATH = ARTIFACT_DIR / "external-opus-manual-submission-brief.json"
BRIEF_PATH = ARTIFACT_DIR / "external-opus-manual-submission-brief.md"
CAPTURE_PATH = ARTIFACT_DIR / "external-opus-response-capture-card.md"
FAILURE_CASE_PATH = FAILURE_DIR / "external-opus-manual-submission-brief-failures.json"

TOKENS = [
    "OPUS_PASS_SANDBOX_CLOSEOUT",
    "OPUS_REVISE_SANDBOX_CLOSEOUT",
    "OPUS_BLOCKED_NEEDS_USER",
]
EXPECTED_VALIDATOR = "2026-06-19-p2-102-opus-result-intake-dry-run-validator-sandbox"
FALSE_AUTHORITY_KEYS = [
    "external_submission_performed",
    "raw_opus_response_present",
    "actual_opus_result_present",
    "validated_opus_pass_present",
    "user_approval_present",
    "mainline_ready",
    "mainline_merge_allowed",
    "promotion_allowed",
    "reviewed_knowledge_ready",
    "evidence_support_ready",
    "action_basis_ready",
    "commit_push_sync_ready",
    "goal_complete_now",
]
FINAL_STATUSES = {
    "verification.md": "local_verification_passed",
    "reviewer-report.md": "review_pass_no_blocker",
    "boundary-audit.md": "pass_boundary",
    "product-acceptance-report.md": "pass_product_grade",
    "next-step.md": "pass_product_grade_pending_next_slice",
}


def load_json(path: Path, failures: list[str]) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        failures.append(f"json_load_failed:{path.name}:{exc}")
        return {}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def dotted_get(payload: dict, dotted_path: str):
    current = payload
    for part in dotted_path.split("."):
        if not isinstance(current, dict) or part not in current:
            return None
        current = current[part]
    return current


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


def validate(packet: dict, brief_text: str, capture_text: str) -> list[str]:
    failures = []
    if packet.get("record_kind") != "external_opus_manual_submission_brief":
        failures.append("record_kind_mismatch")
    if packet.get("slice_id") != SLICE_ID:
        failures.append("slice_id_mismatch")
    sources = packet.get("source_inputs", {})
    hashes = packet.get("source_hashes", {})
    manual = packet.get("manual_submission", {})
    authority = packet.get("authority_flags", {})

    for key in ["dispatch_packet", "dispatch_message", "dispatch_checklist"]:
        path_text = sources.get(key)
        if not path_text:
            failures.append(f"source_missing:{key}")
            continue
        source_path = REPO_ROOT / path_text
        if not source_path.exists():
            failures.append(f"source_file_missing:{key}")
            continue
        actual_hash = sha256_file(source_path)
        hash_key = f"{key}_sha256"
        if hashes.get(hash_key) != actual_hash:
            failures.append(f"source_hash_mismatch:{key.replace('_', '-')}")

    if hashes.get("dispatch_message_sha256") != hashes.get("expected_dispatch_message_sha256"):
        failures.append("source_hash_mismatch:dispatch_message")
    if hashes.get("dispatch_checklist_sha256") != hashes.get("expected_dispatch_checklist_sha256"):
        failures.append("source_hash_mismatch:dispatch_checklist")
    if manual.get("brief_ready") is not True:
        failures.append("brief_not_ready")
    if manual.get("required_conclusion_tokens") != TOKENS:
        failures.append("required_tokens_mismatch")
    if manual.get("post_response_validator_slice") != EXPECTED_VALIDATOR:
        failures.append("post_response_validator_mismatch")
    if manual.get("raw_response_present") is not False:
        failures.append("raw_response_present")
    if manual.get("new_sandbox_intake_required") is not True:
        failures.append("new_sandbox_intake_not_required")
    for key in FALSE_AUTHORITY_KEYS:
        if authority.get(key) is not False:
            failures.append(f"authority_overclaim:{key}")

    for token in TOKENS:
        if token not in brief_text or token not in capture_text:
            failures.append(f"missing_token:{token}")
    for phrase in [
        "not an Opus response",
        "not Opus approval",
        "not user approval",
        "not mainline readiness",
        "not reviewed knowledge",
        "not evidence support",
        "not action basis",
        "not goal completion",
    ]:
        if phrase not in brief_text:
            failures.append(f"brief_missing_phrase:{phrase}")
    for phrase in [
        "new sandbox-only intake slice",
        "Do not paste a response into this p2-107 slice",
        "raw Opus response is external review evidence only",
    ]:
        if phrase not in capture_text:
            failures.append(f"capture_missing_phrase:{phrase}")
    return failures


def mutate(packet: dict, mutation: str) -> tuple[dict, str, str]:
    mutated = copy.deepcopy(packet)
    brief = BRIEF_PATH.read_text(encoding="utf-8") if BRIEF_PATH.exists() else ""
    capture = CAPTURE_PATH.read_text(encoding="utf-8") if CAPTURE_PATH.exists() else ""
    if mutation == "dispatch_message_hash_drift":
        mutated["source_hashes"]["dispatch_message_sha256"] = "bad"
    elif mutation == "dispatch_checklist_hash_drift":
        mutated["source_hashes"]["dispatch_checklist_sha256"] = "bad"
    elif mutation == "missing_required_token":
        mutated["manual_submission"]["required_conclusion_tokens"] = TOKENS[:-1]
    elif mutation == "wrong_validator_slice":
        mutated["manual_submission"]["post_response_validator_slice"] = "wrong-validator"
    elif mutation == "brief_missing_boundary":
        brief = brief.replace("not an Opus response", "external review handoff")
    elif mutation == "capture_missing_new_sandbox":
        capture = capture.replace("new sandbox-only intake slice", "later place")
    elif mutation.endswith("_true"):
        key = mutation[:-5]
        mutated["authority_flags"][key] = True
    return mutated, brief, capture


def verify(final_gate: bool = False) -> dict:
    failures = []
    packet = load_json(PACKET_PATH, failures) if PACKET_PATH.exists() else {}
    brief = BRIEF_PATH.read_text(encoding="utf-8") if BRIEF_PATH.exists() else ""
    capture = CAPTURE_PATH.read_text(encoding="utf-8") if CAPTURE_PATH.exists() else ""
    if not brief:
        failures.append("missing_brief")
    if not capture:
        failures.append("missing_capture_card")
    failures.extend(validate(packet, brief, capture))

    fixtures = sorted(FIXTURES_DIR.glob("*.json"))
    if len(fixtures) != 4:
        failures.append(f"fixture_count_mismatch:{len(fixtures)}")
    for fixture_path in fixtures:
        fixture = load_json(fixture_path, failures)
        if fixture.get("expected") is not True:
            failures.append(f"fixture_not_positive:{fixture_path.name}")
        for key, expected in fixture.get("checks", {}).items():
            actual = dotted_get(packet, key)
            if actual != expected:
                failures.append(f"fixture_check_failed:{fixture_path.name}:{key}:expected={expected}:actual={actual}")

    failure_payload = load_json(FAILURE_CASE_PATH, failures) if FAILURE_CASE_PATH.exists() else {}
    cases = failure_payload.get("failure_cases", [])
    expected_failure_hits = 0
    if len(cases) < 18:
        failures.append(f"failure_case_count_too_low:{len(cases)}")
    for case in cases:
        mutated_packet, mutated_brief, mutated_capture = mutate(packet, case.get("mutation"))
        actual = validate(mutated_packet, mutated_brief, mutated_capture)
        if case.get("expected_failure") in actual:
            expected_failure_hits += 1
        else:
            failures.append(f"failure_case_not_caught:{case.get('id')}:{case.get('expected_failure')}:{actual}")

    if final_gate:
        for filename, expected in FINAL_STATUSES.items():
            path = SLICE_DIR / filename
            if not path.exists():
                failures.append(f"final_gate_missing_report:{filename}")
                continue
            actual = frontmatter_status(path)
            if actual != expected:
                failures.append(f"final_gate_status:{filename}:expected={expected}:actual={actual}")

    summary = {
        "brief_ready": bool(packet.get("manual_submission", {}).get("brief_ready")),
        "fixture_count": len(fixtures),
        "failure_case_count": len(cases),
        "expected_failure_hits": expected_failure_hits,
        "external_submission_performed": bool(packet.get("authority_flags", {}).get("external_submission_performed")),
        "raw_opus_response_present": bool(packet.get("authority_flags", {}).get("raw_opus_response_present")),
        "validated_opus_pass_present": bool(packet.get("authority_flags", {}).get("validated_opus_pass_present")),
        "user_approval_present": bool(packet.get("authority_flags", {}).get("user_approval_present")),
        "mainline_ready": bool(packet.get("authority_flags", {}).get("mainline_ready")),
        "goal_complete_now": bool(packet.get("authority_flags", {}).get("goal_complete_now")),
        "final_gate": final_gate,
    }
    return {"passed": not failures, "failures": failures, "summary": summary}


if __name__ == "__main__":
    result = verify(final_gate="--final-gate" in sys.argv)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    sys.exit(0 if result["passed"] else 1)
