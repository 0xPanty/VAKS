from __future__ import annotations

import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-62-user-decision-operator-runbook-dry-run-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-61-user-decision-freeze-operator-readiness-brief-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
SOURCE_ROOT = SANDBOX_ROOT / SOURCE_SLICE_ID
ARTIFACT = ROOT / "artifact"

RUNBOOK_JSON = ARTIFACT / "user_decision_operator_runbook_dry_run.json"
RUNBOOK_MD = ARTIFACT / "user_decision_operator_runbook_dry_run.md"
RUNBOOK_HTML = ARTIFACT / "user_decision_operator_runbook_dry_run.html"

SOURCE_BRIEF = SOURCE_ROOT / "artifact" / "user_decision_freeze_operator_readiness_brief.json"
SOURCE_REPORTS = {
    "verification": SOURCE_ROOT / "verification.md",
    "reviewer": SOURCE_ROOT / "reviewer-report.md",
    "boundary": SOURCE_ROOT / "boundary-audit.md",
    "product": SOURCE_ROOT / "product-acceptance-report.md",
    "next_step": SOURCE_ROOT / "next-step.md",
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
    "do_not_install_hooks",
    "do_not_use_mcp_write_tool",
    "do_not_create_reviewed_knowledge",
    "do_not_create_evidence_support",
    "do_not_create_action_basis",
    "do_not_collect_user_approval_by_inference",
]

