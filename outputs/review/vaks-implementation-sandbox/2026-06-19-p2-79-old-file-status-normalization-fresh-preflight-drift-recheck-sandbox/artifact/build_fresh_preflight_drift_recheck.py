from __future__ import annotations

import html
import importlib.util
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = SLICE_ROOT.parents[3]
SLICE_ID = SLICE_ROOT.name

P2_72 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-72-original-slice-normalization-decision-packet-sandbox/artifact/original_slice_normalization_decision_packet.json"
P2_75 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request.json"
P2_77 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-77-old-file-status-normalization-executor-readiness-gate-sandbox/artifact/old_file_status_normalization_executor_readiness_gate.json"
STRICT_STATUS_PACKAGE = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-16-p2-67-user-decision-strict-status-package-sandbox/artifact/strict_status_package.py"

OUT_JSON = SLICE_ROOT / "artifact/fresh_preflight_drift_recheck.json"
OUT_MD = SLICE_ROOT / "artifact/fresh_preflight_drift_recheck.md"
OUT_HTML = SLICE_ROOT / "artifact/fresh_preflight_drift_recheck.html"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(WORKSPACE)).replace("\\", "/")


def strict_package():
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_79", STRICT_STATUS_PACKAGE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load strict status package")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_status(path: Path) -> dict:
    if not path.exists():
        return {
            "target_exists": False,
            "frontmatter_valid": False,
            "disk_status": None,
            "frontmatter_errors": ["missing_target"],
        }
    parsed = strict_package().parse_strict_frontmatter_status(path.read_text(encoding="utf-8"))
    return {
        "target_exists": True,
        "frontmatter_valid": bool(parsed.get("valid")),
        "disk_status": parsed.get("status"),
        "frontmatter_errors": parsed.get("errors", []),
    }


def build_recheck() -> dict:
    decision = load_json(P2_72)
    approval = load_json(P2_75)
    readiness = load_json(P2_77)
    changes = decision["dry_run_manifest"]["status_changes"]
    checked_changes = []

    for index, change in enumerate(changes, start=1):
        target_path = WORKSPACE / change["target_path"]
        status_info = read_status(target_path)
        disk_status = status_info["disk_status"]
        current_matches_manifest = disk_status == change["current_status"]
        proposed_already_applied = disk_status == change["proposed_status"]
        checked_changes.append(
            {
                "change_index": index,
                "old_slice_id": change["slice_id"],
                "target_path": change["target_path"],
                "field": change["field"],
                "manifest_current_status": change["current_status"],
                "disk_current_status": disk_status,
                "proposed_status": change["proposed_status"],
                "target_exists": status_info["target_exists"],
                "frontmatter_valid": status_info["frontmatter_valid"],
                "frontmatter_errors": status_info["frontmatter_errors"],
                "current_status_matches_manifest": current_matches_manifest,
                "proposed_status_already_applied": proposed_already_applied,
                "change_kind": change["change_kind"],
                "body_edit_planned": False,
                "artifact_edit_planned": False,
                "write_applied": False,
                "requires_exact_approval_before_write": True,
            }
        )

    target_paths = {item["target_path"] for item in checked_changes}
    old_slice_ids = {item["old_slice_id"] for item in checked_changes}
    missing = [item for item in checked_changes if not item["target_exists"]]
    invalid = [item for item in checked_changes if not item["frontmatter_valid"]]
    mismatches = [item for item in checked_changes if item["target_exists"] and item["frontmatter_valid"] and not item["current_status_matches_manifest"]]
    proposed_applied = [item for item in checked_changes if item["proposed_status_already_applied"]]
    clean = not missing and not invalid and not mismatches and not proposed_applied
    p2_77_decision = readiness["current_decision"]

    return {
        "record_kind": "sandbox_fresh_preflight_drift_recheck",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_72_decision_packet_json": rel(P2_72),
            "p2_75_approval_request_json": rel(P2_75),
            "p2_77_readiness_gate_json": rel(P2_77),
            "p2_67_strict_status_package": rel(STRICT_STATUS_PACKAGE),
        },
        "summary": {
            "target_change_count": len(checked_changes),
            "target_file_count": len(target_paths),
            "target_old_slice_count": len(old_slice_ids),
            "missing_target_count": len(missing),
            "frontmatter_invalid_count": len(invalid),
            "current_status_mismatch_count": len(mismatches),
            "proposed_status_already_applied_count": len(proposed_applied),
            "body_edit_planned_count": 0,
            "artifact_edit_planned_count": 0,
            "old_slice_writes_applied": 0,
        },
        "gate": {
            "approval_collected": bool(approval["authority_flags"]["user_approval_collected"]),
            "current_text_matches_exact_approval": bool(p2_77_decision["approval_phrase_matched"]),
            "executor_write_allowed": False,
            "generic_language_is_not_approval": bool(approval["request"]["generic_language_is_not_approval"]),
            "fresh_drift_recheck_passed": clean,
            "fresh_drift_recheck_is_not_write_authority": True,
            "p2_77_readiness": p2_77_decision["readiness"],
            "blocked_reason": "Fresh drift recheck passed, but exact p2-75 approval is still not collected.",
        },
        "checked_changes": checked_changes,
        "blocked_if": {
            "missing_target_count_positive": len(missing) > 0,
            "frontmatter_invalid_count_positive": len(invalid) > 0,
            "current_status_mismatch_count_positive": len(mismatches) > 0,
            "proposed_status_already_applied_count_positive": len(proposed_applied) > 0,
        },
        "authority_flags": {
            "fresh_preflight_drift_recheck_only": True,
            "approval_collected": False,
            "executor_write_allowed": False,
            "old_slice_write_allowed_now": False,
            "old_slice_writes_applied": 0,
            "normalization_applied": False,
            "rollback_applied": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": False,
        },
    }


