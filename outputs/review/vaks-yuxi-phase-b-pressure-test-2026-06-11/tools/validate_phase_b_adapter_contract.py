import argparse
import csv
import json
import re
from collections import Counter, defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parents[4]
SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")
CLICKBACK_RE = re.compile(r"^(?P<path>.+):L(?P<start>\d+)-L(?P<end>\d+)$")
SUPPORT_BUCKETS = {"core_framework", "reviewed"}
RISK_BUCKETS = {"raw", "candidate", "summary", "qa", "overlay", "feedback", "diagnostic", "unknown"}

MANIFEST_REQUIRED = {
    "vaks_record_id",
    "vault_path",
    "heading_or_anchor",
    "selector_or_line_range",
    "source_hash",
    "indexed_source_hash",
    "chunk_hash",
    "record_kind",
    "knowledge_status",
    "review_state",
    "relation_state",
    "retrieval_policy",
    "authority_badge",
    "usage_badge",
    "temporal_badge",
    "warning_code",
    "retrieval_reasons",
    "source_clickback",
    "indexed_at",
}

RECEIPT_REQUIRED = MANIFEST_REQUIRED | {
    "query_id",
    "query_group",
    "query_intent",
    "mode",
    "rank",
    "retrieval_receipt",
}


def load_jsonl(path: Path):
    with path.open(encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            line = line.strip()
            if not line:
                continue
            yield line_no, json.loads(line)


def check(condition: bool, errors: list[dict], code: str, path: Path, line_no: int | None, detail: str) -> None:
    if not condition:
        errors.append(
            {
                "code": code,
                "path": str(path),
                "line": line_no or "",
                "detail": detail,
            }
        )


def validate_hash(value: str) -> bool:
    return bool(value and HEX64_RE.match(value))


def resolve_clickback(value: str) -> tuple[Path | None, int | None, int | None]:
    match = CLICKBACK_RE.match(value or "")
    if not match:
        return None, None, None
    rel_path = match.group("path")
    target = (ROOT / rel_path).resolve()
    return target, int(match.group("start")), int(match.group("end"))


def validate_clickback(value: str, errors: list[dict], path: Path, line_no: int) -> None:
    target, start, end = resolve_clickback(value)
    check(target is not None, errors, "bad_clickback_format", path, line_no, value)
    if target is None or start is None or end is None:
        return
    try:
        target.relative_to(ROOT.resolve())
    except ValueError:
        check(False, errors, "clickback_outside_root", path, line_no, str(target))
        return
    check(target.exists(), errors, "clickback_missing_file", path, line_no, str(target))
    check(start >= 1 and end >= start, errors, "clickback_bad_range", path, line_no, value)
    if target.exists():
        try:
            line_count = len(target.read_text(encoding="utf-8", errors="replace").splitlines()) or 1
            check(end <= line_count, errors, "clickback_range_past_eof", path, line_no, f"{value} > {line_count}")
        except OSError as exc:
            check(False, errors, "clickback_unreadable", path, line_no, str(exc))


def validate_policy(policy: dict, errors: list[dict], path: Path, line_no: int, expected_kind: str) -> None:
    check(isinstance(policy, dict), errors, "policy_not_object", path, line_no, str(policy))
    if not isinstance(policy, dict):
        return
    for key in ["policy_kind", "pack_allowed", "action_basis_allowed", "authority_bucket"]:
        check(key in policy, errors, "policy_missing_field", path, line_no, key)
    check(policy.get("policy_kind") == expected_kind, errors, "policy_kind_mismatch", path, line_no, str(policy.get("policy_kind")))
    check(isinstance(policy.get("pack_allowed"), bool), errors, "pack_allowed_not_bool", path, line_no, str(policy.get("pack_allowed")))
    check(
        isinstance(policy.get("action_basis_allowed"), bool),
        errors,
        "action_basis_allowed_not_bool",
        path,
        line_no,
        str(policy.get("action_basis_allowed")),
    )


def validate_manifest(path: Path, expected_count: int | None = None) -> tuple[int, list[dict], Counter]:
    errors: list[dict] = []
    counts: Counter = Counter()
    seen_ids: set[str] = set()
    row_count = 0
    for line_no, row in load_jsonl(path):
        row_count += 1
        missing = MANIFEST_REQUIRED - set(row)
        check(not missing, errors, "manifest_missing_fields", path, line_no, ",".join(sorted(missing)))
        validate_policy(row.get("retrieval_policy"), errors, path, line_no, "phase_b_skeleton_manifest")
        policy = row.get("retrieval_policy") if isinstance(row.get("retrieval_policy"), dict) else {}
        bucket = policy.get("authority_bucket")
        counts[f"bucket:{bucket}"] += 1
        check(row.get("vaks_record_id") not in seen_ids, errors, "duplicate_vaks_record_id", path, line_no, row.get("vaks_record_id", ""))
        seen_ids.add(row.get("vaks_record_id"))
        check(validate_hash(row.get("source_hash", "")), errors, "bad_source_hash", path, line_no, row.get("source_hash", ""))
        check(validate_hash(row.get("chunk_hash", "")), errors, "bad_chunk_hash", path, line_no, row.get("chunk_hash", ""))
        validate_clickback(row.get("source_clickback", ""), errors, path, line_no)
        action_allowed = bool(policy.get("action_basis_allowed"))
        check(
            not action_allowed or bucket in SUPPORT_BUCKETS,
            errors,
            "manifest_action_basis_leak",
            path,
            line_no,
            f"bucket={bucket}",
        )
        if bucket in RISK_BUCKETS:
            check(row.get("warning_code") or bucket not in {"raw", "feedback"}, errors, "risky_manifest_missing_warning", path, line_no, f"bucket={bucket}")
    if expected_count is not None:
        check(row_count == expected_count, errors, "manifest_count_mismatch", path, None, f"{row_count} != {expected_count}")
    return row_count, errors, counts


def validate_receipts(path: Path, expected_queries: int, expected_results: int) -> tuple[int, list[dict], Counter]:
    errors: list[dict] = []
    counts: Counter = Counter()
    per_query: dict[str, int] = defaultdict(int)
    row_count = 0
    for line_no, row in load_jsonl(path):
        row_count += 1
        missing = RECEIPT_REQUIRED - set(row)
        check(not missing, errors, "receipt_missing_fields", path, line_no, ",".join(sorted(missing)))
        validate_policy(row.get("retrieval_policy"), errors, path, line_no, "phase_b_skeleton_bucket_local")
        policy = row.get("retrieval_policy") if isinstance(row.get("retrieval_policy"), dict) else {}
        receipt = row.get("retrieval_receipt") if isinstance(row.get("retrieval_receipt"), dict) else {}
        bucket = policy.get("authority_bucket")
        counts[f"bucket:{bucket}"] += 1
        per_query[row.get("query_id", "")] += 1
        check(row.get("mode") == "vaks_b_adapter_skeleton", errors, "receipt_mode_mismatch", path, line_no, row.get("mode", ""))
        check(receipt.get("receipt_present") is True, errors, "receipt_present_not_true", path, line_no, str(receipt))
        check(receipt.get("bucket") == bucket, errors, "receipt_bucket_mismatch", path, line_no, str(receipt))
        check(validate_hash(row.get("source_hash", "")), errors, "bad_source_hash", path, line_no, row.get("source_hash", ""))
        check(validate_hash(row.get("chunk_hash", "")), errors, "bad_chunk_hash", path, line_no, row.get("chunk_hash", ""))
        validate_clickback(row.get("source_clickback", ""), errors, path, line_no)
        action_allowed = bool(policy.get("action_basis_allowed"))
        query_intent = row.get("query_intent")
        check(
            not action_allowed or (bucket in SUPPORT_BUCKETS and query_intent == "action"),
            errors,
            "receipt_action_basis_leak",
            path,
            line_no,
            f"bucket={bucket};intent={query_intent}",
        )
        if query_intent in {"action", "evidence"} and bucket not in SUPPORT_BUCKETS:
            check(row.get("warning_code"), errors, "risky_receipt_missing_warning", path, line_no, f"bucket={bucket};intent={query_intent}")
        if bucket not in SUPPORT_BUCKETS:
            check(row.get("relation_state") == "candidate_relation_only", errors, "risky_relation_state_leak", path, line_no, str(row.get("relation_state")))
    check(row_count == expected_results, errors, "receipt_count_mismatch", path, None, f"{row_count} != {expected_results}")
    check(len(per_query) == expected_queries, errors, "receipt_query_count_mismatch", path, None, f"{len(per_query)} != {expected_queries}")
    wrong_query_counts = {query_id: count for query_id, count in per_query.items() if count != 10}
    check(not wrong_query_counts, errors, "receipt_per_query_count_mismatch", path, None, json.dumps(wrong_query_counts, ensure_ascii=False))
    return row_count, errors, counts


def read_json(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def validate_all() -> dict:
    manifest_summary = read_json(RESULTS_DIR / "phase_b_skeleton_main_manifest_summary.json")
    main_receipt_summary = read_json(RESULTS_DIR / "phase_b_skeleton_main_receipt_summary.json")
    holdout_receipt_summary = read_json(RESULTS_DIR / "phase_b_skeleton_holdout_receipt_summary.json")

    errors: list[dict] = []
    sections = []

    for item in manifest_summary:
        path = Path(item["manifest_path"])
        row_count, section_errors, counts = validate_manifest(path, expected_count=item["chunks"])
        errors.extend(section_errors)
        sections.append({"section": f"manifest:{item['corpus']}", "rows": row_count, "errors": len(section_errors), "counts": dict(counts)})

    for item in main_receipt_summary:
        path = Path(item["receipt_path"])
        row_count, section_errors, counts = validate_receipts(path, expected_queries=item["queries"], expected_results=item["results"])
        errors.extend(section_errors)
        sections.append({"section": f"main_receipts:{item['corpus']}", "rows": row_count, "errors": len(section_errors), "counts": dict(counts)})

    for item in holdout_receipt_summary:
        path = Path(item["receipt_path"])
        row_count, section_errors, counts = validate_receipts(path, expected_queries=item["queries"], expected_results=item["results"])
        errors.extend(section_errors)
        sections.append({"section": f"holdout_receipts:{item['corpus']}", "rows": row_count, "errors": len(section_errors), "counts": dict(counts)})

    return {
        "contract_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "sections": sections,
        "errors": errors[:200],
    }


def write_report(result: dict) -> None:
    path = SANDBOX_DIR / "PHASE_B_ADAPTER_CONTRACT_TEST.md"
    lines = [
        "---",
        "record_kind: sandbox_adapter_contract_test",
        "status: candidate",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: diagnostic_not_mainline_decision",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Adapter Contract Test",
        "",
        "## Verdict",
        "",
        f"- contract status: {result['contract_status']}",
        f"- error count: {result['error_count']}",
        "",
        "## Sections",
        "",
        "| Section | Rows | Errors |",
        "|---|---:|---:|",
    ]
    for section in result["sections"]:
        lines.append(f"| {section['section']} | {section['rows']} | {section['errors']} |")
    lines.extend(
        [
            "",
            "## Checks",
            "",
            "- manifest required fields",
            "- receipt required fields",
            "- policy kind and policy booleans",
            "- source and chunk hash shape",
            "- click-back target existence and line range",
            "- no action-basis permission leaks",
            "- risky action/evidence results carry warnings",
            "- risky rows cannot claim reviewed relation state",
            "",
        ]
    )
    if result["errors"]:
        lines.extend(["## First Errors", ""])
        for error in result["errors"][:50]:
            lines.append(f"- {error['code']} | {error['path']}:{error['line']} | {error['detail']}")
    else:
        lines.extend(
            [
                "## Boundary",
                "",
                "The contract test is diagnostic only. It does not approve mainline adoption, C-lite, Skills, MCP writes, subagents, formal writeback, or production readiness.",
                "",
            ]
        )
    path.write_text("\n".join(lines), encoding="utf-8")
    (RESULTS_DIR / "phase_b_adapter_contract_test.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8"
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.parse_args()
    result = validate_all()
    write_report(result)
    if result["error_count"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
