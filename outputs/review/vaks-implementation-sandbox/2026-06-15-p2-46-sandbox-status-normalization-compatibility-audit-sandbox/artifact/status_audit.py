from __future__ import annotations

import copy
import hashlib
import json
import re
import shutil
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-46-sandbox-status-normalization-compatibility-audit-sandbox"
SOURCE_LEDGER_SLICE_ID = "2026-06-15-p2-44-sandbox-evidence-ledger-sandbox"
SOURCE_HANDOFF_SLICE_ID = "2026-06-15-p2-45-sandbox-release-candidate-handoff-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = ROOT.parents[3]
SANDBOX_ROOT = ROOT.parent
LEDGER_ROOT = SANDBOX_ROOT / SOURCE_LEDGER_SLICE_ID
HANDOFF_ROOT = SANDBOX_ROOT / SOURCE_HANDOFF_SLICE_ID
LEDGER_PATH = LEDGER_ROOT / "artifact" / "evidence-ledger.json"
HANDOFF_PACKET_PATH = HANDOFF_ROOT / "handoff-packets" / "release-candidate-handoff.md"

VERSION = "sandbox-status-normalization-compatibility-audit-v1"
TRUTH_BOUNDARY = "status_normalization_is_display_compatibility_not_re_acceptance_or_authority"
PURPOSE = "normalize legacy sandbox report statuses for human and follow-up-agent interpretation without editing old slices"
WRITE_SCOPE = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"

REPORTS = [
    "slice-plan.md",
    "source-map.md",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]

ALLOWED_VIEWS = {
    "status-normalization-audit",
    "agent-interpretation-guide",
    "ambiguous-status-inventory",
}

REQUIRED_FIXTURES = {
    "valid-status-normalization-audit.json": "status-normalization-audit",
    "valid-agent-interpretation-guide.json": "agent-interpretation-guide",
    "valid-ambiguous-status-inventory.json": "ambiguous-status-inventory",
}

TOP_LEVEL_FIELDS = {
    "record_kind",
    "slice_id",
    "version",
    "truth_boundary",
    "purpose",
    "write_scope",
    "view",
    "source_snapshot",
    "normalization_policy",
    "report_inventory",
    "canonical_summary",
    "ambiguous_status_inventory",
    "agent_rules",
    "readiness_flags",
    "operation_performed_flags",
    "required_non_claims",
    "operator_note",
}

READINESS_FLAGS = {
    "status_normalization_ready",
    "re_acceptance_performed",
    "enterprise_production_ready",
    "mainline_ready",
    "formal_vault_ready",
    "reviewed_knowledge_ready",
    "evidence_support_ready",
    "action_basis_ready",
    "release_approved",
    "promotion_approved",
}

OPERATION_FLAGS = [
    "legacy_slice_modified",
    "mainline_merge",
    "formal_vault_read",
    "formal_vault_write",
    "obsidian_sync",
    "commit",
    "push",
    "promotion",
    "dependency_install",
    "background_service",
    "mcp_write_tool",
    "hooks",
    "re_acceptance_run",
    "product_status_overwritten",
    "auto_advance",
]

REQUIRED_NON_CLAIMS = [
    "not re-acceptance",
    "not release approval",
    "not promotion approval",
    "not mainline ready",
    "not enterprise production ready",
    "not formal vault approval",
    "not Obsidian sync",
    "not commit",
    "not push",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "not old-slice edit",
    "not auto advance",
]

PRODUCT_PASS_STATUSES = {
    "pass_product_grade",
    "pass_product_grade_round_2",
    "pass_product_grade_after_revision",
}

REVIEWER_PASS_STATUSES = {
    "pass",
    "review_pass_no_blocker_round_2",
    "review_pass_no_blocker",
    "review_pass_no_blocker_after_revision",
    "review_pass_no_blocker_after_refinement",
    "review_pass_no_blocker_after_repair",
    "reviewer_pass_no_blocker_after_product_revision",
    "reviewer_pass_no_blocker",
    "review_pass_after_product_revision",
    "review_pass_after_third_revision",
    "review_pass_after_first_revision",
    "reviewer_pass",
}

BOUNDARY_PASS_STATUSES = {
    "pass",
    "boundary_pass_no_blocker_round_2",
    "boundary_pass_no_blocker",
    "boundary_pass_no_blocker_after_revision",
    "boundary_pass_no_blocker_after_refinement",
    "boundary_pass_no_blocker_after_repair",
    "boundary_pass_no_blocker_after_product_revision",
    "boundary_pass_after_product_revision",
    "boundary_pass_after_third_revision",
    "boundary_pass_after_first_revision",
    "boundary_pass",
}

VERIFICATION_PASS_STATUSES = {
    "pass",
    "local_verification_pass",
    "local_verification_passed",
    "local_verification_passed_pending_review",
    "local_verification_passed_pending_reacceptance",
    "local_verification_passed_pending_recheck_after_boundary_repair",
    "local_verification_passed_reviewer_boundary_product_passed",
    "local_verification_reviewer_boundary_product_acceptance_passed",
    "local_verification_passed_after_second_reviewer_revision_pending_revalidation",
    "local_verification_passed_browser_file_url_smoke_blocked_by_policy",
    "local_verification_and_final_gate_passed",
}

