#!/usr/bin/env python
"""Merge returned semantic-support Judge A/B CSVs without promoting truth.

This helper is for the Source Intake generic read-only loop sandbox package.
It validates two independent judge returns against the original dispatch
template, merges matching rows, and emits an arbitration queue for disagreements
or missing fields. It does not decide P0, production readiness, reviewed truth,
or action support.
"""

from __future__ import annotations

import argparse
import csv
import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


VISIBLE_FIELDS = [
    "row_id",
    "query",
    "answer_use_claim",
    "anchor_ref",
    "anchor_source_hash",
    "frozen_snapshot_ref",
    "anchor_excerpt",
]

JUDGE_A_FIELDS = [
    "judge_a_id",
    "judge_a_judged_at",
    "judge_a_relevance_0_2",
    "judge_a_sufficiency_0_2",
    "judge_a_notes",
]

JUDGE_B_FIELDS = [
    "judge_b_id",
    "judge_b_judged_at",
    "judge_b_relevance_0_2",
    "judge_b_sufficiency_0_2",
    "judge_b_notes",
]

ARBITER_FIELDS = [
    "arbiter_id",
    "arbiter_judged_at",
    "arbiter_final_relevance_0_2",
    "arbiter_final_sufficiency_0_2",
    "arbiter_notes",
]

MERGED_FIELDS = [
    *VISIBLE_FIELDS,
    *JUDGE_A_FIELDS,
    *JUDGE_B_FIELDS,
    "judge_agreement_status",
    "needs_arbitration",
    "row_validation_errors",
    *ARBITER_FIELDS,
]

VALID_SCORE_VALUES = {"0", "1", "2"}


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return [dict(row) for row in csv.DictReader(f)]


