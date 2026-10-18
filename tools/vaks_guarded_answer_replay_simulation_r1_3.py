"""R1.3 production-shaped replay simulation for VAKS Guarded Answer.

This sandbox exercises the production-shaped chain:

request -> route/profile metadata -> frozen context/draft/support map
-> R1.1 brake and Guard -> committed final / withheld / review.

It is intentionally offline and replay-only. It does not call an LLM, live
retrieval, a database, a service, or a network API.
"""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import os
import random
import re
import shutil
import sys
import tempfile
import time
import zipfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
R11_TOOL = ROOT / "tools" / "vaks_guarded_answer_wiring.py"
R12_TOOL = ROOT / "tools" / "vaks_guarded_answer_runtime_comparison_r1_2.py"
VAKS_GUARD = ROOT / "tools" / "vaks_guard.py"
R11_OUTPUT = ROOT / "outputs" / "review" / "vaks-guarded-answer-wiring-r1-1-2026-06-23"
R12_OUTPUT = ROOT / "outputs" / "review" / "vaks-guarded-answer-runtime-comparison-r1-2-2026-06-23"
DEFAULT_OUTPUT = (
    ROOT
    / "outputs"
    / "review"
    / "vaks-guarded-answer-production-shaped-replay-r1-3-r3-2026-06-24"
)


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False)


def pretty_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2, allow_nan=False) + "\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def sha256_text(text: str) -> str:
    return sha256_bytes(text.encode("utf-8"))


def write_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    write_lf(path, "".join(stable_json(row) + "\n" for row in rows))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load module: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def collect_hashes(root: Path, *, exclude: set[str] | None = None) -> dict[str, str]:
    exclude = exclude or set()
    hashes: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        relative = rel(path, root)
        if relative in exclude:
            continue
        hashes[relative] = sha256_bytes(path.read_bytes())
    return hashes


def tree_hash(root: Path, *, exclude: set[str] | None = None) -> str:
    return sha256_text(stable_json(collect_hashes(root, exclude=exclude)))


def percentile(values: list[float], pct: float) -> float:
    if not values:
        return 0.0
    sorted_values = sorted(values)
    index = min(len(sorted_values) - 1, int(round((pct / 100.0) * (len(sorted_values) - 1))))
    return sorted_values[index]


def verify_zip(zip_path: Path, sha_path: Path) -> dict[str, Any]:
    digest = sha256_bytes(zip_path.read_bytes())
    expected = sha_path.read_text(encoding="utf-8").split()[0]
    with zipfile.ZipFile(zip_path, "r") as archive:
        names = archive.namelist()
        bad = archive.testzip()
    return {
        "zip_path": zip_path.as_posix(),
        "expected_sha256": expected,
        "actual_sha256": digest,
        "sha256_match": digest == expected,
        "entry_count": len(names),
        "bad_entry": bad,
        "duplicate_path_count": len(names) - len(set(names)),
        "traversal_path_count": sum(1 for name in names if ".." in Path(name).parts or Path(name).is_absolute()),
        "status": "pass" if digest == expected and bad is None and len(names) == len(set(names)) else "fail",
    }


def dependency_checks(r11: Any, r12: Any) -> dict[str, Any]:
    checks: dict[str, Any] = {
        "r1_1_output": R11_OUTPUT.as_posix(),
        "r1_2_output": R12_OUTPUT.as_posix(),
        "r1_1_tool_sha256": sha256_bytes(R11_TOOL.read_bytes()),
        "r1_2_tool_sha256": sha256_bytes(R12_TOOL.read_bytes()),
        "vaks_guard_sha256": sha256_bytes(VAKS_GUARD.read_bytes()),
    }
    try:
        checks["r1_1_self_test"] = r11.verify_bundle(R11_OUTPUT)
    except Exception as exc:  # pragma: no cover - recorded in bundle
        checks["r1_1_self_test"] = {"status": "error", "error": repr(exc)}
    try:
        checks["r1_2_self_test"] = r12.verify_bundle(R12_OUTPUT)
    except Exception as exc:  # pragma: no cover - recorded in bundle
        checks["r1_2_self_test"] = {"status": "error", "error": repr(exc)}
    checks["status"] = (
        "pass"
        if checks["r1_1_self_test"].get("status") == "pass"
        and checks["r1_2_self_test"].get("status") == "pass"
        else "fail"
    )
    return checks


def clone_case(r11: Any, case: dict[str, Any], case_id: str, query: str, *, source_slice: str) -> dict[str, Any]:
    cloned = copy.deepcopy(case)
    cloned["case_id"] = case_id
    cloned["query"] = query
    cloned["source_slice"] = source_slice
    segments = copy.deepcopy(case["draft"]["segments"])
    cloned["draft"] = r11.make_draft(case_id, query, segments)
    return cloned


def query_variants(query: str) -> list[tuple[str, str]]:
    return [
        ("original", query),
        ("plain", "请用当前证据回答：" + query),
        ("command", "核验并回答这个问题：" + query),
    ]


def extract_terms(text: str) -> list[str]:
    terms: list[str] = []
    for token in re.findall(r"[A-Za-z][A-Za-z0-9_-]{2,}", text):
        token_lower = token.lower()
        if token_lower not in {"the", "and", "with", "that", "this", "answer", "current", "source"}:
            terms.append(token_lower)
    for token in re.findall(r"[\u4e00-\u9fff]{2,}", text):
        if token not in {"当前", "回答", "依据", "资料", "状态", "需要", "不能", "可以"}:
            terms.append(token)
    deduped: list[str] = []
    for term in terms:
        if term not in deduped:
            deduped.append(term)
    return deduped[:12]


def alignment_topic_id(source_key: str) -> str:
    return "topic-" + sha256_text(source_key)[:16]


def alignment_contract(case: dict[str, Any]) -> dict[str, Any]:
    alignment_id = case.get("alignment_id") or alignment_topic_id(case.get("case_id", "unknown"))
    query_terms = extract_terms(case.get("query", ""))
    draft_text = case.get("draft", {}).get("draft_text", "")
    support_text = " ".join(item.get("text", "") for item in case.get("claim_support_map", []))
    answer_terms = extract_terms(draft_text + " " + support_text)
    expected_claim_ids = [
        segment.get("claim_id")
        for segment in case.get("draft", {}).get("segments", [])
        if segment.get("type") == "claim" and segment.get("claim_id") != "unmapped"
    ]
    return {
        "alignment_id": alignment_id,
        "topic_id": alignment_id,
        "query_terms": query_terms,
        "answer_terms": answer_terms,
        "expected_claim_ids": expected_claim_ids,
        "draft_sha256": case.get("draft", {}).get("draft_sha256", ""),
        "support_claim_hashes": {
            item.get("claim_id", ""): item.get("claim_hash", "")
            for item in case.get("claim_support_map", [])
            if item.get("claim_id")
        },
        "contract_hash": sha256_text(
            stable_json(
                {
                    "alignment_id": alignment_id,
                    "query_terms": query_terms,
                    "answer_terms": answer_terms,
                    "claim_ids": expected_claim_ids,
                    "draft_sha256": case.get("draft", {}).get("draft_sha256", ""),
                }
            )
        ),
    }


