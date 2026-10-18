from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-19-p2-94-opus-review-submission-packet-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = ROOT / "outputs/review/vaks-implementation-sandbox"
SLICE_DIR = SANDBOX_ROOT / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

P2_93_DIR = SANDBOX_ROOT / "2026-06-19-p2-93-opus-reviewable-closeout-packet-sandbox"
P2_93_PACKET_JSON = P2_93_DIR / "artifact/opus_reviewable_closeout_packet.json"
P2_93_PACKET_MD = P2_93_DIR / "artifact/opus_reviewable_closeout_packet.md"
P2_93_CHECKLIST = P2_93_DIR / "artifact/opus-review-checklist.md"
P2_93_VERIFICATION = P2_93_DIR / "verification.md"
P2_93_PRODUCT = P2_93_DIR / "product-acceptance-report.md"
P2_92_AUDIT_JSON = (
    SANDBOX_ROOT
    / "2026-06-19-p2-92-post-apply-current-strict-closeout-audit-sandbox/artifact/post_apply_current_strict_closeout_audit.json"
)
P2_91_EXECUTOR_JSON = (
    SANDBOX_ROOT
    / "2026-06-19-p2-91-old-file-status-normalization-executor-apply-sandbox/artifact/old_file_status_normalization_executor_apply.json"
)


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


def build_manifest(p2_93: dict, p2_92: dict, p2_91: dict) -> dict:
    evidence_items = [
        {
            "id": "EVIDENCE-P2-93-PACKET-MD",
            "path": rel(P2_93_PACKET_MD),
            "purpose": "Human-readable closeout packet for external Opus review.",
            "required": True,
        },
        {
            "id": "EVIDENCE-P2-93-CHECKLIST",
            "path": rel(P2_93_CHECKLIST),
            "purpose": "External review checklist.",
            "required": True,
        },
        {
            "id": "EVIDENCE-P2-93-PACKET-JSON",
            "path": rel(P2_93_PACKET_JSON),
            "purpose": "Machine-readable closeout packet summary.",
            "required": True,
        },
        {
            "id": "EVIDENCE-P2-93-VERIFICATION",
            "path": rel(P2_93_VERIFICATION),
            "purpose": "p2-93 final gate evidence.",
            "required": True,
        },
        {
            "id": "EVIDENCE-P2-93-PRODUCT",
            "path": rel(P2_93_PRODUCT),
            "purpose": "GPT-5.5 Product Acceptance for p2-93.",
            "required": True,
        },
        {
            "id": "EVIDENCE-P2-92-AUDIT",
            "path": rel(P2_92_AUDIT_JSON),
            "purpose": "Post-apply current-strict closeout audit for original 20 slices.",
            "required": True,
        },
        {
            "id": "EVIDENCE-P2-91-EXECUTOR",
            "path": rel(P2_91_EXECUTOR_JSON),
            "purpose": "Approved old-file status-only normalization executor evidence.",
            "required": True,
        },
    ]
    review_questions = [
        "Does the packet prove p2-91 applied only the approved 75 old-file frontmatter status changes?",
        "Does p2-92 prove the original 20 sandbox slices now satisfy current strict closeout labels?",
        "Is body content preserved for all 75 old report files?",
        "Is non-status frontmatter preserved for all 75 old report files?",
        "Does any artifact confuse sandbox closeout with mainline merge, reviewed knowledge, evidence support, action basis, or Opus approval?",
        "Is the evidence sufficient for external acceptance of sandbox closeout, while still requiring separate user approval for any mainline integration?",
    ]
    return {
        "record_kind": "opus_review_evidence_manifest",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "evidence_items": evidence_items,
        "review_questions": review_questions,
        "derived_from": {
            "p2_93_external_review_packet_ready": p2_93["summary"]["external_review_packet_ready"],
            "p2_93_opus_approval_claimed": p2_93["summary"]["opus_approval_claimed"],
            "p2_91_old_slice_writes_applied": p2_91["summary"]["old_slice_writes_applied"],
            "p2_92_current_strict_complete_original_item_count": p2_92["summary"][
                "current_strict_complete_original_item_count"
            ],
            "p2_92_status_operation_count": p2_92["summary"]["status_operation_count"],
        },
    }


def build_submission_prompt(manifest: dict, p2_93: dict) -> str:
    evidence_lines = "\n".join(f"- `{item['path']}`: {item['purpose']}" for item in manifest["evidence_items"])
    question_lines = "\n".join(f"{idx + 1}. {question}" for idx, question in enumerate(manifest["review_questions"]))
    return f"""# Prompt For Opus External Review

You are Opus acting as an independent external reviewer for a VAKS sandbox closeout. Review the local evidence files listed below. Do not assume sandbox closeout means mainline merge, reviewed knowledge, evidence support, action basis, or user approval. This submission packet does not claim Opus approval before you review it.

## Evidence Files To Inspect

{evidence_lines}

## Review Questions

{question_lines}

## Required Output Format

Return exactly one conclusion token on the first line:

- `OPUS_PASS_SANDBOX_CLOSEOUT`
- `OPUS_REVISE_SANDBOX_CLOSEOUT`
- `OPUS_BLOCKED_NEEDS_USER`

Then provide:

- key evidence checked;
- any blockers or missing proof;
- whether the packet is understandable to a future agent;
- explicit boundary verdict: whether it avoids claiming mainline merge, reviewed knowledge, evidence support, action basis, user approval, or Opus approval before this review.

## Current Packet Summary

```json
{json.dumps(p2_93["summary"], ensure_ascii=False, indent=2)}
```
"""


