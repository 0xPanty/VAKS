from __future__ import annotations

import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-61-user-decision-freeze-operator-readiness-brief-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-60-user-decision-index-freeze-checksum-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
SOURCE_ROOT = SANDBOX_ROOT / SOURCE_SLICE_ID
ARTIFACT = ROOT / "artifact"

BRIEF_JSON = ARTIFACT / "user_decision_freeze_operator_readiness_brief.json"
BRIEF_MD = ARTIFACT / "user_decision_freeze_operator_readiness_brief.md"
BRIEF_HTML = ARTIFACT / "user_decision_freeze_operator_readiness_brief.html"

SOURCE_MANIFEST = SOURCE_ROOT / "artifact" / "user_decision_index_freeze_checksum_manifest.json"
SOURCE_REPORTS = {
    "verification": SOURCE_ROOT / "verification.md",
    "reviewer": SOURCE_ROOT / "reviewer-report.md",
    "boundary": SOURCE_ROOT / "boundary-audit.md",
    "product": SOURCE_ROOT / "product-acceptance-report.md",
    "next_step": SOURCE_ROOT / "next-step.md",
}

MANUAL_VERIFICATION_COMMAND = (
    "python -B .\\outputs\\review\\vaks-implementation-sandbox\\"
    f"{SOURCE_SLICE_ID}\\artifact\\verify_user_decision_index_freeze_checksum.py --final-gate"
)

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
    "do_not_treat_checksum_as_user_approval",
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
    product_text = read_text(SOURCE_REPORTS["product"])
    reviewer_text = read_text(SOURCE_REPORTS["reviewer"])
    boundary_text = read_text(SOURCE_REPORTS["boundary"])
    return {
        "verification_status": frontmatter_status(SOURCE_REPORTS["verification"]),
        "reviewer_passed": "REVIEW_PASS_NO_BLOCKER" in reviewer_text,
        "boundary_passed": "PASS_BOUNDARY" in boundary_text,
        "product_acceptance_passed": "PASS_PRODUCT_GRADE" in product_text,
        "next_step_status": frontmatter_status(SOURCE_REPORTS["next_step"]),
    }


def build_brief() -> dict:
    manifest = read_json(SOURCE_MANIFEST)
    status = source_status()
    readiness_inputs = {
        "source_manifest_exists": SOURCE_MANIFEST.exists(),
        "source_manifest_path": SOURCE_MANIFEST.relative_to(WORKSPACE).as_posix(),
        "source_slice_count": len(manifest.get("source_slice_ids", [])),
        "entry_count": manifest.get("entry_count"),
        "missing_count": manifest.get("missing_count"),
        "hash_algorithm": manifest.get("hash_algorithm"),
        "freeze_ready": manifest.get("freeze_ready"),
        "latest_source_final_gate_passed": manifest.get("latest_source_final_gate_passed"),
    }
    brief_ready = (
        readiness_inputs["source_manifest_exists"] is True
        and readiness_inputs["source_slice_count"] == 9
        and isinstance(readiness_inputs["entry_count"], int)
        and readiness_inputs["entry_count"] > 0
        and readiness_inputs["missing_count"] == 0
        and readiness_inputs["hash_algorithm"] == "sha256_bytes"
        and readiness_inputs["freeze_ready"] is True
        and readiness_inputs["latest_source_final_gate_passed"] is True
        and status["verification_status"] == "local_verification_passed"
        and status["reviewer_passed"] is True
        and status["boundary_passed"] is True
        and status["product_acceptance_passed"] is True
        and status["next_step_status"] == "pass_product_grade_pending_next_slice"
    )
    return {
        "record_kind": "sandbox_user_decision_freeze_operator_readiness_brief",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "purpose": "operator-facing readiness brief for the p2-60 checksum freeze",
        "brief_ready": brief_ready,
        "readiness_inputs": readiness_inputs,
        "source_status": status,
        "manual_readonly_verification": {
            "command": MANUAL_VERIFICATION_COMMAND,
            "intent": "manually re-run p2-60 final gate before using the freeze as a sandbox handoff input",
            "automation_by_this_artifact": False,
            "writes_files": False,
        },
        "operator_steps": [
            "Read this brief and confirm the source slice is p2-60.",
            "If drift must be checked, run the manual read-only verification command.",
            "If the command fails, stop and inspect p2-60 before using the handoff index.",
            "If the command passes, use the freeze only as sandbox handoff integrity input.",
            "Ask the user separately before any execution, merge, promotion, sync, commit, or push.",
        ],
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
            "This brief is not user approval.",
            "This brief is not execution authority.",
            "This brief is not mainline approval.",
            "This brief is not promotion approval.",
            "This brief is not formal-vault approval.",
            "This brief is not Obsidian sync approval.",
            "This brief is not reviewed knowledge.",
            "This brief is not evidence support.",
            "This brief is not action basis.",
        ],
    }


