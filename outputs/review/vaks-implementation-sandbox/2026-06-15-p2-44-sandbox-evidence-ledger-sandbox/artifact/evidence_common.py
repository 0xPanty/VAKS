from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-44-sandbox-evidence-ledger-sandbox"
ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[3]
SANDBOX_ROOT = ROOT.parent

VERSION = "sandbox-evidence-ledger-v1"
TRUTH_BOUNDARY = "sandbox_evidence_ledger_not_enterprise_or_mainline_authority"
PURPOSE = "answer whether sandbox plan items landed, were tested, improved the system, and remain non-production"
WRITE_SCOPE = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"

REQUIRED_REPORTS = [
    "slice-plan.md",
    "source-map.md",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

PLAN_ITEMS = [
    ("P0-01", "retrieval receipt template sandbox", "2026-06-15-p0-01-retrieval-receipt-template-sandbox", "P0"),
    ("P0-02", "operation receipt template sandbox", "2026-06-15-p0-02-operation-receipt-template-sandbox", "P0"),
    ("P0-03", "body hash validator sandbox", "2026-06-15-p0-03-body-hash-validator-sandbox", "P0"),
    ("P0-04", "support boundary validator sandbox", "2026-06-15-p0-04-support-boundary-validator-sandbox", "P0"),
    ("P0-05", "action readiness validator sandbox", "2026-06-15-p0-05-action-readiness-validator-sandbox", "P0"),
    ("P0-06", "feedback validator sandbox", "2026-06-15-p0-06-feedback-validator-sandbox", "P0"),
    ("P0-07", "action-boundary failure matrix", "2026-06-15-p0-07-action-boundary-failure-matrix-sandbox", "P0"),
    ("P1-08", "retrieval/operation receipt validator pilot", "2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox", "P1"),
    ("P1-09", "read-only query loop pilot", "2026-06-15-p1-09-read-only-query-loop-pilot-sandbox", "P1"),
    ("P1-10", "runtime artifact exclusion test", "2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox", "P1"),
    ("P1-11", "semantic anchor support check", "2026-06-15-p1-11-semantic-anchor-support-check-sandbox", "P1"),
    ("P1.5-12", "robust RAG retrieval sandbox", "2026-06-15-p1-5-12-robust-rag-retrieval-sandbox", "P1.5"),
    ("P1.5-13", "local Obsidian graph retrieval / read-only MCP sandbox", "2026-06-15-p1-5-13-local-obsidian-graph-retrieval-readonly-mcp-sandbox", "P1.5"),
    ("P1.5-14", "raw intake parser router sandbox", "2026-06-15-p1-5-14-raw-intake-parser-router-sandbox", "P1.5"),
    ("P1.5-15", "markdown validation/search sidecar sandbox", "2026-06-15-p1-5-15-markdown-validation-search-sidecar-sandbox", "P1.5"),
    ("P1.5-16", "MISA runtime memory / VAKS bridge sandbox", "2026-06-15-p1-5-16-misa-runtime-memory-vaks-bridge-sandbox", "P1.5"),
    ("P2-17", "use-surface optimization pass", "2026-06-15-p2-17-use-surface-optimization-pass", "P2"),
    ("P2-18", "Bases cockpit prototype", "2026-06-15-p2-18-bases-cockpit-prototype", "P2"),
    ("P2-19", "product experience screening sandbox", "2026-06-15-p2-19-product-experience-screening-sandbox", "P2"),
    ("P2-20", "product workflow prototype", "2026-06-15-p2-20-product-workflow-prototype", "P2"),
]

IMPROVEMENTS = [
    {
        "id": "receipt_boundaries_are_visible",
        "label": "Receipt boundaries are visible",
        "summary": "Retrieval, operation, and promotion-adjacent paths now have inspectable receipts or dry-run packets.",
        "evidence_slice_ids": [
            "2026-06-15-p0-01-retrieval-receipt-template-sandbox",
            "2026-06-15-p0-02-operation-receipt-template-sandbox",
            "2026-06-15-p2-43-sandbox-promotion-request-dry-run-sandbox",
        ],
    },
    {
        "id": "validators_have_negative_cases",
        "label": "Validators have negative cases",
        "summary": "Validator slices include failure cases so a green check cannot hide known bad paths.",
        "evidence_slice_ids": [
            "2026-06-15-p0-03-body-hash-validator-sandbox",
            "2026-06-15-p0-04-support-boundary-validator-sandbox",
            "2026-06-15-p0-05-action-readiness-validator-sandbox",
            "2026-06-15-p0-06-feedback-validator-sandbox",
            "2026-06-15-p0-07-action-boundary-failure-matrix-sandbox",
        ],
    },
    {
        "id": "retrieval_is_separated_from_support",
        "label": "Retrieval is separated from support",
        "summary": "Retrieval can find candidates, but the ledger preserves that selected_by is not support.",
        "evidence_slice_ids": [
            "2026-06-15-p1-09-read-only-query-loop-pilot-sandbox",
            "2026-06-15-p1-11-semantic-anchor-support-check-sandbox",
            "2026-06-15-p1-5-12-robust-rag-retrieval-sandbox",
        ],
    },
    {
        "id": "product_surfaces_preserve_authority_boundaries",
        "label": "Product surfaces preserve authority boundaries",
        "summary": "Dashboards, briefs, and prototypes expose state without granting approval, truth, support, or action authority.",
        "evidence_slice_ids": [
            "2026-06-15-p2-18-bases-cockpit-prototype",
            "2026-06-15-p2-40-sandbox-product-grade-rollup-dashboard-sandbox",
            "2026-06-15-p2-42-sandbox-executive-readiness-brief-sandbox",
        ],
    },
    {
        "id": "formal_vault_paths_are_dry_run_only",
        "label": "Formal-vault paths are dry-run only",
        "summary": "Formal-vault planning, preflight, and request packets stay inside sandbox and do not touch the vault.",
        "evidence_slice_ids": [
            "2026-06-15-p2-24-formal-vault-write-plan-dry-run-sandbox",
            "2026-06-15-p2-28-formal-vault-execution-preflight-dry-run-sandbox",
            "2026-06-15-p2-32-formal-vault-execution-request-packet-sandbox",
        ],
    },
    {
        "id": "follow_up_agents_have_blind_run_regression",
        "label": "Follow-up agents have blind-run regression",
        "summary": "Independent follow-up-agent runs are tested so authority confusion is caught before continuation.",
        "evidence_slice_ids": [
            "2026-06-15-p2-38-formal-vault-follow-up-agent-blind-run-sandbox",
            "2026-06-15-p2-39-blind-run-regression-maintenance-sandbox",
        ],
    },
    {
        "id": "promotion_requires_separate_approval",
        "label": "Promotion requires separate approval",
        "summary": "The latest dry-run packet makes mainline, formal vault, template/tool, commit/push, and action-basis movement separately approvable.",
        "evidence_slice_ids": [
            "2026-06-15-p2-43-sandbox-promotion-request-dry-run-sandbox",
        ],
    },
]

OPERATION_FLAGS = [
    "formal_vault_read",
    "formal_vault_scan",
    "formal_vault_write",
    "formal_vault_hash",
    "formal_vault_snapshot",
    "formal_vault_state_check",
    "obsidian_sync",
    "commit",
    "push",
    "promotion",
    "dependency_install",
    "background_service",
    "mcp_write_tool",
    "hooks",
    "approval_collection",
    "user_instruction_collection",
    "user_wording_storage",
    "command_emitted",
    "execution_permission_granted",
    "execution_performed",
    "action_basis_creation",
    "reviewed_knowledge_creation",
    "evidence_support_creation",
    "mainline_merge",
    "dirty_tree_repair",
    "auto_advance",
]

REQUIRED_NON_CLAIMS = [
    "not enterprise production ready",
    "not mainline ready",
    "not formal vault approval",
    "not formal vault state",
    "not formal vault access",
    "not Obsidian sync",
    "not commit",
    "not push",
    "not promotion approval",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "not user approval",
    "not execution permission",
    "not auto advance",
]


def rel(path: Path) -> str:
    return path.resolve().relative_to(WORKSPACE).as_posix()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_status(path: Path) -> str | None:
    if not path.exists():
        return None
    match = re.search(r"^status:\s*(.+?)\s*$", path.read_text(encoding="utf-8", errors="ignore"), re.MULTILINE)
    return match.group(1).strip() if match else None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore") if path.exists() else ""


def product_pass_status(status: str | None, text: str) -> bool:
    return bool(status and status.startswith("pass_product_grade") and "PASS_PRODUCT_GRADE" in text)


def reviewer_pass_status(status: str | None, text: str) -> bool:
    return (
        status in {"pass", "reviewer_pass"}
        or (status is not None and status.startswith("review_pass"))
        or "REVIEW_PASS_NO_BLOCKER" in text
        or "REVIEWER_PASS" in text
        or "REVIEW_PASS" in text
    )


def boundary_pass_status(status: str | None, text: str) -> bool:
    return status in {"pass", "boundary_pass"} or "BOUNDARY_PASS_NO_BLOCKER" in text or "BOUNDARY_PASS" in text


def source_slice_dirs() -> list[Path]:
    return [
        path
        for path in sorted(SANDBOX_ROOT.iterdir(), key=lambda item: item.name)
        if path.is_dir() and path.name < SLICE_ID
    ]


def scan_slice(directory: Path) -> dict[str, Any]:
    reports = {name: directory / name for name in REQUIRED_REPORTS}
    product_text = read_text(reports["product-acceptance-report.md"])
    reviewer_text = read_text(reports["reviewer-report.md"])
    boundary_text = read_text(reports["boundary-audit.md"])
    report_statuses = {name: parse_status(path) for name, path in reports.items()}
    report_hashes = {name: sha256_file(path) if path.exists() else None for name, path in reports.items()}
    return {
        "slice_id": directory.name,
        "path": rel(directory),
        "missing_reports": [name for name, path in reports.items() if not path.exists()],
        "report_statuses": report_statuses,
        "report_hashes": report_hashes,
        "has_artifact_dir": (directory / "artifact").exists(),
        "has_prototype_dir": (directory / "prototype").exists(),
        "has_fixtures_dir": (directory / "fixtures").exists(),
        "has_failure_cases_dir": (directory / "failure-cases").exists(),
        "product_pass": product_pass_status(report_statuses["product-acceptance-report.md"], product_text),
        "reviewer_pass": reviewer_pass_status(report_statuses["reviewer-report.md"], reviewer_text),
        "boundary_pass": boundary_pass_status(report_statuses["boundary-audit.md"], boundary_text),
        "verification_present": reports["verification.md"].exists(),
        "revision_mentions": product_text.count("REVISE_BEFORE_NEXT")
        + product_text.count("REVIEWER_REVISE")
        + product_text.count("reviewer_revise"),
        "authority": {
            "enterprise_production_ready": False,
            "mainline_ready": False,
            "formal_vault_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "execution_permission": False,
        },
    }


def scan_all_slices() -> list[dict[str, Any]]:
    return [scan_slice(path) for path in source_slice_dirs()]


def source_by_id(slices: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
    return {item["slice_id"]: item for item in slices}


def plan_coverage(slices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = source_by_id(slices)
    rows = []
    for item_id, label, slice_id, phase in PLAN_ITEMS:
        source = by_id.get(slice_id)
        rows.append(
            {
                "item_id": item_id,
                "phase": phase,
                "label": label,
                "slice_id": slice_id,
                "slice_exists": source is not None,
                "product_pass": bool(source and source["product_pass"]),
                "verification_present": bool(source and source["verification_present"]),
                "reviewer_pass": bool(source and source["reviewer_pass"]),
                "boundary_pass": bool(source and source["boundary_pass"]),
                "has_artifact_or_prototype": bool(source and (source["has_artifact_dir"] or source["has_prototype_dir"])),
                "has_fixtures": bool(source and source["has_fixtures_dir"]),
                "has_failure_cases": bool(source and source["has_failure_cases_dir"]),
                "authority": "sandbox_only",
            }
        )
    return rows


def improvement_rows(slices: list[dict[str, Any]]) -> list[dict[str, Any]]:
    by_id = source_by_id(slices)
    rows = []
    for item in IMPROVEMENTS:
        evidence = [by_id.get(slice_id) for slice_id in item["evidence_slice_ids"]]
        rows.append(
            {
                **item,
                "direction": "positive",
                "authority": "sandbox_evidence_only",
                "all_evidence_product_pass": all(bool(row and row["product_pass"]) for row in evidence),
                "all_evidence_verified": all(bool(row and row["verification_present"]) for row in evidence),
                "non_claim": "positive improvement in sandbox only, not enterprise production proof",
            }
        )
    return rows


def default_ledger(view: str = "full-evidence-ledger") -> dict[str, Any]:
    slices = scan_all_slices()
    coverage = plan_coverage(slices)
    improvements = improvement_rows(slices)
    source_count = len(slices)
    product_pass_count = sum(1 for item in slices if item["product_pass"])
    verification_count = sum(1 for item in slices if item["verification_present"])
    reviewer_pass_count = sum(1 for item in slices if item["reviewer_pass"])
    boundary_pass_count = sum(1 for item in slices if item["boundary_pass"])
    original_pass_count = sum(1 for item in coverage if item["product_pass"])
    original_verified_count = sum(1 for item in coverage if item["verification_present"])
    return {
        "record_kind": "sandbox_evidence_ledger",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
        "view": view,
        "source_root": rel(SANDBOX_ROOT),
        "source_slice_count": source_count,
        "product_pass_count": product_pass_count,
        "verification_present_count": verification_count,
        "reviewer_pass_count": reviewer_pass_count,
        "boundary_pass_count": boundary_pass_count,
        "original_plan_item_count": len(PLAN_ITEMS),
        "original_plan_product_pass_count": original_pass_count,
        "original_plan_verification_count": original_verified_count,
        "hardening_slice_count": source_count - len(PLAN_ITEMS),
        "source_slices": slices,
        "original_plan_coverage": coverage,
        "positive_improvements": improvements,
        "plain_answer": {
            "all_original_plan_items_landed_in_sandbox": original_pass_count == len(PLAN_ITEMS),
            "all_current_sandbox_slices_product_pass": product_pass_count == source_count and source_count >= 43,
            "all_current_sandbox_slices_have_verification": verification_count == source_count and source_count >= 43,
            "all_current_sandbox_slices_have_reviewer_and_boundary": reviewer_pass_count == source_count and boundary_pass_count == source_count and source_count >= 43,
            "positive_improvement_supported": all(item["all_evidence_product_pass"] and item["all_evidence_verified"] for item in improvements),
            "enterprise_product_experience": "sandbox_product_grade_operator_experience_not_enterprise_production",
        },
        "readiness_flags": {
            "sandbox_product_grade_evidence_ready": True,
            "enterprise_production_ready": False,
            "mainline_ready": False,
            "formal_vault_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
        },
        "operation_performed_flags": {name: False for name in OPERATION_FLAGS},
        "required_non_claims": list(REQUIRED_NON_CLAIMS),
    }


def validate_ledger(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    expected = {
        "record_kind": "sandbox_evidence_ledger",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
        "source_root": rel(SANDBOX_ROOT),
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"{key}_mismatch")

    current = default_ledger(data.get("view", "full-evidence-ledger"))
    for key in [
        "source_slice_count",
        "product_pass_count",
        "verification_present_count",
        "reviewer_pass_count",
        "boundary_pass_count",
        "original_plan_item_count",
        "original_plan_product_pass_count",
        "original_plan_verification_count",
        "hardening_slice_count",
        "source_slices",
        "original_plan_coverage",
        "positive_improvements",
    ]:
        if data.get(key) != current.get(key):
            errors.append(f"{key}_mismatch")

    if data.get("source_slice_count", 0) < 43:
        errors.append("source_slice_count_too_low")
    if data.get("product_pass_count") != data.get("source_slice_count"):
        errors.append("not_all_sources_product_pass")
    if data.get("verification_present_count") != data.get("source_slice_count"):
        errors.append("not_all_sources_have_verification")
    if data.get("reviewer_pass_count") != data.get("source_slice_count"):
        errors.append("not_all_sources_have_reviewer_pass")
    if data.get("boundary_pass_count") != data.get("source_slice_count"):
        errors.append("not_all_sources_have_boundary_pass")
    if data.get("original_plan_item_count") != len(PLAN_ITEMS):
        errors.append("original_plan_item_count_mismatch")
    if data.get("original_plan_product_pass_count") != len(PLAN_ITEMS):
        errors.append("not_all_original_plan_items_product_pass")
    if data.get("original_plan_verification_count") != len(PLAN_ITEMS):
        errors.append("not_all_original_plan_items_have_verification")

    for row in data.get("original_plan_coverage", []):
        if row.get("slice_exists") is not True:
            errors.append(f"plan_slice_missing:{row.get('item_id')}")
        for key in [
            "product_pass",
            "verification_present",
            "reviewer_pass",
            "boundary_pass",
            "has_artifact_or_prototype",
            "has_fixtures",
            "has_failure_cases",
        ]:
            if row.get(key) is not True:
                errors.append(f"plan_item_{key}_not_true:{row.get('item_id')}")
        if row.get("authority") != "sandbox_only":
            errors.append(f"plan_item_authority_mismatch:{row.get('item_id')}")

    for row in data.get("source_slices", []):
        if row.get("missing_reports"):
            errors.append(f"source_missing_reports:{row.get('slice_id')}")
        for key in ["product_pass", "verification_present", "reviewer_pass", "boundary_pass"]:
            if row.get(key) is not True:
                errors.append(f"source_{key}_not_true:{row.get('slice_id')}")
        authority = row.get("authority", {})
        for key, value in authority.items():
            if value is not False:
                errors.append(f"source_authority_not_false:{row.get('slice_id')}:{key}")

    for row in data.get("positive_improvements", []):
        if row.get("direction") != "positive":
            errors.append(f"improvement_direction_mismatch:{row.get('id')}")
        if row.get("authority") != "sandbox_evidence_only":
            errors.append(f"improvement_authority_mismatch:{row.get('id')}")
        if row.get("all_evidence_product_pass") is not True:
            errors.append(f"improvement_evidence_not_product_pass:{row.get('id')}")
        if row.get("all_evidence_verified") is not True:
            errors.append(f"improvement_evidence_not_verified:{row.get('id')}")

    plain = data.get("plain_answer", {})
    for key in [
        "all_original_plan_items_landed_in_sandbox",
        "all_current_sandbox_slices_product_pass",
        "all_current_sandbox_slices_have_verification",
        "all_current_sandbox_slices_have_reviewer_and_boundary",
        "positive_improvement_supported",
    ]:
        if plain.get(key) is not True:
            errors.append(f"plain_answer_not_true:{key}")
    if plain.get("enterprise_product_experience") != "sandbox_product_grade_operator_experience_not_enterprise_production":
        errors.append("enterprise_product_experience_mismatch")

    flags = data.get("readiness_flags", {})
    if flags.get("sandbox_product_grade_evidence_ready") is not True:
        errors.append("sandbox_product_grade_evidence_ready_not_true")
    for flag in [
        "enterprise_production_ready",
        "mainline_ready",
        "formal_vault_ready",
        "reviewed_knowledge_ready",
        "evidence_support_ready",
        "action_basis_ready",
    ]:
        if flags.get(flag) is not False:
            errors.append(f"readiness_flag_not_false:{flag}")

    performed = data.get("operation_performed_flags", {})
    if set(performed) != set(OPERATION_FLAGS):
        errors.append("operation_performed_flags_mismatch")
    for name, value in performed.items():
        if value is not False:
            errors.append(f"operation_performed_not_false:{name}")

    if data.get("required_non_claims") != REQUIRED_NON_CLAIMS:
        errors.append("required_non_claims_mismatch")

    return errors


def make_failure_cases(base: dict[str, Any]) -> dict[str, list[str]]:
    cases: dict[str, list[str]] = {}
    index = 1

    def add(name: str, mutate, expected: list[str]) -> None:
        nonlocal index
        sample = copy.deepcopy(base)
        mutate(sample)
        filename = f"{index:03d}-{name}.json"
        write_json(ROOT / "failure-cases" / filename, sample)
        cases[filename] = expected
        index += 1

    for key in ["record_kind", "slice_id", "version", "truth_boundary", "purpose", "write_scope", "source_root"]:
        add(f"top-level-{key}", lambda sample, key=key: sample.__setitem__(key, "wrong"), [f"{key}_mismatch"])

    count_expectations = {
        "source_slice_count": ["source_slice_count_mismatch", "source_slice_count_too_low", "not_all_sources_product_pass", "not_all_sources_have_verification", "not_all_sources_have_reviewer_pass", "not_all_sources_have_boundary_pass"],
        "product_pass_count": ["product_pass_count_mismatch", "not_all_sources_product_pass"],
        "verification_present_count": ["verification_present_count_mismatch", "not_all_sources_have_verification"],
        "reviewer_pass_count": ["reviewer_pass_count_mismatch", "not_all_sources_have_reviewer_pass"],
        "boundary_pass_count": ["boundary_pass_count_mismatch", "not_all_sources_have_boundary_pass"],
        "original_plan_product_pass_count": ["original_plan_product_pass_count_mismatch", "not_all_original_plan_items_product_pass"],
        "original_plan_verification_count": ["original_plan_verification_count_mismatch", "not_all_original_plan_items_have_verification"],
    }
    for key, expected in count_expectations.items():
        add(f"count-{key}", lambda sample, key=key: sample.__setitem__(key, 0), expected)

    add("source-slices-drift", lambda sample: sample.__setitem__("source_slices", []), ["source_slices_mismatch"])
    add("plan-coverage-drift", lambda sample: sample.__setitem__("original_plan_coverage", []), ["original_plan_coverage_mismatch"])
    add("positive-improvements-drift", lambda sample: sample.__setitem__("positive_improvements", []), ["positive_improvements_mismatch"])

    add(
        "plan-item-product-pass-false",
        lambda sample: sample["original_plan_coverage"][0].__setitem__("product_pass", False),
        ["original_plan_coverage_mismatch", f"plan_item_product_pass_not_true:{base['original_plan_coverage'][0]['item_id']}"],
    )
    add(
        "plan-item-missing-fixtures",
        lambda sample: sample["original_plan_coverage"][0].__setitem__("has_fixtures", False),
        ["original_plan_coverage_mismatch", f"plan_item_has_fixtures_not_true:{base['original_plan_coverage'][0]['item_id']}"],
    )
    add(
        "source-product-pass-false",
        lambda sample: sample["source_slices"][0].__setitem__("product_pass", False),
        ["source_slices_mismatch", f"source_product_pass_not_true:{base['source_slices'][0]['slice_id']}"],
    )
    add(
        "source-boundary-pass-false",
        lambda sample: sample["source_slices"][0].__setitem__("boundary_pass", False),
        ["source_slices_mismatch", f"source_boundary_pass_not_true:{base['source_slices'][0]['slice_id']}"],
    )
    add(
        "source-mainline-authority-true",
        lambda sample: sample["source_slices"][0]["authority"].__setitem__("mainline_ready", True),
        ["source_slices_mismatch", f"source_authority_not_false:{base['source_slices'][0]['slice_id']}:mainline_ready"],
    )
    add(
        "improvement-not-positive",
        lambda sample: sample["positive_improvements"][0].__setitem__("direction", "neutral"),
        ["positive_improvements_mismatch", f"improvement_direction_mismatch:{base['positive_improvements'][0]['id']}"],
    )
    add(
        "improvement-evidence-not-pass",
        lambda sample: sample["positive_improvements"][0].__setitem__("all_evidence_product_pass", False),
        ["positive_improvements_mismatch", f"improvement_evidence_not_product_pass:{base['positive_improvements'][0]['id']}"],
    )

    for key in [
        "all_original_plan_items_landed_in_sandbox",
        "all_current_sandbox_slices_product_pass",
        "all_current_sandbox_slices_have_verification",
        "all_current_sandbox_slices_have_reviewer_and_boundary",
        "positive_improvement_supported",
    ]:
        add(f"plain-answer-{key}-false", lambda sample, key=key: sample["plain_answer"].__setitem__(key, False), [f"plain_answer_not_true:{key}"])
    add(
        "plain-answer-enterprise-claim",
        lambda sample: sample["plain_answer"].__setitem__("enterprise_product_experience", "enterprise_production_ready"),
        ["enterprise_product_experience_mismatch"],
    )

    for flag in [
        "enterprise_production_ready",
        "mainline_ready",
        "formal_vault_ready",
        "reviewed_knowledge_ready",
        "evidence_support_ready",
        "action_basis_ready",
    ]:
        add(f"readiness-{flag}-true", lambda sample, flag=flag: sample["readiness_flags"].__setitem__(flag, True), [f"readiness_flag_not_false:{flag}"])

    for op in OPERATION_FLAGS:
        add(f"operation-{op}-performed", lambda sample, op=op: sample["operation_performed_flags"].__setitem__(op, True), [f"operation_performed_not_false:{op}"])

    for non_claim in REQUIRED_NON_CLAIMS:
        add(f"missing-non-claim-{non_claim.replace(' ', '-')}", lambda sample, non_claim=non_claim: sample["required_non_claims"].remove(non_claim), ["required_non_claims_mismatch"])
    add("extra-non-claim", lambda sample: sample["required_non_claims"].append("unexpected expansion"), ["required_non_claims_mismatch"])

    return cases


def reset_generated() -> None:
    for directory in ["fixtures", "failure-cases", "prototype/sandbox-evidence-ledger", "ledger-packets"]:
        path = ROOT / directory
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)


def validate_failure_cases() -> dict[str, Any]:
    oracle_path = ROOT / "artifact" / "failure-case-oracle.json"
    failure_dir = ROOT / "failure-cases"
    if not oracle_path.exists():
        return {"count": 0, "actual_file_count": 0, "orphan_count": 0, "mismatches": [{"file": "failure-case-oracle.json", "expected": ["oracle_present"], "actual": ["missing_oracle"]}]}
    oracle = read_json(oracle_path).get("cases", {})
    actual_files = {path.name for path in failure_dir.glob("*.json")} if failure_dir.exists() else set()
    if not oracle:
        return {"count": 0, "actual_file_count": len(actual_files), "orphan_count": len(actual_files), "mismatches": [{"file": "failure-case-oracle.json", "expected": ["oracle_non_empty"], "actual": ["empty_oracle"]}]}
    expected_files = set(oracle)
    mismatches = []
    for extra in sorted(actual_files - expected_files):
        mismatches.append({"file": extra, "expected": ["not_present_outside_oracle"], "actual": ["orphan_failure_case_file"]})
    for name, expected in oracle.items():
        path = failure_dir / name
        if not path.exists():
            mismatches.append({"file": name, "expected": expected, "actual": ["missing_failure_case"]})
            continue
        actual = validate_ledger(read_json(path))
        if sorted(actual) != sorted(expected):
            mismatches.append({"file": name, "expected": expected, "actual": actual})
    return {"count": len(oracle), "actual_file_count": len(actual_files), "orphan_count": len(actual_files - expected_files), "mismatches": mismatches}


def validate_fixtures() -> dict[str, Any]:
    details = []
    errors = []
    for path in sorted((ROOT / "fixtures").glob("*.json")):
        fixture_errors = validate_ledger(read_json(path))
        details.append({"file": path.name, "errors": fixture_errors})
        if fixture_errors:
            errors.append({"file": path.name, "errors": fixture_errors})
    if not details:
        errors.append({"file": "fixtures", "errors": ["missing_positive_fixtures"]})
    return {"count": len(details), "fixtures": details, "errors": errors}


def validate_readout() -> dict[str, Any]:
    path = ROOT / "ledger-packets" / "plain-answer.md"
    issues: list[str] = []
    if not path.exists():
        return {"path": str(path), "issues": ["missing_readout"]}
    text = path.read_text(encoding="utf-8", errors="ignore")
    for phrase in [
        "all original plan items landed in sandbox",
        "all current sandbox slices have verification",
        "positive improvement is supported",
        "not enterprise production",
        "not mainline ready",
        "not action basis",
    ]:
        if phrase not in text:
            issues.append(f"readout_phrase_missing:{phrase}")
    return {"path": str(path), "issues": issues}


def validate_prototype() -> dict[str, Any]:
    prototype = ROOT / "prototype" / "sandbox-evidence-ledger"
    issues: list[str] = []
    expected = default_ledger()
    for item in ["index.html", "app.js", "receipt.json"]:
        if not (prototype / item).exists():
            issues.append(f"missing_prototype_file:{item}")
    if (prototype / "index.html").exists():
        html_raw = (prototype / "index.html").read_text(encoding="utf-8", errors="ignore")
        html = html_raw.lower()
        for forbidden in ["<form", "download", "contenteditable", "<a ", "h:\\obsidian", "onclick"]:
            if forbidden in html:
                issues.append(f"prototype_forbidden:{forbidden}")
        if html.count("data-plan-item=") != len(PLAN_ITEMS):
            issues.append("prototype_plan_item_count_mismatch")
        if html.count("data-source-slice=") != expected["source_slice_count"]:
            issues.append("prototype_source_slice_count_mismatch")
        if html.count("data-improvement=") != len(IMPROVEMENTS):
            issues.append("prototype_improvement_count_mismatch")
        for value in [
            str(expected["source_slice_count"]),
            str(expected["product_pass_count"]),
            str(expected["verification_present_count"]),
            str(expected["original_plan_product_pass_count"]),
        ]:
            if f">{value}<" not in html_raw:
                issues.append(f"prototype_summary_value_missing:{value}")
        for phrase in ["not enterprise production", "not mainline ready", "not action basis"]:
            if phrase not in html:
                issues.append(f"prototype_boundary_phrase_missing:{phrase}")
    if (prototype / "receipt.json").exists():
        receipt = read_json(prototype / "receipt.json")
        for flag in [
            "enterprise_production_ready",
            "mainline_ready",
            "formal_vault_accessed",
            "sync_performed",
            "commit_performed",
            "push_performed",
            "promotion_performed",
            "action_basis_created",
            "reviewed_knowledge_created",
            "evidence_support_created",
            "auto_advanced",
        ]:
            if receipt.get(flag) is not False:
                issues.append(f"prototype_receipt_flag_not_false:{flag}")
        if receipt.get("source_slice_count") != expected["source_slice_count"]:
            issues.append("prototype_receipt_source_count_mismatch")
        if receipt.get("required_non_claims") != REQUIRED_NON_CLAIMS:
            issues.append("prototype_receipt_non_claims_mismatch")
    return {"prototype_path": str(prototype), "issues": issues}


def validate_required_reports(final_gate: bool = False) -> dict[str, Any]:
    required = {
        "slice-plan.md": "built_pending_review",
        "source-map.md": "built_pending_review",
        "verification.md": "local_verification_passed_pending_review",
    }
    if final_gate:
        required.update(
            {
                "reviewer-report.md": "reviewer_pass",
                "boundary-audit.md": "boundary_pass",
                "product-acceptance-report.md": "pass_product_grade",
                "next-step.md": "pass_product_grade_pending_user_next_slice_decision",
            }
        )
    statuses: dict[str, str | None] = {}
    issues: list[str] = []
    for name, expected in required.items():
        status = parse_status(ROOT / name)
        statuses[name] = status
        if status != expected:
            issues.append(f"bad_status:{name}:{status}:expected:{expected}")
    return {"statuses": statuses, "issues": issues}


def validate_all(final_gate: bool = False) -> dict[str, Any]:
    fixture = ROOT / "fixtures" / "valid-evidence-ledger.json"
    config_errors = validate_ledger(read_json(fixture)) if fixture.exists() else ["missing_valid_fixture"]
    ledger_path = ROOT / "artifact" / "evidence-ledger.json"
    ledger_errors = validate_ledger(read_json(ledger_path)) if ledger_path.exists() else ["missing_evidence_ledger"]
    fixtures = validate_fixtures()
    failure_cases = validate_failure_cases()
    prototype = validate_prototype()
    readout = validate_readout()
    reports = validate_required_reports(final_gate=final_gate)
    failures: list[str] = []
    failures.extend(config_errors)
    failures.extend([f"evidence_ledger_error:{item}" for item in ledger_errors])
    failures.extend([f"fixture_error:{item['file']}" for item in fixtures["errors"]])
    failures.extend([f"failure_case_mismatch:{item['file']}" for item in failure_cases["mismatches"]])
    failures.extend(prototype["issues"])
    failures.extend(readout["issues"])
    failures.extend(reports["issues"])
    current = default_ledger()
    return {
        "slice_id": SLICE_ID,
        "passed": not failures,
        "failures": failures,
        "valid_config_errors": config_errors,
        "evidence_ledger_errors": ledger_errors,
        "positive_fixtures": fixtures,
        "failure_cases": failure_cases,
        "prototype": prototype,
        "readout": readout,
        "required_reports": reports,
        "source_summary": {
            "source_slice_count": current["source_slice_count"],
            "product_pass_count": current["product_pass_count"],
            "verification_present_count": current["verification_present_count"],
            "original_plan_item_count": current["original_plan_item_count"],
            "original_plan_product_pass_count": current["original_plan_product_pass_count"],
            "hardening_slice_count": current["hardening_slice_count"],
        },
        "plain_answer": current["plain_answer"],
        "non_claims": REQUIRED_NON_CLAIMS,
    }
