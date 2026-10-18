import csv
import json
import math
import statistics
from collections import Counter, defaultdict
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

PACKET_CSV = RESULTS_DIR / "phase_b_blind_relevance_judgment_packet.csv"
TEMPLATE_CSV = RESULTS_DIR / "phase_b_blind_relevance_external_judgment_template.csv"
MAPPING_CSV = RESULTS_DIR / "phase_b_blind_relevance_external_judgment_mapping.csv"
FILLED_JUDGMENTS_CSV = RESULTS_DIR / "phase_b_blind_relevance_external_judgments.csv"
JUDGED_SUMMARY_CSV = RESULTS_DIR / "phase_b_external_relevance_judged_summary.csv"
KIT_JSON = RESULTS_DIR / "phase_b_external_relevance_judgment_kit.json"
CHECK_JSON = RESULTS_DIR / "phase_b_external_relevance_judgment_kit_check.json"
CHECK_MD = SANDBOX_DIR / "PHASE_B_EXTERNAL_RELEVANCE_JUDGMENT_KIT_CHECK.md"
KIT_MD = SANDBOX_DIR / "PHASE_B_EXTERNAL_RELEVANCE_JUDGMENT_KIT.md"

VALID_GRADES = {"0", "1", "2"}
REQUIRED_TEMPLATE_FIELDS = [
    "row_id",
    "system_slot",
    "corpus",
    "query_id",
    "rank",
    "intent",
    "query",
    "relevance_question",
    "relevant_criteria",
    "borderline_criteria",
    "non_relevant_criteria",
    "path",
    "heading",
    "bucket",
    "status",
    "warning_code",
    "snippet",
    "judge_a_relevance",
    "judge_a_basis",
    "judge_a_id",
    "judge_b_relevance",
    "judge_b_basis",
    "judge_b_id",
    "arbitrated_relevance",
    "arbitration_basis",
    "arbiter_id",
]
FORBIDDEN_JUDGE_TEMPLATE_FIELDS = {"judgment_id", "run_id", "test_set", "mode"}
REQUIRED_MAPPING_FIELDS = [
    "row_id",
    "system_slot",
    "judgment_id",
    "run_id",
    "test_set",
    "corpus",
    "mode",
    "query_id",
    "rank",
]


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8-sig", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def validate_artifacts(errors: list[dict]) -> dict:
    required = [PACKET_CSV, TEMPLATE_CSV, MAPPING_CSV, KIT_JSON, KIT_MD]
    artifacts = []
    for path in required:
        exists = path.exists()
        artifacts.append(
            {"path": str(path.relative_to(SANDBOX_DIR)), "exists": exists, "bytes": path.stat().st_size if exists else 0}
        )
        if not exists:
            add_error(errors, "missing_artifact", str(path))
        elif path.stat().st_size == 0:
            add_error(errors, "empty_artifact", str(path))
    return {"artifacts": artifacts}


