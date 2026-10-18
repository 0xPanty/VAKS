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
COPY_ROOT = SLICE_ROOT / "fixtures/target-copies"

P2_80 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/artifact/old_file_status_normalization_transaction_package.json"
P2_75 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request.json"
P2_77 = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-77-old-file-status-normalization-executor-readiness-gate-sandbox/artifact/old_file_status_normalization_executor_readiness_gate.json"
STRICT_STATUS_PACKAGE = WORKSPACE / "outputs/review/vaks-implementation-sandbox/2026-06-16-p2-67-user-decision-strict-status-package-sandbox/artifact/strict_status_package.py"

OUT_JSON = SLICE_ROOT / "artifact/sandbox_copy_executor_rehearsal.json"
OUT_MD = SLICE_ROOT / "artifact/sandbox_copy_executor_rehearsal.md"
OUT_HTML = SLICE_ROOT / "artifact/sandbox_copy_executor_rehearsal.html"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def rel(path: Path) -> str:
    return str(path.relative_to(WORKSPACE)).replace("\\", "/")


def rel_slice(path: Path) -> str:
    return str(path.relative_to(SLICE_ROOT)).replace("\\", "/")


def strict_package():
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_p2_82", STRICT_STATUS_PACKAGE)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load strict status package")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def parsed_status(text: str) -> str | None:
    parsed = strict_package().parse_strict_frontmatter_status(text)
    return parsed.get("status") if parsed.get("valid") else None


def decode_utf8(data: bytes) -> str:
    return data.decode("utf-8")


def encode_utf8(text: str) -> bytes:
    return text.encode("utf-8")


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


def replace_status(text: str, proposed_status: str) -> dict:
    parsed = parse_frontmatter_lines(text)
    if not parsed["valid"]:
        return {"valid": False, "error": parsed.get("error")}
    lines = list(parsed["lines"])
    status_index = parsed["status_index"]
    original_status_line = lines[status_index]
    content, ending = split_line_ending(original_status_line)
    key, _value = content.split(":", 1)
    after_lines = list(lines)
    after_lines[status_index] = f"{key}: {proposed_status}{ending}"
    after_text = "".join(after_lines)
    rollback_lines = list(after_lines)
    rollback_lines[status_index] = original_status_line
    rollback_text = "".join(rollback_lines)
    return {
        "valid": True,
        "after_text": after_text,
        "rollback_text": rollback_text,
        "body_before": "".join(lines[parsed["closing_index"] + 1 :]),
        "body_after": "".join(after_lines[parsed["closing_index"] + 1 :]),
        "non_status_frontmatter_before": "".join(line for idx, line in enumerate(lines[1 : parsed["closing_index"]], start=1) if idx != status_index),
        "non_status_frontmatter_after": "".join(line for idx, line in enumerate(after_lines[1 : parsed["closing_index"]], start=1) if idx != status_index),
    }


def assert_copy_path(path: Path) -> None:
    resolved = path.resolve()
    resolved_root = COPY_ROOT.resolve()
    try:
        resolved.relative_to(resolved_root)
    except ValueError as exc:
        raise RuntimeError(f"copy path escapes sandbox copy root: {path}") from exc


