from __future__ import annotations

import hashlib
import html
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-89-approval-dependency-closeout-packet-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT_DIR = SLICE_ROOT / "artifact"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURE_DIR = SLICE_ROOT / "failure-cases"

P2_75 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request_contract.json"
P2_86 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-86-approval-to-prewrite-gate-chain-sandbox/artifact/approval_to_prewrite_gate_chain.json"
P2_87 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-87-old-file-status-normalization-diff-preview-sandbox/artifact/old_file_status_normalization_diff_preview.json"
P2_88 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-88-old-file-normalization-user-decision-packet-sandbox/artifact/old_file_normalization_user_decision_packet.json"


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
        "record_kind": "approval_dependency_closeout_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {
                "case_id": "P2-89-FAIL-01-claims-approval-collected",
                "must_fail_when": "The packet says exact p2-75 approval has been collected.",
            },
            {
                "case_id": "P2-89-FAIL-02-executor-write-allowed",
                "must_fail_when": "The packet allows executor writes now.",
            },
            {
                "case_id": "P2-89-FAIL-03-old-writes-applied",
                "must_fail_when": "The packet reports any old-file write.",
            },
            {
                "case_id": "P2-89-FAIL-04-goal-complete",
                "must_fail_when": "The packet claims the full goal is complete.",
            },
            {
                "case_id": "P2-89-FAIL-05-missing-technical-evidence",
                "must_fail_when": "The packet omits 75 preview/hash/body/non-status/old-write evidence.",
            },
            {
                "case_id": "P2-89-FAIL-06-missing-next-stop-rule",
                "must_fail_when": "The packet omits the exact-approval plus fresh-prewrite stop rule.",
            },
            {
                "case_id": "P2-89-FAIL-07-mainline-or-truth-authority",
                "must_fail_when": "The packet implies merge, promotion, reviewed knowledge, evidence support, or action basis.",
            },
            {
                "case_id": "P2-89-FAIL-08-missing-user-decision-link",
                "must_fail_when": "The packet omits the p2-88 decision packet as the user-facing decision surface.",
            },
        ],
    }
    write_json(FAILURE_DIR / "approval-dependency-closeout-failures.json", payload)


