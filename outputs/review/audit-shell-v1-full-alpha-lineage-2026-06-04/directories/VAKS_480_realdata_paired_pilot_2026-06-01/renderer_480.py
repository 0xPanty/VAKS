import argparse
import json
import re
from pathlib import Path


ANCHOR_PROBLEMS = {"missing", "stale", "drift", "moved"}
BLOCKING_SIGNALS = {"action_basis", "promotion", "conflict", "missing_anchor", "explicit_challenge", "high_severity_wrong_answer"}
REVIEW_SIGNALS = {"known_omission", "stale_pointer", "selector_drift", "moved_pointer", "action_outcome", "decision_outcome"}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def one_line(text, limit=180):
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    return text[: limit - 3] + "..." if len(text) > limit else text


def state_for(case):
    signals = set(case.get("signals", []))
    if "regression" in signals:
        return "regressed"
    if signals & BLOCKING_SIGNALS:
        return "blocking"
    if signals & REVIEW_SIGNALS:
        return "for_review"
    if case.get("anchor_status") == "missing":
        return "blocking"
    if case.get("anchor_status") in {"stale", "drift", "moved"}:
        return "for_review"
    if case.get("surface_state") in {"resolved_folded", "parked_nonblocking"}:
        return case["surface_state"]
    return "ordinary"


def full_audit_for(case, variant, state):
    if variant == "baseline_full":
        return True
    return state in {"blocking", "for_review", "regressed"} or case.get("anchor_status") in ANCHOR_PROBLEMS


def tier_for(case, state, full_audit):
    if full_audit:
        if case.get("anchor_status") in ANCHOR_PROBLEMS:
            return "tier: deep_packet anchor_repair"
        return "tier: deep_packet hard_trigger"
    if state == "resolved_folded":
        return "tier: metadata_stub resolved_folded"
    return "tier: metadata_stub ordinary"


def authority_boundary(case):
    family = case.get("authority_family")
    if not family:
        return ""
    if family in {"lineage_as_independence", "source_count_as_independence"}:
        return f"authority_boundary: {family} is not independence proof"
    if family == "feedback_as_truth":
        return "authority_boundary: feedback is no truth change"
    if family in {"dashboard_as_truth", "test_pass_as_truth"}:
        return f"authority_boundary: {family} is diagnostic only"
    if family == "retrieval_rank_as_trust":
        return "authority_boundary: retrieval rank is routing only"
    if family == "cluster_summary_as_reviewed_relation":
        return "authority_boundary: cluster summary is not reviewed relation"
    if family == "llm_summary_as_support":
        return "authority_boundary: model summary is not evidence support"
    return f"authority_boundary: {family} is not truth authority"


def anchor_line(case):
    anchor = case["source_anchor"]
    status = case.get("anchor_status", "valid")
    return f"anchor_health: {status} path={anchor['path']} marker={anchor['marker']}"


def pointer_lines(case, sparse):
    source = case["source_anchor"]
    lines = [
        f"record_pointer: record://{case['id']} path={case['record_path']}",
        f"evidence_pointer: evidence://{case['id']} path={case['evidence_path']} marker=EVIDENCE_{source['marker']}",
    ]
    if sparse:
        lines.append(f"sparse_provenance_pointer: source path={source['path']} marker={source['marker']}")
    else:
        lines.extend(
            [
                f"source_anchor: status={source['status']} path={source['path']} marker={source['marker']}",
                f"source_label: {one_line(case.get('source_label'), 120)}",
                f"evidence_excerpt: {one_line(case.get('evidence'), 260)}",
            ]
        )
    return lines


def can_group(case, full_audit, state, variant):
    if variant not in {"shell_core_plus_recurrence", "shell_core_plus_unversioned_control"}:
        return False
    return (
        not full_audit
        and state == "ordinary"
        and case.get("surface_state") == "ordinary"
        and case.get("anchor_status") == "valid"
        and bool(case.get("recurrence_key"))
    )


def group_id(case, variant):
    parts = [
        case.get("recurrence_key", ""),
        case.get("action_meaning", ""),
        case.get("feedback_type", ""),
        case.get("gap_family", ""),
        case.get("anchor_status", ""),
    ]
    if variant == "shell_core_plus_recurrence":
        parts.insert(0, case.get("fingerprint_version", "fp-v1"))
    return "|".join(parts)


