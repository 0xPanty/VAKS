import argparse
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BLOCKING = {"action_basis", "promotion", "explicit_challenge", "conflict", "missing_anchor", "high_severity_wrong_answer"}
REVIEW = {"known_omission", "insufficient_evidence", "ambiguous_scope", "stale_pointer", "selector_drift", "moved_pointer", "action_outcome", "decision_outcome"}
ANCHOR_PROBLEMS = {"missing", "stale", "drift", "moved"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def compact(text, limit):
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    return text[: limit - 3] + "..." if len(text) > limit else text


def state_for(case, variant):
    if variant == "leaky_or_unversioned_control":
        return case.get("surface_state", "ordinary")
    signals = set(case.get("signals", []))
    if "regression" in signals:
        return "regressed"
    if signals & BLOCKING:
        return "blocking"
    if signals & REVIEW:
        return "for_review"
    if case.get("anchor_status") == "missing":
        return "blocking"
    if case.get("anchor_status") in ANCHOR_PROBLEMS:
        return "for_review"
    if case.get("surface_state") in {"resolved_folded", "parked_nonblocking"}:
        return case["surface_state"]
    return "ordinary"


def full_audit_for(case, variant, state):
    if variant == "baseline_full":
        return True
    if variant == "leaky_or_unversioned_control":
        return state in {"blocking", "for_review", "regressed"}
    return state in {"blocking", "for_review", "regressed"} or case.get("anchor_status") in ANCHOR_PROBLEMS


def boundary(case):
    family = case.get("authority_family")
    if not family:
        return ""
    if "independence" in family or family == "source_count_as_independence":
        return f"authority_boundary: {family} is not independence proof"
    if family in {"dashboard_as_truth", "test_pass_as_truth", "approval_as_truth"}:
        return f"authority_boundary: {family} is diagnostic only"
    if family == "feedback_as_truth":
        return "authority_boundary: feedback is no truth change"
    if family == "retrieval_rank_as_trust":
        return "authority_boundary: retrieval rank is routing only"
    if family == "group_count_as_support":
        return "authority_boundary: group count is triage only and no support strength"
    if family == "llm_summary_as_support":
        return "authority_boundary: model summary is not evidence support"
    if family == "cluster_summary_as_reviewed_relation":
        return "authority_boundary: cluster summary is not reviewed relation"
    return f"authority_boundary: {family} is not truth authority"


def pointer_lines(case, sparse=True):
    anchor = case["source_anchor"]
    if sparse:
        quote_token = json.dumps(anchor["text_quote"])
        return [
            f"pointer_triad: source_path={anchor['path']} source_hash={anchor['document_hash']} source_version={anchor['version_id']} selector={anchor['selector_type']} start={anchor['start']} end={anchor['end']} record_path={case['record_path']} evidence_path={case['evidence_path']} evidence_marker=EVIDENCE_{anchor['marker']} quote={quote_token}"
        ]
    lines = [
        f"source_pointer: path={anchor['path']} hash={anchor['document_hash']} version={anchor['version_id']} selector={anchor['selector_type']} start={anchor['start']} end={anchor['end']} quote={json.dumps(anchor['text_quote'])}",
        f"record_pointer: path={case['record_path']}",
        f"evidence_pointer: path={case['evidence_path']} marker=EVIDENCE_{anchor['marker']}",
    ]
    if not sparse:
        lines.extend([
            f"source_label: {compact(case.get('source_label'), 120)}",
            f"evidence_excerpt: {compact(case.get('evidence'), 520)}",
        ])
    return lines


def group_id(case, variant):
    if not case.get("recurrence_key"):
        return ""
    if variant == "leaky_or_unversioned_control":
        return case.get("recurrence_key", "")
    parts = [
        case.get("fingerprint_version", "fp-v1"),
        case.get("recurrence_key", ""),
        case.get("action_meaning", ""),
        case.get("feedback_type", ""),
        case.get("gap_family", ""),
        case.get("anchor_status", ""),
    ]
    return "|".join(parts)


def groupable(case, variant, state, full_audit):
    if variant == "shell_core_plus_recurrence":
        return state == "ordinary" and not full_audit and case.get("anchor_status") == "valid" and bool(case.get("recurrence_key"))
    if variant == "leaky_or_unversioned_control":
        return bool(case.get("recurrence_key"))
    return False


def build_group_meta(cases, variant):
    meta = {}
    for case in cases:
        state = state_for(case, variant)
        full = full_audit_for(case, variant, state)
        if not groupable(case, variant, state, full):
            continue
        gid = group_id(case, variant)
        bucket = meta.setdefault(gid, {"members": [], "exemplar": case["id"]})
        bucket["members"].append(case["id"])
    for bucket in meta.values():
        bucket["count"] = len(bucket["members"])
    return meta


def render_case(case, variant, group_meta):
    state = state_for(case, variant)
    full = full_audit_for(case, variant, state)
    review_due = state in {"blocking", "for_review", "regressed"}
    queue = review_due or case.get("anchor_status") in ANCHOR_PROBLEMS
    gid = group_id(case, variant) if groupable(case, variant, state, full) else ""
    group = group_meta.get(gid, {}) if gid else {}
    folded_member = bool(gid and group.get("exemplar") != case["id"])

    if variant == "baseline_full":
        front = [
            f"case: {case['id']}",
            f"state: {state}",
            f"summary: {compact(case['claim'], 120)}",
            f"anchor_health: {case['anchor_status']} source={case['source_anchor']['path']}",
            f"open_gap: baseline full audit visible",
            f"why: baseline_full all details open",
        ]
        back = pointer_lines(case, sparse=False)
    elif folded_member:
        front = [
            f"case: {case['id']}",
            f"state: {state}",
            f"summary: folded member exemplar={group['exemplar']} count={group.get('count')}",
            f"anchor_health: {case['anchor_status']} source={case['source_anchor']['path']}",
            "open_gap: recurrence triage only no truth change no support strength",
            "why: light because open ordinary valid-anchor recurrence",
        ]
        back = pointer_lines(case, sparse=True)
        back.append(f"group_id: {gid}")
    else:
        why = "why: thickened by hard trigger or anchor problem" if full else "why: light metadata stub"
        if state == "resolved_folded":
            why = "why: resolved folded stub"
        front = [
            f"case: {case['id']}",
            f"state: {state}",
            f"summary: {compact(case['claim'], 100)}",
            f"anchor_health: {case['anchor_status']} source={case['source_anchor']['path']}",
            f"open_gap: {compact(','.join(case.get('signals', [])) or case.get('layer', 'none'), 80)}",
            why,
        ]
        if variant == "authority_leaky_renderer":
            front[-1] = "why: dashboard green therefore true; tests passed so this is safer to believe"
        elif variant == "fake_precision_feedback_renderer":
            front[-1] = "why: risk 0.18 and feedback +0.17 raise confidence to 87%, so the record looks actionable"
        elif case.get("authority_trap") and variant == "leaky_or_unversioned_control":
            front[-1] = f"why: {case['authority_trap']}"
        elif case.get("authority_family"):
            front[-1] = boundary(case)
        if case.get("anchor_status") in ANCHOR_PROBLEMS:
            front[-1] = f"{front[-1]} ; anchor_problem_visibility: {case['anchor_status']}"
        if review_due:
            front[-1] = f"{front[-1]} ; review_due: true"
        if queue:
            front[-1] = f"{front[-1]} ; queue: unresolved_gate"
        back = pointer_lines(case, sparse=True)
        if gid:
            front[-1] = f"{front[-1]} ; recurrence: triage count={group.get('count', 1)}"
            back.append(f"group_id: {gid}")
        if case.get("object_type") == "feedback" and variant != "leaky_or_unversioned_control":
            front[-1] = f"{front[-1]} ; feedback: categorical no truth change"

    full_lines = []
    if full:
        full_lines = [
            "FULL_AUDIT_OPEN",
            "deep_packet_retained: true",
            f"signals: {','.join(case.get('signals', [])) or 'none'}",
            f"source_anchor: status={case['source_anchor']['status']} path={case['source_anchor']['path']} hash={case['source_anchor']['document_hash']} start={case['source_anchor']['start']} end={case['source_anchor']['end']} quote={json.dumps(case['source_anchor']['text_quote'])}",
            f"evidence_excerpt: {compact(case.get('evidence'), 700)}",
        ]
    return {"case_id": case["id"], "variant": variant, "front": front, "back": back, "full": full_lines, "rendered_text": "\n".join(front + back + full_lines)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--cases", required=True)
    parser.add_argument("--variant", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()
    cases = read_json(args.cases)
    meta = build_group_meta(cases, args.variant)
    artifacts = [render_case(case, args.variant, meta) for case in cases]
    Path(args.out).write_text(json.dumps(artifacts, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"{args.variant}: {len(artifacts)}")


if __name__ == "__main__":
    main()