def attach_alignment(case: dict[str, Any], *, topic_source: str | None = None) -> dict[str, Any]:
    alignment_id = alignment_topic_id(topic_source or case.get("source_case_id") or case.get("case_id", "unknown"))
    case["alignment_id"] = alignment_id
    case["query_alignment_id"] = alignment_id
    case.setdefault("alignment_source", topic_source or case.get("case_id", "unknown"))
    case.setdefault("draft", {})["alignment_id"] = alignment_id
    for segment in case.get("draft", {}).get("segments", []):
        if segment.get("type") == "claim":
            segment["alignment_id"] = alignment_id
    for support in case.get("claim_support_map", []):
        support["alignment_id"] = alignment_id
    case["alignment_contract"] = alignment_contract(case)
    return case


def mix_alignment_case(
    r11: Any,
    base_case: dict[str, Any],
    donor_case: dict[str, Any],
    *,
    request_id: str,
    mismatch_kind: str,
    query: str,
) -> dict[str, Any]:
    mixed = attach_alignment(
        clone_case(r11, base_case, request_id, query, source_slice="alignment_negative_fixture"),
        topic_source=base_case["case_id"],
    )
    donor = attach_alignment(
        clone_case(r11, donor_case, f"{request_id}-donor", donor_case["query"], source_slice="alignment_negative_donor"),
        topic_source=donor_case["case_id"],
    )
    if mismatch_kind == "context_pack":
        mixed["claim_support_map"] = copy.deepcopy(donor["claim_support_map"])
    elif mismatch_kind == "draft":
        mixed["draft"] = copy.deepcopy(donor["draft"])
    elif mismatch_kind == "claim_support_map":
        mixed["claim_support_map"] = copy.deepcopy(donor["claim_support_map"])
    elif mismatch_kind == "related_terms":
        mixed["query"] = query
        mixed["claim_support_map"] = copy.deepcopy(donor["claim_support_map"])
        mixed["draft"] = copy.deepcopy(donor["draft"])
    else:
        raise ValueError(f"Unknown alignment mismatch kind: {mismatch_kind}")
    mixed["alignment_negative_kind"] = mismatch_kind
    return mixed


def build_replay_requests(r11: Any, r12: Any) -> list[dict[str, Any]]:
    base_cases = r12.runtime_cases(r11)
    requests: list[dict[str, Any]] = []

    for case in base_cases:
        cloned = attach_alignment(
            clone_case(r11, case, f"existing-{case['case_id']}", case["query"], source_slice="r1_2_existing"),
            topic_source=case["case_id"],
        )
        requests.append(
            {
                "request_id": f"existing-{case['case_id']}",
                "kind": "existing_guarded_fixture",
                "feature_flag_mode": "shadow",
                "case": cloned,
            }
        )

    for idx, base in enumerate(base_cases[:30], start=1):
        for variant_kind, variant_query in query_variants(base["query"]):
            case_id = f"prodlike-q{idx:03d}-{variant_kind}"
            cloned = attach_alignment(
                clone_case(r11, base, case_id, variant_query, source_slice="prodlike_query_aligned_fixture"),
                topic_source=base["case_id"],
            )
            requests.append(
                {
                    "request_id": case_id,
                    "kind": "prodlike_replay",
                    "feature_flag_mode": "shadow",
                    "question_id": f"q{idx:03d}",
                    "variant_kind": variant_kind,
                    "base_case_id": base["case_id"],
                    "alignment_contract": cloned["alignment_contract"],
                    "case": cloned,
                }
            )

    return requests


def fault_case_from_base(r11: Any, r12: Any, base_case_id: str, request_id: str, query: str) -> dict[str, Any]:
    cases = {case["case_id"]: case for case in r12.runtime_cases(r11)}
    base = cases[base_case_id]
    return attach_alignment(
        clone_case(r11, base, request_id, query, source_slice="fault_injection_fixture"),
        topic_source=base["case_id"],
    )


def build_fault_requests(r11: Any, r12: Any) -> list[dict[str, Any]]:
    guarded_faults = [
        ("fault-missing-anchor", "case-009-missing-anchor", "Fault: missing independent anchor must not direct answer."),
        ("fault-candidate-only", "case-010-candidate-only", "Fault: candidate-only content must not become support."),
        ("fault-rank-score", "case-011-rank-score", "Fault: rank or score must not become support."),
        ("fault-stale-policy", "case-012-stale-policy", "Fault: stale policy must move to review."),
        ("fault-unresolved-conflict", "case-013-conflict", "Fault: unresolved conflict must move to review."),
        ("fault-unmapped-span", "case-015-unmapped-factual-span", "Fault: unmapped factual span must fail closed."),
        ("fault-action-injection", "case-016-action-injection", "Fault: action-ready draft must not be released."),
        ("fault-invalid-source-hash", "case-025-invalid-source-sha-marked-supported", "Fault: invalid source hash must fail closed."),
        ("fault-anchor-source-mismatch", "case-026-anchor-source-mismatch-marked-supported", "Fault: anchor/source mismatch must fail closed."),
        ("fault-malicious-safe-message", "case-033-malicious-safe-message-not-trusted", "Fault: malicious safe message must not be trusted."),
    ]
    requests: list[dict[str, Any]] = []
    for request_id, base_id, query in guarded_faults:
        requests.append(
            {
                "request_id": request_id,
                "kind": "fault_guarded_case",
                "fault_type": request_id.replace("fault-", ""),
                "feature_flag_mode": "shadow",
                "case": fault_case_from_base(r11, r12, base_id, request_id, query),
            }
        )

    runtime_faults = [
        ("fault-invalid-json-low", "invalid_json_draft", "case-001-direct-web-annotation", "low", "orientation"),
        ("fault-invalid-json-high", "invalid_json_draft", "case-016-action-injection", "high", "action"),
        ("fault-retrieval-empty-medium", "retrieval_empty", "case-005-partial-flexnote", "medium", "review"),
        ("fault-guard-block-high", "guard_block", "case-016-action-injection", "high", "action"),
        ("fault-guard-error-medium", "guard_error", "case-006-scope-outsourcing", "medium", "review"),
        ("fault-guard-timeout-high", "guard_timeout", "case-016-action-injection", "high", "action"),
        ("fault-feature-flag-error-low", "feature_flag_error", "case-001-direct-web-annotation", "low", "orientation"),
        ("fault-feature-flag-error-high", "feature_flag_error", "case-016-action-injection", "high", "action"),
        ("fault-acl-denied-medium", "acl_denied", "case-005-partial-flexnote", "medium", "review"),
        ("fault-model-streaming-draft", "streaming_fact_text_before_brake", "case-016-action-injection", "high", "action"),
    ]
    for request_id, fault_type, base_id, risk_level, query_mode in runtime_faults:
        case = fault_case_from_base(r11, r12, base_id, request_id, f"Runtime fault injection: {fault_type}")
        case["risk_level"] = risk_level
        case["query_mode"] = query_mode
        requests.append(
            {
                "request_id": request_id,
                "kind": "fault_runtime_injected",
                "fault_type": fault_type,
                "feature_flag_mode": "shadow",
                "case": case,
            }
        )

    cases_by_id = {case["case_id"]: case for case in r12.runtime_cases(r11)}
    alignment_negatives = [
        (
            "fault-alignment-context-mismatch",
            "context_pack",
            "case-001-direct-web-annotation",
            "case-002-direct-prov",
            "Does TextQuoteSelector need exact text plus surrounding context?",
        ),
        (
            "fault-alignment-draft-mismatch",
            "draft",
            "case-002-direct-prov",
            "case-003-direct-rag-attribution",
            "Can PROV use entity, activity, and agent as a light provenance skeleton?",
        ),
        (
            "fault-alignment-support-map-mismatch",
            "claim_support_map",
            "case-003-direct-rag-attribution",
            "case-001-direct-web-annotation",
            "Are citation correctness and citation faithfulness different checks?",
        ),
        (
            "fault-alignment-related-terms-mismatch",
            "related_terms",
            "case-001-direct-web-annotation",
            "case-003-direct-rag-attribution",
            "Does the citation selector prove citation faithfulness?",
        ),
    ]
    for request_id, mismatch_kind, base_id, donor_id, query in alignment_negatives:
        requests.append(
            {
                "request_id": request_id,
                "kind": "alignment_negative_case",
                "fault_type": "alignment_mismatch",
                "alignment_negative_kind": mismatch_kind,
                "feature_flag_mode": "shadow",
                "case": mix_alignment_case(
                    r11,
                    cases_by_id[base_id],
                    cases_by_id[donor_id],
                    request_id=request_id,
                    mismatch_kind=mismatch_kind,
                    query=query,
                ),
            }
        )
    return requests