def build_manifest_markdown(manifest: dict) -> str:
    evidence_rows = "\n".join(
        f"| `{item['id']}` | `{item['path']}` | {item['purpose']} | `{item['required']}` |"
        for item in manifest["evidence_items"]
    )
    questions = "\n".join(f"- {question}" for question in manifest["review_questions"])
    return f"""# Opus Review Evidence Manifest

## Evidence Items

| ID | Path | Purpose | Required |
| --- | --- | --- | --- |
{evidence_rows}

## Review Questions

{questions}

## Derived Summary

```json
{json.dumps(manifest["derived_from"], ensure_ascii=False, indent=2)}
```
"""


def build_result_intake_gate() -> str:
    return """# Opus Result Intake Gate

## Allowed External Conclusions

- `OPUS_PASS_SANDBOX_CLOSEOUT`: Opus accepts the sandbox closeout evidence as externally reviewable and sufficient for sandbox closeout only.
- `OPUS_REVISE_SANDBOX_CLOSEOUT`: stay in the current sandbox review lane and fix the listed blockers before any further claim.
- `OPUS_BLOCKED_NEEDS_USER`: stop and ask the user for missing evidence, scope clarification, or external-state change.

## Not Allowed

- Do not translate Opus pass into mainline merge.
- Do not translate Opus pass into reviewed knowledge, evidence support, or action basis.
- Do not claim Opus approval unless an actual external Opus conclusion is present.
- Do not commit, push, sync, or promote.
- Do not edit root architecture docs, README, tools, templates, wiki truth layers, or Obsidian vault from this gate.

## Required Intake Record If Opus Responds

Create a later sandbox-only slice that stores:

- Opus raw conclusion token;
- Opus reviewed evidence list;
- Opus blockers, if any;
- boundary audit confirming the result is not mainline approval;
- Product Acceptance deciding the next sandbox step.
"""


def build_packet() -> dict:
    p2_93 = load_json(P2_93_PACKET_JSON)
    p2_92 = load_json(P2_92_AUDIT_JSON)
    p2_91 = load_json(P2_91_EXECUTOR_JSON)
    manifest = build_manifest(p2_93, p2_92, p2_91)
    summary = {
        "evidence_item_count": len(manifest["evidence_items"]),
        "review_question_count": len(manifest["review_questions"]),
        "required_conclusion_token_count": 3,
        "p2_93_external_review_packet_ready": p2_93["summary"]["external_review_packet_ready"],
        "p2_93_opus_approval_claimed": p2_93["summary"]["opus_approval_claimed"],
        "p2_91_old_slice_writes_applied": p2_91["summary"]["old_slice_writes_applied"],
        "p2_91_protected_path_writes": p2_91["summary"]["protected_path_writes"],
        "p2_92_status_operation_count": p2_92["summary"]["status_operation_count"],
        "p2_92_current_strict_complete_original_item_count": p2_92["summary"][
            "current_strict_complete_original_item_count"
        ],
        "submission_packet_ready": True,
        "opus_review_performed": False,
        "opus_approval_claimed": False,
        "mainline_ready": False,
        "promotion_ready": False,
        "reviewed_knowledge_ready": False,
        "evidence_support_ready": False,
        "action_basis_ready": False,
        "goal_complete_now": False,
    }
    return {
        "record_kind": "opus_review_submission_packet",
        "slice_id": SLICE_ID,
        "created_at": datetime.now(timezone.utc).isoformat(),
        "summary": summary,
        "manifest": manifest,
        "submission_prompt_path": "artifact/opus-review-submission-prompt.md",
        "result_intake_gate_path": "artifact/opus-result-intake-gate.md",
        "allowed_external_conclusions": [
            "OPUS_PASS_SANDBOX_CLOSEOUT",
            "OPUS_REVISE_SANDBOX_CLOSEOUT",
            "OPUS_BLOCKED_NEEDS_USER",
        ],
        "authority_flags": {
            "submission_packet_only": True,
            "opus_review_performed": False,
            "opus_approval_claimed": False,
            "mainline_merge": False,
            "promotion": False,
            "reviewed_knowledge": False,
            "evidence_support": False,
            "action_basis": False,
            "user_mainline_approval": False,
            "commit_push_sync": False,
        },
    }


