from __future__ import annotations

import copy
import hashlib
import html
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-86-approval-to-prewrite-gate-chain-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT_DIR = SLICE_ROOT / "artifact"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURE_DIR = SLICE_ROOT / "failure-cases"

P2_85 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-85-exact-approval-classifier-hardening-sandbox/artifact/exact_approval_classifier_hardening.json"
P2_80 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-80-old-file-status-normalization-transaction-package-sandbox/artifact/old_file_status_normalization_transaction_package.json"
P2_82 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-82-old-file-status-normalization-sandbox-copy-executor-rehearsal-sandbox/artifact/sandbox_copy_executor_rehearsal.json"
P2_83 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox/artifact/post_rehearsal_goal_state_cockpit.json"


def repo_path(rel: str) -> Path:
    return REPO_ROOT / rel


def read_json(rel: str) -> dict:
    return json.loads(repo_path(rel).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def file_sha(rel: str) -> str:
    return sha256_bytes(repo_path(rel).read_bytes())


def classify(text: str, exact_phrase: str) -> dict:
    matched = text == exact_phrase
    return {
        "matched_exact_phrase": matched,
        "approval_class": "exact_p2_75_approval" if matched else "not_approval",
        "fixture_match_is_user_approval": False,
    }


def current_preflight(ops: list[dict]) -> dict:
    results = []
    for op in ops:
        path = repo_path(op["target_path"])
        exists = path.exists()
        current_hash = sha256_bytes(path.read_bytes()) if exists else None
        required_hash = op["prewrite_required_hash"]
        results.append(
            {
                "operation_index": op["operation_index"],
                "target_path": op["target_path"],
                "target_exists": exists,
                "current_sha256": current_hash,
                "required_sha256": required_hash,
                "hash_matches_required": exists and current_hash == required_hash,
            }
        )
    return {
        "target_count": len(results),
        "exists_count": sum(1 for item in results if item["target_exists"]),
        "hash_match_count": sum(1 for item in results if item["hash_matches_required"]),
        "hash_mismatch_count": sum(1 for item in results if item["target_exists"] and not item["hash_matches_required"]),
        "missing_count": sum(1 for item in results if not item["target_exists"]),
        "results": results,
    }


def evaluate_gate(scenario: dict, exact_phrase: str, preflight: dict, rehearsal: dict) -> dict:
    approval = classify(scenario["user_text"], exact_phrase)
    hash_match_count = preflight["hash_match_count"] - scenario.get("forced_hash_mismatch_count", 0)
    hash_clean = hash_match_count == preflight["target_count"] and preflight["missing_count"] == 0
    rehearsal_ok = rehearsal["summary"]["final_copy_byte_sha_match_count"] == 75 and scenario.get("rehearsal_evidence_present", True)
    boundary_ok = scenario.get("boundary_passed", True)
    mainline_requested = scenario.get("mainline_requested", False)
    immediate_write_requested = scenario.get("immediate_write_requested", False)
    product_acceptance_as_approval = scenario.get("product_acceptance_as_approval", False)

    blockers = []
    if not approval["matched_exact_phrase"]:
        blockers.append("blocked_no_exact_approval")
    if product_acceptance_as_approval:
        blockers.append("blocked_product_acceptance_is_not_user_approval")
    if not hash_clean:
        blockers.append("blocked_prewrite_hash_or_missing_target")
    if not rehearsal_ok:
        blockers.append("blocked_missing_byte_safe_rehearsal")
    if not boundary_ok:
        blockers.append("blocked_boundary_not_passed")
    if mainline_requested:
        blockers.append("blocked_mainline_authority_request")
    if immediate_write_requested:
        blockers.append("blocked_immediate_write_request")

    if blockers:
        gate_state = blockers[0]
    else:
        gate_state = "ready_for_prewrite_confirmation"

    return {
        "scenario_id": scenario["scenario_id"],
        "description": scenario["description"],
        "approval": approval,
        "hash_match_count": hash_match_count,
        "hash_target_count": preflight["target_count"],
        "hash_clean": hash_clean,
        "rehearsal_ok": rehearsal_ok,
        "boundary_ok": boundary_ok,
        "blockers": blockers,
        "gate_state": gate_state,
        "ready_for_prewrite_confirmation": gate_state == "ready_for_prewrite_confirmation",
        "executor_write_allowed_now": False,
        "old_slice_writes_applied": 0,
        "requires_stop_before_write": True,
        "fixture_match_is_user_approval": False,
    }


def build_scenarios(exact_phrase: str) -> list[dict]:
    return [
        {
            "scenario_id": "POS-01-exact-clean-prewrite-ready",
            "description": "Exact approval fixture, clean hash preflight, rehearsal present, boundary passed.",
            "user_text": exact_phrase,
            "expected_gate_state": "ready_for_prewrite_confirmation",
        },
        {
            "scenario_id": "NEG-01-generic-continuation",
            "description": "Generic continuation is not approval.",
            "user_text": "继续，全部落地",
            "expected_gate_state": "blocked_no_exact_approval",
        },
        {
            "scenario_id": "NEG-02-product-acceptance-as-approval",
            "description": "Product Acceptance cannot substitute for user approval.",
            "user_text": "PASS_PRODUCT_GRADE",
            "product_acceptance_as_approval": True,
            "expected_gate_state": "blocked_no_exact_approval",
        },
        {
            "scenario_id": "NEG-03-hash-drift",
            "description": "Exact phrase cannot override fresh hash drift.",
            "user_text": exact_phrase,
            "forced_hash_mismatch_count": 1,
            "expected_gate_state": "blocked_prewrite_hash_or_missing_target",
        },
        {
            "scenario_id": "NEG-04-missing-rehearsal",
            "description": "Exact phrase cannot skip p2-82 byte-safe rehearsal evidence.",
            "user_text": exact_phrase,
            "rehearsal_evidence_present": False,
            "expected_gate_state": "blocked_missing_byte_safe_rehearsal",
        },
        {
            "scenario_id": "NEG-05-boundary-not-passed",
            "description": "Exact phrase cannot override failed boundary audit.",
            "user_text": exact_phrase,
            "boundary_passed": False,
            "expected_gate_state": "blocked_boundary_not_passed",
        },
        {
            "scenario_id": "NEG-06-mainline-request",
            "description": "Exact old-file normalization phrase does not grant mainline authority.",
            "user_text": exact_phrase,
            "mainline_requested": True,
            "expected_gate_state": "blocked_mainline_authority_request",
        },
        {
            "scenario_id": "NEG-07-immediate-write-request",
            "description": "Even a clean chain reaches prewrite confirmation, not immediate old-file write.",
            "user_text": exact_phrase,
            "immediate_write_requested": True,
            "expected_gate_state": "blocked_immediate_write_request",
        },
    ]


def build_failure_cases() -> None:
    cases = {
        "record_kind": "approval_to_prewrite_gate_chain_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {
                "case_id": "P2-86-FAIL-01-generic-approval",
                "must_fail_when": "Generic continuation reaches prewrite confirmation.",
            },
            {
                "case_id": "P2-86-FAIL-02-product-acceptance-approval",
                "must_fail_when": "Product Acceptance is treated as user approval.",
            },
            {
                "case_id": "P2-86-FAIL-03-hash-drift-override",
                "must_fail_when": "Exact phrase overrides fresh hash drift.",
            },
            {
                "case_id": "P2-86-FAIL-04-missing-rehearsal-override",
                "must_fail_when": "Exact phrase skips byte-safe rehearsal evidence.",
            },
            {
                "case_id": "P2-86-FAIL-05-boundary-override",
                "must_fail_when": "Exact phrase overrides failed boundary audit.",
            },
            {
                "case_id": "P2-86-FAIL-06-mainline-authority-confusion",
                "must_fail_when": "Old-file normalization approval grants mainline authority.",
            },
            {
                "case_id": "P2-86-FAIL-07-immediate-write-confusion",
                "must_fail_when": "Ready-for-prewrite is treated as immediate write authority.",
            },
            {
                "case_id": "P2-86-FAIL-08-fixture-approval-confusion",
                "must_fail_when": "Fixture exact phrase is treated as current user approval collected by this slice.",
            },
        ],
    }
    write_json(FAILURE_DIR / "approval-to-prewrite-gate-chain-failures.json", cases)


