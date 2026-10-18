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
STRICT_STATUS_PACKAGE = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-16-p2-67-user-decision-strict-status-package-sandbox/artifact/strict_status_package.py"
CONTRACT = SLICE_ROOT / "artifact/old_file_status_normalization_executor_preflight_contract.json"

OUT_JSON = SLICE_ROOT / "artifact/old_file_status_normalization_executor_preflight.json"
OUT_MD = SLICE_ROOT / "artifact/old_file_status_normalization_executor_preflight.md"
OUT_HTML = SLICE_ROOT / "artifact/old_file_status_normalization_executor_preflight.html"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(WORKSPACE)).replace("\\", "/")


def strict_package():
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_76_builder", STRICT_STATUS_PACKAGE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load strict status package")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def parse_status(path: Path) -> dict:
    if not path.is_file():
        return {"exists": False, "valid_frontmatter": False, "status": None, "errors": ["missing_target_file"]}
    parsed = strict_package().parse_strict_frontmatter_status(path.read_text(encoding="utf-8"))
    return {
        "exists": True,
        "valid_frontmatter": bool(parsed.get("valid")),
        "status": parsed.get("status"),
        "errors": parsed.get("errors", []),
    }


def build_preflight() -> dict:
    decision = load_json(P2_72)
    approval_request = load_json(P2_75)
    contract = load_json(CONTRACT)
    changes = decision["dry_run_manifest"]["status_changes"]
    preflight_changes = []
    for index, change in enumerate(changes, start=1):
        target = WORKSPACE / change["target_path"]
        parsed = parse_status(target)
        current_matches = parsed["exists"] and parsed["status"] == change["current_status"]
        preflight_changes.append(
            {
                "change_index": index,
                "old_slice_id": change["slice_id"],
                "target_path": change["target_path"],
                "field": change["field"],
                "manifest_current_status": change["current_status"],
                "disk_current_status": parsed["status"],
                "proposed_status": change["proposed_status"],
                "rollback_status": change["current_status"],
                "target_exists": parsed["exists"],
                "frontmatter_valid": parsed["valid_frontmatter"],
                "current_status_matches_manifest": current_matches,
                "change_kind": change["change_kind"],
                "body_edit_planned": False,
                "artifact_edit_planned": False,
                "write_applied": False,
                "rollback_applied": False,
                "requires_exact_approval_before_write": True,
            }
        )
    missing = [item for item in preflight_changes if not item["target_exists"]]
    mismatch = [item for item in preflight_changes if not item["current_status_matches_manifest"]]
    rollback = [
        {
            "change_index": item["change_index"],
            "target_path": item["target_path"],
            "restore_status": item["rollback_status"],
            "rollback_applied": False,
        }
        for item in preflight_changes
    ]
    old_slice_ids = sorted({item["old_slice_id"] for item in preflight_changes})
    return {
        "record_kind": "sandbox_old_file_status_normalization_executor_preflight",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_72_decision_packet_json": rel(P2_72),
            "p2_75_approval_request_json": rel(P2_75),
            "p2_67_strict_status_package": rel(STRICT_STATUS_PACKAGE),
        },
        "summary": {
            "target_change_count": len(preflight_changes),
            "target_file_count": len({item["target_path"] for item in preflight_changes}),
            "target_old_slice_count": len(old_slice_ids),
            "missing_target_count": len(missing),
            "current_status_mismatch_count": len(mismatch),
            "rollback_entry_count": len(rollback),
            "old_slice_writes_applied": 0,
            "all_targets_match_manifest_current_status": len(missing) == 0 and len(mismatch) == 0,
            "all_rollback_entries_restore_manifest_current_status": len(rollback) == len(preflight_changes),
        },
        "approval_gate": {
            "approval_present": False,
            "executor_write_allowed": False,
            "required_exact_phrase": approval_request["request"]["exact_approval_phrase"],
            "p2_75_packet_is_not_approval": True,
            "generic_language_is_not_approval": True,
            "blocked_reason": "No future user message with the exact p2-75 approval phrase is present in this slice.",
        },
        "authority_flags": contract["authority_flags"],
        "allowed_future_edit": contract["allowed_future_edit"],
        "target_old_slice_ids": old_slice_ids,
        "preflight_changes": preflight_changes,
        "rollback_manifest": rollback,
    }


def render_markdown(preflight: dict) -> str:
    summary = preflight["summary"]
    gate = preflight["approval_gate"]
    lines = [
        "# Old-File Status Normalization Executor Preflight",
        "",
        "Sandbox-only executor preflight. It does not apply old-file writes.",
        "",
        "## Summary",
        "",
        f"- target changes: `{summary['target_change_count']}`",
        f"- target files: `{summary['target_file_count']}`",
        f"- old slices covered: `{summary['target_old_slice_count']}`",
        f"- missing targets: `{summary['missing_target_count']}`",
        f"- current status mismatches: `{summary['current_status_mismatch_count']}`",
        f"- rollback entries: `{summary['rollback_entry_count']}`",
        f"- old slice writes applied: `{summary['old_slice_writes_applied']}`",
        "",
        "## Approval Gate",
        "",
        f"- approval present: `{str(gate['approval_present']).lower()}`",
        f"- executor write allowed: `{str(gate['executor_write_allowed']).lower()}`",
        f"- blocked reason: {gate['blocked_reason']}",
        "",
        "## Change Plan",
        "",
        "| # | Target | Current | Proposed | Rollback | Match |",
        "|---:|---|---|---|---|---:|",
    ]
    for item in preflight["preflight_changes"]:
        lines.append(
            "| {idx} | `{target}` | `{current}` | `{proposed}` | `{rollback}` | {match} |".format(
                idx=item["change_index"],
                target=item["target_path"],
                current=item["disk_current_status"],
                proposed=item["proposed_status"],
                rollback=item["rollback_status"],
                match=str(item["current_status_matches_manifest"]),
            )
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "- p2-75 packet is not approval.",
            "- No old slice writes are applied.",
            "- No body, artifact, mainline, template, tool, wiki truth-layer, Obsidian, commit, or push action is allowed.",
        ]
    )
    return "\n".join(lines) + "\n"


def render_html(markdown: str) -> str:
    escaped = html.escape(markdown)
    return (
        "<!doctype html>\n"
        "<html><head><meta charset=\"utf-8\"><title>p2-76 Executor Preflight</title>"
        "<style>body{font-family:Segoe UI,Arial,sans-serif;max-width:1200px;margin:32px auto;line-height:1.5}"
        "pre{white-space:pre-wrap;background:#f6f8fa;padding:16px;border-radius:6px}</style></head>"
        f"<body><pre>{escaped}</pre></body></html>\n"
    )


def main() -> None:
    preflight = build_preflight()
    markdown = render_markdown(preflight)
    OUT_JSON.write_text(json.dumps(preflight, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown, encoding="utf-8")
    OUT_HTML.write_text(render_html(markdown), encoding="utf-8")
    print(json.dumps({"written": [str(OUT_JSON), str(OUT_MD), str(OUT_HTML)]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