def render_case(case, variant, group_meta=None):
    group_meta = group_meta or {}
    state = state_for(case)
    full_audit = full_audit_for(case, variant, state)
    review_due = state in {"blocking", "for_review", "regressed"}
    queue_visible = review_due or case.get("anchor_status") in ANCHOR_PROBLEMS
    group_visible = can_group(case, full_audit, state, variant)
    gid = group_id(case, variant) if group_visible else ""
    group = group_meta.get(gid, {}) if gid else {}
    folded_member = bool(group_visible and group.get("exemplar") and group.get("exemplar") != case["id"])

    if variant == "baseline_full":
        front = [
            f"case: {case['id']}",
            f"dataset: {case['dataset_family']}",
            f"state: {state}",
            f"claim: {one_line(case['claim'], 260)}",
            f"authority_note: {case.get('authority_trap')}" if case.get("authority_trap") else "authority_note: none",
            f"anchor_health: {case.get('anchor_status')} path={case['source_anchor']['path']} marker={case['source_anchor']['marker']}",
            "queue: baseline_all_visible",
        ]
        back = pointer_lines(case, sparse=False)
    elif folded_member:
        front = [
            f"case: {case['id']}",
            f"dataset: {case['dataset_family']}",
            f"state: {state}",
            f"visibility: folded_member exemplar={group['exemplar']} count={group.get('count', 1)}",
            anchor_line(case),
            f"group_id: {gid}",
        ]
        back = pointer_lines(case, sparse=True)
    else:
        front = [
            f"case: {case['id']}",
            f"dataset: {case['dataset_family']}",
            f"state: {state}",
            f"claim: {one_line(case['claim'], 190)}",
            tier_for(case, state, full_audit),
            anchor_line(case),
        ]
        boundary = authority_boundary(case)
        if boundary:
            front.append(boundary)
        if review_due:
            front.append("review_due: true")
        if queue_visible:
            front.append("queue: unresolved_gate")
        if case.get("anchor_status") in ANCHOR_PROBLEMS:
            front.append(f"anchor_problem_visibility: {case.get('anchor_status')} visible")
        if case.get("object_type") == "feedback":
            front.append(f"feedback_revision: type={case.get('feedback_type', 'note')} categorical no truth change no numeric delta")
        if group_visible:
            front.append(f"group_id: {gid}")
            count = group.get("count", 1)
            front.append(f"recurrence_card: exemplar={case['id']} count={count} last_seen=pilot open_only=true")
        back = pointer_lines(case, sparse=True)

    full = []
    if full_audit:
        full.extend(
            [
                "FULL_AUDIT_OPEN",
                "deep_packet_retained: true",
                f"signals: {','.join(case.get('signals', [])) or 'none'}",
                f"source_anchor: status={case['source_anchor']['status']} path={case['source_anchor']['path']} marker={case['source_anchor']['marker']}",
                f"source_label: {one_line(case.get('source_label'), 160)}",
                f"evidence_excerpt: {one_line(case.get('evidence'), 600)}",
            ]
        )
    return {
        "case_id": case["id"],
        "variant": variant,
        "front": front,
        "back": back,
        "full": full,
        "rendered_text": "\n".join(front + back + full),
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    cases = load_json(args.cases)
    group_meta = build_group_meta(cases, args.variant)
    artifacts = [render_case(case, args.variant, group_meta) for case in cases]
    Path(args.out).write_text(json.dumps(artifacts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{args.variant}: {len(artifacts)} artifacts")


def build_group_meta(cases, variant):
    meta = {}
    if variant not in {"shell_core_plus_recurrence", "shell_core_plus_unversioned_control"}:
        return meta
    for case in cases:
        state = state_for(case)
        full_audit = full_audit_for(case, variant, state)
        if not can_group(case, full_audit, state, variant):
            continue
        gid = group_id(case, variant)
        group = meta.setdefault(gid, {"exemplar": case["id"], "members": []})
        group["members"].append(case["id"])
    for group in meta.values():
        group["count"] = len(group["members"])
    return meta


if __name__ == "__main__":
    main()
