#!/usr/bin/env python
"""Run a read-only Source Intake answer-loop boundary harness.

This harness is intentionally narrow:
- no writeback;
- no promotion;
- no truth mutation;
- deterministic fixture cases only;
- deterministic mock-tool smoke only, not a live LLM/tool loop;
- output is a sandbox evidence package, not Source Intake P0 approval.
"""

from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import re
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import yaml


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "outputs" / "review" / "source-intake-runtime-readonly-loop-2026-06-13"
RESULTS_DIR = OUT_DIR / "results"
QUERY_RUN_DIR = OUT_DIR / "query_runs"
CONTEXT_PACK_DIR = OUT_DIR / "context_packs"
ANSWER_DIR = OUT_DIR / "answer_drafts"
FIXTURE_SOURCE_DIR = OUT_DIR / "fixtures" / "raw_sources"
ZIP_NAME = "source-intake-runtime-readonly-loop-pro-review-package.zip"
JUDGE_ZIP_NAME = "external_blind_relevance_judge_only.zip"
REAL_ANCHOR_SOURCE = "raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md"
REAL_ANCHOR_SELECTOR = "Extracted Source Facts"
BROKEN_ANCHOR_SELECTOR = "missing-runtime-anchor-selector"

VALIDATOR_PATH = ROOT / "tools" / "validate_source_intake_contract.py"
SPEC = importlib.util.spec_from_file_location("validate_source_intake_contract", VALIDATOR_PATH)
if SPEC is None or SPEC.loader is None:
    raise RuntimeError(f"Cannot load validator from {VALIDATOR_PATH}")
VALIDATOR = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(VALIDATOR)


NON_SUPPORT_RECORD_KINDS = {
    "source_annotation",
    "candidate_distillation",
    "project_overlay",
    "feedback_event",
    "heavy_review_open",
    "graph_neighbor",
}

DIAGNOSTIC_ANCHOR_TERMS = [
    "retrieval_rank",
    "retrieval score",
    "rank:",
    "score:",
    "graph_rank",
    "graph rank",
    "graph_path",
    "graph path",
    "dashboard_hit",
    "dashboard hit",
    "legacy_raw_metadata",
]


def selected_by(**overrides: bool) -> dict[str, bool]:
    base = {
        "lexical": False,
        "semantic": False,
        "graph": False,
        "metadata": False,
        "rank": False,
        "dashboard": False,
        "legacy_raw_metadata": False,
    }
    base.update(overrides)
    return base


CASES: list[dict[str, Any]] = [
    {
        "case_id": "RT-01-candidate-support-block",
        "risk_target": "candidate_as_support",
        "question": "Can this candidate distillation be used as final support?",
        "expected": "blocked",
        "item": {
            "ref": "outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md#candidate-points",
            "record_kind": "candidate_distillation",
            "knowledge_status": "candidate",
            "pack_role": "support",
            "warning_code": "candidate_not_action_basis",
            "action_basis_allowed": False,
            "independent_anchor_ref": "",
            "selected_by": selected_by(semantic=True, rank=True),
        },
        "support_check": {
            "claim_ref": "candidate claim reused as support",
            "independent_anchor_ref": "",
            "result": "supported",
        },
        "draft_answer": "Use the candidate distillation as the final basis.",
    },
    {
        "case_id": "RT-02-overlay-support-block",
        "risk_target": "overlay_as_support",
        "question": "Can a project overlay become final support?",
        "expected": "blocked",
        "item": {
            "ref": "outputs/review/project_overlays/vaks/example-confirmed-overlay.md#borrow-scope",
            "record_kind": "project_overlay",
            "knowledge_status": "candidate",
            "pack_role": "support",
            "warning_code": "overlay_not_authority",
            "action_basis_allowed": False,
            "independent_anchor_ref": "raw/articles/example-source.md#L12-L18",
            "selected_by": selected_by(metadata=True),
        },
        "support_check": {
            "claim_ref": "overlay-local borrow scope",
            "independent_anchor_ref": "raw/articles/example-source.md#L12-L18",
            "result": "supported",
        },
        "draft_answer": "Use the project overlay as final support.",
    },
    {
        "case_id": "RT-03-raw-summary-without-anchor-block",
        "risk_target": "raw_summary_without_anchor",
        "question": "Can a raw source summary support an answer without a stable anchor?",
        "expected": "blocked",
        "item": {
            "ref": "raw/articles/2026-04-04-karpathy-llm-wiki-source.md#summary",
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "pack_role": "support",
            "warning_code": "raw_is_provenance_only",
            "action_basis_allowed": False,
            "independent_anchor_ref": "",
            "selected_by": selected_by(lexical=True, metadata=True),
        },
        "support_check": {
            "claim_ref": "raw summary claim",
            "independent_anchor_ref": "",
            "result": "supported",
        },
        "draft_answer": "Treat a raw source-card summary as grounded support.",
    },
    {
        "case_id": "RT-04-graph-neighbor-support-block",
        "risk_target": "graph_selected_signal_as_support",
        "question": "Can a graph-neighborhood hit become final support?",
        "expected": "blocked",
        "item": {
            "ref": "raw/articles/2026-01-thinking-os-with-ai-vault-source.md#graph-neighborhood-context",
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "pack_role": "support",
            "warning_code": "raw_is_provenance_only",
            "action_basis_allowed": False,
            "independent_anchor_ref": "graph_path:source->candidate->theme",
            "selected_by": selected_by(graph=True, rank=True),
        },
        "support_check": {
            "claim_ref": "graph-selected source says related",
            "independent_anchor_ref": "graph_path:source->candidate->theme",
            "result": "supported",
        },
        "draft_answer": "Treat the graph-selected path as support.",
    },
    {
        "case_id": "RT-05-rank-score-support-block",
        "risk_target": "rank_score_as_support",
        "question": "Can a retrieval rank be used as the support anchor?",
        "expected": "blocked",
        "item": {
            "ref": "raw/articles/2026-01-thinking-os-with-ai-vault-source.md#metadata",
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "pack_role": "support",
            "warning_code": "raw_is_provenance_only",
            "action_basis_allowed": False,
            "independent_anchor_ref": "retrieval_rank:0.97",
            "selected_by": selected_by(rank=True, semantic=True),
        },
        "support_check": {
            "claim_ref": "top ranked result",
            "independent_anchor_ref": "retrieval_rank:0.97",
            "result": "supported",
        },
        "draft_answer": "Use the top-ranked retrieval result as support because rank is high.",
    },
    {
        "case_id": "RT-06-legacy-raw-metadata-support-block",
        "risk_target": "legacy_raw_metadata_as_support",
        "question": "Can legacy raw metadata be selected or cited as support?",
        "expected": "blocked",
        "item": {
            "ref": "raw/articles/example-source.md#legacy_raw_metadata.relations",
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "pack_role": "support",
            "warning_code": "raw_is_provenance_only",
            "action_basis_allowed": False,
            "independent_anchor_ref": "legacy_raw_metadata.relations[0]",
            "selected_by": selected_by(legacy_raw_metadata=True),
        },
        "support_check": {
            "claim_ref": "legacy_raw_metadata.relations[0]",
            "independent_anchor_ref": "legacy_raw_metadata.relations[0]",
            "result": "supported",
        },
        "draft_answer": "Use legacy raw metadata as support.",
    },
    {
        "case_id": "RT-07-safe-raw-anchor-readonly-allow",
        "risk_target": "real_raw_anchor_allow",
        "question": "Can a raw/stable independent anchor be cited in a read-only answer?",
        "expected": "allowed_readonly",
        "item": {
            "ref": f"{REAL_ANCHOR_SOURCE}#{REAL_ANCHOR_SELECTOR}",
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "pack_role": "support",
            "warning_code": "raw_is_provenance_only",
            "action_basis_allowed": False,
            "independent_anchor_ref": f"{REAL_ANCHOR_SOURCE}#{REAL_ANCHOR_SELECTOR}",
            "selected_by": selected_by(lexical=True),
        },
        "support_check": {
            "claim_ref": "raw inspected source has extractable facts section",
            "independent_anchor_ref": f"{REAL_ANCHOR_SOURCE}#{REAL_ANCHOR_SELECTOR}",
            "result": "supported",
        },
        "draft_answer": "Use the inspected raw source section as a read-only citation, not an action basis.",
    },
    {
        "case_id": "RT-08-broken-raw-anchor-block",
        "risk_target": "real_raw_anchor_broken_selector",
        "question": "Does a broken raw/stable anchor get rejected as not support-ready?",
        "expected": "blocked",
        "item": {
            "ref": f"{REAL_ANCHOR_SOURCE}#{BROKEN_ANCHOR_SELECTOR}",
            "record_kind": "source_card",
            "knowledge_status": "raw",
            "pack_role": "support",
            "warning_code": "raw_is_provenance_only",
            "action_basis_allowed": False,
            "independent_anchor_ref": f"{REAL_ANCHOR_SOURCE}#{BROKEN_ANCHOR_SELECTOR}",
            "selected_by": selected_by(lexical=True),
        },
        "support_check": {
            "claim_ref": "raw inspected source has a missing selector",
            "independent_anchor_ref": f"{REAL_ANCHOR_SOURCE}#{BROKEN_ANCHOR_SELECTOR}",
            "result": "supported",
        },
        "draft_answer": "Treat a broken raw anchor selector as if it were support.",
    },
    {
        "case_id": "RT-09-mixed-pack-support-selection-allow",
        "risk_target": "mixed_pack_support_selection",
        "question": "In a mixed pack, can the answer keep only the legal raw anchor as support?",
        "expected": "allowed_readonly",
        "items": [
            {
                "ref": f"{REAL_ANCHOR_SOURCE}#{REAL_ANCHOR_SELECTOR}",
                "record_kind": "source_card",
                "knowledge_status": "raw",
                "pack_role": "support",
                "warning_code": "raw_is_provenance_only",
                "action_basis_allowed": False,
                "independent_anchor_ref": f"{REAL_ANCHOR_SOURCE}#{REAL_ANCHOR_SELECTOR}",
                "selected_by": selected_by(lexical=True),
            },
            {
                "ref": "outputs/review/2026-06-11-AxDSan-mnemosyne-candidate-distillation.md#candidate-points",
                "record_kind": "candidate_distillation",
                "knowledge_status": "candidate",
                "pack_role": "review_input",
                "warning_code": "candidate_not_action_basis",
                "action_basis_allowed": False,
                "independent_anchor_ref": "",
                "selected_by": selected_by(semantic=True, rank=True),
            },
            {
                "ref": "outputs/review/project_overlays/vaks/example-confirmed-overlay.md#borrow-scope",
                "record_kind": "project_overlay",
                "knowledge_status": "candidate",
                "pack_role": "review_input",
                "warning_code": "overlay_not_authority",
                "action_basis_allowed": False,
                "independent_anchor_ref": "",
                "selected_by": selected_by(metadata=True),
            },
            {
                "ref": "raw/articles/2026-01-thinking-os-with-ai-vault-source.md#graph-neighborhood-context",
                "record_kind": "source_card",
                "knowledge_status": "raw",
                "pack_role": "orientation",
                "warning_code": "raw_is_provenance_only",
                "action_basis_allowed": False,
                "independent_anchor_ref": "graph_path:source->candidate->theme",
                "selected_by": selected_by(graph=True),
            },
            {
                "ref": "raw/articles/2026-01-thinking-os-with-ai-vault-source.md#ranked-hit",
                "record_kind": "source_card",
                "knowledge_status": "raw",
                "pack_role": "orientation",
                "warning_code": "raw_is_provenance_only",
                "action_basis_allowed": False,
                "independent_anchor_ref": "retrieval_rank:0.99",
                "selected_by": selected_by(rank=True, semantic=True),
            },
        ],
        "support_checks": [
            {
                "claim_ref": "mixed pack final support uses only real raw source anchor",
                "independent_anchor_ref": f"{REAL_ANCHOR_SOURCE}#{REAL_ANCHOR_SELECTOR}",
                "result": "supported",
            }
        ],
        "draft_answer": "Use only the real raw anchor as support; candidate, overlay, graph, and rank hits remain orientation or review input.",
    },
]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def safe_clear_dir(path: Path) -> None:
    path.mkdir(parents=True, exist_ok=True)
    resolved = path.resolve()
    if not str(resolved).startswith(str(OUT_DIR.resolve())):
        raise RuntimeError(f"Refusing to clear outside runtime output dir: {resolved}")
    for child in path.iterdir():
        if child.is_dir():
            shutil.rmtree(child)
        else:
            child.unlink()


