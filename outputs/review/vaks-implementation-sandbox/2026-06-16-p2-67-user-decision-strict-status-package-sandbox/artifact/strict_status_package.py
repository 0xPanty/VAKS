from __future__ import annotations


def parse_strict_frontmatter_status(text: str) -> dict:
    lines = text.splitlines()
    errors: list[str] = []
    if not lines or lines[0].strip() != "---":
        return {
            "valid": False,
            "status": None,
            "errors": ["missing_opening_frontmatter_delimiter"],
            "body_status_mentions": [],
        }
    closing_index = None
    for index in range(1, len(lines)):
        if lines[index].strip() == "---":
            closing_index = index
            break
    if closing_index is None:
        return {
            "valid": False,
            "status": None,
            "errors": ["missing_closing_frontmatter_delimiter"],
            "body_status_mentions": [],
        }
    frontmatter = lines[1:closing_index]
    body = lines[closing_index + 1 :]
    values: list[str] = []
    for line in frontmatter:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        if key.strip() == "status":
            values.append(value.strip())
    if not values:
        errors.append("missing_status_in_frontmatter")
    if len(values) > 1:
        errors.append("duplicate_status_in_frontmatter")
    if len(values) == 1 and not values[0]:
        errors.append("empty_status_in_frontmatter")
    body_status_mentions = [
        closing_index + 2 + offset
        for offset, line in enumerate(body)
        if line.strip().lower().startswith("status:")
    ]
    return {
        "valid": not errors,
        "status": values[0] if len(values) == 1 and values[0] else None,
        "errors": errors,
        "body_status_mentions": body_status_mentions,
    }


def status_matches(text: str, expected_status: str) -> bool:
    parsed = parse_strict_frontmatter_status(text)
    return parsed["valid"] is True and parsed["status"] == expected_status
