import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATA = ROOT / "data"
RAW = ROOT / "raw_sources"
FULL = ROOT / "full_anchor_sources"
RECORDS = ROOT / "records"
EVIDENCE = ROOT / "evidence"


AUTHORITY_FAMILIES = [
    "dashboard_as_truth",
    "test_pass_as_truth",
    "lineage_as_independence",
    "source_count_as_independence",
    "group_count_as_support",
    "feedback_as_truth",
    "retrieval_rank_as_trust",
    "llm_summary_as_support",
    "cluster_summary_as_reviewed_relation",
    "approval_as_truth",
]


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def clean(text, limit=1400):
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    return text[:limit] if text else "(missing text)"


def sha(text):
    return hashlib.sha256(text.encode("utf-8", errors="ignore")).hexdigest()


def short(text):
    return hashlib.sha1(text.encode("utf-8", errors="ignore")).hexdigest()[:10]


def profile_for_pool(index):
    if index < 60:
        return {"layer": "ordinary_stable", "signals": [], "surface_state": "ordinary", "anchor_status": "valid", "object_type": "claim"}
    if index < 90:
        cycle = ["action_basis", "explicit_challenge", "conflict"]
        return {"layer": "action_challenge_conflict", "signals": [cycle[(index - 60) % 3]], "surface_state": "ordinary", "anchor_status": "valid", "object_type": "claim"}
    if index < 115:
        cycle = ["known_omission", "insufficient_evidence", "ambiguous_scope"]
        return {"layer": "omission_insufficiency_ambiguity", "signals": [cycle[(index - 90) % 3]], "surface_state": "ordinary", "anchor_status": "valid", "object_type": "claim"}
    if index < 130:
        statuses = ["missing", "stale", "drift", "moved"]
        status = statuses[(index - 115) % 4]
        signal = {"missing": "missing_anchor", "stale": "stale_pointer", "drift": "selector_drift", "moved": "moved_pointer"}[status]
        return {"layer": "anchor_problem", "signals": [signal], "surface_state": "ordinary", "anchor_status": status, "object_type": "claim"}
    if index < 150:
        surface = "resolved_folded" if index < 138 else "ordinary"
        return {"layer": "resolved_repeated_recurrence", "signals": [], "surface_state": surface, "anchor_status": "valid", "object_type": "feedback", "recurrence": True}
    family = AUTHORITY_FAMILIES[(index - 150) % len(AUTHORITY_FAMILIES)]
    return {"layer": "authority_leak_bait", "signals": [], "surface_state": "ordinary", "anchor_status": "valid", "object_type": "claim", "authority_family": family}


def authority_trap(family):
    traps = {
        "dashboard_as_truth": "Green dashboard checks make this answer dependable.",
        "test_pass_as_truth": "The eval passed, making this claim safer to believe.",
        "lineage_as_independence": "The lineage chain independently confirms the point.",
        "source_count_as_independence": "The presence of several URLs means independent confirmation.",
        "group_count_as_support": "A large group count gives stronger support.",
        "feedback_as_truth": "Users kept approving it, so the fact is probably true.",
        "retrieval_rank_as_trust": "The search result came first, so it carries more authority.",
        "llm_summary_as_support": "The LLM recap gives support for the point.",
        "cluster_summary_as_reviewed_relation": "The grouped summary makes the relation accepted.",
        "approval_as_truth": "Reviewer approval means the claim is true.",
    }
    return traps.get(family, "")


