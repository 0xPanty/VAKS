import copy
import hashlib
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-19-p2-106-external-opus-dispatch-packet-sandbox"
HERE = Path(__file__).resolve()
SLICE_DIR = HERE.parents[1]
REPO_ROOT = SLICE_DIR.parents[3]
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

PACKET_PATH = ARTIFACT_DIR / "external-opus-dispatch-packet.json"
MESSAGE_PATH = ARTIFACT_DIR / "external-opus-dispatch-message.md"
CHECKLIST_PATH = ARTIFACT_DIR / "external-opus-dispatch-checklist.md"
FAILURE_CASE_PATH = FAILURE_DIR / "external-opus-dispatch-failures.json"
EXPECTED_SOURCE_INPUTS = {
    "transfer_manifest": "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-100-opus-review-transfer-package-sandbox/artifact/opus-review-transfer-package-manifest.json",
    "transfer_zip": "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-100-opus-review-transfer-package-sandbox/artifact/opus-review-transfer-package.zip",
    "transfer_sha_file": "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-100-opus-review-transfer-package-sandbox/artifact/opus-review-transfer-package-sha256.txt",
    "operator_control_card": "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-101-opus-external-review-operator-kit-sandbox/artifact/opus-external-review-operator-control-card.json",
    "operator_submission_message": "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-101-opus-external-review-operator-kit-sandbox/artifact/opus-external-review-submission-message.md",
    "readiness_cockpit": "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-105-external-review-chain-readiness-preflight-sandbox/artifact/external-review-chain-readiness-cockpit.json",
}
EXPECTED_POST_RESPONSE_VALIDATOR = "2026-06-19-p2-102-opus-result-intake-dry-run-validator-sandbox"

TOKENS = [
    "OPUS_PASS_SANDBOX_CLOSEOUT",
    "OPUS_REVISE_SANDBOX_CLOSEOUT",
    "OPUS_BLOCKED_NEEDS_USER",
]

