from __future__ import annotations

import hashlib
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
P2_79 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-79-old-file-status-normalization-fresh-preflight-drift-recheck-sandbox/artifact/fresh_preflight_drift_recheck.json"
STRICT_STATUS_PACKAGE = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-16-p2-67-user-decision-strict-status-package-sandbox/artifact/strict_status_package.py"

OUT_JSON = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_package.json"
OUT_MD = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_package.md"
OUT_HTML = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_package.html"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(WORKSPACE)).replace("\\", "/")


def strict_package():
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_80", STRICT_STATUS_PACKAGE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load strict status package")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def read_target(path: Path) -> dict:
    if not path.exists():
        return {
            "target_exists": False,
            "frontmatter_valid": False,
            "disk_status": None,
            "target_sha256": None,
            "frontmatter_errors": ["missing_target"],
        }
    data = path.read_bytes()
    parsed = strict_package().parse_strict_frontmatter_status(data.decode("utf-8"))
    return {
        "target_exists": True,
        "frontmatter_valid": bool(parsed.get("valid")),
        "disk_status": parsed.get("status"),
        "target_sha256": hashlib.sha256(data).hexdigest(),
        "frontmatter_errors": parsed.get("errors", []),
    }


def build_package() -> dict:
    p2_72 = load_json(P2_72)
    p2_75 = load_json(P2_75)
    p2_77 = load_json(P2_77)
    p2_79 = load_json(P2_79)
    changes = p2_72["dry_run_manifest"]["status_changes"]
    operations = []

    for index, change in enumerate(changes, start=1):
        target_path = WORKSPACE / change["target_path"]
        target = read_target(target_path)
        before_status = target["disk_status"]
        operations.append(
            {
                "operation_index": index,
                "operation_kind": "status_only_frontmatter_normalization",
                "old_slice_id": change["slice_id"],
                "target_path": change["target_path"],
                "target_exists": target["target_exists"],
                "frontmatter_valid": target["frontmatter_valid"],
                "frontmatter_errors": target["frontmatter_errors"],
                "current_target_file_sha256": target["target_sha256"],
                "field": change["field"],
                "manifest_current_status": change["current_status"],
                "before_status": before_status,
                "proposed_status": change["proposed_status"],
                "rollback_status": change["current_status"],
                "current_status_matches_manifest": before_status == change["current_status"],
                "proposed_status_already_applied": before_status == change["proposed_status"],
                "rollback_status_equals_manifest_current_status": change["current_status"] == change["current_status"],
                "body_edit_planned": False,
                "artifact_edit_planned": False,
                "write_applied": False,
                "rollback_applied": False,
                "requires_exact_p2_75_approval": True,
                "requires_fresh_hash_check_before_write": True,
                "prewrite_required_hash": target["target_sha256"],
                "prewrite_hash_mismatch_blocks_execution": True,
            }
        )

    unique_targets = {op["target_path"] for op in operations}
    old_slices = {op["old_slice_id"] for op in operations}
    hash_records = [op for op in operations if isinstance(op["current_target_file_sha256"], str) and len(op["current_target_file_sha256"]) == 64]
    mismatches = [op for op in operations if not op["current_status_matches_manifest"]]
    proposed_applied = [op for op in operations if op["proposed_status_already_applied"]]
    missing = [op for op in operations if not op["target_exists"]]
    invalid = [op for op in operations if not op["frontmatter_valid"]]
    p2_77_decision = p2_77["current_decision"]

    return {
        "record_kind": "sandbox_old_file_status_normalization_transaction_package",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_72_decision_packet_json": rel(P2_72),
            "p2_75_approval_request_json": rel(P2_75),
            "p2_77_readiness_gate_json": rel(P2_77),
            "p2_79_fresh_drift_recheck_json": rel(P2_79),
            "p2_67_strict_status_package": rel(STRICT_STATUS_PACKAGE),
        },
        "summary": {
            "transaction_operation_count": len(operations),
            "unique_target_file_count": len(unique_targets),
            "target_old_slice_count": len(old_slices),
            "current_status_mismatch_count": len(mismatches),
            "proposed_status_already_applied_count": len(proposed_applied),
            "missing_target_count": len(missing),
            "frontmatter_invalid_count": len(invalid),
            "hash_record_count": len(hash_records),
            "write_applied_count": len([op for op in operations if op["write_applied"]]),
            "old_slice_writes_applied": 0,
        },
        "gate": {
            "requires_exact_p2_75_approval": True,
            "approval_collected_now": bool(p2_75["authority_flags"]["user_approval_collected"]),
            "p2_77_readiness": p2_77_decision["readiness"],
            "p2_79_fresh_drift_recheck_passed": bool(p2_79["gate"]["fresh_drift_recheck_passed"]),
            "requires_fresh_hash_check_before_write": True,
            "requires_boundary_audit_before_write": True,
            "requires_stop_before_write": True,
            "executor_write_allowed_now": False,
            "transaction_package_is_not_approval": True,
        },
        "transaction_operations": operations,
        "future_executor_preconditions": [
            "future_user_message_must_exactly_match_p2_75_phrase",
            "fresh_prewrite_preflight_must_pass",
            "each_target_sha256_must_match_prewrite_required_hash",
            "boundary_audit_must_pass",
            "stop_before_write_must_be_observed",
        ],
        "authority_flags": {
            "transaction_package_only": True,
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


def render_markdown(package: dict) -> str:
    summary = package["summary"]
    gate = package["gate"]
    lines = [
        "# Old-File Status Normalization Transaction Package",
        "",
        "Sandbox-only no-write transaction package. It does not execute old-file status normalization.",
        "",
        "## Summary",
        "",
        f"- transaction_operation_count: `{summary['transaction_operation_count']}`",
        f"- unique_target_file_count: `{summary['unique_target_file_count']}`",
        f"- target_old_slice_count: `{summary['target_old_slice_count']}`",
        f"- current_status_mismatch_count: `{summary['current_status_mismatch_count']}`",
        f"- proposed_status_already_applied_count: `{summary['proposed_status_already_applied_count']}`",
        f"- missing_target_count: `{summary['missing_target_count']}`",
        f"- frontmatter_invalid_count: `{summary['frontmatter_invalid_count']}`",
        f"- hash_record_count: `{summary['hash_record_count']}`",
        f"- write_applied_count: `{summary['write_applied_count']}`",
        f"- old_slice_writes_applied: `{summary['old_slice_writes_applied']}`",
        "",
        "## Gate",
        "",
        f"- requires_exact_p2_75_approval: `{str(gate['requires_exact_p2_75_approval']).lower()}`",
        f"- approval_collected_now: `{str(gate['approval_collected_now']).lower()}`",
        f"- p2_77_readiness: `{gate['p2_77_readiness']}`",
        f"- p2_79_fresh_drift_recheck_passed: `{str(gate['p2_79_fresh_drift_recheck_passed']).lower()}`",
        f"- requires_fresh_hash_check_before_write: `{str(gate['requires_fresh_hash_check_before_write']).lower()}`",
        f"- requires_boundary_audit_before_write: `{str(gate['requires_boundary_audit_before_write']).lower()}`",
        f"- requires_stop_before_write: `{str(gate['requires_stop_before_write']).lower()}`",
        f"- executor_write_allowed_now: `{str(gate['executor_write_allowed_now']).lower()}`",
        f"- transaction_package_is_not_approval: `{str(gate['transaction_package_is_not_approval']).lower()}`",
        "",
        "## Future Executor Preconditions",
        "",
    ]
    for item in package["future_executor_preconditions"]:
        lines.append(f"- `{item}`")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- Transaction package is not approval.",
            "- Hash match is process integrity, not evidence support.",
            "- No old slice write, normalization, rollback, mainline merge, promotion, reviewed knowledge, evidence support, action basis, or goal completion is authorized.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_html(markdown: str) -> str:
    escaped = html.escape(markdown)
    return (
        "<!doctype html>\n"
        "<html><head><meta charset=\"utf-8\"><title>p2-80 Transaction Package</title>"
        "<style>body{font-family:Segoe UI,Arial,sans-serif;max-width:1100px;margin:32px auto;line-height:1.5}"
        "pre{white-space:pre-wrap;background:#f6f8fa;padding:16px;border-radius:6px}</style></head>"
        f"<body><pre>{escaped}</pre></body></html>\n"
    )


def main() -> None:
    package = build_package()
    markdown = render_markdown(package)
    OUT_JSON.write_text(json.dumps(package, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown, encoding="utf-8")
    OUT_HTML.write_text(render_html(markdown), encoding="utf-8")
    print(json.dumps({"written": [str(OUT_JSON), str(OUT_MD), str(OUT_HTML)]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