def make_source(case, source_kind="dataset"):
    marker = f"{case['id']}_ANCHOR"
    quote = clean(case["evidence"] or case["claim"], 220)
    body = (
        f"# Source {case['id']}\n"
        f"kind: {source_kind}\n"
        f"dataset: {case['dataset_family']}\n"
        f"marker: {marker}\n\n"
        f"claim: {case['claim']}\n\n"
        f"evidence quote begins: {quote}\n"
        f"evidence quote ends.\n"
    )
    source_dir = FULL if source_kind != "dataset" else RAW
    path = source_dir / f"{case['id']}.md"
    status = case["anchor_status"]
    stored_body = body
    selector_quote = quote
    start = stored_body.find(selector_quote)
    if status == "missing":
        stored_body = ""
        start = -1
    elif status == "stale":
        stored_body = body.replace(selector_quote, f"STALE VERSION OF {selector_quote[:80]}")
        start = stored_body.find(selector_quote)
    elif status == "drift":
        stored_body = body.replace(selector_quote, f"moved earlier {selector_quote}")
        start = max(0, body.find(selector_quote) + 7)
    elif status == "moved":
        stored_body = body
        path = source_dir / f"{case['id']}_moved.md"
        start = body.find(selector_quote)

    if stored_body:
        path.write_text(stored_body, encoding="utf-8")
    end = start + len(selector_quote) if start >= 0 else -1
    expected_hash = sha(body if status in {"stale"} else stored_body) if stored_body else ""
    if status == "stale":
        expected_hash = sha(body)
    case["source_anchor"] = {
        "status": status,
        "path": str(path.relative_to(ROOT)).replace("\\", "/") if status != "missing" else f"{source_dir.name}/{case['id']}.md",
        "document_hash": expected_hash,
        "version_id": f"{source_kind}-v1",
        "selector_type": "text_quote+char_offset",
        "marker": marker,
        "text_quote": selector_quote,
        "start": start,
        "end": end,
    }
    case["record_path"] = f"records/{case['id']}.json"
    case["evidence_path"] = f"evidence/{case['id']}.md"
    evidence_body = f"# Evidence {case['id']}\nmarker: EVIDENCE_{marker}\nquote: {selector_quote}\n"
    (EVIDENCE / f"{case['id']}.md").write_text(evidence_body, encoding="utf-8")


def save_record(case):
    (RECORDS / f"{case['id']}.json").write_text(json.dumps(case, ensure_ascii=False, indent=2), encoding="utf-8")


def recurrence_fields(family, index):
    if index < 130 or index >= 150:
        return {}
    base = short(f"{family}:800-recurrence:{index // 10}")
    version = "fp-v1" if index < 140 else "fp-v2"
    return {
        "recurrence_key": f"rec-{base}",
        "action_meaning": "scope_fit_note",
        "feedback_type": "scope_fit",
        "gap_family": "minor_repeat",
        "fingerprint_version": version,
    }


def build_main_pool(family, rows):
    cases = []
    for index in range(160):
        row = rows[index % len(rows)] if rows else {}
        profile = profile_for_pool(index)
        cid = f"{family.upper()}-{index + 1:03d}"
        case = {
            "id": cid,
            "pool": "main_public",
            "dataset_family": family,
            "source_row_index": index % len(rows) if rows else None,
            "layer": profile["layer"],
            "claim": clean(row.get("claim", "")),
            "evidence": clean(row.get("evidence", "")),
            "source_label": clean(row.get("label", ""), 120),
            "surface_state": profile["surface_state"],
            "signals": profile["signals"],
            "anchor_status": profile["anchor_status"],
            "object_type": profile["object_type"],
            "authority_family": profile.get("authority_family", ""),
            "authority_trap": authority_trap(profile.get("authority_family", "")),
            **recurrence_fields(family, index),
        }
        make_source(case, "dataset")
        save_record(case)
        cases.append(case)
    return cases


def build_full_anchor_pack(seed_rows):
    kinds = ["pdf_text", "web_page", "repo_file", "release_note", "manual_span"]
    cases = []
    for index in range(80):
        row = seed_rows[index % len(seed_rows)]
        kind = kinds[index % len(kinds)]
        signal = ["", "action_basis", "known_omission", ""][index % 4]
        cid = f"FULLANCHOR-{index + 1:03d}"
        case = {
            "id": cid,
            "pool": "full_anchor_real_pack",
            "dataset_family": row.get("family", "mixed"),
            "source_row_index": row.get("index"),
            "layer": "full_anchor_click",
            "claim": clean(row.get("claim", "")),
            "evidence": clean(row.get("evidence", "")),
            "source_label": clean(row.get("label", ""), 120),
            "surface_state": "ordinary",
            "signals": [signal] if signal else [],
            "anchor_status": "valid",
            "object_type": "claim",
            "authority_family": "",
            "authority_trap": "",
            "full_anchor_kind": kind,
        }
        make_source(case, kind)
        save_record(case)
        cases.append(case)
    return cases


