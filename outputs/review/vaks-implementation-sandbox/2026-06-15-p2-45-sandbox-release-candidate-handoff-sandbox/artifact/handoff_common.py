from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-45-sandbox-release-candidate-handoff-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-44-sandbox-evidence-ledger-sandbox"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[3]
SOURCE_ROOT = ROOT.parent / SOURCE_SLICE_ID
SOURCE_LEDGER = SOURCE_ROOT / "artifact" / "evidence-ledger.json"
SOURCE_PRODUCT_REPORT = SOURCE_ROOT / "product-acceptance-report.md"

VERSION = "sandbox-release-candidate-handoff-v1"
TRUTH_BOUNDARY = "sandbox_release_candidate_handoff_not_release_or_promotion"
PURPOSE = "user and follow-up-agent handoff package for sandbox product-grade evidence"
WRITE_SCOPE = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"

USER_QUESTIONS = [
    {
        "id": "what_landed",
        "label": "What landed?",
        "answer": "The original P0/P1/P1.5/P2 plan items landed as sandbox artifacts, with additional hardening slices.",
    },
    {
        "id": "was_it_tested",
        "label": "Was it tested?",
        "answer": "The evidence ledger reports 43 prior sandbox slices with verification evidence and Product PASS.",
    },
    {
        "id": "is_it_positive",
        "label": "Is it a positive improvement?",
        "answer": "Yes, as sandbox-only improvements supported by sandbox file evidence.",
    },
    {
        "id": "is_it_enterprise",
        "label": "Is it enterprise production?",
        "answer": "No. It is sandbox product-grade operator experience, not enterprise production readiness.",
    },
]

STOP_CONDITIONS = [
    "mainline_merge",
    "formal_vault_write_or_sync",
    "template_or_tool_movement",
    "commit_or_push",
    "action_basis_use",
    "reviewed_knowledge_or_evidence_support_claim",
    "enterprise_production_claim",
]

APPROVAL_REQUIREMENTS = [
    "separate explicit user approval for mainline merge",
    "separate explicit user approval for formal vault write or sync",
    "separate explicit user approval for template or tool movement",
    "separate explicit user approval for commit or push",
    "separate explicit user approval before using sandbox output as action basis",
]

OPERATION_FLAGS = [
    "formal_vault_read",
    "formal_vault_scan",
    "formal_vault_write",
    "formal_vault_hash",
    "formal_vault_snapshot",
    "formal_vault_state_check",
    "obsidian_sync",
    "commit",
    "push",
    "promotion",
    "dependency_install",
    "background_service",
    "mcp_write_tool",
    "hooks",
    "approval_collection",
    "user_instruction_collection",
    "user_wording_storage",
    "command_emitted",
    "execution_permission_granted",
    "execution_performed",
    "action_basis_creation",
    "reviewed_knowledge_creation",
    "evidence_support_creation",
    "mainline_merge",
    "dirty_tree_repair",
    "auto_advance",
]

REQUIRED_NON_CLAIMS = [
    "not release approval",
    "not promotion approval",
    "not mainline ready",
    "not enterprise production ready",
    "not formal vault approval",
    "not formal vault state",
    "not formal vault access",
    "not Obsidian sync",
    "not commit",
    "not push",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "not user approval",
    "not execution permission",
    "not auto advance",
]

ALLOWED_VIEWS = {
    "release-candidate-handoff",
    "plain-user-answer",
    "follow-up-agent-runbook",
}

REQUIRED_FIXTURES = {
    "valid-release-candidate-handoff.json": "release-candidate-handoff",
    "valid-plain-user-answer.json": "plain-user-answer",
    "valid-follow-up-agent-runbook.json": "follow-up-agent-runbook",
}

TOP_LEVEL_FIELDS = {
    "record_kind",
    "slice_id",
    "version",
    "truth_boundary",
    "purpose",
    "write_scope",
    "view",
    "source_snapshot",
    "release_candidate_status",
    "user_readable_answers",
    "follow_up_agent_runbook",
    "approval_requirements",
    "readiness_flags",
    "operation_performed_flags",
    "required_non_claims",
    "operator_note",
}

