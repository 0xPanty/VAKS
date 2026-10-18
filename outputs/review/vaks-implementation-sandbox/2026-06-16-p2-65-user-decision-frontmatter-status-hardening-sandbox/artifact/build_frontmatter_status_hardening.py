from __future__ import annotations

import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-65-user-decision-frontmatter-status-hardening-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-64-user-decision-replay-portability-audit-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
SOURCE_ROOT = SANDBOX_ROOT / SOURCE_SLICE_ID
ARTIFACT = ROOT / "artifact"

OUTPUT_JSON = ARTIFACT / "frontmatter_status_hardening.json"
OUTPUT_MD = ARTIFACT / "frontmatter_status_hardening.md"
OUTPUT_HTML = ARTIFACT / "frontmatter_status_hardening.html"

SOURCE_REPORTS = {
    "verification": SOURCE_ROOT / "verification.md",
    "reviewer": SOURCE_ROOT / "reviewer-report.md",
    "boundary": SOURCE_ROOT / "boundary-audit.md",
    "product": SOURCE_ROOT / "product-acceptance-report.md",
    "next_step": SOURCE_ROOT / "next-step.md",
}

EXPECTED_SOURCE_STATUSES = {
    "verification": "local_verification_passed",
    "reviewer": "review_pass_no_blocker",
    "boundary": "pass_boundary",
    "product": "pass_product_grade",
    "next_step": "pass_product_grade_pending_next_slice",
}