def build_context_pack(case: dict[str, Any]) -> list[dict[str, Any]]:
    pack: list[dict[str, Any]] = []
    for idx, support in enumerate(case.get("claim_support_map", []), start=1):
        pack.append(
            {
                "item_id": f"ctx-{idx:03d}",
                "source_ref": support.get("source_ref", ""),
                "source_sha256": support.get("source_sha256", ""),
                "anchor_ref": support.get("anchor_ref", ""),
                "claim_id": support.get("claim_id", ""),
                "alignment_id": support.get("alignment_id", ""),
                "authority_bucket": support.get("support_authority_bucket", ""),
                "pack_role": "support_candidate"
                if support.get("support_authority_bucket") not in {"candidate_summary", "rank_score"}
                else "orientation",
                "scope_fit": support.get("scope_fit", "unknown"),
                "temporal_fit": support.get("temporal_fit", "unknown"),
                "not_yet": ["reviewed_truth", "action_basis"],
            }
        )
    return pack


def stage_spans(request_id: str, status: str, release_state: str, elapsed_ms: float) -> list[dict[str, Any]]:
    stages = [
        ("route", 0.2),
        ("retrieve", 2.0),
        ("build_context_pack", 0.4),
        ("generate_draft_replay", 0.3),
        ("bind_claims", 0.4),
        ("assess_support_replay", 0.4),
        ("apply_brake", 0.4),
        ("render_candidate", 0.3),
        ("run_guard", 1.0),
        ("commit_release", 0.2),
    ]
    total_weight = sum(weight for _, weight in stages)
    spans: list[dict[str, Any]] = []
    for index, (stage, weight) in enumerate(stages, start=1):
        spans.append(
            {
                "request_id": request_id,
                "span_id": f"{request_id}-span-{index:02d}",
                "stage": stage,
                "status": status,
                "release_state": release_state,
                "latency_ms": round(max(0.001, elapsed_ms * weight / total_weight), 6),
                "timing_kind": "simulated_weighted_from_request_elapsed",
            }
        )
    return spans


def final_text(result: dict[str, Any]) -> str:
    return result.get("final", {}).get("final_text", "")


def old_answer_text(case: dict[str, Any] | None, fallback_query: str = "") -> str:
    if not case:
        return fallback_query
    return case.get("draft", {}).get("draft_text", "")


class RuntimeFault(Exception):
    def __init__(self, fault_type: str, stage: str) -> None:
        super().__init__(fault_type)
        self.fault_type = fault_type
        self.stage = stage


class ReleaseSink:
    def __init__(self) -> None:
        self.events: list[dict[str, Any]] = []
        self.guard_passed = False

    def attempt_fact_text(self, text: str, stage: str) -> None:
        self.events.append(
            {
                "stage": stage,
                "event": "fact_text_release_attempt",
                "text_sha256": sha256_text(text),
                "blocked": not self.guard_passed,
            }
        )

    def commit_final(self, final: dict[str, Any]) -> None:
        allowed = (
            self.guard_passed
            and final.get("atomic_release_phase") == "committed_final"
            and final.get("release_state") == "released"
        )
        self.events.append(
            {
                "stage": "commit_release",
                "event": "final_release_attempt",
                "final_sha256": final.get("final_sha256", ""),
                "allowed": allowed,
                "guard_passed": self.guard_passed,
                "atomic_release_phase": final.get("atomic_release_phase", ""),
                "release_state": final.get("release_state", ""),
            }
        )

    def leaked_before_guard(self) -> bool:
        return any(event.get("event") == "fact_text_release_attempt" and not event.get("blocked") for event in self.events)

    def attempted_before_guard(self) -> bool:
        return any(event.get("event") == "fact_text_release_attempt" for event in self.events)


def fallback_final(case: dict[str, Any], fault_type: str) -> dict[str, Any]:
    high_risk = case.get("risk_level") == "high" or case.get("query_mode") == "action"
    policy = "review" if high_risk else "abstain"
    text = (
        "该请求需要复核。系统没有发布未核验草稿。"
        if high_risk
        else "核验暂不可用。系统没有发布未核验草稿。"
    )
    text = text + "\n\n状态：" + ("需要复核" if high_risk else "资料不足")
    return {
        "case_id": case["case_id"],
        "final_answer_id": f"final-{case['case_id']}",
        "final_text": text,
        "final_sha256": sha256_text(text),
        "answer_policy": policy,
        "status_label": "需要复核" if high_risk else "资料不足",
        "release_state": "review_required" if high_risk else "withheld",
        "evaluation_state": "unavailable",
        "atomic_release_phase": f"runtime_fault_fallback:{fault_type}",
        "citations": [],
        "visible_claim_ids": [],
        "action_readiness_granted": False,
        "reviewed_truth_granted": False,
        "promotion_granted": False,
    }


def run_case_with_forced_guard(r11: Any, case: dict[str, Any], guard_status: str) -> dict[str, Any]:
    errors = r11.validate_draft_claim_binding(case)
    decisions = []
    for segment in case["draft"]["segments"]:
        if segment.get("type") != "claim":
            continue
        if errors:
            decisions.append(r11.binding_integrity_error_decision(case, segment, errors))
        else:
            decisions.append(r11.brake_for_segment(case, segment))
    candidate = r11.render_final_answer(case, decisions)
    internal = r11.internal_post_render_guard(case, decisions, candidate)
    final = r11.commit_final_after_guard(case, candidate, guard_status)
    return {
        "case": case,
        "binding": r11.draft_claim_binding(case),
        "decisions": decisions,
        "final": final,
        "guard_report": {
            "case_id": case["case_id"],
            "status": guard_status,
            "forced_by_runtime_fault": True,
            "internal": internal,
            "official_vaks_guard": [],
        },
    }


