import csv
import json
import re
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
PACKAGE_PATH = SANDBOX_DIR / "PHASE_B_INTEGRATION_READINESS_PACKAGE.md"
REPORT_PATH = SANDBOX_DIR / "PHASE_B_INTEGRATION_READINESS_CHECK.md"
JSON_REPORT_PATH = RESULTS_DIR / "phase_b_integration_readiness_check.json"

SKELETON_MODE = "vaks_b_adapter_skeleton"

MAIN_THRESHOLDS = {
    "primary": {"queries": "30", "hit_at_5": "30/30", "hit_at_10": "30/30", "mrr": 1.0},
    "full": {"queries": "30", "hit_at_5": "30/30", "hit_at_10": "30/30", "mrr": 1.0},
}

HOLDOUT_THRESHOLDS = {
    "primary": {"queries": "15", "hit_at_5": "12/15", "hit_at_10": "13/15", "mrr": 0.7811},
    "full": {"queries": "15", "hit_at_5": "13/15", "hit_at_10": "13/15", "mrr": 0.7591},
}

REQUIRED_PACKAGE_STRINGS = [
    "not ready for mainline adoption",
    "contract-passing adapter skeleton",
    "tools/vaks_phase_b_adapter.py",
    "VaksPhaseBAdapter",
    "chunk_manifest_rows",
    "adapter.query",
    "read_only_markdown_yaml_vault",
    "expected_terms is evaluation scaffolding",
    "Required Result Fields",
    "indexed_source_hash",
    "retrieval_policy",
    "action_basis_allowed",
    "authority_bucket",
    "Insertion Point",
    "reviewed write path",
    "truth-confidence updates",
    "action-gate approval",
    "Skills / MCP write tools",
    "subagent production evidence",
    "Failure Modes",
    "Rollback Path",
    "No C-lite, no Skills, no MCP writes",
]

