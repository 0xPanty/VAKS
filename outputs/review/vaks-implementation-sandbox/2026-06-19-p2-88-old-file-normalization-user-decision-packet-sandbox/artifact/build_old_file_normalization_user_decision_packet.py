from __future__ import annotations

import hashlib
import html
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-88-old-file-normalization-user-decision-packet-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT_DIR = SLICE_ROOT / "artifact"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURE_DIR = SLICE_ROOT / "failure-cases"

P2_75_CONTRACT = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request_contract.json"
P2_86_GATE_CHAIN = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-86-approval-to-prewrite-gate-chain-sandbox/artifact/approval_to_prewrite_gate_chain.json"
P2_87_DIFF_PREVIEW = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-87-old-file-status-normalization-diff-preview-sandbox/artifact/old_file_status_normalization_diff_preview.json"


def repo_path(rel: str) -> Path:
    return REPO_ROOT / rel


def read_json(rel: str) -> dict:
    return json.loads(repo_path(rel).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_file(rel: str) -> str:
    return hashlib.sha256(repo_path(rel).read_bytes()).hexdigest()


def build_failure_cases() -> None:
    payload = {
        "record_kind": "old_file_normalization_user_decision_packet_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {
                "case_id": "P2-88-FAIL-01-missing-exact-approval-phrase",
                "must_fail_when": "The decision packet omits or alters the exact p2-75 approval phrase.",
            },
            {
                "case_id": "P2-88-FAIL-02-generic-language-treated-as-approval",
                "must_fail_when": "Generic language such as continue, go ahead, or all done is treated as approval.",
            },
            {
                "case_id": "P2-88-FAIL-03-preview-count-not-75",
                "must_fail_when": "The packet does not carry the 75-operation p2-87 preview evidence.",
            },
            {
                "case_id": "P2-88-FAIL-04-preview-cleanliness-not-proven",
                "must_fail_when": "Hash match, body unchanged, non-status frontmatter unchanged, or old-write counts are wrong.",
            },
            {
                "case_id": "P2-88-FAIL-05-packet-authorizes-write",
                "must_fail_when": "The decision packet claims to authorize or execute old-file writes.",
            },
            {
                "case_id": "P2-88-FAIL-06-p2-75-gap-closed-without-user",
                "must_fail_when": "The artifact marks p2-75 exact approval as collected.",
            },
            {
                "case_id": "P2-88-FAIL-07-mainline-or-truth-authority",
                "must_fail_when": "The packet implies merge, promotion, reviewed knowledge, evidence support, or action basis.",
            },
            {
                "case_id": "P2-88-FAIL-08-missing-non-approval-option",
                "must_fail_when": "The packet lacks withhold, revise, or reject/park options.",
            },
        ],
    }
    write_json(FAILURE_DIR / "old-file-normalization-user-decision-packet-failures.json", payload)


