from __future__ import annotations

import hashlib
import html
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-87-old-file-status-normalization-diff-preview-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT_DIR = SLICE_ROOT / "artifact"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURE_DIR = SLICE_ROOT / "failure-cases"

P2_80 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/artifact/old_file_status_normalization_transaction_package.json"
P2_86 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-86-approval-to-prewrite-gate-chain-sandbox/artifact/approval_to_prewrite_gate_chain.json"


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


def preview_operation(op: dict) -> dict:
    target_path = op["target_path"]
    raw = repo_path(target_path).read_bytes()
    before_sha = sha256_bytes(raw)
    text = raw.decode("utf-8")
    parsed = parse_frontmatter(text)
    before_status = parsed["status_value"]
    proposed_status = op["proposed_status"]
    rollback_status = op["rollback_status"]

    lines = list(parsed["lines"])
    old_line_body, newline = split_newline(lines[parsed["status_index"]])
    prefix = old_line_body.split("status:", 1)[0]
    proposed_line = f"{prefix}status: {proposed_status}{newline}"
    lines[parsed["status_index"]] = proposed_line
    proposed_text = "".join(lines)
    proposed_bytes = proposed_text.encode("utf-8")
    proposed_sha = sha256_bytes(proposed_bytes)
    proposed_parsed = parse_frontmatter(proposed_text)

    return {
        "operation_index": op["operation_index"],
        "old_slice_id": op["old_slice_id"],
        "target_path": target_path,
        "field": op["field"],
        "before_status": before_status,
        "manifest_current_status": op["manifest_current_status"],
        "proposed_status": proposed_status,
        "rollback_status": rollback_status,
        "status_line_delta": {
            "before": old_line_body,
            "after": proposed_line.rstrip("\r\n"),
        },
        "before_sha256": before_sha,
        "prewrite_required_hash": op["prewrite_required_hash"],
        "before_hash_matches_prewrite_required": before_sha == op["prewrite_required_hash"],
        "proposed_sha256": proposed_sha,
        "body_sha256_before": sha256_bytes(parsed["body_text"].encode("utf-8")),
        "body_sha256_after": sha256_bytes(proposed_parsed["body_text"].encode("utf-8")),
        "body_unchanged": parsed["body_text"] == proposed_parsed["body_text"],
        "non_status_frontmatter_sha256_before": sha256_bytes(parsed["non_status_frontmatter_text"].encode("utf-8")),
        "non_status_frontmatter_sha256_after": sha256_bytes(proposed_parsed["non_status_frontmatter_text"].encode("utf-8")),
        "non_status_frontmatter_unchanged": parsed["non_status_frontmatter_text"]
        == proposed_parsed["non_status_frontmatter_text"],
        "proposed_status_applied_in_preview": proposed_parsed["status_value"] == proposed_status,
        "old_slice_write_applied": False,
        "preview_only": True,
    }


def build_failure_cases() -> None:
    payload = {
        "record_kind": "old_file_status_normalization_diff_preview_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {
                "case_id": "P2-87-FAIL-01-incomplete-preview",
                "must_fail_when": "The preview does not include all 75 operations.",
            },
            {
                "case_id": "P2-87-FAIL-02-body-drift",
                "must_fail_when": "Any operation changes body content.",
            },
            {
                "case_id": "P2-87-FAIL-03-non-status-frontmatter-drift",
                "must_fail_when": "Any operation changes non-status frontmatter.",
            },
            {
                "case_id": "P2-87-FAIL-04-prewrite-hash-mismatch",
                "must_fail_when": "Any target hash differs from p2-80 prewrite hash.",
            },
            {
                "case_id": "P2-87-FAIL-05-status-not-applied-in-preview",
                "must_fail_when": "A proposed preview does not set the proposed status.",
            },
            {
                "case_id": "P2-87-FAIL-06-old-slice-write",
                "must_fail_when": "The preview writes old slice files.",
            },
            {
                "case_id": "P2-87-FAIL-07-preview-as-approval",
                "must_fail_when": "The preview is treated as user approval or write authority.",
            },
            {
                "case_id": "P2-87-FAIL-08-mainline-authority",
                "must_fail_when": "The preview implies mainline, promotion, reviewed knowledge, evidence support, or action basis.",
            },
        ],
    }
    write_json(FAILURE_DIR / "old-file-status-normalization-diff-preview-failures.json", payload)


def build_markdown(report: dict) -> str:
    lines = [
        "---",
        f"slice_id: {SLICE_ID}",
        "status: generated",
        "---",
        "",
        "# Old-File Status Normalization Diff Preview",
        "",
        "## Summary",
        "",
        f"- preview_operation_count: {report['summary']['preview_operation_count']}",
        f"- prewrite_hash_match_count: {report['summary']['prewrite_hash_match_count']}",
        f"- body_unchanged_count: {report['summary']['body_unchanged_count']}",
        f"- non_status_frontmatter_unchanged_count: {report['summary']['non_status_frontmatter_unchanged_count']}",
        f"- old_slice_writes_applied: {report['summary']['old_slice_writes_applied']}",
        "",
        "## All 75 Preview Rows",
        "",
        "| # | target | before | proposed | rollback | delta |",
        "|---:|---|---|---|---|---|",
    ]
    for item in report["preview_operations"]:
        target = item["target_path"].replace("|", "\\|")
        delta = f"`- {item['status_line_delta']['before']}`<br>`+ {item['status_line_delta']['after']}`"
        lines.append(
            f"| {item['operation_index']} | `{target}` | `{item['before_status']}` | `{item['proposed_status']}` | `{item['rollback_status']}` | {delta} |"
        )
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a preview-only sandbox artifact. It does not write old files, collect approval, or authorize execution.",
            "",
        ]
    )
    return "\n".join(lines)