SOURCE_SNAPSHOT_FIELDS = {
    "source_slice_id",
    "ledger_path",
    "ledger_sha256",
    "product_report_path",
    "product_report_sha256",
    "source_product_status",
    "source_product_pass_text",
    "source_slice_count",
    "product_pass_count",
    "verification_present_count",
    "original_plan_item_count",
    "original_plan_product_pass_count",
    "hardening_slice_count",
    "plain_answer",
    "readiness_flags",
}

SOURCE_PLAIN_ANSWER_FIELDS = {
    "all_original_plan_items_landed_in_sandbox",
    "all_current_sandbox_slices_product_pass",
    "all_current_sandbox_slices_have_verification",
    "all_current_sandbox_slices_have_reviewer_and_boundary",
    "positive_improvement_supported",
    "enterprise_product_experience",
}

SOURCE_READINESS_FLAGS = {
    "sandbox_product_grade_evidence_ready",
    "enterprise_production_ready",
    "mainline_ready",
    "formal_vault_ready",
    "reviewed_knowledge_ready",
    "evidence_support_ready",
    "action_basis_ready",
}

HANDOFF_READINESS_FLAGS = {
    "sandbox_release_candidate_handoff_ready",
    "release_approved",
    "enterprise_production_ready",
    "mainline_ready",
    "formal_vault_ready",
    "reviewed_knowledge_ready",
    "evidence_support_ready",
    "action_basis_ready",
}


def rel(path: Path) -> str:
    return path.resolve().relative_to(WORKSPACE).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_status(path: Path) -> str | None:
    if not path.exists():
        return None
    match = re.search(r"^status:\s*(.+?)\s*$", path.read_text(encoding="utf-8", errors="ignore"), re.MULTILINE)
    return match.group(1).strip() if match else None


def source_snapshot() -> dict[str, Any]:
    ledger = read_json(SOURCE_LEDGER)
    product_text = SOURCE_PRODUCT_REPORT.read_text(encoding="utf-8", errors="ignore")
    return {
        "source_slice_id": SOURCE_SLICE_ID,
        "ledger_path": rel(SOURCE_LEDGER),
        "ledger_sha256": sha256_file(SOURCE_LEDGER),
        "product_report_path": rel(SOURCE_PRODUCT_REPORT),
        "product_report_sha256": sha256_file(SOURCE_PRODUCT_REPORT),
        "source_product_status": parse_status(SOURCE_PRODUCT_REPORT),
        "source_product_pass_text": "PASS_PRODUCT_GRADE" in product_text,
        "source_slice_count": ledger.get("source_slice_count"),
        "product_pass_count": ledger.get("product_pass_count"),
        "verification_present_count": ledger.get("verification_present_count"),
        "original_plan_item_count": ledger.get("original_plan_item_count"),
        "original_plan_product_pass_count": ledger.get("original_plan_product_pass_count"),
        "hardening_slice_count": ledger.get("hardening_slice_count"),
        "plain_answer": ledger.get("plain_answer", {}),
        "readiness_flags": ledger.get("readiness_flags", {}),
    }


def default_handoff(view: str = "release-candidate-handoff") -> dict[str, Any]:
    source = source_snapshot()
    return {
        "record_kind": "sandbox_release_candidate_handoff",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
        "view": view,
        "source_snapshot": source,
        "release_candidate_status": "sandbox_release_candidate_only_not_release",
        "user_readable_answers": copy.deepcopy(USER_QUESTIONS),
        "follow_up_agent_runbook": {
            "read_first": [
                rel(SOURCE_LEDGER),
                rel(SOURCE_PRODUCT_REPORT),
                f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/handoff-packets/release-candidate-handoff.md",
            ],
            "default_verification_command": f"python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_release_candidate_handoff.py",
            "allowed_next_mode": "sandbox_only_or_stop_for_user_approval",
            "must_not_do": STOP_CONDITIONS,
        },
        "approval_requirements": [
            {"id": item, "required": True, "authorized_now": False} for item in APPROVAL_REQUIREMENTS
        ],
        "readiness_flags": {
            "sandbox_release_candidate_handoff_ready": True,
            "release_approved": False,
            "enterprise_production_ready": False,
            "mainline_ready": False,
            "formal_vault_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
        },
        "operation_performed_flags": {name: False for name in OPERATION_FLAGS},
        "required_non_claims": list(REQUIRED_NON_CLAIMS),
    }


