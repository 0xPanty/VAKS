from __future__ import annotations

import json
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

SLICE_ID = "2026-06-15-p2-19-product-experience-screening-sandbox"
RECORD_KIND = "vaks_product_experience_screening"
SLICE_ROOT = Path(
    "outputs/review/vaks-implementation-sandbox/"
    "2026-06-15-p2-19-product-experience-screening-sandbox"
)

REQUIRED_CANDIDATE_IDS = {
    f"P2-PX-{number:02d}" for number in range(1, 16)
}

ALLOWED_DECISIONS = {"keep", "park", "reject"}

FORBIDDEN_SCOPE_FLAGS = {
    "creates_real_ui",
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

FORBIDDEN_IMPORT_FLAGS = {
    "admin_dashboard_before_validators",
    "star_graph_as_confidence",
    "heatmap_as_confidence",
    "ai_summary_as_evidence_support",
    "sqlite_as_reviewed_truth_source",
    "subscription_as_knowledge_authority",
    "consumer_onboarding_hides_boundaries",
}

AUTHORITY_FLAGS = {
    "writes_reviewed_truth",
    "approves_review",
    "promotes",
    "infers_action_ready",
    "mutates_truth_confidence",
    "creates_evidence_support",
    "creates_reviewed_relation",
    "treats_activity_as_confidence",
    "treats_hash_as_evidence_support",
    "treats_badge_as_promotion",
    "treats_navigation_as_authority",
    "runs_mobile_full_review",
    "exposes_reviewed_write_tool",
}

ALLOWED_REQUIRED_VALIDATORS = {
    "action-readiness-validator",
    "activity-not-confidence-check",
    "badge-display-only-check",
    "badge-not-promotion-check",
    "base-cockpit-display-only-check",
    "body-hash-validator",
    "boundary-disclosure-check",
    "candidate-feedback-receipt-check",
    "dirty-not-knowledge-check",
    "dirty-state-guardrail",
    "feedback-validator",
    "hash-not-support-check",
    "mcp-read-candidate-feedback-only-check",
    "misa-readonly-check",
    "mobile-no-full-review-check",
    "navigation-not-authority-check",
    "no-approval-check",
    "no-consumer-boundary-hiding-check",
    "no-reviewed-write-check",
    "no-reviewed-write-tool-check",
    "non-authority-copy-check",
    "operation-receipt-validator",
    "product-boundary-copy-check",
    "rank-not-trust-check",
    "raw-candidate-quarantine-check",
    "relation-boundary-check",
    "retrieval-receipt-validator",
    "review-due-not-truth-mutation-check",
    "review-queue-state-check",
    "status-display-only-check",
    "support-boundary-validator",
}

CANDIDATE_REQUIRED_VALIDATORS = {
    "P2-PX-01": {"product-boundary-copy-check", "non-authority-copy-check"},
    "P2-PX-02": {"retrieval-receipt-validator", "body-hash-validator", "no-reviewed-write-check"},
    "P2-PX-03": {"review-queue-state-check", "support-boundary-validator", "no-approval-check"},
    "P2-PX-04": {"activity-not-confidence-check", "rank-not-trust-check"},
    "P2-PX-05": {"feedback-validator", "review-due-not-truth-mutation-check"},
    "P2-PX-06": {"support-boundary-validator", "action-readiness-validator", "operation-receipt-validator"},
    "P2-PX-07": {"raw-candidate-quarantine-check", "mobile-no-full-review-check"},
    "P2-PX-08": {"mcp-read-candidate-feedback-only-check", "no-reviewed-write-tool-check"},
    "P2-PX-09": {"boundary-disclosure-check", "no-consumer-boundary-hiding-check"},
    "P2-PX-10": {"misa-readonly-check", "candidate-feedback-receipt-check", "no-reviewed-write-check"},
    "P2-PX-11": {"status-display-only-check", "base-cockpit-display-only-check"},
    "P2-PX-12": {"navigation-not-authority-check", "relation-boundary-check"},
    "P2-PX-13": {"operation-receipt-validator", "hash-not-support-check"},
    "P2-PX-14": {"badge-display-only-check", "badge-not-promotion-check"},
    "P2-PX-15": {"dirty-state-guardrail", "dirty-not-knowledge-check"},
}

REQUIRED_NON_CLAIMS = {
    "screening_not_product_build",
    "screening_not_reviewed_knowledge",
    "screening_not_evidence_support",
    "screening_not_action_basis",
    "screening_not_reviewer_approval",
    "screening_not_mainline_readiness",
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


def _normal_path(value: str) -> str:
    return value.replace("\\", "/").lower()


def _is_under_slice(value: str) -> bool:
    normalized = _normal_path(value).rstrip("/") + "/"
    root = _normal_path(str(SLICE_ROOT)).rstrip("/") + "/"
    return normalized.startswith(root)


def _issue(code: str, message: str, path: str) -> dict[str, str]:
    return {"code": code, "message": message, "path": path}


def _get_path(obj: Any, path: str) -> Any:
    current = obj
    for part in path.strip("/").split("/"):
        if part == "":
            continue
        if isinstance(current, list):
            current = current[int(part)]
        else:
            current = current[part]
    return current


def _validate_paths(obj: dict[str, Any], issues: list[dict[str, str]]) -> None:
    scope = obj.get("scope", {})
    paths = []
    paths.extend(scope.get("allowed_write_paths", []) or [])
    paths.extend(scope.get("write_targets", []) or [])
    for index, path in enumerate(paths):
        if not isinstance(path, str):
            issues.append(_issue("PX_REQUIRED_FIELD_MISSING", "path must be a string", f"/scope/paths/{index}"))
            continue
        normal = _normal_path(path)
        if any(marker in normal for marker in PROTECTED_PATH_MARKERS):
            issues.append(_issue("PX_PROTECTED_PATH_TARGET", "path targets a protected location", f"/scope/paths/{index}"))
        if not _is_under_slice(path):
            issues.append(_issue("PX_WRITE_PATH_OUTSIDE_SLICE", "path is outside this slice sandbox", f"/scope/paths/{index}"))


def _candidate_by_id(candidates: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    indexed: dict[str, dict[str, Any]] = {}
    for candidate in candidates:
        cid = candidate.get("id")
        if isinstance(cid, str):
            indexed[cid] = candidate
    return indexed


def validate_screening(obj: dict[str, Any]) -> dict[str, Any]:
    issues: list[dict[str, str]] = []

    if obj.get("record_kind") != RECORD_KIND:
        issues.append(_issue("PX_RECORD_KIND_INVALID", "record_kind is not the product screening kind", "/record_kind"))
    if obj.get("slice_id") != SLICE_ID:
        issues.append(_issue("PX_SLICE_ID_INVALID", "slice_id does not match this slice", "/slice_id"))

    scope = obj.get("scope")
    if not isinstance(scope, dict) or scope.get("sandbox_only") is not True:
        issues.append(_issue("PX_SCOPE_INVALID", "scope must be sandbox_only", "/scope"))
    elif scope.get("product_build") is True:
        issues.append(_issue("PX_SCOPE_INVALID", "screening artifact cannot be a product build", "/scope/product_build"))

    _validate_paths(obj, issues)

    for flag in sorted(FORBIDDEN_SCOPE_FLAGS):
        if scope and scope.get(flag) is not False:
            issues.append(_issue("PX_RUNTIME_OR_SYNC_FORBIDDEN", f"{flag} must be false", f"/scope/{flag}"))

    import_controls = obj.get("forbidden_import_controls", {})
    if not isinstance(import_controls, dict):
        issues.append(_issue("PX_FORBIDDEN_IMPORT", "forbidden_import_controls must be an object", "/forbidden_import_controls"))
    else:
        for flag in sorted(FORBIDDEN_IMPORT_FLAGS):
            if import_controls.get(flag) is not False:
                issues.append(_issue("PX_FORBIDDEN_IMPORT", f"{flag} must be false", f"/forbidden_import_controls/{flag}"))

    non_claims = obj.get("non_claims", {})
    if not isinstance(non_claims, dict):
        issues.append(_issue("PX_NON_CLAIMS_MISSING", "non_claims must be an object", "/non_claims"))
    else:
        missing = sorted(flag for flag in REQUIRED_NON_CLAIMS if non_claims.get(flag) is not True)
        if missing:
            issues.append(_issue("PX_NON_CLAIMS_MISSING", "missing non-claims: " + ", ".join(missing), "/non_claims"))

    candidates = obj.get("candidates")
    if not isinstance(candidates, list):
        issues.append(_issue("PX_REQUIRED_FIELD_MISSING", "candidates must be a list", "/candidates"))
        candidates = []

    seen_ids: dict[str, int] = {}
    ranks: dict[int, str] = {}
    for index, candidate in enumerate(candidates):
        path = f"/candidates/{index}"
        cid = candidate.get("id")
        if not isinstance(cid, str):
            issues.append(_issue("PX_REQUIRED_FIELD_MISSING", "candidate id is required", f"{path}/id"))
            continue
        if cid in seen_ids:
            issues.append(_issue("PX_DUPLICATE_CANDIDATE", f"duplicate candidate id {cid}", f"{path}/id"))
        seen_ids[cid] = index
        if cid not in REQUIRED_CANDIDATE_IDS:
            issues.append(_issue("PX_UNKNOWN_CANDIDATE", f"unknown candidate id {cid}", f"{path}/id"))

        rank = candidate.get("rank")
        if not isinstance(rank, int):
            issues.append(_issue("PX_REQUIRED_FIELD_MISSING", "rank is required", f"{path}/rank"))
        elif rank in ranks:
            issues.append(_issue("PX_DUPLICATE_RANK", f"rank {rank} is shared by {ranks[rank]} and {cid}", f"{path}/rank"))
        else:
            ranks[rank] = cid

        decision = candidate.get("decision")
        if decision not in ALLOWED_DECISIONS:
            issues.append(_issue("PX_INVALID_DECISION", "decision must be keep, park, or reject", f"{path}/decision"))

        for field in ("candidate", "target_layer", "rationale"):
            if not candidate.get(field):
                issues.append(_issue("PX_REQUIRED_FIELD_MISSING", f"{field} is required", f"{path}/{field}"))

        if not candidate.get("source_inspiration"):
            issues.append(_issue("PX_SOURCE_INSPIRATION_MISSING", "source_inspiration is required", f"{path}/source_inspiration"))
        validators = candidate.get("required_validators")
        if not validators:
            issues.append(_issue("PX_REQUIRED_VALIDATORS_MISSING", "required_validators is required", f"{path}/required_validators"))
        elif not isinstance(validators, list) or not all(isinstance(item, str) for item in validators):
            issues.append(_issue("PX_REQUIRED_VALIDATORS_MISSING", "required_validators must be a string list", f"{path}/required_validators"))
        else:
            unknown_validators = sorted(set(validators).difference(ALLOWED_REQUIRED_VALIDATORS))
            if unknown_validators:
                issues.append(_issue("PX_VALIDATOR_NAME_INVALID", "unknown validators: " + ", ".join(unknown_validators), f"{path}/required_validators"))
            required_for_candidate = CANDIDATE_REQUIRED_VALIDATORS.get(cid, set())
            missing_validators = sorted(required_for_candidate.difference(validators))
            if missing_validators:
                issues.append(_issue("PX_REQUIRED_VALIDATORS_MISSING", "missing required validators: " + ", ".join(missing_validators), f"{path}/required_validators"))
        if not candidate.get("boundary_warning"):
            issues.append(_issue("PX_BOUNDARY_WARNING_MISSING", "boundary_warning is required", f"{path}/boundary_warning"))
        if not candidate.get("minimal_wireflow") or len(candidate.get("minimal_wireflow", [])) < 2:
            issues.append(_issue("PX_WIREFLOW_MISSING", "minimal_wireflow needs at least two steps", f"{path}/minimal_wireflow"))

        if decision == "keep" and not candidate.get("p2_20_role"):
            issues.append(_issue("PX_KEEP_HANDOFF_ROLE_MISSING", "kept candidates need a P2-20 role", f"{path}/p2_20_role"))
        if decision in {"park", "reject"} and "because" not in str(candidate.get("rationale", "")).lower():
            issues.append(_issue("PX_DECISION_RATIONALE_MISSING", "park/reject decisions need an explicit because rationale", f"{path}/rationale"))

        flags = candidate.get("authority_flags", {})
        if not isinstance(flags, dict):
            issues.append(_issue("PX_AUTHORITY_FLAG_FORBIDDEN", "authority_flags must be an object", f"{path}/authority_flags"))
        else:
            if flags.get("all_authority_changes_disabled") is not True:
                issues.append(_issue("PX_AUTHORITY_FLAG_FORBIDDEN", "all authority changes must be disabled", f"{path}/authority_flags/all_authority_changes_disabled"))
            for flag in sorted(AUTHORITY_FLAGS):
                if flag not in flags:
                    issues.append(_issue("PX_AUTHORITY_FLAG_FORBIDDEN", f"{flag} must be explicitly present and false", f"{path}/authority_flags/{flag}"))
                elif flags.get(flag) is not False:
                    issues.append(_issue("PX_AUTHORITY_FLAG_FORBIDDEN", f"{flag} must be false", f"{path}/authority_flags/{flag}"))

        if cid == "P2-PX-09" and candidate.get("exposes_boundaries") is not True:
            issues.append(_issue("PX_ONBOARDING_BOUNDARY_HIDDEN", "product onboarding must expose boundaries", path))

    missing_ids = sorted(REQUIRED_CANDIDATE_IDS.difference(seen_ids))
    if missing_ids:
        issues.append(_issue("PX_REQUIRED_CANDIDATE_MISSING", "missing candidates: " + ", ".join(missing_ids), "/candidates"))

    if set(ranks) != set(range(1, len(candidates) + 1)):
        issues.append(_issue("PX_RANK_SEQUENCE_INVALID", "ranks must be contiguous from 1 to candidate count", "/candidates"))

    p2_20 = obj.get("p2_20_handoff", {})
    if not isinstance(p2_20, dict) or not p2_20.get("selected_candidate_ids"):
        issues.append(_issue("PX_P2_20_HANDOFF_MISSING", "p2_20_handoff.selected_candidate_ids is required", "/p2_20_handoff"))
    else:
        by_id = _candidate_by_id(candidates)
        selected = p2_20.get("selected_candidate_ids", [])
        parked = p2_20.get("parked_candidate_ids", [])
        rejected = p2_20.get("rejected_candidate_ids", [])
        handoff_lists = {
            "selected_candidate_ids": selected,
            "parked_candidate_ids": parked,
            "rejected_candidate_ids": rejected,
        }
        for name, values in handoff_lists.items():
            if not isinstance(values, list) or not all(isinstance(item, str) for item in values):
                issues.append(_issue("PX_P2_20_HANDOFF_MISSING", f"{name} must be a string list", f"/p2_20_handoff/{name}"))
        all_handoff_ids = selected + parked + rejected if all(isinstance(values, list) for values in handoff_lists.values()) else []
        if len(all_handoff_ids) != len(set(all_handoff_ids)):
            issues.append(_issue("PX_P2_20_HANDOFF_INCOMPLETE", "handoff ids must not repeat across selected, parked, and rejected lists", "/p2_20_handoff"))
        for cid in selected:
            if cid not in by_id:
                issues.append(_issue("PX_P2_20_HANDOFF_MISSING", f"selected id {cid} is not present", "/p2_20_handoff/selected_candidate_ids"))
            elif by_id[cid].get("decision") != "keep":
                issues.append(_issue("PX_P2_20_SELECTED_NOT_KEEP", f"selected id {cid} is not keep", "/p2_20_handoff/selected_candidate_ids"))
            elif not by_id[cid].get("p2_20_role"):
                issues.append(_issue("PX_KEEP_HANDOFF_ROLE_MISSING", f"selected id {cid} lacks p2_20_role", "/p2_20_handoff/selected_candidate_ids"))
        keep_ids = {candidate.get("id") for candidate in candidates if candidate.get("decision") == "keep"}
        park_ids = {candidate.get("id") for candidate in candidates if candidate.get("decision") == "park"}
        reject_ids = {candidate.get("id") for candidate in candidates if candidate.get("decision") == "reject"}
        if set(selected) != keep_ids or set(parked) != park_ids or set(rejected) != reject_ids:
            issues.append(_issue("PX_P2_20_HANDOFF_INCOMPLETE", "handoff lists must exactly match keep, park, and reject decisions", "/p2_20_handoff"))

    return {"valid": not issues, "issues": issues}


def validate_path(path: Path) -> dict[str, Any]:
    obj = json.loads(path.read_text(encoding="utf-8"))
    result = validate_screening(obj)
    result["path"] = str(path)
    return result


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        print("usage: product_experience_screening_validator.py <screening.json>", file=sys.stderr)
        return 2
    result = validate_path(Path(argv[1]))
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["valid"] else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
