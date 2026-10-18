import csv
import json
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

PACKET_CSV = RESULTS_DIR / "phase_b_blind_relevance_judgment_packet.csv"
TEMPLATE_CSV = RESULTS_DIR / "phase_b_blind_relevance_external_judgment_template.csv"
MAPPING_CSV = RESULTS_DIR / "phase_b_blind_relevance_external_judgment_mapping.csv"
KIT_JSON = RESULTS_DIR / "phase_b_external_relevance_judgment_kit.json"
KIT_MD = SANDBOX_DIR / "PHASE_B_EXTERNAL_RELEVANCE_JUDGMENT_KIT.md"

COPY_FIELDS = [
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
]

MAPPING_FIELDS = [
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

JUDGMENT_FIELDS = [
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


def build_template_and_mapping(packet_rows: list[dict]) -> tuple[list[dict], list[dict]]:
    rows = []
    mapping = []
    modes = sorted({row.get("mode", "") for row in packet_rows})
    mode_slots = {mode: f"system_{idx:02d}" for idx, mode in enumerate(modes, start=1)}
    for index, row in enumerate(packet_rows, start=1):
        row_id = f"ERJ-{index:04d}"
        system_slot = mode_slots[row.get("mode", "")]
        out = {field: row.get(field, "") for field in COPY_FIELDS if field not in {"row_id", "system_slot"}}
        out["row_id"] = row_id
        out["system_slot"] = system_slot
        out.update({field: "" for field in JUDGMENT_FIELDS})
        rows.append(out)
        mapping.append(
            {
                "row_id": row_id,
                "system_slot": system_slot,
                "judgment_id": row.get("judgment_id", ""),
                "run_id": row.get("run_id", ""),
                "test_set": row.get("test_set", ""),
                "corpus": row.get("corpus", ""),
                "mode": row.get("mode", ""),
                "query_id": row.get("query_id", ""),
                "rank": row.get("rank", ""),
            }
        )
    return rows, mapping


def write_markdown(summary: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_external_relevance_judgment_kit",
        "status: pending_external_judgment",
        "project_id: VAKS",
        "created_at: 2026-06-12",
        "truth_boundary: judgment_kit_not_completed_external_judgment",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B External Relevance Judgment Kit",
        "",
        "## Plain Task",
        "",
        "Pro's latest audit says the next P0 is external/manual relevance judgment for the existing blind relevance packet.",
        "",
        "Use this template:",
        "",
        "```text",
        "results/phase_b_blind_relevance_external_judgment_template.csv",
        "```",
        "",
        "Create this filled file:",
        "",
        "```text",
        "results/phase_b_blind_relevance_external_judgments.csv",
        "```",
        "",
        "## Required Workflow",
        "",
        "```text",
        "Judge A fills judge_a_relevance, judge_a_basis, judge_a_id.",
        "Judge B independently fills judge_b_relevance, judge_b_basis, judge_b_id.",
        "The arbiter fills arbitrated_relevance, arbitration_basis, arbiter_id for every row.",
        "If Judge A and Judge B agree, arbitration_basis may simply say agreement.",
        "If they disagree, arbitration_basis should briefly explain why the final grade was chosen.",
        "```",
        "",
        "## Grade",
        "",
        "```text",
        "2 = relevant",
        "1 = borderline / partially relevant",
        "0 = not relevant",
        "```",
        "",
        "Judge only by the row's query, relevance_question, criteria, path, heading, bucket/status, warning, and snippet.",
        "",
        "Do not use expected_terms. Do not look at the internal heuristic judgment file before judging.",
        "",
        "The judge-facing template intentionally hides concrete system names. `system_slot` is an opaque label only; the system mapping is for post-judgment statistics and should not be shown to judges before grading.",
        "",
        "## Template Summary",
        "",
        "```text",
        f"packet rows: {summary['packet_rows']}",
        f"template rows: {summary['template_rows']}",
        f"query count: {summary['query_count']}",
        f"corpora: {', '.join(summary['corpora'])}",
        f"system slots: {', '.join(summary['system_slots'])}",
        "mapping file: results/phase_b_blind_relevance_external_judgment_mapping.csv",
        "status: pending_external_judgment",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "This kit prepares external/manual relevance judgment.",
        "It does not complete external/manual relevance judgment.",
        "It does not validate original Yuxi runtime.",
        "It does not approve C-lite, writeback, action basis, or core-doc strong conclusions.",
        "```",
        "",
    ]
    KIT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    packet_rows = read_csv(PACKET_CSV)
    template_rows, mapping_rows = build_template_and_mapping(packet_rows)
    write_csv(TEMPLATE_CSV, template_rows)
    write_csv(MAPPING_CSV, mapping_rows)
    summary = {
        "artifact_kind": "phase_b_external_relevance_judgment_kit",
        "created_at": "2026-06-12",
        "truth_boundary": "judgment_kit_not_completed_external_judgment",
        "action_basis_allowed": False,
        "packet_rows": len(packet_rows),
        "template_rows": len(template_rows),
        "mapping_rows": len(mapping_rows),
        "query_count": len({row["query_id"] for row in template_rows}),
        "corpora": sorted({row["corpus"] for row in template_rows}),
        "system_slots": sorted({row["system_slot"] for row in template_rows}),
        "system_identity_hidden_from_judge_template": True,
        "mapping_file": "results/phase_b_blind_relevance_external_judgment_mapping.csv",
        "required_external_judgment_file": "results/phase_b_blind_relevance_external_judgments.csv",
        "required_judges": 2,
        "requires_arbitration": True,
        "status": "pending_external_judgment",
        "hard_stops": [
            "template_is_not_completed_external_judgment",
            "do_not_use_internal_judgments_as_external_judgment",
            "do_not_claim_original_yuxi_runtime_validated",
            "do_not_enter_c_lite_from_this_kit",
        ],
    }
    KIT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(summary)
    print(f"external relevance template rows: {summary['template_rows']}")
    print(f"status: {summary['status']}")


if __name__ == "__main__":
    main()