def render_markdown(recheck: dict) -> str:
    summary = recheck["summary"]
    gate = recheck["gate"]
    lines = [
        "# Fresh Preflight Drift Recheck",
        "",
        "Sandbox-only drift recheck. It does not write old slice files.",
        "",
        "## Summary",
        "",
        f"- target_change_count: `{summary['target_change_count']}`",
        f"- target_file_count: `{summary['target_file_count']}`",
        f"- target_old_slice_count: `{summary['target_old_slice_count']}`",
        f"- missing_target_count: `{summary['missing_target_count']}`",
        f"- frontmatter_invalid_count: `{summary['frontmatter_invalid_count']}`",
        f"- current_status_mismatch_count: `{summary['current_status_mismatch_count']}`",
        f"- proposed_status_already_applied_count: `{summary['proposed_status_already_applied_count']}`",
        f"- old_slice_writes_applied: `{summary['old_slice_writes_applied']}`",
        "",
        "## Gate",
        "",
        f"- approval_collected: `{str(gate['approval_collected']).lower()}`",
        f"- current_text_matches_exact_approval: `{str(gate['current_text_matches_exact_approval']).lower()}`",
        f"- executor_write_allowed: `{str(gate['executor_write_allowed']).lower()}`",
        f"- generic_language_is_not_approval: `{str(gate['generic_language_is_not_approval']).lower()}`",
        f"- fresh_drift_recheck_passed: `{str(gate['fresh_drift_recheck_passed']).lower()}`",
        f"- fresh_drift_recheck_is_not_write_authority: `{str(gate['fresh_drift_recheck_is_not_write_authority']).lower()}`",
        f"- p2_77_readiness: `{gate['p2_77_readiness']}`",
        f"- blocked_reason: {gate['blocked_reason']}",
        "",
        "## Boundary",
        "",
        "- Clean drift recheck is not approval.",
        "- p2-75 request packet is not approval.",
        "- p2-77 readiness gate is blocked.",
        "- No old slice write, normalization, rollback, mainline merge, promotion, reviewed knowledge, evidence support, or action basis is authorized.",
    ]
    return "\n".join(lines) + "\n"


def render_html(markdown: str) -> str:
    escaped = html.escape(markdown)
    return (
        "<!doctype html>\n"
        "<html><head><meta charset=\"utf-8\"><title>p2-79 Fresh Preflight</title>"
        "<style>body{font-family:Segoe UI,Arial,sans-serif;max-width:1100px;margin:32px auto;line-height:1.5}"
        "pre{white-space:pre-wrap;background:#f6f8fa;padding:16px;border-radius:6px}</style></head>"
        f"<body><pre>{escaped}</pre></body></html>\n"
    )


def main() -> None:
    recheck = build_recheck()
    markdown = render_markdown(recheck)
    OUT_JSON.write_text(json.dumps(recheck, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown, encoding="utf-8")
    OUT_HTML.write_text(render_html(markdown), encoding="utf-8")
    print(json.dumps({"written": [str(OUT_JSON), str(OUT_MD), str(OUT_HTML)]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