def write_csv(path: Path, rows: list[dict[str, Any]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def required_missing(row: dict[str, str], fields: list[str]) -> list[str]:
    return [field for field in fields if not str(row.get(field, "")).strip()]


def invalid_scores(row: dict[str, str], fields: list[str]) -> list[str]:
    bad: list[str] = []
    for field in fields:
        value = str(row.get(field, "")).strip()
        if value and value not in VALID_SCORE_VALUES:
            bad.append(field)
    return bad


def index_by_row_id(rows: list[dict[str, str]], label: str) -> tuple[dict[str, dict[str, str]], list[str]]:
    indexed: dict[str, dict[str, str]] = {}
    errors: list[str] = []
    for i, row in enumerate(rows, start=2):
        row_id = str(row.get("row_id", "")).strip()
        if not row_id:
            errors.append(f"{label}: row {i} missing row_id")
            continue
        if row_id in indexed:
            errors.append(f"{label}: duplicate row_id {row_id}")
            continue
        indexed[row_id] = row
    return indexed, errors


def visible_mismatch(a: dict[str, str], b: dict[str, str]) -> list[str]:
    return [
        field
        for field in VISIBLE_FIELDS
        if str(a.get(field, "")).strip() != str(b.get(field, "")).strip()
    ]


def baseline_visible_mismatch(row: dict[str, str], baseline: dict[str, str]) -> list[str]:
    return [
        field
        for field in VISIBLE_FIELDS
        if str(row.get(field, "")).strip() != str(baseline.get(field, "")).strip()
    ]


def load_baseline(path: Path) -> tuple[list[str], dict[str, dict[str, str]], list[str]]:
    rows = read_csv(path)
    indexed, errors = index_by_row_id(rows, "base_template")
    ordered_ids = [str(row.get("row_id", "")).strip() for row in rows if str(row.get("row_id", "")).strip()]
    return ordered_ids, indexed, errors


def merge(judge_a: Path, judge_b: Path, out_dir: Path, base_template: Path | None = None) -> dict[str, Any]:
    a_rows = read_csv(judge_a)
    b_rows = read_csv(judge_b)
    a_by_id, errors = index_by_row_id(a_rows, "judge_a")
    b_by_id, b_errors = index_by_row_id(b_rows, "judge_b")
    errors.extend(b_errors)

    baseline_by_id: dict[str, dict[str, str]] = {}
    expected_ids: list[str] = []
    unexpected_ids: list[str] = []
    if base_template:
        expected_ids, baseline_by_id, baseline_errors = load_baseline(base_template)
        errors.extend(baseline_errors)
        expected_set = set(expected_ids)
        returned_set = set(a_by_id) | set(b_by_id)
        missing_expected = sorted(expected_set - returned_set)
        unexpected_ids = sorted(returned_set - expected_set)
        for row_id in missing_expected:
            errors.append(f"row_id {row_id}: missing from both judge returns")
        for row_id in unexpected_ids:
            errors.append(f"row_id {row_id}: unexpected row_id not present in base template")
        all_ids = expected_ids + unexpected_ids
    else:
        errors.append("base_template: not provided; dispatch baseline integrity was not checked")
        all_ids = sorted(set(a_by_id) | set(b_by_id))

    merged_rows: list[dict[str, Any]] = []
    arbitration_rows: list[dict[str, Any]] = []

    completed_a = 0
    completed_b = 0
    agreement_count = 0
    disagreement_count = 0
    missing_or_invalid_count = 0

    for row_id in all_ids:
        a = a_by_id.get(row_id)
        b = b_by_id.get(row_id)
        baseline = baseline_by_id.get(row_id, {"row_id": row_id})
        row_errors: list[str] = []
        if not a or not b:
            missing_side = "both judge returns" if not a and not b else "one judge return"
            row_errors.append(f"missing from {missing_side}")
            errors.append(f"row_id {row_id}: missing from {missing_side}")
            base = baseline or a or b or {"row_id": row_id}
            row = {field: base.get(field, "") for field in VISIBLE_FIELDS}
            row.update({
                "judge_agreement_status": "missing_judge_return",
                "needs_arbitration": True,
                "row_validation_errors": "; ".join(row_errors),
            })
            merged_rows.append(row)
            arbitration_rows.append(row)
            missing_or_invalid_count += 1
            continue

        mismatch = visible_mismatch(a, b)
        if mismatch:
            row_errors.append(f"visible field mismatch between returns: {', '.join(mismatch)}")
            errors.append(f"row_id {row_id}: visible field mismatch between returns {mismatch}")
        if base_template and baseline:
            a_baseline_mismatch = baseline_visible_mismatch(a, baseline)
            b_baseline_mismatch = baseline_visible_mismatch(b, baseline)
            if a_baseline_mismatch:
                row_errors.append(f"judge_a visible fields changed from base template: {', '.join(a_baseline_mismatch)}")
                errors.append(f"row_id {row_id}: judge_a visible fields changed from base template {a_baseline_mismatch}")
            if b_baseline_mismatch:
                row_errors.append(f"judge_b visible fields changed from base template: {', '.join(b_baseline_mismatch)}")
                errors.append(f"row_id {row_id}: judge_b visible fields changed from base template {b_baseline_mismatch}")

        a_missing = required_missing(a, ["judge_a_id", "judge_a_judged_at", "judge_a_relevance_0_2", "judge_a_sufficiency_0_2"])
        b_missing = required_missing(b, ["judge_b_id", "judge_b_judged_at", "judge_b_relevance_0_2", "judge_b_sufficiency_0_2"])
        a_bad = invalid_scores(a, ["judge_a_relevance_0_2", "judge_a_sufficiency_0_2"])
        b_bad = invalid_scores(b, ["judge_b_relevance_0_2", "judge_b_sufficiency_0_2"])
        if a_missing:
            row_errors.append(f"judge_a missing required fields: {', '.join(a_missing)}")
            errors.append(f"row_id {row_id}: judge_a missing required fields {a_missing}")
        if b_missing:
            row_errors.append(f"judge_b missing required fields: {', '.join(b_missing)}")
            errors.append(f"row_id {row_id}: judge_b missing required fields {b_missing}")
        if a_bad:
            row_errors.append(f"judge_a invalid score fields: {', '.join(a_bad)}")
            errors.append(f"row_id {row_id}: judge_a invalid score fields {a_bad}")
        if b_bad:
            row_errors.append(f"judge_b invalid score fields: {', '.join(b_bad)}")
            errors.append(f"row_id {row_id}: judge_b invalid score fields {b_bad}")
        row_complete_a = not a_missing and not a_bad
        row_complete_b = not b_missing and not b_bad
        completed_a += int(row_complete_a)
        completed_b += int(row_complete_b)

        row: dict[str, Any] = {
            field: (baseline.get(field, "") if base_template and baseline else a.get(field, ""))
            for field in VISIBLE_FIELDS
        }
        for field in JUDGE_A_FIELDS:
            row[field] = a.get(field, "")
        for field in JUDGE_B_FIELDS:
            row[field] = b.get(field, "")

        if row_id in unexpected_ids:
            row_errors.append("unexpected row_id not present in base template")

        if not row_complete_a or not row_complete_b or mismatch or row_errors:
            row["judge_agreement_status"] = "missing_or_invalid_judgment"
            row["needs_arbitration"] = True
            missing_or_invalid_count += 1
        else:
            same_relevance = a["judge_a_relevance_0_2"] == b["judge_b_relevance_0_2"]
            same_sufficiency = a["judge_a_sufficiency_0_2"] == b["judge_b_sufficiency_0_2"]
            if same_relevance and same_sufficiency:
                row["judge_agreement_status"] = "agree"
                row["needs_arbitration"] = False
                row["arbiter_final_relevance_0_2"] = a["judge_a_relevance_0_2"]
                row["arbiter_final_sufficiency_0_2"] = a["judge_a_sufficiency_0_2"]
                row["arbiter_notes"] = "auto-filled because Judge A and Judge B agreed"
                agreement_count += 1
            else:
                row["judge_agreement_status"] = "disagree"
                row["needs_arbitration"] = True
                disagreement_count += 1

        row["row_validation_errors"] = "; ".join(row_errors)
        for field in ARBITER_FIELDS:
            row.setdefault(field, "")
        merged_rows.append(row)
        if row["needs_arbitration"]:
            arbitration_rows.append(row)

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    status = "ready_for_arbitration" if arbitration_rows else "dual_judgment_complete_no_disagreements"
    if errors or missing_or_invalid_count:
        status = "not_ready_missing_or_invalid_returns"

    summary = {
        "status": status,
        "checked_at": now,
        "judge_a_csv": str(judge_a),
        "judge_b_csv": str(judge_b),
        "base_template_csv": str(base_template) if base_template else None,
        "dispatch_integrity_status": "checked_against_base_template" if base_template else "not_checked_missing_base_template",
        "expected_row_count": len(expected_ids) if base_template else None,
        "row_count": len(all_ids),
        "completed_judge_a_rows": completed_a,
        "completed_judge_b_rows": completed_b,
        "agreement_count": agreement_count,
        "disagreement_count": disagreement_count,
        "missing_or_invalid_count": missing_or_invalid_count,
        "arbitration_queue_count": len(arbitration_rows),
        "errors": errors,
        "merged_csv": str(out_dir / "semantic_support_judgment_merged.csv"),
        "arbitration_queue_csv": str(out_dir / "semantic_support_arbitration_queue.csv"),
        "truth_boundary": "This merges independent semantic-support judgments only. It is not P0 approval, production runtime validation, reviewed truth promotion, or action readiness.",
    }

    out_dir.mkdir(parents=True, exist_ok=True)
    write_csv(out_dir / "semantic_support_judgment_merged.csv", merged_rows, MERGED_FIELDS)
    write_csv(out_dir / "semantic_support_arbitration_queue.csv", arbitration_rows, MERGED_FIELDS)
    (out_dir / "semantic_support_judgment_merge_summary.json").write_text(
        json.dumps(summary, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    return summary


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--judge-a", required=True, type=Path)
    parser.add_argument("--judge-b", required=True, type=Path)
    parser.add_argument("--base-template", type=Path, help="Original dispatch template used to hard-check expected row IDs and visible fields.")
    parser.add_argument("--out-dir", type=Path, default=Path("outputs/review/source-intake-generic-readonly-loop-2026-06-14/judge-return-results"))
    args = parser.parse_args()

    summary = merge(args.judge_a, args.judge_b, args.out_dir, args.base_template)
    print(json.dumps(summary, ensure_ascii=False))
    return 0 if summary["status"] != "not_ready_missing_or_invalid_returns" else 1


if __name__ == "__main__":
    raise SystemExit(main())
