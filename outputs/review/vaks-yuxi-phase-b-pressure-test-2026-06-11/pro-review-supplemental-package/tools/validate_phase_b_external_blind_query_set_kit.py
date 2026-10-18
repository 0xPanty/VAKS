import json
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"

TEMPLATE_JSONL = SANDBOX_DIR / "queries_phase_b_external_blind_template.jsonl"
FILLED_JSONL = SANDBOX_DIR / "queries_phase_b_external_blind.jsonl"
AUTHOR_MANIFEST_TEMPLATE_JSON = RESULTS_DIR / "phase_b_external_blind_query_author_manifest_template.json"
AUTHOR_MANIFEST_JSON = RESULTS_DIR / "phase_b_external_blind_query_author_manifest.json"
KIT_JSON = RESULTS_DIR / "phase_b_external_blind_query_set_kit.json"
CHECK_JSON = RESULTS_DIR / "phase_b_external_blind_query_set_kit_check.json"
KIT_MD = SANDBOX_DIR / "PHASE_B_EXTERNAL_BLIND_QUERY_SET_KIT.md"
CHECK_MD = SANDBOX_DIR / "PHASE_B_EXTERNAL_BLIND_QUERY_SET_KIT_CHECK.md"

EXISTING_QUERY_FILES = [
    "queries_phase_b.jsonl",
    "queries_phase_b_holdout.jsonl",
    "queries_phase_b_adversarial.jsonl",
    "queries_phase_b_agent_blind.jsonl",
    "queries_phase_b_blind_relevance.jsonl",
]

REQUIRED_FIELDS = {
    "id",
    "group",
    "intent",
    "query",
    "needs_boundary_warning",
    "risk_note",
}


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def read_jsonl(path: Path) -> list[dict]:
    rows = []
    for line_number, line in enumerate(path.read_text(encoding="utf-8-sig").splitlines(), start=1):
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{path}:{line_number}: {exc}") from exc
    return rows


def validate_artifacts(errors: list[dict]) -> dict:
    required = [TEMPLATE_JSONL, AUTHOR_MANIFEST_TEMPLATE_JSON, KIT_JSON, KIT_MD]
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


def validate_template(errors: list[dict], template_rows: list[dict], kit: dict) -> dict:
    if len(template_rows) != int(kit.get("template_rows") or -1):
        add_error(errors, "template_row_count_mismatch", f"{len(template_rows)} != {kit.get('template_rows')}")
    ids = [row.get("id") for row in template_rows]
    if len(set(ids)) != len(ids):
        add_error(errors, "duplicate_template_ids", str(ids))
    for row in template_rows:
        missing = sorted(REQUIRED_FIELDS - set(row))
        if missing:
            add_error(errors, "template_missing_fields", f"{row.get('id')}:{','.join(missing)}")
        if "expected_terms" in row:
            add_error(errors, "template_should_not_include_expected_terms", str(row.get("id")))
        if row.get("query") or row.get("group") or row.get("intent") or row.get("risk_note"):
            add_error(errors, "template_contains_prefilled_query_content", str(row.get("id")))
    if kit.get("external_author_must_not_write_expected_terms") is not True:
        add_error(errors, "kit_missing_expected_terms_boundary", str(kit.get("external_author_must_not_write_expected_terms")))
    hard_stops = set(kit.get("hard_stops") or [])
    for required in [
        "template_is_not_completed_external_blind",
        "do_not_use_internal_queries_as_external_blind",
        "do_not_claim_original_yuxi_runtime_validated",
        "do_not_enter_c_lite_from_this_kit",
    ]:
        if required not in hard_stops:
            add_error(errors, "missing_hard_stop", required)
    return {"template_rows": len(template_rows)}


def validate_author_manifest(errors: list[dict], filled_exists: bool) -> dict:
    if not filled_exists:
        return {
            "author_manifest_status": "pending_external_queries",
            "author_type": "",
            "allowed_docs_seen_count": 0,
        }
    if not AUTHOR_MANIFEST_JSON.exists():
        add_error(errors, "missing_author_manifest", str(AUTHOR_MANIFEST_JSON))
        return {"author_manifest_status": "missing", "author_type": "", "allowed_docs_seen_count": 0}
    manifest = read_json(AUTHOR_MANIFEST_JSON)
    if manifest.get("artifact_kind") != "phase_b_external_blind_query_author_manifest":
        add_error(errors, "bad_author_manifest_kind", str(manifest.get("artifact_kind")))
    if manifest.get("author_type") not in {"external_human", "different_model_family"}:
        add_error(errors, "bad_author_type", str(manifest.get("author_type")))
    if not str(manifest.get("author_id_or_model_family", "")).strip():
        add_error(errors, "missing_author_id_or_model_family", "")
    if not str(manifest.get("generation_method", "")).strip():
        add_error(errors, "missing_generation_method", "")
    for field in [
        "attestation_no_phase_b_query_access",
        "attestation_no_phase_b_result_access",
        "attestation_no_phase_b_report_access",
    ]:
        if manifest.get(field) is not True:
            add_error(errors, "author_attestation_not_true", field)
    if not isinstance(manifest.get("allowed_docs_seen"), list) or not manifest.get("allowed_docs_seen"):
        add_error(errors, "allowed_docs_seen_missing", "")
    return {
        "author_manifest_status": "complete",
        "author_type": manifest.get("author_type", ""),
        "allowed_docs_seen_count": len(manifest.get("allowed_docs_seen") or []),
    }