def build_report() -> dict:
    p75 = read_json(P2_75)
    p86 = read_json(P2_86)
    p87 = read_json(P2_87)
    p88 = read_json(P2_88)
    exact_phrase = p75["exact_approval_phrase"]

    return {
        "record_kind": "sandbox_approval_dependency_closeout_packet",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_75_approval_contract": P2_75,
            "p2_86_gate_chain": P2_86,
            "p2_87_diff_preview": P2_87,
            "p2_88_user_decision_packet": P2_88,
        },
        "source_digest": {
            "p2_75_approval_contract": sha256_file(P2_75),
            "p2_86_gate_chain": sha256_file(P2_86),
            "p2_87_diff_preview": sha256_file(P2_87),
            "p2_88_user_decision_packet": sha256_file(P2_88),
        },
        "technical_readiness": {
            "status": "ready_for_user_decision_not_ready_to_write",
            "original_items": p75["expected_numbers"]["original_items"],
            "status_changes": p75["expected_numbers"]["status_changes"],
            "preview_operation_count": p87["summary"]["preview_operation_count"],
            "prewrite_hash_match_count": p87["summary"]["prewrite_hash_match_count"],
            "body_unchanged_count": p87["summary"]["body_unchanged_count"],
            "non_status_frontmatter_unchanged_count": p87["summary"]["non_status_frontmatter_unchanged_count"],
            "old_slice_writes_applied": p87["summary"]["old_slice_writes_applied"],
            "decision_option_count": p88["summary"]["decision_option_count"],
            "p2_86_positive_ready_count": p86["summary"]["positive_ready_count"],
            "p2_86_negative_blocked_count": p86["summary"]["negative_blocked_count"],
        },
        "approval_dependency": {
            "blocking_condition": "missing_exact_p2_75_user_approval",
            "exact_approval_phrase": exact_phrase,
            "exact_approval_collected": False,
            "generic_language_is_not_approval": True,
            "decision_packet": P2_88,
        },
        "executor_status": {
            "executor_write_allowed_now": False,
            "ready_for_prewrite_confirmation_only": True,
            "requires_exact_approval_before_executor_slice": True,
            "requires_fresh_prewrite_gate_after_approval": True,
            "requires_stop_before_any_old_file_write": True,
            "old_slice_write_allowed": False,
        },
        "operator_summary": {
            "plain_verdict": "All known sandbox preparation artifacts are product-grade through p2-88, but old-file normalization is not applied and the full goal is not complete.",
            "safe_next_actions": [
                "Wait for the exact p2-75 approval phrase.",
                "If the exact phrase is provided, run a fresh prewrite gate before any executor write.",
                "If approval is withheld, leave old files unchanged and keep this as the closeout state.",
            ],
            "unsafe_actions": [
                "Do not treat continue, all done, go ahead, or product-grade as approval.",
                "Do not write old files from this packet.",
                "Do not merge mainline, promote knowledge, create reviewed knowledge, evidence support, or action basis from this packet.",
            ],
        },
        "authority_flags": {
            "closeout_packet_only": True,
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
    readiness = report["technical_readiness"]
    dependency = report["approval_dependency"]
    executor = report["executor_status"]
    lines = [
        "---",
        f"slice_id: {SLICE_ID}",
        "status: generated",
        "---",
        "",
        "# Approval Dependency Closeout Packet",
        "",
        "## Plain Verdict",
        "",
        report["operator_summary"]["plain_verdict"],
        "",
        "## Technical Readiness",
        "",
        f"- status_changes: {readiness['status_changes']}",
        f"- preview_operation_count: {readiness['preview_operation_count']}",
        f"- prewrite_hash_match_count: {readiness['prewrite_hash_match_count']}/75",
        f"- body_unchanged_count: {readiness['body_unchanged_count']}/75",
        f"- non_status_frontmatter_unchanged_count: {readiness['non_status_frontmatter_unchanged_count']}/75",
        f"- old_slice_writes_applied: {readiness['old_slice_writes_applied']}",
        f"- decision_option_count: {readiness['decision_option_count']}",
        "",
        "## Approval Dependency",
        "",
        f"- blocking_condition: `{dependency['blocking_condition']}`",
        f"- exact_approval_collected: `{str(dependency['exact_approval_collected']).lower()}`",
        f"- generic_language_is_not_approval: `{str(dependency['generic_language_is_not_approval']).lower()}`",
        "",
        "```text",
        dependency["exact_approval_phrase"],
        "```",
        "",
        "## Executor Status",
        "",
    ]
    for key, value in executor.items():
        lines.append(f"- {key}: `{str(value).lower()}`")
    lines.extend(["", "## Safe Next Actions", ""])
    for item in report["operator_summary"]["safe_next_actions"]:
        lines.append(f"- {item}")
    lines.extend(["", "## Unsafe Actions", ""])
    for item in report["operator_summary"]["unsafe_actions"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This closeout packet is not approval, not write authority, not normalization, not merge, not promotion, not reviewed knowledge, not evidence support, not action basis, and not goal completion.",
            "",
        ]
    )
    return "\n".join(lines)