def build_rehearsal() -> dict:
    package = load_json(P2_80)
    approval = load_json(P2_75)
    readiness = load_json(P2_77)
    COPY_ROOT.mkdir(parents=True, exist_ok=True)
    results = []

    for op in package["transaction_operations"]:
        original_path = WORKSPACE / op["target_path"]
        copy_path = COPY_ROOT / f"{op['operation_index']:03d}.md"
        assert_copy_path(copy_path)
        original_bytes = original_path.read_bytes()
        original_text = decode_utf8(original_bytes)
        original_sha = sha256_bytes(original_bytes)
        copy_path.write_bytes(original_bytes)
        copy_before_bytes = copy_path.read_bytes()
        copy_before_sha = sha256_bytes(copy_before_bytes)
        simulation = replace_status(decode_utf8(copy_before_bytes), op["proposed_status"])
        if simulation["valid"]:
            after_bytes = encode_utf8(simulation["after_text"])
            copy_path.write_bytes(after_bytes)
            after_read_bytes = copy_path.read_bytes()
            after_text = decode_utf8(after_read_bytes)
            after_status = parsed_status(after_text)
            after_byte_sha = sha256_bytes(after_read_bytes)
            after_body_unchanged = simulation["body_before"] == simulation["body_after"]
            after_body_bytes_unchanged = encode_utf8(simulation["body_before"]) == encode_utf8(simulation["body_after"])
            after_non_status_frontmatter_unchanged = simulation["non_status_frontmatter_before"] == simulation["non_status_frontmatter_after"]
            copy_path.write_bytes(encode_utf8(simulation["rollback_text"]))
            final_bytes = copy_path.read_bytes()
            final_text = decode_utf8(final_bytes)
            final_status = parsed_status(final_text)
            final_sha = sha256_bytes(final_bytes)
        else:
            after_status = None
            after_byte_sha = None
            after_body_unchanged = False
            after_body_bytes_unchanged = False
            after_non_status_frontmatter_unchanged = False
            final_bytes = copy_path.read_bytes()
            final_text = decode_utf8(final_bytes)
            final_status = parsed_status(final_text)
            final_sha = sha256_bytes(final_bytes)
        results.append(
            {
                "operation_index": op["operation_index"],
                "old_slice_id": op["old_slice_id"],
                "original_target_path": op["target_path"],
                "sandbox_copy_path": rel_slice(copy_path),
                "copy_path_within_slice": True,
                "original_sha256": original_sha,
                "original_byte_length": len(original_bytes),
                "p2_80_required_hash": op["prewrite_required_hash"],
                "original_hash_matches_p2_80": original_sha == op["prewrite_required_hash"],
                "copy_before_sha256": copy_before_sha,
                "copy_before_byte_length": len(copy_before_bytes),
                "copy_before_sha_matches_original": copy_before_sha == original_sha,
                "before_status": parsed_status(original_text),
                "proposed_status": op["proposed_status"],
                "rollback_status": op["rollback_status"],
                "apply_write_to_fixture": simulation["valid"],
                "after_status": after_status,
                "after_status_matches_proposed": after_status == op["proposed_status"],
                "after_byte_sha256": after_byte_sha,
                "body_unchanged_after_apply": after_body_unchanged,
                "body_bytes_unchanged_after_apply": after_body_bytes_unchanged,
                "non_status_frontmatter_unchanged": after_non_status_frontmatter_unchanged,
                "rollback_write_to_fixture": simulation["valid"],
                "final_copy_status": final_status,
                "final_copy_status_matches_rollback": final_status == op["rollback_status"],
                "final_copy_sha256": final_sha,
                "final_copy_byte_length": len(final_bytes),
                "final_copy_sha_matches_original": final_sha == original_sha,
                "final_copy_byte_sha_matches_original": final_sha == original_sha,
                "old_slice_write_applied": False,
                "write_target_family": "sandbox_fixture_copy",
                "simulation_error": simulation.get("error"),
            }
        )

    summary = {
        "fixture_copy_count": len(results),
        "fixture_apply_write_count": len([item for item in results if item["apply_write_to_fixture"]]),
        "fixture_rollback_write_count": len([item for item in results if item["rollback_write_to_fixture"]]),
        "copy_before_byte_sha_match_count": len([item for item in results if item["copy_before_sha_matches_original"]]),
        "after_status_match_count": len([item for item in results if item["after_status_matches_proposed"]]),
        "body_unchanged_after_apply_count": len([item for item in results if item["body_unchanged_after_apply"]]),
        "body_bytes_unchanged_after_apply_count": len([item for item in results if item["body_bytes_unchanged_after_apply"]]),
        "final_copy_sha_match_count": len([item for item in results if item["final_copy_sha_matches_original"]]),
        "final_copy_byte_sha_match_count": len([item for item in results if item["final_copy_byte_sha_matches_original"]]),
        "final_copy_status_match_count": len([item for item in results if item["final_copy_status_matches_rollback"]]),
        "non_status_frontmatter_unchanged_count": len([item for item in results if item["non_status_frontmatter_unchanged"]]),
        "rehearsal_failure_count": len([item for item in results if item["simulation_error"]]),
        "old_slice_writes_applied": 0,
    }
    p2_77_decision = readiness["current_decision"]
    return {
        "record_kind": "sandbox_copy_executor_rehearsal",
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
            "rehearsal_is_not_approval": True,
            "rehearsal_is_not_write_authority": True,
            "writes_limited_to_sandbox_fixtures": True,
            "requires_exact_p2_75_approval_before_real_write": True,
            "requires_fresh_hash_check_before_real_write": True,
            "requires_stop_before_write": True,
        },
        "rehearsal_results": results,
        "authority_flags": {
            "sandbox_copy_rehearsal_only": True,
            "approval_collected": False,
            "executor_write_allowed": False,
            "old_slice_write_allowed_now": False,
            "old_slice_writes_applied": 0,
            "normalization_applied": False,
            "rollback_applied_to_old_slices": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": False,
        },
    }


