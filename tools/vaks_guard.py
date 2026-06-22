#!/usr/bin/env python3
"""VAKS Guard read-only lazy-gate checks.

This tool wraps the seven sandbox-proven guard families into one stdlib-only
runtime checker. It is diagnostic only: a pass is not reviewer approval,
reviewed knowledge, evidence support, action basis, promotion, or write
permission.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Iterable


TOOL_NAME = "vaks_guard"
VERSION = "0.1.0"

STATUS_PASS = "pass"
STATUS_WARN = "warn"
STATUS_BLOCK = "block"
RUN_EXECUTED = "executed"
RUN_SKIPPED = "skipped"
RUN_ERROR = "error"

AUTHORITY_BOUNDARY = (
    "VAKS Guard is a read-only lazy gate. It identifies machine-detectable "
    "contract violations only. It does not create reviewed knowledge, evidence "
    "support, action approval, reviewer approval, promotion, mainline readiness, "
    "or write authorization."
)

NOT_CHECKED_BY_GUARD = [
    "semantic truth of any claim",
    "whether an evidence span actually supports a claim beyond contract checks",
    "reviewer approval",
    "owner risk acceptance",
    "permission to execute an operation",
    "mainline promotion or merge readiness",
]


@dataclass(frozen=True)
class Issue:
    code: str
    message: str
    item_id: str = ""

    def as_dict(self) -> dict[str, str]:
        result = {"code": self.code, "message": self.message}
        if self.item_id:
            result["item_id"] = self.item_id
        return result


@dataclass(frozen=True)
class GuardResult:
    guard: str
    path: str
    status: str
    code: str
    message: str
    next_step: str
    authority_boundary: str = AUTHORITY_BOUNDARY
    details: dict[str, Any] | None = None

    def as_dict(self) -> dict[str, Any]:
        data = {
            "guard": self.guard,
            "status": self.status,
            "code": self.code,
            "message": self.message,
            "location": self.path,
            "rule_ref": self.guard,
            "next_step": self.next_step,
        }
        if self.details:
            data["details"] = self.details
        return data


def strip_quotes(value: str) -> str:
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        return value[1:-1]
    return value


def parse_scalar_flat(raw: str) -> Any:
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


def parse_scalar_nested(value: str) -> Any:
    value = value.strip()
    if value == "":
        return None
    if value.lower() == "true":
        return True
    if value.lower() == "false":
        return False
    return strip_quotes(value)


def duplicate_key_error(key: str) -> ValueError:
    return ValueError(f"duplicate key is not allowed: {key}")


def normalize_frontmatter_key(raw_key: str) -> str:
    key = raw_key.strip()
    if not key:
        raise ValueError("empty frontmatter key is not allowed")
    if "\t" in key:
        raise ValueError(f"tab is not allowed in frontmatter key: {raw_key}")
    if key[0] in {"'", '"'} or key[-1] in {"'", '"'}:
        if len(key) < 2 or key[0] != key[-1] or key[0] not in {"'", '"'}:
            raise ValueError(f"unsupported quoted frontmatter key: {raw_key}")
        key = key[1:-1].strip()
        if not key:
            raise ValueError("empty quoted frontmatter key is not allowed")
    if "'" in key or '"' in key:
        raise ValueError(f"quote is not allowed inside frontmatter key: {raw_key}")
    return key


def ensure_no_tab_indentation(raw_line: str) -> None:
    indentation = raw_line[: len(raw_line) - len(raw_line.lstrip(" \t"))]
    if "\t" in indentation:
        raise ValueError(f"tab indentation is not supported: {raw_line}")


def split_frontmatter(text: str) -> tuple[list[str], str] | None:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            return lines[1:index], "\n".join(lines[index + 1 :])
    return None


def parse_frontmatter_flat(text: str, strict: bool = True) -> dict[str, Any]:
    split = split_frontmatter(text)
    if split is None:
        if strict:
            raise ValueError("missing frontmatter fence")
        return {}
    fm_lines, _body = split
    record: dict[str, Any] = {}
    for line in fm_lines:
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        ensure_no_tab_indentation(line)
        if ":" not in line:
            if strict:
                raise ValueError(f"invalid frontmatter line: {line}")
            continue
        key, raw_value = line.split(":", 1)
        key = normalize_frontmatter_key(key)
        if key in record:
            raise duplicate_key_error(key)
        record[key] = parse_scalar_flat(raw_value)
    return record


def parse_frontmatter_nested(text: str) -> tuple[dict[str, Any], str]:
    split = split_frontmatter(text)
    if split is None:
        return {}, text
    fm_lines, body = split
    data: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(-1, data)]
    for raw_line in fm_lines:
        if not raw_line.strip() or raw_line.lstrip().startswith("#"):
            continue
        ensure_no_tab_indentation(raw_line)
        if ":" not in raw_line:
            raise ValueError(f"invalid frontmatter line: {raw_line}")
        indent = len(raw_line) - len(raw_line.lstrip(" "))
        key, raw_value = raw_line.strip().split(":", 1)
        key = normalize_frontmatter_key(key)
        while stack and indent <= stack[-1][0]:
            stack.pop()
        current = stack[-1][1]
        if key in current:
            raise duplicate_key_error(key)
        if raw_value.strip() == "":
            child: dict[str, Any] = {}
            current[key] = child
            stack.append((indent, child))
        else:
            current[key] = parse_scalar_nested(raw_value)
    return data, body


def reject_duplicate_json_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    result: dict[str, Any] = {}
    for key, value in pairs:
        if key in result:
            raise duplicate_key_error(key)
        result[key] = value
    return result


def load_json_text_strict(text: str) -> Any:
    return json.loads(text, object_pairs_hook=reject_duplicate_json_object)


def load_json_file_strict(path: Path) -> Any:
    return load_json_text_strict(path.read_text(encoding="utf-8"))


def norm(value: Any) -> str:
    if value is None:
        return ""
    if isinstance(value, bool):
        return "true" if value else "false"
    return str(value).strip().lower().replace(" ", "_").replace("-", "_")


def norm_pathish(value: Any) -> str:
    return norm(value).replace("\\", "/")


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
    if isinstance(value, dict):
        return any(has_value(item) for item in value.values())
    return str(value).strip() != ""


def field_is_set(value: Any) -> bool:
    if value is None:
        return False
    if isinstance(value, bool):
        return value
    if isinstance(value, list):
        return any(field_is_set(item) for item in value)
    return norm(value) not in {"", "false", "no", "0", "none", "null"}


def nonzero_number(value: Any) -> bool:
    if value is None or value == "":
        return False
    try:
        return float(str(value).strip()) != 0.0
    except ValueError:
        return True


def add_once(issues: list[Issue], code: str, message: str, item_id: str = "") -> None:
    key = (code, item_id)
    if key not in {(issue.code, issue.item_id) for issue in issues}:
        issues.append(Issue(code, message, item_id))


def next_step_for(code: str) -> str:
    if code == "ok":
        return "No guard action needed."
    if code in {"no_applicable_records", "no_applicable_input"}:
        return "Run VAKS Guard only when matching VAKS records exist for the selected mode."
    if code == "missing_required_input":
        return "Provide an existing file or directory before running this guard."
    if code == "missing_mode_or_guard":
        return "Choose an explicit lazy-gate mode, or use --guard only for parity/self-test checks."
    if code == "mode_guard_conflict":
        return "Use either --mode or --guard, not both; --guard is only for direct parity/self-test checks."
    if code == "tool_runtime_error":
        return "Treat this as a tool failure, inspect the input, and rerun after repair."
    if "frontmatter" in code.lower() or "parse" in code.lower() or "decode" in code.lower():
        return "Repair the input encoding and frontmatter/JSON structure before rerunning the guard."
    if code == "body_hash_not_required_for_draft":
        return "No action needed for draft records; add body_hash before fixed review or writeback use."
    if "hash" in code.lower() or "body_changed" in code.lower():
        return "Recompute the current body hash and rerun review or restore the reviewed body."
    if "support" in code.lower() or "anchor" in code.lower():
        return "Attach a specific raw/source anchor or evidence packet before claiming support."
    if code.startswith("AR_"):
        return "Keep action not-ready until evidence, scope, risk, intent, and approval requirements are satisfied."
    if code.startswith("FB_"):
        return "Route feedback to activation, review pressure, or review_due without mutating truth."
    if code.startswith(("RV_", "OV_")):
        return "Fix the receipt fields and keep receipt authority strictly process-only."
    if code.startswith("RA_"):
        return "Exclude runtime artifacts from retrieval/context/action use; do not delete files from this check."
    if code.startswith("MATRIX_"):
        return "Repair the failure matrix shape, coverage, and authority non-claim flags."
    return "Review the VAKS boundary for this code and repair the record before reuse."


def results_from_issues(
    guard: str,
    path: Path,
    issues: list[Issue],
    *,
    pass_message: str,
    warnings: Iterable[str] = (),
    details: dict[str, Any] | None = None,
) -> list[GuardResult]:
    if issues:
        grouped: dict[str, dict[str, Any]] = {}
        for issue in issues:
            entry = grouped.setdefault(
                issue.code,
                {"message": issue.message, "item_ids": []},
            )
            if issue.item_id:
                entry["item_ids"].append(issue.item_id)
        results: list[GuardResult] = []
        for code, entry in grouped.items():
            issue_details = dict(details or {})
            if entry["item_ids"]:
                issue_details["item_ids"] = sorted(set(entry["item_ids"]))
            results.append(
                GuardResult(
                    guard=guard,
                    path=str(path),
                    status=STATUS_BLOCK,
                    code=code,
                    message=entry["message"],
                    next_step=next_step_for(code),
                    details=issue_details or None,
                )
            )
        return results
    warning_list = list(warnings)
    if warning_list:
        return [
            GuardResult(
                guard=guard,
                path=str(path),
                status=STATUS_WARN,
                code=warning,
                message=warning.replace("_", " "),
                next_step=next_step_for(warning),
                details=details,
            )
            for warning in warning_list
        ]
    return [
        GuardResult(
            guard=guard,
            path=str(path),
            status=STATUS_PASS,
            code="ok",
            message=pass_message,
            next_step=next_step_for("ok"),
            details=details,
        )
    ]


# P0-03 body hash guard -----------------------------------------------------

VALID_STATUS_REQUIRING_HASH = {"fixed", "approved", "writeback_ready"}
VALID_REVIEW_OBJECT_STATES_REQUIRING_HASH = {
    "fixed_for_review",
    "revised_after_review",
    "approved",
    "writeback_ready",
}


def canonical_body(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = text.split("\n")
    while lines and lines[0].strip() == "":
        lines.pop(0)
    if lines and lines[0].lstrip().startswith("#"):
        lines = lines[1:]
    return "\n".join(lines).strip()


def sha256_body(text: str) -> str:
    return hashlib.sha256(canonical_body(text).encode("utf-8")).hexdigest()


def heading_level(line: str) -> int | None:
    stripped = line.lstrip()
    if not stripped.startswith("#"):
        return None
    count = 0
    for char in stripped:
        if char == "#":
            count += 1
        else:
            break
    if count and len(stripped) > count and stripped[count] == " ":
        return count
    return None


def normalize_heading_selector(selector: str) -> str:
    return selector.strip().lstrip("#").strip().lower()


def extract_markdown_section(text: str, selector: str) -> str | None:
    wanted = normalize_heading_selector(selector)
    lines = text.replace("\r\n", "\n").replace("\r", "\n").split("\n")
    start = None
    start_level = None
    for index, line in enumerate(lines):
        level = heading_level(line)
        if level is None:
            continue
        heading_text = line.lstrip()[level:].strip()
        if heading_text.lower() == wanted:
            start = index
            start_level = level
            break
    if start is None or start_level is None:
        return None
    end = len(lines)
    for index in range(start + 1, len(lines)):
        level = heading_level(lines[index])
        if level is not None and level <= start_level:
            end = index
            break
    return "\n".join(lines[start:end])


def split_location(body_location: str) -> tuple[str, str | None]:
    if body_location.startswith("#"):
        return "", body_location
    if "#" in body_location:
        path_part, heading_part = body_location.split("#", 1)
        return path_part, "#" + heading_part
    return body_location, None


def resolve_body_path(record_path: Path, path_location: str) -> Path:
    raw = Path(path_location)
    if raw.is_absolute():
        return raw
    return (record_path.parent / raw).resolve()


def path_is_inside(child: Path, parent: Path) -> bool:
    try:
        child.resolve().relative_to(parent.resolve())
        return True
    except ValueError:
        return False


def resolve_body_text(
    record_path: Path, record_body: str, body_location: Any
) -> tuple[str | None, str | None, str | None]:
    if not isinstance(body_location, str) or not body_location.strip():
        return None, None, "missing_candidate_body_location"
    path_part, section_selector = split_location(body_location.strip())
    if path_part:
        body_path = resolve_body_path(record_path, path_part)
        if not path_is_inside(body_path, record_path.parent):
            return str(body_path), None, "candidate_body_location_outside_record_dir"
        try:
            body_text = body_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            return str(body_path), None, "candidate_body_location_not_found"
        except UnicodeDecodeError:
            return str(body_path), None, "candidate_body_location_decode_error"
        except OSError:
            return str(body_path), None, "candidate_body_location_read_error"
    else:
        body_path = record_path
        body_text = record_body
    if section_selector:
        section = extract_markdown_section(body_text, section_selector)
        if section is None:
            return str(body_path) + section_selector, None, "candidate_body_section_not_found"
        return str(body_path) + section_selector, section, None
    return str(body_path), body_text, None


def validate_body_hash(path: Path) -> list[GuardResult]:
    try:
        text = path.read_text(encoding="utf-8")
        frontmatter, record_body = parse_frontmatter_nested(text)
    except UnicodeDecodeError as exc:
        return results_from_issues(
            "body_hash",
            path,
            [Issue("BH_DECODE_ERROR", str(exc))],
            pass_message="Body hash boundary passed.",
        )
    except OSError as exc:
        return results_from_issues(
            "body_hash",
            path,
            [Issue("BH_READ_ERROR", str(exc))],
            pass_message="Body hash boundary passed.",
        )
    except ValueError as exc:
        return results_from_issues(
            "body_hash",
            path,
            [Issue("BH_INVALID_FRONTMATTER", str(exc))],
            pass_message="Body hash boundary passed.",
        )
    body_ref, body_text, body_error = resolve_body_text(
        path, record_body, frontmatter.get("candidate_body_location")
    )
    issues: list[Issue] = []
    warnings: list[str] = []

    review_status = str(frontmatter.get("review_status") or "draft")
    review_object_state = str(frontmatter.get("review_object_state") or "")
    writeback_ready = bool(frontmatter.get("writeback_ready"))
    body_hash = frontmatter.get("body_hash")
    approval = frontmatter.get("approval_integrity")
    checked_body_hash = approval.get("checked_body_hash") if isinstance(approval, dict) else None

    requires_hash = (
        writeback_ready
        or review_status in VALID_STATUS_REQUIRING_HASH
        or review_object_state in VALID_REVIEW_OBJECT_STATES_REQUIRING_HASH
    )
    if requires_hash and not body_hash:
        add_once(
            issues,
            "fixed_or_approved_missing_body_hash",
            "fixed, approved, or writeback-ready candidate is missing body_hash.",
        )

    computed_hash = None
    if body_error:
        add_once(issues, body_error, body_error.replace("_", " "))
    else:
        computed_hash = sha256_body(body_text or "")

    if computed_hash and body_hash and str(body_hash) != computed_hash:
        if writeback_ready:
            add_once(
                issues,
                "writeback_ready_body_changed",
                "writeback-ready body no longer matches recorded body_hash.",
            )
        else:
            add_once(
                issues,
                "body_hash_mismatch",
                "candidate body no longer matches recorded body_hash.",
            )

    if computed_hash and checked_body_hash and str(checked_body_hash) != computed_hash:
        add_once(
            issues,
            "checked_body_hash_mismatch",
            "approval_integrity.checked_body_hash does not match current body.",
        )

    if not requires_hash and not body_hash:
        warnings.append("body_hash_not_required_for_draft")

    return results_from_issues(
        "body_hash",
        path,
        issues,
        pass_message="Body hash boundary passed.",
        warnings=warnings,
        details={"candidate_body_location": body_ref, "computed_body_hash": computed_hash},
    )


# P0-04 support boundary guard --------------------------------------------

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


def validate_support_boundary(path: Path) -> list[GuardResult]:
    try:
        data, _body = parse_frontmatter_nested(path.read_text(encoding="utf-8"))
    except UnicodeDecodeError as exc:
        return results_from_issues(
            "support_boundary",
            path,
            [Issue("SB_DECODE_ERROR", str(exc))],
            pass_message="Support boundary passed.",
        )
    except OSError as exc:
        return results_from_issues(
            "support_boundary",
            path,
            [Issue("SB_READ_ERROR", str(exc))],
            pass_message="Support boundary passed.",
        )
    except ValueError as exc:
        return results_from_issues(
            "support_boundary",
            path,
            [Issue("SB_INVALID_FRONTMATTER", str(exc))],
            pass_message="Support boundary passed.",
        )
    support_claimed = truthy(data, "support_claimed") or data.get("pack_role") == "support"
    evidence_role = data.get("evidence_role")
    record_kind = data.get("proposed_support_record_kind")
    bucket = data.get("proposed_support_authority_bucket")
    target_ref = data.get("target_ref")
    support_ref = data.get("proposed_support_ref")
    issues: list[Issue] = []

    if support_claimed and (bucket in CANDIDATE_BUCKETS or record_kind in CANDIDATE_RECORD_KINDS):
        add_once(issues, "candidate_as_support", "candidate or overlay material cannot be support.")
    if support_claimed and evidence_role == "direct_support" and truthy(data, "url_only"):
        add_once(issues, "url_only_direct_support", "URL-only citation cannot be direct support.")
    if support_claimed and any(truthy(data, key) for key in RANK_FIELDS):
        add_once(
            issues,
            "rank_or_score_as_support_or_trust",
            "rank, score, graph rank, or retrieval rank cannot be support or trust.",
        )
    if support_claimed and (
        bucket == "feedback"
        or record_kind in FEEDBACK_RECORD_KINDS
        or truthy(data, "feedback_used_as_support")
    ):
        add_once(issues, "feedback_as_support", "feedback cannot be evidence support.")
    if support_claimed and record_kind in SOURCE_SUMMARY_KINDS and truthy(
        data, "source_summary_self_support"
    ):
        add_once(
            issues,
            "source_summary_self_support",
            "source summary cannot support its own extracted claim without an independent anchor.",
        )
    if support_claimed and (
        target_ref == support_ref
        or record_kind in CLAIM_NOTE_KINDS
        and truthy(data, "claim_note_self_support")
    ):
        add_once(
            issues,
            "claim_note_self_support_loop",
            "claim note cannot support itself.",
        )
    if support_claimed and (
        record_kind in LEGACY_METADATA_KINDS
        or truthy(data, "legacy_raw_metadata_used_as_support")
    ):
        add_once(
            issues,
            "legacy_metadata_support",
            "legacy metadata cannot be evidence support.",
        )
    if support_claimed and evidence_role == "background_context":
        add_once(
            issues,
            "background_context_counted_as_support",
            "background context cannot be counted as support.",
        )
    if (
        not issues
        and support_claimed
        and evidence_role in {"direct_support", "inferential_support"}
        and not has_current_anchor(data)
    ):
        add_once(
            issues,
            "support_claim_missing_independent_anchor",
            "support claim requires an independent current anchor.",
        )
    if (
        not issues
        and support_claimed
        and evidence_role == "inferential_support"
        and not data.get("reviewer_note")
    ):
        add_once(
            issues,
            "inferential_support_missing_reviewer_note",
            "inferential support requires reviewer_note.",
        )

    return results_from_issues(
        "support_boundary",
        path,
        issues,
        pass_message="Support boundary passed.",
    )


# P0-05 action readiness guard --------------------------------------------

READY_STATE = "ready"

BAD_BASIS_CODES = {
    "candidate": "AR_CANDIDATE_BASIS_READY",
    "candidate_distillation": "AR_CANDIDATE_BASIS_READY",
    "candidate_point": "AR_CANDIDATE_BASIS_READY",
    "project_overlay": "AR_CANDIDATE_BASIS_READY",
    "feedback": "AR_FEEDBACK_BASIS_READY",
    "feedback_event": "AR_FEEDBACK_BASIS_READY",
    "retrieval_rank": "AR_RETRIEVAL_RANK_BASIS_READY",
    "retrieval_score": "AR_RETRIEVAL_RANK_BASIS_READY",
    "graph_rank": "AR_RETRIEVAL_RANK_BASIS_READY",
    "source_summary": "AR_SOURCE_SUMMARY_BASIS_READY",
    "briefing_summary": "AR_SOURCE_SUMMARY_BASIS_READY",
}

DIAGNOSTIC_BASIS = {
    "validator_pass",
    "test_pass",
    "lint_pass",
    "blind_review",
    "llm_judge",
    "operation_receipt",
}

POSITIVE_ACTION_BASIS = {"reviewed_support", "evidence_packet"}
SIGNIFICANT_ACTION_MODES = {
    "decision",
    "implementation",
    "propose_write",
    "write",
    "delete",
    "schema_change",
    "deploy",
}
WRITE_OPERATION_MODES = {"write", "delete", "schema_change"}


def ar_is_ready(record: dict[str, Any]) -> bool:
    return norm(record.get("action_readiness")) == READY_STATE or as_bool(
        record.get("action_basis_ready_claimed")
    )


def ar_is_significant_action(record: dict[str, Any]) -> bool:
    action_mode = norm(record.get("action_mode"))
    operation_mode = norm(record.get("operation_mode"))
    return (
        as_bool(record.get("significant_action"))
        or action_mode in SIGNIFICANT_ACTION_MODES
        or operation_mode in SIGNIFICANT_ACTION_MODES
    )


def validate_action_record(record: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if norm(record.get("record_kind")) != "action_readiness_check":
        add_once(
            issues,
            "AR_INVALID_RECORD_KIND",
            "record_kind must be action_readiness_check.",
        )
    if not has_value(record.get("action_id")):
        add_once(issues, "AR_MISSING_ACTION_ID", "action_id is required.")
    if not has_value(record.get("action_readiness")):
        add_once(
            issues,
            "AR_MISSING_ACTION_READINESS",
            "action_readiness is required.",
        )
    if issues:
        return issues
    if not ar_is_ready(record):
        return issues

    evidence_sufficiency = norm(record.get("evidence_sufficiency"))
    temporal_applicability = norm(record.get("temporal_applicability"))
    evidence_support_status = norm(record.get("evidence_support_status"))
    basis_materials = set(as_list(record.get("basis_materials")))

    if evidence_sufficiency == "insufficient":
        add_once(
            issues,
            "AR_INSUFFICIENT_EVIDENCE_READY",
            "insufficient evidence_sufficiency cannot produce ready action basis.",
        )
    if evidence_sufficiency == "out_of_scope":
        add_once(
            issues,
            "AR_OUT_OF_SCOPE_READY",
            "out_of_scope evidence_sufficiency cannot produce ready action basis.",
        )
    if evidence_sufficiency == "risky" or as_bool(record.get("unresolved_risk")):
        add_once(
            issues,
            "AR_UNRESOLVED_RISK_READY",
            "unresolved or risky evidence cannot be action_readiness ready.",
        )
    if evidence_sufficiency != "sufficient":
        add_once(
            issues,
            "AR_EVIDENCE_SUFFICIENCY_NOT_SUFFICIENT",
            "ready action basis requires explicit evidence_sufficiency: sufficient.",
        )
    if evidence_support_status in {
        "unsupported",
        "unclear",
        "missing_anchor",
        "not_checked",
        "self_support_loop",
    }:
        add_once(
            issues,
            "AR_SUPPORT_NOT_SUPPORTED_READY",
            "ready action basis requires supported current evidence, not weak support.",
        )
    if temporal_applicability in {"stale", "superseded", "out_of_scope"}:
        if not (
            has_value(record.get("replacement_basis_ref"))
            or has_value(record.get("narrowed_scope_ref"))
        ):
            add_once(
                issues,
                "AR_STALE_SUPERSEDED_WITHOUT_REPLACEMENT_READY",
                "stale, superseded, or out_of_scope basis needs replacement or narrowed scope before ready.",
            )
    if as_bool(record.get("warnings_or_gaps_trimmed")) or as_bool(
        record.get("missing_evidence_trimmed")
    ):
        add_once(
            issues,
            "AR_HIDDEN_WARNING_OR_GAP_READY",
            "known warning, gap, or missing evidence was hidden by trimming.",
        )
    if ar_is_significant_action(record) and not as_bool(record.get("intent_confirmed")):
        add_once(
            issues,
            "AR_MISSING_INTENT_CONFIRMATION",
            "significant action requires explicit intent confirmation before ready.",
        )
    if ar_is_significant_action(record) and not as_bool(
        record.get("success_criteria_present")
    ):
        add_once(
            issues,
            "AR_MISSING_SUCCESS_CRITERIA",
            "significant action basis needs visible success criteria.",
        )
    for material in sorted(basis_materials):
        if material in BAD_BASIS_CODES:
            code = BAD_BASIS_CODES[material]
            add_once(
                issues,
                code,
                f"{material} can orient review but cannot be action basis.",
            )
    has_positive_basis = bool(basis_materials.intersection(POSITIVE_ACTION_BASIS)) or any(
        has_value(record.get(field))
        for field in ("action_basis_ref", "reviewed_support_refs", "evidence_packet_ref")
    )
    if not has_positive_basis:
        add_once(
            issues,
            "AR_MISSING_REVIEWED_ACTION_BASIS",
            "ready action basis requires reviewed support or an evidence packet reference.",
        )
    if "context_pack" in basis_materials and not (
        "reviewed_support" in basis_materials or "evidence_packet" in basis_materials
    ):
        add_once(
            issues,
            "AR_CONTEXT_PACK_ONLY_READY",
            "context pack alone is not ready action basis.",
        )
    if basis_materials.intersection(DIAGNOSTIC_BASIS):
        add_once(
            issues,
            "AR_DIAGNOSTIC_BASIS_READY",
            "diagnostic, receipt, or judge output cannot substitute for action basis.",
        )
    reviewed_write = as_bool(record.get("reviewed_write")) or norm(
        record.get("target_bucket")
    ) in {"reviewed", "reviewed_knowledge", "decision"}
    if reviewed_write and not as_bool(record.get("approved")):
        add_once(
            issues,
            "AR_REVIEWED_WRITE_MISSING_APPROVAL",
            "reviewed write needs explicit approval before ready.",
        )
    if reviewed_write and not as_bool(record.get("checked_body_hash_present")):
        add_once(
            issues,
            "AR_REVIEWED_WRITE_MISSING_CHECKED_BODY_HASH",
            "reviewed write needs checked body hash before ready.",
        )
    operation_mode = norm(record.get("operation_mode"))
    action_mode = norm(record.get("action_mode"))
    destructive = (
        operation_mode in {"delete", "schema_change"}
        or action_mode in {"delete", "schema_change"}
        or as_bool(record.get("rollback_required"))
    )
    if destructive and not as_bool(record.get("rollback_plan_present")):
        add_once(
            issues,
            "AR_DESTRUCTIVE_MISSING_ROLLBACK",
            "destructive or hard-to-rollback action needs a rollback plan.",
        )
    actor_tier = norm(record.get("actor_tier"))
    if actor_tier in {"read_only", "readonly", "suggest_only"} and (
        operation_mode in WRITE_OPERATION_MODES or action_mode in WRITE_OPERATION_MODES
    ):
        add_once(
            issues,
            "AR_READ_ONLY_ACTOR_WRITE",
            "read-only or suggest-only actor cannot perform write operations.",
        )
    if (operation_mode == "schema_change" or action_mode == "schema_change") and not as_bool(
        record.get("owner_final")
    ):
        add_once(
            issues,
            "AR_SCHEMA_CHANGE_MISSING_OWNER_FINAL",
            "schema change needs owner_final before ready.",
        )
    return issues


def validate_action_readiness(path: Path) -> list[GuardResult]:
    try:
        record = parse_frontmatter_flat(path.read_text(encoding="utf-8"))
        issues = validate_action_record(record)
    except OSError as exc:
        issues = [Issue("AR_READ_ERROR", str(exc))]
    except ValueError as exc:
        issues = [Issue("AR_INVALID_FRONTMATTER", str(exc))]
    return results_from_issues(
        "action_readiness",
        path,
        issues,
        pass_message="Action readiness boundary passed.",
    )


# P0-06 feedback guard ------------------------------------------------------

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

EXPLICIT_CORRECTION_EVENTS = {"explicit_correction", "correction", "correction_or_retraction"}
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


def is_feedback_record(record: dict[str, Any]) -> bool:
    return norm(record.get("record_kind")) in {"feedback_event", "feedback-event"} or norm(
        record.get("record_type")
    ) in {"feedback_event", "feedback-event"}


def validate_feedback_record(record: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not is_feedback_record(record):
        add_once(
            issues,
            "FB_INVALID_RECORD_KIND",
            "record_kind or record_type must be feedback_event.",
        )
    if not has_value(record.get("feedback_id")):
        add_once(issues, "FB_MISSING_FEEDBACK_ID", "feedback_id is required.")
    if not has_value(record.get("event_type")) and not has_value(record.get("event_kind")):
        add_once(
            issues,
            "FB_MISSING_EVENT_TYPE",
            "event_type or event_kind is required.",
        )
    if issues:
        return issues

    effects = set(as_list(record.get("affects"))).union(set(as_list(record.get("effect_affects"))))
    mutations = set(as_list(record.get("direct_mutations")))
    never_affects = set(as_list(record.get("never_affects_directly")))
    feedback_type = norm(record.get("feedback_type"))
    event_type = norm(record.get("event_type") or record.get("event_kind"))
    polarity = norm(record.get("polarity"))

    if effects.intersection(FORBIDDEN_DIRECT_EFFECTS) or mutations.intersection(
        FORBIDDEN_DIRECT_EFFECTS
    ):
        add_once(
            issues,
            "FB_FORBIDDEN_DIRECT_EFFECT",
            "feedback cannot directly affect truth, verification, source reliability, reviewed notes, or reviewed relations.",
        )
    if (
        nonzero_number(record.get("truth_confidence_delta"))
        or nonzero_number(record.get("confidence_delta"))
        or has_value(record.get("truth_confidence"))
    ):
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
    if (
        nonzero_number(record.get("source_reliability_delta"))
        or has_value(record.get("source_reliability"))
        or field_is_set(record.get("source_reliability_mutation_allowed"))
    ):
        add_once(
            issues,
            "FB_SOURCE_RELIABILITY_MUTATION",
            "feedback cannot directly modify source reliability.",
        )
    if (
        field_is_set(record.get("reviewed_note_mutation_allowed"))
        or field_is_set(record.get("mutates_reviewed_note"))
        or field_is_set(record.get("reviewed_note_mutation"))
    ):
        add_once(
            issues,
            "FB_REVIEWED_NOTE_MUTATION",
            "feedback cannot directly mutate reviewed notes.",
        )
    if (
        field_is_set(record.get("mutates_reviewed_relation"))
        or field_is_set(record.get("reviewed_relation_mutation"))
        or field_is_set(record.get("reviewed_relation_strength"))
        or nonzero_number(record.get("reviewed_relation_strength_delta"))
    ):
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
    if not has_value(record.get("project_ref")) and not has_value(record.get("observed_in_context")):
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
            "unknown feedback effect should not silently pass in this contract.",
        )
    expected_never = {"truth_confidence", "verification_status", "source_reliability"}
    if never_affects and not expected_never.issubset(never_affects):
        add_once(
            issues,
            "FB_INCOMPLETE_NEVER_AFFECTS_DIRECTLY",
            "never_affects_directly should include truth_confidence, verification_status, and source_reliability.",
        )
    return issues


def validate_feedback(path: Path) -> list[GuardResult]:
    try:
        record = parse_frontmatter_flat(path.read_text(encoding="utf-8"))
        issues = validate_feedback_record(record)
    except OSError as exc:
        issues = [Issue("FB_READ_ERROR", str(exc))]
    except ValueError as exc:
        issues = [Issue("FB_INVALID_FRONTMATTER", str(exc))]
    return results_from_issues(
        "feedback",
        path,
        issues,
        pass_message="Feedback boundary passed.",
    )


# P1-08 receipt guard -------------------------------------------------------

RETRIEVAL_FORBIDDEN_SUPPORT_BUCKETS = {
    "candidate",
    "candidate_distillation",
    "candidate_point",
    "project_overlay",
    "source_annotation",
    "feedback",
    "feedback_event",
}
RETRIEVAL_AUTHORITY_BUCKETS = {
    "reviewed",
    "raw_anchor",
    "candidate",
    "candidate_distillation",
    "candidate_point",
    "project_overlay",
    "source_annotation",
    "feedback",
    "feedback_event",
}
RETRIEVAL_REQUEST_BUCKETS = RETRIEVAL_AUTHORITY_BUCKETS.union({"mixed_for_orientation"})
RETRIEVAL_PACK_ROLES = {
    "orientation",
    "review_input",
    "support",
    "anchor",
    "counterexample",
    "background_context",
}
OPERATION_ACTOR_TIERS = {
    "read_only",
    "suggest_only",
    "candidate_write",
    "reviewed_write",
    "owner_final",
}
OPERATION_MODES = {"read", "suggest", "propose_write", "write", "delete", "schema_change"}
OPERATION_TARGET_SCOPES = {
    "candidate",
    "sandbox",
    "reviewed",
    "mainline",
    "formal",
    "schema",
    "protected",
}
BAD_OPERATION_BASIS_MATERIALS = {
    "candidate",
    "candidate_distillation",
    "candidate_point",
    "project_overlay",
    "source_annotation",
    "feedback",
    "feedback_event",
    "retrieval_receipt",
    "retrieval_rank",
    "retrieval_score",
    "graph_rank",
    "source_summary",
    "briefing_summary",
    "context_pack",
}
AUTHORITY_CLAIMS = {
    "truth",
    "truth_confidence",
    "reviewed_truth",
    "reviewed_knowledge",
    "reviewed_relation",
    "review_approval",
    "reviewer_approval",
    "evidence_support",
    "direct_support",
    "action_basis",
    "action_readiness",
    "mainline_ready",
    "promotion_ready",
    "owner_approval",
}
RETRIEVAL_BOUNDARY_FLAGS = {
    "selected_by_is_not_support",
    "same_bucket_rrf_only",
    "cross_bucket_rank_not_authority",
    "legacy_raw_metadata_excluded",
    "candidate_overlay_feedback_not_support",
    "url_only_not_direct_support",
    "graph_rank_not_trust",
    "receipt_not_review_approval",
    "receipt_not_action_basis",
    "receipt_not_reviewed_knowledge",
}
OPERATION_BOUNDARY_FLAGS = {
    "receipt_not_truth",
    "receipt_not_review_approval",
    "receipt_not_reviewed_knowledge",
    "receipt_not_action_basis",
    "validator_pass_not_reviewer_approval",
    "sandbox_not_mainline",
}
WRITE_MODES = {"write", "delete", "schema_change"}
SIGNIFICANT_OPERATION_MODES = {"propose_write", "write", "delete", "schema_change"}


def add_missing(issues: list[Issue], field: str) -> None:
    add_once(issues, "RV_OV_MISSING_REQUIRED_FIELD", f"missing required field: {field}.")


def receipt_claims_authority(record: dict[str, Any]) -> bool:
    explicit_claims = set(as_list(record.get("receipt_claims"))).union(
        set(as_list(record.get("operation_claims")))
    )
    if explicit_claims.intersection(AUTHORITY_CLAIMS):
        return True
    for claim in AUTHORITY_CLAIMS:
        if as_bool(record.get(f"claims_{claim}")):
            return True
        if as_bool(record.get(f"receipt_claims_{claim}")):
            return True
        if as_bool(record.get(f"operation_claims_{claim}")):
            return True
    return False


def validate_boundary_flags(
    record: dict[str, Any], expected_flags: set[str], issue_code: str, issues: list[Issue]
) -> None:
    for flag in sorted(expected_flags):
        if flag in record and not as_bool(record.get(flag)):
            add_once(issues, issue_code, f"boundary flag must remain true: {flag}.")


def validate_retrieval_receipt(record: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not has_value(record.get("receipt_id")) and not has_value(record.get("query_id")):
        add_missing(issues, "receipt_id or query_id")
    for field in (
        "query_mode",
        "requested_authority_bucket",
        "included_buckets",
        "rrf_scope",
        "selected_item_authority_buckets",
        "selected_item_pack_roles",
    ):
        if not has_value(record.get(field)):
            add_missing(issues, field)
    if issues:
        return issues

    requested_bucket = norm(record.get("requested_authority_bucket"))
    if requested_bucket not in RETRIEVAL_REQUEST_BUCKETS:
        add_once(
            issues,
            "RV_UNKNOWN_AUTHORITY_BUCKET",
            "requested_authority_bucket must be a known receipt bucket.",
        )
    included_buckets = set(as_list(record.get("included_buckets")))
    selected_buckets = set(as_list(record.get("selected_item_authority_buckets")))
    unknown_buckets = sorted(
        included_buckets.union(selected_buckets).difference(RETRIEVAL_AUTHORITY_BUCKETS)
    )
    if unknown_buckets:
        add_once(
            issues,
            "RV_UNKNOWN_AUTHORITY_BUCKET",
            f"unknown authority bucket(s): {unknown_buckets}.",
        )
    roles = set(as_list(record.get("selected_item_pack_roles")))
    unknown_roles = sorted(roles.difference(RETRIEVAL_PACK_ROLES))
    if unknown_roles:
        add_once(
            issues,
            "RV_UNKNOWN_PACK_ROLE",
            f"unknown selected item pack role(s): {unknown_roles}.",
        )
    rrf_scope = norm(record.get("rrf_scope"))
    if rrf_scope != "same_authority_bucket_only":
        add_once(
            issues,
            "RV_CROSS_BUCKET_RRF",
            "rrf_scope must stay same_authority_bucket_only.",
        )
    if as_bool(record.get("cross_bucket_rrf_used")) or as_bool(record.get("cross_bucket_rank_used")):
        add_once(
            issues,
            "RV_CROSS_BUCKET_RRF",
            "cross-bucket fusion/ranking cannot create authority.",
        )
    if (
        as_bool(record.get("selected_by_claims_support"))
        or as_bool(record.get("retrieval_rank_claims_support"))
        or as_bool(record.get("scores_are_support"))
    ):
        add_once(
            issues,
            "RV_SELECTED_BY_AS_SUPPORT",
            "selected_by or retrieval scores cannot be evidence support.",
        )
    if as_bool(record.get("graph_rank_claims_trust")):
        add_once(
            issues,
            "RV_GRAPH_RANK_AS_TRUST",
            "graph rank cannot create trust, support, or confidence.",
        )
    if (
        selected_buckets.intersection(RETRIEVAL_FORBIDDEN_SUPPORT_BUCKETS)
        and ("support" in roles or as_bool(record.get("selected_item_action_basis_allowed")))
    ):
        add_once(
            issues,
            "RV_CANDIDATE_OVERLAY_FEEDBACK_AS_SUPPORT",
            "candidate, overlay, source annotation, or feedback items cannot be support or action basis.",
        )
    if as_bool(record.get("legacy_raw_metadata_used")):
        add_once(
            issues,
            "RV_LEGACY_RAW_METADATA_USED",
            "legacy raw metadata must stay excluded from support receipts.",
        )
    evidence_role = norm(record.get("support_evidence_role"))
    support_result = norm(record.get("support_result"))
    support_claimed = (
        as_bool(record.get("support_claimed"))
        or support_result == "supported"
        or evidence_role in {"direct_support", "inferential_support"}
    )
    anchor_kind = norm(record.get("support_anchor_kind"))
    weak_anchor_kind = anchor_kind in {"url_only", "metadata_only", "summary_only", "briefing_summary"}
    if (evidence_role == "direct_support" or support_claimed) and weak_anchor_kind:
        add_once(
            issues,
            "RV_URL_ONLY_DIRECT_SUPPORT",
            "url-only, metadata-only, or summary-only material cannot be claimed support.",
        )
    if support_claimed and not has_value(record.get("independent_anchor_ref")):
        add_once(
            issues,
            "RV_MISSING_INDEPENDENT_SUPPORT_ANCHOR",
            "claimed support requires an independent anchor reference.",
        )
    if receipt_claims_authority(record):
        add_once(
            issues,
            "RV_RECEIPT_CLAIMS_AUTHORITY",
            "retrieval receipts cannot claim truth, review approval, support, action basis, or mainline readiness.",
        )
    validate_boundary_flags(
        record, RETRIEVAL_BOUNDARY_FLAGS, "RV_SUPPORT_BOUNDARY_FLAG_FALSE", issues
    )
    return issues


def is_significant_operation(record: dict[str, Any]) -> bool:
    mode = norm(record.get("operation_mode"))
    return (
        mode in SIGNIFICANT_OPERATION_MODES
        or as_bool(record.get("actual_write_performed"))
        or as_bool(record.get("intent_confirmation_required"))
    )


def validate_operation_receipt(record: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if not has_value(record.get("operation_id")) and not has_value(record.get("receipt_id")):
        add_missing(issues, "operation_id or receipt_id")
    for field in ("actor_tier", "operation_mode", "actual_write_performed"):
        if field not in record:
            add_missing(issues, field)
    if issues:
        return issues

    actor_tier = norm(record.get("actor_tier"))
    mode = norm(record.get("operation_mode"))
    target_scope = norm(record.get("target_scope"))
    actual_write = as_bool(record.get("actual_write_performed"))

    if actor_tier not in OPERATION_ACTOR_TIERS:
        add_once(
            issues,
            "OV_UNKNOWN_ACTOR_TIER",
            "actor_tier must be one of the known operation receipt tiers.",
        )
    if mode not in OPERATION_MODES:
        add_once(
            issues,
            "OV_UNKNOWN_OPERATION_MODE",
            "operation_mode must be one of the known operation modes.",
        )
    if target_scope and target_scope not in OPERATION_TARGET_SCOPES:
        add_once(
            issues,
            "OV_UNKNOWN_TARGET_SCOPE",
            "target_scope must be one of the known target scopes.",
        )
    if actor_tier == "read_only" and (mode != "read" or actual_write):
        add_once(
            issues,
            "OV_ACTOR_TIER_CANNOT_WRITE",
            "read_only actors cannot suggest action writes or perform writes.",
        )
    if actor_tier == "suggest_only" and (
        mode not in {"read", "suggest", "propose_write"} or actual_write
    ):
        add_once(
            issues,
            "OV_ACTOR_TIER_CANNOT_WRITE",
            "suggest_only actors can propose but cannot perform writes.",
        )
    if actor_tier == "candidate_write" and mode in WRITE_MODES and target_scope not in {
        "candidate",
        "sandbox",
    }:
        add_once(
            issues,
            "OV_CANDIDATE_WRITE_OUT_OF_SCOPE",
            "candidate_write actors can write only candidate or sandbox scopes.",
        )
    if mode == "schema_change" and (
        actor_tier != "owner_final" or not as_bool(record.get("owner_final_present"))
    ):
        add_once(
            issues,
            "OV_SCHEMA_CHANGE_MISSING_OWNER_FINAL",
            "schema_change requires owner_final actor and owner-final approval.",
        )
    if mode == "delete" and (
        actor_tier != "owner_final" or not as_bool(record.get("owner_final_present"))
    ):
        add_once(
            issues,
            "OV_DESTRUCTIVE_OPERATION_REQUIRES_OWNER_FINAL",
            "delete requires owner_final actor and owner-final approval.",
        )
    formal_write = mode in WRITE_MODES and target_scope in {
        "reviewed",
        "mainline",
        "formal",
        "schema",
        "protected",
    }
    reviewed_write = mode == "write" and (actor_tier == "reviewed_write" or target_scope == "reviewed")
    approval_required_write = reviewed_write or formal_write or (
        actual_write and target_scope in {"mainline", "formal", "schema", "protected"}
    )
    if approval_required_write and (
        not as_bool(record.get("approval_present")) or not has_value(record.get("checked_body_hash"))
    ):
        add_once(
            issues,
            "OV_REVIEWED_WRITE_MISSING_APPROVAL_OR_HASH",
            "reviewed, formal, schema, protected, or mainline writes require approval and checked_body_hash.",
        )
    if "checked_body_hash_match" in record and not as_bool(record.get("checked_body_hash_match")):
        add_once(
            issues,
            "OV_CHECKED_BODY_HASH_MISMATCH",
            "checked_body_hash mismatch invalidates approval for the changed body.",
        )
    rollback_required = (
        as_bool(record.get("rollback_required"))
        or mode in {"delete", "schema_change"}
        or (mode == "write" and target_scope in {"reviewed", "mainline"})
    )
    if rollback_required and not as_bool(record.get("rollback_plan_present")):
        add_once(
            issues,
            "OV_ROLLBACK_REQUIRED",
            "delete, schema_change, reviewed/mainline write, or explicitly rollback-required operation needs a rollback plan.",
        )
    if is_significant_operation(record) and not as_bool(record.get("user_intent_confirmed")):
        add_once(
            issues,
            "OV_MISSING_INTENT_CONFIRMATION",
            "significant operations require user intent confirmation.",
        )
    basis_materials = set(as_list(record.get("basis_materials")))
    action_basis_sensitive = (
        mode in SIGNIFICANT_OPERATION_MODES
        or actual_write
        or as_bool(record.get("action_basis_ready_claimed"))
    )
    if action_basis_sensitive and basis_materials.intersection(BAD_OPERATION_BASIS_MATERIALS):
        add_once(
            issues,
            "OV_INVALID_ACTION_BASIS",
            "candidate, feedback, retrieval, summary, context-pack, or rank material cannot be action basis.",
        )
    if receipt_claims_authority(record):
        add_once(
            issues,
            "OV_RECEIPT_CLAIMS_AUTHORITY",
            "operation receipts cannot claim truth, review approval, reviewed knowledge, action basis, or mainline readiness.",
        )
    validate_boundary_flags(
        record, OPERATION_BOUNDARY_FLAGS, "OV_OPERATION_BOUNDARY_FLAG_FALSE", issues
    )
    return issues


def validate_receipt(path: Path) -> list[GuardResult]:
    try:
        record = parse_frontmatter_flat(path.read_text(encoding="utf-8"))
    except Exception as exc:
        issues = [Issue("RV_OV_PARSE_ERROR", str(exc))]
        return results_from_issues("receipt", path, issues, pass_message="Receipt boundary passed.")
    record_kind = norm(record.get("record_kind"))
    if record_kind == "retrieval_receipt":
        issues = validate_retrieval_receipt(record)
    elif record_kind == "operation_receipt":
        issues = validate_operation_receipt(record)
    else:
        issues = [
            Issue(
                "RV_OV_INVALID_RECORD_KIND",
                "record_kind must be retrieval_receipt or operation_receipt.",
            )
        ]
    return results_from_issues("receipt", path, issues, pass_message="Receipt boundary passed.")


def validate_receipt_kind(path: Path, expected_kind: str, guard: str) -> list[GuardResult]:
    try:
        record = parse_frontmatter_flat(path.read_text(encoding="utf-8"))
    except Exception as exc:
        issues = [Issue("RV_OV_PARSE_ERROR", str(exc))]
        return results_from_issues(guard, path, issues, pass_message="Receipt boundary passed.")

    record_kind = norm(record.get("record_kind"))
    if record_kind != expected_kind:
        issues = [
            Issue(
                "RV_OV_INVALID_RECORD_KIND",
                f"record_kind must be {expected_kind} for this guard.",
            )
        ]
    elif expected_kind == "retrieval_receipt":
        issues = validate_retrieval_receipt(record)
    else:
        issues = validate_operation_receipt(record)
    return results_from_issues(guard, path, issues, pass_message="Receipt boundary passed.")


def validate_retrieval_receipt_file(path: Path) -> list[GuardResult]:
    return validate_receipt_kind(path, "retrieval_receipt", "retrieval_receipt")


def validate_operation_receipt_file(path: Path) -> list[GuardResult]:
    return validate_receipt_kind(path, "operation_receipt", "operation_receipt")


# P0-07 failure matrix guard ------------------------------------------------

MATRIX_SLICE_ID = "2026-06-15-p0-07-action-boundary-failure-matrix-sandbox"
MATRIX_REQUIRED_CASES = {
    "AB-01",
    "AB-02",
    "AB-03",
    "AB-04",
    "AB-05",
    "AB-06",
    "AB-07",
    "AB-08",
    "AB-09",
    "AB-10",
    "AB-11",
    "AB-12",
}
MATRIX_REQUIRED_CASE_FIELDS = {
    "case_id",
    "title",
    "failure_mode",
    "boundary_class",
    "source_refs",
    "blocked_by",
    "detection",
    "expected_outcome",
    "fixture_refs",
    "validator_or_check_refs",
    "authority_non_claims",
}
MATRIX_FALSE_AUTHORITY_FLAGS = {
    "mainline_ready",
    "reviewer_approval_created",
    "reviewed_knowledge_created",
    "evidence_support_created",
    "action_basis_created",
    "promotion_authorized",
}
MATRIX_BLOCKING_OUTCOMES = {"blocked", "not_ready", "requires_review", "reject"}


def validate_matrix_authority_flags(value: Any, issues: list[Issue], context: str) -> None:
    if not isinstance(value, dict):
        add_once(
            issues,
            "MATRIX_MISSING_AUTHORITY_NON_CLAIM",
            f"{context} authority_non_claims must be an object.",
        )
        return
    for flag in MATRIX_FALSE_AUTHORITY_FLAGS:
        if flag not in value:
            add_once(
                issues,
                "MATRIX_MISSING_AUTHORITY_NON_CLAIM",
                f"{context} missing authority_non_claims.{flag}.",
            )
        elif value[flag] is not False:
            add_once(
                issues,
                "MATRIX_FORBIDDEN_AUTHORITY_CLAIM",
                f"{context} authority_non_claims.{flag} must be false.",
            )


def validate_matrix_case(case: Any, issues: list[Issue]) -> None:
    if not isinstance(case, dict):
        add_once(issues, "MATRIX_INVALID_CASE", "case entry must be an object.")
        return
    case_id = str(case.get("case_id", "")).strip()
    context = case_id or "case"
    for field in MATRIX_REQUIRED_CASE_FIELDS:
        if field not in case or not has_value(case.get(field)):
            add_once(
                issues,
                "MATRIX_CASE_MISSING_FIELD",
                f"{context} missing required field {field}.",
            )
    for list_field in ("source_refs", "blocked_by", "fixture_refs", "validator_or_check_refs"):
        if not isinstance(case.get(list_field), list) or not case.get(list_field):
            add_once(
                issues,
                "MATRIX_CASE_MISSING_FIELD",
                f"{context} field {list_field} must be a non-empty list.",
            )
    for guard in case.get("blocked_by", []):
        if not isinstance(guard, dict) or not has_value(guard.get("slice_id")) or not has_value(
            guard.get("guard")
        ):
            add_once(
                issues,
                "MATRIX_CASE_MISSING_GUARD",
                f"{context} blocked_by entries need slice_id and guard.",
            )
    outcome = case.get("expected_outcome")
    if not isinstance(outcome, dict) or str(outcome.get("status", "")).strip() not in MATRIX_BLOCKING_OUTCOMES:
        add_once(
            issues,
            "MATRIX_CASE_NOT_BLOCKING",
            f"{context} expected_outcome.status must be blocking.",
        )
    validate_matrix_authority_flags(case.get("authority_non_claims"), issues, context)


def validate_matrix_data(data: Any) -> list[Issue]:
    issues: list[Issue] = []
    if not isinstance(data, dict):
        return [Issue("MATRIX_INVALID_JSON_SHAPE", "top-level JSON must be an object.")]
    if data.get("record_kind") != "action_boundary_failure_matrix":
        add_once(
            issues,
            "MATRIX_INVALID_RECORD_KIND",
            "record_kind must be action_boundary_failure_matrix.",
        )
    if data.get("slice_id") != MATRIX_SLICE_ID:
        add_once(issues, "MATRIX_INVALID_SLICE_ID", f"slice_id must be {MATRIX_SLICE_ID}.")
    validate_matrix_authority_flags(data.get("authority_non_claims"), issues, "matrix")
    cases = data.get("cases")
    if not isinstance(cases, list):
        add_once(issues, "MATRIX_CASES_NOT_LIST", "cases must be a list.")
        return issues
    seen: set[str] = set()
    case_ids: set[str] = set()
    for case in cases:
        case_id = str(case.get("case_id", "")).strip() if isinstance(case, dict) else ""
        if case_id in seen:
            add_once(issues, "MATRIX_DUPLICATE_CASE_ID", f"duplicate case_id {case_id}.")
        if case_id:
            seen.add(case_id)
            case_ids.add(case_id)
            if case_id.startswith("AB-") and case_id not in MATRIX_REQUIRED_CASES:
                add_once(issues, "MATRIX_UNKNOWN_CASE_ID", f"unknown required-scope case {case_id}.")
        validate_matrix_case(case, issues)
    missing = sorted(MATRIX_REQUIRED_CASES - case_ids)
    if missing:
        add_once(
            issues,
            "MATRIX_MISSING_REQUIRED_CASE",
            "missing required cases: " + ", ".join(missing),
        )
    return issues


def validate_failure_matrix(path: Path) -> list[GuardResult]:
    try:
        data = load_json_file_strict(path)
        issues = validate_matrix_data(data)
    except OSError as exc:
        issues = [Issue("MATRIX_READ_ERROR", str(exc))]
    except (UnicodeDecodeError, ValueError, json.JSONDecodeError) as exc:
        issues = [Issue("MATRIX_JSON_PARSE_ERROR", str(exc))]
    return results_from_issues(
        "failure_matrix",
        path,
        issues,
        pass_message="Failure matrix boundary passed.",
    )


# P1-10 runtime artifact guard ---------------------------------------------

RUNTIME_ARTIFACT_KINDS = {
    "python_cache",
    "bytecode_cache",
    "test_output",
    "suite_output",
    "verifier_output",
    "execution_log",
    "temporary_receipt",
    "generated_receipt",
    "scratch_file",
    "lockfile",
    "runtime_cache",
    "derived_index",
    "temporary_download",
    "transient_state",
    "benchmark_output",
}
DURABLE_NON_RUNTIME_KINDS = {
    "source_record",
    "raw_anchor",
    "reviewed_note",
    "reviewed_summary",
    "decision_record",
    "candidate_note",
    "project_overlay",
    "feedback_record",
    "sandbox_contract",
    "sandbox_verification_doc",
    "fixture",
    "failure_case",
    "source_map",
    "next_step_doc",
}
ALLOWED_ARTIFACT_KINDS = RUNTIME_ARTIFACT_KINDS.union(DURABLE_NON_RUNTIME_KINDS)
RUNTIME_PATH_MARKERS = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    ".cache",
    "node_modules/.cache",
    "tmp/",
    "temp/",
    "scratch/",
    "run-output",
    "suite-output",
    "verification-output",
    "generated-receipts",
    "runtime-cache",
    "derived-index",
}
RUNTIME_SUFFIXES = {".pyc", ".pyo", ".log", ".tmp", ".temp", ".lock", ".sqlite", ".db"}
SUPPORT_ROLES = {"support", "direct_support", "inferential_support", "evidence_support", "anchor"}
ACTION_ROLES = {"action_basis", "ready_action_basis"}
AUTHORITY_BUCKETS_FORBIDDEN_TO_RUNTIME = {
    "reviewed",
    "reviewed_knowledge",
    "raw",
    "raw_anchor",
    "support",
    "evidence_support",
    "action",
    "action_basis",
}
RUNTIME_AUTHORITY_CLAIMS = {
    "truth",
    "truth_confidence",
    "reviewed_knowledge",
    "reviewed_relation",
    "reviewer_approval",
    "evidence_support",
    "direct_support",
    "action_basis",
    "mainline_ready",
    "promotion_ready",
}
REQUIRED_RUNTIME_EXCLUSION_REASON = "runtime_artifact_excluded"


def raw_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def path_looks_runtime(path: str) -> bool:
    normalized = path.replace("\\", "/").lower()
    canonical = normalized.replace("_", "-").replace(" ", "-")
    if any(marker in normalized for marker in RUNTIME_PATH_MARKERS):
        return True
    if any(marker.replace("_", "-").replace(" ", "-") in canonical for marker in RUNTIME_PATH_MARKERS):
        return True
    return any(normalized.endswith(suffix) for suffix in RUNTIME_SUFFIXES)


def runtime_item_id(item: dict[str, Any]) -> str:
    return raw_text(item.get("id")) or raw_text(item.get("path")) or "<unknown>"


def artifact_kind(item: dict[str, Any]) -> str:
    return norm(item.get("artifact_kind"))


def is_runtime_artifact(item: dict[str, Any]) -> bool:
    kind = artifact_kind(item)
    path = raw_text(item.get("path"))
    return as_bool(item.get("runtime_artifact")) or kind in RUNTIME_ARTIFACT_KINDS or path_looks_runtime(path)


def validate_runtime_item(item: dict[str, Any], exclude_runtime: bool) -> list[Issue]:
    issues: list[Issue] = []
    current_id = runtime_item_id(item)
    kind = artifact_kind(item)
    runtime = is_runtime_artifact(item)
    if not has_value(item.get("id")):
        add_once(issues, "RA_MISSING_ITEM_ID", "item id is required.", current_id)
    if not has_value(item.get("path")):
        add_once(issues, "RA_MISSING_ITEM_PATH", "item path is required.", current_id)
    if kind not in ALLOWED_ARTIFACT_KINDS:
        add_once(
            issues,
            "RA_UNKNOWN_ARTIFACT_KIND",
            "artifact_kind must be a known durable or runtime kind.",
            current_id,
        )
    if runtime and item.get("runtime_artifact") is False:
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_MISLABELED",
            "path or kind indicates runtime artifact but runtime_artifact is false.",
            current_id,
        )
    seen_by_retrieval = as_bool(item.get("seen_by_retrieval"))
    selected = as_bool(item.get("selected"))
    excluded = as_bool(item.get("excluded"))
    excluded_reason = norm(item.get("excluded_reason"))
    pack_role = norm(item.get("pack_role"))
    evidence_role = norm(item.get("evidence_role"))
    authority_bucket = norm(item.get("authority_bucket"))
    action_basis_allowed = as_bool(item.get("action_basis_allowed")) or as_bool(
        item.get("used_as_action_basis")
    )
    if runtime and not exclude_runtime:
        add_once(
            issues,
            "RA_RUNTIME_FILTER_DISABLED",
            "runtime artifacts require exclude_runtime_artifacts=true.",
            current_id,
        )
    if runtime and seen_by_retrieval and not excluded:
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_NOT_EXCLUDED",
            "retrieval-visible runtime artifact must be excluded.",
            current_id,
        )
    if runtime and excluded and excluded_reason != REQUIRED_RUNTIME_EXCLUSION_REASON:
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_BAD_EXCLUSION_REASON",
            "runtime artifact exclusion must use runtime_artifact_excluded reason.",
            current_id,
        )
    if runtime and selected:
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_SELECTED",
            "runtime artifact cannot be selected for query context.",
            current_id,
        )
    if runtime and (
        pack_role in SUPPORT_ROLES
        or evidence_role in SUPPORT_ROLES
        or as_bool(item.get("support_claimed"))
    ):
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_AS_SUPPORT",
            "runtime artifact cannot be evidence support or support anchor.",
            current_id,
        )
    if runtime and (
        action_basis_allowed or pack_role in ACTION_ROLES or evidence_role in ACTION_ROLES
    ):
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_ACTION_BASIS",
            "runtime artifact cannot be action basis.",
            current_id,
        )
    if runtime and authority_bucket in AUTHORITY_BUCKETS_FORBIDDEN_TO_RUNTIME:
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_AUTHORITY_BUCKET",
            "runtime artifact cannot carry reviewed/raw/support/action authority bucket.",
            current_id,
        )
    claims = set(as_list(item.get("artifact_claims"))).union(set(as_list(item.get("receipt_claims"))))
    if runtime and claims.intersection(RUNTIME_AUTHORITY_CLAIMS):
        add_once(
            issues,
            "RA_RUNTIME_ARTIFACT_CLAIMS_AUTHORITY",
            "runtime artifact cannot claim truth, support, approval, action basis, or mainline readiness.",
            current_id,
        )
    return issues


def validate_runtime_manifest_data(manifest: dict[str, Any]) -> list[Issue]:
    issues: list[Issue] = []
    if norm(manifest.get("record_kind")) != "runtime_artifact_exclusion_manifest":
        add_once(
            issues,
            "RA_INVALID_RECORD_KIND",
            "record_kind must be runtime_artifact_exclusion_manifest.",
        )
    if not has_value(manifest.get("scenario_id")):
        add_once(issues, "RA_MISSING_SCENARIO_ID", "scenario_id is required.")
    if "exclude_runtime_artifacts" not in manifest:
        add_once(issues, "RA_MISSING_RUNTIME_FILTER", "exclude_runtime_artifacts is required.")
    exclude_runtime = as_bool(manifest.get("exclude_runtime_artifacts"))
    if not exclude_runtime:
        add_once(
            issues,
            "RA_RUNTIME_FILTER_DISABLED",
            "exclude_runtime_artifacts must be true.",
        )
    items = manifest.get("items")
    if not isinstance(items, list) or not items:
        add_once(issues, "RA_MISSING_ITEMS", "items must be a non-empty list.")
        return issues
    seen_ids: set[str] = set()
    for item in items:
        if not isinstance(item, dict):
            add_once(issues, "RA_INVALID_ITEM", "each item must be an object.")
            continue
        current_id = runtime_item_id(item)
        if current_id in seen_ids:
            add_once(issues, "RA_DUPLICATE_ITEM_ID", "item ids must be unique.", current_id)
        seen_ids.add(current_id)
        issues.extend(validate_runtime_item(item, exclude_runtime))
    return issues


def runtime_manifest_details(manifest: dict[str, Any], issues: list[Issue]) -> dict[str, Any]:
    items = manifest.get("items", [])
    if not isinstance(items, list):
        items = []
    return {
        "scenario_id": manifest.get("scenario_id", ""),
        "issue_codes": sorted({issue.code for issue in issues}),
        "runtime_artifact_ids": [
            runtime_item_id(item)
            for item in items
            if isinstance(item, dict) and is_runtime_artifact(item)
        ],
        "selected_item_ids": [
            runtime_item_id(item)
            for item in items
            if isinstance(item, dict) and as_bool(item.get("selected"))
        ],
    }


def validate_runtime_artifacts(path: Path) -> list[GuardResult]:
    try:
        manifest = load_json_file_strict(path)
        issues = validate_runtime_manifest_data(manifest)
        details = runtime_manifest_details(manifest, issues)
    except Exception as exc:
        issues = [Issue("RA_PARSE_OR_RUNTIME_ERROR", str(exc))]
        details = None
    return results_from_issues(
        "runtime_artifacts",
        path,
        issues,
        pass_message="Runtime artifact exclusion boundary passed.",
        details=details,
    )


def scan_runtime_paths(path: Path) -> list[GuardResult]:
    if path.is_file() and path.suffix.lower() == ".json":
        return validate_runtime_artifacts(path)
    if path.is_file():
        if path_looks_runtime(str(path)):
            return [
                GuardResult(
                    guard="runtime_artifacts",
                    path=str(path),
                    status=STATUS_WARN,
                    code="runtime_artifact_detected",
                    message="Path looks like a runtime artifact; exclude it from context selection.",
                    next_step="Exclude this path from retrieval/context/action use; do not delete it from this check.",
                )
            ]
        return []
    runtime_paths = [
        p
        for p in path.rglob("*")
        if p.is_file()
        and path_looks_runtime(str(p.relative_to(path)))
        and not guard_applies("runtime_artifacts", p)
    ]
    if not runtime_paths:
        return []
    return [
        GuardResult(
            guard="runtime_artifacts",
            path=str(p),
            status=STATUS_WARN,
            code="runtime_artifact_detected",
            message="Runtime-like path detected; exclude it from context selection.",
            next_step="Exclude this path from retrieval/context/action use; do not delete it from this check.",
        )
        for p in runtime_paths
    ]


GUARD_FUNCS: dict[str, Callable[[Path], list[GuardResult]]] = {
    "body_hash": validate_body_hash,
    "support_boundary": validate_support_boundary,
    "action_readiness": validate_action_readiness,
    "feedback": validate_feedback,
    "retrieval_receipt": validate_retrieval_receipt_file,
    "operation_receipt": validate_operation_receipt_file,
    "receipt": validate_receipt,
    "failure_matrix": validate_failure_matrix,
    "runtime_artifacts": validate_runtime_artifacts,
}

MODE_GUARDS = {
    "review": ("body_hash", "support_boundary"),
    "action-preflight": ("support_boundary", "action_readiness"),
    "feedback": ("feedback",),
    "retrieval": ("retrieval_receipt", "runtime_artifacts"),
    "operation-preflight": ("operation_receipt", "body_hash", "runtime_artifacts"),
    "artifact-selection": ("runtime_artifacts",),
}

CHECKED_SCOPE_BY_MODE = {
    "review": [
        "candidate body hash contract",
        "review/support authority bucket contract",
    ],
    "action-preflight": [
        "support boundary contract",
        "action readiness consistency contract",
    ],
    "feedback": [
        "feedback non-truth-mutation contract",
    ],
    "retrieval": [
        "retrieval receipt process contract",
        "runtime artifact exclusion contract",
    ],
    "operation-preflight": [
        "operation receipt process contract",
        "candidate body hash contract when applicable",
        "runtime artifact exclusion contract",
    ],
    "artifact-selection": [
        "runtime artifact exclusion contract",
    ],
}

CHECKED_SCOPE_BY_GUARD = {
    "body_hash": ["candidate body hash contract"],
    "support_boundary": ["support authority bucket contract"],
    "action_readiness": ["action readiness consistency contract"],
    "feedback": ["feedback non-truth-mutation contract"],
    "retrieval_receipt": ["retrieval receipt process contract"],
    "operation_receipt": ["operation receipt process contract"],
    "receipt": ["retrieval/operation receipt process contract"],
    "failure_matrix": ["action-boundary failure matrix regression oracle"],
    "runtime_artifacts": ["runtime artifact exclusion contract"],
}

MARKDOWN_GUARDS = {
    "body_hash",
    "support_boundary",
    "action_readiness",
    "feedback",
    "retrieval_receipt",
    "operation_receipt",
    "receipt",
}

JSON_GUARDS = {"failure_matrix", "runtime_artifacts"}


def input_integrity_result(path: Path, guards: Iterable[str]) -> GuardResult | None:
    guard_set = set(guards)
    if path.suffix.lower() == ".md" and guard_set.intersection(MARKDOWN_GUARDS):
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError as exc:
            return GuardResult(
                guard="input_contract",
                path=str(path),
                status=STATUS_BLOCK,
                code="INPUT_DECODE_ERROR",
                message=str(exc),
                next_step=next_step_for("INPUT_DECODE_ERROR"),
            )
        except OSError as exc:
            return GuardResult(
                guard="input_contract",
                path=str(path),
                status=STATUS_BLOCK,
                code="INPUT_READ_ERROR",
                message=str(exc),
                next_step=next_step_for("INPUT_READ_ERROR"),
            )
        if split_frontmatter(text) is not None:
            try:
                parse_frontmatter_nested(text)
            except ValueError as exc:
                return GuardResult(
                    guard="input_contract",
                    path=str(path),
                    status=STATUS_BLOCK,
                    code="INPUT_INVALID_FRONTMATTER",
                    message=str(exc),
                    next_step=next_step_for("INPUT_INVALID_FRONTMATTER"),
                )
    if path.suffix.lower() == ".json" and guard_set.intersection(JSON_GUARDS):
        try:
            load_json_file_strict(path)
        except UnicodeDecodeError as exc:
            return GuardResult(
                guard="input_contract",
                path=str(path),
                status=STATUS_BLOCK,
                code="INPUT_JSON_DECODE_ERROR",
                message=str(exc),
                next_step=next_step_for("INPUT_JSON_DECODE_ERROR"),
            )
        except (OSError, ValueError, json.JSONDecodeError) as exc:
            return GuardResult(
                guard="input_contract",
                path=str(path),
                status=STATUS_BLOCK,
                code="INPUT_INVALID_JSON",
                message=str(exc),
                next_step=next_step_for("INPUT_INVALID_JSON"),
            )
    return None


def file_record_kind(path: Path) -> str:
    try:
        if path.suffix.lower() == ".json":
            data = load_json_file_strict(path)
            return norm(data.get("record_kind")) if isinstance(data, dict) else ""
        return norm(parse_frontmatter_flat(path.read_text(encoding="utf-8"), strict=False).get("record_kind"))
    except Exception:
        return ""


def guard_applies(guard: str, path: Path) -> bool:
    if not path.is_file():
        return False
    suffix = path.suffix.lower()
    record_kind = file_record_kind(path)
    if guard == "body_hash":
        if suffix != ".md":
            return False
        try:
            fm, _body = parse_frontmatter_nested(path.read_text(encoding="utf-8"))
        except Exception:
            return False
        return any(
            key in fm
            for key in (
                "candidate_body_location",
                "body_hash",
                "review_status",
                "review_object_state",
                "writeback_ready",
            )
        )
    if guard == "support_boundary":
        if suffix != ".md":
            return False
        try:
            fm, _body = parse_frontmatter_nested(path.read_text(encoding="utf-8"))
        except Exception:
            return False
        return any(
            key in fm
            for key in (
                "support_claimed",
                "pack_role",
                "evidence_role",
                "proposed_support_record_kind",
                "proposed_support_authority_bucket",
            )
        )
    if guard == "action_readiness":
        return suffix == ".md" and (
            record_kind == "action_readiness_check"
            or "action_readiness" in parse_frontmatter_flat(path.read_text(encoding="utf-8"), strict=False)
        )
    if guard == "feedback":
        return suffix == ".md" and record_kind in {"feedback_event", "feedback-event"}
    if guard == "retrieval_receipt":
        return suffix == ".md" and record_kind == "retrieval_receipt"
    if guard == "operation_receipt":
        return suffix == ".md" and record_kind == "operation_receipt"
    if guard == "receipt":
        return suffix == ".md" and record_kind in {"retrieval_receipt", "operation_receipt"}
    if guard == "failure_matrix":
        return suffix == ".json" and record_kind == "action_boundary_failure_matrix"
    if guard == "runtime_artifacts":
        return suffix == ".json" and record_kind == "runtime_artifact_exclusion_manifest"
    return False


def collect_files(path: Path) -> list[Path]:
    if path.is_file():
        return [path]
    return sorted(p for p in path.rglob("*") if p.is_file() and p.suffix.lower() in {".md", ".json"})


def run_check(path: Path, guard: str | None, mode: str) -> list[GuardResult]:
    files = collect_files(path)
    results: list[GuardResult] = []
    guards = (guard,) if guard else MODE_GUARDS[mode]
    if "runtime_artifacts" in guards and (
        path.is_dir() or (path.is_file() and not guard_applies("runtime_artifacts", path))
    ):
        results.extend(scan_runtime_paths(path))
    for file_path in files:
        input_error = input_integrity_result(file_path, guards)
        if input_error is not None:
            results.append(input_error)
            continue
        for current_guard in guards:
            if current_guard == "runtime_artifacts" and not guard_applies(current_guard, file_path):
                continue
            if guard is None and not guard_applies(current_guard, file_path):
                continue
            if guard is not None and not guard_applies(current_guard, file_path):
                continue
            results.extend(GUARD_FUNCS[current_guard](file_path))
    return results


def overall_status(results: list[GuardResult]) -> str | None:
    if not results:
        return None
    statuses = {result.status for result in results}
    if STATUS_BLOCK in statuses:
        return STATUS_BLOCK
    if STATUS_WARN in statuses:
        return STATUS_WARN
    return STATUS_PASS


def count_statuses(results: list[GuardResult]) -> dict[str, int]:
    summary = {STATUS_PASS: 0, STATUS_WARN: 0, STATUS_BLOCK: 0}
    for result in results:
        summary[result.status] += 1
    return summary


def checked_scope_for(mode: str | None, guard: str | None) -> list[str]:
    if guard:
        return CHECKED_SCOPE_BY_GUARD.get(guard, [guard])
    if mode:
        return CHECKED_SCOPE_BY_MODE.get(mode, [mode])
    return []


def summarize_results(
    path: Path,
    results: list[GuardResult],
    *,
    mode: str | None,
    guard: str | None = None,
    run_state: str = RUN_EXECUTED,
    code: str = "",
    message: str = "",
) -> dict[str, Any]:
    status = overall_status(results)
    return {
        "tool": TOOL_NAME,
        "version": VERSION,
        "mode": mode or (f"guard:{guard}" if guard else None),
        "target": str(path),
        "run_state": run_state,
        "status": status,
        "code": code,
        "message": message,
        "summary": count_statuses(results),
        "findings": [result.as_dict() for result in results],
        "checked_scope": checked_scope_for(mode, guard),
        "not_checked": NOT_CHECKED_BY_GUARD,
        "authority_boundary": AUTHORITY_BOUNDARY,
    }


def error_payload(path: Path, *, mode: str | None, guard: str | None, code: str) -> dict[str, Any]:
    return summarize_results(
        path,
        [],
        mode=mode,
        guard=guard,
        run_state=RUN_ERROR,
        code=code,
        message=next_step_for(code),
    )


def skipped_payload(path: Path, *, mode: str | None, guard: str | None) -> dict[str, Any]:
    return summarize_results(
        path,
        [],
        mode=mode,
        guard=guard,
        run_state=RUN_SKIPPED,
        code="no_applicable_input",
        message="No applicable VAKS Guard input was found for this target and mode.",
    )


def build_check_payload(path: Path, guard: str | None, mode: str | None) -> dict[str, Any]:
    if mode and guard:
        return error_payload(path, mode=mode, guard=guard, code="mode_guard_conflict")
    if not mode and not guard:
        return error_payload(path, mode=mode, guard=guard, code="missing_mode_or_guard")
    if not path.exists():
        return error_payload(path, mode=mode, guard=guard, code="missing_required_input")
    try:
        results = run_check(path, guard, mode or "")
    except Exception:
        return error_payload(path, mode=mode, guard=guard, code="tool_runtime_error")
    if not results:
        return skipped_payload(path, mode=mode, guard=guard)
    return summarize_results(path, results, mode=mode, guard=guard)


def emit(payload: dict[str, Any], json_output: bool) -> None:
    if json_output:
        print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        return
    status = payload["status"] or "null"
    print(
        f"{payload['run_state'].upper()} {status.upper()} "
        f"{payload['mode']} {payload['target']}"
    )
    if payload.get("code"):
        print(f"- {payload['code']}: {payload.get('message', '')}")
    for result in payload["findings"]:
        print(
            f"- [{result['status']}] {result['guard']} {result['code']}: "
            f"{result['message']} next={result['next_step']}"
        )


def direct_case_files(root: Path, suffix: str) -> list[Path]:
    if not root.exists():
        return []
    return sorted(p for p in root.iterdir() if p.is_file() and p.suffix.lower() == suffix)


SELF_TEST_CONFIG = {
    "body_hash": {
        "suffix": ".md",
        "expected_positive": 5,
        "expected_failure": 5,
    },
    "support_boundary": {
        "suffix": ".md",
        "expected_positive": 3,
        "expected_failure": 10,
    },
    "action_readiness": {
        "suffix": ".md",
        "expected_positive": 4,
        "expected_failure": 25,
    },
    "feedback": {
        "suffix": ".md",
        "expected_positive": 4,
        "expected_failure": 31,
    },
    "failure_matrix": {
        "suffix": ".json",
        "expected_positive": 3,
        "expected_failure": 7,
    },
    "receipt": {
        "suffix": ".md",
        "expected_positive": 4,
        "expected_failure": 27,
    },
    "runtime_artifacts": {
        "suffix": ".json",
        "expected_positive": 4,
        "expected_failure": 20,
    },
}


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_manifest(test_root: Path) -> dict[str, Any]:
    manifest_path = test_root / "manifest.json"
    report: dict[str, Any] = {
        "path": str(manifest_path),
        "checked_source_validators": 0,
        "checked_case_hashes": 0,
        "missing_source_validators": [],
        "warnings": [],
        "failures": [],
    }
    if not manifest_path.exists():
        report["failures"].append("manifest.json is missing.")
        return report
    try:
        manifest = load_json_file_strict(manifest_path)
    except Exception as exc:
        report["failures"].append(f"manifest.json could not be parsed: {exc}")
        return report

    repo_root = Path(__file__).resolve().parents[1]
    for entry in manifest.get("source_validators", []):
        rel_path = entry.get("path", "")
        expected_hash = entry.get("sha256", "")
        source_path = repo_root / rel_path
        if not source_path.exists():
            report["missing_source_validators"].append(rel_path)
            report["warnings"].append(
                f"optional provenance source validator missing: {rel_path}"
            )
            continue
        report["checked_source_validators"] += 1
        actual_hash = sha256_file(source_path)
        if actual_hash != expected_hash:
            report["failures"].append(f"source validator hash drifted: {rel_path}")

    copied_cases = manifest.get("copied_cases", {})
    for guard, guard_manifest in copied_cases.items():
        case_hashes = guard_manifest.get("file_hashes", {})
        for rel_case, expected_hash in case_hashes.items():
            case_path = test_root / guard / rel_case
            if not case_path.exists():
                report["failures"].append(f"copied case missing: {guard}/{rel_case}")
                continue
            report["checked_case_hashes"] += 1
            actual_hash = sha256_file(case_path)
            if actual_hash != expected_hash:
                report["failures"].append(f"copied case hash drifted: {guard}/{rel_case}")

    expected_hash = manifest.get("expected_results_sha256", "")
    expected_path = test_root / "expected_results.json"
    if expected_hash:
        if not expected_path.exists():
            report["failures"].append("expected_results.json is missing.")
        elif sha256_file(expected_path) != expected_hash:
            report["failures"].append("expected_results.json hash drifted.")
    return report


def run_contract_tests() -> dict[str, Any]:
    failures: list[str] = []
    missing_payload = build_check_payload(
        Path("__vaks_guard_missing_input__.md"),
        guard=None,
        mode="review",
    )
    if missing_payload["run_state"] != RUN_ERROR or missing_payload["status"] is not None:
        failures.append("missing path did not return error/null status.")
    if missing_payload["code"] != "missing_required_input":
        failures.append("missing path did not return missing_required_input.")

    with tempfile.TemporaryDirectory(prefix="vaks-guard-self-test-") as temp_dir:
        temp_root = Path(temp_dir)

        bad_frontmatter = temp_root / "bad-feedback.md"
        bad_frontmatter.write_text(
            "---\nrecord_kind: feedback_event\ninvalid frontmatter line\n---\n",
            encoding="utf-8",
        )
        bad_results = validate_feedback(bad_frontmatter)
        bad_status = overall_status(bad_results)
        bad_codes = {result.code for result in bad_results}
        if bad_status != STATUS_BLOCK or "FB_INVALID_FRONTMATTER" not in bad_codes:
            failures.append("invalid frontmatter did not block with FB_INVALID_FRONTMATTER.")

        bad_nested_frontmatter = temp_root / "bad-support-nested.md"
        bad_nested_frontmatter.write_text(
            "---\n"
            "support_claimed: true\n"
            "proposed_support_authority_bucket: reviewed\n"
            "approval_integrity:\n"
            "  checked_body_hash: abc\n"
            "  illegal nested line\n"
            "---\n",
            encoding="utf-8",
        )
        nested_payload = build_check_payload(
            bad_nested_frontmatter,
            guard=None,
            mode="review",
        )
        if nested_payload["status"] != STATUS_BLOCK:
            failures.append("invalid nested frontmatter did not block in review mode.")
        nested_codes = {
            finding["code"] for finding in nested_payload.get("findings", [])
        }
        if "INPUT_INVALID_FRONTMATTER" not in nested_codes:
            failures.append("invalid nested frontmatter did not report INPUT_INVALID_FRONTMATTER.")

        spaced_key_duplicate = temp_root / "spaced-key-duplicate.md"
        spaced_key_duplicate.write_text(
            "---\n"
            "support_claimed: false\n"
            "support_claimed : true\n"
            "pack_role: orientation\n"
            "pack_role : support\n"
            "proposed_support_authority_bucket: reviewed\n"
            "proposed_support_authority_bucket : candidate\n"
            "---\n",
            encoding="utf-8",
        )
        spaced_key_payload = build_check_payload(
            spaced_key_duplicate,
            guard=None,
            mode="review",
        )
        if spaced_key_payload["status"] != STATUS_BLOCK:
            failures.append("spaced duplicate frontmatter key did not block.")
        spaced_key_codes = {
            finding["code"] for finding in spaced_key_payload.get("findings", [])
        }
        if "INPUT_INVALID_FRONTMATTER" not in spaced_key_codes:
            failures.append("spaced duplicate key did not report INPUT_INVALID_FRONTMATTER.")

        quoted_key_duplicate = temp_root / "quoted-key-duplicate.md"
        quoted_key_duplicate.write_text(
            "---\n"
            "support_claimed: false\n"
            "\"support_claimed\": true\n"
            "pack_role: orientation\n"
            "\"pack_role\": support\n"
            "proposed_support_authority_bucket: reviewed\n"
            "\"proposed_support_authority_bucket\": candidate\n"
            "---\n",
            encoding="utf-8",
        )
        quoted_key_payload = build_check_payload(
            quoted_key_duplicate,
            guard=None,
            mode="review",
        )
        if quoted_key_payload["status"] != STATUS_BLOCK:
            failures.append("quoted duplicate frontmatter key did not block.")
        quoted_key_codes = {
            finding["code"] for finding in quoted_key_payload.get("findings", [])
        }
        if "INPUT_INVALID_FRONTMATTER" not in quoted_key_codes:
            failures.append("quoted duplicate key did not report INPUT_INVALID_FRONTMATTER.")

        tab_indentation = temp_root / "tab-indentation.md"
        tab_indentation.write_text(
            "---\n"
            "support_claimed: true\n"
            "approval_integrity:\n"
            "\tchecked_body_hash: abc\n"
            "---\n",
            encoding="utf-8",
        )
        tab_payload = build_check_payload(
            tab_indentation,
            guard=None,
            mode="review",
        )
        if tab_payload["status"] != STATUS_BLOCK:
            failures.append("tab-indented frontmatter did not block.")
        tab_codes = {finding["code"] for finding in tab_payload.get("findings", [])}
        if "INPUT_INVALID_FRONTMATTER" not in tab_codes:
            failures.append("tab-indented frontmatter did not report INPUT_INVALID_FRONTMATTER.")

        empty_key = temp_root / "empty-key.md"
        empty_key.write_text(
            "---\n"
            ": value\n"
            "support_claimed: true\n"
            "---\n",
            encoding="utf-8",
        )
        empty_key_payload = build_check_payload(
            empty_key,
            guard=None,
            mode="review",
        )
        if empty_key_payload["status"] != STATUS_BLOCK:
            failures.append("empty frontmatter key did not block.")
        empty_key_codes = {
            finding["code"] for finding in empty_key_payload.get("findings", [])
        }
        if "INPUT_INVALID_FRONTMATTER" not in empty_key_codes:
            failures.append("empty frontmatter key did not report INPUT_INVALID_FRONTMATTER.")

        duplicate_feedback = temp_root / "duplicate-feedback-key.md"
        duplicate_feedback.write_text(
            "---\n"
            "record_kind: feedback_event\n"
            "feedback_kind: correction\n"
            "affects: [usefulness, truth_confidence]\n"
            "affects: [usefulness]\n"
            "never_affects_directly: [truth_confidence, verification_status, source_reliability]\n"
            "---\n",
            encoding="utf-8",
        )
        duplicate_payload = build_check_payload(
            duplicate_feedback,
            guard=None,
            mode="feedback",
        )
        if duplicate_payload["status"] != STATUS_BLOCK:
            failures.append("duplicate frontmatter key did not block in feedback mode.")
        duplicate_codes = {
            finding["code"] for finding in duplicate_payload.get("findings", [])
        }
        if "INPUT_INVALID_FRONTMATTER" not in duplicate_codes:
            failures.append("duplicate frontmatter key did not report INPUT_INVALID_FRONTMATTER.")

        duplicate_json = temp_root / "duplicate-runtime-key.json"
        duplicate_json.write_text(
            "{"
            "\"record_kind\":\"runtime_artifact_exclusion_manifest\","
            "\"scenario_id\":\"duplicate-json\","
            "\"exclude_runtime_artifacts\":true,"
            "\"exclude_runtime_artifacts\":false,"
            "\"items\":[{\"id\":\"runtime_1\",\"artifact_kind\":\"python_cache\",\"selected\":false}]"
            "}",
            encoding="utf-8",
        )
        duplicate_json_payload = build_check_payload(
            duplicate_json,
            guard=None,
            mode="artifact-selection",
        )
        if duplicate_json_payload["status"] != STATUS_BLOCK:
            failures.append("duplicate JSON key did not block in artifact-selection mode.")
        duplicate_json_codes = {
            finding["code"] for finding in duplicate_json_payload.get("findings", [])
        }
        if "INPUT_INVALID_JSON" not in duplicate_json_codes:
            failures.append("duplicate JSON key did not report INPUT_INVALID_JSON.")

        non_utf_body = temp_root / "non-utf-body.bin"
        non_utf_body.write_bytes(b"\xff\xfe\xfa")
        body_hash_record = temp_root / "body-ref-non-utf.md"
        body_hash_record.write_text(
            "---\n"
            "candidate_body_location: non-utf-body.bin\n"
            "review_status: fixed\n"
            "body_hash: 0000\n"
            "---\n",
            encoding="utf-8",
        )
        non_utf_payload = build_check_payload(
            body_hash_record,
            guard="body_hash",
            mode=None,
        )
        if non_utf_payload["status"] != STATUS_BLOCK:
            failures.append("non-UTF-8 referenced body did not block.")
        non_utf_codes = {
            finding["code"] for finding in non_utf_payload.get("findings", [])
        }
        if "candidate_body_location_decode_error" not in non_utf_codes:
            failures.append("non-UTF-8 referenced body did not report decode error.")

        non_utf_record = temp_root / "non-utf-record.md"
        non_utf_record.write_bytes(b"\xff\xfe\xfa")
        non_utf_record_payload = build_check_payload(
            non_utf_record,
            guard=None,
            mode="feedback",
        )
        if non_utf_record_payload["status"] != STATUS_BLOCK:
            failures.append("non-UTF-8 Markdown input did not block.")
        non_utf_record_codes = {
            finding["code"] for finding in non_utf_record_payload.get("findings", [])
        }
        if "INPUT_DECODE_ERROR" not in non_utf_record_codes:
            failures.append("non-UTF-8 Markdown input did not report INPUT_DECODE_ERROR.")

        plain_markdown = temp_root / "plain.md"
        plain_markdown.write_text("# plain document\n\nNo VAKS guard record here.\n", encoding="utf-8")
        plain_payload = build_check_payload(
            plain_markdown,
            guard="support_boundary",
            mode=None,
        )
        if plain_payload["run_state"] != RUN_SKIPPED or plain_payload["status"] is not None:
            failures.append("direct guard on non-applicable input did not skip/null.")
        if plain_payload["code"] != "no_applicable_input":
            failures.append("direct guard on non-applicable input did not report no_applicable_input.")

        conflict_payload = build_check_payload(
            duplicate_feedback,
            guard="retrieval_receipt",
            mode="feedback",
        )
        if conflict_payload["run_state"] != RUN_ERROR or conflict_payload["status"] is not None:
            failures.append("mode+guard conflict did not return error/null.")
        if conflict_payload["code"] != "mode_guard_conflict":
            failures.append("mode+guard conflict did not report mode_guard_conflict.")

        empty_receipt = temp_root / "empty-retrieval-receipt.md"
        empty_receipt.write_text(
            "---\nrecord_kind: retrieval_receipt\n---\n",
            encoding="utf-8",
        )
        receipt_results = validate_receipt(empty_receipt)
        receipt_status = overall_status(receipt_results)
        receipt_codes = {result.code for result in receipt_results}
        if (
            receipt_status != STATUS_BLOCK
            or "RV_OV_MISSING_REQUIRED_FIELD" not in receipt_codes
        ):
            failures.append("empty receipt did not block with RV_OV_MISSING_REQUIRED_FIELD.")

    return {
        "missing_path": missing_payload,
        "failures": failures,
    }


def run_self_test() -> dict[str, Any]:
    test_root = Path(__file__).resolve().parent / "tests" / "vaks_guard"
    expected_path = test_root / "expected_results.json"
    if expected_path.exists():
        expected_payload = load_json_file_strict(expected_path)
        expected_cases = expected_payload.get("cases", {})
    else:
        expected_payload = None
        expected_cases = {}
    guard_reports: dict[str, Any] = {}
    failures: list[str] = []
    for guard, config in SELF_TEST_CONFIG.items():
        guard_root = test_root / guard
        suffix = str(config["suffix"])
        positive_files = direct_case_files(guard_root / "fixtures", suffix)
        failure_files = direct_case_files(guard_root / "failure-cases", suffix)
        positive_blocked: list[str] = []
        failure_not_blocked: list[str] = []
        code_mismatches: list[dict[str, Any]] = []
        seen_case_keys: set[str] = set()
        positive_statuses = {STATUS_PASS: 0, STATUS_WARN: 0, STATUS_BLOCK: 0}
        failure_statuses = {STATUS_PASS: 0, STATUS_WARN: 0, STATUS_BLOCK: 0}

        for file_path in positive_files:
            results = GUARD_FUNCS[guard](file_path)
            status = overall_status(results)
            positive_statuses[status] += 1
            if status == STATUS_BLOCK:
                positive_blocked.append(str(file_path))
            compare_expected_case(
                test_root,
                guard,
                file_path,
                status,
                results,
                expected_cases,
                code_mismatches,
                seen_case_keys,
            )
        for file_path in failure_files:
            results = GUARD_FUNCS[guard](file_path)
            status = overall_status(results)
            failure_statuses[status] += 1
            if status != STATUS_BLOCK:
                failure_not_blocked.append(str(file_path))
            compare_expected_case(
                test_root,
                guard,
                file_path,
                status,
                results,
                expected_cases,
                code_mismatches,
                seen_case_keys,
            )

        if len(positive_files) != config["expected_positive"]:
            failures.append(
                f"{guard}: expected {config['expected_positive']} positive files, found {len(positive_files)}"
            )
        if len(failure_files) != config["expected_failure"]:
            failures.append(
                f"{guard}: expected {config['expected_failure']} failure files, found {len(failure_files)}"
            )
        if positive_blocked:
            failures.append(f"{guard}: positive files blocked: {positive_blocked}")
        if failure_not_blocked:
            failures.append(f"{guard}: failure files not blocked: {failure_not_blocked}")
        if code_mismatches:
            failures.append(f"{guard}: expected code/status mismatches: {code_mismatches}")

        missing_expected = sorted(set(expected_cases.get(guard, {})) - seen_case_keys)
        if missing_expected:
            failures.append(f"{guard}: expected cases not exercised: {missing_expected}")

        guard_reports[guard] = {
            "positive_files": len(positive_files),
            "failure_files": len(failure_files),
            "positive_statuses": positive_statuses,
            "failure_statuses": failure_statuses,
            "positive_blocked": positive_blocked,
            "failure_not_blocked": failure_not_blocked,
            "code_mismatches": code_mismatches,
        }

    manifest_report = verify_manifest(test_root)
    contract_report = run_contract_tests()
    failures.extend(f"manifest: {failure}" for failure in manifest_report["failures"])
    failures.extend(f"contract: {failure}" for failure in contract_report["failures"])

    return {
        "tool": TOOL_NAME,
        "version": VERSION,
        "run_state": RUN_EXECUTED,
        "status": STATUS_PASS if not failures else STATUS_BLOCK,
        "test_root": str(test_root),
        "expected_results": str(expected_path) if expected_payload is not None else "",
        "guard_reports": guard_reports,
        "manifest_report": manifest_report,
        "contract_report": contract_report,
        "failures": failures,
        "authority_boundary": AUTHORITY_BOUNDARY,
    }


def compare_expected_case(
    test_root: Path,
    guard: str,
    file_path: Path,
    status: str,
    results: list[GuardResult],
    expected_cases: dict[str, Any],
    code_mismatches: list[dict[str, Any]],
    seen_case_keys: set[str],
) -> None:
    guard_root = test_root / guard
    case_key = file_path.relative_to(guard_root).as_posix()
    seen_case_keys.add(case_key)
    expected = expected_cases.get(guard, {}).get(case_key)
    if expected is None:
        code_mismatches.append(
            {
                "case": case_key,
                "expected_missing": True,
                "actual_status": status,
                "actual_codes": sorted(
                    result.code for result in results if result.code != "ok"
                ),
            }
        )
        return
    actual_codes = sorted({result.code for result in results if result.code != "ok"})
    expected_codes = sorted(expected.get("expected_codes", []))
    expected_status = expected.get("expected_status", STATUS_PASS)
    if actual_codes != expected_codes or status != expected_status:
        code_mismatches.append(
            {
                "case": case_key,
                "expected_status": expected_status,
                "actual_status": status,
                "expected_codes": expected_codes,
                "actual_codes": actual_codes,
            }
        )


def exit_code_for_payload(payload: dict[str, Any]) -> int:
    if payload.get("run_state") in {RUN_ERROR, RUN_SKIPPED}:
        return 3
    if payload.get("status") == STATUS_BLOCK:
        return 2
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Run VAKS Guard read-only lazy gates. The tool reports contract "
            "violations only; it does not approve review, support, action, "
            "promotion, or writes."
        )
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", help="check one file or folder")
    check_parser.add_argument("path", type=Path)
    check_parser.add_argument(
        "--mode",
        choices=sorted(MODE_GUARDS),
        help="explicit lazy-gate mode; no default all-vault scan exists",
    )
    check_parser.add_argument(
        "--guard",
        choices=sorted(GUARD_FUNCS),
        help="run one guard directly, used for parity/self-test checks",
    )
    check_parser.add_argument("--json", action="store_true")

    self_parser = subparsers.add_parser("self-test", help="run copied parity fixtures")
    self_parser.add_argument("--json", action="store_true")

    args = parser.parse_args(argv)

    if args.command == "self-test":
        payload = run_self_test()
        if args.json:
            print(json.dumps(payload, indent=2, sort_keys=True, ensure_ascii=False))
        else:
            print(f"{payload['status'].upper()} self-test {payload['test_root']}")
            for guard, report in payload["guard_reports"].items():
                print(
                    f"- {guard}: positives={report['positive_files']} "
                    f"statuses={report['positive_statuses']} failures={report['failure_files']} "
                    f"statuses={report['failure_statuses']}"
                )
            print(
                f"- manifest: source_validators={payload['manifest_report']['checked_source_validators']} "
                f"case_hashes={payload['manifest_report']['checked_case_hashes']}"
            )
            for failure in payload["failures"]:
                print(f"FAIL: {failure}")
        return 0 if payload["status"] == STATUS_PASS else 2

    payload = build_check_payload(args.path, args.guard, args.mode)
    emit(payload, args.json)
    return exit_code_for_payload(payload)


if __name__ == "__main__":
    raise SystemExit(main())
