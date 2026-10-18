from __future__ import annotations

import copy
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
VALIDATOR_PATH = ROOT / "artifact" / "product_workflow_validator.py"
ORACLE_PATH = ROOT / "artifact" / "failure-case-oracle.json"


def _load_validator():
    spec = importlib.util.spec_from_file_location("product_workflow_validator", VALIDATOR_PATH)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def _load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def _set_nested(container: Any, path: str, value: Any) -> None:
    parts = [part for part in path.strip("/").split("/") if part]
    current = container
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    last = parts[-1]
    if isinstance(current, list):
        current[int(last)] = value
    else:
        current[last] = value


def _delete_nested(container: Any, path: str) -> None:
    parts = [part for part in path.strip("/").split("/") if part]
    current = container
    for part in parts[:-1]:
        current = current[int(part)] if isinstance(current, list) else current[part]
    last = parts[-1]
    if isinstance(current, list):
        del current[int(last)]
    else:
        current.pop(last, None)


def _apply_mutation(obj: dict[str, Any], mutation: dict[str, Any]) -> None:
    op = mutation["op"]
    if op == "set":
        _set_nested(obj, mutation["path"], mutation["value"])
    elif op == "delete":
        _delete_nested(obj, mutation["path"])
    elif op == "remove_step":
        sid = mutation["id"]
        obj["steps"] = [step for step in obj.get("steps", []) if step.get("id") != sid]
    elif op == "swap_steps":
        a, b = mutation["a"], mutation["b"]
        steps = obj["steps"]
        steps[a], steps[b] = steps[b], steps[a]
    else:
        raise ValueError(f"unknown mutation op: {op}")


def _materialize_case(path: Path) -> dict[str, Any]:
    case = _load_json(path)
    base_path = ROOT / case.get("base_fixture", "fixtures/valid-product-workflow.json")
    obj = copy.deepcopy(_load_json(base_path))
    for mutation in case.get("mutations", []):
        _apply_mutation(obj, mutation)
    return obj


def _run_one(validator: Any, path: Path, expected: dict[str, Any] | None) -> dict[str, Any]:
    if expected is None:
        return {
            "path": str(path.relative_to(ROOT)),
            "valid": False,
            "issue_codes": ["WF_VERIFIER_ERROR"],
            "expected_valid": False,
            "expected_codes": ["WF_VERIFIER_ERROR"],
            "allowed_extra_codes": [],
            "problems": ["missing oracle entry"],
        }
    if "failure-cases" in path.parts:
        result = validator.validate_workflow(_materialize_case(path))
    else:
        result = validator.validate_path(path)
    issue_codes = sorted({issue["code"] for issue in result["issues"]})
    expected_codes = sorted(expected.get("expected_codes", []))
    allowed_extra = sorted(expected.get("allowed_extra_codes", []))
    problems = []
    if result["valid"] != expected["expected_valid"]:
        problems.append(f"expected valid={expected['expected_valid']}, got {result['valid']}")
    missing = sorted(set(expected_codes).difference(issue_codes))
    unexpected = sorted(set(issue_codes).difference(expected_codes).difference(allowed_extra))
    if missing:
        problems.append("missing codes: " + ", ".join(missing))
    if unexpected:
        problems.append("unexpected codes: " + ", ".join(unexpected))
    return {
        "path": str(path.relative_to(ROOT)),
        "valid": result["valid"],
        "issue_codes": issue_codes,
        "expected_valid": expected["expected_valid"],
        "expected_codes": expected_codes,
        "allowed_extra_codes": allowed_extra,
        "problems": problems,
    }


def main() -> int:
    validator = _load_validator()
    oracle = _load_json(ORACLE_PATH)
    cases = []
    cases.extend(sorted((ROOT / "fixtures").glob("*.json")))
    prototypes = sorted((ROOT / "prototype").glob("*.json"))
    cases.extend(prototypes)
    cases.extend(sorted((ROOT / "failure-cases").glob("*.json")))
    results = []
    seen = set()
    for path in cases:
        rel = str(path.relative_to(ROOT)).replace("\\", "/")
        seen.add(rel)
        results.append(_run_one(validator, path, oracle.get(rel)))
    for rel in sorted(set(oracle).difference(seen)):
        results.append({"path": rel, "valid": False, "issue_codes": ["WF_VERIFIER_ERROR"], "expected_valid": oracle[rel].get("expected_valid"), "expected_codes": oracle[rel].get("expected_codes", []), "allowed_extra_codes": oracle[rel].get("allowed_extra_codes", []), "problems": ["oracle entry has no matching case file"]})
    failures = [result for result in results if result["problems"]]
    summary = {
        "slice_id": "2026-06-15-p2-20-product-workflow-prototype",
        "positive_fixtures": len(list((ROOT / "fixtures").glob("*.json"))),
        "prototype_artifacts": len(prototypes),
        "failure_cases": len(list((ROOT / "failure-cases").glob("*.json"))),
        "passed": not failures and len(prototypes) > 0,
        "failures": failures,
        "non_claims": {
            "suite_pass_not_product_build": True,
            "suite_pass_not_reviewed_knowledge": True,
            "suite_pass_not_evidence_support": True,
            "suite_pass_not_action_basis": True,
            "suite_pass_not_mainline_readiness": True,
        },
        "results": results,
    }
    if not prototypes:
        summary["passed"] = False
        summary["failures"].append({"path": "prototype/", "problems": ["missing prototype artifact"]})
    print(json.dumps(summary, indent=2, sort_keys=True))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
