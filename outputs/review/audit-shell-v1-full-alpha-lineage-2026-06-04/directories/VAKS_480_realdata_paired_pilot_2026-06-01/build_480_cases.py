import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA_DIR = ROOT / "data"
RAW_DIR = ROOT / "raw_sources"
RECORD_DIR = ROOT / "records"
EVIDENCE_DIR = ROOT / "evidence"


ANCHOR_PROBLEMS = ["missing", "stale", "drift", "moved"]
AUTHORITY_FAMILIES = [
    "lineage_as_independence",
    "source_count_as_independence",
    "feedback_as_truth",
    "dashboard_as_truth",
    "test_pass_as_truth",
    "retrieval_rank_as_trust",
    "cluster_summary_as_reviewed_relation",
    "llm_summary_as_support",
]


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def clean(text, limit=1200):
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    return text[:limit]


def short_hash(text):
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()[:10]


def profile_for(index):
    if index < 50:
        return {"surface_state": "ordinary", "signals": [], "anchor_status": "valid", "object_type": "claim"}
    if index < 60:
        return {"surface_state": "resolved_folded", "signals": [], "anchor_status": "valid", "object_type": "claim"}
    if index < 72:
        return {"surface_state": "ordinary", "signals": ["action_basis"], "anchor_status": "valid", "object_type": "claim"}
    if index < 84:
        return {"surface_state": "ordinary", "signals": ["conflict"], "anchor_status": "valid", "object_type": "claim"}
    if index < 92:
        return {"surface_state": "ordinary", "signals": ["known_omission"], "anchor_status": "valid", "object_type": "claim"}
    if index < 100:
        status = ANCHOR_PROBLEMS[(index - 92) % len(ANCHOR_PROBLEMS)]
        signal = {
            "missing": "missing_anchor",
            "stale": "stale_pointer",
            "drift": "selector_drift",
            "moved": "moved_pointer",
        }[status]
        return {"surface_state": "ordinary", "signals": [signal], "anchor_status": status, "object_type": "claim"}
    if index < 106:
        return {"surface_state": "ordinary", "signals": [], "anchor_status": "valid", "object_type": "feedback", "recurrence_band": "v1"}
    if index < 110:
        return {"surface_state": "ordinary", "signals": [], "anchor_status": "valid", "object_type": "feedback", "recurrence_band": "v2"}
    if index < 114:
        signal = ["regression", "explicit_challenge", "action_outcome", "missing_anchor"][index - 110]
        status = "missing" if signal == "missing_anchor" else "valid"
        return {"surface_state": "ordinary", "signals": [signal], "anchor_status": status, "object_type": "feedback", "recurrence_band": "breakout"}
    if index < 120:
        family = AUTHORITY_FAMILIES[(index - 114) % len(AUTHORITY_FAMILIES)]
        return {"surface_state": "ordinary", "signals": [], "anchor_status": "valid", "object_type": "claim", "authority_family": family}
    raise ValueError(index)


def gold_state(signals, surface_state, anchor_status):
    signals = set(signals)
    if "regression" in signals:
        return "regressed"
    if signals & {"action_basis", "promotion", "conflict", "missing_anchor", "explicit_challenge", "high_severity_wrong_answer"}:
        return "blocking"
    if signals & {"known_omission", "stale_pointer", "selector_drift", "moved_pointer", "action_outcome", "decision_outcome"}:
        return "for_review"
    if surface_state in {"resolved_folded", "parked_nonblocking"}:
        return surface_state
    if anchor_status in {"stale", "drift", "moved"}:
        return "for_review"
    if anchor_status == "missing":
        return "blocking"
    return "ordinary"


def full_audit_for(state, anchor_status):
    return state in {"blocking", "for_review", "regressed"} or anchor_status in {"missing", "stale", "drift", "moved"}


def authority_trap(family):
    traps = {
        "lineage_as_independence": "The lineage chain shows this is independently supported.",
        "source_count_as_independence": "Many sources appear, so independence is stronger.",
        "feedback_as_truth": "Repeated user feedback makes the claim more correct.",
        "dashboard_as_truth": "Green checks on the dashboard make the claim reliable.",
        "test_pass_as_truth": "Because the benchmark passed, we can trust this answer.",
        "retrieval_rank_as_trust": "The top retrieval rank means this source is most trustworthy.",
        "cluster_summary_as_reviewed_relation": "The cluster summary proves this relation is reviewed.",
        "llm_summary_as_support": "The model summary itself supports the claim.",
    }
    return traps.get(family, "")


def recurrence_fields(family, index, claim):
    if index < 100 or index >= 114:
        return {}
    base = short_hash(f"{family}:shared-open-recurrence")
    if 100 <= index < 106:
        version = "fp-v1"
        gold = f"{family}-open-v1-{base}"
    elif 106 <= index < 110:
        version = "fp-v2"
        gold = f"{family}-open-v2-{base}"
    else:
        version = "fp-v1"
        gold = ""
    return {
        "recurrence_key": f"rec-{base}",
        "action_meaning": "scope_fit_note",
        "feedback_type": "scope_fit",
        "gap_family": "minor_repeat",
        "fingerprint_version": version,
        "gold_group_id": gold,
        "dedup_open_only": True,
    }