PLANNING_WORK_STATE_STATUSES = {
    "draft",
    "drafted",
    "draft_for_review",
    "in_progress",
    "ready_for_recheck",
    "implemented_pending_review",
    "built_pending_verification",
    "built_pending_review",
}

NEXT_STEP_STATUSES = {
    "pending_acceptance",
    "pending_product_acceptance",
    "pending_product_reacceptance",
    "pass_product_grade_next_slice_allowed",
    "pass_product_grade_enter_p2_17",
    "pass_product_grade_enter_p2_18",
    "pass_product_grade_next_p2_19",
    "pass_product_grade_next_p2_20",
    "sandbox_series_complete_pending_user_mainline_decision",
    "pass_product_grade_pending_user_mainline_decision",
    "pass_product_grade_pending_user_next_slice_decision",
}


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


def write_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip() + "\n", encoding="utf-8")


def parse_status(path: Path) -> str | None:
    if not path.exists():
        return None
    match = re.search(r"^status:\s*(.+?)\s*$", path.read_text(encoding="utf-8", errors="ignore"), re.MULTILINE)
    return match.group(1).strip() if match else None


def normalize_report_status(report_name: str, raw_status: str | None) -> dict[str, Any]:
    raw = "" if raw_status is None else str(raw_status).strip().lower()
    if raw_status is None:
        return {
            "canonical": "legacy_missing_frontmatter_status",
            "gate_role": "non_gate_report_metadata",
            "blocking": False,
            "reason": "missing legacy frontmatter status is interpreted through gate booleans, not as failure",
        }
    if report_name == "product-acceptance-report.md" and raw in PRODUCT_PASS_STATUSES:
        return {"canonical": "product_pass", "gate_role": "product_acceptance_gate", "blocking": False, "reason": "Product Acceptance PASS is explicit"}
    if report_name == "reviewer-report.md" and raw in REVIEWER_PASS_STATUSES:
        return {"canonical": "reviewer_pass", "gate_role": "reviewer_gate", "blocking": False, "reason": "Reviewer PASS is explicit"}
    if report_name == "boundary-audit.md" and raw in BOUNDARY_PASS_STATUSES:
        return {"canonical": "boundary_pass", "gate_role": "boundary_gate", "blocking": False, "reason": "Boundary PASS is explicit"}
    if report_name == "verification.md" and raw in VERIFICATION_PASS_STATUSES:
        return {"canonical": "verification_pass", "gate_role": "local_verification_gate", "blocking": False, "reason": "Verification PASS is explicit"}
    if report_name in {"slice-plan.md", "source-map.md"} and raw == "pass_product_grade":
        return {
            "canonical": "legacy_gate_label_in_non_gate_report",
            "gate_role": "planning_metadata_not_acceptance_gate",
            "blocking": False,
            "reason": "legacy planning/source-map status reused a gate label; actual gate is still Product Acceptance report",
        }
    if report_name in {"slice-plan.md", "source-map.md"} and raw in PLANNING_WORK_STATE_STATUSES:
        return {
            "canonical": "legacy_work_state_not_gate",
            "gate_role": "planning_metadata_not_acceptance_gate",
            "blocking": False,
            "reason": "planning/source-map status is legacy work-state metadata; gate booleans carry pass/fail",
        }
    if report_name == "next-step.md" and raw in NEXT_STEP_STATUSES:
        return {
            "canonical": "continuation_instruction_not_acceptance_gate",
            "gate_role": "next_step_instruction_not_acceptance_gate",
            "blocking": False,
            "reason": "next-step pending means do not auto-advance, not Product Acceptance failure",
        }
    return {
        "canonical": "unknown_status",
        "gate_role": "unknown",
        "blocking": True,
        "reason": "status string is outside the compatibility policy",
    }


def legacy_slice_entry(item: dict[str, Any]) -> dict[str, Any]:
    statuses = item.get("report_statuses", {})
    normalized = {name: normalize_report_status(name, statuses.get(name)) for name in REPORTS}
    gates = {
        "product_pass": item.get("product_pass") is True,
        "reviewer_pass": item.get("reviewer_pass") is True,
        "boundary_pass": item.get("boundary_pass") is True,
        "verification_present": item.get("verification_present") is True,
    }
    return {
        "slice_id": item.get("slice_id"),
        "path": item.get("path"),
        "source": "p2-44-ledger",
        "report_statuses": {name: statuses.get(name) for name in REPORTS},
        "normalized_report_statuses": normalized,
        "gates": gates,
        "gate_pass": all(gates.values()),
        "interpretation": "product_passed_legacy_statuses_are_display_metadata" if all(gates.values()) else "gate_failure_or_incomplete",
    }


