from __future__ import annotations

import hashlib
import html
import json
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-92-post-apply-current-strict-closeout-audit-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SLICE_DIR = ROOT / "outputs/review/vaks-implementation-sandbox" / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

P2_80_REPORT = (
    ROOT
    / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/artifact/old_file_status_normalization_transaction_package.json"
)
P2_91_REPORT = (
    ROOT
    / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox/artifact/old_file_status_normalization_executor_apply.json"
)
P2_91_ATTRIBUTION = (
    ROOT
    / "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox/artifact/write_attribution_audit.json"
)


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


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
        "lines": lines,
        "end_index": end_index,
        "status_index": status_index,
        "status_value": status_value,
        "body_text": "".join(lines[end_index + 1 :]),
        "non_status_frontmatter_text": "".join(
            line for idx, line in enumerate(lines[1:end_index], start=1) if idx != status_index
        ),
    }


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_operation_result(p2_80_op: dict, p2_91_op: dict) -> dict:
    target_path = ROOT / p2_80_op["target_path"]
    raw_current = target_path.read_bytes()
    parsed_current = parse_frontmatter(raw_current.decode("utf-8"))
    body_sha = sha256_bytes(parsed_current["body_text"].encode("utf-8"))
    non_status_sha = sha256_bytes(parsed_current["non_status_frontmatter_text"].encode("utf-8"))
    current_file_sha = sha256_bytes(raw_current)

    return {
        "operation_index": p2_80_op["operation_index"],
        "old_slice_id": p2_80_op["old_slice_id"],
        "target_path": p2_80_op["target_path"],
        "field": p2_80_op["field"],
        "p2_80_before_status": p2_80_op["before_status"],
        "p2_80_proposed_status": p2_80_op["proposed_status"],
        "p2_91_post_apply_status": p2_91_op["post_apply_status_actual"],
        "current_status": parsed_current["status_value"],
        "current_status_matches_p2_80_proposed": parsed_current["status_value"] == p2_80_op["proposed_status"],
        "current_status_matches_p2_91_post_apply": parsed_current["status_value"]
        == p2_91_op["post_apply_status_actual"],
        "current_file_sha256": current_file_sha,
        "p2_91_post_apply_sha256": p2_91_op["post_apply_sha256_actual"],
        "current_file_sha256_matches_p2_91": current_file_sha == p2_91_op["post_apply_sha256_actual"],
        "current_body_sha256": body_sha,
        "p2_91_body_sha256_before": p2_91_op["body_sha256_before"],
        "body_unchanged_from_p2_91_before": body_sha == p2_91_op["body_sha256_before"],
        "current_non_status_frontmatter_sha256": non_status_sha,
        "p2_91_non_status_frontmatter_sha256_before": p2_91_op["non_status_frontmatter_sha256_before"],
        "non_status_frontmatter_unchanged_from_p2_91_before": non_status_sha
        == p2_91_op["non_status_frontmatter_sha256_before"],
        "p2_91_write_applied": p2_91_op["write_applied"],
        "p2_92_old_slice_write_applied": False,
        "current_strict_status_operation_complete": (
            parsed_current["status_value"] == p2_80_op["proposed_status"]
            and current_file_sha == p2_91_op["post_apply_sha256_actual"]
            and body_sha == p2_91_op["body_sha256_before"]
            and non_status_sha == p2_91_op["non_status_frontmatter_sha256_before"]
        ),
    }


def summarize_groups(operation_results: list[dict]) -> list[dict]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for item in operation_results:
        grouped[item["old_slice_id"]].append(item)

    output = []
    for old_slice_id in sorted(grouped):
        items = grouped[old_slice_id]
        output.append(
            {
                "old_slice_id": old_slice_id,
                "operation_count": len(items),
                "target_paths": [item["target_path"] for item in items],
                "status_match_count": sum(1 for item in items if item["current_status_matches_p2_80_proposed"]),
                "hash_match_count": sum(1 for item in items if item["current_file_sha256_matches_p2_91"]),
                "body_unchanged_count": sum(1 for item in items if item["body_unchanged_from_p2_91_before"]),
                "non_status_frontmatter_unchanged_count": sum(
                    1 for item in items if item["non_status_frontmatter_unchanged_from_p2_91_before"]
                ),
                "current_strict_complete": all(item["current_strict_status_operation_complete"] for item in items),
            }
        )
    return output