def validate_handoff(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in sorted(set(data) - TOP_LEVEL_FIELDS):
        errors.append(f"unknown_top_level_field:{key}")
    view = data.get("view")
    if view not in ALLOWED_VIEWS:
        errors.append(f"view_not_allowed:{view}")
    if "operator_note" in data:
        note = data.get("operator_note")
        if not isinstance(note, str) or "sandbox only" not in note:
            errors.append("operator_note_not_sandbox_only")

    expected = {
        "record_kind": "sandbox_release_candidate_handoff",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
        "release_candidate_status": "sandbox_release_candidate_only_not_release",
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"{key}_mismatch")

    current = default_handoff(data.get("view", "release-candidate-handoff"))
    for key in ["source_snapshot", "user_readable_answers", "follow_up_agent_runbook", "approval_requirements"]:
        if data.get(key) != current.get(key):
            errors.append(f"{key}_mismatch")

    source = data.get("source_snapshot", {})
    if set(source) != SOURCE_SNAPSHOT_FIELDS:
        errors.append("source_snapshot_keys_mismatch")
    if source.get("source_product_status") != "pass_product_grade":
        errors.append("source_product_status_not_pass")
    if source.get("source_product_pass_text") is not True:
        errors.append("source_product_pass_text_missing")
    for key, expected_value in {
        "source_slice_count": 43,
        "product_pass_count": 43,
        "verification_present_count": 43,
        "original_plan_item_count": 20,
        "original_plan_product_pass_count": 20,
    }.items():
        if source.get(key) != expected_value:
            errors.append(f"source_{key}_mismatch")
    if source.get("plain_answer", {}).get("enterprise_product_experience") != "sandbox_product_grade_operator_experience_not_enterprise_production":
        errors.append("source_enterprise_experience_mismatch")
    plain_answer = source.get("plain_answer", {})
    if set(plain_answer) != SOURCE_PLAIN_ANSWER_FIELDS:
        errors.append("source_plain_answer_keys_mismatch")
    source_flags = source.get("readiness_flags", {})
    if set(source_flags) != SOURCE_READINESS_FLAGS:
        errors.append("source_readiness_flags_keys_mismatch")
    if source_flags.get("sandbox_product_grade_evidence_ready") is not True:
        errors.append("source_sandbox_product_grade_evidence_ready_not_true")
    for flag in SOURCE_READINESS_FLAGS - {"sandbox_product_grade_evidence_ready"}:
        if source_flags.get(flag) is not False:
            errors.append(f"source_readiness_flag_not_false:{flag}")

    for item in data.get("approval_requirements", []):
        if item.get("required") is not True:
            errors.append(f"approval_not_required:{item.get('id')}")
        if item.get("authorized_now") is not False:
            errors.append(f"approval_authorized_now:{item.get('id')}")

    flags = data.get("readiness_flags", {})
    if set(flags) != HANDOFF_READINESS_FLAGS:
        errors.append("readiness_flags_keys_mismatch")
    if flags.get("sandbox_release_candidate_handoff_ready") is not True:
        errors.append("sandbox_release_candidate_handoff_ready_not_true")
    for flag in [
        "release_approved",
        "enterprise_production_ready",
        "mainline_ready",
        "formal_vault_ready",
        "reviewed_knowledge_ready",
        "evidence_support_ready",
        "action_basis_ready",
    ]:
        if flags.get(flag) is not False:
            errors.append(f"readiness_flag_not_false:{flag}")

    performed = data.get("operation_performed_flags", {})
    if set(performed) != set(OPERATION_FLAGS):
        errors.append("operation_performed_flags_mismatch")
    for name, value in performed.items():
        if value is not False:
            errors.append(f"operation_performed_not_false:{name}")

    if data.get("required_non_claims") != REQUIRED_NON_CLAIMS:
        errors.append("required_non_claims_mismatch")

    return errors


def make_failure_cases(base: dict[str, Any]) -> dict[str, list[str]]:
    cases: dict[str, list[str]] = {}
    index = 1

    def add(name: str, mutate, expected: list[str]) -> None:
        nonlocal index
        sample = copy.deepcopy(base)
        mutate(sample)
        filename = f"{index:03d}-{name}.json"
        write_json(ROOT / "failure-cases" / filename, sample)
        cases[filename] = expected
        index += 1

    for key in ["record_kind", "slice_id", "version", "truth_boundary", "purpose", "write_scope", "release_candidate_status"]:
        add(f"top-level-{key}", lambda sample, key=key: sample.__setitem__(key, "wrong"), [f"{key}_mismatch"])
    add("top-level-view", lambda sample: sample.__setitem__("view", "wrong"), ["view_not_allowed:wrong"])
    add("extra-top-level-release-approved-claim", lambda sample: sample.__setitem__("release_approved_claim", True), ["unknown_top_level_field:release_approved_claim"])
    add("extra-top-level-action-basis-ready-claim", lambda sample: sample.__setitem__("action_basis_ready_claim", True), ["unknown_top_level_field:action_basis_ready_claim"])

    add("source-snapshot-drift", lambda sample: sample.__setitem__("source_snapshot", {}), ["source_snapshot_mismatch", "source_snapshot_keys_mismatch", "source_product_status_not_pass", "source_product_pass_text_missing", "source_source_slice_count_mismatch", "source_product_pass_count_mismatch", "source_verification_present_count_mismatch", "source_original_plan_item_count_mismatch", "source_original_plan_product_pass_count_mismatch", "source_enterprise_experience_mismatch", "source_plain_answer_keys_mismatch", "source_readiness_flags_keys_mismatch", "source_sandbox_product_grade_evidence_ready_not_true", "source_readiness_flag_not_false:enterprise_production_ready", "source_readiness_flag_not_false:mainline_ready", "source_readiness_flag_not_false:formal_vault_ready", "source_readiness_flag_not_false:reviewed_knowledge_ready", "source_readiness_flag_not_false:evidence_support_ready", "source_readiness_flag_not_false:action_basis_ready"])
    add("user-answers-drift", lambda sample: sample.__setitem__("user_readable_answers", []), ["user_readable_answers_mismatch"])
    add("runbook-drift", lambda sample: sample.__setitem__("follow_up_agent_runbook", {}), ["follow_up_agent_runbook_mismatch"])
    add("source-product-count-drift", lambda sample: sample["source_snapshot"].__setitem__("product_pass_count", 42), ["source_snapshot_mismatch", "source_product_pass_count_mismatch"])
    add("source-enterprise-claim", lambda sample: sample["source_snapshot"]["plain_answer"].__setitem__("enterprise_product_experience", "enterprise_production_ready"), ["source_snapshot_mismatch", "source_enterprise_experience_mismatch"])
    add("source-readiness-enterprise-true", lambda sample: sample["source_snapshot"]["readiness_flags"].__setitem__("enterprise_production_ready", True), ["source_snapshot_mismatch", "source_readiness_flag_not_false:enterprise_production_ready"])
    add("extra-handoff-readiness-claim", lambda sample: sample["readiness_flags"].__setitem__("release_approved_claim", True), ["readiness_flags_keys_mismatch"])

    for requirement in APPROVAL_REQUIREMENTS:
        add(
            f"approval-{requirement.replace(' ', '-')}-authorized",
            lambda sample, requirement=requirement: next(item for item in sample["approval_requirements"] if item["id"] == requirement).__setitem__("authorized_now", True),
            ["approval_requirements_mismatch", f"approval_authorized_now:{requirement}"],
        )

    for flag in ["release_approved", "enterprise_production_ready", "mainline_ready", "formal_vault_ready", "reviewed_knowledge_ready", "evidence_support_ready", "action_basis_ready"]:
        add(f"readiness-{flag}-true", lambda sample, flag=flag: sample["readiness_flags"].__setitem__(flag, True), [f"readiness_flag_not_false:{flag}"])

    for op in OPERATION_FLAGS:
        add(f"operation-{op}-performed", lambda sample, op=op: sample["operation_performed_flags"].__setitem__(op, True), [f"operation_performed_not_false:{op}"])

    for non_claim in REQUIRED_NON_CLAIMS:
        add(f"missing-non-claim-{non_claim.replace(' ', '-')}", lambda sample, non_claim=non_claim: sample["required_non_claims"].remove(non_claim), ["required_non_claims_mismatch"])
    add("extra-non-claim", lambda sample: sample["required_non_claims"].append("unexpected expansion"), ["required_non_claims_mismatch"])

    return cases


def reset_generated() -> None:
    for directory in ["fixtures", "failure-cases", "prototype/sandbox-release-candidate-handoff", "handoff-packets"]:
        path = ROOT / directory
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)


