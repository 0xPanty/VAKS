from __future__ import annotations

import hashlib
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT = SLICE_ROOT / "artifact" / "old_file_status_normalization_executor_apply.json"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURES = SLICE_ROOT / "failure-cases" / "old-file-status-normalization-executor-failures.json"

REQUIRED_FILES = [
    "slice-plan.md",
    "source-map.md",
    "artifact/apply_old_file_status_normalization.py",
    "artifact/repair_line_endings_after_apply.py",
    "artifact/verify_old_file_status_normalization_executor_apply.py",
    "artifact/old_file_status_normalization_executor_apply.json",
    "artifact/old_file_status_normalization_executor_apply.md",
    "artifact/old_file_status_normalization_executor_apply.html",
    "artifact/write_attribution_audit.json",
    "artifact/write_attribution_audit.md",
    "failure-cases/old-file-status-normalization-executor-failures.json",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

REQUIRED_FIXTURES = {
    "all-75-status-only-writes-applied.json",
    "body-content-unchanged-after-apply.json",
    "non-status-frontmatter-unchanged-after-apply.json",
    "protected-paths-not-written.json",
    "sandbox-not-mainline-authority.json",
}

REQUIRED_FAILURE_CASES = {
    "P2-91-FAIL-01-missing-exact-approval",
    "P2-91-FAIL-02-prewrite-hash-drift",
    "P2-91-FAIL-03-current-status-mismatch",
    "P2-91-FAIL-04-body-drift",
    "P2-91-FAIL-05-non-status-frontmatter-drift",
    "P2-91-FAIL-06-wrong-target-or-count",
    "P2-91-FAIL-07-protected-path-write",
    "P2-91-FAIL-08-mainline-or-truth-authority",
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def split_newline(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    return line, ""


def parse_frontmatter(text: str) -> dict:
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter fence")
    end_index = None
    for idx in range(1, len(lines)):
        if lines[idx].strip() == "---":
            end_index = idx
            break
    if end_index is None:
        raise ValueError("missing closing frontmatter fence")
    status_index = None
    status_value = None
    for idx in range(1, end_index):
        content, _newline = split_newline(lines[idx])
        if content.startswith("status:"):
            status_index = idx
            status_value = content.split(":", 1)[1].strip()
            break
    if status_index is None:
        raise ValueError("missing status line")
    return {
        "status_value": status_value,
        "body_text": "".join(lines[end_index + 1 :]),
        "non_status_frontmatter_text": "".join(
            line for idx, line in enumerate(lines[1:end_index], start=1) if idx != status_index
        ),
    }


def frontmatter_status(path: Path) -> str | None:
    return parse_frontmatter(path.read_text(encoding="utf-8"))["status_value"]


def check(final_gate: bool = False) -> dict:
    failures: list[str] = []
    for rel in REQUIRED_FILES:
        if not (SLICE_ROOT / rel).exists():
            failures.append(f"missing required file: {rel}")

    payload = load_json(ARTIFACT) if ARTIFACT.exists() else {}
    summary = payload.get("summary", {})
    expected_summary = {
        "passed_prewrite": True,
        "transaction_operation_count": 75,
        "unique_target_file_count": 75,
        "prewrite_hash_match_count": 75,
        "prewrite_status_match_count": 75,
        "post_apply_status_match_count": 75,
        "body_unchanged_count": 75,
        "non_status_frontmatter_unchanged_count": 75,
        "old_slice_writes_applied": 75,
        "protected_path_writes": 0,
        "normalization_applied": True,
        "mainline_ready": False,
        "promotion_ready": False,
        "reviewed_knowledge_ready": False,
        "evidence_support_ready": False,
        "action_basis_ready": False,
    }
    for key, expected in expected_summary.items():
        if summary.get(key) != expected:
            failures.append(f"summary mismatch for {key}: expected {expected!r}, got {summary.get(key)!r}")

    if payload.get("approval", {}).get("exact_p2_75_approval_phrase_present") is not True:
        failures.append("exact approval phrase not recorded")

    ops = payload.get("execution_operations", [])
    if len(ops) != 75:
        failures.append(f"expected 75 execution operations, found {len(ops)}")
    if len({op.get("target_path") for op in ops}) != 75:
        failures.append("execution target paths are not unique 75")

    for op in ops:
        target = REPO_ROOT / op["target_path"]
        if not target.exists():
            failures.append(f"target missing after apply: {op['target_path']}")
            continue
        raw = target.read_bytes()
        parsed = parse_frontmatter(raw.decode("utf-8"))
        if sha256_bytes(raw) != op.get("post_apply_sha256_actual"):
            failures.append(f"current hash mismatch for operation {op['operation_index']}")
        if parsed["status_value"] != op.get("proposed_status"):
            failures.append(f"current status mismatch for operation {op['operation_index']}")
        if sha256_bytes(parsed["body_text"].encode("utf-8")) != op.get("body_sha256_before"):
            failures.append(f"body changed for operation {op['operation_index']}")
        if (
            sha256_bytes(parsed["non_status_frontmatter_text"].encode("utf-8"))
            != op.get("non_status_frontmatter_sha256_before")
        ):
            failures.append(f"non-status frontmatter changed for operation {op['operation_index']}")
        if op.get("write_applied") is not True:
            failures.append(f"write not recorded for operation {op['operation_index']}")

    authority = payload.get("authority_flags", {})
    for key in [
        "body_content_edits_allowed",
        "artifact_edits_allowed",
        "tools_templates_edits_allowed",
        "wiki_truth_layer_edits_allowed",
        "mainline_edits_allowed",
        "obsidian_sync_allowed",
        "commit_push_allowed",
        "mainline_ready",
        "promotion_ready",
        "reviewed_knowledge_ready",
        "evidence_support_ready",
        "action_basis_ready",
        "goal_complete_now",
    ]:
        if authority.get(key) is not False:
            failures.append(f"authority flag must remain false: {key}")

    fixture_names = {path.name for path in FIXTURES_DIR.glob("*.json")} if FIXTURES_DIR.exists() else set()
    missing_fixtures = REQUIRED_FIXTURES - fixture_names
    if missing_fixtures:
        failures.append(f"missing fixtures: {sorted(missing_fixtures)}")
    fixture_expectations = {
        "all-75-status-only-writes-applied.json": {
            "old_slice_writes_applied": 75,
            "post_apply_status_match_count": 75,
        },
        "body-content-unchanged-after-apply.json": {"body_unchanged_count": 75},
        "non-status-frontmatter-unchanged-after-apply.json": {
            "non_status_frontmatter_unchanged_count": 75
        },
        "protected-paths-not-written.json": {"protected_path_writes": 0},
        "sandbox-not-mainline-authority.json": {
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "action_basis_ready": False,
        },
    }
    for name, expected_fields in fixture_expectations.items():
        fixture_path = FIXTURES_DIR / name
        if not fixture_path.exists():
            continue
        fixture_payload = load_json(fixture_path)
        for key, expected in expected_fields.items():
            if fixture_payload.get(key) != expected:
                failures.append(
                    f"fixture {name} expected {key}={expected!r}, got {fixture_payload.get(key)!r}"
                )

    failure_payload = load_json(FAILURES) if FAILURES.exists() else {"failure_cases": []}
    failure_ids = {case.get("case_id") for case in failure_payload.get("failure_cases", [])}
    missing_failure_cases = REQUIRED_FAILURE_CASES - failure_ids
    if missing_failure_cases:
        failures.append(f"missing failure cases: {sorted(missing_failure_cases)}")

    md_text = (SLICE_ROOT / "artifact" / "old_file_status_normalization_executor_apply.md").read_text(encoding="utf-8") if (SLICE_ROOT / "artifact" / "old_file_status_normalization_executor_apply.md").exists() else ""
    html_text = (SLICE_ROOT / "artifact" / "old_file_status_normalization_executor_apply.html").read_text(encoding="utf-8") if (SLICE_ROOT / "artifact" / "old_file_status_normalization_executor_apply.html").exists() else ""
    for needle in ["old_slice_writes_applied: 75", "body_unchanged_count: 75", "protected_path_writes: 0"]:
        if needle not in md_text:
            failures.append(f"markdown missing: {needle}")
    for needle in ["p2-91 Executor Apply", "Writes Applied", "Protected Writes"]:
        if needle not in html_text:
            failures.append(f"html missing: {needle}")
    attribution_path = SLICE_ROOT / "artifact" / "write_attribution_audit.json"
    if attribution_path.exists():
        attribution = load_json(attribution_path)
        if attribution.get("allowed_target_count") != 75:
            failures.append("attribution audit allowed_target_count must be 75")
        if attribution.get("execution_summary", {}).get("protected_path_writes") != 0:
            failures.append("attribution audit protected_path_writes must be 0")
        if "pre-existing baseline" not in attribution.get("protected_path_status_attribution", ""):
            failures.append("attribution audit must state protected path dirty is pre-existing baseline")

    if final_gate:
        report_statuses = {
            "verification.md": "local_verification_passed",
            "reviewer-report.md": "review_pass_no_blocker",
            "boundary-audit.md": "pass_boundary",
            "product-acceptance-report.md": "pass_product_grade",
            "next-step.md": "pass_product_grade_pending_next_slice",
        }
        for rel, expected in report_statuses.items():
            actual = frontmatter_status(SLICE_ROOT / rel)
            if actual != expected:
                failures.append(f"{rel} status expected {expected!r}, got {actual!r}")

    result = {
        "passed": not failures,
        "failures": failures,
        "summary": {
            "slice_id": SLICE_ID,
            "fixture_count": len(fixture_names),
            "failure_case_count": len(failure_ids),
            "transaction_operation_count": summary.get("transaction_operation_count"),
            "old_slice_writes_applied": summary.get("old_slice_writes_applied"),
            "post_apply_status_match_count": summary.get("post_apply_status_match_count"),
            "body_unchanged_count": summary.get("body_unchanged_count"),
            "non_status_frontmatter_unchanged_count": summary.get("non_status_frontmatter_unchanged_count"),
            "protected_path_writes": summary.get("protected_path_writes"),
            "final_gate": final_gate,
        },
    }
    return result


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()
    result = check(final_gate=args.final_gate)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    if not result["passed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