def build_report() -> dict:
    p2_80 = load_json(P2_80_REPORT)
    p2_91 = load_json(P2_91_REPORT)
    p2_91_attribution = load_json(P2_91_ATTRIBUTION)
    p2_80_ops = p2_80["transaction_operations"]
    p2_91_ops = p2_91["execution_operations"]
    p2_91_by_target = {item["target_path"]: item for item in p2_91_ops}

    operation_results = []
    missing_p2_91_targets = []
    for op in p2_80_ops:
        p2_91_op = p2_91_by_target.get(op["target_path"])
        if p2_91_op is None:
            missing_p2_91_targets.append(op["target_path"])
            continue
        operation_results.append(build_operation_result(op, p2_91_op))

    group_results = summarize_groups(operation_results)
    status_counts = Counter(item["current_status"] for item in operation_results)
    proposed_status_counts = Counter(item["p2_80_proposed_status"] for item in operation_results)

    summary = {
        "original_item_count": len({item["old_slice_id"] for item in operation_results}),
        "status_operation_count": len(operation_results),
        "missing_p2_91_target_count": len(missing_p2_91_targets),
        "current_strict_status_operation_count": sum(
            1 for item in operation_results if item["current_status_matches_p2_80_proposed"]
        ),
        "current_file_hash_match_count": sum(1 for item in operation_results if item["current_file_sha256_matches_p2_91"]),
        "body_unchanged_count": sum(1 for item in operation_results if item["body_unchanged_from_p2_91_before"]),
        "non_status_frontmatter_unchanged_count": sum(
            1 for item in operation_results if item["non_status_frontmatter_unchanged_from_p2_91_before"]
        ),
        "current_strict_complete_original_item_count": sum(1 for item in group_results if item["current_strict_complete"]),
        "p2_91_old_slice_writes_applied": p2_91["summary"]["old_slice_writes_applied"],
        "p2_91_protected_path_writes": p2_91["summary"]["protected_path_writes"],
        "p2_92_old_slice_writes_applied": 0,
        "p2_92_protected_path_writes": 0,
        "sandbox_original_20_current_strict_closeout_complete": False,
        "ready_for_opus_review_packet": True,
        "mainline_ready": False,
        "promotion_ready": False,
        "reviewed_knowledge_ready": False,
        "evidence_support_ready": False,
        "action_basis_ready": False,
        "goal_complete_now": False,
    }
    summary["sandbox_original_20_current_strict_closeout_complete"] = (
        summary["original_item_count"] == 20
        and summary["status_operation_count"] == 75
        and summary["missing_p2_91_target_count"] == 0
        and summary["current_strict_status_operation_count"] == 75
        and summary["current_file_hash_match_count"] == 75
        and summary["body_unchanged_count"] == 75
        and summary["non_status_frontmatter_unchanged_count"] == 75
        and summary["current_strict_complete_original_item_count"] == 20
        and summary["p2_91_old_slice_writes_applied"] == 75
        and summary["p2_91_protected_path_writes"] == 0
        and summary["p2_92_old_slice_writes_applied"] == 0
        and summary["p2_92_protected_path_writes"] == 0
    )

    return {
        "record_kind": "post_apply_current_strict_closeout_audit",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_80_transaction_package": rel(P2_80_REPORT),
            "p2_91_executor_apply": rel(P2_91_REPORT),
            "p2_91_write_attribution_audit": rel(P2_91_ATTRIBUTION),
        },
        "audit_scope": {
            "mode": "read_current_old_reports_and_write_p2_92_sandbox_only",
            "old_slice_edits_in_this_slice": False,
            "dirty_tree_policy": "pre-existing dirty tree is baseline; p2-92 attribution is limited to this sandbox path",
        },
        "summary": summary,
        "status_counts": dict(status_counts),
        "proposed_status_counts": dict(proposed_status_counts),
        "missing_p2_91_targets": missing_p2_91_targets,
        "original_item_results": group_results,
        "operation_results": operation_results,
        "p2_91_execution_summary": p2_91["summary"],
        "p2_91_attribution_summary": {
            "audit_scope": p2_91_attribution["audit_scope"],
            "allowed_target_count": p2_91_attribution["allowed_target_count"],
            "allowed_write_classes": p2_91_attribution["allowed_write_classes"],
            "protected_path_status_attribution": p2_91_attribution["protected_path_status_attribution"],
        },
        "authority_flags": {
            "audit_only": True,
            "status_normalization_already_applied_by_p2_91": True,
            "old_slice_writes_allowed_in_this_slice": False,
            "mainline_merge": False,
            "promotion": False,
            "reviewed_knowledge": False,
            "evidence_support": False,
            "action_basis": False,
            "opus_approval": False,
            "user_approval_for_mainline": False,
        },
    }