def p45_entry() -> dict[str, Any]:
    statuses = {name: parse_status(HANDOFF_ROOT / name) for name in REPORTS}
    normalized = {name: normalize_report_status(name, statuses.get(name)) for name in REPORTS}
    gates = {
        "product_pass": statuses.get("product-acceptance-report.md") == "pass_product_grade",
        "reviewer_pass": statuses.get("reviewer-report.md") == "reviewer_pass",
        "boundary_pass": statuses.get("boundary-audit.md") == "boundary_pass",
        "verification_present": statuses.get("verification.md") == "local_verification_passed_pending_review",
    }
    return {
        "slice_id": SOURCE_HANDOFF_SLICE_ID,
        "path": rel(HANDOFF_ROOT),
        "source": "p2-45-live-files",
        "report_statuses": statuses,
        "normalized_report_statuses": normalized,
        "gates": gates,
        "gate_pass": all(gates.values()),
        "interpretation": "product_passed_release_candidate_handoff" if all(gates.values()) else "gate_failure_or_incomplete",
    }


def source_snapshot() -> dict[str, Any]:
    ledger = read_json(LEDGER_PATH)
    return {
        "ledger_slice_id": SOURCE_LEDGER_SLICE_ID,
        "ledger_path": rel(LEDGER_PATH),
        "ledger_sha256": sha256_file(LEDGER_PATH),
        "ledger_source_slice_count": ledger.get("source_slice_count"),
        "ledger_product_pass_count": ledger.get("product_pass_count"),
        "ledger_verification_present_count": ledger.get("verification_present_count"),
        "handoff_slice_id": SOURCE_HANDOFF_SLICE_ID,
        "handoff_packet_path": rel(HANDOFF_PACKET_PATH),
        "handoff_packet_sha256": sha256_file(HANDOFF_PACKET_PATH),
        "handoff_product_status": parse_status(HANDOFF_ROOT / "product-acceptance-report.md"),
    }


def build_inventory() -> list[dict[str, Any]]:
    ledger = read_json(LEDGER_PATH)
    inventory = [legacy_slice_entry(item) for item in ledger.get("source_slices", [])]
    inventory.append(p45_entry())
    return inventory


def summarize_inventory(inventory: list[dict[str, Any]]) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    raw_counter: dict[str, Counter[str]] = defaultdict(Counter)
    canonical_counter: Counter[str] = Counter()
    ambiguous: list[dict[str, Any]] = []
    for item in inventory:
        for report, raw_status in item["report_statuses"].items():
            raw_counter[report][str(raw_status)] += 1
            normalized = item["normalized_report_statuses"][report]
            canonical_counter[normalized["canonical"]] += 1
            if normalized["canonical"] in {
            "legacy_missing_frontmatter_status",
            "legacy_gate_label_in_non_gate_report",
            "legacy_work_state_not_gate",
                "continuation_instruction_not_acceptance_gate",
                "legacy_ambiguous_nonblocking_status",
            }:
                ambiguous.append(
                    {
                        "slice_id": item["slice_id"],
                        "report": report,
                        "raw_status": raw_status,
                        "canonical": normalized["canonical"],
                        "blocking": normalized["blocking"],
                        "reason": normalized["reason"],
                    }
                )
    summary = {
        "examined_slice_count": len(inventory),
        "all_examined_gate_pass": all(item["gate_pass"] for item in inventory),
        "gate_pass_count": sum(1 for item in inventory if item["gate_pass"]),
        "legacy_ambiguous_status_count": len(ambiguous),
        "unknown_status_count": canonical_counter.get("unknown_status", 0),
        "canonical_status_counts": dict(sorted(canonical_counter.items())),
        "raw_status_counts_by_report": {report: dict(counter) for report, counter in sorted(raw_counter.items())},
    }
    return summary, ambiguous


def default_audit(view: str = "status-normalization-audit") -> dict[str, Any]:
    inventory = build_inventory()
    summary, ambiguous = summarize_inventory(inventory)
    return {
        "record_kind": "sandbox_status_normalization_compatibility_audit",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
        "view": view,
        "source_snapshot": source_snapshot(),
        "normalization_policy": {
            "principle": "raw report statuses are display compatibility inputs; Product Acceptance remains the gate",
            "legacy_pending_or_draft": "nonblocking_metadata_when_gate_booleans_pass",
            "missing_source_map_status": "legacy_missing_frontmatter_status_not_product_failure",
            "next_step_pending": "means stop before auto-advance, not failed acceptance",
            "unknown_status": "blocking_until_mapped_or_explained",
        },
        "report_inventory": inventory,
        "canonical_summary": summary,
        "ambiguous_status_inventory": ambiguous,
        "agent_rules": [
            "run the slice verifier before interpreting the audit",
            "do not infer failure from legacy draft, pending, or missing planning statuses when gate booleans pass",
            "do not infer approval or authority from status normalization",
            "unknown statuses are blocking until a later sandbox maps them",
            "do not edit old slices to make statuses look cleaner",
        ],
        "readiness_flags": {
            "status_normalization_ready": True,
            "re_acceptance_performed": False,
            "enterprise_production_ready": False,
            "mainline_ready": False,
            "formal_vault_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "release_approved": False,
            "promotion_approved": False,
        },
        "operation_performed_flags": {name: False for name in OPERATION_FLAGS},
        "required_non_claims": list(REQUIRED_NON_CLAIMS),
    }


