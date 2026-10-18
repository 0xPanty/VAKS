from __future__ import annotations

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
CONTRACT_PATH = ROOT / "artifact" / "user_decision_operator_handoff_index_contract.json"

MUST_NOT_REQUIRED = {
    "execute_option",
    "merge_mainline",
    "promote",
    "sync_obsidian",
    "commit",
    "push",
    "install_dependencies",
    "start_background_service",
    "install_hooks",
    "use_mcp_write_tool",
    "write_reviewed_knowledge",
    "create_evidence_support",
    "create_action_basis",
    "start_future_slice_by_inference",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise TypeError(f"{path} is not an object")
    return payload


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def frontmatter_status(path: Path) -> str:
    for line in read_text(path).splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def status_starts(path: Path, prefix: str) -> bool:
    return frontmatter_status(path).lower().startswith(prefix.lower())


def exact_token_line(path: Path, tokens: set[str]) -> bool:
    for line in read_text(path).splitlines():
        normalized = line.strip().strip("`").strip(".").strip()
        if normalized in tokens:
            return True
    return False


def product_pass(path: Path) -> bool:
    return status_starts(path, "pass_product_grade") or exact_token_line(path, {"PASS_PRODUCT_GRADE"})


def reviewer_pass(path: Path) -> bool:
    return status_starts(path, "reviewer_pass") or exact_token_line(path, {"REVIEW_PASS_NO_BLOCKER", "REVIEW_PASS", "PASS_REVIEWER"})


def boundary_pass(path: Path) -> bool:
    return status_starts(path, "boundary_pass") or exact_token_line(path, {"PASS_BOUNDARY"})


def source_report(slice_info: dict) -> dict:
    slice_id = slice_info["slice_id"]
    root = SANDBOX_ROOT / slice_id
    final_gate = slice_info["final_gate_command"]
    return {
        "slice_id": slice_id,
        "label": slice_info["label"],
        "operator_use": slice_info["operator_use"],
        "root_exists": root.exists(),
        "product_pass": product_pass(root / "product-acceptance-report.md"),
        "reviewer_pass": reviewer_pass(root / "reviewer-report.md"),
        "boundary_pass": boundary_pass(root / "boundary-audit.md"),
        "verification_present": (root / "verification.md").exists(),
        "verification_status": frontmatter_status(root / "verification.md"),
        "next_step_status": frontmatter_status(root / "next-step.md"),
        "final_gate_command": final_gate,
        "final_gate_declared": "--final-gate" in final_gate and slice_id in final_gate,
        "must_not": slice_info["must_not"],
        "allowed_use": "operator_orientation_and_gate_routing_only",
        "not_authority": [
            "not_user_decision",
            "not_execution_authority",
            "not_mainline_approval",
            "not_promotion_approval",
            "not_obsidian_sync_approval",
            "not_reviewed_knowledge",
            "not_evidence_support",
            "not_action_basis",
        ],
    }


def run_latest_source_gate(contract: dict) -> dict:
    command = contract["latest_source_final_gate_command"]
    parts = [part.strip("\"'") for part in shlex.split(command, posix=False)]
    script_part = next((part for part in parts if part.endswith(".py")), "")
    if not script_part:
        return {"passed": False, "returncode": 1, "error": "no Python script found in latest_source_final_gate_command"}
    script = WORKSPACE / script_part.lstrip(".\\/")
    result = subprocess.run(
        [sys.executable, "-B", str(script), "--final-gate"],
        cwd=str(WORKSPACE),
        text=True,
        capture_output=True,
        check=False,
    )
    payload: dict = {"passed": False, "returncode": result.returncode}
    if result.stdout.strip():
        try:
            parsed = json.loads(result.stdout)
            if isinstance(parsed, dict):
                payload.update(parsed)
        except json.JSONDecodeError:
            payload["stdout"] = result.stdout
    if result.stderr.strip():
        payload["stderr"] = result.stderr
    return payload


def render_markdown(index: dict) -> str:
    lines = [
        "# User Decision Operator Handoff Index",
        "",
        "Sandbox-only operator index. It routes a follow-up agent to the right user-decision guard artifacts and gates. It is not a user decision, execution authority, mainline approval, promotion approval, Obsidian sync approval, reviewed knowledge, evidence support, or action basis.",
        "",
        f"- source chain ready: `{index['source_chain_ready']}`",
        f"- p2-59 self reports passed: `{index['self_report_gate']['overall_pass']}`",
        f"- handoff ready: `{index['handoff_ready']}`",
        "",
        "| Slice | Product | Reviewer | Boundary | Verification | Gate command | Use |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for entry in index["entries"]:
        lines.append(
            "| `{slice_id}` | {product} | {reviewer} | {boundary} | `{verification}` | `{gate}` | {use} |".format(
                slice_id=entry["slice_id"],
                product="PASS" if entry["product_pass"] else "FAIL",
                reviewer="PASS" if entry["reviewer_pass"] else "FAIL",
                boundary="PASS" if entry["boundary_pass"] else "FAIL",
                verification=entry["verification_status"],
                gate=entry["final_gate_command"],
                use=entry["operator_use"],
            )
        )
    lines.extend(
        [
            "",
            "## Recommended Operator Route",
            "",
            f"1. Run latest gate: `{index['latest_source_final_gate_command']}`",
            "2. Read this index for routing only.",
            "3. Ask the user for separate scope before any mainline, sync, promotion, commit, push, dependency, service, hook, MCP-write, reviewed-knowledge, evidence-support, or action-basis step.",
            "",
            "## must_not",
            "",
        ]
    )
    lines.extend(f"- `{item}`" for item in index["must_not"])
    return "\n".join(lines)


def run_index() -> dict:
    contract = load_json(CONTRACT_PATH)
    entries = [source_report(item) for item in contract["source_slices"]]
    source_chain_ready = all(
        entry["root_exists"]
        and entry["product_pass"]
        and entry["reviewer_pass"]
        and entry["boundary_pass"]
        and entry["verification_present"]
        and entry["final_gate_declared"]
        and MUST_NOT_REQUIRED <= set(entry["must_not"])
        for entry in entries
    )
    latest_gate = run_latest_source_gate(contract)
    self_report_gate = {
        "reviewer_pass": reviewer_pass(ROOT / "reviewer-report.md"),
        "boundary_pass": boundary_pass(ROOT / "boundary-audit.md"),
        "product_pass": product_pass(ROOT / "product-acceptance-report.md"),
        "next_step_pass": frontmatter_status(ROOT / "next-step.md") == "pass_product_grade_pending_next_slice",
    }
    self_report_gate["overall_pass"] = all(self_report_gate.values())
    index = {
        "record_kind": "sandbox_user_decision_operator_handoff_index",
        "slice_id": contract["slice_id"],
        "source_slice_ids": [item["slice_id"] for item in contract["source_slices"]],
        "truth_boundary": "operator_handoff_index_not_user_decision_or_execution_authority",
        "entries": entries,
        "entry_count": len(entries),
        "latest_source_final_gate_command": contract["latest_source_final_gate_command"],
        "latest_source_final_gate_passed": latest_gate.get("passed") is True,
        "latest_source_final_gate_summary": latest_gate.get("summary", {}),
        "source_chain_ready": source_chain_ready and latest_gate.get("passed") is True,
        "self_report_gate": self_report_gate,
        "automatic_execution": False,
        "mainline_ready": False,
        "promotion_ready": False,
        "action_basis_ready": False,
        "operator_next_action": "read_index_and_run_latest_gate_only_until_p2_59_product_pass",
        "must_not": contract["output_contract"]["must_not"],
        "required_non_claims": contract["required_non_claims"],
    }
    index["handoff_ready"] = (
        index["source_chain_ready"]
        and index["self_report_gate"]["overall_pass"]
        and len(entries) == contract["expected_entry_count"]
        and MUST_NOT_REQUIRED <= set(index["must_not"])
    )
    index["handoff_markdown"] = render_markdown(index)
    return index


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args()
    index = run_index()
    if args.markdown:
        print(index["handoff_markdown"])
    else:
        print(json.dumps(index, ensure_ascii=False, indent=2))
    return 0 if index["handoff_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
