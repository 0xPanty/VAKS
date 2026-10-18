from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-98-single-file-opus-review-dossier-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = ROOT / "outputs/review/vaks-implementation-sandbox"
SLICE_DIR = SANDBOX_ROOT / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

P2_91 = SANDBOX_ROOT / "2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox/artifact/old_file_status_normalization_executor_apply.json"
P2_92 = SANDBOX_ROOT / "2026-06-19-p2-92-post-apply-current-strict-closeout-audit-sandbox/artifact/post_apply_current_strict_closeout_audit.json"
P2_94 = SANDBOX_ROOT / "2026-06-19-p2-94-opus-review-submission-packet-sandbox/artifact/opus-review-submission-packet.json"
P2_96 = SANDBOX_ROOT / "2026-06-19-p2-96-opus-result-intake-skeleton-sandbox/artifact/opus-result-intake-status.json"
P2_97 = SANDBOX_ROOT / "2026-06-19-p2-97-external-review-wait-state-guard-sandbox/artifact/external-review-wait-state-guard.json"


def rel(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def build_dossier() -> dict:
    p2_91 = load_json(P2_91)
    p2_92 = load_json(P2_92)
    p2_94 = load_json(P2_94)
    p2_96 = load_json(P2_96)
    p2_97 = load_json(P2_97)
    allowed_tokens = p2_94["allowed_external_conclusions"]
    summary = {
        "dossier_ready": True,
        "evidence_digest_count": 5,
        "allowed_conclusion_token_count": len(allowed_tokens),
        "p2_91_old_slice_writes_applied": p2_91["summary"]["old_slice_writes_applied"],
        "p2_91_protected_path_writes": p2_91["summary"]["protected_path_writes"],
        "p2_92_original_item_count": p2_92["summary"]["original_item_count"],
        "p2_92_current_strict_complete_original_item_count": p2_92["summary"][
            "current_strict_complete_original_item_count"
        ],
        "p2_94_submission_packet_ready": p2_94["summary"]["submission_packet_ready"],
        "p2_96_result_intake_ready": p2_96["summary"]["result_intake_ready"],
        "p2_97_guard_state": p2_97["summary"]["guard_state"],
        "actual_opus_result_present": False,
        "opus_approval_claimed": False,
        "mainline_ready": False,
        "reviewed_knowledge_ready": False,
        "evidence_support_ready": False,
        "action_basis_ready": False,
        "goal_complete_now": False,
    }
    return {
        "record_kind": "single_file_opus_review_dossier",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "source_inputs": {
            "p2_91": rel(P2_91),
            "p2_92": rel(P2_92),
            "p2_94": rel(P2_94),
            "p2_96": rel(P2_96),
            "p2_97": rel(P2_97),
        },
        "summary": summary,
        "allowed_conclusion_tokens": allowed_tokens,
        "review_questions": p2_94["manifest"]["review_questions"],
        "evidence_digest": [
            {
                "id": "p2-91",
                "verdict": "approved old-file status-only normalization applied",
                "key_counts": {
                    "old_slice_writes_applied": p2_91["summary"]["old_slice_writes_applied"],
                    "protected_path_writes": p2_91["summary"]["protected_path_writes"],
                    "body_unchanged_count": p2_91["summary"]["body_unchanged_count"],
                    "non_status_frontmatter_unchanged_count": p2_91["summary"][
                        "non_status_frontmatter_unchanged_count"
                    ],
                },
            },
            {
                "id": "p2-92",
                "verdict": "original 20 slices current-strict complete",
                "key_counts": {
                    "original_item_count": p2_92["summary"]["original_item_count"],
                    "status_operation_count": p2_92["summary"]["status_operation_count"],
                    "current_strict_complete_original_item_count": p2_92["summary"][
                        "current_strict_complete_original_item_count"
                    ],
                    "body_unchanged_count": p2_92["summary"]["body_unchanged_count"],
                    "non_status_frontmatter_unchanged_count": p2_92["summary"][
                        "non_status_frontmatter_unchanged_count"
                    ],
                },
            },
            {
                "id": "p2-94",
                "verdict": "external review submission packet ready",
                "key_counts": {
                    "evidence_item_count": p2_94["summary"]["evidence_item_count"],
                    "review_question_count": p2_94["summary"]["review_question_count"],
                    "submission_packet_ready": p2_94["summary"]["submission_packet_ready"],
                },
            },
            {
                "id": "p2-96",
                "verdict": "future Opus result intake skeleton ready",
                "key_counts": {
                    "result_intake_ready": p2_96["summary"]["result_intake_ready"],
                    "actual_opus_result_present": p2_96["summary"]["actual_opus_result_present"],
                    "opus_approval_claimed": p2_96["summary"]["opus_approval_claimed"],
                },
            },
            {
                "id": "p2-97",
                "verdict": "STOP/WAIT guard active",
                "key_counts": {
                    "guard_state": p2_97["summary"]["guard_state"],
                    "external_opus_review_pending": p2_97["summary"]["external_opus_review_pending"],
                    "may_merge_mainline": p2_97["summary"]["may_merge_mainline"],
                    "may_claim_complete": p2_97["summary"]["may_claim_complete"],
                },
            },
        ],
        "authority_flags": {
            "dossier_only": True,
            "actual_opus_result_present": False,
            "opus_approval_claimed": False,
            "mainline_merge": False,
            "reviewed_knowledge": False,
            "evidence_support": False,
            "action_basis": False,
            "goal_complete_now": False,
        },
    }


def render_dossier_md(dossier: dict) -> str:
    s = dossier["summary"]
    summary_rows = "\n".join(f"| `{key}` | `{value}` |" for key, value in s.items())
    tokens = "\n".join(f"- `{token}`" for token in dossier["allowed_conclusion_tokens"])
    questions = "\n".join(f"{idx + 1}. {q}" for idx, q in enumerate(dossier["review_questions"]))
    evidence_sections = []
    for item in dossier["evidence_digest"]:
        counts = "\n".join(f"  - `{k}`: `{v}`" for k, v in item["key_counts"].items())
        evidence_sections.append(f"### {item['id']}\n\nVerdict: {item['verdict']}\n\n{counts}")
    evidence_text = "\n\n".join(evidence_sections)
    return f"""# Single-File Opus Review Dossier

## Instruction To Opus

You are reviewing VAKS sandbox closeout evidence. Decide whether the sandbox closeout evidence is acceptable for sandbox closeout only. Do not treat any pass as mainline approval, reviewed knowledge, evidence support, action basis, commit, push, or sync.

## Current Boundary

Actual Opus result is not present. Opus approval is not claimed. Mainline is not ready. Goal is not complete.

## Summary

| Field | Value |
| --- | --- |
{summary_rows}

## Evidence Digest

{evidence_text}

## Review Questions

{questions}

## Allowed First-Line Conclusion Tokens

{tokens}

## Required Output

First line must be one allowed token. Then list evidence checked, blockers if any, and an explicit boundary verdict.

## No-Merge Rule

Do not merge mainline, do not claim completion, and do not create reviewed knowledge, evidence support, or action basis from this dossier. A later sandbox-only result intake slice must validate the real Opus response.
"""


def write_fixtures(dossier: dict) -> None:
    s = dossier["summary"]
    write_json(
        FIXTURES_DIR / "dossier-ready.json",
        {
            "case_id": "dossier-ready",
            "dossier_ready": s["dossier_ready"],
            "evidence_digest_count": s["evidence_digest_count"],
            "allowed_conclusion_token_count": s["allowed_conclusion_token_count"],
            "passed": s["dossier_ready"] and s["evidence_digest_count"] == 5 and s["allowed_conclusion_token_count"] == 3,
        },
    )
    write_json(
        FIXTURES_DIR / "p2-91-p2-92-evidence-carried.json",
        {
            "case_id": "p2-91-p2-92-evidence-carried",
            "p2_91_old_slice_writes_applied": s["p2_91_old_slice_writes_applied"],
            "p2_92_current_strict_complete_original_item_count": s[
                "p2_92_current_strict_complete_original_item_count"
            ],
            "passed": s["p2_91_old_slice_writes_applied"] == 75
            and s["p2_92_current_strict_complete_original_item_count"] == 20,
        },
    )
    write_json(
        FIXTURES_DIR / "external-review-and-intake-ready.json",
        {
            "case_id": "external-review-and-intake-ready",
            "p2_94_submission_packet_ready": s["p2_94_submission_packet_ready"],
            "p2_96_result_intake_ready": s["p2_96_result_intake_ready"],
            "p2_97_guard_state": s["p2_97_guard_state"],
            "passed": s["p2_94_submission_packet_ready"]
            and s["p2_96_result_intake_ready"]
            and s["p2_97_guard_state"] == "STOP_WAIT_EXTERNAL_OPUS_REVIEW",
        },
    )
    write_json(
        FIXTURES_DIR / "authority-boundary-false.json",
        {
            "case_id": "authority-boundary-false",
            "actual_opus_result_present": s["actual_opus_result_present"],
            "opus_approval_claimed": s["opus_approval_claimed"],
            "mainline_ready": s["mainline_ready"],
            "reviewed_knowledge_ready": s["reviewed_knowledge_ready"],
            "evidence_support_ready": s["evidence_support_ready"],
            "action_basis_ready": s["action_basis_ready"],
            "goal_complete_now": s["goal_complete_now"],
            "passed": not any(
                [
                    s["actual_opus_result_present"],
                    s["opus_approval_claimed"],
                    s["mainline_ready"],
                    s["reviewed_knowledge_ready"],
                    s["evidence_support_ready"],
                    s["action_basis_ready"],
                    s["goal_complete_now"],
                ]
            ),
        },
    )
    write_json(
        FIXTURES_DIR / "allowed-tokens-exact.json",
        {
            "case_id": "allowed-tokens-exact",
            "allowed_conclusion_tokens": dossier["allowed_conclusion_tokens"],
            "passed": dossier["allowed_conclusion_tokens"]
            == [
                "OPUS_PASS_SANDBOX_CLOSEOUT",
                "OPUS_REVISE_SANDBOX_CLOSEOUT",
                "OPUS_BLOCKED_NEEDS_USER",
            ],
        },
    )


def write_failure_cases() -> None:
    write_json(
        FAILURE_DIR / "single-file-opus-review-dossier-failures.json",
        {
            "record_kind": "single_file_opus_review_dossier_failure_cases",
            "slice_id": SLICE_ID,
            "failure_cases": [
                {
                    "case_id": "P2-98-FAIL-01-missing-dossier",
                    "must_fail_when": "The single-file dossier is missing.",
                },
                {
                    "case_id": "P2-98-FAIL-02-missing-evidence-digest",
                    "must_fail_when": "The dossier omits one of p2-91, p2-92, p2-94, p2-96, or p2-97.",
                },
                {
                    "case_id": "P2-98-FAIL-03-wrong-opus-token-set",
                    "must_fail_when": "The dossier changes or expands the allowed Opus conclusion tokens.",
                },
                {
                    "case_id": "P2-98-FAIL-04-opus-approval-claimed",
                    "must_fail_when": "The dossier claims actual Opus approval.",
                },
                {
                    "case_id": "P2-98-FAIL-05-mainline-or-truth-authority-claimed",
                    "must_fail_when": "The dossier claims mainline readiness, reviewed knowledge, evidence support, or action basis.",
                },
                {
                    "case_id": "P2-98-FAIL-06-goal-complete-claimed",
                    "must_fail_when": "The dossier claims the overall goal is complete.",
                },
                {
                    "case_id": "P2-98-FAIL-07-no-intake-instruction",
                    "must_fail_when": "The dossier omits the requirement for later sandbox-only result intake.",
                },
                {
                    "case_id": "P2-98-FAIL-08-protected-path-write",
                    "must_fail_when": "This slice writes outside its own sandbox path.",
                },
            ],
        },
    )


def write_outputs() -> dict:
    dossier = build_dossier()
    write_json(ARTIFACT_DIR / "single-file-opus-review-dossier.json", dossier)
    write_text(ARTIFACT_DIR / "single-file-opus-review-dossier.md", render_dossier_md(dossier))
    write_fixtures(dossier)
    write_failure_cases()
    return dossier


def main() -> None:
    dossier = write_outputs()
    print(json.dumps({"written": True, "summary": dossier["summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()

