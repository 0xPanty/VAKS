import argparse
import json
import re
from collections import defaultdict
from pathlib import Path


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


def full_audit(text):
    return "FULL_AUDIT_OPEN" in text


def review_due(text):
    return "review_due: true" in text


def queue_visible(text):
    return "queue: unresolved_gate" in text


def parse_group(text):
    match = re.search(r"group_id:\s*([^\n;]+)", text)
    return match.group(1).strip() if match else ""


def parse_anchor_health(text):
    line = parse_line(text, "anchor_health: ")
    if not line:
        return {"status": "missing_line"}
    parts = line.split()
    status = parts[1]
    result = {"status": status}
    for part in parts[2:]:
        if "=" in part:
            key, value = part.split("=", 1)
            result[key] = value
    return result


def anchor_resolves(anchor, root):
    if anchor.get("status") != "valid":
        return False
    path = root / anchor.get("path", "")
    if not path.exists():
        return False
    return anchor.get("marker", "") in path.read_text(encoding="utf-8")


def has_anchor_problem_visibility(text):
    return "anchor_problem_visibility:" in text or re.search(r"anchor_health:\s+(missing|stale|drift|moved).*problem visible", text) is not None


def authority_leaks(text, rules):
    lower = text.lower()
    return any(re.search(pattern, lower) for pattern in rules["leakage_patterns"])


def authority_boundary_visible(text, rules):
    lower = text.lower()
    return any(token in lower for token in rules["boundary_tokens"])


def check_case(artifact, gold, rules, root):
    text = artifact["rendered_text"]
    anchor = parse_anchor_health(text)
    anchor_ok = True
    if gold["anchor_health"] == "valid":
        anchor_ok = anchor_resolves(anchor, root)
    else:
        anchor_ok = has_anchor_problem_visibility(text)
    leak = authority_leaks(text, rules)
    boundary_ok = (not gold.get("authority_boundary_required")) or (authority_boundary_visible(text, rules) and not leak)
    front_ok = len(artifact["front"]) <= 6
    return {
        "case_id": artifact["case_id"],
        "state_ok": parse_state(text) == gold["state"],
        "false_lite": gold["full_audit"] and not full_audit(text),
        "ordinary_false_positive": (not gold["full_audit"]) and full_audit(text),
        "review_due_fn": gold["review_due"] and not review_due(text),
        "review_due_fp": (not gold["review_due"]) and review_due(text),
        "anchor_ok": anchor_ok,
        "anchor_problem_visibility_ok": (not gold.get("anchor_problem_visibility")) or has_anchor_problem_visibility(text),
        "authority_leakage": leak,
        "authority_boundary_ok": boundary_ok,
        "queue_ok": queue_visible(text) == gold.get("queue_visible", False),
        "front_ok": front_ok,
        "front_lines": len(artifact["front"]),
        "rendered_lines": len(artifact["front"]) + len(artifact["back"]) + len(artifact["full"]),
        "group_id": parse_group(text),
    }


def evaluate_groups(rows, gold):
    groups = defaultdict(list)
    for row in rows:
        if row["group_id"]:
            groups[row["group_id"]].append(row["case_id"])
    severe = []
    grouped_gold_members = set()
    for group_id, ids in groups.items():
        if len(ids) <= 1:
            continue
        expected = {gold[i].get("group_id", "") for i in ids}
        can_group = all(gold[i].get("can_group", False) for i in ids)
        if (not can_group) or len(expected) != 1 or "" in expected:
            severe.append({"group_id": group_id, "case_ids": ids, "expected_group_ids": sorted(expected)})
        else:
            grouped_gold_members.update(ids)
    gold_groupable = [cid for cid, item in gold.items() if item.get("can_group", False)]
    recall = len(grouped_gold_members) / len(gold_groupable) if gold_groupable else 1.0
    grouped_count = sum(len(ids) for ids in groups.values() if len(ids) > 1)
    group_cards = sum(1 for ids in groups.values() if len(ids) > 1)
    reduction = ((grouped_count - group_cards) / grouped_count * 100) if grouped_count else 0.0
    return {
        "groups": dict(groups),
        "severe_over_grouping": severe,
        "grouping_recall": round(recall, 4),
        "grouped_reduction_pct": round(reduction, 1),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts", required=True)
    parser.add_argument("--gold", required=True)
    parser.add_argument("--rules", required=True)
    parser.add_argument("--root", default=".")
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    artifacts = load_json(args.artifacts)
    gold = load_json(args.gold)
    rules = load_json(args.rules)
    root = Path(args.root)
    rows = [check_case(artifact, gold[artifact["case_id"]], rules, root) for artifact in artifacts]
    groups = evaluate_groups(rows, gold)
    Path(args.out).write_text(json.dumps({"checks": rows, "grouping": groups}, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