def build_markdown(report: dict) -> str:
    lines = [
        "---",
        f"slice_id: {SLICE_ID}",
        "status: generated",
        "---",
        "",
        "# Approval To Prewrite Gate Chain",
        "",
        "## Summary",
        "",
        f"- target_count: {report['summary']['target_count']}",
        f"- fresh_hash_match_count: {report['summary']['fresh_hash_match_count']}",
        f"- positive_ready_count: {report['summary']['positive_ready_count']}",
        f"- negative_blocked_count: {report['summary']['negative_blocked_count']}",
        f"- executor_write_allowed_now: {str(report['summary']['executor_write_allowed_now']).lower()}",
        f"- old_slice_writes_applied: {report['summary']['old_slice_writes_applied']}",
        "",
        "## Scenarios",
        "",
    ]
    for result in report["gate_results"]:
        lines.extend(
            [
                f"### {result['scenario_id']}",
                "",
                f"- gate_state: {result['gate_state']}",
                f"- ready_for_prewrite_confirmation: {str(result['ready_for_prewrite_confirmation']).lower()}",
                f"- executor_write_allowed_now: {str(result['executor_write_allowed_now']).lower()}",
                f"- blockers: {', '.join(result['blockers']) if result['blockers'] else 'none'}",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            "This slice is a no-write gate-chain integration artifact. It does not collect user approval and does not authorize old-file writes.",
            "",
        ]
    )
    return "\n".join(lines)


