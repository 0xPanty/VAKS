from __future__ import annotations

import hashlib
import html
import json
from collections import Counter
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-90-post-approval-executor-handoff-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT_DIR = SLICE_ROOT / "artifact"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURE_DIR = SLICE_ROOT / "failure-cases"

P2_80 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/artifact/old_file_status_normalization_transaction_package.json"
P2_89 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-89-approval-dependency-closeout-packet-sandbox/artifact/approval_dependency_closeout_packet.json"


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
        "record_kind": "post_approval_executor_handoff_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {
                "case_id": "P2-90-FAIL-01-claims-current-write-authority",
                "must_fail_when": "The handoff says old-file writes are allowed now.",
            },
            {
                "case_id": "P2-90-FAIL-02-skips-fresh-prewrite-gate",
                "must_fail_when": "The handoff allows immediate writing after approval without fresh prewrite checks.",
            },
            {
                "case_id": "P2-90-FAIL-03-missing-exact-approval-prerequisite",
                "must_fail_when": "The handoff omits the exact p2-75 approval prerequisite.",
            },
            {
                "case_id": "P2-90-FAIL-04-target-count-drift",
                "must_fail_when": "The operation count is not 75.",
            },
            {
                "case_id": "P2-90-FAIL-05-allows-body-or-artifact-edits",
                "must_fail_when": "The handoff allows body content, artifact, tools, templates, wiki truth layer, or mainline edits.",
            },
            {
                "case_id": "P2-90-FAIL-06-missing-rollback-or-audit",
                "must_fail_when": "The handoff omits rollback, path audit, or final gate requirements.",
            },
            {
                "case_id": "P2-90-FAIL-07-mainline-or-truth-authority",
                "must_fail_when": "The handoff implies merge, promotion, reviewed knowledge, evidence support, or action basis.",
            },
            {
                "case_id": "P2-90-FAIL-08-goal-complete",
                "must_fail_when": "The handoff claims the full goal is complete before old-file normalization is actually executed and verified.",
            },
        ],
    }
    write_json(FAILURE_DIR / "post-approval-executor-handoff-failures.json", payload)