def validate_audit(data: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    for key in sorted(set(data) - TOP_LEVEL_FIELDS):
        errors.append(f"unknown_top_level_field:{key}")
    view = data.get("view")
    if view not in ALLOWED_VIEWS:
        errors.append(f"view_not_allowed:{view}")
    if "operator_note" in data:
        note = data.get("operator_note")
        if not isinstance(note, str) or "sandbox only" not in note:
            errors.append("operator_note_not_sandbox_only")

    expected = {
        "record_kind": "sandbox_status_normalization_compatibility_audit",
        "slice_id": SLICE_ID,
        "version": VERSION,
        "truth_boundary": TRUTH_BOUNDARY,
        "purpose": PURPOSE,
        "write_scope": WRITE_SCOPE,
    }
    for key, value in expected.items():
        if data.get(key) != value:
            errors.append(f"{key}_mismatch")

    current = default_audit(view if view in ALLOWED_VIEWS else "status-normalization-audit")
    for key in [
        "source_snapshot",
        "normalization_policy",
        "report_inventory",
        "canonical_summary",
        "ambiguous_status_inventory",
        "agent_rules",
    ]:
        if data.get(key) != current.get(key):
            errors.append(f"{key}_mismatch")

    summary = data.get("canonical_summary", {})
    if summary.get("examined_slice_count") != 44:
        errors.append("examined_slice_count_mismatch")
    if summary.get("gate_pass_count") != 44:
        errors.append("gate_pass_count_mismatch")
    if summary.get("all_examined_gate_pass") is not True:
        errors.append("all_examined_gate_pass_not_true")
    if summary.get("legacy_ambiguous_status_count", 0) <= 0:
        errors.append("legacy_ambiguous_status_inventory_missing")
    if summary.get("unknown_status_count") != 0:
        errors.append("unknown_status_present")

    for item in data.get("report_inventory", []):
        if item.get("gate_pass") is not True:
            errors.append(f"slice_gate_not_pass:{item.get('slice_id')}")
        for report, normalized in item.get("normalized_report_statuses", {}).items():
            if normalized.get("canonical") == "unknown_status":
                errors.append(f"unknown_status:{item.get('slice_id')}:{report}")
            if normalized.get("blocking") is True:
                errors.append(f"blocking_status:{item.get('slice_id')}:{report}")

    for item in data.get("ambiguous_status_inventory", []):
        if item.get("blocking") is not False:
            errors.append(f"ambiguous_status_marked_blocking:{item.get('slice_id')}:{item.get('report')}")

    rules = data.get("agent_rules", [])
    required_rule_fragments = [
        "do not infer failure",
        "do not infer approval",
        "unknown statuses are blocking",
        "do not edit old slices",
    ]
    for fragment in required_rule_fragments:
        if not any(fragment in str(rule) for rule in rules):
            errors.append(f"agent_rule_missing:{fragment}")

    flags = data.get("readiness_flags", {})
    if set(flags) != READINESS_FLAGS:
        errors.append("readiness_flags_keys_mismatch")
    if flags.get("status_normalization_ready") is not True:
        errors.append("status_normalization_ready_not_true")
    for flag in READINESS_FLAGS - {"status_normalization_ready"}:
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


def reset_generated() -> None:
    for directory in ["fixtures", "failure-cases", "prototype/status-normalization-audit", "readouts"]:
        path = ROOT / directory
        if path.exists():
            shutil.rmtree(path)
        path.mkdir(parents=True, exist_ok=True)


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

    def set_report_status(sample: dict[str, Any], report: str, raw_status: str) -> None:
        sample["report_inventory"][0]["report_statuses"][report] = raw_status
        sample["report_inventory"][0]["normalized_report_statuses"][report] = normalize_report_status(report, raw_status)

    for key in ["record_kind", "slice_id", "version", "truth_boundary", "purpose", "write_scope"]:
        add(f"top-level-{key}", lambda sample, key=key: sample.__setitem__(key, "wrong"), [f"{key}_mismatch"])
    add("bad-view", lambda sample: sample.__setitem__("view", "wrong"), ["view_not_allowed:wrong"])
    add("extra-release-approval-claim", lambda sample: sample.__setitem__("release_approval_claim", True), ["unknown_top_level_field:release_approval_claim"])
    add("source-snapshot-drift", lambda sample: sample.__setitem__("source_snapshot", {}), ["source_snapshot_mismatch"])
    add("inventory-drift", lambda sample: sample.__setitem__("report_inventory", []), ["report_inventory_mismatch"])
    add("summary-count-drift", lambda sample: sample["canonical_summary"].__setitem__("examined_slice_count", 43), ["canonical_summary_mismatch", "examined_slice_count_mismatch"])
    add("gate-pass-count-drift", lambda sample: sample["canonical_summary"].__setitem__("gate_pass_count", 43), ["canonical_summary_mismatch", "gate_pass_count_mismatch"])
    add("unknown-status-count", lambda sample: sample["canonical_summary"].__setitem__("unknown_status_count", 1), ["canonical_summary_mismatch", "unknown_status_present"])
    add("legacy-ambiguity-removed", lambda sample: sample["canonical_summary"].__setitem__("legacy_ambiguous_status_count", 0), ["canonical_summary_mismatch", "legacy_ambiguous_status_inventory_missing"])
    add("slice-gate-false", lambda sample: sample["report_inventory"][0].__setitem__("gate_pass", False), ["report_inventory_mismatch", f"slice_gate_not_pass:{base['report_inventory'][0]['slice_id']}"])
    add("normalized-status-blocking", lambda sample: sample["report_inventory"][0]["normalized_report_statuses"]["slice-plan.md"].__setitem__("blocking", True), ["report_inventory_mismatch", f"blocking_status:{base['report_inventory'][0]['slice_id']}:slice-plan.md"])
    add("normalized-status-unknown", lambda sample: sample["report_inventory"][0]["normalized_report_statuses"]["slice-plan.md"].__setitem__("canonical", "unknown_status"), ["report_inventory_mismatch", f"unknown_status:{base['report_inventory'][0]['slice_id']}:slice-plan.md"])
    add("negative-product-status-not-pass", lambda sample: set_report_status(sample, "product-acceptance-report.md", "not_pass_product_grade"), ["report_inventory_mismatch", f"unknown_status:{base['report_inventory'][0]['slice_id']}:product-acceptance-report.md", f"blocking_status:{base['report_inventory'][0]['slice_id']}:product-acceptance-report.md"])
    add("negative-verification-status-not-passed", lambda sample: set_report_status(sample, "verification.md", "not_passed"), ["report_inventory_mismatch", f"unknown_status:{base['report_inventory'][0]['slice_id']}:verification.md", f"blocking_status:{base['report_inventory'][0]['slice_id']}:verification.md"])
    add("negative-reviewer-status-failed", lambda sample: set_report_status(sample, "reviewer-report.md", "review_pass_failed"), ["report_inventory_mismatch", f"unknown_status:{base['report_inventory'][0]['slice_id']}:reviewer-report.md", f"blocking_status:{base['report_inventory'][0]['slice_id']}:reviewer-report.md"])
    add("negative-boundary-status-failed", lambda sample: set_report_status(sample, "boundary-audit.md", "boundary_pass_failed"), ["report_inventory_mismatch", f"unknown_status:{base['report_inventory'][0]['slice_id']}:boundary-audit.md", f"blocking_status:{base['report_inventory'][0]['slice_id']}:boundary-audit.md"])
    add("negative-next-step-status-blocked", lambda sample: set_report_status(sample, "next-step.md", "pass_product_grade_blocked"), ["report_inventory_mismatch", f"unknown_status:{base['report_inventory'][0]['slice_id']}:next-step.md", f"blocking_status:{base['report_inventory'][0]['slice_id']}:next-step.md"])
    add("ambiguous-marked-blocking", lambda sample: sample["ambiguous_status_inventory"][0].__setitem__("blocking", True), ["ambiguous_status_inventory_mismatch", f"ambiguous_status_marked_blocking:{base['ambiguous_status_inventory'][0]['slice_id']}:{base['ambiguous_status_inventory'][0]['report']}"])
    add("agent-rule-missing", lambda sample: sample["agent_rules"].pop(), ["agent_rules_mismatch", "agent_rule_missing:do not edit old slices"])
    add("readiness-mainline-true", lambda sample: sample["readiness_flags"].__setitem__("mainline_ready", True), ["readiness_flag_not_false:mainline_ready"])
    add("readiness-reacceptance-true", lambda sample: sample["readiness_flags"].__setitem__("re_acceptance_performed", True), ["readiness_flag_not_false:re_acceptance_performed"])
    add("operation-old-slice-modified", lambda sample: sample["operation_performed_flags"].__setitem__("legacy_slice_modified", True), ["operation_performed_not_false:legacy_slice_modified"])
    add("operation-commit", lambda sample: sample["operation_performed_flags"].__setitem__("commit", True), ["operation_performed_not_false:commit"])
    for non_claim in REQUIRED_NON_CLAIMS:
        add(f"missing-non-claim-{non_claim.replace(' ', '-')}", lambda sample, non_claim=non_claim: sample["required_non_claims"].remove(non_claim), ["required_non_claims_mismatch"])
    add("extra-non-claim", lambda sample: sample["required_non_claims"].append("unexpected authority"), ["required_non_claims_mismatch"])
    return cases


def build_fixtures() -> None:
    reset_generated()
    base = default_audit("status-normalization-audit")
    write_json(ROOT / "fixtures" / "valid-status-normalization-audit.json", base)
    guide = default_audit("agent-interpretation-guide")
    guide["operator_note"] = "Agent interpretation guide view. Still sandbox only."
    write_json(ROOT / "fixtures" / "valid-agent-interpretation-guide.json", guide)
    inventory = default_audit("ambiguous-status-inventory")
    inventory["operator_note"] = "Ambiguous status inventory view. Still sandbox only."
    write_json(ROOT / "fixtures" / "valid-ambiguous-status-inventory.json", inventory)
    cases = make_failure_cases(base)
    write_json(ROOT / "artifact" / "failure-case-oracle.json", {"slice_id": SLICE_ID, "cases": cases})
    lines = ["# Failure Case Oracle", "", f"Slice: `{SLICE_ID}`", "", f"Total cases: {len(cases)}", ""]
    for name, expected in cases.items():
        lines.append(f"- `{name}` -> `{', '.join(expected)}`")
    write_text(ROOT / "artifact" / "failure-case-oracle.md", "\n".join(lines))


def build_readout_and_contract() -> None:
    audit = default_audit()
    summary = audit["canonical_summary"]
    write_json(ROOT / "artifact" / "status-normalization-audit.json", audit)
    write_text(
        ROOT / "artifact" / "status-normalization-contract.md",
        f"""
# Status Normalization Compatibility Contract

Slice: `{SLICE_ID}`

This contract normalizes legacy sandbox report statuses for display and handoff only.
It is not re-acceptance, release approval, promotion approval, mainline readiness,
formal vault approval, reviewed knowledge, evidence support, or action basis.

## Compatibility Rules

- Product Acceptance remains the decisive gate.
- Legacy `draft`, `pending`, `in_progress`, and missing planning/source-map statuses are nonblocking when gate booleans pass.
- `next-step` pending means stop before auto-advance; it does not mean Product Acceptance failed.
- Unknown raw statuses are blocking until a later sandbox maps or explains them.
- Old slices must not be edited just to make status strings prettier.
""",
    )
    write_text(
        ROOT / "readouts" / "status-normalization-guide.md",
        f"""
# Status Normalization Guide

Status: sandbox display compatibility only.

Examined slices: `{summary['examined_slice_count']}`

Gate-pass slices: `{summary['gate_pass_count']}`

Legacy ambiguous/nonblocking statuses: `{summary['legacy_ambiguous_status_count']}`

Unknown statuses: `{summary['unknown_status_count']}`

Interpretation:

- The prior sandbox evidence remains Product Acceptance gated.
- Heterogeneous report strings are normalized so follow-up agents do not mistake old `pending`, `draft`, or missing planning statuses for failed Product Acceptance.
- This guide does not re-accept, release, promote, merge, sync, commit, push, or authorize action-basis use.
""",
    )


def build_prototype() -> None:
    audit = default_audit()
    summary = audit["canonical_summary"]
    prototype = ROOT / "prototype" / "status-normalization-audit"
    rows = "\n".join(
        f"<tr><td>{key}</td><td>{value}</td></tr>"
        for key, value in summary["canonical_status_counts"].items()
    )
    write_text(
        prototype / "index.html",
        f"""
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Status Normalization Audit</title>
  <style>
    body {{ margin: 0; font-family: Arial, sans-serif; background: #f8fafc; color: #1f2933; }}
    main {{ max-width: 980px; margin: 0 auto; padding: 28px 18px 44px; }}
    h1 {{ margin: 0 0 8px; font-size: 28px; }}
    .summary {{ color: #526273; max-width: 820px; }}
    table {{ width: 100%; border-collapse: collapse; margin-top: 18px; background: #fff; border: 1px solid #d9e1ec; }}
    th, td {{ text-align: left; padding: 10px 12px; border-bottom: 1px solid #e6edf5; }}
    .notice {{ margin-top: 16px; border-left: 4px solid #2f6fed; background: #edf4ff; padding: 12px 14px; }}
  </style>
</head>
<body>
  <main>
    <h1>Status Normalization Audit</h1>
    <p class="summary">sandbox display compatibility only. Examined {summary['examined_slice_count']} slices; gate-pass {summary['gate_pass_count']}; unknown statuses {summary['unknown_status_count']}; not re-acceptance; not enterprise production; not action basis.</p>
    <table>
      <thead><tr><th>Canonical status</th><th>Count</th></tr></thead>
      <tbody>{rows}</tbody>
    </table>
    <section class="notice">Legacy pending, draft, and missing planning statuses are interpreted beside Product Acceptance, Reviewer, Boundary, and verification gates. No old slice is edited.</section>
  </main>
  <script src="app.js"></script>
</body>
</html>
""",
    )
    write_text(prototype / "app.js", 'document.documentElement.dataset.statusNormalizationAuditReady = "true";')
    receipt = {
        "record_kind": "status_normalization_audit_prototype_receipt",
        "slice_id": SLICE_ID,
        "re_acceptance_performed": False,
        "release_approved": False,
        "promotion_approved": False,
        "enterprise_production_ready": False,
        "mainline_ready": False,
        "formal_vault_accessed": False,
        "sync_performed": False,
        "commit_performed": False,
        "push_performed": False,
        "old_slice_modified": False,
        "action_basis_created": False,
        "required_non_claims": REQUIRED_NON_CLAIMS,
    }
    write_json(prototype / "receipt.json", receipt)


def frontmatter(status: str) -> str:
    return f"---\nstatus: {status}\nslice_id: {SLICE_ID}\n---\n"


def build_reports() -> None:
    audit = default_audit()
    summary = audit["canonical_summary"]
    write_text(
        ROOT / "slice-plan.md",
        frontmatter("built_pending_review")
        + f"""
# Slice Plan

## Objective

Build a sandbox-only status normalization compatibility audit so follow-up agents can interpret heterogeneous legacy report statuses without editing old slices or confusing display status with Product Acceptance.

## Inputs

- `{rel(LEDGER_PATH)}`
- `{rel(HANDOFF_PACKET_PATH)}`

## Only Write Path

`{WRITE_SCOPE}`

## Non-Goals

- No re-acceptance of old slices.
- No edits to old slices.
- No mainline merge, formal vault operation, commit, push, promotion, reviewed knowledge, evidence support, or action basis.
""",
    )
    write_text(
        ROOT / "source-map.md",
        frontmatter("built_pending_review")
        + f"""
# Source Map

Source ledger:

- `{audit['source_snapshot']['ledger_path']}`
- sha256: `{audit['source_snapshot']['ledger_sha256']}`

Source handoff:

- `{audit['source_snapshot']['handoff_packet_path']}`
- sha256: `{audit['source_snapshot']['handoff_packet_sha256']}`

Examined slices: `{summary['examined_slice_count']}`

This map records display compatibility only. It is not authority, promotion, or mainline readiness.
""",
    )
    write_text(
        ROOT / "verification.md",
        frontmatter("local_verification_passed_pending_review")
        + f"""
# Verification

Default read-only verification command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_status_normalization_audit.py
```

Expected result:

- Positive fixtures pass.
- Failure cases match the oracle.
- Unknown statuses count is `0`.
- All examined slices remain gate-pass by Product/Reviewer/Boundary/verification booleans.
- Prototype and readout preserve sandbox-only boundaries.

Builder-only regeneration command:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_status_normalization_audit.py --rebuild
```

Final gate command after reviews:

```powershell
python -B .\\outputs\\review\\vaks-implementation-sandbox\\{SLICE_ID}\\artifact\\verify_status_normalization_audit.py --final-gate
```
""",
    )
    write_text(ROOT / "reviewer-report.md", frontmatter("reviewer_pending") + "# Reviewer Report\n\nPending independent read-only review.\n")
    write_text(ROOT / "boundary-audit.md", frontmatter("boundary_pending") + "# Boundary Audit\n\nPending independent boundary audit.\n")
    write_text(ROOT / "product-acceptance-report.md", frontmatter("product_acceptance_pending") + "# Product Acceptance Report\n\nPending GPT-5.5 extra-high Product Acceptance.\n")
    write_text(ROOT / "next-step.md", frontmatter("next_step_pending_product_acceptance") + "# Next Step\n\nDo not advance until Product Acceptance passes this slice.\n")


def build() -> None:
    build_fixtures()
    build_readout_and_contract()
    build_prototype()
    build_reports()


def validate_failure_cases() -> dict[str, Any]:
    oracle_path = ROOT / "artifact" / "failure-case-oracle.json"
    failure_dir = ROOT / "failure-cases"
    if not oracle_path.exists():
        return {"count": 0, "actual_file_count": 0, "orphan_count": 0, "mismatches": [{"file": "failure-case-oracle.json", "expected": ["oracle_present"], "actual": ["missing_oracle"]}]}
    oracle = read_json(oracle_path).get("cases", {})
    actual_files = {path.name for path in failure_dir.glob("*.json")} if failure_dir.exists() else set()
    mismatches = []
    for extra in sorted(actual_files - set(oracle)):
        mismatches.append({"file": extra, "expected": ["not_present_outside_oracle"], "actual": ["orphan_failure_case_file"]})
    for name, expected in oracle.items():
        path = failure_dir / name
        if not path.exists():
            mismatches.append({"file": name, "expected": expected, "actual": ["missing_failure_case"]})
            continue
        actual = validate_audit(read_json(path))
        if sorted(actual) != sorted(expected):
            mismatches.append({"file": name, "expected": expected, "actual": actual})
    return {"count": len(oracle), "actual_file_count": len(actual_files), "orphan_count": len(actual_files - set(oracle)), "mismatches": mismatches}


def validate_fixtures() -> dict[str, Any]:
    fixture_dir = ROOT / "fixtures"
    actual_files = {path.name for path in fixture_dir.glob("*.json")} if fixture_dir.exists() else set()
    errors = []
    details = []
    for missing in sorted(set(REQUIRED_FIXTURES) - actual_files):
        errors.append({"file": missing, "errors": ["missing_required_fixture"]})
    for extra in sorted(actual_files - set(REQUIRED_FIXTURES)):
        errors.append({"file": extra, "errors": ["unexpected_fixture_file"]})
    for path in sorted(fixture_dir.glob("*.json")):
        data = read_json(path)
        fixture_errors = validate_audit(data)
        expected_view = REQUIRED_FIXTURES.get(path.name)
        if expected_view and data.get("view") != expected_view:
            fixture_errors.append(f"fixture_view_mismatch:{expected_view}")
        if path.name == "valid-status-normalization-audit.json" and "operator_note" in data:
            fixture_errors.append("fixture_operator_note_unexpected")
        if path.name != "valid-status-normalization-audit.json" and path.name in REQUIRED_FIXTURES and "operator_note" not in data:
            fixture_errors.append("fixture_operator_note_missing")
        details.append({"file": path.name, "errors": fixture_errors})
        if fixture_errors:
            errors.append({"file": path.name, "errors": fixture_errors})
    return {"count": len(details), "fixtures": details, "errors": errors}


def validate_readout() -> dict[str, Any]:
    path = ROOT / "readouts" / "status-normalization-guide.md"
    issues: list[str] = []
    if not path.exists():
        return {"path": str(path), "issues": ["missing_readout"]}
    text = path.read_text(encoding="utf-8", errors="ignore")
    for phrase in ["sandbox display compatibility only", "Examined slices", "Unknown statuses", "does not re-accept", "authorize action-basis"]:
        if phrase not in text:
            issues.append(f"readout_phrase_missing:{phrase}")
    return {"path": str(path), "issues": issues}


def validate_prototype() -> dict[str, Any]:
    prototype = ROOT / "prototype" / "status-normalization-audit"
    issues: list[str] = []
    for item in ["index.html", "app.js", "receipt.json"]:
        if not (prototype / item).exists():
            issues.append(f"missing_prototype_file:{item}")
    if (prototype / "index.html").exists():
        html = (prototype / "index.html").read_text(encoding="utf-8", errors="ignore").lower()
        for forbidden in ["<form", "download", "contenteditable", "<a ", "h:\\obsidian", "onclick"]:
            if forbidden in html:
                issues.append(f"prototype_forbidden:{forbidden}")
        for phrase in ["sandbox display compatibility only", "not re-acceptance", "not enterprise production", "not action basis", "no old slice is edited"]:
            if phrase not in html:
                issues.append(f"prototype_phrase_missing:{phrase}")
    if (prototype / "app.js").exists():
        js = (prototype / "app.js").read_text(encoding="utf-8", errors="ignore").strip()
        if js != 'document.documentElement.dataset.statusNormalizationAuditReady = "true";':
            issues.append("prototype_app_js_not_static_receipt_marker")
    if (prototype / "receipt.json").exists():
        receipt = read_json(prototype / "receipt.json")
        for flag in [
            "re_acceptance_performed",
            "release_approved",
            "promotion_approved",
            "enterprise_production_ready",
            "mainline_ready",
            "formal_vault_accessed",
            "sync_performed",
            "commit_performed",
            "push_performed",
            "old_slice_modified",
            "action_basis_created",
        ]:
            if receipt.get(flag) is not False:
                issues.append(f"prototype_receipt_flag_not_false:{flag}")
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
    primary = ROOT / "fixtures" / "valid-status-normalization-audit.json"
    config_errors = validate_audit(read_json(primary)) if primary.exists() else ["missing_valid_fixture"]
    artifact_path = ROOT / "artifact" / "status-normalization-audit.json"
    artifact_errors = validate_audit(read_json(artifact_path)) if artifact_path.exists() else ["missing_status_normalization_audit"]
    fixtures = validate_fixtures()
    failure_cases = validate_failure_cases()
    prototype = validate_prototype()
    readout = validate_readout()
    reports = validate_required_reports(final_gate=final_gate)
    failures: list[str] = []
    failures.extend(config_errors)
    failures.extend([f"artifact_error:{item}" for item in artifact_errors])
    failures.extend([f"fixture_error:{item['file']}" for item in fixtures["errors"]])
    failures.extend([f"failure_case_mismatch:{item['file']}" for item in failure_cases["mismatches"]])
    failures.extend(prototype["issues"])
    failures.extend(readout["issues"])
    failures.extend(reports["issues"])
    current = default_audit()
    return {
        "slice_id": SLICE_ID,
        "passed": not failures,
        "failures": failures,
        "valid_config_errors": config_errors,
        "artifact_errors": artifact_errors,
        "positive_fixtures": fixtures,
        "failure_cases": failure_cases,
        "prototype": prototype,
        "readout": readout,
        "required_reports": reports,
        "source_snapshot": current["source_snapshot"],
        "canonical_summary": current["canonical_summary"],
        "non_claims": REQUIRED_NON_CLAIMS,
    }


if __name__ == "__main__":
    build()
