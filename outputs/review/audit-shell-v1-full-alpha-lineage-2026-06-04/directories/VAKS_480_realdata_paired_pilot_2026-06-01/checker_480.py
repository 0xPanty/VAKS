import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ANCHOR_PROBLEMS = {"missing", "stale", "drift", "moved"}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def parse_line(text, prefix):
    for line in text.splitlines():
        if line.startswith(prefix):
            return line
    return ""


def parse_state(text):
    line = parse_line(text, "state: ")
    return line.split(": ", 1)[1].strip() if line else "missing"


def has_full_audit(text):
    return "FULL_AUDIT_OPEN" in text


def has_review_due(text):
    return "review_due: true" in text


def has_queue(text):
    return "queue: unresolved_gate" in text or "queue: baseline_all_visible" in text


def parse_key_values(line):
    result = {}
    for item in line.split():
        if "=" in item:
            key, value = item.split("=", 1)
            result[key.strip()] = value.strip()
    return result


def resolve_path(rel_path):
    return ROOT / rel_path


def source_anchor_ok(text, expected_status):
    if expected_status != "valid":
        return True
    line = parse_line(text, "source_anchor: ")
    if not line:
        line = parse_line(text, "sparse_provenance_pointer: source ")
    if not line:
        line = parse_line(text, "anchor_health: valid ")
    values = parse_key_values(line)
    path = resolve_path(values.get("path", ""))
    marker = values.get("marker", "")
    return path.exists() and marker in path.read_text(encoding="utf-8", errors="ignore")


def anchor_problem_visible(text, expected_status):
    if expected_status not in ANCHOR_PROBLEMS:
        return True
    return (
        f"anchor_health: {expected_status}" in text
        and "anchor_problem_visibility:" in text
        and expected_status in text
    )


def pointer_ok(text, prefix, marker_prefix=None):
    line = parse_line(text, prefix)
    if not line:
        return False
    values = parse_key_values(line)
    path = resolve_path(values.get("path", ""))
    if not path.exists():
        return False
    if marker_prefix:
        marker = values.get("marker", "")
        return marker and marker in path.read_text(encoding="utf-8", errors="ignore")
    return True


def authority_leaks(text, rules):
    lower = text.lower()
    return any(re.search(pattern, lower) for pattern in rules["leakage_patterns"])


def authority_boundary_ok(text, required, rules):
    if not required:
        return True
    lower = text.lower()
    return any(token in lower for token in rules["boundary_tokens"])


def parse_group_id(text):
    line = parse_line(text, "group_id: ")
    return line.split(": ", 1)[1].strip() if line else ""


def front_metrics(artifact):
    front = artifact["front"]
    front_text = "\n".join(front)
    line_chars = [len(line) for line in front]
    return {
        "front_lines": len(front),
        "front_chars": len(front_text),
        "max_front_line_chars": max(line_chars) if line_chars else 0,
        "front_budget_warning": len(front) > 10 or len(front_text) > 1400 or (max(line_chars) if line_chars else 0) > 260,
    }


def check_artifact(artifact, gold, rules):
    cid = artifact["case_id"]
    expected = gold[cid]
    text = artifact["rendered_text"]
    observed_state = parse_state(text)
    group_id = parse_group_id(text)
    metrics = front_metrics(artifact)
    record_ok = pointer_ok(text, "record_pointer: ")
    evidence_ok = pointer_ok(text, "evidence_pointer: ", marker_prefix="EVIDENCE_")
    row = {
        "case_id": cid,
        "dataset_family": expected["dataset_family"],
        "observed_state": observed_state,
        "expected_state": expected["state"],
        "state_ok": observed_state == expected["state"],
        "full_audit": has_full_audit(text),
        "false_lite": expected["full_audit"] and not has_full_audit(text),
        "review_due_fn": expected["review_due"] and not has_review_due(text),
        "queue_fn": expected["queue_visible"] and not has_queue(text),
        "source_anchor_ok": source_anchor_ok(text, expected["anchor_status"]),
        "anchor_problem_visibility_ok": anchor_problem_visible(text, expected["anchor_status"]),
        "record_pointer_ok": record_ok,
        "evidence_pointer_ok": evidence_ok,
        "authority_leakage": authority_leaks(text, rules),
        "authority_boundary_ok": authority_boundary_ok(text, expected["authority_boundary_required"], rules),
        "group_id": group_id,
        "gold_group_id": expected["gold_group_id"],
        "can_group": expected["can_group"],
        "must_not_group": expected["must_not_group"],
        "serious_folded": (expected["full_audit"] or expected["queue_visible"]) and bool(group_id),
        **metrics,
        "rendered_lines": len(artifact["front"]) + len(artifact["back"]) + len(artifact["full"]),
        "rendered_chars": len(text),
        "front_line_chars": [len(line) for line in artifact["front"]],
    }
    return row


def grouping_summary(rows):
    predicted = defaultdict(list)
    expected = defaultdict(list)
    for row in rows:
        if row["group_id"]:
            predicted[row["group_id"]].append(row)
        if row["gold_group_id"]:
            expected[row["gold_group_id"]].append(row)

    severe = []
    for gid, members in predicted.items():
        gold_ids = {member["gold_group_id"] for member in members if member["gold_group_id"]}
        has_must_not = any(member["must_not_group"] for member in members)
        if len(members) > 1 and (has_must_not or len(gold_ids) > 1):
            severe.append(
                {
                    "group_id": gid,
                    "members": [member["case_id"] for member in members],
                    "gold_group_ids": sorted(gold_ids),
                    "has_must_not_group": has_must_not,
                }
            )

    expected_multi = {gid: members for gid, members in expected.items() if len(members) > 1}
    recalled = 0
    for gid, members in expected_multi.items():
        predicted_sets = defaultdict(set)
        for member in members:
            observed = next(row for row in rows if row["case_id"] == member["case_id"])
            if observed["group_id"]:
                predicted_sets[observed["group_id"]].add(member["case_id"])
        if any(len(case_ids) == len(members) for case_ids in predicted_sets.values()):
            recalled += 1

    predicted_grouped_members = sum(len(members) for members in predicted.values() if len(members) > 1)
    expected_groupable_members = sum(len(members) for members in expected_multi.values())
    return {
        "expected_multi_groups": len(expected_multi),
        "recalled_multi_groups": recalled,
        "grouping_recall": round(recalled / len(expected_multi), 4) if expected_multi else 1.0,
        "predicted_grouped_members": predicted_grouped_members,
        "expected_groupable_members": expected_groupable_members,
        "grouped_reduction_pct": round((1 - len([gid for gid, members in predicted.items() if len(members) > 1]) / predicted_grouped_members) * 100, 1) if predicted_grouped_members else 0.0,
        "severe_over_grouping": severe,
        "serious_folded_count": sum(1 for row in rows if row["serious_folded"]),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts", required=True)
    parser.add_argument("--gold", required=True)
    parser.add_argument("--authority-rules", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    artifacts = load_json(args.artifacts)
    gold = load_json(args.gold)
    rules = load_json(args.authority_rules)
    rows = [check_artifact(artifact, gold, rules) for artifact in artifacts]
    payload = {"checks": rows, "grouping": grouping_summary(rows)}
    Path(args.out).write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"checked {len(rows)} artifacts -> {args.out}")


if __name__ == "__main__":
    main()
