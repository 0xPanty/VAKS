import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parent
BLOCKING = {"action_basis", "promotion", "explicit_challenge", "conflict", "missing_anchor", "high_severity_wrong_answer"}
REVIEW = {"known_omission", "insufficient_evidence", "ambiguous_scope", "stale_pointer", "selector_drift", "moved_pointer", "action_outcome", "decision_outcome"}
ANCHOR_PROBLEMS = {"missing", "stale", "drift", "moved"}


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def state_for(case):
    signals = set(case.get("signals", []))
    if "regression" in signals:
        return "regressed"
    if signals & BLOCKING:
        return "blocking"
    if signals & REVIEW:
        return "for_review"
    if case.get("anchor_status") == "missing":
        return "blocking"
    if case.get("anchor_status") in {"stale", "drift", "moved"}:
        return "for_review"
    if case.get("surface_state") in {"resolved_folded", "parked_nonblocking"}:
        return case["surface_state"]
    return "ordinary"


def full_audit_for(state, anchor_status):
    return state in {"blocking", "for_review", "regressed"} or anchor_status in ANCHOR_PROBLEMS


def gold_group_id(case, full_audit, state):
    if full_audit or state != "ordinary" or case.get("anchor_status") != "valid" or not case.get("recurrence_key"):
        return ""
    parts = [
        case.get("fingerprint_version", "fp-v1"),
        case.get("recurrence_key", ""),
        case.get("action_meaning", ""),
        case.get("feedback_type", ""),
        case.get("gap_family", ""),
        case.get("anchor_status", ""),
    ]
    return "|".join(parts)


def make_gold(case):
    state = state_for(case)
    full_audit = full_audit_for(state, case.get("anchor_status", "valid"))
    group_id = gold_group_id(case, full_audit, state)
    return {
        "state": state,
        "full_audit": full_audit,
        "review_due": state in {"blocking", "for_review", "regressed"},
        "queue_visible": state in {"blocking", "for_review", "regressed"} or case.get("anchor_status") in ANCHOR_PROBLEMS,
        "anchor_status": case.get("anchor_status", "valid"),
        "valid_anchor_expected": case.get("anchor_status") == "valid",
        "anchor_problem_visibility_required": case.get("anchor_status") in ANCHOR_PROBLEMS,
        "record_pointer_required": True,
        "evidence_pointer_required": True,
        "source_pointer_required": True,
        "authority_boundary_required": bool(case.get("authority_family")),
        "recurrence_candidate": bool(case.get("recurrence_key")),
        "can_group": bool(group_id),
        "gold_group_id": group_id,
        "must_not_group": full_audit or not group_id,
        "ordinary": state in {"ordinary", "resolved_folded", "parked_nonblocking"} and not full_audit,
        "serious": full_audit or state in {"blocking", "for_review", "regressed"},
        "resolved": state == "resolved_folded",
        "pool": case.get("pool"),
        "layer": case.get("layer"),
        "dataset_family": case.get("dataset_family"),
    }


def sha_file(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def main():
    cases = read_json(ROOT / "candidate_cases.json")
    gold = {case["id"]: make_gold(case) for case in cases}
    out = ROOT / "gold_oracle_frozen.json"
    write_json(out, gold)
    digest = sha_file(out)
    (ROOT / "gold_oracle_frozen.sha256").write_text(f"{digest}  gold_oracle_frozen.json\n", encoding="utf-8")
    manifest = {
        "frozen_at_utc": datetime.now(timezone.utc).isoformat(),
        "gold_file": "gold_oracle_frozen.json",
        "sha256": digest,
        "case_count": len(cases),
        "gold_origin": "machine_frozen_from_explicit_case_overlays_not_human_adjudicated",
        "warning": "This proves frozen-gold workflow and rule consistency, not independent human oracle validity.",
    }
    write_json(ROOT / "gold_freeze_manifest.json", manifest)
    print(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
