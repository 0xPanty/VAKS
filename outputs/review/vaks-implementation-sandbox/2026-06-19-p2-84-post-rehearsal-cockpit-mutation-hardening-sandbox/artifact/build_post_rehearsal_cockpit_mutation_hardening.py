from __future__ import annotations

import copy
import hashlib
import html
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-84-post-rehearsal-cockpit-mutation-hardening-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT_DIR = SLICE_ROOT / "artifact"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
MUTANTS_DIR = FIXTURES_DIR / "mutants"
FAILURE_DIR = SLICE_ROOT / "failure-cases"

P2_83_COCKPIT = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox/artifact/post_rehearsal_goal_state_cockpit.json"
P2_83_FAILURES = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox/failure-cases/post-rehearsal-goal-state-cockpit-failures.json"
P2_83_PRODUCT = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox/product-acceptance-report.md"


MUTATION_SPECS = [
    {
        "case_id": "MUT-01-all-done-overclaim",
        "expected_failure_code": "all_done_overclaim",
        "source_failure_case": "P2-83-FAIL-01-all-done-overclaim",
        "description": "Claims all work is done while old-file strict completion remains 0.",
    },
    {
        "case_id": "MUT-02-generic-continuation-as-approval",
        "expected_failure_code": "generic_continuation_as_approval",
        "source_failure_case": "P2-83-FAIL-02-generic-continuation-as-approval",
        "description": "Treats generic continuation as old-file write approval.",
    },
    {
        "case_id": "MUT-03-rehearsal-as-write-authority",
        "expected_failure_code": "rehearsal_as_write_authority",
        "source_failure_case": "P2-83-FAIL-03-rehearsal-as-write-authority",
        "description": "Treats p2-82 sandbox rehearsal as current executor authority.",
    },
    {
        "case_id": "MUT-04-missing-byte-safety-rollup",
        "expected_failure_code": "missing_byte_safety_rollup",
        "source_failure_case": "P2-83-FAIL-04-missing-byte-safety-rollup",
        "description": "Drops p2-82 byte-level rollback evidence.",
    },
    {
        "case_id": "MUT-05-stale-pre-p2-82-status-surface",
        "expected_failure_code": "stale_pre_p2_82_status_surface",
        "source_failure_case": "P2-83-FAIL-05-stale-pre-p2-82-status-surface",
        "description": "Looks like a pre-p2-82 surface that omits p2-82 source evidence.",
    },
    {
        "case_id": "MUT-06-mainline-authority-confusion",
        "expected_failure_code": "mainline_authority_confusion",
        "source_failure_case": "P2-83-FAIL-06-mainline-authority-confusion",
        "description": "Creates merge/promotion/reviewed/action authority.",
    },
    {
        "case_id": "MUT-07-product-acceptance-as-user-approval",
        "expected_failure_code": "product_acceptance_as_user_approval",
        "source_failure_case": "P2-83-FAIL-07-product-acceptance-confusion",
        "description": "Treats Product Acceptance as user write approval.",
    },
    {
        "case_id": "MUT-08-path-boundary-violation",
        "expected_failure_code": "path_boundary_violation",
        "source_failure_case": "P2-83-FAIL-08-path-boundary-violation",
        "description": "Adds a planned write outside the p2-84 sandbox.",
    },
]


def repo_path(rel: str) -> Path:
    return REPO_ROOT / rel