def validate_template(
    errors: list[dict], packet_rows: list[dict], template_rows: list[dict], mapping_rows: list[dict], kit: dict
) -> dict:
    if not template_rows:
        add_error(errors, "empty_template", "0 rows")
        return {}
    if not mapping_rows:
        add_error(errors, "empty_mapping", "0 rows")
        return {}
    missing_fields = [field for field in REQUIRED_TEMPLATE_FIELDS if field not in template_rows[0]]
    if missing_fields:
        add_error(errors, "template_missing_fields", ",".join(missing_fields))
    forbidden_fields = sorted(FORBIDDEN_JUDGE_TEMPLATE_FIELDS & set(template_rows[0]))
    if forbidden_fields:
        add_error(errors, "template_leaks_system_identity_fields", ",".join(forbidden_fields))
    missing_mapping_fields = [field for field in REQUIRED_MAPPING_FIELDS if field not in mapping_rows[0]]
    if missing_mapping_fields:
        add_error(errors, "mapping_missing_fields", ",".join(missing_mapping_fields))
    packet_ids = {row["judgment_id"] for row in packet_rows}
    mapping_ids = {row["judgment_id"] for row in mapping_rows}
    if packet_ids != mapping_ids:
        add_error(errors, "mapping_id_set_mismatch", f"packet={len(packet_ids)} mapping={len(mapping_ids)}")
    template_row_ids = {row["row_id"] for row in template_rows}
    mapping_row_ids = {row["row_id"] for row in mapping_rows}
    if template_row_ids != mapping_row_ids:
        add_error(errors, "template_mapping_row_id_mismatch", f"template={len(template_row_ids)} mapping={len(mapping_row_ids)}")
    if len(template_rows) != len(packet_rows):
        add_error(errors, "template_row_count_mismatch", f"{len(template_rows)} != {len(packet_rows)}")
    if len(mapping_rows) != len(packet_rows):
        add_error(errors, "mapping_row_count_mismatch", f"{len(mapping_rows)} != {len(packet_rows)}")
    duplicate_ids = [item for item, count in Counter(row["row_id"] for row in template_rows).items() if count > 1]
    if duplicate_ids:
        add_error(errors, "duplicate_template_ids", f"{len(duplicate_ids)} duplicates; first={duplicate_ids[:5]}")
    duplicate_mapping_ids = [item for item, count in Counter(row["row_id"] for row in mapping_rows).items() if count > 1]
    if duplicate_mapping_ids:
        add_error(errors, "duplicate_mapping_row_ids", f"{len(duplicate_mapping_ids)} duplicates; first={duplicate_mapping_ids[:5]}")
    leaking_values = []
    known_modes = {row.get("mode", "") for row in mapping_rows}
    for row in template_rows:
        for field, value in row.items():
            if value in known_modes:
                leaking_values.append(f"{row.get('row_id')}:{field}:{value}")
    if leaking_values:
        add_error(errors, "template_leaks_mode_values", f"{len(leaking_values)} leaks; first={leaking_values[:5]}")
    if kit.get("system_identity_hidden_from_judge_template") is not True:
        add_error(errors, "kit_does_not_mark_system_identity_hidden", str(kit.get("system_identity_hidden_from_judge_template")))
    nonblank_judgment_cells = []
    for row in template_rows:
        for field in [
            "judge_a_relevance",
            "judge_a_basis",
            "judge_a_id",
            "judge_b_relevance",
            "judge_b_basis",
            "judge_b_id",
            "arbitrated_relevance",
            "arbitration_basis",
            "arbiter_id",
        ]:
            if row.get(field, "").strip():
                nonblank_judgment_cells.append(f"{row['row_id']}:{field}")
    if nonblank_judgment_cells:
        add_error(errors, "template_contains_prefilled_judgment_cells", f"{len(nonblank_judgment_cells)} cells")
    if kit.get("status") != "pending_external_judgment":
        add_error(errors, "bad_kit_status", str(kit.get("status")))
    if kit.get("requires_arbitration") is not True:
        add_error(errors, "kit_missing_arbitration_requirement", str(kit.get("requires_arbitration")))
    return {
        "packet_rows": len(packet_rows),
        "template_rows": len(template_rows),
        "mapping_rows": len(mapping_rows),
        "query_count": len({row["query_id"] for row in template_rows}),
        "corpora": sorted({row["corpus"] for row in template_rows}),
        "system_slots": sorted({row["system_slot"] for row in template_rows}),
        "mapped_modes": sorted({row["mode"] for row in mapping_rows}),
    }


def dcg(grades: list[int]) -> float:
    return sum(((2**grade - 1) / math.log2(idx + 2)) for idx, grade in enumerate(grades))


