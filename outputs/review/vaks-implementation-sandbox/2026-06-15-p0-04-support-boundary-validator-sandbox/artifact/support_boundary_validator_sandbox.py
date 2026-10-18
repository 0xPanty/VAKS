#!/usr/bin/env python3
"""Sandbox support-boundary validator for VAKS P0-04.

This script validates one support-claim fixture per Markdown file. It is local to
this sandbox slice. It is not a mainline tool, reviewer approval, reviewed
knowledge, evidence support, or action basis.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any


CANDIDATE_BUCKETS = {"candidate", "project_overlay"}
CANDIDATE_RECORD_KINDS = {
    "candidate_distillation",
    "review_candidate",
    "source_annotation",
    "project_overlay",
}
FEEDBACK_RECORD_KINDS = {"feedback_event", "feedback_summary", "use_ledger"}
LEGACY_METADATA_KINDS = {"legacy_raw_metadata", "legacy_metadata"}
SOURCE_SUMMARY_KINDS = {"source_summary", "architecture_review_summary"}
CLAIM_NOTE_KINDS = {"claim_note", "reviewed_claim", "wiki_claim"}
RANK_FIELDS = {
    "rank_counted_as_support",
    "score_counted_as_support",
    "graph_rank_as_trust",
    "retrieval_rank_as_trust",
}


def parse_scalar(value: str) -> Any:
    value = value.strip()
    if value == "":
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    if (value.startswith('"') and value.endswith('"')) or (
        value.startswith("'") and value.endswith("'")
    ):
        return value[1:-1]
    return value


def parse_frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}

    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}

    data: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, data)]
    for raw_line in lines[1:end]:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        if ":" not in raw_line:
            continue
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        key, raw_value = raw_line.strip().split(":", 1)
        while stack and indent <= stack[-1][0]:
            stack.pop()
        current = stack[-1][1]
        if raw_value.strip() == "":
            child: dict[str, Any] = {}
            current[key] = child
            stack.append((indent, child))
        else:
            current[key] = parse_scalar(raw_value)
    return data


def truthy(data: dict[str, Any], key: str) -> bool:
    return bool(data.get(key))


def has_current_anchor(data: dict[str, Any]) -> bool:
    if data.get("anchor_type") in {
        "raw_span",
        "source_snapshot",
        "code_line",
        "quote",
        "transcript_segment",
        "stable_artifact",
    }:
        return bool(data.get("independent_anchor_ref") and data.get("anchor_selector"))
    return False


def validation_codes(path: Path) -> dict[str, Any]:
    data = parse_frontmatter(path.read_text(encoding="utf-8"))
    support_claimed = truthy(data, "support_claimed") or data.get("pack_role") == "support"
    evidence_role = data.get("evidence_role")
    record_kind = data.get("proposed_support_record_kind")
    bucket = data.get("proposed_support_authority_bucket")
    target_ref = data.get("target_ref")
    support_ref = data.get("proposed_support_ref")

    codes: list[str] = []
    warnings: list[str] = []

    if support_claimed and (bucket in CANDIDATE_BUCKETS or record_kind in CANDIDATE_RECORD_KINDS):
        codes.append("candidate_as_support")

    if support_claimed and evidence_role == "direct_support" and truthy(data, "url_only"):
        codes.append("url_only_direct_support")

    if support_claimed and any(truthy(data, key) for key in RANK_FIELDS):
        codes.append("rank_or_score_as_support_or_trust")

    if support_claimed and (
        bucket == "feedback" or record_kind in FEEDBACK_RECORD_KINDS or truthy(data, "feedback_used_as_support")
    ):
        codes.append("feedback_as_support")

    if support_claimed and (
        record_kind in SOURCE_SUMMARY_KINDS and truthy(data, "source_summary_self_support")
    ):
        codes.append("source_summary_self_support")

    if support_claimed and (
        target_ref == support_ref
        or record_kind in CLAIM_NOTE_KINDS and truthy(data, "claim_note_self_support")
    ):
        codes.append("claim_note_self_support_loop")

    if support_claimed and (
        record_kind in LEGACY_METADATA_KINDS or truthy(data, "legacy_raw_metadata_used_as_support")
    ):
        codes.append("legacy_metadata_support")

    if support_claimed and evidence_role == "background_context":
        codes.append("background_context_counted_as_support")

    if (
        not codes
        and support_claimed
        and evidence_role in {"direct_support", "inferential_support"}
        and not has_current_anchor(data)
    ):
        codes.append("support_claim_missing_independent_anchor")

    if (
        not codes
        and support_claimed
        and evidence_role == "inferential_support"
        and not data.get("reviewer_note")
    ):
        codes.append("inferential_support_missing_reviewer_note")

    return {
        "record": str(path),
        "valid": not codes,
        "codes": codes,
        "warnings": warnings,
        "authority_boundary": {
            "validator_pass_is_not_evidence_support": True,
            "validator_pass_is_not_reviewer_approval": True,
            "validator_pass_is_not_reviewed_knowledge": True,
            "validator_pass_is_not_action_basis": True,
            "sandbox_not_mainline": True,
        },
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate sandbox support-boundary fixture records."
    )
    parser.add_argument("records", nargs="+", help="Support-boundary fixture records.")
    parser.add_argument("--json", action="store_true", help="Emit JSON lines.")
    args = parser.parse_args(argv)

    any_invalid = False
    for raw_record in args.records:
        result = validation_codes(Path(raw_record).resolve())
        any_invalid = any_invalid or not result["valid"]
        if args.json:
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        elif result["valid"]:
            warnings = ",".join(result["warnings"]) if result["warnings"] else "none"
            print(f"PASS {result['record']} warnings={warnings}")
        else:
            print(f"FAIL {result['record']} codes={','.join(result['codes'])}")
    return 1 if any_invalid else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
