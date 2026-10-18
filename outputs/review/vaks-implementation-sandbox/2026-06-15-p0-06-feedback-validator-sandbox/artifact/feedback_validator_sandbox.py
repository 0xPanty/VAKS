#!/usr/bin/env python3
"""
Sandbox-only P0-06 feedback event validator.

This prototype checks one Markdown file with flat YAML-like frontmatter. It is
read-only and uses only the Python standard library. It does not write feedback,
approve review_due, mutate truth, modify reviewed notes, or promote anything to
mainline architecture.
"""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ALLOWED_EFFECTS = {
    "usefulness",
    "scope_fit",
    "activation_ranking",
    "review_due",
    "future_recommendation",
    "risk_calibration",
    "option_framing",
    "missing_point_candidate",
    "missing_evidence_candidate",
    "scope_mismatch_candidate",
    "implementation_note_candidate",
    "decision_follow_up_candidate",
}

FORBIDDEN_DIRECT_EFFECTS = {
    "truth_confidence",
    "truth_confidence_delta",
    "truth_score",
    "confidence_delta",
    "verification_status",
    "verification_status_delta",
    "source_reliability",
    "source_reliability_delta",
    "decision_outcome",
    "reviewed_note",
    "reviewed_note_mutation",
    "reviewed_relation",
    "reviewed_relation_strength",
    "reviewed_relation_strength_delta",
    "reviewed_relation_mutation",
}

EXPLICIT_CORRECTION_EVENTS = {
    "explicit_correction",
    "correction",
    "correction_or_retraction",
}

NEGATIVE_FEEDBACK_TYPES = {
    "irrelevant",
    "misleading",
    "wrong_scope",
    "stale",
    "missing",
    "contradicted",
    "incomplete",
    "too_weak",
    "too_broad",
}


@dataclass(frozen=True)
class Issue:
    code: str
    message: str

    def as_dict(self) -> dict[str, str]:
        return {"code": self.code, "message": self.message}


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_scalar(raw: str) -> Any:
    value = raw.strip()
    if value == "":
        return ""
    lower = value.lower()
    if lower in {"true", "yes"}:
        return True
    if lower in {"false", "no"}:
        return False
    if lower in {"null", "none"}:
        return ""
    if value.startswith("[") and value.endswith("]"):
        inner = value[1:-1].strip()
        if not inner:
            return []
        return [strip_quotes(part.strip()) for part in inner.split(",")]
    return strip_quotes(value)


def parse_frontmatter(text: str) -> dict[str, Any]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        raise ValueError("missing opening frontmatter fence")

    closing_index = None
    for index, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            closing_index = index
            break

    if closing_index is None:
        raise ValueError("missing closing frontmatter fence")

    record: dict[str, Any] = {}
    for line in lines[1:closing_index]:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if ":" not in line:
            raise ValueError(f"invalid frontmatter line: {line}")
        key, raw_value = line.split(":", 1)
        record[key.strip()] = parse_scalar(raw_value)
    return record


