import csv
import json
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
QUERY_FILE = SANDBOX_DIR / "queries_phase_b_adversarial.jsonl"
AUDIT_JSON = RESULTS_DIR / "phase_b_p1_adversarial_audit.json"
COMBINED_SUMMARY = RESULTS_DIR / "phase_b_p1_adversarial_combined_summary.csv"
REPORT_MD = SANDBOX_DIR / "PHASE_B_P1_ADVERSARIAL_AUDIT_REPORT.md"
CHECK_JSON = RESULTS_DIR / "phase_b_p1_adversarial_audit_check.json"
CHECK_MD = SANDBOX_DIR / "PHASE_B_P1_ADVERSARIAL_AUDIT_CHECK.md"


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def count_jsonl(path: Path) -> int:
    return sum(1 for line in path.read_text(encoding="utf-8").splitlines() if line.strip())


def write_md(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_p1_adversarial_audit_check",
        f"status: {result['p1_adversarial_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: fresh_adversarial_not_external_blind",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B P1 Adversarial Audit Check",
        "",
        "## Result",
        "",
        "```text",
        f"status: {result['p1_adversarial_check_status']}",
        f"error count: {result['error_count']}",
        f"query count: {result['query_count']}",
        "```",
        "",
        "## Errors",
        "",
    ]
    if result["errors"]:
        lines.extend(f"- {item['code']}: {item['detail']}" for item in result["errors"])
    else:
        lines.append("- none")
    lines.append("")
    CHECK_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    errors: list[dict] = []
    required = [
        QUERY_FILE,
        AUDIT_JSON,
        COMBINED_SUMMARY,
        REPORT_MD,
        RESULTS_DIR / "phase_b_adversarial_summary.csv",
        RESULTS_DIR / "phase_b_adversarial_query_metrics.csv",
        RESULTS_DIR / "phase_b_p1_adversarial_clean_vaks_only_summary.csv",
    ]
    for path in required:
        if not path.exists():
            add_error(errors, "missing_artifact", str(path))
        elif path.stat().st_size == 0:
            add_error(errors, "empty_artifact", str(path))
    query_count = count_jsonl(QUERY_FILE) if QUERY_FILE.exists() else 0
    if query_count != 30:
        add_error(errors, "query_count_mismatch", str(query_count))
    audit = json.loads(AUDIT_JSON.read_text(encoding="utf-8")) if AUDIT_JSON.exists() else {}
    if audit.get("p1_adversarial_status") != "pass":
        add_error(errors, "audit_status_not_pass", str(audit.get("p1_adversarial_status")))
    if int(audit.get("failed_criteria") if audit.get("failed_criteria") is not None else -1) != 0:
        add_error(errors, "failed_criteria_nonzero", str(audit.get("failed_criteria")))
    summary = read_csv(COMBINED_SUMMARY) if COMBINED_SUMMARY.exists() else []
    expected_modes = {
        "baseline_file_lexical",
        "vaks_only_lexical_bucket",
        "vaks_b_bucket_local",
        "vaks_b_adapter_skeleton",
        "yuxi_native_profile",
    }
    for corpus in ["primary", "full"]:
        present = {row["mode"] for row in summary if row["corpus"] == corpus}
        missing = sorted(expected_modes - present)
        if missing:
            add_error(errors, "missing_summary_modes", f"{corpus}:{','.join(missing)}")
    result = {
        "p1_adversarial_check_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "query_count": query_count,
        "audit": audit,
    }
    CHECK_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_md(result)
    print(f"p1 adversarial check status: {result['p1_adversarial_check_status']}")
    print(f"error count: {result['error_count']}")


if __name__ == "__main__":
    main()