def summarize_judgments(rows: list[dict], mapping_by_row_id: dict[str, dict]) -> list[dict]:
    grouped: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
    for row in rows:
        mapping = mapping_by_row_id[row["row_id"]]
        enriched = dict(row)
        enriched["mode"] = mapping["mode"]
        enriched["query_id"] = mapping["query_id"]
        enriched["rank"] = mapping["rank"]
        grouped[(row["corpus"], mapping["mode"], mapping["query_id"])].append(enriched)
    per_query = []
    for (corpus, mode, query_id), items in grouped.items():
        items.sort(key=lambda row: int(row["rank"]))
        grades = [int(row["arbitrated_relevance"]) for row in items]
        first_rel = next((idx + 1 for idx, grade in enumerate(grades) if grade >= 2), 0)
        ideal = sorted(grades, reverse=True)
        per_query.append(
            {
                "corpus": corpus,
                "mode": mode,
                "query_id": query_id,
                "relevant_at_5": sum(1 for grade in grades if grade >= 2),
                "borderline_at_5": sum(1 for grade in grades if grade == 1),
                "judged_mrr_at_5": 1.0 / first_rel if first_rel else 0.0,
                "ndcg_at_5": (dcg(grades) / dcg(ideal)) if dcg(ideal) else 0.0,
                "has_relevant_at_5": any(grade >= 2 for grade in grades),
            }
        )
    summary_grouped: dict[tuple[str, str], list[dict]] = defaultdict(list)
    for row in per_query:
        summary_grouped[(row["corpus"], row["mode"])].append(row)
    summary = []
    for (corpus, mode), items in sorted(summary_grouped.items()):
        summary.append(
            {
                "corpus": corpus,
                "mode": mode,
                "queries": len(items),
                "hit_at_5_judged": f"{sum(1 for item in items if item['has_relevant_at_5'])}/{len(items)}",
                "mean_relevant_at_5": f"{statistics.mean(item['relevant_at_5'] for item in items):.4f}",
                "mean_borderline_at_5": f"{statistics.mean(item['borderline_at_5'] for item in items):.4f}",
                "judged_mrr_at_5": f"{statistics.mean(item['judged_mrr_at_5'] for item in items):.4f}",
                "ndcg_at_5": f"{statistics.mean(item['ndcg_at_5'] for item in items):.4f}",
            }
        )
    return summary


def cohen_kappa(pairs: list[tuple[str, str]]) -> float:
    if not pairs:
        return 0.0
    observed = sum(1 for a, b in pairs if a == b) / len(pairs)
    a_counts = Counter(a for a, _ in pairs)
    b_counts = Counter(b for _, b in pairs)
    expected = sum((a_counts[grade] / len(pairs)) * (b_counts[grade] / len(pairs)) for grade in VALID_GRADES)
    if expected == 1:
        return 1.0
    return (observed - expected) / (1 - expected)


def validate_external_judgments(errors: list[dict], template_rows: list[dict], mapping_rows: list[dict]) -> dict:
    if not FILLED_JUDGMENTS_CSV.exists():
        return {
            "external_judgment_status": "pending_external_judgment",
            "judgment_rows": 0,
            "missing_judgment_rows": len(template_rows),
            "disagreement_rows": 0,
            "summary_rows": 0,
        }
    rows = read_csv(FILLED_JUDGMENTS_CSV)
    template_ids = {row["row_id"] for row in template_rows}
    row_ids = {row["row_id"] for row in rows}
    mapping_by_row_id = {row["row_id"]: row for row in mapping_rows}
    missing = sorted(template_ids - row_ids)
    extra = sorted(row_ids - template_ids)
    if missing:
        add_error(errors, "external_judgment_missing_rows", f"{len(missing)} missing; first={missing[:5]}")
    if extra:
        add_error(errors, "external_judgment_extra_rows", f"{len(extra)} extra; first={extra[:5]}")
    if len(rows) != len(template_rows):
        add_error(errors, "external_judgment_row_count_mismatch", f"{len(rows)} != {len(template_rows)}")

    bad_grades = []
    missing_basis = []
    missing_ids = []
    same_judge = []
    pairs = []
    disagreements = 0
    for row in rows:
        for field in ["judge_a_relevance", "judge_b_relevance", "arbitrated_relevance"]:
            if str(row.get(field, "")).strip() not in VALID_GRADES:
                bad_grades.append(f"{row.get('row_id')}:{field}")
        for field in ["judge_a_basis", "judge_b_basis", "arbitration_basis"]:
            if not row.get(field, "").strip():
                missing_basis.append(f"{row.get('row_id')}:{field}")
        for field in ["judge_a_id", "judge_b_id", "arbiter_id"]:
            if not row.get(field, "").strip():
                missing_ids.append(f"{row.get('row_id')}:{field}")
        if row.get("judge_a_id", "").strip() and row.get("judge_a_id", "").strip() == row.get("judge_b_id", "").strip():
            same_judge.append(row.get("row_id"))
        a = str(row.get("judge_a_relevance", "")).strip()
        b = str(row.get("judge_b_relevance", "")).strip()
        if a in VALID_GRADES and b in VALID_GRADES:
            pairs.append((a, b))
            if a != b:
                disagreements += 1
    if bad_grades:
        add_error(errors, "bad_external_judgment_grade", f"{len(bad_grades)} bad; first={bad_grades[:5]}")
    if missing_basis:
        add_error(errors, "missing_external_judgment_basis", f"{len(missing_basis)} missing; first={missing_basis[:5]}")
    if missing_ids:
        add_error(errors, "missing_external_judge_id", f"{len(missing_ids)} missing; first={missing_ids[:5]}")
    if same_judge:
        add_error(errors, "judge_a_and_b_not_independent", f"{len(same_judge)} same id; first={same_judge[:5]}")

    if not any(error["code"].startswith("external_judgment") or error["code"].startswith("bad_external") or error["code"].startswith("missing_external") or error["code"] == "judge_a_and_b_not_independent" for error in errors):
        summary = summarize_judgments(rows, mapping_by_row_id)
        write_csv(JUDGED_SUMMARY_CSV, summary)
        status = "complete"
    else:
        summary = []
        status = "invalid"
    agreement = sum(1 for a, b in pairs if a == b) / len(pairs) if pairs else 0.0
    return {
        "external_judgment_status": status,
        "judgment_rows": len(rows),
        "missing_judgment_rows": len(missing),
        "disagreement_rows": disagreements,
        "judge_agreement_rate": f"{agreement:.4f}",
        "cohen_kappa": f"{cohen_kappa(pairs):.4f}",
        "summary_rows": len(summary),
    }


