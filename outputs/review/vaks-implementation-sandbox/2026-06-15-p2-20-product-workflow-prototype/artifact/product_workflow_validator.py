from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

SLICE_ID = "2026-06-15-p2-20-product-workflow-prototype"
RECORD_KIND = "vaks_product_workflow_prototype"
SLICE_ROOT = Path(
    "outputs/review/vaks-implementation-sandbox/"
    "2026-06-15-p2-20-product-workflow-prototype"
)
REPO_ROOT = Path(__file__).resolve().parents[5]
RESOLVED_SLICE_ROOT = (REPO_ROOT / SLICE_ROOT).resolve()
SOURCE_SCREENING_REF = (
    "outputs/review/vaks-implementation-sandbox/"
    "2026-06-15-p2-19-product-experience-screening-sandbox/"
    "prototype/product-experience-screening-backlog.json"
)

REQUIRED_STEP_IDS = [
    "WF-01",
    "WF-02",
    "WF-03",
    "WF-04",
    "WF-05",
    "WF-06",
    "WF-07",
    "WF-08",
    "WF-09",
    "WF-10",
    "WF-11",
]

STEP_EXPECTATIONS = {
    "WF-01": {"workflow_key": "capability_boundary", "p2_px_ref": "P2-PX-01"},
    "WF-02": {"workflow_key": "onboarding", "p2_px_ref": "P2-PX-09"},
    "WF-03": {"workflow_key": "home_status", "p2_px_ref": "P2-PX-11"},
    "WF-04": {"workflow_key": "layer_badge", "p2_px_ref": "P2-PX-14"},
    "WF-05": {"workflow_key": "quick_capture", "p2_px_ref": "P2-PX-02"},
    "WF-06": {"workflow_key": "candidate_funnel", "p2_px_ref": "P2-PX-03"},
    "WF-07": {"workflow_key": "review_due", "p2_px_ref": "P2-PX-05"},
    "WF-08": {"workflow_key": "context_export", "p2_px_ref": "P2-PX-06"},
    "WF-09": {"workflow_key": "hash_receipt", "p2_px_ref": "P2-PX-13"},
    "WF-10": {"workflow_key": "dirty_guardrail", "p2_px_ref": "P2-PX-15"},
    "WF-11": {"workflow_key": "action_boundary_exit", "p2_px_ref": "P2-PX-06"},
}

REQUIRED_QUESTIONS = {
    "where_do_i_put_this",
    "what_state_is_it_in",
    "orientation_review_or_action",
    "what_blocks_promotion_or_action",
    "what_receipt_proves_no_authority_mutation",
}

FORBIDDEN_SCOPE_FLAGS = {
    "creates_production_ui",
    "creates_real_base_files",
    "starts_runtime_or_service",
    "installs_dependencies",
    "uses_mcp_write_tools",
    "runs_hooks",
    "runs_long_automation",
    "syncs_obsidian",
    "commits",
    "pushes",
    "promotes_mainline",
}

AUTHORITY_FLAGS = {
    "writes_reviewed_truth",
    "approves_review",
    "promotes",
    "infers_action_ready",
    "mutates_truth_confidence",
    "creates_evidence_support",
    "creates_reviewed_relation",
    "treats_status_as_authority",
    "treats_badge_as_promotion",
    "treats_hash_as_support",
    "treats_export_as_action_basis",
    "treats_navigation_as_authority",
    "replaces_validators",
}

REQUIRED_NON_CLAIMS = {
    "workflow_not_product_build",
    "workflow_not_reviewed_knowledge",
    "workflow_not_evidence_support",
    "workflow_not_action_basis",
    "workflow_not_reviewer_approval",
    "workflow_not_mainline_readiness",
}

PROTECTED_PATH_MARKERS = {
    "schema.md",
    "architecture_principles.md",
    "fusion_architecture_v0_2_draft.md",
    "readme.md",
    "wiki/claims/",
    "wiki/patterns/",
    "wiki/decisions/",
    "templates/",
    "tools/",
    "h:/obsidian/",
    "h:\\obsidian\\",
}

STEP_REQUIRED_VALIDATORS = {
    "WF-01": {"boundary-disclosure-check"},
    "WF-02": {"boundary-disclosure-check", "no-consumer-boundary-hiding-check"},
    "WF-03": {"status-display-only-check"},
    "WF-04": {"badge-display-only-check", "badge-not-promotion-check"},
    "WF-05": {"retrieval-receipt-validator", "body-hash-validator", "no-reviewed-write-check"},
    "WF-06": {"review-queue-state-check", "support-boundary-validator", "no-approval-check"},
    "WF-07": {"feedback-validator", "review-due-not-truth-mutation-check"},
    "WF-08": {"support-boundary-validator", "action-readiness-validator", "operation-receipt-validator"},
    "WF-09": {"operation-receipt-validator", "hash-not-support-check"},
    "WF-10": {"dirty-state-guardrail", "dirty-not-knowledge-check"},
    "WF-11": {"action-readiness-validator", "evidence-sufficiency-gate", "non-action-basis-exit-check"},
}