def render_markdown(brief: dict) -> str:
    inputs = brief["readiness_inputs"]
    flags = brief["readiness_flags"]
    lines = [
        "# User Decision Freeze Operator Readiness Brief",
        "",
        "Sandbox-only operator brief for the p2-60 checksum freeze. It explains what is frozen, how to manually verify drift, and what still cannot be executed without separate user approval.",
        "",
        f"- brief ready: `{brief['brief_ready']}`",
        f"- source slice: `{brief['source_slice_id']}`",
        f"- frozen source slices: `{inputs['source_slice_count']}`",
        f"- frozen file entries: `{inputs['entry_count']}`",
        f"- missing count: `{inputs['missing_count']}`",
        f"- hash algorithm: `{inputs['hash_algorithm']}`",
        f"- freeze ready: `{inputs['freeze_ready']}`",
        "",
        "## Manual Drift Verification",
        "",
        "Run this only when an operator needs to re-check p2-60 before using the handoff chain:",
        "",
        "```powershell",
        brief["manual_readonly_verification"]["command"],
        "```",
        "",
        "This p2-61 builder does not run that command. It only records the manual read-only check.",
        "",
        "## Operator Steps",
        "",
    ]
    lines.extend(f"{idx}. {step}" for idx, step in enumerate(brief["operator_steps"], start=1))
    lines.extend(["", "## Readiness Flags", ""])
    lines.extend(f"- `{key}`: `{value}`" for key, value in flags.items())
    lines.extend(["", "## Hard No", ""])
    lines.extend(f"- `{item}`" for item in brief["hard_no"])
    return "\n".join(lines)


def render_html(brief: dict) -> str:
    inputs = brief["readiness_inputs"]
    steps = "".join(f"<li>{step}</li>" for step in brief["operator_steps"])
    flags = "".join(f"<tr><td>{key}</td><td>{value}</td></tr>" for key, value in brief["readiness_flags"].items())
    hard_no = "".join(f"<li>{item}</li>" for item in brief["hard_no"])
    command = brief["manual_readonly_verification"]["command"]
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>User Decision Freeze Operator Readiness Brief</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }}
    main {{ max-width: 1080px; margin: 0 auto; }}
    code, pre {{ background: #eef2f7; padding: 2px 4px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #d1d5db; padding: 8px; text-align: left; }}
    th {{ background: #e5e7eb; }}
  </style>
</head>
<body>
<main>
  <h1>User Decision Freeze Operator Readiness Brief</h1>
  <p>Sandbox-only brief for the p2-60 checksum freeze. It is not user approval, execution authority, mainline approval, promotion approval, reviewed knowledge, evidence support, or action basis.</p>
  <p><strong>Brief ready:</strong> {brief['brief_ready']}<br><strong>Frozen entries:</strong> {inputs['entry_count']}<br><strong>Source slices:</strong> {inputs['source_slice_count']}</p>
  <h2>Manual drift verification</h2>
  <pre>{command}</pre>
  <p>The p2-61 builder records this manual read-only check and does not run it.</p>
  <h2>Operator steps</h2>
  <ol>{steps}</ol>
  <h2>Readiness flags</h2>
  <table><thead><tr><th>Flag</th><th>Value</th></tr></thead><tbody>{flags}</tbody></table>
  <h2>Hard no</h2>
  <ul>{hard_no}</ul>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    brief = build_brief()
    BRIEF_JSON.write_text(json.dumps(brief, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    BRIEF_MD.write_text(render_markdown(brief) + "\n", encoding="utf-8")
    BRIEF_HTML.write_text(render_html(brief), encoding="utf-8")
    print(
        json.dumps(
            {
                "brief_ready": brief["brief_ready"],
                "source_slice_id": brief["source_slice_id"],
                "entry_count": brief["readiness_inputs"]["entry_count"],
                "source_slice_count": brief["readiness_inputs"]["source_slice_count"],
                "brief": str(BRIEF_JSON),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if brief["brief_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
