import json
from pathlib import Path


SANDBOX_DIR = Path(__file__).resolve().parents[1]
RESULTS_DIR = SANDBOX_DIR / "results"
CHECK_JSON = RESULTS_DIR / "phase_b_next_step_specs_check.json"
CHECK_MD = SANDBOX_DIR / "PHASE_B_NEXT_STEP_SPECS_CHECK.md"

REQUIRED_FILES = {
    "PHASE_B_EXTERNAL_VALIDATION_NEXT_STEPS.md": [
        "do_not_claim_original_yuxi_runtime_validated",
        "do_not_enter_c_lite_from_current_evidence",
        "Docker/Compose available locally, or a remote runner is explicitly provided.",
    ],
    "PHASE_B_EXTERNAL_BLIND_QUERY_SET_KIT.md": [
        "Create this filled file:",
        "queries_phase_b_external_blind.jsonl",
        "results/phase_b_external_blind_query_author_manifest.json",
        "Do not read existing Phase B query files.",
        "External author should not write expected_terms.",
        "This kit prepares external blind query generation.",
    ],
    "PHASE_B_READ_ONLY_ANSWER_LOOP_PILOT_SPEC.md": [
        "This is a pre-C-lite sandbox pilot concept, not a C-lite readiness claim.",
        "It is still not C-lite and does not imply C-lite is next.",
        "do_not_allow_writeback",
        "do_not_create_action_basis",
    ],
}


def add_error(errors: list[dict], code: str, detail: str) -> None:
    errors.append({"code": code, "detail": detail})


def validate_files(errors: list[dict]) -> dict:
    records = []
    for rel, required_markers in REQUIRED_FILES.items():
        path = SANDBOX_DIR / rel
        exists = path.exists()
        text = path.read_text(encoding="utf-8") if exists else ""
        records.append({"path": rel, "exists": exists, "bytes": path.stat().st_size if exists else 0})
        if not exists:
            add_error(errors, "missing_next_step_spec", rel)
            continue
        if path.stat().st_size == 0:
            add_error(errors, "empty_next_step_spec", rel)
        for marker in required_markers:
            if marker not in text:
                add_error(errors, "missing_required_marker", f"{rel}:{marker}")
    return {"files": records}


def write_report(result: dict) -> None:
    lines = [
        "---",
        "record_kind: sandbox_next_step_specs_check",
        f"status: {result['next_step_specs_check_status']}",
        "project_id: VAKS",
        "created_at: 2026-06-11",
        "truth_boundary: next_step_specs_check_not_c_lite_approval",
        "action_basis_allowed: false",
        "---",
        "",
        "# Phase B Next-Step Specs Check",
        "",
        "## Result",
        "",
        "```text",
        f"status: {result['next_step_specs_check_status']}",
        f"error count: {result['error_count']}",
        "```",
        "",
        "## Boundary",
        "",
        "```text",
        "These specs describe future tests.",
        "They do not validate original Yuxi runtime, enter C-lite, or approve writeback.",
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


def main() -> None:
    errors: list[dict] = []
    files = validate_files(errors)
    result = {
        "next_step_specs_check_status": "pass" if not errors else "fail",
        "error_count": len(errors),
        "errors": errors,
        "files": files,
    }
    CHECK_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    write_report(result)
    print(f"next-step specs check status: {result['next_step_specs_check_status']}")
    print(f"error count: {result['error_count']}")


if __name__ == "__main__":
    main()