def build_html(report: dict) -> str:
    rows = "\n".join(
        f"<tr><td>{html.escape(item['scenario_id'])}</td><td>{html.escape(item['gate_state'])}</td><td>{str(item['ready_for_prewrite_confirmation']).lower()}</td><td>{str(item['executor_write_allowed_now']).lower()}</td></tr>"
        for item in report["gate_results"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>p2-86 Approval To Prewrite Gate</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fa; color: #1d2530; }}
    main {{ max-width: 1080px; margin: 0 auto; padding: 32px 20px; }}
    h1 {{ font-size: 28px; margin: 0 0 16px; letter-spacing: 0; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(190px, 1fr)); gap: 12px; margin-bottom: 22px; }}
    .metric {{ background: #fff; border: 1px solid #d9e0e8; border-radius: 8px; padding: 14px; }}
    .metric span {{ display: block; color: #596575; font-size: 13px; }}
    .metric strong {{ display: block; font-size: 24px; margin-top: 6px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; border: 1px solid #d9e0e8; }}
    th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid #e5e9ef; }}
    th {{ color: #526070; font-size: 13px; }}
    .boundary {{ margin-top: 20px; background: #fff4f2; border-left: 4px solid #a63d40; padding: 14px; }}
  </style>
</head>
<body>
  <main>
    <h1>p2-86 Approval To Prewrite Gate</h1>
    <section class="metrics">
      <div class="metric"><span>Fresh hash match</span><strong>{report['summary']['fresh_hash_match_count']}/{report['summary']['target_count']}</strong></div>
      <div class="metric"><span>Positive ready</span><strong>{report['summary']['positive_ready_count']}</strong></div>
      <div class="metric"><span>Negative blocked</span><strong>{report['summary']['negative_blocked_count']}</strong></div>
      <div class="metric"><span>Old writes</span><strong>{report['summary']['old_slice_writes_applied']}</strong></div>
    </section>
    <table>
      <thead><tr><th>Scenario</th><th>Gate State</th><th>Prewrite Ready</th><th>Write Allowed Now</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <section class="boundary">Ready-for-prewrite is not old-file write authority. This slice writes no old files.</section>
  </main>
</body>
</html>
"""


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)

    p2_85 = read_json(P2_85)
    p2_80 = read_json(P2_80)
    p2_82 = read_json(P2_82)
    p2_83 = read_json(P2_83)
    exact_phrase = p2_85["approval_contract"]["exact_phrase"]
    operations = p2_80["transaction_operations"]
    preflight = current_preflight(operations)
    scenarios = build_scenarios(exact_phrase)
    gate_results = [evaluate_gate(scenario, exact_phrase, preflight, p2_82) for scenario in scenarios]

    for scenario, result in zip(scenarios, gate_results):
        fixture = copy.deepcopy(scenario)
        fixture["result"] = result
        write_json(FIXTURES_DIR / f"{scenario['scenario_id']}.json", fixture)

    positive_ready = sum(1 for item in gate_results if item["scenario_id"].startswith("POS-") and item["ready_for_prewrite_confirmation"])
    negative_blocked = sum(1 for item in gate_results if item["scenario_id"].startswith("NEG-") and not item["ready_for_prewrite_confirmation"])
    report = {
        "record_kind": "sandbox_approval_to_prewrite_gate_chain",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_85_classifier": P2_85,
            "p2_80_transaction_package": P2_80,
            "p2_82_copy_rehearsal": P2_82,
            "p2_83_cockpit": P2_83,
        },
        "source_digest": {
            "p2_85_classifier": file_sha(P2_85),
            "p2_80_transaction_package": file_sha(P2_80),
            "p2_82_copy_rehearsal": file_sha(P2_82),
            "p2_83_cockpit": file_sha(P2_83),
        },
        "summary": {
            "target_count": preflight["target_count"],
            "fresh_hash_match_count": preflight["hash_match_count"],
            "fresh_hash_mismatch_count": preflight["hash_mismatch_count"],
            "fresh_missing_count": preflight["missing_count"],
            "p2_82_final_copy_byte_hash_restored_count": p2_82["summary"]["final_copy_byte_sha_match_count"],
            "p2_83_goal_complete_now": p2_83["status_summary"]["goal_complete_now"],
            "scenario_count": len(gate_results),
            "positive_ready_count": positive_ready,
            "negative_blocked_count": negative_blocked,
            "executor_write_allowed_now": False,
            "old_slice_writes_applied": 0,
            "user_approval_collected_by_this_slice": False,
        },
        "preflight_summary": {
            key: preflight[key]
            for key in ["target_count", "exists_count", "hash_match_count", "hash_mismatch_count", "missing_count"]
        },
        "gate_results": gate_results,
        "authority_flags": {
            "gate_chain_only": True,
            "fixture_exact_phrase_is_user_approval": False,
            "approval_collected": False,
            "ready_for_prewrite_is_write_authority": False,
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
    write_json(ARTIFACT_DIR / "approval_to_prewrite_gate_chain.json", report)
    (ARTIFACT_DIR / "approval_to_prewrite_gate_chain.md").write_text(build_markdown(report), encoding="utf-8")
    (ARTIFACT_DIR / "approval_to_prewrite_gate_chain.html").write_text(build_html(report), encoding="utf-8")
    build_failure_cases()
    print(json.dumps({"built": True, "slice_id": SLICE_ID}, indent=2))


if __name__ == "__main__":
    main()