HARD_NO = [
    "do_not_execute_user_decision_option",
    "do_not_merge_mainline",
    "do_not_promote",
    "do_not_sync_obsidian",
    "do_not_commit",
    "do_not_push",
    "do_not_install_dependencies",
    "do_not_start_background_service",
    "do_not_use_mcp_write_tool",
    "do_not_create_reviewed_knowledge",
    "do_not_create_evidence_support",
    "do_not_create_action_basis",
    "do_not_collect_user_approval_by_inference",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def relative(path: Path) -> str:
    return path.relative_to(WORKSPACE).as_posix()


def parse_strict_frontmatter_status(text: str) -> dict:
    lines = text.splitlines()
    errors: list[str] = []
    if not lines or lines[0].strip() != "---":
        return {
            "valid": False,
            "status": None,
            "errors": ["missing_opening_frontmatter_delimiter"],
            "frontmatter_line_count": 0,
            "body_status_mentions": [],
        }
    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        return {
            "valid": False,
            "status": None,
            "errors": ["missing_closing_frontmatter_delimiter"],
            "frontmatter_line_count": len(lines) - 1,
            "body_status_mentions": [],
        }
    frontmatter = lines[1:closing_index]
    body = lines[closing_index + 1 :]
    status_values: list[str] = []
    status_lines: list[int] = []
    for offset, line in enumerate(frontmatter, start=2):
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip() == "status":
            status_values.append(value.strip())
            status_lines.append(offset)
    if len(status_values) == 0:
        errors.append("missing_status_in_frontmatter")
    if len(status_values) > 1:
        errors.append("duplicate_status_in_frontmatter")
    if len(status_values) == 1 and not status_values[0]:
        errors.append("empty_status_in_frontmatter")
    body_status_mentions = [
        closing_index + 2 + offset
        for offset, line in enumerate(body)
        if line.strip().lower().startswith("status:")
    ]
    return {
        "valid": not errors,
        "status": status_values[0] if len(status_values) == 1 and status_values[0] else None,
        "errors": errors,
        "frontmatter_line_count": len(frontmatter),
        "body_status_mentions": body_status_mentions,
    }


def source_statuses() -> dict:
    statuses = {}
    for name, path in SOURCE_REPORTS.items():
        parsed = parse_strict_frontmatter_status(read_text(path))
        statuses[name] = {
            "path": relative(path),
            "valid_frontmatter": parsed["valid"],
            "status": parsed["status"],
            "expected_status": EXPECTED_SOURCE_STATUSES[name],
            "matches_expected": parsed["valid"] and parsed["status"] == EXPECTED_SOURCE_STATUSES[name],
            "body_status_mentions": parsed["body_status_mentions"],
        }
    return statuses


def build_hardening() -> dict:
    statuses = source_statuses()
    all_source_statuses_match = all(item["matches_expected"] for item in statuses.values())
    parser_contract = {
        "requires_opening_frontmatter_delimiter": True,
        "requires_closing_frontmatter_delimiter": True,
        "requires_exactly_one_status_in_frontmatter": True,
        "requires_non_empty_status": True,
        "ignores_body_status_mentions": True,
        "does_not_substring_match_pass_tokens": True,
    }
    sample = parse_strict_frontmatter_status(
        "---\n"
        "slice_id: sample\n"
        "status: pass_product_grade\n"
        "---\n"
        "\n"
        "status: product_acceptance_pending\n"
        "\n"
        "The body tries to override frontmatter, but the parser must not use it.\n"
    )
    return {
        "record_kind": "sandbox_frontmatter_status_hardening",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "purpose": "strict YAML-frontmatter status parsing for user-decision closeout gates",
        "frontmatter_status_hardening_ready": all_source_statuses_match and sample["valid"] and sample["status"] == "pass_product_grade",
        "parser_contract": parser_contract,
        "source_statuses": statuses,
        "sample_behavior": {
            "frontmatter_status_wins": sample["status"] == "pass_product_grade",
            "body_status_mentions_detected_not_used": len(sample["body_status_mentions"]) == 1,
        },
        "readiness_flags": {
            "automatic_execution": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "formal_vault_ready": False,
            "obsidian_sync_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "user_approval_collected": False,
        },
        "hard_no": HARD_NO,
    }


def render_markdown(payload: dict) -> str:
    lines = [
        "# Frontmatter Status Hardening",
        "",
        "Sandbox-only strict status parser for user-decision closeout reports.",
        "",
        f"- hardening ready: `{payload['frontmatter_status_hardening_ready']}`",
        f"- source slice: `{payload['source_slice_id']}`",
        "",
        "## Source Statuses",
        "",
        "| report | status | expected | match |",
        "| --- | --- | --- | --- |",
    ]
    for name, item in payload["source_statuses"].items():
        lines.append(f"| {name} | `{item['status']}` | `{item['expected_status']}` | `{item['matches_expected']}` |")
    lines.extend(["", "## Parser Contract", ""])
    lines.extend(f"- `{key}`: `{value}`" for key, value in payload["parser_contract"].items())
    lines.extend(["", "## Hard No", ""])
    lines.extend(f"- `{item}`" for item in payload["hard_no"])
    return "\n".join(lines)


def render_html(payload: dict) -> str:
    rows = "".join(
        f"<tr><td>{name}</td><td>{item['status']}</td><td>{item['expected_status']}</td><td>{item['matches_expected']}</td></tr>"
        for name, item in payload["source_statuses"].items()
    )
    contract = "".join(f"<li>{key}: {value}</li>" for key, value in payload["parser_contract"].items())
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Frontmatter Status Hardening</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }}
    main {{ max-width: 980px; margin: 0 auto; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #d1d5db; padding: 8px; text-align: left; }}
    th {{ background: #e5e7eb; }}
  </style>
</head>
<body>
<main>
  <h1>Frontmatter Status Hardening</h1>
  <p>Sandbox-only strict parser. It does not approve execution, merge, promotion, sync, reviewed knowledge, evidence support, action basis, or user approval.</p>
  <p><strong>Hardening ready:</strong> {payload['frontmatter_status_hardening_ready']}</p>
  <table><thead><tr><th>Report</th><th>Status</th><th>Expected</th><th>Match</th></tr></thead><tbody>{rows}</tbody></table>
  <h2>Parser Contract</h2>
  <ul>{contract}</ul>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    payload = build_hardening()
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(payload) + "\n", encoding="utf-8")
    OUTPUT_HTML.write_text(render_html(payload), encoding="utf-8")
    print(
        json.dumps(
            {
                "frontmatter_status_hardening_ready": payload["frontmatter_status_hardening_ready"],
                "source_slice_id": payload["source_slice_id"],
                "source_status_match_count": sum(1 for item in payload["source_statuses"].values() if item["matches_expected"]),
                "audit": str(OUTPUT_JSON),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if payload["frontmatter_status_hardening_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