def _normal_path(value: str) -> str:
    return value.replace("\\", "/").lower()


def _is_under_slice(value: str) -> bool:
    candidate = Path(value)
    if not candidate.is_absolute():
        candidate = REPO_ROOT / candidate
    try:
        candidate.resolve().relative_to(RESOLVED_SLICE_ROOT)
        return True
    except ValueError:
        return False


def _issue(code: str, message: str, path: str) -> dict[str, str]:
    return {"code": code, "message": message, "path": path}


def _validate_paths(obj: dict[str, Any], issues: list[dict[str, str]]) -> None:
    scope = obj.get("scope", {})
    if not isinstance(scope, dict):
        return
    paths = []
    paths.extend(scope.get("allowed_write_paths", []) or [])
    paths.extend(scope.get("write_targets", []) or [])
    for index, path in enumerate(paths):
        if not isinstance(path, str):
            issues.append(_issue("WF_REQUIRED_FIELD_MISSING", "path must be a string", f"/scope/paths/{index}"))
            continue
        normal = _normal_path(path)
        if any(marker in normal for marker in PROTECTED_PATH_MARKERS):
            issues.append(_issue("WF_PROTECTED_PATH_TARGET", "path targets a protected location", f"/scope/paths/{index}"))
        if not _is_under_slice(path):
            issues.append(_issue("WF_WRITE_PATH_OUTSIDE_SLICE", "path is outside this slice sandbox", f"/scope/paths/{index}"))


