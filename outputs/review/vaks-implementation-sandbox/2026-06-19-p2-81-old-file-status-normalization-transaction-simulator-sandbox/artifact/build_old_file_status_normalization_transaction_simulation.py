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

P2_80 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/artifact/old_file_status_normalization_transaction_package.json"
P2_75 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request.json"
P2_77 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-77-old-file-status-normalization-executor-readiness-gate-sandbox/artifact/old_file_status_normalization_executor_readiness_gate.json"
STRICT_STATUS_PACKAGE = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-16-p2-67-user-decision-strict-status-package-sandbox/artifact/strict_status_package.py"

OUT_JSON = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_simulation.json"
OUT_MD = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_simulation.md"
OUT_HTML = SLICE_ROOT / "artifact/old_file_status_normalization_transaction_simulation.html"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(WORKSPACE)).replace("\\", "/")


def strict_package():
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_81", STRICT_STATUS_PACKAGE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load strict status package")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def split_line_ending(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    return line, ""


def parse_frontmatter_lines(text: str) -> dict:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {"valid": False, "error": "missing_opening_frontmatter_delimiter"}
    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        return {"valid": False, "error": "missing_closing_frontmatter_delimiter"}
    status_indexes: list[int] = []
    for index in range(1, closing_index):
        content, _ending = split_line_ending(lines[index])
        if ":" not in content:
            continue
        key, _value = content.split(":", 1)
        if key.strip() == "status":
            status_indexes.append(index)
    if len(status_indexes) != 1:
        return {"valid": False, "error": "status_field_count_not_one", "status_indexes": status_indexes}
    return {
        "valid": True,
        "lines": lines,
        "closing_index": closing_index,
        "status_index": status_indexes[0],
    }


def replace_status_in_memory(text: str, proposed_status: str) -> dict:
    parsed = parse_frontmatter_lines(text)
    if not parsed["valid"]:
        return {"valid": False, "error": parsed.get("error")}
    lines = list(parsed["lines"])
    status_index = parsed["status_index"]
    original_status_line = lines[status_index]
    content, ending = split_line_ending(original_status_line)
    key, _value = content.split(":", 1)
    simulated_status_line = f"{key}: {proposed_status}{ending}"
    after_lines = list(lines)
    after_lines[status_index] = simulated_status_line
    after_text = "".join(after_lines)
    rollback_lines = list(after_lines)
    rollback_lines[status_index] = original_status_line
    rollback_text = "".join(rollback_lines)
    return {
        "valid": True,
        "status_index": status_index,
        "closing_index": parsed["closing_index"],
        "original_status_line_sha256": sha256_text(original_status_line),
        "simulated_status_line_sha256": sha256_text(simulated_status_line),
        "after_text": after_text,
        "rollback_text": rollback_text,
        "body_before": "".join(lines[parsed["closing_index"] + 1 :]),
        "body_after": "".join(after_lines[parsed["closing_index"] + 1 :]),
        "non_status_frontmatter_before": "".join(line for idx, line in enumerate(lines[1 : parsed["closing_index"]], start=1) if idx != status_index),
        "non_status_frontmatter_after": "".join(line for idx, line in enumerate(after_lines[1 : parsed["closing_index"]], start=1) if idx != status_index),
    }


def parsed_status(text: str) -> str | None:
    parsed = strict_package().parse_strict_frontmatter_status(text)
    return parsed.get("status") if parsed.get("valid") else None


def build_simulation() -> dict:
    package = load_json(P2_80)
    approval = load_json(P2_75)
    readiness = load_json(P2_77)
    results = []

    for op in package["transaction_operations"]:
        target_path = WORKSPACE / op["target_path"]
        before_text = target_path.read_text(encoding="utf-8")
        before_sha = sha256_text(before_text)
        simulation = replace_status_in_memory(before_text, op["proposed_status"])
        if simulation["valid"]:
            after_text = simulation["after_text"]
            rollback_text = simulation["rollback_text"]
            after_status = parsed_status(after_text)
            rollback_status = parsed_status(rollback_text)
            after_sha = sha256_text(after_text)
            rollback_sha = sha256_text(rollback_text)
            body_unchanged = simulation["body_before"] == simulation["body_after"]
            non_status_frontmatter_unchanged = simulation["non_status_frontmatter_before"] == simulation["non_status_frontmatter_after"]
        else:
            after_status = None
            rollback_status = None
            after_sha = None
            rollback_sha = None
            body_unchanged = False
            non_status_frontmatter_unchanged = False
        results.append(
            {
                "operation_index": op["operation_index"],
                "old_slice_id": op["old_slice_id"],
                "target_path": op["target_path"],
                "before_sha256": before_sha,
                "p2_80_required_hash": op["prewrite_required_hash"],
                "before_hash_matches_p2_80": before_sha == op["prewrite_required_hash"],
                "before_status": parsed_status(before_text),
                "p2_80_before_status": op["before_status"],
                "proposed_status": op["proposed_status"],
                "rollback_status": op["rollback_status"],
                "simulation_valid": simulation["valid"],
                "simulation_error": simulation.get("error"),
                "after_status": after_status,
                "after_status_matches_proposed": after_status == op["proposed_status"],
                "rollback_status_after_simulation": rollback_status,
                "rollback_status_matches_rollback_status": rollback_status == op["rollback_status"],
                "after_sha256": after_sha,
                "rollback_sha256": rollback_sha,
                "rollback_sha_matches_original": rollback_sha == before_sha,
                "body_unchanged": body_unchanged,
                "non_status_frontmatter_unchanged": non_status_frontmatter_unchanged,
                "status_only_change": body_unchanged and non_status_frontmatter_unchanged and after_status == op["proposed_status"],
                "write_applied": False,
                "old_slice_write_applied": False,
            }
        )

    summary = {
        "simulated_operation_count": len(results),
        "unique_target_file_count": len({item["target_path"] for item in results}),
        "target_old_slice_count": len({item["old_slice_id"] for item in results}),
        "after_status_match_count": len([item for item in results if item["after_status_matches_proposed"]]),
        "rollback_status_match_count": len([item for item in results if item["rollback_status_matches_rollback_status"]]),
        "body_unchanged_count": len([item for item in results if item["body_unchanged"]]),
        "rollback_sha_match_count": len([item for item in results if item["rollback_sha_matches_original"]]),
        "status_only_change_count": len([item for item in results if item["status_only_change"]]),
        "simulation_failure_count": len([item for item in results if not item["simulation_valid"]]),
        "old_slice_writes_applied": 0,
    }
    p2_77_decision = readiness["current_decision"]
    return {
        "record_kind": "sandbox_old_file_status_normalization_transaction_simulation",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_80_transaction_package_json": rel(P2_80),
            "p2_75_approval_request_json": rel(P2_75),
            "p2_77_readiness_gate_json": rel(P2_77),
            "p2_67_strict_status_package": rel(STRICT_STATUS_PACKAGE),
        },
        "summary": summary,
        "gate": {
            "approval_collected_now": bool(approval["authority_flags"]["user_approval_collected"]),
            "p2_77_readiness": p2_77_decision["readiness"],
            "executor_write_allowed_now": False,
            "simulation_is_not_approval": True,
            "simulation_is_not_write_authority": True,
            "requires_exact_p2_75_approval_before_real_write": True,
            "requires_fresh_hash_check_before_real_write": True,
            "requires_stop_before_write": True,
        },
        "simulation_results": results,
        "authority_flags": {
            "simulation_only": True,
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


def render_markdown(simulation: dict) -> str:
    summary = simulation["summary"]
    gate = simulation["gate"]
    lines = [
        "# Old-File Status Normalization Transaction Simulation",
        "",
        "Sandbox-only in-memory simulation. It does not write old slice files.",
        "",
        "## Summary",
        "",
        f"- simulated_operation_count: `{summary['simulated_operation_count']}`",
        f"- unique_target_file_count: `{summary['unique_target_file_count']}`",
        f"- target_old_slice_count: `{summary['target_old_slice_count']}`",
        f"- after_status_match_count: `{summary['after_status_match_count']}`",
        f"- rollback_status_match_count: `{summary['rollback_status_match_count']}`",
        f"- body_unchanged_count: `{summary['body_unchanged_count']}`",
        f"- rollback_sha_match_count: `{summary['rollback_sha_match_count']}`",
        f"- status_only_change_count: `{summary['status_only_change_count']}`",
        f"- simulation_failure_count: `{summary['simulation_failure_count']}`",
        f"- old_slice_writes_applied: `{summary['old_slice_writes_applied']}`",
        "",
        "## Gate",
        "",
        f"- approval_collected_now: `{str(gate['approval_collected_now']).lower()}`",
        f"- p2_77_readiness: `{gate['p2_77_readiness']}`",
        f"- executor_write_allowed_now: `{str(gate['executor_write_allowed_now']).lower()}`",
        f"- simulation_is_not_approval: `{str(gate['simulation_is_not_approval']).lower()}`",
        f"- simulation_is_not_write_authority: `{str(gate['simulation_is_not_write_authority']).lower()}`",
        f"- requires_exact_p2_75_approval_before_real_write: `{str(gate['requires_exact_p2_75_approval_before_real_write']).lower()}`",
        f"- requires_fresh_hash_check_before_real_write: `{str(gate['requires_fresh_hash_check_before_real_write']).lower()}`",
        f"- requires_stop_before_write: `{str(gate['requires_stop_before_write']).lower()}`",
        "",
        "## Boundary",
        "",
        "- Simulation success is not approval.",
        "- Simulation success is not write authority.",
        "- No old slice write, normalization, rollback, mainline merge, promotion, reviewed knowledge, evidence support, action basis, or goal completion is authorized.",
    ]
    return "\n".join(lines) + "\n"


def render_html(markdown: str) -> str:
    escaped = html.escape(markdown)
    return (
        "<!doctype html>\n"
        "<html><head><meta charset=\"utf-8\"><title>p2-81 Transaction Simulation</title>"
        "<style>body{font-family:Segoe UI,Arial,sans-serif;max-width:1100px;margin:32px auto;line-height:1.5}"
        "pre{white-space:pre-wrap;background:#f6f8fa;padding:16px;border-radius:6px}</style></head>"
        f"<body><pre>{escaped}</pre></body></html>\n"
    )


def main() -> None:
    simulation = build_simulation()
    markdown = render_markdown(simulation)
    OUT_JSON.write_text(json.dumps(simulation, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown, encoding="utf-8")
    OUT_HTML.write_text(render_html(markdown), encoding="utf-8")
    print(json.dumps({"written": [str(OUT_JSON), str(OUT_MD), str(OUT_HTML)]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