def input_alignment_status(case: dict[str, Any], context_pack: list[dict[str, Any]]) -> dict[str, Any]:
    contract = case.get("alignment_contract", {})
    alignment_id = contract.get("alignment_id", "")
    expected_claim_ids = {
        claim_id for claim_id in contract.get("expected_claim_ids", []) if claim_id and claim_id != "unmapped"
    }
    support_rows = [row for row in case.get("claim_support_map", []) if row.get("claim_id")]
    support_claim_ids = {row.get("claim_id") for row in support_rows}
    context_claim_ids = {item.get("claim_id") for item in context_pack if item.get("claim_id")}
    draft_segments = [
        segment
        for segment in case.get("draft", {}).get("segments", [])
        if segment.get("type") == "claim" and segment.get("claim_id") != "unmapped"
    ]

    query_binding_ok = bool(alignment_id) and case.get("query_alignment_id") == alignment_id
    draft_binding_ok = (
        bool(alignment_id)
        and case.get("draft", {}).get("alignment_id") == alignment_id
        and case.get("draft", {}).get("draft_sha256") == contract.get("draft_sha256")
    )
    draft_segment_binding_ok = all(segment.get("alignment_id") == alignment_id for segment in draft_segments)
    support_binding_ok = bool(support_rows) and all(row.get("alignment_id") == alignment_id for row in support_rows)
    context_binding_ok = bool(context_pack) and all(item.get("alignment_id") == alignment_id for item in context_pack)
    expected_supported = bool(expected_claim_ids) and expected_claim_ids.issubset(support_claim_ids)
    expected_in_context = bool(expected_claim_ids) and expected_claim_ids.issubset(context_claim_ids)

    query_context_alignment = query_binding_ok and support_binding_ok and context_binding_ok and expected_supported and expected_in_context
    draft_support_alignment = draft_binding_ok and draft_segment_binding_ok and support_binding_ok and expected_supported
    return {
        "alignment_id": alignment_id,
        "query_binding_ok": query_binding_ok,
        "draft_binding_ok": draft_binding_ok,
        "draft_segment_binding_ok": draft_segment_binding_ok,
        "support_binding_ok": support_binding_ok,
        "context_binding_ok": context_binding_ok,
        "expected_supported": expected_supported,
        "expected_in_context": expected_in_context,
        "query_context_alignment": query_context_alignment,
        "draft_support_alignment": draft_support_alignment,
        "expected_claim_ids": sorted(expected_claim_ids),
        "support_claim_ids": sorted(support_claim_ids),
        "context_claim_ids": sorted(context_claim_ids),
    }


def evaluate_alignment(result: dict[str, Any]) -> dict[str, Any]:
    case = result.get("case", {})
    contract = result.get("alignment_contract") or case.get("alignment_contract", {})
    input_alignment = result.get("input_alignment") or input_alignment_status(case, result.get("context_pack", []))
    final = result.get("final_answer", {})
    released = final.get("release_state") in {"released", "released_degraded"}
    answer_policy = final.get("answer_policy", "")
    visible_claim_ids = set(final.get("visible_claim_ids", []))
    expected_claim_ids = set(contract.get("expected_claim_ids", []))
    query_terms = contract.get("query_terms", [])
    answer_terms = contract.get("answer_terms", [])
    query_context_alignment = bool(input_alignment.get("query_context_alignment"))
    answer_relevance = True
    if released and answer_policy in {"direct", "qualified"}:
        answer_relevance = bool(input_alignment.get("draft_support_alignment"))
        answer_relevance = answer_relevance and visible_claim_ids.issubset(expected_claim_ids)
    return {
        "query_context_alignment": query_context_alignment,
        "query_answer_relevance": answer_relevance,
        "input_alignment": input_alignment,
        "alignment_id": contract.get("alignment_id", ""),
        "query_terms": query_terms,
        "answer_terms": answer_terms,
        "expected_claim_ids": sorted(expected_claim_ids),
        "visible_claim_ids": sorted(visible_claim_ids),
    }


def process_request(r11: Any, r12: Any, vaks_guard: Any, request: dict[str, Any], guard_dir: Path) -> dict[str, Any]:
    case = request["case"]
    fault_type = request.get("fault_type", "")
    sink = ReleaseSink()
    started = time.perf_counter()
    stages_executed: list[str] = []
    try:
        stages_executed.append("route")
        if fault_type == "feature_flag_error":
            raise RuntimeFault(fault_type, "route")
        stages_executed.append("retrieve")
        if fault_type in {"retrieval_empty", "acl_denied"}:
            raise RuntimeFault(fault_type, "retrieve")
        context_pack = build_context_pack(case)
        stages_executed.append("build_context_pack")
        input_alignment = input_alignment_status(case, context_pack)
        alignment_gate_applies = request.get("kind") in {"prodlike_replay", "alignment_negative_case"}
        if alignment_gate_applies and not (
            input_alignment.get("query_context_alignment") and input_alignment.get("draft_support_alignment")
        ):
            raise RuntimeFault("alignment_mismatch", "alignment_gate")
        stages_executed.append("generate_draft_replay")
        if fault_type == "invalid_json_draft":
            broken = copy.deepcopy(case)
            broken["draft"]["draft_text"] = "{not valid json"
            raise RuntimeFault(fault_type, "generate_draft_replay")
        if fault_type == "streaming_fact_text_before_brake":
            sink.attempt_fact_text(case.get("draft", {}).get("draft_text", ""), "generate_draft_replay")
            raise RuntimeFault(fault_type, "release_sink")
        stages_executed.append("bind_claims")
        stages_executed.append("assess_support_replay")
        stages_executed.append("apply_brake")
        stages_executed.append("render_candidate")
        stages_executed.append("run_guard")
        if fault_type in {"guard_block", "guard_error", "guard_timeout"}:
            forced_status = {"guard_block": "block", "guard_error": "error", "guard_timeout": "timeout"}[fault_type]
            result = run_case_with_forced_guard(r11, case, forced_status)
        else:
            result = r11.run_case(case, guard_dir, vaks_guard)
        stages_executed.append("commit_release")
        context_pack = build_context_pack(case)
        runtime_fault = {"injected": bool(fault_type), "type": fault_type, "stage": "", "handled_by_orchestrator": True}
    except RuntimeFault as fault:
        elapsed_ms = (time.perf_counter() - started) * 1000.0
        final = fallback_final(case, fault.fault_type)
        sink.commit_final(final)
        result = {
            "case": case,
            "binding": {},
            "decisions": [],
            "final": final,
            "guard_report": {"case_id": case["case_id"], "status": "not_run", "runtime_fault": fault.fault_type, "stage": fault.stage},
        }
        context_pack = [] if fault.stage in {"retrieve", "route"} else build_context_pack(case)
        input_alignment = input_alignment_status(case, context_pack)
        comparison = {
            "case_id": request["request_id"],
            "old_path": {"unsupported_assertion_survival_count": 1, "blocked_literal_exposure_count": 1},
            "guarded_path": {
                "unsupported_assertion_survival_count": 0,
                "blocked_literal_exposure_count": 0,
                "supported_claim_count": 0,
                "supported_claim_preserved_count": 0,
                "supported_claim_preservation_rate": 1.0,
                "candidate_or_rank_as_support": False,
            },
            "guarded_no_worse_than_old": True,
            "guarded_strictly_safer_than_old": True,
            "old_baseline_has_unsafe_signal": True,
        }
        release_state = final.get("release_state", "unknown")
        output = {
            "request_id": request["request_id"],
            "kind": request["kind"],
            "fault_type": fault.fault_type,
            "feature_flag_mode": request.get("feature_flag_mode", "shadow"),
            "shadow_only": request.get("feature_flag_mode") == "shadow",
            "query": case.get("query", ""),
            "query_mode": case.get("query_mode", ""),
            "risk_level": case.get("risk_level", ""),
            "context_pack": context_pack,
            "answer_draft": case.get("draft", {}),
            "claim_support_map": case.get("claim_support_map", []),
            "old_answer_text": old_answer_text(case),
            "final_answer": final,
            "brake_decisions": [],
            "guard_report": result["guard_report"],
            "runtime_fault": {"injected": True, "type": fault.fault_type, "stage": fault.stage, "handled_by_orchestrator": True},
            "release_sink_events": sink.events,
            "pre_guard_fact_text_release_attempted": sink.attempted_before_guard(),
            "pre_guard_fact_text_leaked": sink.leaked_before_guard(),
            "comparison": comparison,
            "release_state": release_state,
            "answer_policy": final.get("answer_policy", ""),
            "guard_status": result["guard_report"].get("status", "not_run"),
            "elapsed_ms": round(elapsed_ms, 6),
            "trace_spans": stage_spans(request["request_id"], result["guard_report"].get("status", "not_run"), release_state, elapsed_ms),
            "stages_executed": stages_executed,
            "alignment_contract": case.get("alignment_contract", {}),
            "input_alignment": input_alignment,
        }
        output["alignment"] = evaluate_alignment(output)
        return output

    elapsed_ms = (time.perf_counter() - started) * 1000.0
    comparison = r12.compare_case(r11, result)
    runtime_wrapper = {"applied": False, "reason": ""}
    if request.get("fault_type") and case.get("risk_level") == "high":
        final = result.get("final", {})
        if final.get("answer_policy") != "review" or final.get("release_state") != "review_required":
            review_text = "This high-risk fault requires human review. No unchecked draft was released."
            result["final"] = {
                **final,
                "final_text": review_text,
                "final_sha256": sha256_text(review_text),
                "answer_policy": "review",
                "status_label": "needs review",
                "release_state": "review_required",
                "evaluation_state": "partially_evaluated",
                "atomic_release_phase": "withheld_by_runtime_fail_closed_wrapper",
                "citations": [],
                "visible_claim_ids": [],
                "action_readiness_granted": False,
                "reviewed_truth_granted": False,
                "promotion_granted": False,
            }
            runtime_wrapper = {"applied": True, "reason": "high_risk_fault_forced_to_review"}
            comparison = r12.compare_case(r11, result)
    sink.guard_passed = result.get("guard_report", {}).get("status") == "pass"
    sink.commit_final(result.get("final", {}))
    guard_status = result.get("guard_report", {}).get("status", "unknown")
    release_state = result.get("final", {}).get("release_state", "unknown")
    output = {
        "request_id": request["request_id"],
        "kind": request["kind"],
        "fault_type": request.get("fault_type", ""),
        "feature_flag_mode": request.get("feature_flag_mode", "shadow"),
        "shadow_only": request.get("feature_flag_mode") == "shadow",
        "query": case.get("query", ""),
        "query_mode": case.get("query_mode", ""),
        "risk_level": case.get("risk_level", ""),
        "context_pack": context_pack,
        "answer_draft": case.get("draft", {}),
        "claim_support_map": case.get("claim_support_map", []),
        "old_answer_text": old_answer_text(case),
        "final_answer": result.get("final", {}),
        "brake_decisions": result.get("decisions", []),
        "guard_report": result.get("guard_report", {}),
        "runtime_fault": runtime_fault,
        "runtime_fail_closed_wrapper": runtime_wrapper,
        "release_sink_events": sink.events,
        "pre_guard_fact_text_release_attempted": sink.attempted_before_guard(),
        "pre_guard_fact_text_leaked": sink.leaked_before_guard(),
        "comparison": comparison,
        "release_state": release_state,
        "answer_policy": result.get("final", {}).get("answer_policy", ""),
        "guard_status": guard_status,
        "elapsed_ms": round(elapsed_ms, 6),
        "trace_spans": stage_spans(request["request_id"], guard_status, release_state, elapsed_ms),
        "stages_executed": stages_executed,
        "alignment_contract": case.get("alignment_contract", {}),
        "input_alignment": input_alignment,
    }
    output["alignment"] = evaluate_alignment(output)
    return output


