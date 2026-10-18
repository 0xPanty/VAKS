from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT_PATH = ROOT / "artifact" / "user_response_classifier_contract.json"

MUST_NOT = [
    "execute_option",
    "merge_mainline",
    "promote",
    "sync_obsidian",
    "commit",
    "push",
    "write_reviewed_knowledge",
    "create_evidence_support",
    "create_action_basis",
]


def load_contract() -> dict:
    with CONTRACT_PATH.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def normalize(text: str | None) -> str:
    if text is None:
        return ""
    lowered = text.strip().lower()
    lowered = re.sub(r"\s+", " ", lowered)
    return lowered


def token_present(normalized: str, token: str) -> bool:
    token = token.lower()
    if re.fullmatch(r"[abcd]", token):
        return bool(re.search(rf"(?<![a-z0-9]){re.escape(token)}(?![a-z0-9])", normalized))
    return token in normalized


def detect_options(normalized: str, contract: dict) -> list[str]:
    option_tokens = contract["token_policy"]["option_tokens"]
    detected: list[str] = []
    for option in ("A", "B", "C", "D"):
        tokens = option_tokens[option]
        if any(token_present(normalized, token) for token in tokens):
            detected.append(option)
    return detected


def detect_execution_tokens(normalized: str, contract: dict) -> list[str]:
    tokens = contract["token_policy"]["execution_boundary_tokens"]
    found = [token for token in tokens if token_present(normalized, token)]
    return sorted(set(found), key=found.index)


def policy_by_case(contract: dict) -> dict[str, dict]:
    return {item["case_id"]: item for item in contract["response_policy"]}


def choose_case(normalized: str, detected_options: list[str], execution_tokens: list[str]) -> str:
    if not normalized:
        return "no_reply"
    if execution_tokens:
        return "approval_with_execution_words"
    if len(detected_options) > 1:
        return "multiple_options"
    if len(detected_options) == 1:
        return {
            "A": "explicit_A",
            "B": "explicit_B",
            "C": "explicit_C",
            "D": "explicit_D",
        }[detected_options[0]]
    return "ambiguous_reply"


def classify(text: str | None) -> dict:
    contract = load_contract()
    normalized = normalize(text)
    detected_options = detect_options(normalized, contract)
    execution_tokens = detect_execution_tokens(normalized, contract)
    case_id = choose_case(normalized, detected_options, execution_tokens)
    policy = policy_by_case(contract)[case_id]
    return {
        "record_kind": "sandbox_user_response_classifier_dry_run_result",
        "slice_id": contract["slice_id"],
        "source_slice_id": contract["source_slice_id"],
        "truth_boundary": "dry_run_result_not_user_decision_or_execution_authority",
        "input_text": "" if text is None else text,
        "normalized_text": normalized,
        "detected_options": detected_options,
        "detected_execution_tokens": execution_tokens,
        "case_id": case_id,
        "result": policy["result"],
        "safe_next_step": policy["safe_next_step"],
        "automatic_execution": False,
        "requires_clarification": policy["requires_clarification"],
        "requires_new_scope": policy["requires_new_scope"],
        "requires_separate_user_approval": policy["requires_separate_user_approval"],
        "requires_explicit_allowed_paths": policy["requires_explicit_allowed_paths"],
        "must_not": MUST_NOT,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--text", default="")
    args = parser.parse_args()
    print(json.dumps(classify(args.text), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