def build_adversarial(seed_rows):
    cases = []
    for index in range(80):
        row = seed_rows[index % len(seed_rows)]
        cid = f"HOLDOUT-{index + 1:03d}"
        profile = {"layer": "", "signals": [], "anchor_status": "valid", "surface_state": "ordinary", "object_type": "claim"}
        rec = {}
        authority_family = ""
        if index < 16:
            profile.update({"layer": "false_lite_trap", "signals": [["action_basis"], ["promotion"], ["explicit_challenge"], ["conflict"]][index % 4]})
        elif index < 28:
            profile.update({"layer": "review_due_trap", "signals": [["known_omission"], ["ambiguous_scope"], ["insufficient_evidence"]][index % 3]})
        elif index < 44:
            statuses = ["missing", "stale", "drift", "moved"]
            status = statuses[(index - 28) % 4]
            signal = {"missing": "missing_anchor", "stale": "stale_pointer", "drift": "selector_drift", "moved": "moved_pointer"}[status]
            profile.update({"layer": "anchor_jumpback_failure", "signals": [signal], "anchor_status": status})
        elif index < 64:
            near = index - 44
            profile.update({"layer": "over_grouping_near_miss", "object_type": "feedback"})
            rec = {
                "recurrence_key": f"holdout-near-{near // 5}",
                "action_meaning": ["scope_fit_note", "action_basis_note"][near % 5 == 1],
                "feedback_type": "scope_fit",
                "gap_family": ["minor_repeat", "conflict_neighbor"][near % 5 == 2],
                "fingerprint_version": ["fp-v1", "fp-v2"][near % 5 == 3],
            }
            if near % 5 == 4:
                profile["anchor_status"] = "stale"
                profile["signals"] = ["stale_pointer"]
        elif index < 72:
            profile.update({"layer": "authority_leakage_paraphrase"})
            authority_family = AUTHORITY_FAMILIES[(index - 64) % len(AUTHORITY_FAMILIES)]
        else:
            profile.update({"layer": "serious_folded_violation", "object_type": "feedback", "signals": [["regression"], ["missing_anchor"], ["conflict"], ["action_basis"]][(index - 72) % 4]})
            profile["anchor_status"] = "missing" if "missing_anchor" in profile["signals"] else "valid"
            rec = {
                "recurrence_key": f"serious-fold-{index // 2}",
                "action_meaning": "scope_fit_note",
                "feedback_type": "scope_fit",
                "gap_family": "minor_repeat",
                "fingerprint_version": "fp-v1",
            }
        case = {
            "id": cid,
            "pool": "adversarial_holdout",
            "dataset_family": row.get("family", "mixed"),
            "source_row_index": row.get("index"),
            "layer": profile["layer"],
            "claim": clean(row.get("claim", "")),
            "evidence": clean(row.get("evidence", "")),
            "source_label": clean(row.get("label", ""), 120),
            "surface_state": profile["surface_state"],
            "signals": profile["signals"],
            "anchor_status": profile["anchor_status"],
            "object_type": profile["object_type"],
            "authority_family": authority_family,
            "authority_trap": authority_trap(authority_family),
            **rec,
        }
        make_source(case, "holdout")
        save_record(case)
        cases.append(case)
    return cases


def seed_rows(fetched):
    rows = []
    for family in ["scifact", "averitec", "ambifc", "fever"]:
        for index, row in enumerate(fetched.get(family, {}).get("rows", [])[:180]):
            rows.append({"family": family, "index": index, **row})
    return rows


def main():
    for directory in [RAW, FULL, RECORDS, EVIDENCE]:
        directory.mkdir(exist_ok=True)
    fetched = read_json(DATA / "fetched_rows.json")
    cases = []
    manifest = {}
    for family in ["scifact", "averitec", "ambifc", "fever"]:
        rows = fetched.get(family, {}).get("rows", [])
        cases.extend(build_main_pool(family, rows[:180]))
        manifest[family] = {"source_rows": len(rows), "pilot_cases": 160, "source_status": fetched.get(family, {}).get("source_status", "unknown")}
    seeds = seed_rows(fetched)
    cases.extend(build_full_anchor_pack(seeds))
    cases.extend(build_adversarial(seeds))
    manifest["full_anchor_real_pack"] = {"pilot_cases": 80}
    manifest["adversarial_holdout"] = {"pilot_cases": 80}
    write_json(ROOT / "candidate_cases.json", cases)
    write_json(DATA / "case_build_manifest.json", manifest)
    print(json.dumps({"cases": len(cases), "manifest": manifest}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
