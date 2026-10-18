from __future__ import annotations

import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

from silky_workbench_builder import PROTOTYPE_VAULT, SLICE_ROOT, write_package
from silky_workbench_validator import validate_config_file, validate_generated_vault


def _read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _hash_formal_vault_sample(formal_vault: Path) -> dict[str, Any]:
    if not formal_vault.exists():
        return {"exists": False, "file_count": 0, "sample20_hash": None}
    files = sorted([item for item in formal_vault.rglob("*") if item.is_file()], key=lambda item: str(item))
    sample_hashes = []
    for item in files[:20]:
        sample_hashes.append(hashlib.sha256(item.read_bytes()).hexdigest())
    return {
        "exists": True,
        "file_count": len(files),
        "sample20_hash": hashlib.sha256("".join(sample_hashes).encode("utf-8")).hexdigest().upper(),
    }


def _run_git_status_slice() -> list[str]:
    rel = SLICE_ROOT.as_posix()
    proc = subprocess.run(
        ["git", "status", "--short", "--untracked-files=all", "--", rel],
        cwd=SLICE_ROOT.parents[3],
        capture_output=True,
        text=True,
        check=False,
    )
    return [line for line in proc.stdout.splitlines() if line.strip()]


def _validate_links_and_search(vault_root: Path) -> dict[str, Any]:
    md_files = list(vault_root.rglob("*.md"))
    text = "\n".join(path.read_text(encoding="utf-8-sig") for path in md_files)
    search_targets = {
        "PASS_PRODUCT_GRADE": 20,
        "not action basis": 20,
        "not evidence support": 20,
        "reviewed knowledge": 20,
        "dirty state": 5,
        "review due": 5,
        "hash receipt": 5,
        "next safe step": 20,
        "no sync": 20,
        "no commit": 20,
        "no push": 20,
    }
    hits = {target: text.lower().count(target.lower()) for target in search_targets}
    failures = [target for target, minimum in search_targets.items() if hits[target] < minimum]
    return {"hits": hits, "search_failures": failures}


def _validate_cockpit(vault_root: Path) -> dict[str, Any]:
    html = vault_root / "cockpit.html"
    text = html.read_text(encoding="utf-8-sig")
    required = [
        'data-sandbox-only="true"',
        'id="quickSearch"',
        'id="laneTabs"',
        'id="boundaryRail"',
        'id="sliceGrid"',
        "VAKS Silky Workbench",
        "not action basis",
        "not evidence support",
    ]
    missing = [item for item in required if item not in text]
    return {"missing": missing, "bytes": len(text.encode("utf-8"))}


def _copy_to_temp_and_smoke(vault_root: Path) -> dict[str, Any]:
    temp_root = Path(tempfile.mkdtemp(prefix="vaks-silky-workbench-smoke-"))
    copied = temp_root / "vault"
    shutil.copytree(vault_root, copied)
    result = {
        "temp_root": str(temp_root),
        "copied_files": len([item for item in copied.rglob("*") if item.is_file()]),
        "deleted": False,
    }
    shutil.rmtree(temp_root)
    result["deleted"] = not temp_root.exists()
    return result


def _validate_failure_cases(oracle_path: Path) -> tuple[int, list[dict[str, Any]]]:
    oracle = _read_json(oracle_path)
    failures = []
    for name, expected in sorted(oracle.items()):
        path = SLICE_ROOT / "failure-cases" / name
        result = validate_config_file(path, SLICE_ROOT)
        codes = {issue["code"] for issue in result["issues"]}
        expected_codes = set(expected["expected_codes"])
        if result["valid"] or not expected_codes.issubset(codes):
            failures.append({"case": name, "expected": sorted(expected_codes), "actual": sorted(codes)})
    return len(oracle), failures


def main() -> int:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true", help="rebuild docs, fixtures, and prototype before validation")
    parser.add_argument("--temp-smoke", action="store_true", help="copy generated vault to a temporary directory and delete it")
    parser.add_argument("--check-formal-vault", action="store_true", help="read formal vault file count/hash before and after validation")
    parser.add_argument("--formal-vault-path", type=Path, help="formal vault path to audit when --check-formal-vault is set")
    args = parser.parse_args()

    if args.check_formal_vault and args.formal_vault_path is None:
        raise SystemExit("--formal-vault-path is required with --check-formal-vault")

    formal_before = _hash_formal_vault_sample(args.formal_vault_path) if args.check_formal_vault else {"checked": False}
    if args.rebuild:
        build_summary = write_package()
    else:
        build_summary = {
            "slice_id": SLICE_ROOT.name,
            "prototype_vault": str(PROTOTYPE_VAULT.relative_to(SLICE_ROOT)),
            "slice_cards": len(list((PROTOTYPE_VAULT / "Cards").glob("*.md"))) if (PROTOTYPE_VAULT / "Cards").exists() else 0,
            "lanes": None,
        }

    positive_results = []
    for path in sorted((SLICE_ROOT / "fixtures").glob("*.json")):
        result = validate_config_file(path, SLICE_ROOT)
        positive_results.append({"path": str(path.relative_to(SLICE_ROOT)), "valid": result["valid"], "issues": result["issues"]})

    failure_count, failure_mismatches = _validate_failure_cases(SLICE_ROOT / "artifact" / "failure-case-oracle.json")
    vault_issues = validate_generated_vault(PROTOTYPE_VAULT)
    search_result = _validate_links_and_search(PROTOTYPE_VAULT)
    cockpit = _validate_cockpit(PROTOTYPE_VAULT)
    temp_smoke = _copy_to_temp_and_smoke(PROTOTYPE_VAULT) if args.temp_smoke else {"checked": False}
    formal_after = _hash_formal_vault_sample(args.formal_vault_path) if args.check_formal_vault else {"checked": False}
    git_status = _run_git_status_slice()

    failures = []
    if any(not item["valid"] for item in positive_results):
        failures.append("positive_fixture_failed")
    if failure_mismatches:
        failures.append("failure_case_oracle_mismatch")
    if vault_issues:
        failures.append("generated_vault_invalid")
    if search_result["search_failures"]:
        failures.append("search_targets_missing")
    if cockpit["missing"]:
        failures.append("cockpit_markers_missing")
    if args.temp_smoke and not temp_smoke["deleted"]:
        failures.append("temp_smoke_not_deleted")
    if args.check_formal_vault and formal_before != formal_after:
        failures.append("formal_vault_changed")

    summary = {
        "slice_id": build_summary["slice_id"],
        "passed": not failures,
        "failures": failures,
        "positive_fixtures": len(positive_results),
        "failure_cases": failure_count,
        "failure_case_mismatches": failure_mismatches,
        "generated_vault_issues": vault_issues,
        "search_result": search_result,
        "cockpit": cockpit,
        "temp_smoke": temp_smoke,
        "formal_vault_before": formal_before,
        "formal_vault_after": formal_after,
        "git_status_scoped_lines": len(git_status),
        "git_status_scoped_sample": git_status[:5],
        "prototype_vault": build_summary["prototype_vault"],
        "slice_cards": build_summary["slice_cards"],
        "lanes": build_summary["lanes"],
    }
    print(json.dumps(summary, indent=2, ensure_ascii=False))
    return 0 if summary["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