def validate_failure_cases() -> dict[str, Any]:
    oracle_path = ROOT / "artifact" / "failure-case-oracle.json"
    failure_dir = ROOT / "failure-cases"
    if not oracle_path.exists():
        return {"count": 0, "actual_file_count": 0, "orphan_count": 0, "mismatches": [{"file": "failure-case-oracle.json", "expected": ["oracle_present"], "actual": ["missing_oracle"]}]}
    oracle = read_json(oracle_path).get("cases", {})
    actual_files = {path.name for path in failure_dir.glob("*.json")} if failure_dir.exists() else set()
    mismatches = []
    for extra in sorted(actual_files - set(oracle)):
        mismatches.append({"file": extra, "expected": ["not_present_outside_oracle"], "actual": ["orphan_failure_case_file"]})
    for name, expected in oracle.items():
        path = failure_dir / name
        if not path.exists():
            mismatches.append({"file": name, "expected": expected, "actual": ["missing_failure_case"]})
            continue
        actual = validate_handoff(read_json(path))
        if sorted(actual) != sorted(expected):
            mismatches.append({"file": name, "expected": expected, "actual": actual})
    return {"count": len(oracle), "actual_file_count": len(actual_files), "orphan_count": len(actual_files - set(oracle)), "mismatches": mismatches}