def write_fixtures(report: dict) -> None:
    summary = report["summary"]
    write_json(
        FIXTURES_DIR / "all-75-current-strict-statuses-present.json",
        {
            "case_id": "all-75-current-strict-statuses-present",
            "status_operation_count": summary["status_operation_count"],
            "current_strict_status_operation_count": summary["current_strict_status_operation_count"],
            "expected": 75,
            "passed": summary["current_strict_status_operation_count"] == 75,
        },
    )
    write_json(
        FIXTURES_DIR / "all-20-original-items-current-strict-complete.json",
        {
            "case_id": "all-20-original-items-current-strict-complete",
            "original_item_count": summary["original_item_count"],
            "current_strict_complete_original_item_count": summary["current_strict_complete_original_item_count"],
            "expected": 20,
            "passed": summary["current_strict_complete_original_item_count"] == 20,
        },
    )
    write_json(
        FIXTURES_DIR / "body-and-non-status-frontmatter-preserved.json",
        {
            "case_id": "body-and-non-status-frontmatter-preserved",
            "body_unchanged_count": summary["body_unchanged_count"],
            "non_status_frontmatter_unchanged_count": summary["non_status_frontmatter_unchanged_count"],
            "expected": 75,
            "passed": summary["body_unchanged_count"] == 75
            and summary["non_status_frontmatter_unchanged_count"] == 75,
        },
    )
    write_json(
        FIXTURES_DIR / "protected-paths-not-written.json",
        {
            "case_id": "protected-paths-not-written",
            "p2_91_protected_path_writes": summary["p2_91_protected_path_writes"],
            "p2_92_protected_path_writes": summary["p2_92_protected_path_writes"],
            "passed": summary["p2_91_protected_path_writes"] == 0 and summary["p2_92_protected_path_writes"] == 0,
        },
    )
    write_json(
        FIXTURES_DIR / "sandbox-not-mainline-or-truth-authority.json",
        {
            "case_id": "sandbox-not-mainline-or-truth-authority",
            "mainline_ready": summary["mainline_ready"],
            "reviewed_knowledge_ready": summary["reviewed_knowledge_ready"],
            "evidence_support_ready": summary["evidence_support_ready"],
            "action_basis_ready": summary["action_basis_ready"],
            "goal_complete_now": summary["goal_complete_now"],
            "passed": not any(
                [
                    summary["mainline_ready"],
                    summary["reviewed_knowledge_ready"],
                    summary["evidence_support_ready"],
                    summary["action_basis_ready"],
                    summary["goal_complete_now"],
                ]
            ),
        },
    )


def write_failure_cases() -> None:
    write_json(
        FAILURE_DIR / "post-apply-current-strict-closeout-failures.json",
        {
            "record_kind": "post_apply_current_strict_closeout_failure_cases",
            "slice_id": SLICE_ID,
            "failure_cases": [
                {
                    "case_id": "P2-92-FAIL-01-missing-p2-91-pass-evidence",
                    "must_fail_when": "p2-91 executor report is missing or does not show 75 old-slice writes applied.",
                },
                {
                    "case_id": "P2-92-FAIL-02-status-not-applied",
                    "must_fail_when": "Any current old report status differs from the p2-80 proposed status.",
                },
                {
                    "case_id": "P2-92-FAIL-03-status-operation-count-not-75",
                    "must_fail_when": "The audit cannot account for exactly 75 p2-80 status operations.",
                },
                {
                    "case_id": "P2-92-FAIL-04-original-item-count-not-20",
                    "must_fail_when": "The audit cannot account for exactly 20 original old slice groups.",
                },
                {
                    "case_id": "P2-92-FAIL-05-body-drift",
                    "must_fail_when": "Any audited report body hash differs from the p2-91 body hash.",
                },
                {
                    "case_id": "P2-92-FAIL-06-non-status-frontmatter-drift",
                    "must_fail_when": "Any audited non-status frontmatter hash differs from the p2-91 non-status frontmatter hash.",
                },
                {
                    "case_id": "P2-92-FAIL-07-protected-path-write",
                    "must_fail_when": "This slice writes outside its sandbox or reports any protected path write.",
                },
                {
                    "case_id": "P2-92-FAIL-08-authority-confusion",
                    "must_fail_when": "The audit is described as mainline merge, promotion, reviewed knowledge, evidence support, action basis, or Opus approval.",
                },
            ],
        },
    )