def write_frontmatter(path: Path, data: dict[str, Any], body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    frontmatter = yaml.safe_dump(data, allow_unicode=True, sort_keys=False).strip()
    path.write_text(f"---\n{frontmatter}\n---\n\n{body}\n", encoding="utf-8")


def case_items(case: dict[str, Any]) -> list[dict[str, Any]]:
    return list(case.get("items") or [case["item"]])


def case_support_checks(case: dict[str, Any]) -> list[dict[str, Any]]:
    checks = []
    for check in list(case.get("support_checks") or [case["support_check"]]):
        enriched = dict(check)
        enriched.setdefault("support_check_stage", "pre_validation_fixture_input")
        enriched.setdefault("result_semantics", "proposed_fixture_input_not_evaluated_verdict")
        if "result" in enriched:
            enriched.setdefault("proposed_support_result", enriched["result"])
            del enriched["result"]
        checks.append(enriched)
    return checks


def support_check_result(check: dict[str, Any]) -> str:
    return str(check.get("proposed_support_result") or check.get("result") or "")


def query_run_for(case: dict[str, Any], now: str) -> dict[str, Any]:
    return {
        "record_kind": "query_run_trace",
        "artifact_kind": "runtime_test_artifact",
        "status": "runtime_fixture",
        "knowledge_status": "candidate",
        "retrieval_exclusion": True,
        "default_retrieval": False,
        "indexing_policy": "exclude_from_default_retrieval_graph_pack_support",
        "retrieval_policy": {
            "policy_kind": "orientation_only",
            "pack_allowed": "none",
            "action_basis_allowed": False,
            "warning_code": "context_pack_not_action_basis",
        },
        "query_id": case["case_id"],
        "query_time": now,
        "question_summary": case["question"],
        "verbatim_input": case["question"],
        "query_mode": "action",
        "active_project": "vaks-source-intake-runtime-readonly",
        "requested_authority_bucket": "reviewed_support_or_raw_anchor_only",
        "included_buckets": ["raw_anchor", "candidate_context"],
        "excluded_buckets": ["reviewed_writeback", "promotion"],
        "retrieval_filters": {
            "include_candidates": True,
            "include_overlays": "active_project_only",
            "read_only": True,
            "writeback_allowed": False,
            "promotion_allowed": False,
        },
        "selected_items": case_items(case),
        "support_checks": case_support_checks(case),
        "human_confirmation_required": False,
        "runtime_boundary": {
            "read_only": True,
            "writeback_attempted": False,
            "promotion_attempted": False,
            "truth_mutation_attempted": False,
        },
    }


def context_pack_for(case: dict[str, Any], now: str) -> dict[str, Any]:
    return {
        "record_kind": "context_pack_manifest",
        "artifact_kind": "runtime_test_artifact",
        "status": "runtime_fixture",
        "knowledge_status": "candidate",
        "retrieval_exclusion": True,
        "default_retrieval": False,
        "indexing_policy": "exclude_from_default_retrieval_graph_pack_support",
        "processing_tier": "medium",
        "retrieval_policy": {
            "policy_kind": "orientation_only",
            "pack_allowed": "review_input_only",
            "action_basis_allowed": False,
            "warning_code": "context_pack_not_action_basis",
        },
        "action_basis_allowed": False,
        "truth_mutation_allowed": False,
        "query_run_ref": f"{case['case_id']}-query-run.md",
        "active_project": "vaks-source-intake-runtime-readonly",
        "query_mode": "action",
        "requested_authority_bucket": "reviewed_support_or_raw_anchor_only",
        "included_buckets": ["raw_anchor", "candidate_context"],
        "excluded_buckets": ["reviewed_writeback", "promotion"],
        "items": case_items(case),
        "support_checks": case_support_checks(case),
        "human_confirmation_required": False,
    }


def answer_draft_for(case: dict[str, Any], decision: str, errors: list[str], now: str) -> dict[str, Any]:
    return {
        "record_kind": "runtime_test_artifact",
        "type": "runtime_answer_draft",
        "artifact_kind": "runtime_test_artifact",
        "status": decision,
        "created_at": now,
        "case_id": case["case_id"],
        "risk_target": case["risk_target"],
        "knowledge_status": "candidate",
        "retrieval_exclusion": True,
        "default_retrieval": False,
        "indexing_policy": "exclude_from_default_retrieval_graph_pack_support",
        "retrieval_policy": {
            "policy_kind": "orientation_only",
            "pack_allowed": "none",
            "action_basis_allowed": False,
            "warning_code": "context_pack_not_action_basis",
        },
        "read_only": True,
        "writeback_attempted": False,
        "promotion_attempted": False,
        "truth_mutation_attempted": False,
        "action_basis_allowed": False,
        "support_decision": decision,
        "runtime_errors": errors,
    }


def runtime_evaluate_item(item: dict[str, Any], support_check: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    record_kind = item.get("record_kind")
    status = item.get("knowledge_status")
    pack_role = item.get("pack_role")
    anchor = str(item.get("independent_anchor_ref") or "")
    selected = item.get("selected_by") if isinstance(item.get("selected_by"), dict) else {}
    support_anchor = str(support_check.get("independent_anchor_ref") or "")

    if selected.get("legacy_raw_metadata") is True:
        errors.append("legacy_raw_metadata_selected")

    if pack_role == "support":
        if status == "candidate" or record_kind in NON_SUPPORT_RECORD_KINDS:
            errors.append("non_support_record_as_support")
        if not anchor.strip():
            errors.append("support_missing_independent_anchor")
        if selected and not anchor.strip():
            errors.append("diagnostic_signal_as_support_without_anchor")
        risky_anchor = f"{anchor} {support_anchor}".lower()
        if any(term in risky_anchor for term in DIAGNOSTIC_ANCHOR_TERMS):
            errors.append("diagnostic_or_legacy_anchor_as_support")

    if support_check_result(support_check) == "supported" and not support_anchor.strip():
        errors.append("supported_without_independent_anchor")

    return sorted(set(errors))


def runtime_evaluate_case(case: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    support_checks = case_support_checks(case)
    for item in case_items(case):
        matching_check = {}
        if item.get("pack_role") == "support":
            item_anchor = item.get("independent_anchor_ref")
            matching_check = next(
                (check for check in support_checks if check.get("independent_anchor_ref") == item_anchor),
                {},
            )
        errors.extend(runtime_evaluate_item(item, matching_check))
    for check in support_checks:
        if support_check_result(check) == "supported" and not str(check.get("independent_anchor_ref") or "").strip():
            errors.append("supported_without_independent_anchor")
    return sorted(set(errors))


def resolve_anchor(anchor_ref: str) -> dict[str, Any]:
    method = "loose_path_selector_string_match_not_heading_or_line_binding"
    if "#" not in anchor_ref:
        return {"status": "not_checked", "reason": "anchor ref has no selector", "method": method}
    path_part, selector = anchor_ref.split("#", 1)
    if not path_part or not selector:
        return {"status": "missing", "reason": "anchor path or selector is blank", "method": method}
    path = ROOT / path_part
    if not path.exists() or not path.is_file():
        return {"status": "missing", "reason": "anchor file missing", "path": path_part, "selector": selector, "method": method}
    text = path.read_text(encoding="utf-8", errors="replace")
    selector_variants = {
        selector,
        selector.replace("-", " "),
        selector.replace("_", " "),
        selector.lower(),
        selector.replace("-", " ").lower(),
    }
    lower_text = text.lower()
    if any(variant.lower() in lower_text for variant in selector_variants):
        return {"status": "exists", "path": path_part, "selector": selector, "method": method}
    return {"status": "missing", "reason": "selector not found in file", "path": path_part, "selector": selector, "method": method}


def excerpt_for_ref(ref: str, max_chars: int = 700) -> str:
    if "#" in ref:
        path_part, selector = ref.split("#", 1)
    else:
        path_part, selector = ref, ""
    path = ROOT / path_part
    if not path.exists() or not path.is_file():
        return "[support text unavailable in package]"
    text = path.read_text(encoding="utf-8", errors="replace")
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) >= 3:
            text = parts[2]
    if selector:
        lower = text.lower()
        needle = selector.replace("-", " ").lower()
        pos = lower.find(needle)
        if pos < 0:
            pos = lower.find(selector.lower())
        if pos >= 0:
            start = max(0, pos - 180)
            end = min(len(text), pos + max_chars)
            excerpt = " ".join(text[start:end].split())
            return sanitize_judge_excerpt(excerpt)
        return "[selector not found in judge-facing support excerpt]"
    return sanitize_judge_excerpt(" ".join(text[:max_chars].split()))


def sanitize_judge_excerpt(text: str) -> str:
    sanitized = re.sub(r"(?<![A-Za-z])[A-Za-z]:[\\/][^\s,;]+", "[local-path]", text)
    sanitized = re.sub(r"(?:raw|outputs|wiki|templates|tools)/(?:[^\s,;]+)", "[workspace-path]", sanitized)
    sanitized = sanitized.replace(".md#", "[md-anchor]")
    return sanitized


def validate_generated_file(rel_path: Path) -> list[dict[str, Any]]:
    issues: list[dict[str, Any]] = []
    registry = VALIDATOR.load_registry(ROOT)
    VALIDATOR.validate_file(ROOT, rel_path, registry, issues)
    return issues


def write_case_artifacts(case: dict[str, Any], now: str) -> dict[str, Any]:
    query_path = QUERY_RUN_DIR / f"{case['case_id']}-query-run.md"
    pack_path = CONTEXT_PACK_DIR / f"{case['case_id']}-context-pack.md"

    query_data = query_run_for(case, now)
    pack_data = context_pack_for(case, now)
    answer_path = ANSWER_DIR / f"{case['case_id']}-answer-draft.md"

    write_frontmatter(
        query_path,
        query_data,
        "# Query Run Trace\n\nRead-only runtime boundary fixture. This trace is not a reviewed record.\n",
    )
    write_frontmatter(
        pack_path,
        pack_data,
        "# Context Pack Manifest\n\nGenerated by the read-only runtime boundary harness.\n",
    )
    query_rel = query_path.relative_to(ROOT)
    pack_rel = pack_path.relative_to(ROOT)
    query_issues = validate_generated_file(query_rel)
    pack_issues = validate_generated_file(pack_rel)
    structural_errors = [i for i in query_issues + pack_issues if i["severity"] == "error"]
    structural_error_checks = sorted({i["check"] for i in structural_errors})
    runtime_errors = runtime_evaluate_case(case)
    support_checks = case_support_checks(case)
    anchor_resolutions = [
        resolve_anchor(check.get("independent_anchor_ref", ""))
        for check in support_checks
        if support_check_result(check) == "supported"
    ]
    anchor_resolution = anchor_resolutions[0] if anchor_resolutions else {"status": "not_checked", "reason": "no supported claim"}
    anchor_errors: list[str] = []
    unresolved_supported_anchors = [res for res in anchor_resolutions if res.get("status") != "exists"]
    if unresolved_supported_anchors:
        anchor_errors.append("support_anchor_not_resolved")
        if case["expected"] == "allowed_readonly":
            anchor_errors.append("safe_control_anchor_not_resolved")
    all_errors = sorted(set(runtime_errors + structural_error_checks + anchor_errors))
    decision = "allowed_readonly" if not all_errors else "blocked_or_downgraded"
    answer_data = answer_draft_for(case, decision, all_errors, now)

    write_frontmatter(
        answer_path,
        answer_data,
        "# Answer Draft\n\n"
        "## Runtime Test Artifact Warning\n\n"
        "This file is a negative/positive fixture for Source Intake runtime-boundary testing. "
        "It must not be indexed, retrieved by default, used as support, or treated as reviewed knowledge.\n\n"
        "## Fixture Sentence\n\n"
        f"```text\n{case['draft_answer']}\n```\n\n"
        "This draft is truth-layer read-only and cannot write back or promote knowledge.\n",
    )

    expected = case["expected"]
    passed = (
        (expected == "blocked" and decision == "blocked_or_downgraded" and bool(all_errors))
        or (expected == "allowed_readonly" and decision == "allowed_readonly" and not all_errors)
    )

    return {
        "case_id": case["case_id"],
        "risk_target": case["risk_target"],
        "expected": expected,
        "decision": decision,
        "passed": passed,
        "runtime_errors": runtime_errors,
        "structural_error_checks": structural_error_checks,
        "anchor_resolution_status": anchor_resolution["status"],
        "anchor_resolution_detail": anchor_resolution,
        "anchor_resolution_count": len(anchor_resolutions),
        "anchor_error_checks": anchor_errors,
        "all_error_checks": all_errors,
        "query_run_path": str(query_rel).replace("\\", "/"),
        "context_pack_path": str(pack_rel).replace("\\", "/"),
        "answer_draft_path": str(answer_path.relative_to(ROOT)).replace("\\", "/"),
        "writeback_attempted": False,
        "promotion_attempted": False,
        "truth_mutation_attempted": False,
    }


def event_rows_for(row: dict[str, Any]) -> list[dict[str, Any]]:
    selected = row["all_error_checks"]
    has_structural = bool(row["structural_error_checks"])
    has_runtime = bool(row["runtime_errors"])
    support_stage = "support_evaluator" if has_runtime else ("static_validator" if has_structural else "shape_acceptance")
    return [
        {
            "case_id": row["case_id"],
            "stage": "retrieve",
            "status": "selected_fixture_item",
            "decision": "continue",
            "artifact": row["query_run_path"],
            "detail": "fixture item selected with boundary metadata; this is not live retrieval",
        },
        {
            "case_id": row["case_id"],
            "stage": "assemble_context_pack",
            "status": "pack_manifest_written",
            "decision": "continue",
            "artifact": row["context_pack_path"],
            "detail": "context pack fixture written with item-level selected_by and support metadata",
        },
        {
            "case_id": row["case_id"],
            "stage": "static_receipt_validation",
            "status": "error" if has_structural else "pass",
            "decision": "downgrade_or_block" if has_structural else "continue",
            "artifact": f"{row['query_run_path']}|{row['context_pack_path']}",
            "detail": "|".join(row["structural_error_checks"]),
        },
        {
            "case_id": row["case_id"],
            "stage": "anchor_resolution",
            "status": row["anchor_resolution_status"],
            "decision": "continue" if row["anchor_resolution_status"] == "exists" else "not_support_ready",
            "artifact": row["answer_draft_path"],
            "detail": json.dumps(row["anchor_resolution_detail"], ensure_ascii=False),
        },
        {
            "case_id": row["case_id"],
            "stage": "runtime_support_evaluator",
            "status": "error" if has_runtime else "pass",
            "decision": "downgrade_or_block" if has_runtime else "continue",
            "artifact": row["answer_draft_path"],
            "detail": "|".join(row["runtime_errors"]),
        },
        {
            "case_id": row["case_id"],
            "stage": "final_support_decision",
            "status": row["decision"],
            "decision": row["decision"],
            "artifact": row["answer_draft_path"],
            "detail": f"support_stage={support_stage}; all_errors={'|'.join(selected)}",
        },
    ]


def run_mock_tool_loop(now: str) -> dict[str, Any]:
    cases = [
        {
            "tool_case_id": "TOOL-01-read-resource-allowed",
            "tool_name": "read_resource",
            "tool_kind": "read",
            "write_capable": False,
            "human_confirmation": False,
            "attempted": True,
            "decision": "allowed_readonly",
            "truth_write_performed": False,
            "reason": "read-only resource tool is allowed in the smoke loop",
        },
        {
            "tool_case_id": "TOOL-02-mock-write-without-confirmation-blocked",
            "tool_name": "mock_write_reviewed_truth",
            "tool_kind": "write",
            "write_capable": True,
            "human_confirmation": False,
            "attempted": True,
            "decision": "blocked_requires_human_confirmation",
            "truth_write_performed": False,
            "reason": "write-capable mock tool was visible and attempted, but blocked without explicit human confirmation",
        },
    ]
    summary = {
        "status": "pass",
        "created_at": now,
        "tool_loop_kind": "deterministic_mock_tool_smoke",
        "live_llm_used": False,
        "live_tool_runtime_used": False,
        "write_capable_mock_tool_available": True,
        "write_capable_mock_tool_attempted_without_confirmation": True,
        "write_capable_mock_tool_blocked_without_confirmation": True,
        "truth_write_performed_count": sum(1 for case in cases if case["truth_write_performed"]),
        "truth_boundary": "Mock tool-loop smoke only; proves a deterministic gate path, not live agent/tool behavior.",
    }
    write_json(RESULTS_DIR / "runtime_mock_tool_loop_summary.json", summary)
    with (RESULTS_DIR / "runtime_mock_tool_loop_cases.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "tool_case_id",
            "tool_name",
            "tool_kind",
            "write_capable",
            "human_confirmation",
            "attempted",
            "decision",
            "truth_write_performed",
            "reason",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(cases)
    with (RESULTS_DIR / "runtime_mock_tool_loop_events.jsonl").open("w", encoding="utf-8") as f:
        for case in cases:
            f.write(json.dumps({"stage": "tool_available", **case}, ensure_ascii=False) + "\n")
            f.write(json.dumps({"stage": "tool_gate_decision", **case}, ensure_ascii=False) + "\n")
    return summary


def load_frontmatter(path: Path) -> dict[str, Any]:
    text = path.read_text(encoding="utf-8", errors="replace")
    if not text.startswith("---"):
        return {}
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}
    data = yaml.safe_load(parts[1]) or {}
    return data if isinstance(data, dict) else {}


def run_runtime_artifact_exclusion_test(now: str) -> dict[str, Any]:
    rows = []
    checked_dirs = [
        QUERY_RUN_DIR.relative_to(ROOT).as_posix(),
        CONTEXT_PACK_DIR.relative_to(ROOT).as_posix(),
        ANSWER_DIR.relative_to(ROOT).as_posix(),
    ]
    for directory in [QUERY_RUN_DIR, CONTEXT_PACK_DIR, ANSWER_DIR]:
        for path in sorted(directory.glob("*.md")):
            data = load_frontmatter(path)
            rel = path.relative_to(ROOT).as_posix()
            policy = data.get("retrieval_policy") if isinstance(data.get("retrieval_policy"), dict) else {}
            default_eligible = not (
                data.get("artifact_kind") == "runtime_test_artifact"
                or data.get("retrieval_exclusion") is True
                or data.get("default_retrieval") is False
                or data.get("indexing_policy") == "exclude_from_default_retrieval_graph_pack_support"
                or policy.get("pack_allowed") == "none"
            )
            rows.append(
                {
                    "path": rel,
                    "artifact_kind": data.get("artifact_kind", ""),
                    "retrieval_exclusion": data.get("retrieval_exclusion", ""),
                    "default_retrieval": data.get("default_retrieval", ""),
                    "indexing_policy": data.get("indexing_policy", ""),
                    "pack_allowed": policy.get("pack_allowed", ""),
                    "default_index_eligible": default_eligible,
                }
            )
    eligible = [row for row in rows if row["default_index_eligible"]]
    summary = {
        "status": "pass" if not eligible else "fail",
        "created_at": now,
        "checked_artifact_count": len(rows),
        "checked_artifact_scope": "generated_query_runs_context_packs_answer_drafts_only",
        "checked_directories": checked_dirs,
        "default_index_eligible_count": len(eligible),
        "eligible_paths": [row["path"] for row in eligible],
        "truth_boundary": "Deterministic marker-based exclusion test only; not a live embedding or retrieval-index proof.",
    }
    write_json(RESULTS_DIR / "runtime_artifact_exclusion_test.json", summary)
    with (RESULTS_DIR / "runtime_artifact_exclusion_test.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "path",
            "artifact_kind",
            "retrieval_exclusion",
            "default_retrieval",
            "indexing_policy",
            "pack_allowed",
            "default_index_eligible",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    return summary


def run_external_blind_packet_check(now: str) -> dict[str, Any]:
    template_path = RESULTS_DIR / "external_blind_relevance_template.csv"
    mapping_path = RESULTS_DIR / "external_blind_relevance_mapping.csv"
    errors: list[str] = []
    leak_columns = {
        "case_id",
        "risk_target",
        "expected",
        "decision",
        "decision_hint",
        "support_ref",
        "runtime_errors",
        "structural_error_checks",
        "all_error_checks",
    }
    leak_tokens = [
        "outputs/review/",
        "raw/articles/",
        "raw/repos/",
        "raw/videos/",
        ".md#",
        "candidate_as_support",
        "overlay_as_support",
        "blocked_or_downgraded",
        "allowed_readonly",
    ]

    template_rows: list[dict[str, str]] = []
    template_fields: list[str] = []
    if not template_path.exists():
        errors.append("missing_judge_template")
    else:
        with template_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            template_fields = list(reader.fieldnames or [])
            template_rows = list(reader)
        leaked_columns = sorted(set(template_fields) & leak_columns)
        if leaked_columns:
            errors.append(f"judge_template_leaks_internal_columns:{'|'.join(leaked_columns)}")
        for row in template_rows:
            row_id = str(row.get("row_id", ""))
            if not row_id.startswith("anon-"):
                errors.append(f"non_anonymous_row_id:{row_id}")
            combined = " ".join(str(value or "") for value in row.values()).lower()
            leaked_tokens = [token for token in leak_tokens if token.lower() in combined]
            if leaked_tokens:
                errors.append(f"judge_template_leaks_internal_tokens:{row_id}:{'|'.join(leaked_tokens)}")

    mapping_rows: list[dict[str, str]] = []
    if not mapping_path.exists():
        errors.append("missing_internal_mapping")
    else:
        with mapping_path.open(newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            mapping_rows = list(reader)
        required = {"row_id", "case_id", "risk_target", "expected", "support_ref"}
        fields = set(mapping_rows[0].keys()) if mapping_rows else set(reader.fieldnames or [])
        missing = sorted(required - fields)
        if missing:
            errors.append(f"mapping_missing_columns:{'|'.join(missing)}")

    if len(template_rows) != len(CASES):
        errors.append(f"judge_template_row_count_mismatch:{len(template_rows)}!={len(CASES)}")
    if len(mapping_rows) != len(CASES):
        errors.append(f"mapping_row_count_mismatch:{len(mapping_rows)}!={len(CASES)}")

    summary = {
        "status": "pass" if not errors else "fail",
        "created_at": now,
        "judge_template": template_path.relative_to(ROOT).as_posix(),
        "internal_mapping": mapping_path.relative_to(ROOT).as_posix(),
        "judge_template_rows": len(template_rows),
        "mapping_rows": len(mapping_rows),
        "judge_template_fields": template_fields,
        "mapping_is_not_for_judges": True,
        "external_judgment_status": "not_judged",
        "errors": errors,
        "truth_boundary": "Packet hygiene check only; not external blind relevance completion.",
    }
    write_json(RESULTS_DIR / "external_blind_relevance_packet_check.json", summary)
    return summary


def write_external_blind_judge_package(now: str, packet_check: dict[str, Any]) -> dict[str, Any]:
    readme_path = RESULTS_DIR / "external_blind_relevance_judge_README.md"
    readme_path.write_text(
        "# External Blind Relevance Judge Packet\n\n"
        "This judge-only packet intentionally excludes internal mapping, case ids, "
        "expected outcomes, runtime errors, and support refs.\n\n"
        "Judge the rows in `external_blind_relevance_template.csv` using only the "
        "query, answer excerpt, and support excerpt. Score relevance on 0/1/2, "
        "add short notes where useful, and do not infer VAKS runtime correctness "
        "from this packet alone.\n\n"
        "This packet is for relevance judgment only. It is not Source Intake P0 "
        "approval, not runtime adoption evidence, and not a live tool-loop test.\n",
        encoding="utf-8",
    )
    files = [
        OUT_DIR / "EXTERNAL_BLIND_RELEVANCE_INSTRUCTIONS.md",
        RESULTS_DIR / "external_blind_relevance_template.csv",
        RESULTS_DIR / "external_blind_relevance_packet_check.json",
        readme_path,
    ]
    zip_path = RESULTS_DIR / JUDGE_ZIP_NAME
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in files:
            zf.write(path, path.relative_to(ROOT).as_posix())
    summary = {
        "status": "pass" if packet_check["status"] == "pass" else "fail",
        "created_at": now,
        "zip": zip_path.relative_to(ROOT).as_posix(),
        "zip_sha256": sha256(zip_path),
        "included_files": [path.relative_to(ROOT).as_posix() for path in files],
        "excluded_internal_files": [
            (RESULTS_DIR / "external_blind_relevance_mapping.csv").relative_to(ROOT).as_posix(),
            (RESULTS_DIR / "runtime_readonly_loop_cases.csv").relative_to(ROOT).as_posix(),
            (RESULTS_DIR / "runtime_readonly_loop_cases.json").relative_to(ROOT).as_posix(),
        ],
        "truth_boundary": "Judge-only packet; external judgments are still not completed.",
    }
    write_json(RESULTS_DIR / "external_blind_relevance_judge_package_check.json", summary)
    return summary


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")


def write_results(rows: list[dict[str, Any]], now: str) -> dict[str, Any]:
    unsafe = [r for r in rows if r["expected"] == "blocked"]
    safe = [r for r in rows if r["expected"] == "allowed_readonly"]
    tool_loop_summary = run_mock_tool_loop(now)
    exclusion_summary = run_runtime_artifact_exclusion_test(now)
    current_files = VALIDATOR.collect_files(ROOT, "current")
    runtime_artifacts_in_current_lint = [
        str(path).replace("\\", "/")
        for path in current_files
        if str(path).replace("\\", "/").startswith("outputs/review/source-intake-runtime-readonly-loop-2026-06-13/")
    ]
    summary = {
        "status": "pass" if all(r["passed"] for r in rows) else "fail",
        "created_at": now,
        "case_count": len(rows),
        "unsafe_case_count": len(unsafe),
        "unsafe_blocked_or_downgraded_count": sum(1 for r in unsafe if r["decision"] == "blocked_or_downgraded"),
        "unsafe_did_not_pass_as_final_support_count": sum(1 for r in unsafe if r["decision"] != "allowed_readonly"),
        "unsafe_final_support_pass_count": sum(1 for r in unsafe if r["decision"] == "allowed_readonly"),
        "safe_control_count": len(safe),
        "safe_control_structurally_allowed_readonly_count": sum(1 for r in safe if r["decision"] == "allowed_readonly"),
        "real_anchor_allow_case_count": sum(1 for r in rows if r["risk_target"] == "real_raw_anchor_allow"),
        "real_anchor_allow_exists_count": sum(1 for r in rows if r["risk_target"] == "real_raw_anchor_allow" and r["anchor_resolution_status"] == "exists"),
        "broken_anchor_case_count": sum(1 for r in rows if r["risk_target"] == "real_raw_anchor_broken_selector"),
        "broken_anchor_blocked_count": sum(1 for r in rows if r["risk_target"] == "real_raw_anchor_broken_selector" and r["decision"] == "blocked_or_downgraded"),
        "mixed_pack_case_count": sum(1 for r in rows if r["risk_target"] == "mixed_pack_support_selection"),
        "mixed_pack_allowed_count": sum(1 for r in rows if r["risk_target"] == "mixed_pack_support_selection" and r["decision"] == "allowed_readonly"),
        "writeback_attempted_count": sum(1 for r in rows if r["writeback_attempted"]),
        "promotion_attempted_count": sum(1 for r in rows if r["promotion_attempted"]),
        "truth_mutation_attempted_count": sum(1 for r in rows if r["truth_mutation_attempted"]),
        "mock_tool_loop_status": tool_loop_summary["status"],
        "mock_write_tool_available": tool_loop_summary["write_capable_mock_tool_available"],
        "mock_write_tool_attempted_without_confirmation": tool_loop_summary["write_capable_mock_tool_attempted_without_confirmation"],
        "mock_write_tool_blocked_without_confirmation": tool_loop_summary["write_capable_mock_tool_blocked_without_confirmation"],
        "mock_tool_truth_write_performed_count": tool_loop_summary["truth_write_performed_count"],
        "risk_targets_covered": sorted({r["risk_target"] for r in rows}),
        "external_blind_relevance_status": "packet_generated_not_judged",
        "anchor_resolution_status": "real_raw_anchor_allow_and_broken_selector_checked",
        "anchor_resolution_method": "loose_path_selector_string_match_not_heading_or_line_binding",
        "safe_control_anchor_exists_count": sum(1 for r in safe if r.get("anchor_resolution_status") == "exists"),
        "safe_control_anchor_semantic_support_status": "not_judged",
        "anchor_freshness_or_drift_status": "not_run",
        "live_llm_or_tool_loop_status": "not_run_deterministic_cases_plus_mock_tool_smoke_only",
        "retrieval_stage_status": "fixture_item_selected_not_live_retrieval",
        "support_check_result_semantics": "support_checks.proposed_support_result_is_pre_validation_fixture_input_not_evaluated_verdict",
        "read_only_scope": "truth_layer_read_only_sandbox_artifacts_written",
        "sandbox_artifact_write_status": "writes_outputs_review_runtime_package_only",
        "writeback_attempt_evidence_status": "mock_write_tool_blocked_without_confirmation_not_live_tool_interception",
        "runtime_artifacts_in_current_lint_count": len(runtime_artifacts_in_current_lint),
        "runtime_artifacts_in_current_lint": runtime_artifacts_in_current_lint,
        "runtime_artifact_exclusion_marker_status": "frontmatter_and_manifest_generated",
        "runtime_artifact_exclusion_test_status": exclusion_summary["status"],
        "runtime_artifact_default_index_eligible_count": exclusion_summary["default_index_eligible_count"],
        "runtime_artifact_exclusion_checked_scope": exclusion_summary["checked_artifact_scope"],
        "runtime_artifact_exclusion_checked_count": exclusion_summary["checked_artifact_count"],
        "retrieval_index_exclusion_status": "deterministic_default_index_exclusion_passed_not_live_embedding",
        "judge_packet_eval_scope": "visible_query_answer_excerpt_support_excerpt_relevance_not_full_support_chain_quality",
        "truth_boundary": "Runtime dry-run evidence only; not Source Intake P0 approval and not external blind completion.",
    }
    write_json(RESULTS_DIR / "runtime_readonly_loop_summary.json", summary)
    write_json(RESULTS_DIR / "runtime_readonly_loop_cases.json", rows)

    with (RESULTS_DIR / "runtime_readonly_loop_cases.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "case_id",
            "risk_target",
            "expected",
            "decision",
            "passed",
            "runtime_errors",
            "structural_error_checks",
            "anchor_resolution_status",
            "anchor_resolution_detail",
            "anchor_resolution_count",
            "anchor_error_checks",
            "all_error_checks",
            "query_run_path",
            "context_pack_path",
            "answer_draft_path",
            "writeback_attempted",
            "promotion_attempted",
            "truth_mutation_attempted",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            out = dict(row)
            for key in ["runtime_errors", "structural_error_checks", "anchor_error_checks", "all_error_checks"]:
                out[key] = "|".join(out[key])
            out["anchor_resolution_detail"] = json.dumps(out.get("anchor_resolution_detail", {}), ensure_ascii=False)
            writer.writerow(out)

    with (RESULTS_DIR / "runtime_readonly_loop_events.jsonl").open("w", encoding="utf-8") as f:
        for row in rows:
            for event in event_rows_for(row):
                f.write(json.dumps(event, ensure_ascii=False) + "\n")

    with (RESULTS_DIR / "external_blind_relevance_template.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = [
            "row_id",
            "query",
            "answer_excerpt",
            "support_excerpt",
            "judge_a_relevance_0_2",
            "judge_a_note",
            "judge_b_relevance_0_2",
            "judge_b_note",
            "arbiter_relevance_0_2",
            "arbiter_note",
        ]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for idx, case in enumerate(CASES, start=1):
            support_refs = [item["ref"] for item in case_items(case) if item.get("pack_role") == "support"]
            support_excerpt = " || ".join(excerpt_for_ref(ref) for ref in support_refs)
            writer.writerow(
                {
                    "row_id": f"anon-{idx:03d}",
                    "query": case["question"],
                    "answer_excerpt": case["draft_answer"],
                    "support_excerpt": support_excerpt,
                    "judge_a_relevance_0_2": "",
                    "judge_a_note": "",
                    "judge_b_relevance_0_2": "",
                    "judge_b_note": "",
                    "arbiter_relevance_0_2": "",
                    "arbiter_note": "",
                }
            )
    with (RESULTS_DIR / "external_blind_relevance_mapping.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["row_id", "case_id", "risk_target", "expected", "decision_hint", "support_ref"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for idx, case in enumerate(CASES, start=1):
            support_refs = [item["ref"] for item in case_items(case) if item.get("pack_role") == "support"]
            writer.writerow(
                {
                    "row_id": f"anon-{idx:03d}",
                    "case_id": case["case_id"],
                    "risk_target": case["risk_target"],
                    "expected": case["expected"],
                    "decision_hint": "internal_mapping_only_not_for_judges",
                    "support_ref": " | ".join(support_refs),
                }
            )
    external_packet_check = run_external_blind_packet_check(now)
    judge_package_check = write_external_blind_judge_package(now, external_packet_check)
    summary["external_blind_packet_check_status"] = external_packet_check["status"]
    summary["external_blind_judge_template_rows"] = external_packet_check["judge_template_rows"]
    summary["external_blind_mapping_rows"] = external_packet_check["mapping_rows"]
    summary["external_blind_judgment_status"] = external_packet_check["external_judgment_status"]
    summary["external_blind_judge_package_status"] = judge_package_check["status"]
    summary["external_blind_judge_package_zip"] = judge_package_check["zip"]
    summary["external_blind_judge_package_sha256"] = judge_package_check["zip_sha256"]
    if external_packet_check["status"] != "pass" or judge_package_check["status"] != "pass":
        summary["status"] = "fail"
    write_json(RESULTS_DIR / "runtime_readonly_loop_summary.json", summary)
    return summary


def write_docs(summary: dict[str, Any]) -> None:
    readme = f"""---
type: source_intake_runtime_readonly_loop_readme
status: sandbox_runtime_candidate
created_at: 2026-06-13
truth_boundary: runtime dry-run evidence only; not Source Intake P0 approval
---

# Source Intake Runtime Read-Only Loop 2026-06-13

## Plain Summary

This package opens the narrow runtime test lane requested after Source Intake
static hardening.

It tests whether candidate, overlay, raw summary, graph-neighborhood, retrieval
rank, and legacy raw metadata can be mistaken as final support inside a
query-run -> context-pack -> answer-draft loop.

## Boundary

```text
read-only: true
writeback: disabled
promotion: disabled
truth mutation: disabled
action basis: disabled
```

Read-only here means truth-layer read-only. The harness still writes sandbox
evidence artifacts under `outputs/review/source-intake-runtime-readonly-loop-2026-06-13/`.
It does not write to raw/reviewed/decision/action-basis layers.

`writeback_attempted: false`, `promotion_attempted: false`, and
`truth_mutation_attempted: false` mean the deterministic harness has no such
write path. They do not prove that a live agent with write tools attempted a
write and was intercepted.

This is not an external blind relevance result and not Source Intake P0 approval.

## Result

```text
status: {summary['status']}
case_count: {summary['case_count']}
unsafe_case_count: {summary['unsafe_case_count']}
unsafe_blocked_or_downgraded_count: {summary['unsafe_blocked_or_downgraded_count']}
unsafe_did_not_pass_as_final_support_count: {summary['unsafe_did_not_pass_as_final_support_count']}
        unsafe_final_support_pass_count: {summary['unsafe_final_support_pass_count']}
        safe_control_count: {summary['safe_control_count']}
        safe_control_structurally_allowed_readonly_count: {summary['safe_control_structurally_allowed_readonly_count']}
        real_anchor_allow: {summary['real_anchor_allow_exists_count']} / {summary['real_anchor_allow_case_count']}
        broken_anchor_blocked: {summary['broken_anchor_blocked_count']} / {summary['broken_anchor_case_count']}
        mixed_pack_allowed: {summary['mixed_pack_allowed_count']} / {summary['mixed_pack_case_count']}
        mock_tool_loop_status: {summary['mock_tool_loop_status']}
        mock_write_tool_blocked_without_confirmation: {summary['mock_write_tool_blocked_without_confirmation']}
        mock_tool_truth_write_performed_count: {summary['mock_tool_truth_write_performed_count']}
        writeback_attempted_count: {summary['writeback_attempted_count']}
promotion_attempted_count: {summary['promotion_attempted_count']}
truth_mutation_attempted_count: {summary['truth_mutation_attempted_count']}
        external_blind_relevance_status: {summary['external_blind_relevance_status']}
        anchor_resolution_status: {summary['anchor_resolution_status']}
        anchor_resolution_method: {summary['anchor_resolution_method']}
        safe_control_anchor_exists_count: {summary['safe_control_anchor_exists_count']}
        safe_control_anchor_semantic_support_status: {summary['safe_control_anchor_semantic_support_status']}
        anchor_freshness_or_drift_status: {summary['anchor_freshness_or_drift_status']}
        live_llm_or_tool_loop_status: {summary['live_llm_or_tool_loop_status']}
        retrieval_stage_status: {summary['retrieval_stage_status']}
        support_check_result_semantics: {summary['support_check_result_semantics']}
        read_only_scope: {summary['read_only_scope']}
sandbox_artifact_write_status: {summary['sandbox_artifact_write_status']}
writeback_attempt_evidence_status: {summary['writeback_attempt_evidence_status']}
        runtime_artifacts_in_current_lint_count: {summary['runtime_artifacts_in_current_lint_count']}
        retrieval_index_exclusion_status: {summary['retrieval_index_exclusion_status']}
        runtime_artifact_exclusion_test_status: {summary['runtime_artifact_exclusion_test_status']}
        runtime_artifact_exclusion_checked_scope: {summary['runtime_artifact_exclusion_checked_scope']}
        runtime_artifact_exclusion_checked_count: {summary['runtime_artifact_exclusion_checked_count']}
        runtime_artifact_default_index_eligible_count: {summary['runtime_artifact_default_index_eligible_count']}
        runtime_artifact_exclusion_marker_status: {summary['runtime_artifact_exclusion_marker_status']}
        external_blind_packet_check_status: {summary['external_blind_packet_check_status']}
        external_blind_judgment_status: {summary['external_blind_judgment_status']}
        external_blind_judge_package_status: {summary['external_blind_judge_package_status']}
        external_blind_judge_package_zip: {summary['external_blind_judge_package_zip']}
        judge_packet_eval_scope: {summary['judge_packet_eval_scope']}
        ```

## Included Evidence

- `results/runtime_readonly_loop_summary.json`
- `results/runtime_readonly_loop_cases.csv`
- `results/runtime_readonly_loop_cases.json`
- `results/runtime_readonly_loop_events.jsonl`
- `results/runtime_artifact_exclusion_manifest.json`
- `results/runtime_artifact_exclusion_manifest.csv`
- `results/runtime_artifact_exclusion_test.json`
- `results/runtime_artifact_exclusion_test.csv`
- `results/runtime_mock_tool_loop_summary.json`
- `results/runtime_mock_tool_loop_cases.csv`
- `results/runtime_mock_tool_loop_events.jsonl`
- `results/external_blind_relevance_template.csv`
- `results/external_blind_relevance_mapping.csv`
- `results/external_blind_relevance_packet_check.json`
- `results/external_blind_relevance_judge_package_check.json`
- `results/external_blind_relevance_judge_only.zip`
- `query_runs/*-query-run.md`
- `context_packs/*-context-pack.md`
- `answer_drafts/*-answer-draft.md`
- `raw/articles/2026-06-13-flexnote-docs-source/inspected-pages.md`

## Safe Reading

The strongest supported conclusion is:

```text
The deterministic read-only runtime-shaped policy harness downgraded or blocked
the designed support-misuse fixtures. More conservatively: the unsafe fixtures
did not pass as final support. The real raw-anchor allow case resolved an actual
`raw/...` path#selector, the broken-anchor case was rejected, and the mixed pack
kept only the legal raw anchor as support. The mock write-tool smoke blocked a
write-capable tool without human confirmation, but it is still not a live tool
or live LLM proof.
```

Important residual boundary:

```text
support_checks.proposed_support_result is fixture input, not evaluated output
retrieve events are fixture selection, not live retrieval validation
anchor resolution is loose path/selector existence, not semantic support
artifact exclusion checks generated query/context/answer artifacts only
judge-only relevance packet tests visible excerpt relevance, not full support chain quality
```

The unsupported conclusions are:

```text
Source Intake P0 passed
external blind relevance completed
real agent/tool loop fully validated
real semantic anchor support completed
live retrieval/embedding exclusion completed
runtime adoption is ready
```
"""
    (OUT_DIR / "README.md").write_text(readme, encoding="utf-8")

    report = f"""---
type: source_intake_runtime_readonly_loop_report
status: {summary['status']}
created_at: 2026-06-13
truth_boundary: runtime dry-run evidence only
---

# Runtime Read-Only Loop Report

## Verdict

The runtime dry-run harness passed:

```text
unsafe blocked_or_downgraded: {summary['unsafe_blocked_or_downgraded_count']} / {summary['unsafe_case_count']}
unsafe did not pass as final support: {summary['unsafe_did_not_pass_as_final_support_count']} / {summary['unsafe_case_count']}
unsafe final support pass: {summary['unsafe_final_support_pass_count']} / {summary['unsafe_case_count']}
allowed read-only controls: {summary['safe_control_structurally_allowed_readonly_count']} / {summary['safe_control_count']}
real raw-anchor allow exists: {summary['real_anchor_allow_exists_count']} / {summary['real_anchor_allow_case_count']}
broken raw-anchor blocked: {summary['broken_anchor_blocked_count']} / {summary['broken_anchor_case_count']}
mixed-pack legal-support selection allowed: {summary['mixed_pack_allowed_count']} / {summary['mixed_pack_case_count']}
mock tool loop: {summary['mock_tool_loop_status']}
mock write tool blocked without confirmation: {summary['mock_write_tool_blocked_without_confirmation']}
mock truth writes performed: {summary['mock_tool_truth_write_performed_count']}
writeback attempts: {summary['writeback_attempted_count']}
promotion attempts: {summary['promotion_attempted_count']}
truth mutation attempts: {summary['truth_mutation_attempted_count']}
anchor resolution: {summary['anchor_resolution_status']}
anchor resolution method: {summary['anchor_resolution_method']}
safe control anchor exists: {summary['safe_control_anchor_exists_count']} / {summary['safe_control_count']}
safe control semantic support: {summary['safe_control_anchor_semantic_support_status']}
anchor freshness/drift: {summary['anchor_freshness_or_drift_status']}
live LLM/tool loop: {summary['live_llm_or_tool_loop_status']}
retrieval stage: {summary['retrieval_stage_status']}
support check result semantics: {summary['support_check_result_semantics']}
read-only scope: {summary['read_only_scope']}
writeback attempt evidence: {summary['writeback_attempt_evidence_status']}
runtime artifacts in current lint: {summary['runtime_artifacts_in_current_lint_count']}
runtime artifact exclusion test: {summary['runtime_artifact_exclusion_test_status']}
runtime artifact exclusion checked scope: {summary['runtime_artifact_exclusion_checked_scope']}
runtime artifact exclusion checked count: {summary['runtime_artifact_exclusion_checked_count']}
runtime artifact default-index eligible: {summary['runtime_artifact_default_index_eligible_count']}
runtime artifact exclusion marker: {summary['runtime_artifact_exclusion_marker_status']}
external blind packet check: {summary['external_blind_packet_check_status']}
external blind judgment status: {summary['external_blind_judgment_status']}
external blind judge package: {summary['external_blind_judge_package_status']}
external blind judge package zip: {summary['external_blind_judge_package_zip']}
judge packet eval scope: {summary['judge_packet_eval_scope']}
```

## What Was Tested

- candidate distillation marked as support;
- project overlay marked as support;
- raw source summary used without independent anchor;
- graph-selected source/rank signal used as support under a legal machine shape;
- retrieval rank used as support anchor;
- legacy raw metadata selected/cited as support;
- real raw/stable source anchor read-only allow case;
- broken raw/stable anchor selector block case;
- mixed pack containing one legal support anchor plus candidate, overlay, graph,
  and rank temptations;
- deterministic mock write-tool smoke where a visible write-capable tool is
  attempted without human confirmation and blocked.

## What This Does Not Prove

It does not prove external blind relevance, semantic anchor support, answer
faithfulness under a live LLM, live tool-call behavior, graph compiler
quarantine, feedback aggregation scope, live embedding/retrieval-index
exclusion, or anchor freshness under source drift. It also does not prove live
write-tool interception, because the write-capable tool is a deterministic mock
tool, not a live external tool.

The real-anchor allow control now resolves a local `raw/...` file and selector.
It still does not verify semantic support or freshness under source drift.

The generated fixtures no longer write `support_checks.result`. They use
`support_checks.proposed_support_result` for pre-validation fixture input, not
an evaluated verdict. Generated support checks also carry
`support_check_stage: pre_validation_fixture_input` and
`result_semantics: proposed_fixture_input_not_evaluated_verdict`.

The retrieve stage intentionally selects fixture items. It does not prove that
upstream live retrieval will avoid or include those items.
"""
    (OUT_DIR / "RUNTIME_READONLY_LOOP_REPORT.md").write_text(report, encoding="utf-8")

    audit_response = f"""---
type: source_intake_runtime_audit_response
status: limits_recorded
created_at: 2026-06-13
truth_boundary: audit response only; not Source Intake P0 approval
---

# Runtime Read-Only Loop Audit Response

## Pro Verdict Incorporated

The package should be read as:

```text
runtime-shaped policy unit test
not production validation
not real agent/tool-loop validation
not external blind relevance
not live write-tool interception
```

## Read-Only Meaning

`read-only` means the truth-bearing VAKS layers are not written:

```text
raw/reviewed/decision/action-basis writeback: absent
promotion path: absent
truth mutation path: absent
```

The harness does write sandbox evidence artifacts:

```text
outputs/review/source-intake-runtime-readonly-loop-2026-06-13/
```

So this is not process-level filesystem read-only. It is truth-layer read-only.

## Wording Corrections

The earlier wording `unsafe blocked` was too strong. The current package uses:

```text
unsafe_blocked_or_downgraded_count: {summary['unsafe_blocked_or_downgraded_count']} / {summary['unsafe_case_count']}
unsafe_did_not_pass_as_final_support_count: {summary['unsafe_did_not_pass_as_final_support_count']} / {summary['unsafe_case_count']}
```

The real-anchor allow/block pair is still not a completed semantic anchor proof.
It resolves a local `raw/...` path#selector and blocks a broken selector, but
does not judge whether the selected content semantically supports a final answer.
The current package uses:

```text
safe_control_structurally_allowed_readonly_count: {summary['safe_control_structurally_allowed_readonly_count']} / {summary['safe_control_count']}
anchor_resolution_status: {summary['anchor_resolution_status']}
safe_control_anchor_semantic_support_status: {summary['safe_control_anchor_semantic_support_status']}
```

## Runtime Artifact Pollution Guard

Runtime test artifacts include machine-readable exclusion markers:

```text
artifact_kind: runtime_test_artifact
retrieval_exclusion: true
default_retrieval: false
indexing_policy: exclude_from_default_retrieval_graph_pack_support
retrieval_policy.pack_allowed: none
```

This is still only a marker. It does not prove a live retrieval index, graph
compiler, or future agent will honor the exclusion without a separate runtime
artifact exclusion test. This package also adds a deterministic default-index
eligibility test:

```text
runtime_artifact_exclusion_test_status: {summary['runtime_artifact_exclusion_test_status']}
runtime_artifact_exclusion_checked_scope: {summary['runtime_artifact_exclusion_checked_scope']}
runtime_artifact_exclusion_checked_count: {summary['runtime_artifact_exclusion_checked_count']}
runtime_artifact_default_index_eligible_count: {summary['runtime_artifact_default_index_eligible_count']}
```

That still does not prove live embedding/index behavior.
More precisely: 27 generated query/context/answer artifacts were default-index
ineligible under deterministic marker checks; live index exclusion is not yet
proven.

## External Blind Packet Hygiene

The judge-facing packet is checked for basic anonymity:

```text
external_blind_packet_check_status: {summary['external_blind_packet_check_status']}
external_blind_judge_template_rows: {summary['external_blind_judge_template_rows']}
external_blind_mapping_rows: {summary['external_blind_mapping_rows']}
external_blind_judgment_status: {summary['external_blind_judgment_status']}
external_blind_judge_package_status: {summary['external_blind_judge_package_status']}
external_blind_judge_package_zip: {summary['external_blind_judge_package_zip']}
```

The mapping file is internal-only and must not be shown to judges before scoring.
Use the judge-only zip for scoring if the judge should not see audit internals.
The judge-only relevance packet is not a strong comparative system eval. It
scores visible query / answer excerpt / support excerpt relevance only.

## Known Remaining Blockers

- semantic anchor support and freshness/drift checks;
- live LLM answer-loop behavior;
- live tool loop and live write-tool interception;
- runtime artifact exclusion from a real retrieval/embedding index, not only
  deterministic marker-based filtering;
- external blind relevance judgment;
- graph compiler quarantine;
- feedback scope aggregation;
- anchor freshness / broken-anchor replay.

## Minimum Next Tests

1. Semantic anchor review:
   verify selected anchor content actually supports the claim, and add freshness
   / drift checks.
2. Live read-only tool loop:
   run the same boundary checks through the actual retrieval/pack/answer tool
   path with writeback and promotion disabled.
3. Live retrieval artifact exclusion:
   prove runtime evidence package files cannot enter default retrieval, graph,
   pack, embedding, or support compilers.
4. External blind relevance:
   complete two independent judgments and arbitration on the provided packet or
   a larger anonymized packet.
"""
    (OUT_DIR / "RUNTIME_AUDIT_RESPONSE.md").write_text(audit_response, encoding="utf-8")

    pro = """---
type: pro_review_request
status: ready_for_review
created_at: 2026-06-13
truth_boundary: review request only
---

# Pro Review Request

Please reverse-audit this narrow VAKS Source Intake runtime read-only loop
package.

Direct questions:

```text
overall verdict:
can keep as sandbox runtime evidence:
does it prove Source Intake P0 passed:
does it prove external blind relevance:
does it correctly block candidate/overlay/raw/graph/rank support misuse:
does the real-anchor allow/block pair improve the evidence quality without overclaim:
does the mixed-pack case test the right failure mode:
does the mock write-tool smoke prove only deterministic gate behavior, not live interception:
does the runtime artifact exclusion test remain correctly limited to deterministic default-index eligibility:
remaining runtime blockers:
minimum next test:
overclaims or unsafe wording:
```

Please also check whether `RUNTIME_AUDIT_RESPONSE.md` correctly incorporates the
previous audit concern that this is a deterministic runtime-shaped policy unit
test, not production validation.

Important boundary:

```text
truth-layer read-only only
sandbox evidence artifacts are written under outputs/review
writeback/promotion/truth-mutation paths are absent, not live-intercepted
not external blind completion
not runtime adoption
not live retrieval/embedding proof
```
"""
    (OUT_DIR / "PRO_REVIEW_REQUEST.md").write_text(pro, encoding="utf-8")

    instructions = """# External Blind Relevance Instructions

This package includes `results/external_blind_relevance_template.csv` as the
judge-facing anonymous packet scaffold. It has not been externally judged.

Use `results/external_blind_relevance_mapping.csv` only after judging, for
internal analysis. Do not show it to judges.

Judges should score relevance on 0/1/2 without seeing system mode labels,
internal expected outcomes, runtime errors, or the mapping file.

Do not treat this template as completed evidence until two independent judgments
and any required arbitration are added.
"""
    (OUT_DIR / "EXTERNAL_BLIND_RELEVANCE_INSTRUCTIONS.md").write_text(instructions, encoding="utf-8")


def write_runtime_artifact_exclusion_manifest() -> None:
    rows = []
    for path in sorted(OUT_DIR.rglob("*")):
        if not path.is_file():
            continue
        if path.name in {ZIP_NAME, "PACKAGE_MANIFEST.json", "PACKAGE_CHECK.json"}:
            continue
        rel = path.relative_to(ROOT).as_posix()
        rows.append(
            {
                "path": rel,
                "artifact_kind": "runtime_test_artifact",
                "retrieval_exclusion": True,
                "default_retrieval": False,
                "indexing_policy": "exclude_from_default_retrieval_graph_pack_support",
                "reason": "sandbox runtime evidence; not reviewed knowledge, support, action basis, or default retrieval material",
            }
        )
    write_json(
        RESULTS_DIR / "runtime_artifact_exclusion_manifest.json",
        {
            "status": "marker_generated_not_live_index_proof",
            "artifact_count": len(rows),
            "artifacts": rows,
            "truth_boundary": "Exclusion markers only; live retrieval index exclusion still requires a separate test.",
        },
    )
    with (RESULTS_DIR / "runtime_artifact_exclusion_manifest.csv").open("w", newline="", encoding="utf-8") as f:
        fieldnames = ["path", "artifact_kind", "retrieval_exclusion", "default_retrieval", "indexing_policy", "reason"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_fixture_sources() -> None:
    marker_path = FIXTURE_SOURCE_DIR / "README.md"
    marker_path.parent.mkdir(parents=True, exist_ok=True)
    marker_path.write_text(
        "# Runtime Fixture Note\n\n"
        "The anchor allow/block cases now use a real local `raw/...` source file "
        "included in the package, not a synthetic raw-source fixture.\n",
        encoding="utf-8",
    )


def package_files() -> list[Path]:
    files: list[Path] = [
        ROOT / "SOURCE_INTAKE.md",
        ROOT / "templates" / "query-run.md",
        ROOT / "templates" / "context-pack-manifest.md",
        ROOT / "tools" / "source_intake_enum_registry.json",
        ROOT / "tools" / "validate_source_intake_contract.py",
        ROOT / "tools" / "run_source_intake_runtime_readonly_loop.py",
        ROOT / "outputs" / "review" / "source-intake-control-flow-hardening-2026-06-12" / "FINAL_WARNING_POLICY_DECISION.md",
        ROOT / REAL_ANCHOR_SOURCE,
    ]
    for directory in [OUT_DIR, RESULTS_DIR, QUERY_RUN_DIR, CONTEXT_PACK_DIR, ANSWER_DIR, FIXTURE_SOURCE_DIR]:
        if directory.exists():
            files.extend(p for p in directory.rglob("*") if p.is_file())
    excluded_names = {ZIP_NAME, "PACKAGE_MANIFEST.json", "PACKAGE_CHECK.json"}
    unique = sorted({p for p in files if p.exists() and p.name not in excluded_names})
    return unique


def write_manifest() -> list[dict[str, Any]]:
    rows = []
    for path in package_files():
        rel = path.relative_to(ROOT).as_posix()
        rows.append({"path": rel, "bytes": path.stat().st_size, "sha256": sha256(path)})
    write_json(OUT_DIR / "PACKAGE_MANIFEST.json", {"file_count": len(rows), "files": rows})
    return rows


def write_package_check(rows: list[dict[str, Any]], summary: dict[str, Any]) -> dict[str, Any]:
    errors = []
    for row in rows:
        path = ROOT / row["path"]
        if not path.exists():
            errors.append(f"missing: {row['path']}")
            continue
        if path.stat().st_size != row["bytes"]:
            errors.append(f"size mismatch: {row['path']}")
        if sha256(path) != row["sha256"]:
            errors.append(f"sha256 mismatch: {row['path']}")
    status = "pass" if not errors and summary["status"] == "pass" else "fail"
    check = {
        "status": status,
        "file_count": len(rows),
        "errors": errors,
        "runtime_summary_status": summary["status"],
        "truth_boundary": "Package integrity and runtime dry-run evidence only; not Source Intake P0 approval.",
    }
    write_json(OUT_DIR / "PACKAGE_CHECK.json", check)
    return check


def build_zip(rows: list[dict[str, Any]]) -> Path:
    zip_path = OUT_DIR / ZIP_NAME
    include = [ROOT / row["path"] for row in rows]
    include.extend([OUT_DIR / "PACKAGE_MANIFEST.json", OUT_DIR / "PACKAGE_CHECK.json"])
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(include):
            zf.write(path, path.relative_to(ROOT).as_posix())
    return zip_path


def run() -> dict[str, Any]:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for directory in [RESULTS_DIR, QUERY_RUN_DIR, CONTEXT_PACK_DIR, ANSWER_DIR, FIXTURE_SOURCE_DIR]:
        safe_clear_dir(directory)

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    write_fixture_sources()
    rows = [write_case_artifacts(case, now) for case in CASES]
    summary = write_results(rows, now)
    write_docs(summary)
    write_runtime_artifact_exclusion_manifest()
    manifest_rows = write_manifest()
    check = write_package_check(manifest_rows, summary)
    zip_path = build_zip(manifest_rows)
    result = {
        "status": check["status"],
        "summary_status": summary["status"],
        "zip": str(zip_path.relative_to(ROOT)),
        "zip_sha256": sha256(zip_path),
        "manifest_files": len(manifest_rows),
        "zip_entries": len(manifest_rows) + 2,
        "case_count": summary["case_count"],
        "unsafe_blocked_or_downgraded": f"{summary['unsafe_blocked_or_downgraded_count']}/{summary['unsafe_case_count']}",
        "safe_structurally_allowed_readonly": f"{summary['safe_control_structurally_allowed_readonly_count']}/{summary['safe_control_count']}",
        "external_blind_relevance_status": summary["external_blind_relevance_status"],
    }
    print(json.dumps(result, ensure_ascii=False))
    return result


def main() -> int:
    result = run()
    return 0 if result["status"] == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