def validate_fixtures() -> dict[str, Any]:
    details = []
    errors = []
    fixture_dir = ROOT / "fixtures"
    actual_files = {path.name for path in fixture_dir.glob("*.json")} if fixture_dir.exists() else set()
    required_files = set(REQUIRED_FIXTURES)
    for missing in sorted(required_files - actual_files):
        errors.append({"file": missing, "errors": ["missing_required_fixture"]})
    for extra in sorted(actual_files - required_files):
        errors.append({"file": extra, "errors": ["unexpected_fixture_file"]})
    for path in sorted((ROOT / "fixtures").glob("*.json")):
        data = read_json(path)
        fixture_errors = validate_handoff(data)
        expected_view = REQUIRED_FIXTURES.get(path.name)
        if expected_view and data.get("view") != expected_view:
            fixture_errors.append(f"fixture_view_mismatch:{expected_view}")
        if path.name == "valid-release-candidate-handoff.json" and "operator_note" in data:
            fixture_errors.append("fixture_operator_note_unexpected")
        if path.name != "valid-release-candidate-handoff.json" and path.name in required_files and "operator_note" not in data:
            fixture_errors.append("fixture_operator_note_missing")
        details.append({"file": path.name, "errors": fixture_errors})
        if fixture_errors:
            errors.append({"file": path.name, "errors": fixture_errors})
    if not details:
        errors.append({"file": "fixtures", "errors": ["missing_positive_fixtures"]})
    return {"count": len(details), "fixtures": details, "errors": errors}


def validate_readout() -> dict[str, Any]:
    path = ROOT / "handoff-packets" / "release-candidate-handoff.md"
    issues: list[str] = []
    if not path.exists():
        return {"path": str(path), "issues": ["missing_readout"]}
    text = path.read_text(encoding="utf-8", errors="ignore")
    for phrase in ["sandbox release candidate only", "43", "20", "not enterprise production", "not mainline ready", "stop and ask"]:
        if phrase not in text:
            issues.append(f"readout_phrase_missing:{phrase}")
    for item in USER_QUESTIONS:
        if item["label"] not in text or item["answer"] not in text:
            issues.append(f"readout_answer_missing:{item['id']}")
    return {"path": str(path), "issues": issues}


