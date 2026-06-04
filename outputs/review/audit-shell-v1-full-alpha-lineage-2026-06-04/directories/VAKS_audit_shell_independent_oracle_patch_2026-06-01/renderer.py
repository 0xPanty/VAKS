import argparse
import json
from pathlib import Path


HARD_BLOCKING = {
    "action_basis",
    "promotion",
    "conflict",
    "missing_anchor",
    "high_severity_wrong_answer",
    "reviewer_blocks",
}

HARD_REVIEW = {
    "known_omission",
    "stale_pointer",
    "selector_drift",
    "moved_pointer",
    "action_outcome",
    "decision_outcome",
}

ANCHOR_PROBLEMS = {"missing", "stale", "drift", "moved"}


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def state_for(case, variant):
    if variant == "control_leaky":
        return case.get("surface_state", "ordinary")
    signals = set(case.get("signals", []))
    if "regression" in signals:
        return "regressed"
    if signals & HARD_BLOCKING:
        return "blocking"
    if signals & HARD_REVIEW:
        return "for_review"
    if case.get("surface_state") in {"resolved_folded", "parked_nonblocking"}:
        return case["surface_state"]
    return "ordinary"


def full_audit_for(case, state, variant):
    if variant == "baseline_full":
        return True
    if variant == "control_leaky":
        return state in {"blocking", "for_review", "regressed"}
    return state in {"blocking", "for_review", "regressed"} or case.get("anchor_status") in ANCHOR_PROBLEMS


def anchor_front(case, anchors):
    status = case.get("anchor_status", "valid")
    key = case.get("anchor_key", "")
    if status == "valid":
        meta = anchors.get(key, {})
        return f"anchor_health: valid key={key} path={meta.get('path')} marker={meta.get('marker')}"
    return f"anchor_health: {status} key={key} problem visible"


def boundary_for(case):
    family = case.get("authority_family")
    if not family:
        return ""
    if "independence" in family:
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


def group_id_for(case, variant, full_audit):
    if full_audit or not case.get("recurrence_key"):
        return ""
    parts = [
        case.get("recurrence_key", ""),
        case.get("action_meaning", ""),
        case.get("feedback_type", ""),
        case.get("gap_family", ""),
        case.get("anchor_status", ""),
    ]
    if variant == "candidate_with_version":
        parts.insert(0, case.get("fingerprint_version", "v1"))
    return "|".join(parts)


def render_case(case, anchors, variant):
    state = state_for(case, variant)
    full_audit = full_audit_for(case, state, variant)
    review_due = full_audit and state in {"blocking", "for_review", "regressed"}
    queue_visible = state in {"blocking", "for_review", "regressed"} or case.get("anchor_status") in ANCHOR_PROBLEMS

    front = [
        f"case: {case['id']}",
        f"state: {state}",
        f"summary: {case['summary']}",
        anchor_front(case, anchors),
    ]

    if variant == "control_leaky":
        front.append(f"signal: {case.get('signal_text', '')}")
    else:
        boundary = boundary_for(case)
        if boundary:
            front.append(boundary)

    if full_audit:
        front.append("upgrade: hard trigger or anchor problem")
    if review_due:
        front.append("review_due: true")
    if queue_visible:
        front.append("queue: unresolved_gate")

    group_id = group_id_for(case, variant, full_audit)
    if group_id:
        front.append(f"group_id: {group_id}")
        front.append("recurrence_digest: latest + unresolved exemplar + count + last_seen")
        if variant == "candidate_with_version":
            front.append(f"fingerprint_version: {case.get('fingerprint_version', 'v1')}")

    if case.get("object_type") == "feedback" and variant != "control_leaky":
        front.append(f"feedback_revision: type={case.get('feedback_type', 'note')} no truth change no numeric delta")

    front = compact_front(front)

    back = [f"full_record_pointer: record://{case['id']}"]
    if case.get("anchor_status") == "valid":
        back.append("sparse_provenance: anchor pointer only; detail available in full record")
    else:
        back.append(f"anchor_problem_visibility: {case.get('anchor_status')} shown on front")

    full = []
    if full_audit:
        full.extend([
            "FULL_AUDIT_OPEN",
            "deep_packet_retained: true",
            f"evidence_packet_pointer: evidence://{case['id']}",
        ])

    return {
        "case_id": case["id"],
        "variant": variant,
        "front": front,
        "back": back,
        "full": full,
        "rendered_text": "\n".join(front + back + full),
    }


def compact_front(lines):
    priority = []
    rest = []
    for line in lines:
        if line.startswith(("case:", "state:", "summary:", "anchor_health:")):
            priority.append(line)
        else:
            rest.append(line)
    if rest:
        priority.append("flags: " + " ; ".join(rest))
    return priority


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True)
    parser.add_argument("--anchors", required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    cases = load_json(args.cases)
    anchors = load_json(args.anchors)
    artifacts = [render_case(case, anchors, args.variant) for case in cases]
    Path(args.out).write_text(json.dumps(artifacts, ensure_ascii=False, indent=2), encoding="utf-8")


if __name__ == "__main__":
    main()
