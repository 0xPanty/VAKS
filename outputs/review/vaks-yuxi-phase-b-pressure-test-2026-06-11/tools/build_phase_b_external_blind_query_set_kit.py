import json
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

TEMPLATE_JSONL = SANDBOX_DIR / "queries_phase_b_external_blind_template.jsonl"
MANIFEST_TEMPLATE_JSON = RESULTS_DIR / "phase_b_external_blind_query_author_manifest_template.json"
KIT_JSON = RESULTS_DIR / "phase_b_external_blind_query_set_kit.json"
KIT_MD = SANDBOX_DIR / "PHASE_B_EXTERNAL_BLIND_QUERY_SET_KIT.md"

INTENTS = [
    "action",
    "evidence",
    "review",
    "retrieval_design",
    "source_intake",
    "context_pack",
    "graph_retrieval",
    "agent_access",
]


def template_rows() -> list[dict]:
    rows = []
    for index in range(1, 21):
        rows.append(
            {
                "id": f"EXT-BLIND-{index:03d}",
                "group": "",
                "intent": "",
                "query": "",
                "needs_boundary_warning": None,
                "risk_note": "",
            }
        )
    return rows


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(row, ensure_ascii=False) for row in rows) + "\n", encoding="utf-8")


def write_manifest_template(path: Path) -> None:
    manifest = {
        "artifact_kind": "phase_b_external_blind_query_author_manifest",
        "created_at": "",
        "author_type": "external_human | different_model_family",
        "author_id_or_model_family": "",
        "generation_method": "",
        "attestation_no_phase_b_query_access": None,
        "attestation_no_phase_b_result_access": None,
        "attestation_no_phase_b_report_access": None,
        "allowed_docs_seen": [],
        "notes": "",
    }
    path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def write_markdown(summary: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_external_blind_query_set_kit",
        "status: pending_external_queries",
        "project_id: VAKS",
        "created_at: 2026-06-12",
        "truth_boundary: query_set_kit_not_completed_external_blind",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B External Blind Query Set Kit",
        "",
        "## Plain Task",
        "",
        "Pro's latest audit asks for 15-20 external blind queries written by an external human or at least a different model family.",
        "",
        "Use this template:",
        "",
        "```text",
        "queries_phase_b_external_blind_template.jsonl",
        "```",
        "",
        "Create this filled file:",
        "",
        "```text",
        "queries_phase_b_external_blind.jsonl",
        "```",
        "",
        "Also fill this author/provenance manifest:",
        "",
        "```text",
        "results/phase_b_external_blind_query_author_manifest.json",
        "```",
        "",
        "## Author Restriction",
        "",
        "```text",
        "Do not read existing Phase B query files.",
        "Do not read existing Phase B result CSV/JSON files.",
        "Do not read existing Phase B reports.",
        "Allowed source access: VAKS core docs and high-level architecture docs only.",
        "Target count: 15-20 filled queries.",
        "External author should not write expected_terms.",
        "Expected terms may be added later by an internal scorer without changing query text.",
        "```",
        "",
        "## Required JSONL Fields",
        "",
        "```yaml",
        "id: EXT-BLIND-001",
        "group: short category",
        f"intent: one of {', '.join(INTENTS)}",
        "query: user-facing query text",
        "needs_boundary_warning: true | false",
        "risk_note: why this query pressures retrieval/governance",
        "```",
        "",
        "## Author Manifest Fields",
        "",
        "```yaml",
        "author_type: external_human | different_model_family",
        "author_id_or_model_family:",
        "generation_method:",
        "attestation_no_phase_b_query_access: true",
        "attestation_no_phase_b_result_access: true",
        "attestation_no_phase_b_report_access: true",
        "allowed_docs_seen:",
        "  - README.md",
        "  - FUSION_ARCHITECTURE_V0_2_DRAFT.md",
        "notes:",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "This kit prepares external blind query generation.",
        "It does not complete external blind testing.",
        "Generated queries are test inputs, not reviewed knowledge.",
        "Passing this kit does not validate original Yuxi runtime, C-lite, writeback, or action basis.",
        "```",
        "",
        "## Template Summary",
        "",
        "```text",
        f"template rows: {summary['template_rows']}",
        "filled query file: queries_phase_b_external_blind.jsonl",
        "author manifest template: results/phase_b_external_blind_query_author_manifest_template.json",
        "author manifest filled file: results/phase_b_external_blind_query_author_manifest.json",
        "status: pending_external_queries",
        "```",
        "",
    ]
    KIT_MD.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    rows = template_rows()
    write_jsonl(TEMPLATE_JSONL, rows)
    write_manifest_template(MANIFEST_TEMPLATE_JSON)
    summary = {
        "artifact_kind": "phase_b_external_blind_query_set_kit",
        "created_at": "2026-06-12",
        "truth_boundary": "query_set_kit_not_completed_external_blind",
        "action_basis_allowed": False,
        "template_rows": len(rows),
        "target_filled_query_min": 15,
        "target_filled_query_max": 20,
        "filled_query_file": "queries_phase_b_external_blind.jsonl",
        "author_manifest_template": "results/phase_b_external_blind_query_author_manifest_template.json",
        "filled_author_manifest_file": "results/phase_b_external_blind_query_author_manifest.json",
        "external_author_must_not_write_expected_terms": True,
        "expected_terms_added_later_by_internal_scorer_only": True,
        "allowed_intents": INTENTS,
        "status": "pending_external_queries",
        "hard_stops": [
            "template_is_not_completed_external_blind",
            "do_not_use_internal_queries_as_external_blind",
            "do_not_claim_original_yuxi_runtime_validated",
            "do_not_enter_c_lite_from_this_kit",
        ],
    }
    KIT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    write_markdown(summary)
    print(f"external blind query template rows: {summary['template_rows']}")
    print(f"status: {summary['status']}")


if __name__ == "__main__":
    main()
