from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
CONTRACT_PATH = ROOT / "artifact" / "user_decision_e2e_simulator_contract.json"
CLASSIFIER_PATH = (
    WORKSPACE
    / "outputs"
    / "review"
    / "vaks-implementation-sandbox"
    / "2026-06-16-p2-53-user-response-classifier-dry-run-sandbox"
    / "artifact"
    / "classify_user_response_dry_run.py"
)
RENDERER_PATH = (
    WORKSPACE
    / "outputs"
    / "review"
    / "vaks-implementation-sandbox"
    / "2026-06-16-p2-54-safe-user-response-renderer-dry-run-sandbox"
    / "artifact"
    / "render_safe_user_response.py"
)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def import_module(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot load {name}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def simulate(text: str | None) -> dict:
    contract = load_json(CONTRACT_PATH)
    classifier = import_module("p2_53_classifier", CLASSIFIER_PATH)
    renderer = import_module("p2_54_renderer", RENDERER_PATH)
    raw_text = "" if text is None else text
    if raw_text == "__synthetic_unknown_case__":
        classification = {
            "case_id": "synthetic_unknown_case",
            "safe_next_step": "synthetic_unknown_next_step",
            "automatic_execution": False,
        }
    else:
        classification = classifier.classify(raw_text)
    rendered = renderer.render(raw_text)
    classifier_case = classification["case_id"]
    renderer_case = rendered["classifier_case_id"]
    renderer_reply_id = rendered["reply_id"]
    unknown_fallback = classifier_case not in {
        "no_reply",
        "explicit_A",
        "explicit_B",
        "explicit_C",
        "explicit_D",
        "ambiguous_reply",
        "multiple_options",
        "approval_with_execution_words",
    } and renderer_reply_id == "stop_for_unknown_classifier_case"
    case_consistent = classifier_case == renderer_case or unknown_fallback
    must_not = contract["simulation_output_contract"]["must_not"]
    return {
        "record_kind": "sandbox_user_decision_e2e_dry_run_result",
        "slice_id": contract["slice_id"],
        "source_slice_id": contract["source_slice_id"],
        "truth_boundary": "e2e_dry_run_result_not_user_decision_or_execution_authority",
        "input_text": raw_text,
        "classifier": {
            "case_id": classifier_case,
            "safe_next_step": classification["safe_next_step"],
            "automatic_execution": classification["automatic_execution"],
        },
        "renderer": {
            "classifier_case_id": renderer_case,
            "reply_id": renderer_reply_id,
            "reply": rendered["reply"],
            "next_step": rendered["next_step"],
            "automatic_execution": rendered["automatic_execution"],
        },
        "consistency": {
            "case_consistent": case_consistent,
            "unknown_fallback": unknown_fallback,
            "reply_present": bool(rendered["reply"]),
        },
        "automatic_execution": False,
        "decision_collected": False,
        "ready_to_execute": False,
        "mainline_ready": False,
        "promotion_ready": False,
        "action_basis_ready": False,
        "must_not": must_not,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default="")
    args = parser.parse_args()
    print(json.dumps(simulate(args.text), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