def existing_queries() -> dict[str, str]:
    rows = {}
    for rel in EXISTING_QUERY_FILES:
        path = SANDBOX_DIR / rel
        if not path.exists():
            continue
        for row in read_jsonl(path):
            rows[row.get("id", "")] = row.get("query", "")
    return rows


def validate_filled_queries(errors: list[dict], kit: dict) -> dict:
    if not FILLED_JSONL.exists():
        return {
            "external_blind_query_status": "pending_external_queries",
            "filled_query_rows": 0,
            "unique_query_rows": 0,
        }
    try:
        rows = read_jsonl(FILLED_JSONL)
    except ValueError as exc:
        add_error(errors, "filled_query_jsonl_invalid", str(exc))
        return {
            "external_blind_query_status": "invalid",
            "filled_query_rows": 0,
            "unique_query_rows": 0,
        }
    min_rows = int(kit.get("target_filled_query_min") or 15)
    max_rows = int(kit.get("target_filled_query_max") or 20)
    if not (min_rows <= len(rows) <= max_rows):
        add_error(errors, "filled_query_count_out_of_range", f"{len(rows)} not in [{min_rows}, {max_rows}]")
    allowed_intents = set(kit.get("allowed_intents") or [])
    ids = [row.get("id", "") for row in rows]
    queries = [row.get("query", "") for row in rows]
    if len(set(ids)) != len(ids):
        add_error(errors, "duplicate_filled_query_ids", str(ids))
    if len(set(queries)) != len(queries):
        add_error(errors, "duplicate_filled_query_text", "duplicate query text exists")
    previous = existing_queries()
    previous_text = {text.strip() for text in previous.values() if text.strip()}
    id_collisions = sorted(set(ids) & set(previous))
    text_collisions = sorted({query for query in queries if query.strip() in previous_text})
    if id_collisions:
        add_error(errors, "filled_query_id_collides_with_existing", ",".join(id_collisions))
    if text_collisions:
        add_error(errors, "filled_query_text_collides_with_existing", str(text_collisions[:3]))
    for row in rows:
        row_id = row.get("id", "<missing>")
        missing = sorted(REQUIRED_FIELDS - set(row))
        if missing:
            add_error(errors, "filled_query_missing_fields", f"{row_id}:{','.join(missing)}")
            continue
        if "expected_terms" in row:
            add_error(errors, "filled_query_should_not_include_expected_terms", row_id)
        for field in ["id", "group", "intent", "query", "risk_note"]:
            if not str(row.get(field, "")).strip():
                add_error(errors, "filled_query_blank_required_field", f"{row_id}:{field}")
        if row.get("intent") not in allowed_intents:
            add_error(errors, "filled_query_bad_intent", f"{row_id}:{row.get('intent')}")
        if not isinstance(row.get("needs_boundary_warning"), bool):
            add_error(errors, "filled_query_needs_boundary_warning_not_bool", row_id)
    invalid_prefixes = [row_id for row_id in ids if not str(row_id).startswith("EXT-BLIND-")]
    if invalid_prefixes:
        add_error(errors, "filled_query_bad_id_prefix", ",".join(invalid_prefixes[:5]))
    return {
        "external_blind_query_status": "complete" if not errors else "invalid",
        "filled_query_rows": len(rows),
        "unique_query_rows": len(set(queries)),
    }


def write_report(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_external_blind_query_set_kit_check",
        f"status: {result['external_blind_query_set_kit_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-12",
        "truth_boundary: external_blind_query_kit_check_not_completed_external_test",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B External Blind Query Set Kit Check",
        "",
        "## Result",
        "",
        "```text",
        f"status: {result['external_blind_query_set_kit_check_status']}",
        f"error count: {result['error_count']}",
        f"template rows: {result['template'].get('template_rows')}",
        f"external blind query status: {result['filled_queries']['external_blind_query_status']}",
        f"filled query rows: {result['filled_queries']['filled_query_rows']}",
        f"author manifest status: {result['author_manifest']['author_manifest_status']}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "pending_external_queries means the authoring template is ready, not that external blind testing is complete.",
        "External authors must not write expected_terms; scoring hints may be added later without editing query text.",
        "A completed external query file also requires an author/provenance manifest with no-access attestations.",
        "Generated queries are test inputs only, not reviewed knowledge.",
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
    kit = read_json(KIT_JSON) if KIT_JSON.exists() else {}
    template_rows = read_jsonl(TEMPLATE_JSONL) if TEMPLATE_JSONL.exists() else []
    template = validate_template(errors, template_rows, kit) if kit and template_rows else {}
    filled = validate_filled_queries(errors, kit) if kit else {
        "external_blind_query_status": "missing_kit",
        "filled_query_rows": 0,
        "unique_query_rows": 0,
    }
    author_manifest = validate_author_manifest(errors, FILLED_JSONL.exists())
    status = "pass" if not errors else "fail"
    if not errors and filled.get("external_blind_query_status") == "pending_external_queries":
        status = "pending_external_queries"
    result = {
        "external_blind_query_set_kit_check_status": status,
        "error_count": len(errors),
        "errors": errors,
        "artifacts": artifacts,
        "template": template,
        "filled_queries": filled,
        "author_manifest": author_manifest,
    }
    CHECK_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(result)
    print(f"external blind query set kit check status: {status}")
    print(f"error count: {len(errors)}")
    print(f"external blind query status: {filled.get('external_blind_query_status')}")
    return 0 if not errors else 1


if __name__ == "__main__":
    raise SystemExit(main())