def read_json(rel: str) -> dict:
    return json.loads(repo_path(rel).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def source_sha(rel: str) -> str:
    return hashlib.sha256(repo_path(rel).read_bytes()).hexdigest()


def planned_write_within_slice(path: str) -> bool:
    norm = path.replace("\\", "/")
    allowed = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"
    return norm.startswith(allowed)


def validate_cockpit(payload: dict) -> list[str]:
    failures: list[str] = []
    summary = payload.get("status_summary", {})
    plain = payload.get("plain_answer", {})
    decision = payload.get("decision_matrix", {})
    authority = payload.get("authority_flags", {})
    sources = payload.get("source_inputs", {})

    if summary.get("old_slice_current_strict_final_gate_count") != 0:
        failures.append("old_file_strict_count_changed")
    if summary.get("pending_status_change_count") != 75:
        failures.append("pending_status_change_count_changed")
    if summary.get("old_slice_writes_applied") != 0:
        failures.append("old_slice_write_applied")
    if summary.get("goal_complete_now") is not False or plain.get("all_done_product_grade") is not False or decision.get("can_claim_all_done") is not False:
        failures.append("all_done_overclaim")

    first_route = (payload.get("next_action_router") or [{}])[0]
    if first_route.get("old_file_write_allowed") is not False:
        failures.append("generic_continuation_as_approval")

    if decision.get("can_execute_old_file_normalization_now") is not False or authority.get("executor_write_allowed") is not False:
        failures.append("rehearsal_as_write_authority")

    if summary.get("p2_82_final_copy_byte_hash_restored_count") != 75:
        failures.append("missing_byte_safety_rollup")

    if "p2_82_copy_rehearsal" not in sources or summary.get("p2_82_fixture_copy_count") != 75:
        failures.append("stale_pre_p2_82_status_surface")

    if decision.get("can_merge_mainline_now") is not False or authority.get("mainline_ready") is not False or authority.get("promotion_ready") is not False or authority.get("reviewed_knowledge_ready") is not False or authority.get("action_basis_ready") is not False:
        failures.append("mainline_authority_confusion")

    if decision.get("can_treat_product_acceptance_as_user_write_approval") is not False or authority.get("approval_collected") is not False:
        failures.append("product_acceptance_as_user_approval")

    for path in payload.get("planned_write_paths", []):
        if not planned_write_within_slice(str(path)):
            failures.append("path_boundary_violation")
            break

    return sorted(set(failures))


def mutate(base: dict, case_id: str) -> dict:
    payload = copy.deepcopy(base)
    payload["mutation_case_id"] = case_id
    payload["mutation_note"] = "This is a negative fixture generated inside p2-84 only."
    if case_id == "MUT-01-all-done-overclaim":
        payload["plain_answer"]["all_done_product_grade"] = True
        payload["status_summary"]["goal_complete_now"] = True
        payload["decision_matrix"]["can_claim_all_done"] = True
    elif case_id == "MUT-02-generic-continuation-as-approval":
        payload["next_action_router"][0]["old_file_write_allowed"] = True
        payload["next_action_router"][0]["route"] = "execute old-file status normalization"
    elif case_id == "MUT-03-rehearsal-as-write-authority":
        payload["decision_matrix"]["can_execute_old_file_normalization_now"] = True
        payload["authority_flags"]["executor_write_allowed"] = True
    elif case_id == "MUT-04-missing-byte-safety-rollup":
        payload["status_summary"]["p2_82_final_copy_byte_hash_restored_count"] = 0
    elif case_id == "MUT-05-stale-pre-p2-82-status-surface":
        payload["source_inputs"].pop("p2_82_copy_rehearsal", None)
        payload["status_summary"]["p2_82_fixture_copy_count"] = 0
    elif case_id == "MUT-06-mainline-authority-confusion":
        payload["decision_matrix"]["can_merge_mainline_now"] = True
        payload["authority_flags"]["mainline_ready"] = True
        payload["authority_flags"]["promotion_ready"] = True
        payload["authority_flags"]["reviewed_knowledge_ready"] = True
        payload["authority_flags"]["action_basis_ready"] = True
    elif case_id == "MUT-07-product-acceptance-as-user-approval":
        payload["decision_matrix"]["can_treat_product_acceptance_as_user_write_approval"] = True
        payload["authority_flags"]["approval_collected"] = True
    elif case_id == "MUT-08-path-boundary-violation":
        payload["planned_write_paths"] = ["outputs/review/vaks-implementation-sandbox/2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox/product-acceptance-report.md"]
    else:
        raise ValueError(f"Unknown mutation case: {case_id}")
    return payload


def build_markdown(report: dict) -> str:
    lines = [
        "---",
        f"slice_id: {SLICE_ID}",
        "status: generated",
        "---",
        "",
        "# Post-Rehearsal Cockpit Mutation Hardening",
        "",
        "## Summary",
        "",
        f"- baseline_passed: {str(report['summary']['baseline_passed']).lower()}",
        f"- mutation_count: {report['summary']['mutation_count']}",
        f"- expected_mutation_fail_count: {report['summary']['expected_mutation_fail_count']}",
        f"- unexpected_pass_count: {report['summary']['unexpected_pass_count']}",
        f"- unexpected_failure_count: {report['summary']['unexpected_failure_count']}",
        "",
        "## Mutations",
        "",
    ]
    for result in report["mutation_results"]:
        lines.extend(
            [
                f"### {result['case_id']}",
                "",
                f"- expected_failure_code: {result['expected_failure_code']}",
                f"- failed_as_expected: {str(result['failed_as_expected']).lower()}",
                f"- observed_failures: {', '.join(result['observed_failures'])}",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            "All mutations are fixture copies inside this slice. p2-84 does not edit p2-83, old slices, mainline docs, wiki truth layers, templates, tools, or Obsidian.",
            "",
        ]
    )
    return "\n".join(lines)


def build_html(report: dict) -> str:
    rows = "\n".join(
        f"<tr><td>{html.escape(item['case_id'])}</td><td>{html.escape(item['expected_failure_code'])}</td><td>{str(item['failed_as_expected']).lower()}</td></tr>"
        for item in report["mutation_results"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>p2-84 Mutation Hardening</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fa; color: #1b222c; }}
    main {{ max-width: 1040px; margin: 0 auto; padding: 32px 20px; }}
    h1 {{ font-size: 28px; margin: 0 0 16px; letter-spacing: 0; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 22px; }}
    .metric {{ background: white; border: 1px solid #d9e0e8; border-radius: 8px; padding: 14px; }}
    .metric span {{ display: block; color: #596575; font-size: 13px; }}
    .metric strong {{ display: block; font-size: 24px; margin-top: 6px; }}
    table {{ width: 100%; border-collapse: collapse; background: white; border: 1px solid #d9e0e8; }}
    th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid #e5e9ef; }}
    th {{ color: #526070; font-size: 13px; }}
    .boundary {{ margin-top: 20px; background: #fff4f2; border-left: 4px solid #a63d40; padding: 14px; }}
  </style>
</head>
<body>
  <main>
    <h1>p2-84 Mutation Hardening</h1>
    <section class="metrics">
      <div class="metric"><span>Baseline passed</span><strong>{str(report['summary']['baseline_passed']).lower()}</strong></div>
      <div class="metric"><span>Mutations</span><strong>{report['summary']['mutation_count']}</strong></div>
      <div class="metric"><span>Failed as expected</span><strong>{report['summary']['expected_mutation_fail_count']}/8</strong></div>
      <div class="metric"><span>Unexpected pass</span><strong>{report['summary']['unexpected_pass_count']}</strong></div>
    </section>
    <table>
      <thead><tr><th>Case</th><th>Expected Failure</th><th>Failed As Expected</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <section class="boundary">Mutation fixtures are sandbox copies only. This artifact creates no old-file write authority.</section>
  </main>
</body>
</html>
"""


def build_failure_cases() -> None:
    payload = {
        "record_kind": "post_rehearsal_cockpit_mutation_hardening_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {
                "case_id": spec["case_id"],
                "expected_failure_code": spec["expected_failure_code"],
                "source_failure_case": spec["source_failure_case"],
                "must_fail_when": spec["description"],
            }
            for spec in MUTATION_SPECS
        ],
    }
    write_json(FAILURE_DIR / "post-rehearsal-cockpit-mutation-hardening-failures.json", payload)


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    MUTANTS_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)

    baseline = read_json(P2_83_COCKPIT)
    write_json(FIXTURES_DIR / "baseline-p2-83-cockpit.json", baseline)

    mutation_results = []
    for spec in MUTATION_SPECS:
        mutant = mutate(baseline, spec["case_id"])
        mutant_path = MUTANTS_DIR / f"{spec['case_id']}.json"
        write_json(mutant_path, mutant)
        observed = validate_cockpit(mutant)
        mutation_results.append(
            {
                "case_id": spec["case_id"],
                "source_failure_case": spec["source_failure_case"],
                "expected_failure_code": spec["expected_failure_code"],
                "observed_failures": observed,
                "failed_as_expected": spec["expected_failure_code"] in observed,
                "fixture_path": str(mutant_path.relative_to(SLICE_ROOT)).replace("\\", "/"),
            }
        )

    baseline_failures = validate_cockpit(baseline)
    report = {
        "record_kind": "sandbox_post_rehearsal_cockpit_mutation_hardening",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_83_cockpit": P2_83_COCKPIT,
            "p2_83_failure_cases": P2_83_FAILURES,
            "p2_83_product_acceptance_report": P2_83_PRODUCT,
        },
        "source_digest": {
            "p2_83_cockpit": source_sha(P2_83_COCKPIT),
            "p2_83_failure_cases": source_sha(P2_83_FAILURES),
            "p2_83_product_acceptance_report": source_sha(P2_83_PRODUCT),
        },
        "summary": {
            "baseline_passed": not baseline_failures,
            "baseline_failure_count": len(baseline_failures),
            "mutation_count": len(MUTATION_SPECS),
            "expected_mutation_fail_count": sum(1 for item in mutation_results if item["failed_as_expected"]),
            "unexpected_pass_count": sum(1 for item in mutation_results if not item["observed_failures"]),
            "unexpected_failure_count": sum(1 for item in mutation_results if item["observed_failures"] and not item["failed_as_expected"]),
            "old_slice_writes_applied": 0,
            "p2_83_files_modified": 0,
        },
        "baseline_validation_failures": baseline_failures,
        "mutation_results": mutation_results,
        "authority_flags": {
            "mutation_hardening_only": True,
            "p2_83_write_allowed": False,
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
    write_json(ARTIFACT_DIR / "post_rehearsal_cockpit_mutation_hardening.json", report)
    (ARTIFACT_DIR / "post_rehearsal_cockpit_mutation_hardening.md").write_text(build_markdown(report), encoding="utf-8")
    (ARTIFACT_DIR / "post_rehearsal_cockpit_mutation_hardening.html").write_text(build_html(report), encoding="utf-8")
    build_failure_cases()
    print(json.dumps({"built": True, "slice_id": SLICE_ID}, indent=2))


if __name__ == "__main__":
    main()
