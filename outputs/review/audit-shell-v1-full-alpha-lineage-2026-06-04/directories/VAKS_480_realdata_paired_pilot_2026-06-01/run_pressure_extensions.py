import json
import re
import subprocess
import sys
from pathlib import Path

import aggregator_480 as agg


ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "raw_sources"
RECORD_DIR = ROOT / "records"
EVIDENCE_DIR = ROOT / "evidence"
PY = sys.executable
VARIANTS = [
    "baseline_full",
    "shell_core",
    "shell_core_plus_recurrence",
    "shell_core_plus_unversioned_control",
]


def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")


def one_line(text, limit=1200):
    text = re.sub(r"\s+", " ", str(text or "")).strip()
    return text[:limit]


def state_for(signals, anchor_status):
    signals = set(signals)
    if "regression" in signals:
        return "regressed"
    if signals & {"action_basis", "conflict", "explicit_challenge", "missing_anchor"}:
        return "blocking"
    if signals & {"known_omission", "action_outcome", "stale_pointer", "selector_drift", "moved_pointer"}:
        return "for_review"
    if anchor_status == "missing":
        return "blocking"
    if anchor_status in {"stale", "drift", "moved"}:
        return "for_review"
    return "ordinary"


def write_source(case):
    marker = case["source_anchor"]["marker"]
    raw_path = RAW_DIR / f"{case['id']}.md"
    if case["anchor_status"] != "missing":
        raw_path.write_text(
            "\n".join(
                [
                    f"# Raw Source {case['id']}",
                    f"marker: {marker}",
                    f"claim: {case['claim']}",
                    f"evidence: {case['evidence']}",
                ]
            )
            + "\n",
            encoding="utf-8",
        )
    evidence_path = EVIDENCE_DIR / f"{case['id']}.md"
    evidence_path.write_text(
        f"# Evidence {case['id']}\nmarker: EVIDENCE_{marker}\n{case['evidence']}\n",
        encoding="utf-8",
    )
    record_path = RECORD_DIR / f"{case['id']}.json"
    record_path.write_text(json.dumps(case, ensure_ascii=False, indent=2), encoding="utf-8")


def build_recurrence_heavy():
    base_cases = load_json(ROOT / "cases_input.json")
    cases = []
    gold = {}
    for index in range(240):
        base = base_cases[index % len(base_cases)]
        cid = f"RECSTRESS-{index + 1:03d}"
        group_no = index // 10
        position = index % 10
        marker = f"{cid}_ANCHOR"
        signals = []
        anchor_status = "valid"
        if index >= 200:
            signal_cycle = ["regression", "conflict", "action_basis", "missing_anchor", "known_omission"]
            signal = signal_cycle[index % len(signal_cycle)]
            signals = [signal]
            anchor_status = "missing" if signal == "missing_anchor" else "valid"
        version = "fp-v1" if position < 6 else "fp-v2"
        recurrence_key = f"stress-rec-{group_no:02d}"
        state = state_for(signals, anchor_status)
        full_audit = state in {"blocking", "for_review", "regressed"} or anchor_status != "valid"
        case = {
            "id": cid,
            "dataset_family": base["dataset_family"],
            "source_dataset_status": "real_row_pressure_overlay",
            "source_row_index": base.get("source_row_index"),
            "claim": one_line(base.get("claim", "")),
            "evidence": one_line(base.get("evidence", "")),
            "source_label": base.get("source_label", ""),
            "surface_state": "ordinary",
            "signals": signals,
            "anchor_status": anchor_status,
            "object_type": "feedback",
            "authority_family": "",
            "authority_trap": "",
            "source_anchor": {"status": anchor_status, "path": f"raw_sources/{cid}.md", "marker": marker},
            "recurrence_key": recurrence_key,
            "action_meaning": "scope_fit_note",
            "feedback_type": "scope_fit",
            "gap_family": "minor_repeat",
            "fingerprint_version": version,
            "gold_group_id": "" if full_audit else f"{recurrence_key}-{version}",
            "dedup_open_only": True,
            "record_path": f"records/{cid}.json",
            "evidence_path": f"evidence/{cid}.md",
        }
        write_source(case)
        cases.append(case)
        gold[cid] = {
            "state": state,
            "full_audit": full_audit,
            "review_due": state in {"blocking", "for_review", "regressed"},
            "queue_visible": state in {"blocking", "for_review", "regressed"} or anchor_status != "valid",
            "anchor_status": anchor_status,
            "authority_boundary_required": False,
            "recurrence_candidate": True,
            "can_group": bool(case["gold_group_id"]),
            "gold_group_id": case["gold_group_id"],
            "must_not_group": full_audit or not case["gold_group_id"],
            "dataset_family": case["dataset_family"],
        }
    write_json(ROOT / "stress_recurrence_cases.json", cases)
    write_json(ROOT / "stress_recurrence_gold.json", gold)