def build_html(report: dict) -> str:
    readiness = report["technical_readiness"]
    dependency = report["approval_dependency"]
    safe = "".join(f"<li>{html.escape(item)}</li>" for item in report["operator_summary"]["safe_next_actions"])
    unsafe = "".join(f"<li>{html.escape(item)}</li>" for item in report["operator_summary"]["unsafe_actions"])
    phrase = html.escape(dependency["exact_approval_phrase"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>p2-89 Approval Dependency Closeout</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fa; color: #202832; }}
    main {{ max-width: 1040px; margin: 0 auto; padding: 32px 20px; }}
    h1 {{ font-size: 28px; margin: 0 0 12px; letter-spacing: 0; }}
    .verdict {{ background: #fff; border-left: 4px solid #a63d40; padding: 14px; margin: 18px 0; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(170px, 1fr)); gap: 12px; }}
    .metric {{ background: #fff; border: 1px solid #d9e0e8; border-radius: 8px; padding: 14px; }}
    .metric span {{ display: block; color: #596575; font-size: 13px; }}
    .metric strong {{ display: block; margin-top: 6px; font-size: 24px; }}
    pre {{ white-space: pre-wrap; background: #1f2933; color: #f4f7fb; border-radius: 8px; padding: 14px; }}
    section {{ margin-top: 22px; }}
  </style>
</head>
<body>
  <main>
    <h1>p2-89 Approval Dependency Closeout</h1>
    <div class="verdict">{html.escape(report['operator_summary']['plain_verdict'])}</div>
    <section class="metrics">
      <div class="metric"><span>Preview operations</span><strong>{readiness['preview_operation_count']}</strong></div>
      <div class="metric"><span>Hash matches</span><strong>{readiness['prewrite_hash_match_count']}/75</strong></div>
      <div class="metric"><span>Old writes</span><strong>{readiness['old_slice_writes_applied']}</strong></div>
      <div class="metric"><span>Approval collected</span><strong>{str(dependency['exact_approval_collected']).lower()}</strong></div>
    </section>
    <section>
      <h2>Exact Approval Phrase</h2>
      <pre>{phrase}</pre>
    </section>
    <section>
      <h2>Safe Next Actions</h2>
      <ul>{safe}</ul>
    </section>
    <section>
      <h2>Unsafe Actions</h2>
      <ul>{unsafe}</ul>
    </section>
  </main>
</body>
</html>
"""


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    write_json(ARTIFACT_DIR / "approval_dependency_closeout_packet.json", report)
    (ARTIFACT_DIR / "approval_dependency_closeout_packet.md").write_text(build_markdown(report), encoding="utf-8")
    (ARTIFACT_DIR / "approval_dependency_closeout_packet.html").write_text(build_html(report), encoding="utf-8")
    build_failure_cases()

    fixtures = {
        "technical-readiness-clean.json": {
            "case_id": "technical-readiness-clean",
            "preview_operation_count": report["technical_readiness"]["preview_operation_count"],
            "prewrite_hash_match_count": report["technical_readiness"]["prewrite_hash_match_count"],
            "body_unchanged_count": report["technical_readiness"]["body_unchanged_count"],
            "non_status_frontmatter_unchanged_count": report["technical_readiness"]["non_status_frontmatter_unchanged_count"],
            "old_slice_writes_applied": report["technical_readiness"]["old_slice_writes_applied"],
        },
        "approval-gap-open.json": {
            "case_id": "approval-gap-open",
            "blocking_condition": report["approval_dependency"]["blocking_condition"],
            "exact_approval_collected": report["approval_dependency"]["exact_approval_collected"],
        },
        "executor-not-authorized.json": {
            "case_id": "executor-not-authorized",
            "executor_write_allowed_now": report["executor_status"]["executor_write_allowed_now"],
            "old_slice_write_allowed": report["executor_status"]["old_slice_write_allowed"],
        },
        "goal-not-complete.json": {
            "case_id": "goal-not-complete",
            "goal_complete_now": report["authority_flags"]["goal_complete_now"],
            "normalization_applied": report["authority_flags"]["normalization_applied"],
        },
        "decision-packet-linked.json": {
            "case_id": "decision-packet-linked",
            "decision_packet": report["approval_dependency"]["decision_packet"],
            "decision_option_count": report["technical_readiness"]["decision_option_count"],
        },
    }
    for name, fixture in fixtures.items():
        write_json(FIXTURES_DIR / name, fixture)
    print(json.dumps({"built": True, "slice_id": SLICE_ID}, indent=2))


if __name__ == "__main__":
    main()
