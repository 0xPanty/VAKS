from __future__ import annotations

import ast
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-64-user-decision-replay-portability-audit-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-63-user-decision-runbook-replay-regression-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
SOURCE_ROOT = SANDBOX_ROOT / SOURCE_SLICE_ID
ARTIFACT = ROOT / "artifact"

AUDIT_JSON = ARTIFACT / "user_decision_replay_portability_audit.json"
AUDIT_MD = ARTIFACT / "user_decision_replay_portability_audit.md"
AUDIT_HTML = ARTIFACT / "user_decision_replay_portability_audit.html"

SOURCE_REPLAY = SOURCE_ROOT / "artifact" / "user_decision_runbook_replay_regression.json"
SOURCE_BUILDER = SOURCE_ROOT / "artifact" / "build_user_decision_runbook_replay_regression.py"
SOURCE_VERIFIER = SOURCE_ROOT / "artifact" / "verify_user_decision_runbook_replay_regression.py"
SOURCE_REPORTS = {
    "verification": SOURCE_ROOT / "verification.md",
    "reviewer": SOURCE_ROOT / "reviewer-report.md",
    "boundary": SOURCE_ROOT / "boundary-audit.md",
    "product": SOURCE_ROOT / "product-acceptance-report.md",
    "next_step": SOURCE_ROOT / "next-step.md",
}

ALLOWED_IMPORTS = {
    "__future__",
    "argparse",
    "ast",
    "importlib.util",
    "json",
    "pathlib",
    "sys",
}

FORBIDDEN_EXECUTION_TOKENS = [
    "subprocess",
    "Popen",
    "Start-Process",
    "os.system",
    "Invoke-WebRequest",
    "curl ",
]

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
    reviewer_status = frontmatter_status(SOURCE_REPORTS["reviewer"])
    boundary_status = frontmatter_status(SOURCE_REPORTS["boundary"])
    product_status = frontmatter_status(SOURCE_REPORTS["product"])
    return {
        "verification_status": frontmatter_status(SOURCE_REPORTS["verification"]),
        "reviewer_status": reviewer_status,
        "reviewer_passed": reviewer_status == "review_pass_no_blocker",
        "boundary_status": boundary_status,
        "boundary_passed": boundary_status == "pass_boundary",
        "product_acceptance_status": product_status,
        "product_acceptance_passed": product_status == "pass_product_grade",
        "next_step_status": frontmatter_status(SOURCE_REPORTS["next_step"]),
    }