def build_report() -> dict:
    p2_75 = read_json(P2_75_CONTRACT)
    p2_86 = read_json(P2_86_GATE_CHAIN)
    p2_87 = read_json(P2_87_DIFF_PREVIEW)
    previews = p2_87["preview_operations"]
    target_file_counts = Counter(Path(item["target_path"]).name for item in previews)
    proposed_status_counts = Counter(item["proposed_status"] for item in previews)
    exact_phrase = p2_75["exact_approval_phrase"]

    options = [
        {
            "option_id": "approve_with_exact_phrase",
            "label": "Approve status-only normalization with the exact phrase",
            "required_text": exact_phrase,
            "effect": "Allows a later executor slice to perform a final prewrite confirmation flow. This packet itself still does not write old files.",
            "old_file_write_allowed_by_this_packet": False,
        },
        {
            "option_id": "withhold_approval",
            "label": "Do not approve now",
            "required_text": "",
            "effect": "Keep original old-file statuses unchanged. The original 20 remain normalization candidates rather than current strict closeout.",
            "old_file_write_allowed_by_this_packet": False,
        },
        {
            "option_id": "request_revision",
            "label": "Ask for a revised packet or more evidence",
            "required_text": "",
            "effect": "Stay in sandbox and revise a future decision packet or preview artifact before any old-file write.",
            "old_file_write_allowed_by_this_packet": False,
        },
        {
            "option_id": "reject_or_park",
            "label": "Reject or park status normalization",
            "required_text": "",
            "effect": "Record that the old-file status-only normalization is not being applied without a later separate approval.",
            "old_file_write_allowed_by_this_packet": False,
        },
    ]

    return {
        "record_kind": "sandbox_old_file_normalization_user_decision_packet",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_75_contract": P2_75_CONTRACT,
            "p2_86_gate_chain": P2_86_GATE_CHAIN,
            "p2_87_diff_preview": P2_87_DIFF_PREVIEW,
        },
        "source_digest": {
            "p2_75_contract": sha256_file(P2_75_CONTRACT),
            "p2_86_gate_chain": sha256_file(P2_86_GATE_CHAIN),
            "p2_87_diff_preview": sha256_file(P2_87_DIFF_PREVIEW),
        },
        "summary": {
            "original_items": p2_75["expected_numbers"]["original_items"],
            "status_changes": p2_75["expected_numbers"]["status_changes"],
            "preview_operation_count": p2_87["summary"]["preview_operation_count"],
            "prewrite_hash_match_count": p2_87["summary"]["prewrite_hash_match_count"],
            "body_unchanged_count": p2_87["summary"]["body_unchanged_count"],
            "non_status_frontmatter_unchanged_count": p2_87["summary"]["non_status_frontmatter_unchanged_count"],
            "old_slice_writes_applied": p2_87["summary"]["old_slice_writes_applied"],
            "p2_86_executor_write_allowed_now": p2_86["summary"]["executor_write_allowed_now"],
            "p2_86_positive_ready_count": p2_86["summary"]["positive_ready_count"],
            "p2_75_exact_approval_collected": False,
            "decision_option_count": len(options),
        },
        "approval_contract": {
            "exact_approval_phrase": exact_phrase,
            "generic_language_is_not_approval": True,
            "non_approval_examples": p2_75["non_approval_examples"],
            "phrase_in_this_packet_is_instructional_only": True,
            "packet_collects_approval": False,
        },
        "decision_options": options,
        "change_summary": {
            "target_file_counts": dict(sorted(target_file_counts.items())),
            "proposed_status_counts": dict(sorted(proposed_status_counts.items())),
            "sample_operations": previews[:5],
            "full_preview_artifact": P2_87_DIFF_PREVIEW,
        },
        "readiness_chain": {
            "positive_ready_count": p2_86["summary"]["positive_ready_count"],
            "negative_blocked_count": p2_86["summary"]["negative_blocked_count"],
            "executor_write_allowed_now": p2_86["summary"]["executor_write_allowed_now"],
            "ready_state_name": "ready_for_prewrite_confirmation",
            "still_requires_stop_before_write": True,
        },
        "authority_flags": {
            "decision_packet_only": True,
            "phrase_display_is_user_approval": False,
            "user_approval_collected": False,
            "packet_authorizes_write": False,
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


def build_markdown(report: dict) -> str:
    phrase = report["approval_contract"]["exact_approval_phrase"]
    lines = [
        "---",
        f"slice_id: {SLICE_ID}",
        "status: generated",
        "---",
        "",
        "# Old-File Normalization User Decision Packet",
        "",
        "## Current State",
        "",
        f"- Original items: {report['summary']['original_items']}",
        f"- Proposed status-only changes: {report['summary']['status_changes']}",
        f"- Diff preview operations: {report['summary']['preview_operation_count']}",
        f"- Prewrite hash matches: {report['summary']['prewrite_hash_match_count']}/75",
        f"- Body unchanged: {report['summary']['body_unchanged_count']}/75",
        f"- Non-status frontmatter unchanged: {report['summary']['non_status_frontmatter_unchanged_count']}/75",
        f"- Old slice writes applied: {report['summary']['old_slice_writes_applied']}",
        f"- Executor write allowed now: {str(report['summary']['p2_86_executor_write_allowed_now']).lower()}",
        "",
        "## Exact Approval Phrase",
        "",
        "Only the exact phrase below can be treated as the old-file status-only normalization approval input for a later gate. This packet displaying the phrase is not approval.",
        "",
        "```text",
        phrase,
        "```",
        "",
        "## Decision Options",
        "",
        "| option | write allowed by this packet | effect |",
        "|---|---:|---|",
    ]
    for option in report["decision_options"]:
        lines.append(
            f"| `{option['option_id']}` | `{str(option['old_file_write_allowed_by_this_packet']).lower()}` | {option['effect']} |"
        )
    lines.extend(
        [
            "",
            "## Change Summary",
            "",
            "### Target File Counts",
            "",
        ]
    )
    for name, count in report["change_summary"]["target_file_counts"].items():
        lines.append(f"- `{name}`: {count}")
    lines.extend(["", "### Proposed Status Counts", ""])
    for status, count in report["change_summary"]["proposed_status_counts"].items():
        lines.append(f"- `{status}`: {count}")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This is a decision packet only. It does not collect approval, authorize writes, apply normalization, merge mainline, promote knowledge, create reviewed knowledge, create evidence support, create action basis, or complete the goal.",
            "",
        ]
    )
    return "\n".join(lines)