def source_payload(family, row):
    claim = clean(row.get("claim") or row.get("premise") or row.get("text") or row.get("hypothesis"))
    evidence = clean(row.get("evidence") or row.get("passage") or row.get("justification") or row.get("hypothesis"))
    label = clean(row.get("label") or row.get("fever_gold_label") or row.get("category"), 80)
    return claim or "(missing claim text)", evidence or "(missing evidence text)", label


def write_source_files(case):
    raw_path = RAW_DIR / f"{case['id']}.md"
    evidence_path = EVIDENCE_DIR / f"{case['id']}.md"
    record_path = RECORD_DIR / f"{case['id']}.json"
    marker = case["source_anchor"]["marker"]
    status = case["anchor_status"]

    if status == "valid":
        raw_marker = marker
    elif status in {"stale", "drift", "moved"}:
        raw_marker = f"OLD_{marker}"
    else:
        raw_marker = ""

    if status != "missing":
        raw_path.write_text(
            "\n".join(
                [
                    f"# Raw Source {case['id']}",
                    f"dataset: {case['dataset_family']}",
                    f"source_row: {case['source_row_index']}",
                    f"marker: {raw_marker}",
                    f"claim: {case['claim']}",
                    f"label: {case['source_label']}",
                    f"evidence: {case['evidence']}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )

    evidence_path.write_text(
        "\n".join(
            [
                f"# Evidence Packet {case['id']}",
                f"marker: EVIDENCE_{marker}",
                f"claim: {case['claim']}",
                f"evidence: {case['evidence']}",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    record_path.write_text(json.dumps(case, ensure_ascii=False, indent=2), encoding="utf-8")

    return {
        "source_path": f"raw_sources/{case['id']}.md",
        "record_path": f"records/{case['id']}.json",
        "evidence_path": f"evidence/{case['id']}.md",
    }


def build_family(family, rows):
    cases = []
    for index in range(120):
        row = rows[index % max(1, len(rows))] if rows else {}
        profile = profile_for(index)
        claim, evidence, label = source_payload(family, row)
        cid = f"{family.upper()}-{index + 1:03d}"
        marker = f"{cid}_ANCHOR"
        rec = recurrence_fields(family, index, claim)
        state = gold_state(profile["signals"], profile["surface_state"], profile["anchor_status"])
        full_audit = full_audit_for(state, profile["anchor_status"])
        case = {
            "id": cid,
            "dataset_family": family,
            "source_dataset_status": "real_row" if rows else "fallback_missing",
            "source_row_index": index % max(1, len(rows)) if rows else None,
            "claim": claim,
            "evidence": evidence,
            "source_label": label,
            "surface_state": profile["surface_state"],
            "signals": profile["signals"],
            "anchor_status": profile["anchor_status"],
            "object_type": profile["object_type"],
            "authority_family": profile.get("authority_family", ""),
            "authority_trap": authority_trap(profile.get("authority_family", "")),
            "source_anchor": {
                "status": profile["anchor_status"],
                "path": f"raw_sources/{cid}.md",
                "marker": marker,
            },
            **rec,
        }
        paths = write_source_files(case)
        case.update(paths)
        gold = {
            "state": state,
            "full_audit": full_audit,
            "review_due": state in {"blocking", "for_review", "regressed"},
            "queue_visible": state in {"blocking", "for_review", "regressed"} or profile["anchor_status"] in {"missing", "stale", "drift", "moved"},
            "anchor_status": profile["anchor_status"],
            "authority_boundary_required": bool(profile.get("authority_family")),
            "recurrence_candidate": bool(rec.get("recurrence_key")),
            "can_group": bool(rec.get("gold_group_id")) and not full_audit and profile["surface_state"] == "ordinary" and profile["anchor_status"] == "valid",
            "gold_group_id": rec.get("gold_group_id", ""),
            "must_not_group": full_audit or not rec.get("gold_group_id"),
            "dataset_family": family,
        }
        cases.append((case, gold))
    return cases


def main():
    RAW_DIR.mkdir(exist_ok=True)
    RECORD_DIR.mkdir(exist_ok=True)
    EVIDENCE_DIR.mkdir(exist_ok=True)
    fetched = load_json(DATA_DIR / "fetched_rows.json")

    all_cases = []
    gold = {}
    manifest = {}
    for family in ["scifact", "averitec", "ambifc", "fever"]:
        rows = fetched.get(family, {}).get("rows", [])
        manifest[family] = {
            "fetched_rows": len(rows),
            "source_status": fetched.get(family, {}).get("source_status", "missing"),
            "pilot_cases": 120,
        }
        for case, oracle in build_family(family, rows[:120]):
            all_cases.append(case)
            gold[case["id"]] = oracle

    (ROOT / "cases_input.json").write_text(json.dumps(all_cases, ensure_ascii=False, indent=2), encoding="utf-8")
    (ROOT / "gold_oracle.json").write_text(json.dumps(gold, ensure_ascii=False, indent=2), encoding="utf-8")
    (DATA_DIR / "case_build_manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"cases": len(all_cases), "families": manifest}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