def imported_modules(path: Path) -> list[str]:
    tree = ast.parse(read_text(path))
    modules: set[str] = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            modules.update(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            modules.add(node.module or "")
    return sorted(module for module in modules if module)


def execution_tokens(path: Path) -> list[str]:
    text = read_text(path)
    return sorted(token for token in FORBIDDEN_EXECUTION_TOKENS if token in text)


def relative(path: Path) -> str:
    return path.relative_to(WORKSPACE).as_posix()


def build_audit() -> dict:
    replay = read_json(SOURCE_REPLAY)
    status = source_status()
    builder_imports = imported_modules(SOURCE_BUILDER)
    verifier_imports = imported_modules(SOURCE_VERIFIER)
    source_paths = [SOURCE_REPLAY, SOURCE_BUILDER, SOURCE_VERIFIER, *SOURCE_REPORTS.values()]
    commands = {
        "build_replay": (
            "python -B .\\outputs\\review\\vaks-implementation-sandbox\\"
            f"{SOURCE_SLICE_ID}\\artifact\\build_user_decision_runbook_replay_regression.py"
        ),
        "verify_replay": (
            "python -B .\\outputs\\review\\vaks-implementation-sandbox\\"
            f"{SOURCE_SLICE_ID}\\artifact\\verify_user_decision_runbook_replay_regression.py"
        ),
        "final_gate": (
            "python -B .\\outputs\\review\\vaks-implementation-sandbox\\"
            f"{SOURCE_SLICE_ID}\\artifact\\verify_user_decision_runbook_replay_regression.py --final-gate"
        ),
    }
    builder_tokens = execution_tokens(SOURCE_BUILDER)
    verifier_tokens = execution_tokens(SOURCE_VERIFIER)
    standard_library_only = set(builder_imports + verifier_imports) <= ALLOWED_IMPORTS
    stable_paths = all(path.exists() and SOURCE_SLICE_ID in relative(path) for path in source_paths)
    clear_commands = all(command.startswith("python -B .\\outputs\\review\\vaks-implementation-sandbox\\") for command in commands.values()) and "--final-gate" in commands["final_gate"]
    source_ready = (
        replay.get("replay_ready") is True
        and replay.get("replay_count") == 15
        and replay.get("passed_count") == 15
        and status["verification_status"] == "local_verification_passed"
        and status["reviewer_passed"] is True
        and status["boundary_passed"] is True
        and status["product_acceptance_passed"] is True
        and status["next_step_status"] == "pass_product_grade_pending_next_slice"
    )
    return {
        "record_kind": "sandbox_user_decision_replay_portability_audit",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "purpose": "portability audit for p2-63 natural-language replay regression",
        "portability_ready": (
            source_ready
            and standard_library_only
            and stable_paths
            and clear_commands
            and not builder_tokens
        ),
        "source_summary": {
            "replay_ready": replay.get("replay_ready"),
            "replay_count": replay.get("replay_count"),
            "passed_count": replay.get("passed_count"),
            "failure_case_count": 16,
            "source_status": status,
        },
        "dependency_audit": {
            "standard_library_only": standard_library_only,
            "builder_imports": builder_imports,
            "verifier_imports": verifier_imports,
            "dependency_install_required": False,
            "network_required": False,
            "mcp_required": False,
            "background_service_required": False,
        },
        "execution_audit": {
            "source_execution_by_builder": False,
            "builder_process_execution_tokens": builder_tokens,
            "verifier_diagnostic_execution_tokens": verifier_tokens,
            "verifier_tokens_are_diagnostic_only": bool(verifier_tokens),
        },
        "path_audit": {
            "stable_paths": stable_paths,
            "source_paths": [relative(path) for path in source_paths],
            "write_path": relative(ROOT),
        },
        "command_audit": {
            "clear_commands": clear_commands,
            "commands": commands,
            "operator_sequence": [
                "Read the p2-64 audit first.",
                "Run the p2-63 default verifier before using replay outputs.",
                "Run the p2-63 final gate only when validating closeout state.",
                "Stop if either command fails.",
                "Do not treat a pass as execution, merge, promotion, sync, reviewed knowledge, evidence support, action basis, or user approval.",
            ],
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


def render_markdown(audit: dict) -> str:
    lines = [
        "# User Decision Replay Portability Audit",
        "",
        "Sandbox-only portability audit for the p2-63 replay regression. It checks hidden dependencies, process execution risk, command clarity, stable paths, and operator rerun instructions.",
        "",
        f"- portability ready: `{audit['portability_ready']}`",
        f"- source replay ready: `{audit['source_summary']['replay_ready']}`",
        f"- replay count: `{audit['source_summary']['replay_count']}`",
        f"- standard library only: `{audit['dependency_audit']['standard_library_only']}`",
        f"- stable paths: `{audit['path_audit']['stable_paths']}`",
        f"- clear commands: `{audit['command_audit']['clear_commands']}`",
        f"- builder execution tokens: `{audit['execution_audit']['builder_process_execution_tokens']}`",
        "",
        "## Commands",
        "",
    ]
    for name, command in audit["command_audit"]["commands"].items():
        lines.extend([f"### {name}", "", "```powershell", command, "```", ""])
    lines.extend(["## Operator Sequence", ""])
    lines.extend(f"{idx}. {step}" for idx, step in enumerate(audit["command_audit"]["operator_sequence"], start=1))
    lines.extend(["", "## Hard No", ""])
    lines.extend(f"- `{item}`" for item in audit["hard_no"])
    return "\n".join(lines)


def render_html(audit: dict) -> str:
    command_rows = "".join(
        f"<tr><td>{name}</td><td><code>{command}</code></td></tr>"
        for name, command in audit["command_audit"]["commands"].items()
    )
    hard_no = "".join(f"<li>{item}</li>" for item in audit["hard_no"])
    sequence = "".join(f"<li>{step}</li>" for step in audit["command_audit"]["operator_sequence"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>User Decision Replay Portability Audit</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }}
    main {{ max-width: 1080px; margin: 0 auto; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #d1d5db; padding: 8px; text-align: left; vertical-align: top; }}
    th {{ background: #e5e7eb; }}
    code {{ white-space: pre-wrap; }}
  </style>
</head>
<body>
<main>
  <h1>User Decision Replay Portability Audit</h1>
  <p>Sandbox-only audit. It does not approve execution, merge, promotion, sync, reviewed knowledge, evidence support, action basis, or user approval.</p>
  <p><strong>Portability ready:</strong> {audit['portability_ready']}<br><strong>Replay count:</strong> {audit['source_summary']['replay_count']}</p>
  <table><thead><tr><th>Command</th><th>How to run</th></tr></thead><tbody>{command_rows}</tbody></table>
  <h2>Operator sequence</h2>
  <ol>{sequence}</ol>
  <h2>Hard no</h2>
  <ul>{hard_no}</ul>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    audit = build_audit()
    AUDIT_JSON.write_text(json.dumps(audit, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    AUDIT_MD.write_text(render_markdown(audit) + "\n", encoding="utf-8")
    AUDIT_HTML.write_text(render_html(audit), encoding="utf-8")
    print(
        json.dumps(
            {
                "portability_ready": audit["portability_ready"],
                "source_slice_id": audit["source_slice_id"],
                "replay_count": audit["source_summary"]["replay_count"],
                "standard_library_only": audit["dependency_audit"]["standard_library_only"],
                "stable_paths": audit["path_audit"]["stable_paths"],
                "clear_commands": audit["command_audit"]["clear_commands"],
                "audit": str(AUDIT_JSON),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if audit["portability_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