FALSE_AUTHORITY_KEYS = [
    "external_submission_performed",
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


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


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


def validate_packet(packet: dict, message_text: str, checklist_text: str) -> list[str]:
    failures = []
    if packet.get("record_kind") != "external_opus_dispatch_packet":
        failures.append("record_kind_mismatch")
    if packet.get("slice_id") != SLICE_ID:
        failures.append("slice_id_mismatch")

    dispatch = packet.get("dispatch", {})
    authority = packet.get("authority_flags", {})
    readiness = packet.get("readiness_inputs", {})
    source_inputs = packet.get("source_inputs", {})

    for key, expected_path in EXPECTED_SOURCE_INPUTS.items():
        actual_path = source_inputs.get(key)
        if actual_path != expected_path:
            failures.append(f"source_input_path_mismatch:{key}")
            continue
        if not (REPO_ROOT / actual_path).exists():
            failures.append(f"source_input_missing:{key}")

    if dispatch.get("dispatch_ready") is not True:
        failures.append("dispatch_not_ready")
    if dispatch.get("zip_exists") is not True:
        failures.append("zip_missing")
    zip_path = dispatch.get("zip_path")
    if not zip_path:
        failures.append("zip_path_missing")
    else:
        zip_abs = REPO_ROOT / zip_path
        if not zip_abs.exists():
            failures.append("zip_missing")
        elif sha256_file(zip_abs) != dispatch.get("zip_sha256"):
            failures.append("zip_hash_not_verified")
    if dispatch.get("actual_zip_sha256") != dispatch.get("zip_sha256"):
        failures.append("zip_hash_not_verified")
    if dispatch.get("zip_hash_verified") is not True:
        failures.append("zip_hash_not_verified")
    if dispatch.get("source_message_hash_verified") is not True:
        failures.append("source_message_hash_not_verified")
    operator_message_path = source_inputs.get("operator_submission_message")
    operator_card_path = source_inputs.get("operator_control_card")
    if operator_message_path and operator_card_path and (REPO_ROOT / operator_message_path).exists() and (REPO_ROOT / operator_card_path).exists():
        source_message_sha = sha256_text((REPO_ROOT / operator_message_path).read_text(encoding="utf-8"))
        operator_card = json.loads((REPO_ROOT / operator_card_path).read_text(encoding="utf-8"))
        expected_source_sha = operator_card.get("sha256", {}).get("submission_message")
        if dispatch.get("source_message_sha256") != source_message_sha:
            failures.append("source_message_sha_mismatch")
        if source_message_sha != expected_source_sha:
            failures.append("source_message_hash_not_verified")
    if dispatch.get("required_conclusion_tokens") != TOKENS:
        failures.append("required_tokens_mismatch")
    if dispatch.get("post_response_validator_slice") != EXPECTED_POST_RESPONSE_VALIDATOR:
        failures.append("post_response_validator_mismatch")

    for key in [
        "transfer_ready",
        "operator_ready_to_submit",
        "chain_ready_to_submit_external_opus",
        "chain_final_gates_true",
        "chain_product_grade",
    ]:
        if readiness.get(key) is not True:
            failures.append(f"readiness_input_not_true:{key}")

    for key in FALSE_AUTHORITY_KEYS:
        if authority.get(key) is not False:
            failures.append(f"authority_overclaim:{key}")

    for token in TOKENS:
        if token not in message_text:
            failures.append(f"message_missing_token:{token}")
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
        if phrase not in message_text:
            failures.append(f"message_missing_phrase:{phrase}")
    for phrase in [
        "Preserve the raw Opus response",
        "Validate the raw response with p2-102",
        "Do not edit old slices",
    ]:
        if phrase not in checklist_text:
            failures.append(f"checklist_missing_phrase:{phrase}")
    return failures


def mutate(packet: dict, mutation: str) -> tuple[dict, str, str]:
    mutated = copy.deepcopy(packet)
    message = MESSAGE_PATH.read_text(encoding="utf-8") if MESSAGE_PATH.exists() else ""
    checklist = CHECKLIST_PATH.read_text(encoding="utf-8") if CHECKLIST_PATH.exists() else ""
    if mutation == "zip_hash_mismatch":
        mutated["dispatch"]["actual_zip_sha256"] = "bad"
        mutated["dispatch"]["zip_hash_verified"] = False
    elif mutation == "source_message_hash_mismatch":
        mutated["dispatch"]["source_message_hash_verified"] = False
    elif mutation == "source_message_sha_field_mismatch":
        mutated["dispatch"]["source_message_sha256"] = "bad"
    elif mutation == "wrong_operator_message_path":
        mutated["source_inputs"]["operator_submission_message"] = "outputs/review/vaks-implementation-sandbox/wrong/message.md"
    elif mutation == "wrong_readiness_cockpit_path":
        mutated["source_inputs"]["readiness_cockpit"] = "outputs/review/vaks-implementation-sandbox/wrong/cockpit.json"
    elif mutation == "wrong_post_response_validator":
        mutated["dispatch"]["post_response_validator_slice"] = "wrong-validator"
    elif mutation == "dispatch_not_ready":
        mutated["dispatch"]["dispatch_ready"] = False
    elif mutation == "chain_not_ready":
        mutated["readiness_inputs"]["chain_ready_to_submit_external_opus"] = False
    elif mutation == "remove_required_token":
        mutated["dispatch"]["required_conclusion_tokens"] = TOKENS[:-1]
    elif mutation == "prompt_missing_boundary":
        message = message.replace("not an Opus response", "external result")
    elif mutation.endswith("_true"):
        key = mutation[:-5]
        mutated["authority_flags"][key] = True
    return mutated, message, checklist


def verify(final_gate: bool = False) -> dict:
    failures = []
    packet = load_json(PACKET_PATH, failures) if PACKET_PATH.exists() else {}
    message_text = MESSAGE_PATH.read_text(encoding="utf-8") if MESSAGE_PATH.exists() else ""
    checklist_text = CHECKLIST_PATH.read_text(encoding="utf-8") if CHECKLIST_PATH.exists() else ""
    if not message_text:
        failures.append("missing_dispatch_message")
    if not checklist_text:
        failures.append("missing_dispatch_checklist")
    failures.extend(validate_packet(packet, message_text, checklist_text))

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
        if "expected_tokens" in fixture and fixture["expected_tokens"] != packet.get("dispatch", {}).get("required_conclusion_tokens"):
            failures.append(f"fixture_token_check_failed:{fixture_path.name}")

    failure_payload = load_json(FAILURE_CASE_PATH, failures) if FAILURE_CASE_PATH.exists() else {}
    cases = failure_payload.get("failure_cases", [])
    expected_failure_hits = 0
    if len(cases) < 22:
        failures.append(f"failure_case_count_too_low:{len(cases)}")
    for case in cases:
        mutated_packet, mutated_message, mutated_checklist = mutate(packet, case.get("mutation"))
        actual = validate_packet(mutated_packet, mutated_message, mutated_checklist)
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
        "dispatch_ready": bool(packet.get("dispatch", {}).get("dispatch_ready")),
        "zip_hash_verified": bool(packet.get("dispatch", {}).get("zip_hash_verified")),
        "source_message_hash_verified": bool(packet.get("dispatch", {}).get("source_message_hash_verified")),
        "fixture_count": len(fixtures),
        "failure_case_count": len(cases),
        "expected_failure_hits": expected_failure_hits,
        "external_submission_performed": bool(packet.get("authority_flags", {}).get("external_submission_performed")),
        "actual_opus_result_present": bool(packet.get("authority_flags", {}).get("actual_opus_result_present")),
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
