from __future__ import annotations

import hashlib
import html
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-85-exact-approval-classifier-hardening-sandbox"
THIS_FILE = Path(__file__).resolve()
SLICE_ROOT = THIS_FILE.parents[1]
REPO_ROOT = THIS_FILE.parents[5]
ARTIFACT_DIR = SLICE_ROOT / "artifact"
FIXTURES_DIR = SLICE_ROOT / "fixtures"
FAILURE_DIR = SLICE_ROOT / "failure-cases"

P2_75 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-75-old-file-status-normalization-approval-request-sandbox/artifact/old_file_status_normalization_approval_request.json"
P2_77 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-77-old-file-status-normalization-executor-readiness-gate-sandbox/artifact/old_file_status_normalization_executor_readiness_gate.json"
P2_83 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-83-post-rehearsal-goal-state-cockpit-sandbox/artifact/post_rehearsal_goal_state_cockpit.json"
P2_84 = "outputs/review/vaks-implementation-sandbox/2026-06-19-p2-84-post-rehearsal-cockpit-mutation-hardening-sandbox/artifact/post_rehearsal_cockpit_mutation_hardening.json"


def repo_path(rel: str) -> Path:
    return REPO_ROOT / rel


def read_json(rel: str) -> dict:
    return json.loads(repo_path(rel).read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(rel: str) -> str:
    return hashlib.sha256(repo_path(rel).read_bytes()).hexdigest()


def classify(text: str, exact_phrase: str) -> dict:
    matched = text == exact_phrase
    return {
        "input_sha256": sha256_text(text),
        "matched_exact_phrase": matched,
        "approval_class": "exact_p2_75_approval" if matched else "not_approval",
        "old_file_write_allowed_by_this_slice": False,
        "requires_future_executor_slice": matched,
        "reason": "exact byte-for-byte phrase match" if matched else "not an exact p2-75 approval phrase",
    }


def build_cases(exact_phrase: str) -> list[dict]:
    return [
        {
            "case_id": "POS-01-exact-phrase",
            "kind": "positive",
            "input_text": exact_phrase,
            "expected_match": True,
            "expected_class": "exact_p2_75_approval",
        },
        {
            "case_id": "NEG-01-chinese-generic-continue",
            "kind": "negative",
            "input_text": "继续，全部落地",
            "expected_match": False,
            "expected_class": "not_approval",
        },
        {
            "case_id": "NEG-02-english-generic-go-ahead",
            "kind": "negative",
            "input_text": "go ahead and make it product grade",
            "expected_match": False,
            "expected_class": "not_approval",
        },
        {
            "case_id": "NEG-03-paraphrase",
            "kind": "negative",
            "input_text": "I approve the old-file status normalization for the 20 sandbox slices. Do not change anything else.",
            "expected_match": False,
            "expected_class": "not_approval",
        },
        {
            "case_id": "NEG-04-partial-phrase",
            "kind": "negative",
            "input_text": exact_phrase.split(" Do not edit body content", 1)[0] + ".",
            "expected_match": False,
            "expected_class": "not_approval",
        },
        {
            "case_id": "NEG-05-wrong-count",
            "kind": "negative",
            "input_text": exact_phrase.replace("75 dry-run", "74 dry-run"),
            "expected_match": False,
            "expected_class": "not_approval",
        },
        {
            "case_id": "NEG-06-missing-prohibitions",
            "kind": "negative",
            "input_text": exact_phrase.replace(", commit, push, or sync.", "."),
            "expected_match": False,
            "expected_class": "not_approval",
        },
        {
            "case_id": "NEG-07-extra-authority",
            "kind": "negative",
            "input_text": exact_phrase + " Also merge mainline if tests pass.",
            "expected_match": False,
            "expected_class": "not_approval",
        },
        {
            "case_id": "NEG-08-whitespace-variation",
            "kind": "negative",
            "input_text": " " + exact_phrase + " ",
            "expected_match": False,
            "expected_class": "not_approval",
        },
        {
            "case_id": "NEG-09-case-variation",
            "kind": "negative",
            "input_text": exact_phrase.replace("I explicitly approve", "i explicitly approve", 1),
            "expected_match": False,
            "expected_class": "not_approval",
        },
    ]


def build_failure_cases() -> None:
    payload = {
        "record_kind": "exact_approval_classifier_failure_cases",
        "slice_id": SLICE_ID,
        "failure_cases": [
            {
                "case_id": "P2-85-FAIL-01-generic-chinese-approval-confusion",
                "must_fail_when": "Chinese generic continuation is classified as approval.",
            },
            {
                "case_id": "P2-85-FAIL-02-generic-english-approval-confusion",
                "must_fail_when": "English generic go-ahead language is classified as approval.",
            },
            {
                "case_id": "P2-85-FAIL-03-paraphrase-approval-confusion",
                "must_fail_when": "A paraphrase is classified as exact approval.",
            },
            {
                "case_id": "P2-85-FAIL-04-partial-phrase-approval-confusion",
                "must_fail_when": "A partial phrase is classified as exact approval.",
            },
            {
                "case_id": "P2-85-FAIL-05-wrong-count-approval-confusion",
                "must_fail_when": "A phrase with a wrong status-change count is classified as approval.",
            },
            {
                "case_id": "P2-85-FAIL-06-missing-prohibitions-approval-confusion",
                "must_fail_when": "A phrase missing commit/push/sync prohibitions is classified as approval.",
            },
            {
                "case_id": "P2-85-FAIL-07-extra-authority-approval-confusion",
                "must_fail_when": "A phrase adding merge/mainline authority is classified as approval.",
            },
            {
                "case_id": "P2-85-FAIL-08-whitespace-or-case-normalization-confusion",
                "must_fail_when": "Whitespace or case normalization changes are ignored and classified as approval.",
            },
            {
                "case_id": "P2-85-FAIL-09-classifier-pass-as-user-approval",
                "must_fail_when": "This slice treats a fixture pass as user approval collected now.",
            },
        ],
    }
    write_json(FAILURE_DIR / "exact-approval-classifier-failures.json", payload)


def build_markdown(report: dict) -> str:
    lines = [
        "---",
        f"slice_id: {SLICE_ID}",
        "status: generated",
        "---",
        "",
        "# Exact Approval Classifier Hardening",
        "",
        "## Summary",
        "",
        f"- exact_phrase_sha256: {report['approval_contract']['exact_phrase_sha256']}",
        f"- positive_case_count: {report['summary']['positive_case_count']}",
        f"- negative_case_count: {report['summary']['negative_case_count']}",
        f"- classification_pass_count: {report['summary']['classification_pass_count']}",
        f"- classification_failure_count: {report['summary']['classification_failure_count']}",
        f"- user_approval_collected_by_this_slice: {str(report['summary']['user_approval_collected_by_this_slice']).lower()}",
        "",
        "## Cases",
        "",
    ]
    for case in report["classification_cases"]:
        result = case["result"]
        lines.extend(
            [
                f"### {case['case_id']}",
                "",
                f"- kind: {case['kind']}",
                f"- expected_match: {str(case['expected_match']).lower()}",
                f"- matched_exact_phrase: {str(result['matched_exact_phrase']).lower()}",
                f"- approval_class: {result['approval_class']}",
                "",
            ]
        )
    lines.extend(
        [
            "## Boundary",
            "",
            "This classifier is a sandbox hardening artifact. A fixture match is not user approval collected now and does not authorize old-file writes.",
            "",
        ]
    )
    return "\n".join(lines)


def build_html(report: dict) -> str:
    rows = "\n".join(
        f"<tr><td>{html.escape(case['case_id'])}</td><td>{html.escape(case['kind'])}</td><td>{str(case['result']['matched_exact_phrase']).lower()}</td><td>{html.escape(case['result']['approval_class'])}</td></tr>"
        for case in report["classification_cases"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>p2-85 Exact Approval Classifier</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f7f8fa; color: #1d2530; }}
    main {{ max-width: 1040px; margin: 0 auto; padding: 32px 20px; }}
    h1 {{ font-size: 28px; margin: 0 0 16px; letter-spacing: 0; }}
    .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 12px; margin-bottom: 22px; }}
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
    <h1>p2-85 Exact Approval Classifier</h1>
    <section class="metrics">
      <div class="metric"><span>Positive cases</span><strong>{report['summary']['positive_case_count']}</strong></div>
      <div class="metric"><span>Negative cases</span><strong>{report['summary']['negative_case_count']}</strong></div>
      <div class="metric"><span>Classification failures</span><strong>{report['summary']['classification_failure_count']}</strong></div>
      <div class="metric"><span>Approval collected now</span><strong>{str(report['summary']['user_approval_collected_by_this_slice']).lower()}</strong></div>
    </section>
    <table>
      <thead><tr><th>Case</th><th>Kind</th><th>Exact Match</th><th>Class</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <section class="boundary">A classifier fixture pass is not user approval and creates no old-file write authority.</section>
  </main>
</body>
</html>
"""


def main() -> None:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    FIXTURES_DIR.mkdir(parents=True, exist_ok=True)
    FAILURE_DIR.mkdir(parents=True, exist_ok=True)

    p2_75 = read_json(P2_75)
    p2_77 = read_json(P2_77)
    exact_phrase = p2_75["request"]["exact_approval_phrase"]
    cases = build_cases(exact_phrase)
    classified = []
    failures = []
    for case in cases:
        result = classify(case["input_text"], exact_phrase)
        passed = result["matched_exact_phrase"] == case["expected_match"] and result["approval_class"] == case["expected_class"]
        if not passed:
            failures.append(case["case_id"])
        classified_case = dict(case)
        classified_case["result"] = result
        classified_case["passed"] = passed
        classified.append(classified_case)
        write_json(FIXTURES_DIR / f"{case['case_id']}.json", classified_case)

    positive = [case for case in classified if case["kind"] == "positive"]
    negative = [case for case in classified if case["kind"] == "negative"]
    report = {
        "record_kind": "sandbox_exact_approval_classifier_hardening",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_75_approval_request": P2_75,
            "p2_77_readiness_gate": P2_77,
            "p2_83_cockpit": P2_83,
            "p2_84_mutation_hardening": P2_84,
        },
        "source_digest": {
            "p2_75_approval_request": sha256_file(P2_75),
            "p2_77_readiness_gate": sha256_file(P2_77),
            "p2_83_cockpit": sha256_file(P2_83),
            "p2_84_mutation_hardening": sha256_file(P2_84),
        },
        "approval_contract": {
            "exact_phrase": exact_phrase,
            "exact_phrase_sha256": sha256_text(exact_phrase),
            "match_rule": "input_text == exact_phrase",
            "normalization_allowed": False,
            "generic_language_is_not_approval": p2_75["request"]["generic_language_is_not_approval"],
            "p2_77_current_readiness": p2_77["current_decision"]["readiness"],
        },
        "summary": {
            "positive_case_count": len(positive),
            "negative_case_count": len(negative),
            "classification_case_count": len(classified),
            "classification_pass_count": sum(1 for case in classified if case["passed"]),
            "classification_failure_count": len(failures),
            "user_approval_collected_by_this_slice": False,
            "old_slice_writes_applied": 0,
            "executor_write_allowed_now": False,
        },
        "classification_failures": failures,
        "classification_cases": classified,
        "authority_flags": {
            "classifier_hardening_only": True,
            "approval_collected": False,
            "fixture_match_is_user_approval": False,
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

    write_json(ARTIFACT_DIR / "exact_approval_classifier_hardening.json", report)
    (ARTIFACT_DIR / "exact_approval_classifier_hardening.md").write_text(build_markdown(report), encoding="utf-8")
    (ARTIFACT_DIR / "exact_approval_classifier_hardening.html").write_text(build_html(report), encoding="utf-8")
    build_failure_cases()
    print(json.dumps({"built": True, "slice_id": SLICE_ID}, indent=2))


if __name__ == "__main__":
    main()