def validate_workflow(obj: dict[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, str]] = []

    if obj.get("record_kind") != RECORD_KIND:
        issues.append(_issue("WF_RECORD_KIND_INVALID", "record_kind is invalid", "/record_kind"))
    if obj.get("slice_id") != SLICE_ID:
        issues.append(_issue("WF_SLICE_ID_INVALID", "slice_id is invalid", "/slice_id"))

    if obj.get("source_screening_ref") != SOURCE_SCREENING_REF:
        issues.append(_issue("WF_SOURCE_SCREENING_REF_INVALID", "source_screening_ref must point to the P2-19 screening prototype", "/source_screening_ref"))
    elif not (REPO_ROOT / SOURCE_SCREENING_REF).exists():
        issues.append(_issue("WF_SOURCE_SCREENING_REF_INVALID", "source_screening_ref target does not exist", "/source_screening_ref"))

    scope = obj.get("scope")
    if not isinstance(scope, dict) or scope.get("sandbox_only") is not True:
        issues.append(_issue("WF_SCOPE_INVALID", "scope must be sandbox_only", "/scope"))
    elif scope.get("product_build") is True:
        issues.append(_issue("WF_SCOPE_INVALID", "workflow prototype cannot be product_build", "/scope/product_build"))
    scope_obj = scope if isinstance(scope, dict) else {}

    _validate_paths(obj, issues)

    for flag in sorted(FORBIDDEN_SCOPE_FLAGS):
        if scope_obj and scope_obj.get(flag) is not False:
            issues.append(_issue("WF_RUNTIME_OR_SYNC_FORBIDDEN", f"{flag} must be false", f"/scope/{flag}"))

    questions = obj.get("workflow_questions", {})
    if not isinstance(questions, dict):
        issues.append(_issue("WF_QUESTIONS_MISSING", "workflow_questions must be an object", "/workflow_questions"))
    else:
        missing_questions = sorted(key for key in REQUIRED_QUESTIONS if not questions.get(key))
        if missing_questions:
            issues.append(_issue("WF_QUESTIONS_MISSING", "missing questions: " + ", ".join(missing_questions), "/workflow_questions"))

    non_claims = obj.get("non_claims", {})
    if not isinstance(non_claims, dict):
        issues.append(_issue("WF_NON_CLAIMS_MISSING", "non_claims must be an object", "/non_claims"))
    else:
        missing = sorted(flag for flag in REQUIRED_NON_CLAIMS if non_claims.get(flag) is not True)
        if missing:
            issues.append(_issue("WF_NON_CLAIMS_MISSING", "missing non-claims: " + ", ".join(missing), "/non_claims"))

    steps = obj.get("steps")
    if not isinstance(steps, list):
        issues.append(_issue("WF_REQUIRED_STEP_MISSING", "steps must be a list", "/steps"))
        steps = []

    step_ids = [step.get("id") for step in steps if isinstance(step, dict)]
    if step_ids != REQUIRED_STEP_IDS:
        issues.append(_issue("WF_STEP_SEQUENCE_INVALID", "steps must match required sequence", "/steps"))

    for index, step in enumerate(steps):
        path = f"/steps/{index}"
        if not isinstance(step, dict):
            issues.append(_issue("WF_STEP_OBJECT_INVALID", "step must be an object", path))
            continue
        sid = step.get("id")
        expected = STEP_EXPECTATIONS.get(sid)
        if expected:
            if step.get("workflow_key") != expected["workflow_key"]:
                issues.append(_issue("WF_STEP_MAPPING_INVALID", "workflow_key does not match required mapping", f"{path}/workflow_key"))
            if step.get("p2_px_ref") != expected["p2_px_ref"]:
                issues.append(_issue("WF_STEP_MAPPING_INVALID", "p2_px_ref does not match P2-19 kept candidate mapping", f"{path}/p2_px_ref"))
        for field in ("surface", "p2_px_ref", "purpose", "boundary_copy", "allowed_user_value"):
            if not step.get(field):
                issues.append(_issue("WF_REQUIRED_FIELD_MISSING", f"{field} is required", f"{path}/{field}"))
        for field in ("input_contract", "output_contract", "required_validators", "blocking_states", "forbidden_implications"):
            value = step.get(field)
            if not isinstance(value, list) or not value:
                issues.append(_issue("WF_REQUIRED_FIELD_MISSING", f"{field} must be a non-empty list", f"{path}/{field}"))
        validators = step.get("required_validators", [])
        required = STEP_REQUIRED_VALIDATORS.get(sid, set())
        if isinstance(validators, list):
            missing_validators = sorted(required.difference(validators))
            if missing_validators:
                issues.append(_issue("WF_REQUIRED_VALIDATORS_MISSING", "missing validators: " + ", ".join(missing_validators), f"{path}/required_validators"))
        if sid in {"WF-08", "WF-11"} and "not action basis" not in str(step.get("boundary_copy", "")).lower():
            issues.append(_issue("WF_ACTION_BOUNDARY_MISSING", "context/action exit must state not action basis", f"{path}/boundary_copy"))
        if sid == "WF-09" and "not evidence support" not in str(step.get("boundary_copy", "")).lower():
            issues.append(_issue("WF_HASH_SUPPORT_CONFUSION", "hash receipt must state not evidence support", f"{path}/boundary_copy"))

        text_segments = [
            str(step.get("purpose", "")),
            str(step.get("boundary_copy", "")),
            str(step.get("allowed_user_value", "")),
        ]
        for field in ("input_contract", "output_contract", "blocking_states"):
            value = step.get(field)
            if isinstance(value, list):
                text_segments.extend(str(item) for item in value)
        forbidden_phrases = {
            "approves review": "WF_COPY_AUTHORITY_CONFUSION",
            "approve review": "WF_COPY_AUTHORITY_CONFUSION",
            "approved review": "WF_COPY_AUTHORITY_CONFUSION",
            "promotes knowledge": "WF_COPY_AUTHORITY_CONFUSION",
            "promotion authority": "WF_COPY_AUTHORITY_CONFUSION",
            "badge promotion": "WF_COPY_AUTHORITY_CONFUSION",
            "evidence support": "WF_COPY_AUTHORITY_CONFUSION",
            "action basis": "WF_COPY_AUTHORITY_CONFUSION",
            "action-ready": "WF_COPY_AUTHORITY_CONFUSION",
            "action ready": "WF_COPY_AUTHORITY_CONFUSION",
            "truth confidence": "WF_COPY_AUTHORITY_CONFUSION",
            "reviewed truth": "WF_COPY_AUTHORITY_CONFUSION",
        }
        allowed_segment_phrases = {
            "not evidence support",
            "not action basis",
            "not promotion",
            "not support",
            "does not mutate truth confidence",
            "cannot approve review",
            "cannot write reviewed truth",
            "cannot replace validators",
            "cannot approve or promote",
            "cannot infer readiness",
            "cannot hide",
        }
        for segment in text_segments:
            lowered = segment.lower()
            scan_text = lowered
            for allowed in allowed_segment_phrases:
                scan_text = scan_text.replace(allowed, "")
            for phrase, code in forbidden_phrases.items():
                if phrase not in scan_text:
                    continue
                issues.append(_issue(code, f"copy implies authority via phrase: {phrase}", path))
                break

        flags = step.get("authority_flags", {})
        if not isinstance(flags, dict):
            issues.append(_issue("WF_AUTHORITY_FLAG_FORBIDDEN", "authority_flags must be an object", f"{path}/authority_flags"))
        else:
            if flags.get("all_authority_changes_disabled") is not True:
                issues.append(_issue("WF_AUTHORITY_FLAG_FORBIDDEN", "all authority changes must be disabled", f"{path}/authority_flags/all_authority_changes_disabled"))
            for flag in sorted(AUTHORITY_FLAGS):
                if flag not in flags:
                    issues.append(_issue("WF_AUTHORITY_FLAG_FORBIDDEN", f"{flag} must be explicitly present and false", f"{path}/authority_flags/{flag}"))
                elif flags.get(flag) is not False:
                    issues.append(_issue("WF_AUTHORITY_FLAG_FORBIDDEN", f"{flag} must be false", f"{path}/authority_flags/{flag}"))

    return {"valid": not issues, "issues": issues}


def validate_path(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    result = validate_workflow(obj)
    result["path"] = str(path)
    return result


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: product_workflow_validator.py <workflow.json>", file=sys.stderr)
        return 2
    result = validate_path(Path(argv[1]))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
