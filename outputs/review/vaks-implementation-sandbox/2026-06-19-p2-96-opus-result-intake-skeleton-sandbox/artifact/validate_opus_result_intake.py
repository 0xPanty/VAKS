from __future__ import annotations

import argparse
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-96-opus-result-intake-skeleton-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SLICE_DIR = ROOT / "outputs/review/vaks-implementation-sandbox" / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
SCHEMA_JSON = ARTIFACT_DIR / "opus-result-intake-schema.json"


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def validate_record(record: dict, schema: dict) -> list[str]:
    failures: list[str] = []
    token = record.get("raw_conclusion_token")
    if token not in schema["allowed_conclusion_tokens"]:
        failures.append(f"invalid_conclusion_token:{token}")
    for key in schema["required_fields_when_result_exists"]:
        if key not in record:
            failures.append(f"missing_required_field:{key}")
    if not isinstance(record.get("reviewed_evidence", []), list) or not record.get("reviewed_evidence"):
        failures.append("reviewed_evidence_empty_or_not_list")
    if record.get("boundary_verdict") != "not_mainline_approval":
        failures.append(f"invalid_boundary_verdict:{record.get('boundary_verdict')}")
    forbidden_true = [
        "mainline_approval",
        "reviewed_knowledge",
        "evidence_support",
        "action_basis",
        "commit_push_sync",
    ]
    for key in forbidden_true:
        if record.get(key) is True:
            failures.append(f"forbidden_authority_true:{key}")
    return failures


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--record", required=True)
    args = parser.parse_args()
    schema = load_json(SCHEMA_JSON)
    record = load_json(Path(args.record))
    failures = validate_record(record, schema)
    result = {"passed": not failures, "failures": failures, "token": record.get("raw_conclusion_token")}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()