def write_report(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_external_relevance_judgment_kit_check",
        f"status: {result['external_relevance_judgment_kit_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-12",
        "truth_boundary: external_judgment_kit_check_not_runtime_validation",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B External Relevance Judgment Kit Check",
        "",
        "## Result",
        "",
        "```text",
        f"status: {result['external_relevance_judgment_kit_check_status']}",
        f"error count: {result['error_count']}",
        f"template rows: {result['template'].get('template_rows')}",
        f"mapping rows: {result['template'].get('mapping_rows')}",
        f"query count: {result['template'].get('query_count')}",
        f"external judgment status: {result['external_judgments']['external_judgment_status']}",
        f"external judgment rows: {result['external_judgments']['judgment_rows']}",
        f"disagreement rows: {result['external_judgments']['disagreement_rows']}",
        f"judge agreement rate: {result['external_judgments'].get('judge_agreement_rate', 'n/a')}",
        f"cohen kappa: {result['external_judgments'].get('cohen_kappa', 'n/a')}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "pending_external_judgment means the double-judge/arbitration template is ready, not that external judgment is complete.",
        "The judge-facing template hides concrete system names; the mapping file is only for post-judgment statistics.",
        "Only a completed filled file can produce external judged relevance summary.",
        "This check does not validate original Yuxi runtime or approve C-lite/writeback.",
        "```",
        "",
        "## Errors",
        "",
    ]
    if result["errors"]:
        lines.extend(f"- {error['code']}: {error['detail']}" for error in result["errors"])
    else:
        lines.append("- none")
    lines.append("")
    CHECK_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    errors: list[dict] = []
    artifacts = validate_artifacts(errors)
    packet_rows = read_csv(PACKET_CSV) if PACKET_CSV.exists() else []
    template_rows = read_csv(TEMPLATE_CSV) if TEMPLATE_CSV.exists() else []
    mapping_rows = read_csv(MAPPING_CSV) if MAPPING_CSV.exists() else []
    kit = read_json(KIT_JSON) if KIT_JSON.exists() else {}
    template = validate_template(errors, packet_rows, template_rows, mapping_rows, kit) if packet_rows and template_rows else {}
    external = validate_external_judgments(errors, template_rows, mapping_rows) if template_rows else {
        "external_judgment_status": "missing_template",
        "judgment_rows": 0,
        "missing_judgment_rows": 0,
        "disagreement_rows": 0,
        "summary_rows": 0,
    }
    status = "pass" if not errors else "fail"
    if not errors and external.get("external_judgment_status") == "pending_external_judgment":
        status = "pending_external_judgment"
    result = {
        "external_relevance_judgment_kit_check_status": status,
        "error_count": len(errors),
        "errors": errors,
        "artifacts": artifacts,
        "template": template,
        "external_judgments": external,
    }
    CHECK_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(result)
    print(f"external relevance judgment kit check status: {status}")
    print(f"error count: {len(errors)}")
    print(f"external judgment status: {external.get('external_judgment_status')}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