def render_markdown(rehearsal: dict) -> str:
    summary = rehearsal["summary"]
    gate = rehearsal["gate"]
    lines = [
        "# Sandbox Copy Executor Rehearsal",
        "",
        "Sandbox-only copy apply/rollback rehearsal. It does not write old slice files.",
        "",
        "## Summary",
        "",
        f"- fixture_copy_count: `{summary['fixture_copy_count']}`",
        f"- fixture_apply_write_count: `{summary['fixture_apply_write_count']}`",
        f"- fixture_rollback_write_count: `{summary['fixture_rollback_write_count']}`",
        f"- copy_before_byte_sha_match_count: `{summary['copy_before_byte_sha_match_count']}`",
        f"- after_status_match_count: `{summary['after_status_match_count']}`",
        f"- body_unchanged_after_apply_count: `{summary['body_unchanged_after_apply_count']}`",
        f"- body_bytes_unchanged_after_apply_count: `{summary['body_bytes_unchanged_after_apply_count']}`",
        f"- final_copy_sha_match_count: `{summary['final_copy_sha_match_count']}`",
        f"- final_copy_byte_sha_match_count: `{summary['final_copy_byte_sha_match_count']}`",
        f"- final_copy_status_match_count: `{summary['final_copy_status_match_count']}`",
        f"- non_status_frontmatter_unchanged_count: `{summary['non_status_frontmatter_unchanged_count']}`",
        f"- rehearsal_failure_count: `{summary['rehearsal_failure_count']}`",
        f"- old_slice_writes_applied: `{summary['old_slice_writes_applied']}`",
        "",
        "## Gate",
        "",
        f"- approval_collected_now: `{str(gate['approval_collected_now']).lower()}`",
        f"- p2_77_readiness: `{gate['p2_77_readiness']}`",
        f"- executor_write_allowed_now: `{str(gate['executor_write_allowed_now']).lower()}`",
        f"- rehearsal_is_not_approval: `{str(gate['rehearsal_is_not_approval']).lower()}`",
        f"- rehearsal_is_not_write_authority: `{str(gate['rehearsal_is_not_write_authority']).lower()}`",
        f"- writes_limited_to_sandbox_fixtures: `{str(gate['writes_limited_to_sandbox_fixtures']).lower()}`",
        f"- requires_exact_p2_75_approval_before_real_write: `{str(gate['requires_exact_p2_75_approval_before_real_write']).lower()}`",
        f"- requires_fresh_hash_check_before_real_write: `{str(gate['requires_fresh_hash_check_before_real_write']).lower()}`",
        f"- requires_stop_before_write: `{str(gate['requires_stop_before_write']).lower()}`",
        "",
        "## Boundary",
        "",
        "- Rehearsal success is not approval.",
        "- Rehearsal success is not write authority.",
        "- Fixture writes are confined to this sandbox.",
        "- No old slice write, normalization, rollback, mainline merge, promotion, reviewed knowledge, evidence support, action basis, or goal completion is authorized.",
    ]
    return "\n".join(lines) + "\n"


def render_html(markdown: str) -> str:
    escaped = html.escape(markdown)
    return (
        "<!doctype html>\n"
        "<html><head><meta charset=\"utf-8\"><title>p2-82 Sandbox Copy Rehearsal</title>"
        "<style>body{font-family:Segoe UI,Arial,sans-serif;max-width:1100px;margin:32px auto;line-height:1.5}"
        "pre{white-space:pre-wrap;background:#f6f8fa;padding:16px;border-radius:6px}</style></head>"
        f"<body><pre>{escaped}</pre></body></html>\n"
    )


def main() -> None:
    rehearsal = build_rehearsal()
    markdown = render_markdown(rehearsal)
    OUT_JSON.write_text(json.dumps(rehearsal, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    OUT_MD.write_text(markdown, encoding="utf-8")
    OUT_HTML.write_text(render_html(markdown), encoding="utf-8")
    print(json.dumps({"written": [str(OUT_JSON), str(OUT_MD), str(OUT_HTML)]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
