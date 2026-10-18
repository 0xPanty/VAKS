from __future__ import annotations

import hashlib
import html
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT_DIR = SLICE_ROOT / "artifact"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURE_DIR = SLICE_ROOT / "failure-cases"

APPROVAL_TEXT = "I explicitly approve p2-75 old-file status-only normalization: apply the 75 dry-run frontmatter status changes from p2-72 to the original 20 sandbox slice reports only. Do not edit body content, artifacts, tools, templates, wiki truth layers, main architecture docs, README, Obsidian vault, commit, push, or sync."
P2_80 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/artifact/old_file_status_normalization_transaction_package.json"
P2_90 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-90-post-approval-executor-handoff-sandbox/artifact/post_approval_executor_handoff.json"


def repo_path(rel: str) -> Path:
    return REPO_ROOT / rel


def read_json(rel: str) -> dict:
    return json.loads(repo_path(rel).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


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


def build_failure_cases() -> None:
    payload = {
        "record_kind": "old_file_status_normalization_executor_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {
                "case_id": "P2-91-FAIL-01-missing-exact-approval",
                "must_fail_when": "The exact p2-75 approval phrase is not present.",
            },
            {
                "case_id": "P2-91-FAIL-02-prewrite-hash-drift",
                "must_fail_when": "Any target file hash differs from the p2-80 prewrite hash before execution.",
            },
            {
                "case_id": "P2-91-FAIL-03-current-status-mismatch",
                "must_fail_when": "Any target status differs from the p2-80 before status before execution.",
            },
            {
                "case_id": "P2-91-FAIL-04-body-drift",
                "must_fail_when": "Any operation changes body content.",
            },
            {
                "case_id": "P2-91-FAIL-05-non-status-frontmatter-drift",
                "must_fail_when": "Any operation changes non-status frontmatter.",
            },
            {
                "case_id": "P2-91-FAIL-06-wrong-target-or-count",
                "must_fail_when": "The executor writes anything other than the 75 p2-80 target files.",
            },
            {
                "case_id": "P2-91-FAIL-07-protected-path-write",
                "must_fail_when": "The executor writes artifacts, tools, templates, wiki truth layers, root docs, README, Obsidian, commit, push, or sync.",
            },
            {
                "case_id": "P2-91-FAIL-08-mainline-or-truth-authority",
                "must_fail_when": "The executor output claims merge, promotion, reviewed knowledge, evidence support, action basis, or mainline readiness.",
            },
        ],
    }
    write_json(FAILURE_DIR / "old-file-status-normalization-executor-failures.json", payload)


