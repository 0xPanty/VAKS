#!/usr/bin/env python3
"""Sandbox body-hash validator for VAKS P0-03.

This script is intentionally local to this sandbox slice. It is not a mainline
tool, not reviewer approval, and not action basis.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import sys
from typing import Any


VALID_STATUS_REQUIRING_HASH = {"fixed", "approved", "writeback_ready"}
VALID_REVIEW_OBJECT_STATES_REQUIRING_HASH = {
    "fixed_for_review",
    "revised_after_review",
    "approved",
    "writeback_ready",
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


def parse_frontmatter(text: str) -> tuple[dict[str, Any], str]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text

    end = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            end = index
            break
    if end is None:
        return {}, text

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

    body = "\n".join(lines[end + 1 :])
    return data, body


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
    else:
        body_path = record_path
        body_text = record_body

    if section_selector:
        section = extract_markdown_section(body_text, section_selector)
        if section is None:
            return str(body_path) + section_selector, None, "candidate_body_section_not_found"
        return str(body_path) + section_selector, section, None

    return str(body_path), body_text, None


def validation_codes(record_path: Path) -> dict[str, Any]:
    text = record_path.read_text(encoding="utf-8")
    frontmatter, record_body = parse_frontmatter(text)
    body_ref, body_text, body_error = resolve_body_text(
        record_path, record_body, frontmatter.get("candidate_body_location")
    )

    codes: list[str] = []
    warnings: list[str] = []

    review_status = str(frontmatter.get("review_status") or "draft")
    review_object_state = str(frontmatter.get("review_object_state") or "")
    writeback_ready = bool(frontmatter.get("writeback_ready"))
    body_hash = frontmatter.get("body_hash")
    approval = frontmatter.get("approval_integrity")
    checked_body_hash = None
    if isinstance(approval, dict):
        checked_body_hash = approval.get("checked_body_hash")

    requires_hash = (
        writeback_ready
        or review_status in VALID_STATUS_REQUIRING_HASH
        or review_object_state in VALID_REVIEW_OBJECT_STATES_REQUIRING_HASH
    )
    if requires_hash and not body_hash:
        codes.append("fixed_or_approved_missing_body_hash")

    computed_hash = None
    if body_error:
        codes.append(body_error)
    else:
        computed_hash = sha256_body(body_text or "")

    if computed_hash and body_hash and str(body_hash) != computed_hash:
        if writeback_ready:
            codes.append("writeback_ready_body_changed")
        else:
            codes.append("body_hash_mismatch")

    if computed_hash and checked_body_hash and str(checked_body_hash) != computed_hash:
        codes.append("checked_body_hash_mismatch")

    if not requires_hash and not body_hash:
        warnings.append("body_hash_not_required_for_draft")

    return {
        "record": str(record_path),
        "candidate_body_location": body_ref,
        "computed_body_hash": computed_hash,
        "valid": not codes,
        "codes": codes,
        "warnings": warnings,
        "authority_boundary": {
            "validator_pass_is_not_reviewer_approval": True,
            "validator_pass_is_not_reviewed_knowledge": True,
            "validator_pass_is_not_action_basis": True,
            "sandbox_not_mainline": True,
        },
    }


def main(argv: list[str]) -> int:
    parser = argparse.ArgumentParser(
        description="Validate sandbox review candidate body hash records."
    )
    parser.add_argument("records", nargs="+", help="Review candidate fixture records.")
    parser.add_argument(
        "--json", action="store_true", help="Emit JSON lines instead of text lines."
    )
    args = parser.parse_args(argv)

    any_invalid = False
    for raw_record in args.records:
        result = validation_codes(Path(raw_record).resolve())
        any_invalid = any_invalid or not result["valid"]
        if args.json:
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        elif result["valid"]:
            print(f"PASS {result['record']} body_hash={result['computed_body_hash']}")
        else:
            print(f"FAIL {result['record']} codes={','.join(result['codes'])}")

    return 1 if any_invalid else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