def build_report() -> dict:
    p80 = read_json(P2_80)
    p89 = read_json(P2_89)
    operations = p80["transaction_operations"]
    file_counts = Counter(Path(op["target_path"]).name for op in operations)
    exact_phrase = p89["approval_dependency"]["exact_approval_phrase"]

    return {
        "record_kind": "sandbox_post_approval_executor_handoff",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_80_transaction_package": P2_80,
            "p2_89_approval_dependency_closeout": P2_89,
        },
        "source_digest": {
            "p2_80_transaction_package": sha256_file(P2_80),
            "p2_89_approval_dependency_closeout": sha256_file(P2_89),
        },
        "current_status": {
            "exact_approval_collected_now": False,
            "executor_write_allowed_now": False,
            "old_slice_writes_applied": 0,
            "goal_complete_now": False,
            "blocking_condition": p89["approval_dependency"]["blocking_condition"],
        },
        "future_prerequisites": {
            "exact_approval_phrase": exact_phrase,
            "exact_approval_required": True,
            "fresh_prewrite_gate_required_after_approval": True,
            "fresh_boundary_audit_required_after_approval": True,
            "stop_before_any_write_required": True,
        },
        "executor_scope_if_future_gate_passes": {
            "allowed_edit_kind": "status_only_frontmatter_normalization",
            "allowed_field": "frontmatter.status",
            "operation_count": len(operations),
            "unique_target_file_count": len({op["target_path"] for op in operations}),
            "target_file_counts": dict(sorted(file_counts.items())),
            "allowed_target_family": "outputs/review/vaks-implementation-sandbox/2026-06-15-p*-*/{verification.md,reviewer-report.md,boundary-audit.md,product-acceptance-report.md,next-step.md}",
            "body_content_edits_allowed": False,
            "artifact_edits_allowed": False,
            "tools_templates_edits_allowed": False,
            "wiki_truth_layer_edits_allowed": False,
            "mainline_edits_allowed": False,
            "obsidian_sync_allowed": False,
            "commit_push_allowed": False,
        },
        "future_executor_stages": [
            {
                "stage_id": "stage_1_exact_approval_intake",
                "required_result": "exact phrase matched",
                "write_allowed": False,
            },
            {
                "stage_id": "stage_2_fresh_prewrite_recheck",
                "required_result": "75 targets exist and match required hashes at execution time",
                "write_allowed": False,
            },
            {
                "stage_id": "stage_3_boundary_reconfirmation",
                "required_result": "only old report frontmatter.status writes are in scope",
                "write_allowed": False,
            },
            {
                "stage_id": "stage_4_explicit_stop_before_write",
                "required_result": "executor reports the exact target set and waits for final command if policy still requires it",
                "write_allowed": False,
            },
            {
                "stage_id": "stage_5_status_only_apply_if_authorized",
                "required_result": "apply only status lines, then verify body/non-status frontmatter unchanged",
                "write_allowed": "future_only_after_all_prior_gates",
            },
        ],
        "future_verification_requirements": [
            "75 target files changed only in frontmatter.status.",
            "0 body-content changes.",
            "0 non-status-frontmatter changes.",
            "No artifact, tools, templates, wiki truth layer, mainline, README, or Obsidian writes.",
            "Rollback material preserved.",
            "Reviewer, Boundary Auditor, GPT-5.5 Product Acceptance, and final gate complete for the executor slice.",
        ],
        "authority_flags": {
            "handoff_only": True,
            "user_approval_collected": False,
            "handoff_authorizes_write": False,
            "executor_write_allowed_now": False,
            "old_slice_write_allowed_now": False,
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
    current = report["current_status"]
    prereq = report["future_prerequisites"]
    scope = report["executor_scope_if_future_gate_passes"]
    lines = [
        "---",
        f"slice_id: {SLICE_ID}",
        "status: generated",
        "---",
        "",
        "# Post-Approval Executor Handoff",
        "",
        "## Current Status",
        "",
        f"- exact_approval_collected_now: `{str(current['exact_approval_collected_now']).lower()}`",
        f"- executor_write_allowed_now: `{str(current['executor_write_allowed_now']).lower()}`",
        f"- old_slice_writes_applied: {current['old_slice_writes_applied']}",
        f"- goal_complete_now: `{str(current['goal_complete_now']).lower()}`",
        f"- blocking_condition: `{current['blocking_condition']}`",
        "",
        "## Exact Approval Phrase Required",
        "",
        "```text",
        prereq["exact_approval_phrase"],
        "```",
        "",
        "## Future Prerequisites",
        "",
    ]
    for key, value in prereq.items():
        if key != "exact_approval_phrase":
            lines.append(f"- {key}: `{str(value).lower()}`")
    lines.extend(
        [
            "",
            "## Future Executor Scope",
            "",
            f"- operation_count: {scope['operation_count']}",
            f"- unique_target_file_count: {scope['unique_target_file_count']}",
            f"- allowed_edit_kind: `{scope['allowed_edit_kind']}`",
            f"- allowed_field: `{scope['allowed_field']}`",
            f"- allowed_target_family: `{scope['allowed_target_family']}`",
            f"- body_content_edits_allowed: `{str(scope['body_content_edits_allowed']).lower()}`",
            f"- artifact_edits_allowed: `{str(scope['artifact_edits_allowed']).lower()}`",
            f"- tools_templates_edits_allowed: `{str(scope['tools_templates_edits_allowed']).lower()}`",
            f"- wiki_truth_layer_edits_allowed: `{str(scope['wiki_truth_layer_edits_allowed']).lower()}`",
            f"- mainline_edits_allowed: `{str(scope['mainline_edits_allowed']).lower()}`",
            "",
            "## Future Executor Stages",
            "",
        ]
    )
    for stage in report["future_executor_stages"]:
        lines.append(
            f"- `{stage['stage_id']}`: {stage['required_result']} (write_allowed: `{stage['write_allowed']}`)"
        )
    lines.extend(["", "## Verification Requirements", ""])
    for item in report["future_verification_requirements"]:
        lines.append(f"- {item}")
    lines.extend(
        [
            "",
            "## Boundary",
            "",
            "This handoff is not approval, not write authority, not normalization, not merge, not promotion, not reviewed knowledge, not evidence support, not action basis, and not goal completion.",
            "",
        ]
    )
    return "\n".join(lines)


def build_html(report: dict) -> str:
    current = report["current_status"]
    scope = report["executor_scope_if_future_gate_passes"]
    stages = "".join(
        f"<tr><td>{html.escape(stage['stage_id'])}</td><td>{html.escape(stage['required_result'])}</td><td>{html.escape(str(stage['write_allowed']))}</td></tr>"
        for stage in report["future_executor_stages"]
    )
    phrase = html.escape(report["future_prerequisites"]["exact_approval_phrase"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>p2-90 Post-Approval Executor Handoff</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fa; color: #202832; }}
    main {{ max-width: 1080px; margin: 0 auto; padding: 32px 20px; }}
    h1 {{ font-size: 28px; margin: 0 0 16px; letter-spacing: 0; }}
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
    <h1>p2-90 Post-Approval Executor Handoff</h1>
    <section class="metrics">
      <div class="metric"><span>Approval collected now</span><strong>{str(current['exact_approval_collected_now']).lower()}</strong></div>
      <div class="metric"><span>Write allowed now</span><strong>{str(current['executor_write_allowed_now']).lower()}</strong></div>
      <div class="metric"><span>Operations</span><strong>{scope['operation_count']}</strong></div>
      <div class="metric"><span>Old writes</span><strong>{current['old_slice_writes_applied']}</strong></div>
    </section>
    <h2>Exact Approval Phrase Required</h2>
    <pre>{phrase}</pre>
    <h2>Future Executor Stages</h2>
    <table><thead><tr><th>Stage</th><th>Required Result</th><th>Write Allowed</th></tr></thead><tbody>{stages}</tbody></table>
    <section class="boundary">Handoff only. No current approval, write authority, normalization, merge, promotion, reviewed knowledge, evidence support, action basis, or goal completion.</section>
  </main>
</body>
</html>
"""


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)
    report = build_report()
    write_json(ARTIFACT_DIR / "post_approval_executor_handoff.json", report)
    (ARTIFACT_DIR / "post_approval_executor_handoff.md").write_text(build_markdown(report), encoding="utf-8")
    (ARTIFACT_DIR / "post_approval_executor_handoff.html").write_text(build_html(report), encoding="utf-8")
    build_failure_cases()
    fixtures = {
        "current-execution-blocked.json": {
            "case_id": "current-execution-blocked",
            "exact_approval_collected_now": report["current_status"]["exact_approval_collected_now"],
            "executor_write_allowed_now": report["current_status"]["executor_write_allowed_now"],
        },
        "future-prewrite-required.json": {
            "case_id": "future-prewrite-required",
            "fresh_prewrite_gate_required_after_approval": report["future_prerequisites"]["fresh_prewrite_gate_required_after_approval"],
            "stop_before_any_write_required": report["future_prerequisites"]["stop_before_any_write_required"],
        },
        "status-only-scope.json": {
            "case_id": "status-only-scope",
            "operation_count": report["executor_scope_if_future_gate_passes"]["operation_count"],
            "allowed_field": report["executor_scope_if_future_gate_passes"]["allowed_field"],
            "body_content_edits_allowed": report["executor_scope_if_future_gate_passes"]["body_content_edits_allowed"],
        },
        "protected-paths-excluded.json": {
            "case_id": "protected-paths-excluded",
            "tools_templates_edits_allowed": report["executor_scope_if_future_gate_passes"]["tools_templates_edits_allowed"],
            "wiki_truth_layer_edits_allowed": report["executor_scope_if_future_gate_passes"]["wiki_truth_layer_edits_allowed"],
            "mainline_edits_allowed": report["executor_scope_if_future_gate_passes"]["mainline_edits_allowed"],
        },
        "handoff-not-goal-complete.json": {
            "case_id": "handoff-not-goal-complete",
            "goal_complete_now": report["authority_flags"]["goal_complete_now"],
            "normalization_applied": report["authority_flags"]["normalization_applied"],
        },
    }
    for name, fixture in fixtures.items():
        write_json(FIXTURES_DIR / name, fixture)
    print(json.dumps({"built": True, "slice_id": SLICE_ID}, indent=2))


if __name__ == "__main__":
    main()