def plan_operation(op: dict) -> dict:
    target = repo_path(op["target_path"])
    raw_before = target.read_bytes()
    before_sha = sha256_bytes(raw_before)
    text_before = raw_before.decode("utf-8")
    parsed_before = parse_frontmatter(text_before)
    lines = list(parsed_before["lines"])
    old_line_body, newline = split_newline(lines[parsed_before["status_index"]])
    prefix = old_line_body.split("status:", 1)[0]
    new_line = f"{prefix}status: {op['proposed_status']}{newline}"
    lines[parsed_before["status_index"]] = new_line
    text_after = "".join(lines)
    raw_after = text_after.encode("utf-8")
    parsed_after = parse_frontmatter(text_after)
    return {
        "operation_index": op["operation_index"],
        "old_slice_id": op["old_slice_id"],
        "target_path": op["target_path"],
        "before_status": parsed_before["status_value"],
        "expected_before_status": op["before_status"],
        "proposed_status": op["proposed_status"],
        "rollback_status": op["rollback_status"],
        "prewrite_required_hash": op["prewrite_required_hash"],
        "prewrite_sha256": before_sha,
        "prewrite_hash_match": before_sha == op["prewrite_required_hash"],
        "prewrite_status_match": parsed_before["status_value"] == op["before_status"],
        "status_line_delta": {
            "before": old_line_body,
            "after": new_line.rstrip("\r\n"),
        },
        "post_apply_sha256_expected": sha256_bytes(raw_after),
        "body_sha256_before": sha256_bytes(parsed_before["body_text"].encode("utf-8")),
        "body_sha256_after_expected": sha256_bytes(parsed_after["body_text"].encode("utf-8")),
        "body_unchanged_expected": parsed_before["body_text"] == parsed_after["body_text"],
        "non_status_frontmatter_sha256_before": sha256_bytes(
            parsed_before["non_status_frontmatter_text"].encode("utf-8")
        ),
        "non_status_frontmatter_sha256_after_expected": sha256_bytes(
            parsed_after["non_status_frontmatter_text"].encode("utf-8")
        ),
        "non_status_frontmatter_unchanged_expected": parsed_before["non_status_frontmatter_text"]
        == parsed_after["non_status_frontmatter_text"],
        "raw_after_text": text_after,
    }


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)
    p80 = read_json(P2_80)
    p90 = read_json(P2_90)
    operations = p80["transaction_operations"]
    exact_phrase = p90["future_prerequisites"]["exact_approval_phrase"]
    approval_exact_match = APPROVAL_TEXT == exact_phrase
    planned = [plan_operation(op) for op in operations]

    blockers = []
    if not approval_exact_match:
        blockers.append("missing_exact_approval")
    if len(planned) != 75:
        blockers.append("operation_count_not_75")
    if any(not item["prewrite_hash_match"] for item in planned):
        blockers.append("prewrite_hash_mismatch")
    if any(not item["prewrite_status_match"] for item in planned):
        blockers.append("prewrite_status_mismatch")
    if any(not item["body_unchanged_expected"] for item in planned):
        blockers.append("body_change_planned")
    if any(not item["non_status_frontmatter_unchanged_expected"] for item in planned):
        blockers.append("non_status_frontmatter_change_planned")
    if len({item["target_path"] for item in planned}) != 75:
        blockers.append("target_path_count_not_75")
    if blockers:
        write_json(
            ARTIFACT_DIR / "old_file_status_normalization_executor_apply.json",
            {
                "record_kind": "sandbox_old_file_status_normalization_executor_apply",
                "slice_id": SLICE_ID,
                "created_at": datetime.now(timezone.utc).isoformat(),
                "passed_prewrite": False,
                "blockers": blockers,
            },
        )
        raise SystemExit(f"blocked before write: {blockers}")

    for item in planned:
        repo_path(item["target_path"]).write_bytes(item["raw_after_text"].encode("utf-8"))

    execution_ops = []
    for item in planned:
        raw_current = repo_path(item["target_path"]).read_bytes()
        parsed_current = parse_frontmatter(raw_current.decode("utf-8"))
        execution_ops.append(
            {
                key: value
                for key, value in item.items()
                if key != "raw_after_text"
            }
            | {
                "post_apply_sha256_actual": sha256_bytes(raw_current),
                "post_apply_status_actual": parsed_current["status_value"],
                "post_apply_status_match": parsed_current["status_value"] == item["proposed_status"],
                "body_sha256_after_actual": sha256_bytes(parsed_current["body_text"].encode("utf-8")),
                "non_status_frontmatter_sha256_after_actual": sha256_bytes(
                    parsed_current["non_status_frontmatter_text"].encode("utf-8")
                ),
                "body_unchanged_actual": sha256_bytes(parsed_current["body_text"].encode("utf-8"))
                == item["body_sha256_before"],
                "non_status_frontmatter_unchanged_actual": sha256_bytes(
                    parsed_current["non_status_frontmatter_text"].encode("utf-8")
                )
                == item["non_status_frontmatter_sha256_before"],
                "write_applied": True,
            }
        )

    report = {
        "record_kind": "sandbox_old_file_status_normalization_executor_apply",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_80_transaction_package": P2_80,
            "p2_90_executor_handoff": P2_90,
        },
        "approval": {
            "exact_p2_75_approval_phrase_present": approval_exact_match,
            "approval_text": APPROVAL_TEXT,
        },
        "summary": {
            "passed_prewrite": True,
            "transaction_operation_count": len(execution_ops),
            "unique_target_file_count": len({item["target_path"] for item in execution_ops}),
            "prewrite_hash_match_count": sum(1 for item in execution_ops if item["prewrite_hash_match"]),
            "prewrite_status_match_count": sum(1 for item in execution_ops if item["prewrite_status_match"]),
            "post_apply_status_match_count": sum(1 for item in execution_ops if item["post_apply_status_match"]),
            "body_unchanged_count": sum(1 for item in execution_ops if item["body_unchanged_actual"]),
            "non_status_frontmatter_unchanged_count": sum(
                1 for item in execution_ops if item["non_status_frontmatter_unchanged_actual"]
            ),
            "old_slice_writes_applied": len(execution_ops),
            "protected_path_writes": 0,
            "normalization_applied": True,
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
        },
        "execution_operations": execution_ops,
        "rollback_plan": [
            {
                "target_path": item["target_path"],
                "rollback_status": item["rollback_status"],
                "prewrite_sha256": item["prewrite_sha256"],
                "post_apply_sha256": item["post_apply_sha256_actual"],
            }
            for item in execution_ops
        ],
        "authority_flags": {
            "approved_status_only_old_file_normalization": True,
            "body_content_edits_allowed": False,
            "artifact_edits_allowed": False,
            "tools_templates_edits_allowed": False,
            "wiki_truth_layer_edits_allowed": False,
            "mainline_edits_allowed": False,
            "obsidian_sync_allowed": False,
            "commit_push_allowed": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": False,
        },
    }
    write_json(ARTIFACT_DIR / "old_file_status_normalization_executor_apply.json", report)
    write_json(
        FIXTURES_DIR / "all-75-status-only-writes-applied.json",
        {
            "case_id": "all-75-status-only-writes-applied",
            "old_slice_writes_applied": report["summary"]["old_slice_writes_applied"],
            "post_apply_status_match_count": report["summary"]["post_apply_status_match_count"],
        },
    )
    write_json(
        FIXTURES_DIR / "body-content-unchanged-after-apply.json",
        {
            "case_id": "body-content-unchanged-after-apply",
            "body_unchanged_count": report["summary"]["body_unchanged_count"],
        },
    )
    write_json(
        FIXTURES_DIR / "non-status-frontmatter-unchanged-after-apply.json",
        {
            "case_id": "non-status-frontmatter-unchanged-after-apply",
            "non_status_frontmatter_unchanged_count": report["summary"][
                "non_status_frontmatter_unchanged_count"
            ],
        },
    )
    write_json(
        FIXTURES_DIR / "protected-paths-not-written.json",
        {
            "case_id": "protected-paths-not-written",
            "protected_path_writes": report["summary"]["protected_path_writes"],
        },
    )
    write_json(
        FIXTURES_DIR / "sandbox-not-mainline-authority.json",
        {
            "case_id": "sandbox-not-mainline-authority",
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "action_basis_ready": False,
        },
    )
    build_failure_cases()
    write_markdown(report)
    write_html(report)
    print(json.dumps({"applied": True, "slice_id": SLICE_ID}, indent=2))


