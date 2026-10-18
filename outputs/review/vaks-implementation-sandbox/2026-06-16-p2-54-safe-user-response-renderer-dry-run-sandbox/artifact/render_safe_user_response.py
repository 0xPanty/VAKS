from __future__ import annotations

import argparse
import importlib.util
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
CONTRACT_PATH = ROOT / "artifact" / "safe_user_response_renderer_contract.json"
CLASSIFIER_PATH = (
    WORKSPACE
    / "outputs"
    / "review"
    / "vaks-implementation-sandbox"
    / "2026-06-16-p2-53-user-response-classifier-dry-run-sandbox"
    / "artifact"
    / "classify_user_response_dry_run.py"
)


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def import_classifier():
    spec = importlib.util.spec_from_file_location("p2_53_classifier", CLASSIFIER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-53 classifier")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render(text: str | None) -> dict:
    contract = load_json(CONTRACT_PATH)
    classifier = import_classifier()
    raw_text = "" if text is None else text
    if raw_text == "__synthetic_unknown_case__":
        classification = {
            "case_id": "synthetic_unknown_case",
            "safe_next_step": "synthetic_unknown_next_step",
        }
    else:
        classification = classifier.classify(raw_text)
    case_id = classification["case_id"]
    policy_by_case = {item["case_id"]: item for item in contract["render_policy"]}
    policy = policy_by_case.get(case_id, policy_by_case["unknown_case_fallback"])
    return {
        "record_kind": "sandbox_safe_user_response_renderer_result",
        "slice_id": contract["slice_id"],
        "source_slice_id": contract["source_slice_id"],
        "truth_boundary": "dry_run_reply_not_user_decision_or_execution_authority",
        "input_text": raw_text,
        "classifier_case_id": case_id,
        "classifier_safe_next_step": classification["safe_next_step"],
        "reply_id": policy["reply_id"],
        "reply": policy["reply"],
        "next_step": policy["next_step"],
        "automatic_execution": False,
        "must_not": contract["output_contract"]["must_not"],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default="")
    args = parser.parse_args()
    print(json.dumps(render(args.text), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