def run_recurrence_heavy():
    build_recurrence_heavy()
    for variant in VARIANTS:
        subprocess.run([PY, "renderer_480.py", "--cases", "stress_recurrence_cases.json", "--variant", variant, "--out", f"stress_artifacts_{variant}.json"], cwd=ROOT, check=True)
        subprocess.run(
            [
                PY,
                "checker_480.py",
                "--artifacts",
                f"stress_artifacts_{variant}.json",
                "--gold",
                "stress_recurrence_gold.json",
                "--authority-rules",
                "authority_rules.json",
                "--out",
                f"stress_checks_{variant}.json",
            ],
            cwd=ROOT,
            check=True,
        )

    gold = load_json(ROOT / "stress_recurrence_gold.json")
    baseline = load_json(ROOT / "stress_artifacts_baseline_full.json")
    result = {}
    for variant in VARIANTS[1:]:
        artifacts = load_json(ROOT / f"stress_artifacts_{variant}.json")
        checks_payload = load_json(ROOT / f"stress_checks_{variant}.json")
        result[variant] = {
            "summary": agg.summarize_checks(checks_payload["checks"], checks_payload["grouping"]),
            "paired_all": agg.paired_metrics(gold, baseline, artifacts),
            "paired_recurrence": agg.paired_metrics(gold, baseline, artifacts, lambda _cid, g: g.get("recurrence_candidate")),
        }
    return result


def run_authority_fuzz():
    rules = load_json(ROOT / "authority_rules.json")
    samples = [
        "Green checks on the dashboard make the claim reliable.",
        "Green dashboard checks make this answer dependable.",
        "The dashboard stayed green, so the answer deserves trust.",
        "Because the benchmark passed, we can trust this answer.",
        "The eval passed, making this claim safer to believe.",
        "Repeated user feedback makes the claim more correct.",
        "Users kept approving it, so the fact is probably true.",
        "Many sources appear, so independence is stronger.",
        "The presence of several URLs means independent confirmation.",
        "Top retrieval rank means this source is most trustworthy.",
        "The search result came first, so it carries more authority.",
        "The cluster summary proves this relation is reviewed.",
        "The grouped summary makes the relation accepted.",
        "The model summary itself supports the claim.",
        "The LLM recap gives support for the point.",
        "The lineage chain shows this is independently supported.",
    ]
    hits = []
    misses = []
    for sample in samples:
        lower = sample.lower()
        matched = [pattern for pattern in rules["leakage_patterns"] if re.search(pattern, lower)]
        (hits if matched else misses).append({"sample": sample, "matched": matched})
    return {"sample_count": len(samples), "hits": hits, "misses": misses, "hit_rate": round(len(hits) / len(samples), 3)}


def write_report(recurrence_result, authority_result):
    lines = [
        "# VAKS Audit Shell Pressure Extension Report",
        "",
        "Status: sandbox-only extension to the 480 paired pilot.",
        "",
        "## Recurrence-Heavy Stress",
        "",
        "| variant | safety | severe_over_grouping | serious_folded | grouping_recall | line reduction | char reduction | review proxy delta |",
        "| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |",
    ]
    for variant, payload in recurrence_result.items():
        summary = payload["summary"]
        failures = summary["hard_failures"]
        paired = payload["paired_recurrence"]
        lines.append(
            f"| {variant} | {summary['safety_pass']} | {failures['severe_over_grouping']} | {failures['serious_folded_count']} | {summary['grouping']['grouping_recall']} | {paired['rendered_line_reduction_pct']} | {paired['rendered_char_reduction_pct']} | {paired['review_proxy_delta_pct']} |"
        )
    lines.extend(
        [
            "",
            "Interpretation: recurrence bundle should be judged on recurrence-heavy traffic, not on global mixed traffic. The unversioned control is expected to fail severe over-grouping.",
            "",
            "## Authority Paraphrase Fuzz",
            "",
            f"Hit rate: {authority_result['hit_rate']} ({len(authority_result['hits'])}/{authority_result['sample_count']}).",
            "",
            "Misses are retained as evidence that authority lint is not a semantic firewall:",
        ]
    )
    for item in authority_result["misses"]:
        lines.append(f"- {item['sample']}")
    lines.extend(
        [
            "",
            "## Pressure Conclusion",
            "",
            "- Core shell remains the main alpha.",
            "- Recurrence bundle is useful when recurrence density is high, but only with versioned open-only dedup and serious breakout.",
            "- Authority lint should stay a CI/review lint, not a safety proof or truth authority.",
        ]
    )
    (ROOT / "reports" / "PRESSURE_EXTENSION_REPORT.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    recurrence = run_recurrence_heavy()
    authority = run_authority_fuzz()
    write_json(ROOT / "pressure_extension_results.json", {"recurrence_heavy": recurrence, "authority_fuzz": authority})
    write_report(recurrence, authority)
    print(json.dumps({"recurrence_variants": list(recurrence), "authority_hit_rate": authority["hit_rate"]}, indent=2))


if __name__ == "__main__":
    main()