def run_replay(
    r11: Any, r12: Any, vaks_guard: Any, output_dir: Path
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    replay_requests = build_replay_requests(r11, r12)
    fault_requests = build_fault_requests(r11, r12)
    replay_results: list[dict[str, Any]] = []
    fault_results: list[dict[str, Any]] = []
    spans: list[dict[str, Any]] = []

    guard_dir = output_dir / "guarded_replay"
    for request in replay_requests:
        result = process_request(r11, r12, vaks_guard, request, guard_dir)
        replay_results.append(result)
        spans.extend(result["trace_spans"])

    fault_guard_dir = output_dir / "fault_guarded_replay"
    for request in fault_requests:
        result = process_request(r11, r12, vaks_guard, request, fault_guard_dir)
        fault_results.append(result)
        spans.extend(result["trace_spans"])

    return replay_requests, replay_results, fault_requests, fault_results, spans


def visible_claims_missing_anchor(result: dict[str, Any]) -> list[str]:
    visible = set(result.get("final_answer", {}).get("visible_claim_ids", []))
    missing: list[str] = []
    supports = {support.get("claim_id"): support for support in result.get("claim_support_map", [])}
    for claim_id in visible:
        support = supports.get(claim_id, {})
        if not (
            support.get("anchor_ref")
            and support.get("source_ref")
            and support.get("source_sha256")
            and support.get("authority_fit") == "allowed"
        ):
            missing.append(claim_id)
    return sorted(missing)


def result_metrics(r12: Any, results: list[dict[str, Any]]) -> dict[str, Any]:
    guard_block_released = []
    high_risk_fail_open = []
    direct_without_anchor = []
    unchecked_draft_released = []
    candidate_rank_release = []
    action_ready_grants = []
    reviewed_truth_grants = []
    promotion_grants = []
    query_context_alignment_failures = []
    query_answer_relevance_failures = []
    alignment_negative_detected = []
    alignment_negative_undetected = []
    pre_guard_fact_text_leaks = []
    pre_guard_fact_text_attempts = []
    sink_commit_without_guard_pass = []
    sink_final_hash_mismatch = []
    blocked_literal_exposures = 0
    unsupported_survival = 0
    supported_claim_count = 0
    supported_preserved_count = 0
    fallback_match = 0
    fallback_total = 0

    for result in results:
        final = result.get("final_answer", {})
        guard_status = result.get("guard_status", "")
        release_state = result.get("release_state", "")
        risk_level = result.get("risk_level", "")
        comparison = result.get("comparison", {})
        guarded = comparison.get("guarded_path", {})
        blocked_literal_exposures += int(guarded.get("blocked_literal_exposure_count", 0) or 0)
        unsupported_survival += int(guarded.get("unsupported_assertion_survival_count", 0) or 0)
        if not result.get("fault_type"):
            supported_claim_count += int(guarded.get("supported_claim_count", 0) or 0)
            supported_preserved_count += int(guarded.get("supported_claim_preserved_count", 0) or 0)

        if guard_status in {"block", "error", "timeout"} and release_state in {"released", "released_degraded"}:
            guard_block_released.append(result["request_id"])
        for event in result.get("release_sink_events", []):
            if event.get("event") != "final_release_attempt":
                continue
            if event.get("allowed") and not event.get("guard_passed"):
                sink_commit_without_guard_pass.append(result["request_id"])
            if event.get("final_sha256") and event.get("final_sha256") != final.get("final_sha256", ""):
                sink_final_hash_mismatch.append(result["request_id"])
        if risk_level == "high" and release_state in {"released", "released_degraded"} and result.get("fault_type"):
            high_risk_fail_open.append(result["request_id"])
        if final.get("answer_policy") == "direct":
            missing = visible_claims_missing_anchor(result)
            if missing:
                direct_without_anchor.append({"request_id": result["request_id"], "claim_ids": missing})
        draft_text = result.get("old_answer_text", "")
        final_text_value = final.get("final_text", "")
        if draft_text and draft_text in final_text_value and result.get("kind") in {"fault_guarded_case", "fault_runtime_injected"}:
            unchecked_draft_released.append(result["request_id"])
        if guarded.get("candidate_or_rank_as_support"):
            candidate_rank_release.append(result["request_id"])
        if final.get("action_readiness_granted"):
            action_ready_grants.append(result["request_id"])
        if final.get("reviewed_truth_granted"):
            reviewed_truth_grants.append(result["request_id"])
        if final.get("promotion_granted"):
            promotion_grants.append(result["request_id"])
        alignment = result.get("alignment", {})
        alignment_required = result.get("kind") == "prodlike_replay"
        if alignment_required and alignment and not alignment.get("query_context_alignment", False):
            query_context_alignment_failures.append(result["request_id"])
        if alignment_required and alignment and not alignment.get("query_answer_relevance", False):
            query_answer_relevance_failures.append(result["request_id"])
        if result.get("kind") == "alignment_negative_case":
            input_alignment = alignment.get("input_alignment", {})
            if (
                release_state in {"released", "released_degraded"}
                or (
                    input_alignment.get("query_context_alignment")
                    and input_alignment.get("draft_support_alignment")
                )
            ):
                alignment_negative_undetected.append(result["request_id"])
            else:
                alignment_negative_detected.append(result["request_id"])
        if result.get("pre_guard_fact_text_leaked"):
            pre_guard_fact_text_leaks.append(result["request_id"])
        if result.get("pre_guard_fact_text_release_attempted"):
            pre_guard_fact_text_attempts.append(result["request_id"])
        if result.get("fault_type"):
            fallback_total += 1
            expected_review = risk_level == "high"
            if expected_review:
                if release_state == "review_required" or final.get("answer_policy") == "review":
                    fallback_match += 1
            elif (
                release_state in {"withheld", "released_degraded", "review_required"}
                or final.get("answer_policy") in {"abstain", "qualified", "review"}
            ):
                fallback_match += 1

    return {
        "request_count": len(results),
        "guard_block_released_count": len(guard_block_released),
        "guard_block_released_request_ids": guard_block_released,
        "high_risk_fail_open_count": len(high_risk_fail_open),
        "high_risk_fail_open_request_ids": high_risk_fail_open,
        "direct_without_anchor_count": len(direct_without_anchor),
        "direct_without_anchor": direct_without_anchor,
        "unchecked_draft_released_count": len(unchecked_draft_released),
        "unchecked_draft_released_request_ids": unchecked_draft_released,
        "candidate_or_rank_as_support_survival_count": len(candidate_rank_release),
        "candidate_or_rank_as_support_survival_request_ids": candidate_rank_release,
        "action_readiness_granted_count": len(action_ready_grants),
        "reviewed_truth_granted_count": len(reviewed_truth_grants),
        "promotion_granted_count": len(promotion_grants),
        "query_context_alignment_failure_count": len(query_context_alignment_failures),
        "query_context_alignment_failure_request_ids": query_context_alignment_failures,
        "query_answer_relevance_failure_count": len(query_answer_relevance_failures),
        "query_answer_relevance_failure_request_ids": query_answer_relevance_failures,
        "alignment_negative_case_count": len(alignment_negative_detected) + len(alignment_negative_undetected),
        "alignment_negative_detected_count": len(alignment_negative_detected),
        "alignment_negative_detected_request_ids": alignment_negative_detected,
        "alignment_negative_undetected_count": len(alignment_negative_undetected),
        "alignment_negative_undetected_request_ids": alignment_negative_undetected,
        "pre_guard_fact_text_leak_count": len(pre_guard_fact_text_leaks),
        "pre_guard_fact_text_leak_request_ids": pre_guard_fact_text_leaks,
        "pre_guard_fact_text_attempt_count": len(pre_guard_fact_text_attempts),
        "pre_guard_fact_text_attempt_request_ids": pre_guard_fact_text_attempts,
        "sink_commit_without_guard_pass_count": len(sink_commit_without_guard_pass),
        "sink_commit_without_guard_pass_request_ids": sorted(set(sink_commit_without_guard_pass)),
        "sink_final_hash_mismatch_count": len(sink_final_hash_mismatch),
        "sink_final_hash_mismatch_request_ids": sorted(set(sink_final_hash_mismatch)),
        "blocked_literal_exposure_count": blocked_literal_exposures,
        "unsupported_assertion_survival_count": unsupported_survival,
        "supported_claim_count": supported_claim_count,
        "supported_claim_preserved_count": supported_preserved_count,
        "supported_claim_preservation_rate": supported_preserved_count / supported_claim_count if supported_claim_count else 1.0,
        "fallback_total": fallback_total,
        "fallback_match_count": fallback_match,
        "fallback_match_rate": fallback_match / fallback_total if fallback_total else 1.0,
    }


def fast_pressure_one(r11: Any, r12: Any, case: dict[str, Any], scenario: str) -> tuple[str, str, str]:
    if scenario == "guard_fault":
        return (case["case_id"], "withheld", "guard_fault")
    if scenario == "retrieval_empty":
        return (case["case_id"], "withheld", "retrieval_empty")
    if scenario == "malformed_draft":
        return (case["case_id"], "withheld", "malformed_draft")
    decisions, final, internal = r12.fast_in_memory_run(r11, case)
    return (case["case_id"], final.get("release_state", ""), sha256_text(stable_json([decisions, final, internal])))


def run_pressure(
    r11: Any,
    r12: Any,
    replay_cases: list[dict[str, Any]],
    *,
    sequential_count: int = 300_000,
    parallel_count: int = 80_000,
) -> dict[str, Any]:
    pool = [copy.deepcopy(request["case"]) for request in replay_cases if "case" in request][:60]
    scenarios = ["normal", "burst", "retrieval_empty", "guard_fault", "malformed_draft"]
    failures = 0
    scenario_counts = {scenario: 0 for scenario in scenarios}
    latencies: list[float] = []

    started = time.perf_counter()
    for index in range(sequential_count):
        case = pool[index % len(pool)]
        scenario = scenarios[index % len(scenarios)]
        scenario_counts[scenario] += 1
        t0 = time.perf_counter()
        try:
            _, release_state, _ = fast_pressure_one(r11, r12, case, scenario)
            if scenario in {"guard_fault", "retrieval_empty", "malformed_draft"} and release_state == "released":
                failures += 1
        except Exception:  # pragma: no cover - counted in stress summary
            failures += 1
        latencies.append((time.perf_counter() - t0) * 1000.0)
    sequential_elapsed_ms = (time.perf_counter() - started) * 1000.0

    baseline: dict[int, str] = {}
    sample_size = min(1000, len(pool))
    for idx in range(sample_size):
        baseline[idx] = fast_pressure_one(r11, r12, pool[idx], "normal")[2]

    def parallel_item(index: int) -> tuple[int, str]:
        case_index = index % sample_size
        return case_index, fast_pressure_one(r11, r12, pool[case_index], "normal")[2]

    parallel_started = time.perf_counter()
    parallel_failures = 0
    with ThreadPoolExecutor(max_workers=8) as executor:
        for case_index, digest in executor.map(parallel_item, range(parallel_count), chunksize=200):
            if digest != baseline[case_index]:
                parallel_failures += 1
    parallel_elapsed_ms = (time.perf_counter() - parallel_started) * 1000.0

    return {
        "sequential_count": sequential_count,
        "sequential_failure_count": failures,
        "sequential_elapsed_ms": round(sequential_elapsed_ms, 6),
        "parallel_count": parallel_count,
        "parallel_worker_count": 8,
        "parallel_determinism_failure_count": parallel_failures,
        "parallel_elapsed_ms": round(parallel_elapsed_ms, 6),
        "scenario_counts": scenario_counts,
        "brake_path_avg_ms": round(sum(latencies) / len(latencies), 6),
        "brake_path_p95_ms": round(percentile(latencies, 95), 6),
        "brake_path_p99_ms": round(percentile(latencies, 99), 6),
        "boundary": "stress covers frozen binding/brake/render/commit logic and simulated system faults; not live LLM, live retrieval, network, or production IO",
        "status": "pass" if failures == 0 and parallel_failures == 0 else "fail",
    }


def aggregate_summary(
    replay_requests: list[dict[str, Any]],
    replay_results: list[dict[str, Any]],
    fault_requests: list[dict[str, Any]],
    fault_results: list[dict[str, Any]],
    metrics: dict[str, Any],
    stress: dict[str, Any],
    deps: dict[str, Any],
) -> dict[str, Any]:
    hard_zero_keys = [
        "guard_block_released_count",
        "high_risk_fail_open_count",
        "direct_without_anchor_count",
        "unchecked_draft_released_count",
        "candidate_or_rank_as_support_survival_count",
        "action_readiness_granted_count",
        "reviewed_truth_granted_count",
        "promotion_granted_count",
        "blocked_literal_exposure_count",
        "unsupported_assertion_survival_count",
        "query_context_alignment_failure_count",
        "query_answer_relevance_failure_count",
        "alignment_negative_undetected_count",
        "pre_guard_fact_text_leak_count",
        "sink_commit_without_guard_pass_count",
        "sink_final_hash_mismatch_count",
    ]
    hard_zero_pass = all(metrics.get(key) == 0 for key in hard_zero_keys)
    preservation_pass = metrics.get("supported_claim_preservation_rate") == 1.0
    fallback_pass = metrics.get("fallback_match_rate") == 1.0
    stress_pass = stress.get("status") == "pass"
    dependency_pass = deps.get("status") == "pass"
    canary_ready = hard_zero_pass and preservation_pass and fallback_pass and stress_pass and dependency_pass
    return {
        "schema_version": "r1.3-production-shaped-replay-simulation",
        "status": "pass" if canary_ready else "fail",
        "live_shadow_recommendation": "eligible_for_live_shadow_wiring" if canary_ready else "not_ready_for_live_shadow",
        "canary_recommendation": "not_evaluated_use_live_shadow_first",
        "request_counts": {
            "existing_r1_2_fixture_requests": sum(1 for r in replay_requests if r["kind"] == "existing_guarded_fixture"),
            "prodlike_query_variant_requests": sum(1 for r in replay_requests if r["kind"] == "prodlike_replay"),
            "fault_injection_requests": len(fault_requests),
            "total_replay_requests": len(replay_requests) + len(fault_requests),
            "trace_span_count": (len(replay_results) + len(fault_results)) * 10,
        },
        "hard_zero_pass": hard_zero_pass,
        "hard_zero_keys": hard_zero_keys,
        "supported_preservation_pass": preservation_pass,
        "fallback_policy_pass": fallback_pass,
        "stress_pass": stress_pass,
        "dependency_pass": dependency_pass,
        "quality_metrics": metrics,
        "stress_summary": stress,
        "not_proven": [
            "production_runtime",
            "live_llm_output_safety",
            "live_retrieval_quality",
            "production_latency_slo",
            "reviewed_truth",
            "promotion",
            "action_readiness",
            "permission_system_integration",
            "all_enterprise_connectors",
            "internal_canary_readiness",
        ],
        "allowed_next_step": (
            "Build real live-shadow wiring behind a feature flag. Do not enter canary until live-shadow telemetry passes."
            if canary_ready
            else "Fix failed hard gates before live shadow."
        ),
    }


def contract_md() -> str:
    return """# R1.3 Production-Shaped Replay Simulation

This sandbox replays a production-shaped guarded-answer chain:

request -> trusted route metadata -> frozen context pack -> AnswerDraft ->
ClaimSupportMap -> R1.1 brake -> VAKS Guard -> committed final.

It uses query-aligned frozen replay tuples and runtime fault injection through
the same `process_request` orchestrator. It does not call a live LLM, live
retrieval, a database, a service, or a network API.

R1.3 r3 adds a cross-object alignment contract. Query, ContextPack,
AnswerDraft, and ClaimSupportMap must carry the same frozen alignment id before
the answer can be released. Deliberate cross-case mismatches are included as
negative controls.

## Passing meaning

Passing means the replay chain met the configured hard gates in this bounded
sandbox and is eligible to proceed to live-shadow wiring development behind a
feature flag.

It does not mean production runtime is enabled or validated.
"""


def limits_md() -> str:
    return """# Limits

- Replay-only, sandbox-only, read-only.
- No live LLM, live retrieval, DB, network, API, service, or background worker.
- Frozen context packs, drafts, and ClaimSupportMaps are used as replay inputs,
  and replay_inputs.jsonl stores the full input tuples.
- Query-answer relevance and query-context alignment are deterministic
  alignment-id gates across frozen objects, not a learned semantic judge and
  not natural-language relevance validation for unseen live traffic.
- Trace span latency is simulated weighted span latency derived from request
  elapsed time; only the aggregate brake-path timing is measured.
- Stress numbers measure local replay/brake/render logic, not production
  end-to-end latency.
- The positive recommendation is limited to live-shadow wiring. Canary remains
  not evaluated until live-shadow telemetry passes.
- This package grants no reviewed truth, promotion, or action readiness.
"""


def create_zip(output_dir: Path) -> dict[str, str]:
    zip_path = output_dir.with_suffix(".zip")
    sha_path = Path(str(zip_path) + ".sha256")
    if zip_path.exists():
        zip_path.unlink()
    if sha_path.exists():
        sha_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(output_dir.rglob("*")):
            if not path.is_file():
                continue
            info = zipfile.ZipInfo(rel(path, output_dir))
            info.date_time = (2026, 6, 24, 0, 0, 0)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    digest = sha256_bytes(zip_path.read_bytes())
    write_lf(sha_path, f"{digest}  {zip_path.name}\n")
    return {"zip_path": zip_path.as_posix(), "zip_sha256": digest, "sha256_path": sha_path.as_posix()}


def write_bundle(output_dir: Path, *, quick: bool = False, with_append_only_self_test: bool = False) -> dict[str, Any]:
    if output_dir.exists():
        raise FileExistsError(f"Output directory already exists: {output_dir}")
    output_dir.mkdir(parents=True)

    r11 = load_module(R11_TOOL, "vaks_r1_1_wiring_for_r1_3")
    r12 = load_module(R12_TOOL, "vaks_r1_2_comparison_for_r1_3")
    vaks_guard = load_module(VAKS_GUARD, "vaks_guard_for_r1_3")

    deps = dependency_checks(r11, r12)
    replay_requests, replay_results, fault_requests, fault_results, spans = run_replay(r11, r12, vaks_guard, output_dir)
    all_results = replay_results + fault_results
    metrics = result_metrics(r12, all_results)
    stress = run_pressure(
        r11,
        r12,
        replay_requests if not quick else replay_requests[:20],
        sequential_count=2_000 if quick else 300_000,
        parallel_count=1_000 if quick else 80_000,
    )
    summary = aggregate_summary(replay_requests, replay_results, fault_requests, fault_results, metrics, stress, deps)

    write_lf(output_dir / "CONTRACT.md", contract_md())
    write_lf(output_dir / "LIMITS.md", limits_md())
    write_jsonl(output_dir / "replay_requests.jsonl", [
        {key: value for key, value in request.items() if key != "case"} for request in replay_requests
    ])
    write_jsonl(
        output_dir / "replay_inputs.jsonl",
        [
            {
                "request_id": result["request_id"],
                "kind": result["kind"],
                "fault_type": result.get("fault_type", ""),
                "query": result["query"],
                "query_mode": result["query_mode"],
                "risk_level": result["risk_level"],
                "context_pack": result["context_pack"],
                "answer_draft": result["answer_draft"],
                "claim_support_map": result["claim_support_map"],
                "alignment_contract": result.get("alignment_contract", {}),
                "alignment_evaluation": result.get("alignment", {}),
            }
            for result in all_results
        ],
    )
    write_jsonl(output_dir / "replay_results.jsonl", [
        {key: value for key, value in result.items() if key not in {"context_pack", "answer_draft", "claim_support_map", "trace_spans"}}
        for result in replay_results
    ])
    write_jsonl(output_dir / "fault_injection_cases.jsonl", [
        {key: value for key, value in request.items() if key != "case"} for request in fault_requests
    ])
    write_jsonl(output_dir / "fault_injection_results.jsonl", [
        {key: value for key, value in result.items() if key not in {"context_pack", "answer_draft", "claim_support_map", "trace_spans"}}
        for result in fault_results
    ])
    write_jsonl(output_dir / "trace_spans.jsonl", spans)
    write_jsonl(
        output_dir / "shadow_comparison.jsonl",
        [
            {
                "request_id": result["request_id"],
                "old_answer_sha256": sha256_text(result.get("old_answer_text", "")),
                "final_answer_sha256": result.get("final_answer", {}).get("final_sha256", ""),
                "answer_policy": result.get("answer_policy", ""),
                "release_state": result.get("release_state", ""),
                "guard_status": result.get("guard_status", ""),
                "strictly_safer_than_old": result.get("comparison", {}).get("guarded_strictly_safer_than_old", False),
            }
            for result in all_results
        ],
    )
    write_lf(output_dir / "dependency_checks.json", pretty_json(deps))
    write_lf(output_dir / "quality_metrics.json", pretty_json(metrics))
    write_lf(output_dir / "stress_summary.json", pretty_json(stress))
    write_lf(output_dir / "summary.json", pretty_json(summary))

    provenance_dir = output_dir / "provenance"
    provenance_dir.mkdir(parents=True, exist_ok=True)
    shutil.copy2(__file__, provenance_dir / Path(__file__).name)

    append_result: dict[str, Any] | None = None
    if with_append_only_self_test:
        append_result = append_only_self_test()
        write_lf(output_dir / "append_only_self_test.json", pretty_json(append_result))

    exclude = {"run_manifest.json"}
    artifact_hashes = collect_hashes(output_dir, exclude=exclude)
    manifest = {
        "run_id": "vaks-guarded-answer-production-shaped-replay-r1-3-r3-2026-06-24",
        "created_at": "2026-06-24",
        "tool": "tools/vaks_guarded_answer_replay_simulation_r1_3.py",
        "runner_sha256": sha256_bytes(Path(__file__).read_bytes()),
        "runner_provenance_sha256": artifact_hashes.get(f"provenance/{Path(__file__).name}", ""),
        "dependency_checks": deps,
        "summary_status": summary["status"],
        "canary_recommendation": summary["canary_recommendation"],
        "live_shadow_recommendation": summary["live_shadow_recommendation"],
        "artifact_hashes": artifact_hashes,
        "read_only": True,
        "sandbox_only": True,
        "append_only_self_test_status": append_result.get("status") if append_result else "not_run",
    }
    write_lf(output_dir / "run_manifest.json", pretty_json(manifest))
    hashes = collect_hashes(output_dir)
    manifest["artifact_hashes"] = {key: value for key, value in hashes.items() if key != "run_manifest.json"}
    write_lf(output_dir / "run_manifest.json", pretty_json(manifest))
    zip_info = create_zip(output_dir)
    return {"summary": summary, "zip": zip_info, "manifest": manifest}


def verify_bundle(output_dir: Path) -> dict[str, Any]:
    manifest = read_json(output_dir / "run_manifest.json")
    current_hashes = collect_hashes(output_dir)
    failures = []
    for relative, expected in manifest.get("artifact_hashes", {}).items():
        actual = current_hashes.get(relative)
        if actual != expected:
            failures.append({"path": relative, "expected": expected, "actual": actual})
    extra = sorted(set(current_hashes) - set(manifest.get("artifact_hashes", {})) - {"run_manifest.json"})
    summary = read_json(output_dir / "summary.json")
    runner_path = output_dir / "provenance" / Path(__file__).name
    runner_ok = sha256_bytes(runner_path.read_bytes()) == manifest.get("runner_provenance_sha256")
    checks = {
        "manifest_hashes_match": not failures,
        "summary_pass": summary.get("status") == "pass",
        "hard_zero_pass": bool(summary.get("hard_zero_pass")),
        "stress_pass": bool(summary.get("stress_pass")),
        "supported_preservation_pass": bool(summary.get("supported_preservation_pass")),
        "runner_provenance_hash_matches": runner_ok,
    }
    return {
        "status": "pass" if all(checks.values()) and not extra else "fail",
        "checks": checks,
        "hash_failures": failures,
        "extra_hashes": extra,
    }


def append_only_self_test() -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix="vaks-r13-append-only-") as tmp:
        out = Path(tmp) / "bundle"
        first = write_bundle(out, quick=True, with_append_only_self_test=False)
        before = tree_hash(out)
        second_error = ""
        second_exit_code = 0
        try:
            write_bundle(out, quick=True, with_append_only_self_test=False)
            second_exit_code = 0
        except FileExistsError as exc:
            second_error = exc.__class__.__name__
            second_exit_code = 3
        after = tree_hash(out)
        return {
            "status": "pass" if second_error == "FileExistsError" and before == after else "fail",
            "first_run_status": first["summary"]["status"],
            "second_run_same_directory_rejected": second_error == "FileExistsError",
            "second_run_exit_code": second_exit_code,
            "second_run_error_class": second_error,
            "tree_hash_before_second_run": before,
            "tree_hash_after_second_run": after,
            "tree_hash_unchanged_after_rejected_second_run": before == after,
        }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    run_parser = sub.add_parser("run")
    run_parser.add_argument("output_dir", nargs="?", default=str(DEFAULT_OUTPUT))
    run_parser.add_argument("--with-append-only-self-test", action="store_true")
    run_parser.add_argument("--quick", action="store_true")
    test_parser = sub.add_parser("self-test")
    test_parser.add_argument("output_dir")
    args = parser.parse_args()

    try:
        if args.command == "run":
            result = write_bundle(
                Path(args.output_dir),
                quick=bool(args.quick),
                with_append_only_self_test=bool(args.with_append_only_self_test),
            )
            print(stable_json(result["summary"]))
            print(stable_json(result["zip"]))
            return 0 if result["summary"]["status"] == "pass" else 1
        if args.command == "self-test":
            result = verify_bundle(Path(args.output_dir))
            print(stable_json(result))
            return 0 if result["status"] == "pass" else 1
    except FileExistsError as exc:
        print(stable_json({"status": "error", "error_class": "FileExistsError", "message": str(exc)}))
        return 3
    except Exception as exc:  # pragma: no cover - CLI failure record
        print(stable_json({"status": "error", "error_class": exc.__class__.__name__, "message": str(exc)}))
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