def build_html(report: dict) -> str:
    rows = "\n".join(
        f"<tr><td>{item['operation_index']}</td><td>{html.escape(item['target_path'])}</td><td>{html.escape(item['before_status'])}</td><td>{html.escape(item['proposed_status'])}</td><td>{str(item['body_unchanged']).lower()}</td></tr>"
        for item in report["preview_operations"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>p2-87 Status Diff Preview</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fa; color: #1d2530; }}
    main {{ max-width: 1180px; margin: 0 auto; padding: 32px 20px; }}
    h1 {{ font-size: 28px; margin: 0 0 16px; letter-spacing: 0; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; margin-bottom: 22px; }}
    .metric {{ background: #fff; border: 1px solid #d9e0e8; border-radius: 8px; padding: 14px; }}
    .metric span {{ display: block; color: #596575; font-size: 13px; }}
    .metric strong {{ display: block; font-size: 24px; margin-top: 6px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #d9e0e8; font-size: 13px; }}
    th, td {{ text-align: left; padding: 8px 10px; border-bottom: 1px solid #e5e9ef; vertical-align: top; }}
    th {{ color: #526070; }}
    .boundary {{ margin-top: 20px; background: #fff4f2; border-left: 4px solid #a63d40; padding: 14px; }}
  </style>
</head>
<body>
  <main>
    <h1>p2-87 Status Diff Preview</h1>
    <section class="metrics">
      <div class="metric"><span>Operations</span><strong>{report['summary']['preview_operation_count']}</strong></div>
      <div class="metric"><span>Prewrite hash match</span><strong>{report['summary']['prewrite_hash_match_count']}/75</strong></div>
      <div class="metric"><span>Body unchanged</span><strong>{report['summary']['body_unchanged_count']}/75</strong></div>
      <div class="metric"><span>Old writes</span><strong>{report['summary']['old_slice_writes_applied']}</strong></div>
    </section>
    <table>
      <thead><tr><th>#</th><th>Target</th><th>Before</th><th>Proposed</th><th>Body Unchanged</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <section class="boundary">Preview only. No old slice files are written or authorized by this artifact.</section>
  </main>
</body>
</html>
"""


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)

    p2_80 = read_json(P2_80)
    p2_86 = read_json(P2_86)
    operations = p2_80["transaction_operations"]
    previews = [preview_operation(op) for op in operations]

    report = {
        "record_kind": "sandbox_old_file_status_normalization_diff_preview",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_80_transaction_package": P2_80,
            "p2_86_gate_chain": P2_86,
        },
        "source_digest": {
            "p2_80_transaction_package": sha256_bytes(repo_path(P2_80).read_bytes()),
            "p2_86_gate_chain": sha256_bytes(repo_path(P2_86).read_bytes()),
        },
        "summary": {
            "preview_operation_count": len(previews),
            "unique_target_file_count": len({item["target_path"] for item in previews}),
            "prewrite_hash_match_count": sum(1 for item in previews if item["before_hash_matches_prewrite_required"]),
            "body_unchanged_count": sum(1 for item in previews if item["body_unchanged"]),
            "non_status_frontmatter_unchanged_count": sum(
                1 for item in previews if item["non_status_frontmatter_unchanged"]
            ),
            "proposed_status_applied_count": sum(1 for item in previews if item["proposed_status_applied_in_preview"]),
            "p2_86_positive_ready_count": p2_86["summary"]["positive_ready_count"],
            "p2_86_executor_write_allowed_now": p2_86["summary"]["executor_write_allowed_now"],
            "old_slice_writes_applied": 0,
            "preview_authorizes_write": False,
        },
        "preview_operations": previews,
        "authority_flags": {
            "diff_preview_only": True,
            "approval_collected": False,
            "preview_is_user_approval": False,
            "preview_is_write_authority": False,
            "executor_write_allowed": False,
            "old_slice_write_allowed": False,
            "old_slice_writes_applied": 0,
            "normalization_applied": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": False,
        },
    }
    write_json(ARTIFACT_DIR / "old_file_status_normalization_diff_preview.json", report)
    (ARTIFACT_DIR / "old_file_status_normalization_diff_preview.md").write_text(build_markdown(report), encoding="utf-8")
    (ARTIFACT_DIR / "old_file_status_normalization_diff_preview.html").write_text(build_html(report), encoding="utf-8")
    build_failure_cases()

    fixtures = {
        "all-75-previews-present.json": {
            "case_id": "all-75-previews-present",
            "expected_preview_operation_count": 75,
            "observed_preview_operation_count": len(previews),
        },
        "body-content-unchanged.json": {
            "case_id": "body-content-unchanged",
            "expected_body_unchanged_count": 75,
            "observed_body_unchanged_count": report["summary"]["body_unchanged_count"],
        },
        "non-status-frontmatter-unchanged.json": {
            "case_id": "non-status-frontmatter-unchanged",
            "expected_non_status_frontmatter_unchanged_count": 75,
            "observed_non_status_frontmatter_unchanged_count": report["summary"][
                "non_status_frontmatter_unchanged_count"
            ],
        },
        "prewrite-hashes-match.json": {
            "case_id": "prewrite-hashes-match",
            "expected_prewrite_hash_match_count": 75,
            "observed_prewrite_hash_match_count": report["summary"]["prewrite_hash_match_count"],
        },
        "preview-not-write-authority.json": {
            "case_id": "preview-not-write-authority",
            "old_slice_writes_applied": 0,
            "preview_authorizes_write": False,
        },
    }
    for name, fixture in fixtures.items():
        write_json(FIXTURES_DIR / name, fixture)
    print(json.dumps({"built": True, "slice_id": SLICE_ID}, indent=2))


if __name__ == "__main__":
    main()