def write_markdown(report: dict) -> None:
    lines = [
        "---",
        f"slice_id: {SLICE_ID}",
        "status: generated",
        "---",
        "",
        "# Old-File Status Normalization Executor Apply",
        "",
        "## Summary",
        "",
    ]
    for key, value in report["summary"].items():
        lines.append(f"- {key}: {value}")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This applied only the approved 75 old sandbox report `frontmatter.status` lines. It does not merge mainline, promote knowledge, create reviewed knowledge, create evidence support, create action basis, commit, push, sync, or edit protected paths.",
            "",
        ]
    )
    (ARTIFACT_DIR / "old_file_status_normalization_executor_apply.md").write_text(
        "\n".join(lines), encoding="utf-8"
    )


def write_html(report: dict) -> None:
    metrics = report["summary"]
    rows = "\n".join(
        f"<tr><td>{op['operation_index']}</td><td>{html.escape(op['target_path'])}</td><td>{html.escape(op['before_status'])}</td><td>{html.escape(op['proposed_status'])}</td><td>{str(op['body_unchanged_actual']).lower()}</td></tr>"
        for op in report["execution_operations"]
    )
    html_text = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>p2-91 Executor Apply</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fa; color: #202832; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 32px 20px; }}
    h1 {{ font-size: 28px; margin: 0 0 16px; letter-spacing: 0; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; }}
    .metric {{ background: #fff; border: 1px solid #d9e0e8; border-radius: 8px; padding: 14px; }}
    .metric span {{ display: block; color: #596575; font-size: 13px; }}
    .metric strong {{ display: block; margin-top: 6px; font-size: 24px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #d9e0e8; font-size: 13px; margin-top: 20px; }}
    th, td {{ padding: 8px 10px; border-bottom: 1px solid #e6ebf0; text-align: left; vertical-align: top; }}
    .boundary {{ margin-top: 20px; background: #fff4f2; border-left: 4px solid #a63d40; padding: 14px; }}
  </style>
</head>
<body>
  <main>
    <h1>p2-91 Executor Apply</h1>
    <section class="metrics">
      <div class="metric"><span>Writes Applied</span><strong>{metrics['old_slice_writes_applied']}</strong></div>
      <div class="metric"><span>Status Matches</span><strong>{metrics['post_apply_status_match_count']}/75</strong></div>
      <div class="metric"><span>Body Unchanged</span><strong>{metrics['body_unchanged_count']}/75</strong></div>
      <div class="metric"><span>Protected Writes</span><strong>{metrics['protected_path_writes']}</strong></div>
    </section>
    <table><thead><tr><th>#</th><th>Target</th><th>Before</th><th>After</th><th>Body Unchanged</th></tr></thead><tbody>{rows}</tbody></table>
    <section class="boundary">Sandbox old-file status-only normalization only. No mainline, tools, templates, wiki truth layer, Obsidian, commit, push, or sync authority.</section>
  </main>
</body>
</html>
"""
    (ARTIFACT_DIR / "old_file_status_normalization_executor_apply.html").write_text(html_text, encoding="utf-8")


if __name__ == "__main__":
    main()
