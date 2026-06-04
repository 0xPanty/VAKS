import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent
OUT_JSON = ROOT / "data" / "clickback_semantic_landing_eval.json"
OUT_REPORT = ROOT / "reports" / "CLICKBACK_SEMANTIC_LANDING_EVAL.md"


BOILERPLATE_PATTERNS = [
    "about this capture",
    "archive team",
    "wayback machine",
    "captures",
    "save page now",
    "success fail",
    "collected by organization",
]
SEMANTIC_STRATEGIES = {"evidence_substring", "claim_substring", "claim_keyword_window"}
LANDING_BY_STRATEGY = {
    "evidence_substring": "evidence_landing",
    "claim_substring": "claim_landing",
    "claim_keyword_window": "claim_relevant_context_landing",
}


def read_json(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def pct(num, den):
    return round(num / den * 100, 2) if den else None


def norm(text):
    return re.sub(r"\s+", " ", str(text)).strip()


def is_boilerplate(text):
    lower = norm(text).lower()
    return any(pattern in lower for pattern in BOILERPLATE_PATTERNS)


def file_exists(rel_path):
    return bool(rel_path) and (ROOT / rel_path).exists()


def main():
    manifest = read_json("data/clickback_snapshot_manifest.json")
    cases = {case["id"]: case for case in read_json("candidate_cases.json")}
    rows = []

    for log in manifest.get("logs", []):
        case_id = log["case_id"]
        case = cases.get(case_id, {})
        anchor = case.get("source_anchor") or {}
        quote = anchor.get("text_quote") or ""
        quote_strategy = anchor.get("quote_strategy") or log.get("quote_strategy") or ""
        landing_class = anchor.get("landing_class") or log.get("landing_class") or LANDING_BY_STRATEGY.get(quote_strategy, "selector_failure")
        snapshot_path = log.get("snapshot_path") or anchor.get("path") or ""
        record_path = case.get("record_path", "")
        evidence_path = case.get("evidence_path", "")
        transport_success = bool(log.get("ok")) and not bool(log.get("fallback_used"))
        source_path_resolves = file_exists(snapshot_path)
        record_path_resolves = file_exists(record_path)
        evidence_path_resolves = file_exists(evidence_path)
        boilerplate_quote = bool(anchor.get("boilerplate_quote")) or bool(log.get("boilerplate_quote")) or is_boilerplate(quote)
        semantic_selector_success = (
            transport_success
            and source_path_resolves
            and quote_strategy in SEMANTIC_STRATEGIES
            and not boilerplate_quote
        )
        rows.append(
            {
                "case_id": case_id,
                "transport_fetch_success": transport_success,
                "source_path_resolves": source_path_resolves,
                "record_path_resolves": record_path_resolves,
                "evidence_path_resolves": evidence_path_resolves,
                "quote_strategy": quote_strategy,
                "landing_class": landing_class,
                "boilerplate_quote": boilerplate_quote,
                "semantic_selector_success": semantic_selector_success,
                "snapshot_kind": log.get("snapshot_kind", ""),
                "snapshot_path": snapshot_path,
                "claim": case.get("claim", ""),
                "quote_preview": norm(quote)[:220],
                "needs_selector_repair": transport_success and not semantic_selector_success,
            }
        )

    summary = {
        "target": len(rows),
        "transport_fetch_success": sum(row["transport_fetch_success"] for row in rows),
        "source_path_resolves": sum(row["source_path_resolves"] for row in rows),
        "record_path_resolves": sum(row["record_path_resolves"] for row in rows),
        "evidence_path_resolves": sum(row["evidence_path_resolves"] for row in rows),
        "semantic_selector_success": sum(row["semantic_selector_success"] for row in rows),
        "body_window_used": sum(row["quote_strategy"] == "body_window" for row in rows),
        "boilerplate_quote": sum(row["boilerplate_quote"] for row in rows),
        "landing_class_counts": {
            "evidence_landing": sum(row["landing_class"] == "evidence_landing" for row in rows),
            "claim_landing": sum(row["landing_class"] == "claim_landing" for row in rows),
            "claim_relevant_context_landing": sum(row["landing_class"] == "claim_relevant_context_landing" for row in rows),
            "selector_failure": sum(row["landing_class"] == "selector_failure" for row in rows),
        },
    }
    summary["semantic_selector_success_pct"] = pct(summary["semantic_selector_success"], summary["target"])
    payload = {
        "status": "semantic click-back landing evaluation",
        "summary": summary,
        "rows": rows,
        "note": "Transport fetch, path resolution, and selector landing are separate. claim_relevant_context_landing is weaker than evidence_landing and needs operator adjudication.",
    }
    OUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")

    lines = [
        "# Click-back Semantic Landing Evaluation",
        "",
        "Status: sandbox diagnostic. This separates transport fetch, path resolution, and claim-relevant selector landing.",
        "",
        "Current readout:",
        "",
        "| metric | value |",
        "| --- | --- |",
    ]
    for key, value in summary.items():
        lines.append(f"| {key} | {value} |")
    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "- `transport_fetch_success` means a live / immutable snapshot was fetched.",
            "- `source_path_resolves` means the local source handle opens.",
            "- `semantic_selector_success` means the selected quote came from evidence, claim, or claim-keyword matching, not from a generic body window.",
            "- `landing_class` separates evidence landing, claim landing, and weaker claim-relevant context landing.",
            "- `body_window` and boilerplate quotes are not product-grade click-back success.",
            "",
            "## Rows Needing Selector Repair",
            "",
            "| case_id | quote_strategy | landing_class | boilerplate_quote | quote_preview |",
            "| --- | --- | --- | --- | --- |",
        ]
    )
    for row in rows:
        if row["needs_selector_repair"]:
            preview = row["quote_preview"].replace("|", "/")
            lines.append(f"| {row['case_id']} | {row['quote_strategy']} | {row['landing_class']} | {row['boilerplate_quote']} | {preview} |")
    OUT_REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(json.dumps({"out_json": str(OUT_JSON), "out_report": str(OUT_REPORT), "summary": summary}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