REQUIRED_ARTIFACTS = [
    "tools/vaks_phase_b_adapter.py",
    "tools/run_phase_b_pressure.py",
    "tools/validate_phase_b_adapter_contract.py",
    "results/phase_b_summary.csv",
    "results/phase_b_holdout_summary.csv",
    "results/phase_b_adapter_contract_test.json",
    "results/phase_b_skeleton_main_primary_chunk_manifest.jsonl",
    "results/phase_b_skeleton_main_full_chunk_manifest.jsonl",
    "results/phase_b_skeleton_main_primary_retrieval_receipts.jsonl",
    "results/phase_b_skeleton_main_full_retrieval_receipts.jsonl",
    "results/phase_b_skeleton_holdout_primary_retrieval_receipts.jsonl",
    "results/phase_b_skeleton_holdout_full_retrieval_receipts.jsonl",
]


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def load_summary(path: Path) -> dict[tuple[str, str], dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        rows = {}
        for raw_row in reader:
            row = {(key or "").strip().lstrip("\ufeff"): value for key, value in raw_row.items()}
            rows[(row["mode"], row["corpus"])] = row
        return rows


def validate_summary_rows(
    errors: list[dict],
    summary_path: Path,
    thresholds: dict[str, dict[str, object]],
    label: str,
) -> list[dict]:
    summary = load_summary(summary_path)
    rows = []
    for corpus, expected in thresholds.items():
        row = summary.get((SKELETON_MODE, corpus))
        if row is None:
            add_error(errors, "missing_metric_row", f"{label}:{corpus}:{SKELETON_MODE}")
            continue
        rows.append({"set": label, "corpus": corpus, **row})
        for key in ["queries", "hit_at_5", "hit_at_10"]:
            if row.get(key) != expected[key]:
                add_error(errors, "metric_value_mismatch", f"{label}:{corpus}:{key} {row.get(key)} != {expected[key]}")
        for key in ["action_leakage_rate", "forbidden_top1_rate", "cross_bucket_violation_rate"]:
            if float(row.get(key, "1")) != 0.0:
                add_error(errors, "governance_regression", f"{label}:{corpus}:{key}={row.get(key)}")
        for key in ["clickback_coverage", "hash_coverage"]:
            if float(row.get(key, "0")) < 1.0:
                add_error(errors, "coverage_regression", f"{label}:{corpus}:{key}={row.get(key)}")
        if float(row.get("mrr", "0")) + 0.00005 < float(expected["mrr"]):
            add_error(errors, "mrr_below_floor", f"{label}:{corpus}:mrr {row.get('mrr')} < {expected['mrr']}")
    return rows


def validate_contract(errors: list[dict]) -> dict:
    path = RESULTS_DIR / "phase_b_adapter_contract_test.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("contract_status") != "pass":
        add_error(errors, "contract_not_pass", str(data.get("contract_status")))
    if int(data.get("error_count", -1)) != 0:
        add_error(errors, "contract_errors_present", str(data.get("error_count")))
    for section in data.get("sections", []):
        if int(section.get("errors", -1)) != 0:
            add_error(errors, "contract_section_errors", f"{section.get('section')}={section.get('errors')}")
    return data


def validate_package(errors: list[dict]) -> dict:
    text = PACKAGE_PATH.read_text(encoding="utf-8")
    lower = text.lower()
    for needle in REQUIRED_PACKAGE_STRINGS:
        if needle.lower() not in lower:
            add_error(errors, "package_missing_required_string", needle)

    headings = re.findall(r"^##\s+(.+)$", text, flags=re.MULTILINE)
    required_headings = {
        "Decision",
        "Compared Against Previous Version",
        "Adapter API Shape",
        "Inputs",
        "Outputs",
        "Required Result Fields",
        "Insertion Point",
        "Failure Modes",
        "Rollback Path",
        "Required Gates Before Mainline Discussion",
        "Next Candidate Step",
    }
    missing_headings = sorted(required_headings - set(headings))
    if missing_headings:
        add_error(errors, "package_missing_headings", ",".join(missing_headings))
    return {"headings": headings, "bytes": PACKAGE_PATH.stat().st_size}


def validate_artifacts(errors: list[dict]) -> list[dict]:
    artifacts = []
    for rel in REQUIRED_ARTIFACTS:
        path = SANDBOX_DIR / rel
        exists = path.exists()
        artifacts.append({"path": rel, "exists": exists, "bytes": path.stat().st_size if exists else 0})
        if not exists:
            add_error(errors, "missing_required_artifact", rel)
        elif path.stat().st_size == 0:
            add_error(errors, "empty_required_artifact", rel)
    return artifacts


def write_reports(result: dict) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    JSON_REPORT_PATH.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = [
        "---",
        "record_kind: sandbox_integration_readiness_check",
        f"status: {result['readiness_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: diagnostic_not_mainline_decision",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Integration Readiness Check",
        "",
        "## Result",
        "",
        "```text",
        f"readiness status: {result['readiness_status']}",
        f"error count: {result['error_count']}",
        "```",
        "",
        "## Compared Floor",
        "",
        "```text",
        "previous version: contract-passing adapter skeleton",
        "required: tie or beat skeleton metrics, keep zero leakage, keep contract pass",
        "```",
        "",
        "## Metrics Checked",
        "",
        "| Set | Corpus | hit@5 | hit@10 | MRR | Leakage | Forbidden top1 | Cross-bucket violation |",
        "|---|---|---:|---:|---:|---:|---:|---:|",
    ]
    for row in result["metrics"]:
        lines.append(
            "| {set} | {corpus} | {hit_at_5} | {hit_at_10} | {mrr} | {action_leakage_rate} | {forbidden_top1_rate} | {cross_bucket_violation_rate} |".format(
                **row
            )
        )
    lines.extend(
        [
            "",
            "## Contract Checked",
            "",
            "```text",
            f"contract status: {result['contract'].get('contract_status')}",
            f"contract errors: {result['contract'].get('error_count')}",
            "```",
            "",
            "## Package Coverage",
            "",
            "```text",
            f"required headings checked: {len(result['package'].get('headings', []))}",
            f"required artifacts checked: {len(result['artifacts'])}",
            "```",
            "",
            "## Errors",
            "",
        ]
    )
    if result["errors"]:
        for error in result["errors"]:
            lines.append(f"- {error['code']}: {error['detail']}")
    else:
        lines.append("- none")
    lines.append("")
    REPORT_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    errors: list[dict] = []
    artifacts = validate_artifacts(errors)
    package = validate_package(errors)
    contract = validate_contract(errors)
    metrics = []
    metrics.extend(validate_summary_rows(errors, RESULTS_DIR / "phase_b_summary.csv", MAIN_THRESHOLDS, "main"))
    metrics.extend(validate_summary_rows(errors, RESULTS_DIR / "phase_b_holdout_summary.csv", HOLDOUT_THRESHOLDS, "holdout"))

    result = {
        "readiness_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "metrics": metrics,
        "contract": {"contract_status": contract.get("contract_status"), "error_count": contract.get("error_count")},
        "package": package,
        "artifacts": artifacts,
    }
    write_reports(result)
    print(f"readiness status: {result['readiness_status']}")
    print(f"error count: {result['error_count']}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
