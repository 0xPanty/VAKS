from __future__ import annotations

import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-68-user-decision-strict-status-adoption-screen-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-67-user-decision-strict-status-package-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
SOURCE_ROOT = SANDBOX_ROOT / SOURCE_SLICE_ID
ARTIFACT = ROOT / "artifact"

OUTPUT_JSON = ARTIFACT / "strict_status_adoption_screen.json"
OUTPUT_MD = ARTIFACT / "strict_status_adoption_screen.md"
OUTPUT_HTML = ARTIFACT / "strict_status_adoption_screen.html"

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
    "do_not_modify_old_slices",
    "do_not_create_shared_helper",
    "do_not_edit_tools",
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


def strict_status(text: str) -> str | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    closing = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing = index
            break
    if closing is None:
        return None
    values: list[str] = []
    for line in lines[1:closing]:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip() == "status" and value.strip():
            values.append(value.strip())
    return values[0] if len(values) == 1 else None


def source_statuses() -> dict:
    statuses = {}
    for name, path in SOURCE_REPORTS.items():
        status = strict_status(read_text(path))
        statuses[name] = {
            "path": relative(path),
            "status": status,
            "expected_status": EXPECTED_SOURCE_STATUSES[name],
            "matches_expected": status == EXPECTED_SOURCE_STATUSES[name],
        }
    return statuses


def adoption_options() -> list[dict]:
    return [
        {
            "option_id": "future_new_sandbox_verifier_adoption",
            "label": "Use strict status package in future new sandbox verifiers",
            "decision": "RECOMMENDED_NEXT",
            "allowed_without_separate_user_approval": True,
            "write_scope": "new sandbox path only",
            "why": "Uses p2-67 package without rewriting accepted old slices or shared tools.",
            "forbidden_actions": HARD_NO,
        },
        {
            "option_id": "package_only_hold",
            "label": "Keep package as reference-only sandbox artifact",
            "decision": "ALLOW_AS_PARKED_OPTION",
            "allowed_without_separate_user_approval": True,
            "write_scope": "new sandbox path only",
            "why": "Valid conservative fallback if adoption is not needed immediately.",
            "forbidden_actions": HARD_NO,
        },
        {
            "option_id": "old_slice_backfill",
            "label": "Backfill old accepted sandbox verifiers",
            "decision": "PARK_REQUIRES_SEPARATE_USER_APPROVAL",
            "allowed_without_separate_user_approval": False,
            "write_scope": "older sandbox paths",
            "why": "Would rewrite accepted historical artifacts.",
            "forbidden_actions": HARD_NO,
        },
        {
            "option_id": "shared_helper_or_tools_adoption",
            "label": "Move package into shared helper or tools",
            "decision": "PARK_REQUIRES_SEPARATE_USER_APPROVAL",
            "allowed_without_separate_user_approval": False,
            "write_scope": "shared helper or tools path",
            "why": "Would leave the current sandbox write boundary.",
            "forbidden_actions": HARD_NO,
        },
        {
            "option_id": "mainline_integration",
            "label": "Integrate package into main architecture",
            "decision": "PARK_REQUIRES_SEPARATE_USER_APPROVAL",
            "allowed_without_separate_user_approval": False,
            "write_scope": "mainline architecture",
            "why": "Would be promotion/mainline work, not sandbox screening.",
            "forbidden_actions": HARD_NO,
        },
    ]


def build_screen() -> dict:
    statuses = source_statuses()
    options = adoption_options()
    by_id = {item["option_id"]: item for item in options}
    ready = (
        all(item["matches_expected"] for item in statuses.values())
        and by_id["future_new_sandbox_verifier_adoption"]["decision"] == "RECOMMENDED_NEXT"
        and by_id["old_slice_backfill"]["decision"] == "PARK_REQUIRES_SEPARATE_USER_APPROVAL"
        and by_id["shared_helper_or_tools_adoption"]["decision"] == "PARK_REQUIRES_SEPARATE_USER_APPROVAL"
        and by_id["mainline_integration"]["decision"] == "PARK_REQUIRES_SEPARATE_USER_APPROVAL"
    )
    return {
        "record_kind": "sandbox_strict_status_adoption_screen",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "purpose": "screen safe adoption route for strict status package",
        "adoption_screen_ready": ready,
        "source_statuses": statuses,
        "adoption_options": options,
        "recommended_next_slice": {
            "slice_id": "2026-06-16-p2-69-user-decision-future-verifier-adoption-prototype-sandbox",
            "purpose": "prototype use of the strict status package in one new sandbox verifier without editing old slices or shared tools",
            "write_scope": "new sandbox path only",
        },
        "readiness_flags": {
            "dependency_install_required": False,
            "network_required": False,
            "mcp_required": False,
            "background_service_required": False,
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
        "# Strict Status Adoption Screen",
        "",
        "Sandbox-only adoption screening for the strict status package.",
        "",
        f"- adoption screen ready: `{payload['adoption_screen_ready']}`",
        f"- recommended next slice: `{payload['recommended_next_slice']['slice_id']}`",
        "",
        "## Adoption Options",
        "",
        "| option | decision | allowed without separate approval |",
        "| --- | --- | --- |",
    ]
    for option in payload["adoption_options"]:
        lines.append(f"| `{option['option_id']}` | `{option['decision']}` | `{option['allowed_without_separate_user_approval']}` |")
    lines.extend(["", "## Hard No", ""])
    lines.extend(f"- `{item}`" for item in payload["hard_no"])
    return "\n".join(lines)


def render_html(payload: dict) -> str:
    rows = "".join(
        f"<tr><td>{option['option_id']}</td><td>{option['decision']}</td><td>{option['allowed_without_separate_user_approval']}</td></tr>"
        for option in payload["adoption_options"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Strict Status Adoption Screen</title>
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
  <h1>Strict Status Adoption Screen</h1>
  <p>Sandbox-only screen. It does not approve old-slice edits, shared helper edits, tools edits, merge, promotion, sync, reviewed knowledge, evidence support, action basis, or user approval.</p>
  <p><strong>Adoption screen ready:</strong> {payload['adoption_screen_ready']}</p>
  <table><thead><tr><th>Option</th><th>Decision</th><th>Allowed without separate approval</th></tr></thead><tbody>{rows}</tbody></table>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    payload = build_screen()
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(payload) + "\n", encoding="utf-8")
    OUTPUT_HTML.write_text(render_html(payload), encoding="utf-8")
    print(
        json.dumps(
            {
                "adoption_screen_ready": payload["adoption_screen_ready"],
                "recommended_next_slice": payload["recommended_next_slice"]["slice_id"],
                "option_count": len(payload["adoption_options"]),
                "audit": str(OUTPUT_JSON),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if payload["adoption_screen_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