STOP_REQUEST_KINDS = [
    "execute_user_decision_option",
    "merge_mainline",
    "promote",
    "sync_obsidian",
    "commit",
    "push",
    "create_reviewed_knowledge",
    "create_evidence_support",
    "create_action_basis",
    "infer_user_approval",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def read_json(path: Path) -> dict:
    if not path.exists():
        return {}
    payload = json.loads(path.read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def frontmatter_status(path: Path) -> str:
    for line in read_text(path).splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def source_status() -> dict:
    return {
        "verification_status": frontmatter_status(SOURCE_REPORTS["verification"]),
        "reviewer_passed": "REVIEW_PASS_NO_BLOCKER" in read_text(SOURCE_REPORTS["reviewer"]),
        "boundary_passed": "PASS_BOUNDARY" in read_text(SOURCE_REPORTS["boundary"]),
        "product_acceptance_passed": "PASS_PRODUCT_GRADE" in read_text(SOURCE_REPORTS["product"]),
        "next_step_status": frontmatter_status(SOURCE_REPORTS["next_step"]),
    }


def scenario(request_kind: str, decision: str, reason: str, manual_only: bool = False) -> dict:
    return {
        "request_kind": request_kind,
        "decision": decision,
        "reason": reason,
        "manual_only": manual_only,
        "writes_files": False,
        "creates_authority": False,
    }


def build_runbook() -> dict:
    brief = read_json(SOURCE_BRIEF)
    status = source_status()
    flags = brief.get("readiness_flags", {}) if isinstance(brief.get("readiness_flags"), dict) else {}
    source_ready = (
        brief.get("brief_ready") is True
        and brief.get("readiness_inputs", {}).get("entry_count") == 268
        and brief.get("readiness_inputs", {}).get("source_slice_count") == 9
        and brief.get("readiness_inputs", {}).get("missing_count") == 0
        and brief.get("readiness_inputs", {}).get("hash_algorithm") == "sha256_bytes"
        and status["verification_status"] == "local_verification_passed"
        and status["reviewer_passed"] is True
        and status["boundary_passed"] is True
        and status["product_acceptance_passed"] is True
        and status["next_step_status"] == "pass_product_grade_pending_next_slice"
    )
    readiness_flags_clear = all(
        flags.get(key) is False
        for key in [
            "automatic_execution",
            "mainline_ready",
            "promotion_ready",
            "formal_vault_ready",
            "obsidian_sync_ready",
            "reviewed_knowledge_ready",
            "evidence_support_ready",
            "action_basis_ready",
            "user_approval_collected",
        ]
    )
    scenarios = [
        scenario(
            "inspect_readiness_brief",
            "ALLOW_READ_ONLY_INSPECTION",
            "p2-61 brief is product-accepted sandbox guidance and may be inspected read-only.",
        ),
        scenario(
            "inspect_frozen_handoff_chain",
            "ALLOW_READ_ONLY_INSPECTION",
            "p2-61 allows using p2-60 freeze as sandbox handoff integrity input only.",
        ),
        scenario(
            "manual_drift_check",
            "ALLOW_MANUAL_READONLY_VERIFICATION",
            "operator may manually run the p2-61 recorded p2-60 final-gate command; this artifact does not run it.",
            manual_only=True,
        ),
    ]
    scenarios.extend(
        scenario(
            request_kind,
            "STOP_REQUIRE_SEPARATE_USER_APPROVAL",
            "This request crosses sandbox handoff boundaries and needs separate explicit user approval.",
        )
        for request_kind in STOP_REQUEST_KINDS
    )
    return {
        "record_kind": "sandbox_user_decision_operator_runbook_dry_run",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "purpose": "dry-run operator runbook for safe use of the p2-61 readiness brief",
        "dry_run_only": True,
        "source_execution_by_builder": False,
        "runbook_ready": source_ready and readiness_flags_clear,
        "source_summary": {
            "brief_ready": brief.get("brief_ready"),
            "entry_count": brief.get("readiness_inputs", {}).get("entry_count"),
            "source_slice_count": brief.get("readiness_inputs", {}).get("source_slice_count"),
            "manual_verification_command": brief.get("manual_readonly_verification", {}).get("command"),
            "manual_verification_automated_by_source": brief.get("manual_readonly_verification", {}).get("automation_by_this_artifact"),
            "source_status": status,
        },
        "operator_decision_table": scenarios,
        "allowed_decisions": [
            "ALLOW_READ_ONLY_INSPECTION",
            "ALLOW_MANUAL_READONLY_VERIFICATION",
        ],
        "stop_decision": "STOP_REQUIRE_SEPARATE_USER_APPROVAL",
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
        "required_non_claims": [
            "This runbook is a dry-run only.",
            "This runbook is not user approval.",
            "This runbook is not execution authority.",
            "This runbook is not mainline approval.",
            "This runbook is not promotion approval.",
            "This runbook is not Obsidian sync approval.",
            "This runbook is not reviewed knowledge.",
            "This runbook is not evidence support.",
            "This runbook is not action basis.",
        ],
    }


def render_markdown(runbook: dict) -> str:
    lines = [
        "# User Decision Operator Runbook Dry Run",
        "",
        "Sandbox-only dry-run runbook. It uses the p2-61 readiness brief to decide whether a follow-up agent may inspect the frozen handoff chain. It cannot execute, merge, promote, sync, commit, push, create reviewed knowledge, create evidence support, create action basis, or infer user approval.",
        "",
        f"- runbook ready: `{runbook['runbook_ready']}`",
        f"- dry run only: `{runbook['dry_run_only']}`",
        f"- source slice: `{runbook['source_slice_id']}`",
        f"- frozen entries: `{runbook['source_summary']['entry_count']}`",
        "",
        "## Decision Table",
        "",
        "| Request kind | Decision | Manual only |",
        "| --- | --- | --- |",
    ]
    for row in runbook["operator_decision_table"]:
        lines.append(f"| `{row['request_kind']}` | `{row['decision']}` | `{row['manual_only']}` |")
    lines.extend(["", "## Manual Verification Command", "", "```powershell"])
    lines.append(str(runbook["source_summary"]["manual_verification_command"]))
    lines.extend(["```", "", "This runbook records the command only; it does not run it.", "", "## Hard No", ""])
    lines.extend(f"- `{item}`" for item in runbook["hard_no"])
    return "\n".join(lines)


def render_html(runbook: dict) -> str:
    rows = "".join(
        f"<tr><td>{row['request_kind']}</td><td>{row['decision']}</td><td>{row['manual_only']}</td></tr>"
        for row in runbook["operator_decision_table"]
    )
    hard_no = "".join(f"<li>{item}</li>" for item in runbook["hard_no"])
    command = runbook["source_summary"]["manual_verification_command"]
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>User Decision Operator Runbook Dry Run</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }}
    main {{ max-width: 1080px; margin: 0 auto; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #d1d5db; padding: 8px; text-align: left; }}
    th {{ background: #e5e7eb; }}
    pre {{ background: #eef2f7; padding: 12px; overflow-x: auto; }}
  </style>
</head>
<body>
<main>
  <h1>User Decision Operator Runbook Dry Run</h1>
  <p>Sandbox-only dry-run runbook. It allows read-only inspection only and requires separate explicit user approval for execution, merge, promotion, sync, commit, push, reviewed knowledge, evidence support, or action basis.</p>
  <p><strong>Runbook ready:</strong> {runbook['runbook_ready']}<br><strong>Frozen entries:</strong> {runbook['source_summary']['entry_count']}</p>
  <table><thead><tr><th>Request kind</th><th>Decision</th><th>Manual only</th></tr></thead><tbody>{rows}</tbody></table>
  <h2>Manual verification command</h2>
  <pre>{command}</pre>
  <p>This runbook records the command only; it does not run it.</p>
  <h2>Hard no</h2>
  <ul>{hard_no}</ul>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    runbook = build_runbook()
    RUNBOOK_JSON.write_text(json.dumps(runbook, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    RUNBOOK_MD.write_text(render_markdown(runbook) + "\n", encoding="utf-8")
    RUNBOOK_HTML.write_text(render_html(runbook), encoding="utf-8")
    print(
        json.dumps(
            {
                "runbook_ready": runbook["runbook_ready"],
                "source_slice_id": runbook["source_slice_id"],
                "scenario_count": len(runbook["operator_decision_table"]),
                "entry_count": runbook["source_summary"]["entry_count"],
                "runbook": str(RUNBOOK_JSON),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if runbook["runbook_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