def norm(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return norm(value) in {"true", "yes", "1"}


def as_list(value: Any) -> list[str]:
    if value is None or value == "":
        return []
    if isinstance(value, list):
        return [norm(item) for item in value if norm(item)]
    return [norm(item) for item in str(value).split(",") if norm(item)]


def has_value(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, list):
        return any(has_value(item) for item in value)
    return str(value).strip() != ""


def field_is_set(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, list):
        return any(field_is_set(item) for item in value)
    return norm(value) not in {"", "false", "no", "0", "none", "null"}


def add_once(issues: list[Issue], code: str, message: str) -> None:
    if code not in {issue.code for issue in issues}:
        issues.append(Issue(code, message))


def nonzero_number(value: Any) -> bool:
    if value is None or value == "":
        return False
    try:
        return float(str(value).strip()) != 0.0
    except ValueError:
        return True


def is_feedback_record(record: dict[str, Any]) -> bool:
    return norm(record.get("record_kind")) in {"feedback_event", "feedback-event"} or norm(
        record.get("record_type")
    ) in {"feedback_event", "feedback-event"}


def validate_record(record: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []

    if not is_feedback_record(record):
        add_once(
            issues,
            "FB_INVALID_RECORD_KIND",
            "record_kind or record_type must be feedback_event.",
        )

    if not has_value(record.get("feedback_id")):
        add_once(issues, "FB_MISSING_FEEDBACK_ID", "feedback_id is required.")

    if not has_value(record.get("event_type")) and not has_value(
        record.get("event_kind")
    ):
        add_once(
            issues,
            "FB_MISSING_EVENT_TYPE",
            "event_type or event_kind is required.",
        )

    if issues:
        return issues

    effects = set(as_list(record.get("affects"))).union(
        set(as_list(record.get("effect_affects")))
    )
    mutations = set(as_list(record.get("direct_mutations")))
    never_affects = set(as_list(record.get("never_affects_directly")))
    feedback_type = norm(record.get("feedback_type"))
    event_type = norm(record.get("event_type") or record.get("event_kind"))
    polarity = norm(record.get("polarity"))

    direct_forbidden = effects.intersection(FORBIDDEN_DIRECT_EFFECTS) or mutations.intersection(
        FORBIDDEN_DIRECT_EFFECTS
    )
    if direct_forbidden:
        add_once(
            issues,
            "FB_FORBIDDEN_DIRECT_EFFECT",
            "feedback cannot directly affect truth, verification, source reliability, reviewed notes, or reviewed relations.",
        )

    if nonzero_number(record.get("truth_confidence_delta")) or nonzero_number(
        record.get("confidence_delta")
    ) or has_value(record.get("truth_confidence")):
        add_once(
            issues,
            "FB_TRUTH_CONFIDENCE_MUTATION",
            "feedback cannot directly modify truth confidence.",
        )

    if field_is_set(record.get("verification_status_delta")) or field_is_set(
        record.get("verification_status")
    ):
        add_once(
            issues,
            "FB_VERIFICATION_STATUS_MUTATION",
            "feedback cannot directly modify verification status.",
        )

    if nonzero_number(record.get("source_reliability_delta")) or has_value(
        record.get("source_reliability")
    ) or field_is_set(record.get("source_reliability_mutation_allowed")):
        add_once(
            issues,
            "FB_SOURCE_RELIABILITY_MUTATION",
            "feedback cannot directly modify source reliability.",
        )

    if field_is_set(record.get("reviewed_note_mutation_allowed")) or field_is_set(
        record.get("mutates_reviewed_note")
    ) or field_is_set(record.get("reviewed_note_mutation")):
        add_once(
            issues,
            "FB_REVIEWED_NOTE_MUTATION",
            "feedback cannot directly mutate reviewed notes.",
        )

    if field_is_set(record.get("mutates_reviewed_relation")) or field_is_set(
        record.get("reviewed_relation_mutation")
    ) or field_is_set(
        record.get("reviewed_relation_strength")
    ) or nonzero_number(record.get("reviewed_relation_strength_delta")):
        add_once(
            issues,
            "FB_REVIEWED_RELATION_MUTATION",
            "feedback cannot directly mutate reviewed relations or their strength.",
        )

    if event_type in EXPLICIT_CORRECTION_EVENTS and not (
        as_bool(record.get("review_due"))
        or "review_due" in effects
        or has_value(record.get("review_due_ref"))
    ):
        add_once(
            issues,
            "FB_EXPLICIT_CORRECTION_WITHOUT_REVIEW_DUE",
            "explicit correction must create or reference review_due.",
        )

    if (polarity == "negative" or feedback_type in NEGATIVE_FEEDBACK_TYPES) and not (
        as_bool(record.get("review_due"))
        or norm(record.get("review_pressure_effect")) in {"review_due", "blocked", "needs_review"}
        or "review_due" in effects
    ):
        add_once(
            issues,
            "FB_NEGATIVE_WITHOUT_REVIEW_PRESSURE",
            "negative feedback must create review pressure before truth changes.",
        )

    if field_is_set(record.get("action_basis_allowed")):
        add_once(
            issues,
            "FB_ACTION_BASIS_ALLOWED",
            "feedback records cannot be action basis.",
        )

    if has_value(record.get("warning_code")) and norm(record.get("warning_code")) != "feedback_not_truth":
        add_once(
            issues,
            "FB_MISSING_FEEDBACK_NOT_TRUTH_WARNING",
            "feedback records must keep warning_code: feedback_not_truth when warning_code is present.",
        )

    if field_is_set(record.get("global_negative_knowledge")):
        add_once(
            issues,
            "FB_GLOBAL_NEGATIVE_KNOWLEDGE_FROM_LOCAL_FEEDBACK",
            "feedback events cannot carry global negative knowledge; review artifacts own that state.",
        )

    if not has_value(record.get("project_ref")) and not has_value(
        record.get("observed_in_context")
    ):
        add_once(
            issues,
            "FB_MISSING_SCOPE_BINDING",
            "feedback event must bind to project_ref or observed_in_context.",
        )

    if field_is_set(record.get("creates_reviewed_relation")) or field_is_set(
        record.get("promotes_reviewed_knowledge")
    ):
        add_once(
            issues,
            "FB_PROMOTION_FROM_FEEDBACK",
            "feedback cannot create reviewed relation or promote knowledge directly.",
        )

    unknown_effects = effects.difference(ALLOWED_EFFECTS).difference(FORBIDDEN_DIRECT_EFFECTS)
    if unknown_effects:
        add_once(
            issues,
            "FB_UNKNOWN_EFFECT",
            "unknown feedback effect should not silently pass in this sandbox contract.",
        )

    expected_never = {"truth_confidence", "verification_status", "source_reliability"}
    if never_affects and not expected_never.issubset(never_affects):
        add_once(
            issues,
            "FB_INCOMPLETE_NEVER_AFFECTS_DIRECTLY",
            "never_affects_directly should include truth_confidence, verification_status, and source_reliability.",
        )

    return issues


def validate_path(path: Path) -> tuple[dict[str, Any] | None, list[Issue]]:
    try:
        text = path.read_text(encoding="utf-8")
        record = parse_frontmatter(text)
    except OSError as exc:
        return None, [Issue("FB_READ_ERROR", str(exc))]
    except ValueError as exc:
        return None, [Issue("FB_INVALID_FRONTMATTER", str(exc))]
    return record, validate_record(record)


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate one sandbox feedback event record."
    )
    parser.add_argument("record", help="Markdown record with flat frontmatter")
    parser.add_argument("--json", action="store_true", help="emit JSON result")
    args = parser.parse_args(argv)

    path = Path(args.record)
    record, issues = validate_path(path)
    status = "pass" if not issues else "fail"
    payload = {
        "status": status,
        "record": str(path),
        "feedback_id": "" if record is None else record.get("feedback_id", ""),
        "issues": [issue.as_dict() for issue in issues],
    }

    if args.json:
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif not issues:
        print(f"PASS feedback_event {path}")
    else:
        print(f"FAIL feedback_event {path}")
        for issue in issues:
            print(f"{issue.code}: {issue.message}")

    return 0 if not issues else 1


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
