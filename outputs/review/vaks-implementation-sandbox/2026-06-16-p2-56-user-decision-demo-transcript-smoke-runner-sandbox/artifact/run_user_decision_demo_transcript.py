from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
CONTRACT_PATH = ROOT / "artifact" / "user_decision_demo_transcript_contract.json"
SIMULATOR_PATH = (
    WORKSPACE
    / "outputs"
    / "review"
    / "vaks-implementation-sandbox"
    / "2026-06-16-p2-55-user-decision-e2e-dry-run-simulator-sandbox"
    / "artifact"
    / "simulate_user_decision_dry_run.py"
)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def import_simulator():
    spec = importlib.util.spec_from_file_location("p2_55_simulator", SIMULATOR_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-55 simulator")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render_markdown(rows: list[dict], must_not: list[str]) -> str:
    lines = [
        "# User Decision Demo Transcript",
        "",
        "This transcript is dry-run only. It is not a user decision and it is not execution authority.",
        "",
        "| Scenario | User input | Classifier case | Reply id | Safe reply |",
        "| --- | --- | --- | --- | --- |",
    ]
    for row in rows:
        display_input = row["input_text"] if row["input_text"] else "(empty)"
        reply = row["reply"].replace("|", "/")
        lines.append(
            f"| `{row['scenario_id']}` | `{display_input}` | `{row['classifier_case_id']}` | `{row['reply_id']}` | {reply} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "不执行任何选项；sandbox 演示不等于合并、promotion、sync、commit、push、reviewed knowledge、evidence support 或 action basis。",
            "",
            "## must_not",
            "",
        ]
    )
    lines.extend(f"- `{item}`" for item in must_not)
    return "\n".join(lines)


def run_demo() -> dict:
    contract = load_json(CONTRACT_PATH)
    simulator = import_simulator()
    rows = []
    for scenario in contract["demo_scenarios"]:
        output = simulator.simulate(scenario["input_text"])
        rows.append(
            {
                "scenario_id": scenario["scenario_id"],
                "input_text": scenario["input_text"],
                "expected_case_id": scenario["expected_case_id"],
                "expected_reply_id": scenario["expected_reply_id"],
                "classifier_case_id": output["classifier"]["case_id"],
                "reply_id": output["renderer"]["reply_id"],
                "reply": output["renderer"]["reply"],
                "automatic_execution": output["automatic_execution"],
                "decision_collected": output["decision_collected"],
                "ready_to_execute": output["ready_to_execute"],
                "must_not": output["must_not"],
            }
        )
    must_not = contract["output_contract"]["must_not"]
    return {
        "record_kind": "sandbox_user_decision_demo_transcript_result",
        "slice_id": contract["slice_id"],
        "source_slice_id": contract["source_slice_id"],
        "truth_boundary": "demo_transcript_not_user_decision_or_execution_authority",
        "automatic_execution": False,
        "decision_collected": False,
        "ready_to_execute": False,
        "mainline_ready": False,
        "promotion_ready": False,
        "action_basis_ready": False,
        "scenario_count": len(rows),
        "rows": rows,
        "must_not": must_not,
        "transcript_markdown": render_markdown(rows, must_not),
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser()
    parser.add_argument("--markdown", action="store_true")
    args = parser.parse_args()
    result = run_demo()
    if args.markdown:
        print(result["transcript_markdown"])
    else:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