def write_fixtures(packet: dict) -> None:
    s = packet["summary"]
    write_json(
        FIXTURES_DIR / "submission-prompt-ready.json",
        {
            "case_id": "submission-prompt-ready",
            "evidence_item_count": s["evidence_item_count"],
            "review_question_count": s["review_question_count"],
            "submission_packet_ready": s["submission_packet_ready"],
            "passed": s["evidence_item_count"] >= 7 and s["review_question_count"] >= 6 and s["submission_packet_ready"],
        },
    )
    write_json(
        FIXTURES_DIR / "p2-93-evidence-ready-not-opus-approved.json",
        {
            "case_id": "p2-93-evidence-ready-not-opus-approved",
            "p2_93_external_review_packet_ready": s["p2_93_external_review_packet_ready"],
            "p2_93_opus_approval_claimed": s["p2_93_opus_approval_claimed"],
            "passed": s["p2_93_external_review_packet_ready"] and not s["p2_93_opus_approval_claimed"],
        },
    )
    write_json(
        FIXTURES_DIR / "p2-91-p2-92-proof-carried-forward.json",
        {
            "case_id": "p2-91-p2-92-proof-carried-forward",
            "p2_91_old_slice_writes_applied": s["p2_91_old_slice_writes_applied"],
            "p2_91_protected_path_writes": s["p2_91_protected_path_writes"],
            "p2_92_status_operation_count": s["p2_92_status_operation_count"],
            "p2_92_current_strict_complete_original_item_count": s[
                "p2_92_current_strict_complete_original_item_count"
            ],
            "passed": s["p2_91_old_slice_writes_applied"] == 75
            and s["p2_91_protected_path_writes"] == 0
            and s["p2_92_status_operation_count"] == 75
            and s["p2_92_current_strict_complete_original_item_count"] == 20,
        },
    )
    write_json(
        FIXTURES_DIR / "allowed-opus-conclusions.json",
        {
            "case_id": "allowed-opus-conclusions",
            "allowed_external_conclusions": packet["allowed_external_conclusions"],
            "passed": packet["allowed_external_conclusions"]
            == [
                "OPUS_PASS_SANDBOX_CLOSEOUT",
                "OPUS_REVISE_SANDBOX_CLOSEOUT",
                "OPUS_BLOCKED_NEEDS_USER",
            ],
        },
    )
    write_json(
        FIXTURES_DIR / "authority-boundaries-false.json",
        {
            "case_id": "authority-boundaries-false",
            "opus_review_performed": s["opus_review_performed"],
            "opus_approval_claimed": s["opus_approval_claimed"],
            "mainline_ready": s["mainline_ready"],
            "reviewed_knowledge_ready": s["reviewed_knowledge_ready"],
            "evidence_support_ready": s["evidence_support_ready"],
            "action_basis_ready": s["action_basis_ready"],
            "goal_complete_now": s["goal_complete_now"],
            "passed": not any(
                [
                    s["opus_review_performed"],
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


def write_failure_cases() -> None:
    write_json(
        FAILURE_DIR / "opus-review-submission-packet-failures.json",
        {
            "record_kind": "opus_review_submission_packet_failure_cases",
            "slice_id": SLICE_ID,
            "failure_cases": [
                {
                    "case_id": "P2-94-FAIL-01-missing-submission-prompt",
                    "must_fail_when": "No copy-paste Opus prompt is produced.",
                },
                {
                    "case_id": "P2-94-FAIL-02-missing-evidence-manifest",
                    "must_fail_when": "The packet lacks exact evidence paths or review questions.",
                },
                {
                    "case_id": "P2-94-FAIL-03-missing-result-intake-gate",
                    "must_fail_when": "The packet does not define allowed Opus conclusions and next actions.",
                },
                {
                    "case_id": "P2-94-FAIL-04-opus-approval-claimed",
                    "must_fail_when": "The packet claims Opus has already reviewed or approved the work.",
                },
                {
                    "case_id": "P2-94-FAIL-05-mainline-or-truth-authority-claimed",
                    "must_fail_when": "The packet claims mainline readiness, reviewed knowledge, evidence support, or action basis.",
                },
                {
                    "case_id": "P2-94-FAIL-06-p2-93-not-ready",
                    "must_fail_when": "p2-93 no longer proves external review packet readiness.",
                },
                {
                    "case_id": "P2-94-FAIL-07-p2-91-p2-92-proof-not-carried",
                    "must_fail_when": "p2-91/p2-92 proof counts are missing or no longer match expected values.",
                },
                {
                    "case_id": "P2-94-FAIL-08-protected-path-write",
                    "must_fail_when": "This slice writes outside its own sandbox path.",
                },
            ],
        },
    )


def write_outputs(packet: dict) -> None:
    manifest = packet["manifest"]
    p2_93 = load_json(P2_93_PACKET_JSON)
    write_json(ARTIFACT_DIR / "opus-review-evidence-manifest.json", manifest)
    write_text(ARTIFACT_DIR / "opus-review-evidence-manifest.md", build_manifest_markdown(manifest))
    write_text(ARTIFACT_DIR / "opus-review-submission-prompt.md", build_submission_prompt(manifest, p2_93))
    write_text(ARTIFACT_DIR / "opus-result-intake-gate.md", build_result_intake_gate())
    write_json(ARTIFACT_DIR / "opus-review-submission-packet.json", packet)
    write_fixtures(packet)
    write_failure_cases()


def main() -> None:
    packet = build_packet()
    write_outputs(packet)
    print(json.dumps({"written": True, "summary": packet["summary"]}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