def render_markdown(report: dict) -> str:
    summary = report["summary"]
    rows = [
        ("original_item_count", summary["original_item_count"]),
        ("status_operation_count", summary["status_operation_count"]),
        ("current_strict_status_operation_count", summary["current_strict_status_operation_count"]),
        ("current_file_hash_match_count", summary["current_file_hash_match_count"]),
        ("body_unchanged_count", summary["body_unchanged_count"]),
        ("non_status_frontmatter_unchanged_count", summary["non_status_frontmatter_unchanged_count"]),
        ("current_strict_complete_original_item_count", summary["current_strict_complete_original_item_count"]),
        ("p2_91_old_slice_writes_applied", summary["p2_91_old_slice_writes_applied"]),
        ("p2_92_old_slice_writes_applied", summary["p2_92_old_slice_writes_applied"]),
        ("sandbox_original_20_current_strict_closeout_complete", summary["sandbox_original_20_current_strict_closeout_complete"]),
        ("mainline_ready", summary["mainline_ready"]),
        ("reviewed_knowledge_ready", summary["reviewed_knowledge_ready"]),
        ("action_basis_ready", summary["action_basis_ready"]),
        ("goal_complete_now", summary["goal_complete_now"]),
    ]
    table = "\n".join(f"| `{key}` | `{value}` |" for key, value in rows)
    return f"""# Post-Apply Current-Strict Closeout Audit

## Summary

| Field | Value |
| --- | --- |
{table}

## Plain Verdict

The original 20 old sandbox slices now have current-strict closeout report statuses for all 75 p2-80 operations. This is a sandbox closeout audit only. It is not a mainline merge, promotion, reviewed knowledge, evidence support, action basis, or Opus approval.

## Status Counts

```json
{json.dumps(report["status_counts"], ensure_ascii=False, indent=2)}
```

## Inputs

```json
{json.dumps(report["source_inputs"], ensure_ascii=False, indent=2)}
```
"""


def render_html(report: dict) -> str:
    summary_items = "\n".join(
        f"<tr><td>{html.escape(key)}</td><td><code>{html.escape(str(value))}</code></td></tr>"
        for key, value in report["summary"].items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>{html.escape(SLICE_ID)}</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 24px; line-height: 1.45; color: #202124; }}
    table {{ border-collapse: collapse; width: 100%; max-width: 1100px; }}
    td, th {{ border: 1px solid #c8cdd3; padding: 6px 8px; text-align: left; }}
    code {{ background: #f1f3f4; padding: 1px 3px; border-radius: 3px; }}
  </style>
</head>
<body>
  <h1>Post-Apply Current-Strict Closeout Audit</h1>
  <p>The original 20 old sandbox slices are audited after p2-91 status-only normalization.</p>
  <table>
    <thead><tr><th>Field</th><th>Value</th></tr></thead>
    <tbody>
{summary_items}
    </tbody>
  </table>
  <p>This artifact is audit-only and not a mainline merge, promotion, reviewed knowledge, evidence support, action basis, or Opus approval.</p>
</body>
</html>
"""


def write_outputs(report: dict) -> None:
    write_json(ARTIFACT_DIR / "post_apply_current_strict_closeout_audit.json", report)
    write_text(ARTIFACT_DIR / "post_apply_current_strict_closeout_audit.md", render_markdown(report))
    write_text(ARTIFACT_DIR / "post_apply_current_strict_closeout_audit.html", render_html(report))
    write_fixtures(report)
    write_failure_cases()


def main() -> None:
    report = build_report()
    write_outputs(report)
    print(json.dumps({"written": True, "summary": report["summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

