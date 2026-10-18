from __future__ import annotations

import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-66-user-decision-chain-hardening-readiness-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-65-user-decision-frontmatter-status-hardening-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
SOURCE_ROOT = SANDBOX_ROOT / SOURCE_SLICE_ID
ARTIFACT = ROOT / "artifact"

OUTPUT_JSON = ARTIFACT / "chain_hardening_readiness.json"
OUTPUT_MD = ARTIFACT / "chain_hardening_readiness.md"
OUTPUT_HTML = ARTIFACT / "chain_hardening_readiness.html"

SOURCE_VERIFIER = SOURCE_ROOT / "artifact" / "verify_frontmatter_status_hardening.py"
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


def build_decision_options() -> list[dict]:
    return [
        {
            "option_id": "sandbox_chain_hardening_package",
            "label": "Package strict status helper for sandbox reuse",
            "decision": "RECOMMENDED_NEXT",
            "why": "Keeps changes inside a new sandbox while making p2-65 reusable by future user-decision gates.",
            "write_scope": "new sandbox path only",
            "requires_user_separate_approval": False,
            "allowed_actions": [
                "create sandbox package artifact",
                "write package contract",
                "write fixtures and failure cases",
                "run local verifier",
            ],
            "forbidden_actions": HARD_NO,
        },
        {
            "option_id": "old_slice_backfill",
            "label": "Backfill older p2-63/p2-64 verifiers",
            "decision": "PARK_REQUIRES_SEPARATE_USER_APPROVAL",
            "why": "Would modify older sandbox artifacts and risks rewriting accepted historical evidence.",
            "write_scope": "older sandbox paths",
            "requires_user_separate_approval": True,
            "allowed_actions": [],
            "forbidden_actions": HARD_NO,
        },
        {
            "option_id": "shared_helper_or_tools",
            "label": "Move parser into a shared helper or tools path",
            "decision": "PARK_REQUIRES_SEPARATE_USER_APPROVAL",
            "why": "Would touch shared/tooling paths that are outside the current sandbox permission.",
            "write_scope": "shared helper or tools path",
            "requires_user_separate_approval": True,
            "allowed_actions": [],
            "forbidden_actions": HARD_NO,
        },
        {
            "option_id": "return_to_broader_p2_workflow",
            "label": "Return to broader P2 product workflow backlog",
            "decision": "ALLOW_AFTER_RECORDING_HANDOFF",
            "why": "p2-65 is closed; returning to backlog is valid if the next slice records the handoff and does not imply merge.",
            "write_scope": "new sandbox path only",
            "requires_user_separate_approval": False,
            "allowed_actions": [
                "write sandbox handoff",
                "write next backlog selection record",
            ],
            "forbidden_actions": HARD_NO,
        },
    ]


def build_readiness() -> dict:
    statuses = source_statuses()
    source_ready = all(item["matches_expected"] for item in statuses.values())
    options = build_decision_options()
    recommended = [item["option_id"] for item in options if item["decision"] == "RECOMMENDED_NEXT"]
    return {
        "record_kind": "sandbox_chain_hardening_readiness",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "purpose": "decide the next safe sandbox step after strict frontmatter status hardening",
        "chain_hardening_readiness_ready": source_ready and recommended == ["sandbox_chain_hardening_package"],
        "source_statuses": statuses,
        "source_verifier_path": relative(SOURCE_VERIFIER),
        "decision_options": options,
        "recommended_next_slice": {
            "slice_id": "2026-06-16-p2-67-user-decision-strict-status-package-sandbox",
            "purpose": "package the p2-65 strict status parser as a reusable sandbox artifact without modifying old slices or shared tools",
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
        "# Chain Hardening Readiness",
        "",
        "Sandbox-only decision artifact for the next safe user-decision chain hardening step.",
        "",
        f"- readiness ready: `{payload['chain_hardening_readiness_ready']}`",
        f"- recommended next slice: `{payload['recommended_next_slice']['slice_id']}`",
        "",
        "## Decision Options",
        "",
        "| option | decision | separate approval |",
        "| --- | --- | --- |",
    ]
    for option in payload["decision_options"]:
        lines.append(f"| `{option['option_id']}` | `{option['decision']}` | `{option['requires_user_separate_approval']}` |")
    lines.extend(["", "## Hard No", ""])
    lines.extend(f"- `{item}`" for item in payload["hard_no"])
    return "\n".join(lines)


def render_html(payload: dict) -> str:
    rows = "".join(
        f"<tr><td>{option['option_id']}</td><td>{option['decision']}</td><td>{option['requires_user_separate_approval']}</td></tr>"
        for option in payload["decision_options"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Chain Hardening Readiness</title>
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
  <h1>Chain Hardening Readiness</h1>
  <p>Sandbox-only decision artifact. It does not approve old-slice edits, shared helper edits, merge, promotion, sync, reviewed knowledge, evidence support, action basis, or user approval.</p>
  <p><strong>Readiness ready:</strong> {payload['chain_hardening_readiness_ready']}</p>
  <table><thead><tr><th>Option</th><th>Decision</th><th>Separate approval</th></tr></thead><tbody>{rows}</tbody></table>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    payload = build_readiness()
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(payload) + "\n", encoding="utf-8")
    OUTPUT_HTML.write_text(render_html(payload), encoding="utf-8")
    print(
        json.dumps(
            {
                "chain_hardening_readiness_ready": payload["chain_hardening_readiness_ready"],
                "recommended_next_slice": payload["recommended_next_slice"]["slice_id"],
                "option_count": len(payload["decision_options"]),
                "audit": str(OUTPUT_JSON),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if payload["chain_hardening_readiness_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