def validate_prototype() -> dict[str, Any]:
    prototype = ROOT / "prototype" / "sandbox-release-candidate-handoff"
    issues: list[str] = []
    for item in ["index.html", "app.js", "receipt.json"]:
        if not (prototype / item).exists():
            issues.append(f"missing_prototype_file:{item}")
    if (prototype / "index.html").exists():
        html_raw = (prototype / "index.html").read_text(encoding="utf-8", errors="ignore")
        html = html_raw.lower()
        for forbidden in ["<form", "download", "contenteditable", "<a ", "h:\\obsidian", "onclick"]:
            if forbidden in html:
                issues.append(f"prototype_forbidden:{forbidden}")
        if html.count("data-user-question=") != len(USER_QUESTIONS):
            issues.append("prototype_user_question_count_mismatch")
        if html.count("data-stop-condition=") != len(STOP_CONDITIONS):
            issues.append("prototype_stop_condition_count_mismatch")
        for phrase in ["sandbox release candidate only", "not enterprise production", "not mainline ready", "not action basis"]:
            if phrase not in html:
                issues.append(f"prototype_phrase_missing:{phrase}")
    if (prototype / "app.js").exists():
        js = (prototype / "app.js").read_text(encoding="utf-8", errors="ignore").strip()
        if js != 'document.documentElement.dataset.releaseCandidateHandoffReady = "true";':
            issues.append("prototype_app_js_not_static_receipt_marker")
    if (prototype / "receipt.json").exists():
        receipt = read_json(prototype / "receipt.json")
        for flag in ["release_approved", "enterprise_production_ready", "mainline_ready", "formal_vault_accessed", "sync_performed", "commit_performed", "push_performed", "promotion_performed", "action_basis_created", "reviewed_knowledge_created", "evidence_support_created", "auto_advanced"]:
            if receipt.get(flag) is not False:
                issues.append(f"prototype_receipt_flag_not_false:{flag}")
        if receipt.get("required_non_claims") != REQUIRED_NON_CLAIMS:
            issues.append("prototype_receipt_non_claims_mismatch")
    return {"prototype_path": str(prototype), "issues": issues}


def validate_required_reports(final_gate: bool = False) -> dict[str, Any]:
    required = {
        "slice-plan.md": "built_pending_review",
        "source-map.md": "built_pending_review",
        "verification.md": "local_verification_passed_pending_review",
    }
    if final_gate:
        required.update(
            {
                "reviewer-report.md": "reviewer_pass",
                "boundary-audit.md": "boundary_pass",
                "product-acceptance-report.md": "pass_product_grade",
                "next-step.md": "pass_product_grade_pending_user_next_slice_decision",
            }
        )
    statuses: dict[str, str | None] = {}
    issues: list[str] = []
    for name, expected in required.items():
        status = parse_status(ROOT / name)
        statuses[name] = status
        if status != expected:
            issues.append(f"bad_status:{name}:{status}:expected:{expected}")
    return {"statuses": statuses, "issues": issues}


def validate_all(final_gate: bool = False) -> dict[str, Any]:
    fixture = ROOT / "fixtures" / "valid-release-candidate-handoff.json"
    config_errors = validate_handoff(read_json(fixture)) if fixture.exists() else ["missing_valid_fixture"]
    handoff_path = ROOT / "artifact" / "release-candidate-handoff.json"
    handoff_errors = validate_handoff(read_json(handoff_path)) if handoff_path.exists() else ["missing_release_candidate_handoff"]
    fixtures = validate_fixtures()
    failure_cases = validate_failure_cases()
    prototype = validate_prototype()
    readout = validate_readout()
    reports = validate_required_reports(final_gate=final_gate)
    failures: list[str] = []
    failures.extend(config_errors)
    failures.extend([f"release_handoff_error:{item}" for item in handoff_errors])
    failures.extend([f"fixture_error:{item['file']}" for item in fixtures["errors"]])
    failures.extend([f"failure_case_mismatch:{item['file']}" for item in failure_cases["mismatches"]])
    failures.extend(prototype["issues"])
    failures.extend(readout["issues"])
    failures.extend(reports["issues"])
    current = default_handoff()
    return {
        "slice_id": SLICE_ID,
        "passed": not failures,
        "failures": failures,
        "valid_config_errors": config_errors,
        "release_handoff_errors": handoff_errors,
        "positive_fixtures": fixtures,
        "failure_cases": failure_cases,
        "prototype": prototype,
        "readout": readout,
        "required_reports": reports,
        "source_snapshot": current["source_snapshot"],
        "release_candidate_status": current["release_candidate_status"],
        "non_claims": REQUIRED_NON_CLAIMS,
    }