def build_html(report: dict) -> str:
    phrase = html.escape(report["approval_contract"]["exact_approval_phrase"])
    metrics = report["summary"]
    options = "\n".join(
        f"<tr><td>{html.escape(option['option_id'])}</td><td>{str(option['old_file_write_allowed_by_this_packet']).lower()}</td><td>{html.escape(option['effect'])}</td></tr>"
        for option in report["decision_options"]
    )
    file_counts = "\n".join(
        f"<li><code>{html.escape(name)}</code>: {count}</li>"
        for name, count in report["change_summary"]["target_file_counts"].items()
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>p2-88 Old-File Normalization Decision Packet</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; color: #202832; background: #f7f8fa; }}
    main {{ max-width: 1080px; margin: 0 auto; padding: 32px 20px; }}
    h1 {{ font-size: 28px; margin: 0 0 16px; letter-spacing: 0; }}
    h2 {{ font-size: 18px; margin-top: 24px; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; }}
    .metric {{ background: #fff; border: 1px solid #d9e0e8; border-radius: 8px; padding: 14px; }}
    .metric span {{ display: block; color: #596575; font-size: 13px; }}
    .metric strong {{ display: block; margin-top: 6px; font-size: 24px; }}
    pre {{ white-space: pre-wrap; background: #1f2933; color: #f4f7fb; border-radius: 8px; padding: 14px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #d9e0e8; }}
    th, td {{ padding: 9px 10px; border-bottom: 1px solid #e6ebf0; text-align: left; vertical-align: top; }}
    .boundary {{ margin-top: 20px; background: #fff4f2; border-left: 4px solid #a63d40; padding: 14px; }}
  </style>
</head>
<body>
  <main>
    <h1>p2-88 Old-File Normalization Decision Packet</h1>
    <section class="metrics">
      <div class="metric"><span>Preview operations</span><strong>{metrics['preview_operation_count']}</strong></div>
      <div class="metric"><span>Hash matches</span><strong>{metrics['prewrite_hash_match_count']}/75</strong></div>
      <div class="metric"><span>Body unchanged</span><strong>{metrics['body_unchanged_count']}/75</strong></div>
      <div class="metric"><span>Old writes</span><strong>{metrics['old_slice_writes_applied']}</strong></div>
    </section>
    <h2>Exact Approval Phrase</h2>
    <pre>{phrase}</pre>
    <h2>Decision Options</h2>
    <table><thead><tr><th>Option</th><th>Write Allowed By Packet</th><th>Effect</th></tr></thead><tbody>{options}</tbody></table>
    <h2>Target File Counts</h2>
    <ul>{file_counts}</ul>
    <section class="boundary">Decision packet only. It is not approval, write authority, merge, promotion, reviewed knowledge, evidence support, action basis, or goal completion.</section>
  </main>
</body>
</html>
"""


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    write_json(ARTIFACT_DIR / "old_file_normalization_user_decision_packet.json", report)
    (ARTIFACT_DIR / "old_file_normalization_user_decision_packet.md").write_text(build_markdown(report), encoding="utf-8")
    (ARTIFACT_DIR / "old_file_normalization_user_decision_packet.html").write_text(build_html(report), encoding="utf-8")
    build_failure_cases()

    fixtures = {
        "exact-approval-phrase-present.json": {
            "case_id": "exact-approval-phrase-present",
            "exact_approval_phrase": report["approval_contract"]["exact_approval_phrase"],
            "phrase_in_this_packet_is_instructional_only": True,
        },
        "generic-language-still-not-approval.json": {
            "case_id": "generic-language-still-not-approval",
            "non_approval_examples": report["approval_contract"]["non_approval_examples"],
            "generic_language_is_not_approval": True,
        },
        "diff-preview-75-clean.json": {
            "case_id": "diff-preview-75-clean",
            "preview_operation_count": report["summary"]["preview_operation_count"],
            "prewrite_hash_match_count": report["summary"]["prewrite_hash_match_count"],
            "body_unchanged_count": report["summary"]["body_unchanged_count"],
            "non_status_frontmatter_unchanged_count": report["summary"]["non_status_frontmatter_unchanged_count"],
            "old_slice_writes_applied": report["summary"]["old_slice_writes_applied"],
        },
        "decision-options-no-write-authority.json": {
            "case_id": "decision-options-no-write-authority",
            "decision_option_count": report["summary"]["decision_option_count"],
            "any_option_writes_now": any(option["old_file_write_allowed_by_this_packet"] for option in report["decision_options"]),
        },
        "p2-75-gap-preserved.json": {
            "case_id": "p2-75-gap-preserved",
            "p2_75_exact_approval_collected": report["summary"]["p2_75_exact_approval_collected"],
            "packet_collects_approval": report["approval_contract"]["packet_collects_approval"],
        },
    }
    for name, fixture in fixtures.items():
        write_json(FIXTURES_DIR / name, fixture)
    print(json.dumps({"built": True, "slice_id": SLICE_ID}, indent=2))


if __name__ == "__main__":
    main()
