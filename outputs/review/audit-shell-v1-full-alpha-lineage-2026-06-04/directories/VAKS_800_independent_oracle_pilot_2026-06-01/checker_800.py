import argparse
import hashlib
import json
import re
from collections import defaultdict
from pathlib import Path


ROOT = Path(__file__).resolve().parent
ANCHOR_PROBLEMS = {"missing", "stale", "drift", "moved"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def parse_line(text, prefix):
    for line in text.splitlines():
        if line.startswith(prefix):
            return line
    return ""


def parse_state(text):
    line = parse_line(text, "state: ")
    return line.split(": ", 1)[1].strip() if line else "missing"


def parse_kv(line):
    result = {}
    quote_match = re.search(r"quote=(\".*\")$", line)
    if quote_match:
        try:
            result["quote"] = json.loads(quote_match.group(1))
        except Exception:
            result["quote"] = ""
        line = line[: quote_match.start()].strip()
    for item in line.split():
        if "=" in item:
            key, value = item.split("=", 1)
            result[key] = value
    return result


def rel(path):
    return ROOT / path


def sha_text(text):
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def has_full(text):
    return "FULL_AUDIT_OPEN" in text


def has_review_due(text):
    return "review_due: true" in text


def has_queue(text):
    return "queue: unresolved_gate" in text


def parse_group(text):
    match = re.search(r"group_id:\s*([^;\n]+)", text)
    return match.group(1).strip() if match else ""


def resolve_source_pointer(text, expected_valid):
    if not expected_valid:
        return True
    triad = parse_line(text, "pointer_triad: ")
    if triad:
        data = parse_kv(
            triad.replace("source_path=", "path=")
            .replace("source_hash=", "hash=")
            .replace("source_version=", "version=")
        )
        path = rel(data.get("path", ""))
        if not path.exists():
            return False
        body = path.read_text(encoding="utf-8", errors="ignore")
        if data.get("hash") and sha_text(body) != data["hash"]:
            return False
        try:
            start = int(data.get("start", "-1"))
            end = int(data.get("end", "-1"))
        except ValueError:
            return False
        quote = data.get("quote", "")
        return start >= 0 and end >= start and body[start:end] == quote
    line = parse_line(text, "source_pointer: ")
    if not line:
        line = parse_line(text, "source_anchor: ")
    if not line:
        return False
    data = parse_kv(line)
    path = rel(data.get("path", ""))
    if not path.exists():
        return False
    body = path.read_text(encoding="utf-8", errors="ignore")
    if data.get("hash") and sha_text(body) != data["hash"]:
        return False
    try:
        start = int(data.get("start", "-1"))
        end = int(data.get("end", "-1"))
    except ValueError:
        return False
    quote = data.get("quote", "")
    if start < 0 or end < start or body[start:end] != quote:
        return False
    return True


def resolve_record(text):
    triad = parse_line(text, "pointer_triad: ")
    if triad:
        data = parse_kv(triad.replace("record_path=", "path="))
        return rel(data.get("path", "")).exists()
    line = parse_line(text, "record_pointer: ")
    data = parse_kv(line)
    return bool(line and rel(data.get("path", "")).exists())


def resolve_evidence(text):
    triad = parse_line(text, "pointer_triad: ")
    if triad:
        data = parse_kv(triad.replace("evidence_path=", "path=").replace("evidence_marker=", "marker="))
        path = rel(data.get("path", ""))
        return bool(path.exists() and data.get("marker", "") in path.read_text(encoding="utf-8", errors="ignore"))
    line = parse_line(text, "evidence_pointer: ")
    data = parse_kv(line)
    path = rel(data.get("path", ""))
    return bool(line and path.exists() and data.get("marker", "") in path.read_text(encoding="utf-8", errors="ignore"))


def anchor_problem_visible(text, required, status):
    if not required:
        return True
    return f"anchor_health: {status}" in text and "anchor_problem_visibility:" in text


def authority_leaks(text, rules):
    lower = "\n".join(
        line
        for line in text.lower().splitlines()
        if not line.startswith("authority_boundary:") and "no truth change" not in line and "no support strength" not in line
    )
    return any(re.search(pattern, lower) for pattern in rules["leakage_patterns"])


def authority_boundary_ok(text, required, rules):
    if not required:
        return True
    lower = text.lower()
    return any(token in lower for token in rules["boundary_tokens"])


def front_metrics(artifact):
    lines = artifact["front"]
    front = "\n".join(lines)
    lengths = [len(line) for line in lines]
    return {
        "front_lines": len(lines),
        "front_chars": len(front),
        "max_front_line_chars": max(lengths) if lengths else 0,
        "front_line_violation": len(lines) > 6,
    }


def check_one(artifact, gold, rules):
    cid = artifact["case_id"]
    expected = gold[cid]
    text = artifact["rendered_text"]
    observed_state = parse_state(text)
    group_id = parse_group(text)
    source_ok = resolve_source_pointer(text, expected["valid_anchor_expected"])
    record_ok = resolve_record(text)
    evidence_ok = resolve_evidence(text)
    row = {
        "case_id": cid,
        "pool": expected["pool"],
        "layer": expected["layer"],
        "dataset_family": expected["dataset_family"],
        "expected_state": expected["state"],
        "observed_state": observed_state,
        "state_ok": observed_state == expected["state"],
        "full_audit": has_full(text),
        "false_lite": expected["full_audit"] and not has_full(text),
        "ordinary_false_positive": expected["ordinary"] and has_full(text),
        "review_due_fn": expected["review_due"] and not has_review_due(text),
        "queue_fn": expected["queue_visible"] and not has_queue(text),
        "source_anchor_ok": source_ok,
        "anchor_problem_visibility_ok": anchor_problem_visible(text, expected["anchor_problem_visibility_required"], expected["anchor_status"]),
        "record_pointer_ok": record_ok,
        "evidence_pointer_ok": evidence_ok,
        "authority_leakage": authority_leaks(text, rules),
        "authority_boundary_ok": authority_boundary_ok(text, expected["authority_boundary_required"], rules),
        "group_id": group_id,
        "gold_group_id": expected["gold_group_id"],
        "can_group": expected["can_group"],
        "must_not_group": expected["must_not_group"],
        "serious": expected["serious"],
        "ordinary": expected["ordinary"],
        "resolved": expected["resolved"],
        "serious_folded": expected["serious"] and bool(group_id),
        "rendered_lines": len(artifact["front"]) + len(artifact["back"]) + len(artifact["full"]),
        "rendered_chars": len(text),
        **front_metrics(artifact),
    }
    return row


def grouping(rows):
    predicted = defaultdict(list)
    expected = defaultdict(list)
    for row in rows:
        if row["group_id"]:
            predicted[row["group_id"]].append(row)
        if row["gold_group_id"]:
            expected[row["gold_group_id"]].append(row)

    severe = []
    for gid, members in predicted.items():
        gold_ids = {m["gold_group_id"] for m in members if m["gold_group_id"]}
        if any(m["must_not_group"] or m["serious"] for m in members) or len(gold_ids) > 1:
            severe.append({"group_id": gid, "members": [m["case_id"] for m in members], "gold_group_ids": sorted(gold_ids), "has_serious": any(m["serious"] for m in members)})

    expected_multi = {gid: members for gid, members in expected.items() if len(members) > 1}
    recalled = 0
    for gid, members in expected_multi.items():
        observed_ids = {m["case_id"] for m in members}
        candidate_sets = defaultdict(set)
        for row in members:
            if row["group_id"]:
                candidate_sets[row["group_id"]].add(row["case_id"])
        if any(ids == observed_ids for ids in candidate_sets.values()):
            recalled += 1
    grouped_members = sum(len(m) for m in predicted.values() if len(m) > 1)
    group_count = sum(1 for m in predicted.values() if len(m) > 1)
    return {
        "expected_multi_groups": len(expected_multi),
        "recalled_multi_groups": recalled,
        "grouping_recall": round(recalled / len(expected_multi), 4) if expected_multi else 1.0,
        "predicted_grouped_members": grouped_members,
        "grouped_reduction_pct": round((1 - group_count / grouped_members) * 100, 1) if grouped_members else 0.0,
        "severe_over_grouping": severe,
        "serious_folded_count": sum(1 for r in rows if r["serious_folded"]),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts", required=True)
    parser.add_argument("--gold", required=True)
    parser.add_argument("--rules", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    artifacts = read_json(args.artifacts)
    gold = read_json(args.gold)
    rules = read_json(args.rules)
    rows = [check_one(artifact, gold, rules) for artifact in artifacts]
    Path(args.out).write_text(json.dumps({"checks": rows, "grouping": grouping(rows)}, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"checked {len(rows)} -> {args.out}")


if __name__ == "__main__":
    main()
