#!/usr/bin/env python3
"""VAKS Guarded Answer Runtime Comparison R1.2.

Sandbox-only comparative pressure test for the R1.1 guarded answer wiring.

It compares three answer paths over structured local cases:

- old_path: releases the draft text directly;
- disclaimer_path: prepends an unverified warning but still releases the draft;
- guarded_path: uses R1.1 draft binding, brake decisions, safe rendering,
  VAKS Guard checks, and atomic commit.

This tool does not call an LLM, run live retrieval, expose a service, write
truth/review/action state, or modify Obsidian/wiki content.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import random
import shutil
import sys
import tempfile
import time
import zipfile
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

RUN_ID = "vaks-guarded-answer-runtime-comparison-r1-2-2026-06-23"
CONTRACT_VERSION = "r1.2"
DEFAULT_OUTPUT_DIR = Path("outputs/review") / RUN_ID
R1_1_RUNNER = Path("tools/vaks_guarded_answer_wiring.py")
R1_1_DIR = Path("outputs/review/vaks-guarded-answer-wiring-r1-1-2026-06-23")
R1_1_ZIP = Path("outputs/review/vaks-guarded-answer-wiring-r1-1-2026-06-23.zip")
R1_1_SHA = Path("outputs/review/vaks-guarded-answer-wiring-r1-1-2026-06-23.zip.sha256")

STRESS_COUNT = 200_000
PARALLEL_COUNT = 50_000

NOT_PROVEN = [
    "production_runtime_ready",
    "live_llm_generation_validated",
    "live_retrieval_validated",
    "vector_graph_hybrid_retrieval_validated",
    "reviewed_truth",
    "action_readiness",
    "production_latency_slo",
    "real_user_experience_validated",
]


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def pretty_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, indent=2) + "\n"


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.replace("\r\n", "\n"), encoding="utf-8", newline="\n")


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    write_lf(path, "".join(stable_json(row) + "\n" for row in rows))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"cannot_load_module:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def verify_zip(zip_path: Path, sha_path: Path) -> dict[str, Any]:
    if not zip_path.exists() or not sha_path.exists():
        return {"status": "fail", "reason": "missing_zip_or_sha"}
    actual = sha256_bytes(zip_path.read_bytes())
    declared = sha_path.read_text(encoding="utf-8").strip().split()[0].lower()
    with zipfile.ZipFile(zip_path) as archive:
        names = archive.namelist()
        bad = archive.testzip()
    return {
        "status": "pass" if actual == declared and bad is None and len(names) == len(set(names)) else "fail",
        "actual_sha256": actual,
        "declared_sha256": declared,
        "entry_count": len(names),
        "duplicate_path_count": len(names) - len(set(names)),
        "bad_entry": bad,
    }


def collect_hashes(root: Path, *, exclude: set[str] | None = None) -> dict[str, str]:
    exclude = exclude or set()
    result: dict[str, str] = {}
    for path in sorted(root.rglob("*")):
        if path.is_file():
            rel = path.relative_to(root).as_posix()
            if rel not in exclude:
                result[rel] = sha256_bytes(path.read_bytes())
    return result


def tree_hash(root: Path) -> str:
    return sha256_text(stable_json(collect_hashes(root)))


def percentile(values: list[float], q: float) -> float:
    if not values:
        return 0.0
    values = sorted(values)
    idx = min(len(values) - 1, int(round((len(values) - 1) * q)))
    return values[idx]


def make_draft(r11: Any, case_id: str, query: str, segments: list[dict[str, Any]]) -> dict[str, Any]:
    text = "".join(segment["text"] for segment in segments)
    return {
        "draft_id": f"draft-{case_id}",
        "query": query,
        "draft_text": text,
        "draft_sha256": r11.sha256_text(text),
        "segments": segments,
        "immutable": True,
    }


def claim_segment(claim_id: str, text: str) -> dict[str, Any]:
    return {"type": "claim", "claim_id": claim_id, "text": text}


def transition(text: str) -> dict[str, Any]:
    return {"type": "transition", "text": text}


def clone_support(r11: Any, support: dict[str, Any], claim_id: str) -> dict[str, Any]:
    cloned = json.loads(json.dumps(support, ensure_ascii=False))
    cloned["claim_id"] = claim_id
    cloned["claim_hash"] = r11.sha256_text(cloned["text"])
    if isinstance(cloned.get("allowed_expression"), dict) and cloned["allowed_expression"].get("text"):
        cloned["allowed_expression"]["text_hash"] = r11.sha256_text(cloned["allowed_expression"]["text"])
    return cloned


def remap_case(r11: Any, source_case: dict[str, Any], case_id: str, prefix: str) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    segments: list[dict[str, Any]] = []
    supports: list[dict[str, Any]] = []
    support_by_old_id = {item["claim_id"]: item for item in source_case["claim_support_map"]}
    for idx, segment in enumerate(source_case["draft"]["segments"], start=1):
        if segment["type"] == "claim" and segment["claim_id"] in support_by_old_id:
            new_id = f"{prefix}{idx}"
            segments.append(claim_segment(new_id, segment["text"]))
            supports.append(clone_support(r11, support_by_old_id[segment["claim_id"]], new_id))
        elif segment["type"] == "claim":
            new_id = f"{prefix}{idx}"
            segments.append(claim_segment(new_id, segment["text"]))
        else:
            segments.append({"type": segment["type"], "text": segment["text"]})
    return segments, supports


def runtime_cases(r11: Any) -> list[dict[str, Any]]:
    base_cases = json.loads(json.dumps(r11.real_cases(), ensure_ascii=False))
    cases: list[dict[str, Any]] = []
    for case in base_cases:
        copied = json.loads(json.dumps(case, ensure_ascii=False))
        copied["source_slice"] = "r1_1_fixture"
        copied["risk_tags"] = infer_case_risk_tags(copied)
        cases.append(copied)

    by_id = {case["case_id"]: case for case in base_cases}

    def add_composite(case_id: str, query: str, source_ids: list[str], risk: str = "high") -> None:
        segments: list[dict[str, Any]] = []
        supports: list[dict[str, Any]] = []
        for src_index, source_id in enumerate(source_ids, start=1):
            src_segments, src_supports = remap_case(r11, by_id[source_id], case_id, f"c{src_index}_")
            if segments:
                segments.append(transition("另外，"))
            segments.extend(src_segments)
            supports.extend(src_supports)
        cases.append(
            {
                "case_id": case_id,
                "category": "runtime_composite",
                "query": query,
                "risk_level": risk,
                "query_mode": "review" if risk in {"high", "medium"} else "orientation",
                "source_slice": "r1_2_composite",
                "draft": make_draft(r11, case_id, query, segments),
                "claim_support_map": supports,
                "risk_tags": sorted(
                    {
                        tag
                        for source_id in source_ids
                        for tag in infer_case_risk_tags(by_id[source_id])
                    }
                ),
            }
        )

    add_composite("case-034-supported-plus-partial", "一个回答里同时有充分支持和部分支持时会怎样？", ["case-001-direct-web-annotation", "case-005-partial-flexnote"], "medium")
    add_composite("case-035-supported-plus-missing", "一个回答里混入缺失依据结论时会怎样？", ["case-002-direct-prov", "case-009-missing-anchor"], "medium")
    add_composite("case-036-supported-plus-candidate", "候选摘要混进真实回答时会不会被当成依据？", ["case-003-direct-rag-attribution", "case-010-candidate-only"], "medium")
    add_composite("case-037-supported-plus-conflict", "充分支持内容和冲突内容同答时会不会转复核？", ["case-001-direct-web-annotation", "case-013-conflict"], "high")
    add_composite("case-038-supported-plus-stale", "充分支持内容和旧版政策同答时会不会保守？", ["case-002-direct-prov", "case-012-stale-policy"], "high")
    add_composite("case-039-all-supported-multi-claim", "多条 fully supported claim 会不会被误删？", ["case-001-direct-web-annotation", "case-002-direct-prov", "case-003-direct-rag-attribution"], "low")
    add_composite("case-040-partial-no-expression-plus-missing", "无法安全改写的 partial 和 missing 同答时会怎样？", ["case-007-partial-no-expression", "case-009-missing-anchor"], "medium")
    add_composite("case-041-malformed-supported-plus-good", "坏的 supported 记录和好的 supported 记录同答时会不会 fail closed？", ["case-001-direct-web-annotation", "case-025-invalid-source-sha-marked-supported"], "high")
    add_composite("case-042-unmapped-plus-good", "未绑定事实混进有依据回答时会不会拦住？", ["case-001-direct-web-annotation", "case-015-unmapped-factual-span"], "high")
    add_composite("case-043-malicious-safe-message-plus-good", "恶意 safe_message 和好 claim 同答时会不会泄漏？", ["case-001-direct-web-annotation", "case-033-malicious-safe-message-not-trusted"], "medium")
    add_composite("case-044-weak-none-plus-good", "weak coverage none 和好 claim 同答时会不会误发？", ["case-001-direct-web-annotation", "case-032-weak-coverage-none-allowed-expression"], "high")
    add_composite("case-045-binding-mismatch-plus-good", "claim 错绑和好 claim 同答时会不会转复核？", ["case-001-direct-web-annotation", "case-028-draft-claim-text-mismatch"], "high")

    return cases


def infer_case_risk_tags(case: dict[str, Any]) -> list[str]:
    tags: set[str] = set()
    haystack = stable_json(case)
    category = case.get("category", "")
    if "candidate" in category or "候选" in haystack:
        tags.add("candidate_as_support")
    if "rank" in haystack.lower() or "score" in haystack.lower() or "RRF" in haystack or "rerank" in haystack:
        tags.add("rank_as_support")
    if any(term in haystack for term in ["立即导出", "直接执行", "行动依据", "action-ready", "批准执行"]):
        tags.add("action_danger")
    if case.get("risk_level") == "high" and any(item.get("support_result") in {"missing_anchor", "candidate_only", "stale", "conflicting"} for item in case.get("claim_support_map", [])):
        tags.add("high_risk_unsupported_or_conflict")
    return sorted(tags)


def run_guarded_case(r11: Any, vaks_guard: Any, case: dict[str, Any], out_dir: Path) -> dict[str, Any]:
    return r11.run_case(case, out_dir, vaks_guard)


def old_path_answer(case: dict[str, Any]) -> dict[str, Any]:
    text = case["draft"]["draft_text"]
    return {
        "path": "old_path",
        "case_id": case["case_id"],
        "answer_text": text,
        "answer_sha256": sha256_text(text),
        "answer_policy": "direct",
        "release_state": "released",
        "notes": "raw_draft_released_without_brake",
    }


def disclaimer_path_answer(case: dict[str, Any]) -> dict[str, Any]:
    text = "以下内容尚未完成依据核验：\n" + case["draft"]["draft_text"]
    return {
        "path": "disclaimer_path",
        "case_id": case["case_id"],
        "answer_text": text,
        "answer_sha256": sha256_text(text),
        "answer_policy": "qualified",
        "release_state": "released_degraded",
        "notes": "disclaimer_added_but_draft_literals_remain",
    }


def guarded_path_answer(result: dict[str, Any]) -> dict[str, Any]:
    final = result["final"]
    return {
        "path": "guarded_path",
        "case_id": final["case_id"],
        "answer_text": final["final_text"],
        "answer_sha256": final["final_sha256"],
        "answer_policy": final["answer_policy"],
        "release_state": final["release_state"],
        "atomic_release_phase": final["atomic_release_phase"],
        "visible_claim_ids": final["visible_claim_ids"],
    }


def blocked_literals(decisions: list[dict[str, Any]]) -> list[str]:
    return sorted(
        {
            element
            for decision in decisions
            for element in decision.get("blocked_elements", [])
            if isinstance(element, str) and element
        }
    )


def evaluate_text(r11: Any, text: str, decisions: list[dict[str, Any]]) -> dict[str, Any]:
    blocked = blocked_literals(decisions)
    blocked_exposed = [element for element in blocked if element in text]
    unsupported_survival = [
        decision.get("claim_id", "")
        for decision in decisions
        if r11.unsupported_assertion_survived(decision, {"final_text": text})
    ]
    supported_decisions = [decision for decision in decisions if decision.get("reason") == "supported_full_current_matched"]
    supported_preserved = [
        decision.get("claim_id", "")
        for decision in supported_decisions
        if decision.get("safe_text", "") and decision["safe_text"] in text
    ]
    return {
        "blocked_literal_exposure_count": len(blocked_exposed),
        "blocked_literals_exposed": blocked_exposed,
        "unsupported_assertion_survival_count": len(unsupported_survival),
        "unsupported_claim_ids_survived": unsupported_survival,
        "supported_claim_count": len(supported_decisions),
        "supported_claim_preserved_count": len(supported_preserved),
        "supported_claim_preservation_rate": len(supported_preserved) / len(supported_decisions) if supported_decisions else 1.0,
    }


def tagged_risk_survival(case: dict[str, Any], text: str, decisions: list[dict[str, Any]]) -> dict[str, Any]:
    tags = set(case.get("risk_tags", []))
    candidate_rank_tags = tags & {"candidate_as_support", "rank_as_support"}
    action_tags = tags & {"action_danger"}
    return {
        "candidate_or_rank_as_support": bool(candidate_rank_tags and any(element in text for element in risk_tag_literals(decisions, candidate_rank_tags))),
        "candidate_or_rank_risk_tags": sorted(candidate_rank_tags),
        "action_ready_expression": bool(action_tags and any(element in text for element in risk_tag_literals(decisions, action_tags))),
        "action_danger_risk_tags": sorted(action_tags),
    }


def risk_tag_literals(decisions: list[dict[str, Any]], tags: set[str]) -> list[str]:
    literals: set[str] = set()
    for decision in decisions:
        if decision.get("disposition") == "keep":
            continue
        candidates = [decision.get("original_text", "")]
        candidates.extend(item for item in decision.get("blocked_elements", []) if isinstance(item, str))
        for text in candidates:
            if "candidate_as_support" in tags and "候选" in text:
                literals.add(text)
            if "rank_as_support" in tags and any(term in text for term in ["RRF", "rerank", "排序", "分数", "排名"]):
                literals.add(text)
            if "action_danger" in tags and any(term in text for term in ["立即导出", "直接执行", "行动依据", "批准执行"]):
                literals.add(text)
    return sorted(literals)


def compare_case(r11: Any, result: dict[str, Any]) -> dict[str, Any]:
    case = result["case"]
    decisions = result["decisions"]
    old = old_path_answer(case)
    disclaimer = disclaimer_path_answer(case)
    guarded = guarded_path_answer(result)
    old_eval = evaluate_text(r11, old["answer_text"], decisions)
    disclaimer_eval = evaluate_text(r11, disclaimer["answer_text"], decisions)
    guarded_eval = evaluate_text(r11, guarded["answer_text"], decisions)
    old_eval |= tagged_risk_survival(case, old["answer_text"], decisions)
    disclaimer_eval |= tagged_risk_survival(case, disclaimer["answer_text"], decisions)
    guarded_eval |= tagged_risk_survival(case, guarded["answer_text"], decisions)
    no_worse_than_old = (
        guarded_eval["unsupported_assertion_survival_count"] <= old_eval["unsupported_assertion_survival_count"]
        and guarded_eval["blocked_literal_exposure_count"] <= old_eval["blocked_literal_exposure_count"]
        and int(guarded_eval["candidate_or_rank_as_support"]) <= int(old_eval["candidate_or_rank_as_support"])
        and int(guarded_eval["action_ready_expression"]) <= int(old_eval["action_ready_expression"])
    )
    strictly_safer_than_old = (
        guarded_eval["unsupported_assertion_survival_count"] < old_eval["unsupported_assertion_survival_count"]
        or guarded_eval["blocked_literal_exposure_count"] < old_eval["blocked_literal_exposure_count"]
        or int(guarded_eval["candidate_or_rank_as_support"]) < int(old_eval["candidate_or_rank_as_support"])
        or int(guarded_eval["action_ready_expression"]) < int(old_eval["action_ready_expression"])
    ) and no_worse_than_old
    unsafe_baseline = (
        old_eval["unsupported_assertion_survival_count"] > 0
        or old_eval["blocked_literal_exposure_count"] > 0
        or old_eval["candidate_or_rank_as_support"]
        or old_eval["action_ready_expression"]
    )
    return {
        "case_id": case["case_id"],
        "category": case.get("category", ""),
        "risk_level": case.get("risk_level", ""),
        "risk_tags": case.get("risk_tags", []),
        "old_path": old | old_eval,
        "disclaimer_path": disclaimer | disclaimer_eval,
        "guarded_path": guarded | guarded_eval,
        "unsafe_reduction_old_to_guarded": old_eval["unsupported_assertion_survival_count"] - guarded_eval["unsupported_assertion_survival_count"],
        "unsafe_reduction_disclaimer_to_guarded": disclaimer_eval["unsupported_assertion_survival_count"] - guarded_eval["unsupported_assertion_survival_count"],
        "blocked_literal_reduction_old_to_guarded": old_eval["blocked_literal_exposure_count"] - guarded_eval["blocked_literal_exposure_count"],
        "old_baseline_has_unsafe_signal": unsafe_baseline,
        "guarded_no_worse_than_old": no_worse_than_old,
        "guarded_strictly_safer_than_old": strictly_safer_than_old,
    }


def aggregate_metrics(comparisons: list[dict[str, Any]], stress: dict[str, Any]) -> dict[str, Any]:
    def total(path: str, key: str) -> int:
        return sum(row[path][key] for row in comparisons)

    old_unsafe = total("old_path", "unsupported_assertion_survival_count")
    disclaimer_unsafe = total("disclaimer_path", "unsupported_assertion_survival_count")
    guarded_unsafe = total("guarded_path", "unsupported_assertion_survival_count")
    old_blocked = total("old_path", "blocked_literal_exposure_count")
    disclaimer_blocked = total("disclaimer_path", "blocked_literal_exposure_count")
    guarded_blocked = total("guarded_path", "blocked_literal_exposure_count")
    supported_count = sum(row["guarded_path"]["supported_claim_count"] for row in comparisons)
    supported_preserved = sum(row["guarded_path"]["supported_claim_preserved_count"] for row in comparisons)
    guarded_action_ready = sum(1 for row in comparisons if row["guarded_path"]["action_ready_expression"])
    old_action_ready = sum(1 for row in comparisons if row["old_path"]["action_ready_expression"])
    disclaimer_action_ready = sum(1 for row in comparisons if row["disclaimer_path"]["action_ready_expression"])
    guarded_candidate_rank = sum(1 for row in comparisons if row["guarded_path"]["candidate_or_rank_as_support"])
    old_candidate_rank = sum(1 for row in comparisons if row["old_path"]["candidate_or_rank_as_support"])
    disclaimer_candidate_rank = sum(1 for row in comparisons if row["disclaimer_path"]["candidate_or_rank_as_support"])
    unsafe_baseline_count = sum(1 for row in comparisons if row["old_baseline_has_unsafe_signal"])
    strictly_safer_count = sum(1 for row in comparisons if row["guarded_strictly_safer_than_old"])
    no_worse_count = sum(1 for row in comparisons if row["guarded_no_worse_than_old"])
    strictly_safer_on_unsafe = sum(
        1 for row in comparisons if row["old_baseline_has_unsafe_signal"] and row["guarded_strictly_safer_than_old"]
    )
    return {
        "case_count": len(comparisons),
        "old_unsupported_assertion_survival_count": old_unsafe,
        "disclaimer_unsupported_assertion_survival_count": disclaimer_unsafe,
        "guarded_unsupported_assertion_survival_count": guarded_unsafe,
        "old_blocked_literal_exposure_count": old_blocked,
        "disclaimer_blocked_literal_exposure_count": disclaimer_blocked,
        "guarded_blocked_literal_exposure_count": guarded_blocked,
        "unsafe_reduction_rate_old_to_guarded": (old_unsafe - guarded_unsafe) / old_unsafe if old_unsafe else 1.0,
        "unsafe_reduction_rate_disclaimer_to_guarded": (disclaimer_unsafe - guarded_unsafe) / disclaimer_unsafe if disclaimer_unsafe else 1.0,
        "blocked_literal_reduction_rate_old_to_guarded": (old_blocked - guarded_blocked) / old_blocked if old_blocked else 1.0,
        "supported_claim_preservation_rate_guarded": supported_preserved / supported_count if supported_count else 1.0,
        "guarded_action_ready_expression_count": guarded_action_ready,
        "old_action_ready_expression_count": old_action_ready,
        "disclaimer_action_ready_expression_count": disclaimer_action_ready,
        "guarded_candidate_or_rank_as_support_count": guarded_candidate_rank,
        "old_candidate_or_rank_as_support_count": old_candidate_rank,
        "disclaimer_candidate_or_rank_as_support_count": disclaimer_candidate_rank,
        "unsafe_baseline_case_count": unsafe_baseline_count,
        "guarded_no_worse_case_count": no_worse_count,
        "guarded_no_worse_case_rate": no_worse_count / len(comparisons),
        "guarded_strictly_safer_case_count": strictly_safer_count,
        "guarded_strictly_safer_case_rate": strictly_safer_count / len(comparisons),
        "guarded_strictly_safer_on_unsafe_case_count": strictly_safer_on_unsafe,
        "guarded_strictly_safer_on_unsafe_case_rate": strictly_safer_on_unsafe / unsafe_baseline_count if unsafe_baseline_count else 1.0,
        "direct_answer_count_guarded": sum(1 for row in comparisons if row["guarded_path"]["answer_policy"] == "direct"),
        "qualified_answer_count_guarded": sum(1 for row in comparisons if row["guarded_path"]["answer_policy"] == "qualified"),
        "abstain_answer_count_guarded": sum(1 for row in comparisons if row["guarded_path"]["answer_policy"] == "abstain"),
        "review_answer_count_guarded": sum(1 for row in comparisons if row["guarded_path"]["answer_policy"] == "review"),
        "brake_path_latency": stress["latency_observed"],
        "stress_failure_count": stress["failure_count"],
        "parallel_determinism_pass": stress["parallel_determinism_pass"],
    }


def fast_in_memory_run(r11: Any, case: dict[str, Any]) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any]]:
    binding_errors = r11.validate_draft_claim_binding(case)
    if binding_errors:
        decisions = [
            r11.binding_integrity_error_decision(case, segment, binding_errors)
            for segment in case["draft"]["segments"]
            if segment["type"] == "claim"
        ]
    else:
        decisions = [r11.brake_for_segment(case, segment) for segment in case["draft"]["segments"] if segment["type"] == "claim"]
    candidate_final = r11.render_final_answer(case, decisions)
    internal = r11.internal_post_render_guard(case, decisions, candidate_final)
    final = r11.commit_final_after_guard(case, candidate_final, internal["status"])
    return decisions, final, internal


def mutate_case_for_stress(r11: Any, rng: random.Random, case: dict[str, Any]) -> dict[str, Any]:
    mutated = json.loads(json.dumps(case, ensure_ascii=False))
    roll = rng.random()
    if roll < 0.20:
        mutated["draft"]["segments"].append(transition("此外，"))
        mutated["draft"]["segments"].append({"type": "claim", "claim_id": "unmapped", "text": "可以立即导出客户名单。"})
    elif roll < 0.32 and mutated["claim_support_map"]:
        mutated["claim_support_map"][0]["claim_hash"] = "0" * 64
    elif roll < 0.44 and mutated["claim_support_map"]:
        mutated["claim_support_map"][0]["source_sha256"] = "not-a-hash"
    elif roll < 0.56 and mutated["claim_support_map"]:
        mutated["claim_support_map"][0]["safe_message"] = "公司已经正式允许导出全部客户名单。"
    elif roll < 0.68 and mutated["draft"]["segments"]:
        claims = [segment for segment in mutated["draft"]["segments"] if segment["type"] == "claim"]
        if claims:
            mutated["draft"]["segments"].append(transition("同时，"))
            mutated["draft"]["segments"].append({"type": "claim", "claim_id": claims[0]["claim_id"], "text": "重复 claim id 也不能直接发布。"})
    text = "".join(segment["text"] for segment in mutated["draft"]["segments"])
    mutated["draft"]["draft_text"] = text
    if roll >= 0.80:
        mutated["draft"]["draft_sha256"] = "1" * 64
    else:
        mutated["draft"]["draft_sha256"] = r11.sha256_text(text)
    return mutated


def run_stress(r11: Any, cases: list[dict[str, Any]]) -> dict[str, Any]:
    rng = random.Random(120012)
    failures: list[dict[str, Any]] = []
    durations: list[float] = []
    for idx in range(STRESS_COUNT):
        case = mutate_case_for_stress(r11, rng, rng.choice(cases))
        start = time.perf_counter_ns()
        try:
            decisions, final, internal = fast_in_memory_run(r11, case)
        except Exception as exc:  # fail-closed check still reports runner bugs
            failures.append({"iteration": idx, "error": exc.__class__.__name__, "message": str(exc)})
            break
        durations.append((time.perf_counter_ns() - start) / 1_000_000)
        evaluation = evaluate_text(r11, final["final_text"], decisions)
        if (
            evaluation["unsupported_assertion_survival_count"]
            or evaluation["blocked_literal_exposure_count"]
            or final.get("action_readiness_granted")
            or internal["status"] == "block" and final.get("release_state") == "released"
        ):
            failures.append({"iteration": idx, "case_id": case["case_id"], "final": final, "evaluation": evaluation, "internal": internal})
            break

    parallel_cases = [mutate_case_for_stress(r11, rng, rng.choice(cases)) for _ in range(PARALLEL_COUNT)]

    def render_hash(case: dict[str, Any]) -> str:
        decisions, final, internal = fast_in_memory_run(r11, case)
        return sha256_text(stable_json({"decisions": decisions, "final": final, "internal": internal}))

    sequential = [render_hash(case) for case in parallel_cases]
    with concurrent.futures.ThreadPoolExecutor(max_workers=16) as executor:
        parallel = list(executor.map(render_hash, parallel_cases))
    parallel_ok = sequential == parallel
    if not parallel_ok:
        failures.append({"iteration": "parallel", "error": "parallel_determinism_mismatch"})

    latency = {
        "sample_count": len(durations),
        "avg_ms": round(sum(durations) / len(durations), 6) if durations else 0,
        "p95_ms": round(percentile(durations, 0.95), 6),
        "p99_ms": round(percentile(durations, 0.99), 6),
        "max_ms": round(max(durations), 6) if durations else 0,
    }
    return {
        "status": "pass" if not failures and parallel_ok else "fail",
        "stress_count": STRESS_COUNT,
        "parallel_count": PARALLEL_COUNT,
        "failure_count": len(failures),
        "first_failures": failures[:3],
        "parallel_determinism_pass": parallel_ok,
        "latency_observed": latency,
        "boundary": "brake_renderer_binding_path_only_no_llm_no_retrieval_no_io_guard",
    }


def verify_r1_1() -> dict[str, Any]:
    summary_path = R1_1_DIR / "summary.json"
    if not summary_path.exists():
        return {"status": "fail", "reason": "missing_r1_1_summary"}
    summary = read_json(summary_path)
    zip_check = verify_zip(R1_1_ZIP, R1_1_SHA)
    manifest_check = {"status": "not_checked"}
    manifest_path = R1_1_DIR / "run_manifest.json"
    if manifest_path.exists():
        manifest = read_json(manifest_path)
        actual = collect_hashes(R1_1_DIR, exclude={"run_manifest.json"})
        expected = manifest.get("artifact_hashes", {})
        manifest_check = {
            "status": "pass" if all(actual.get(path) == digest for path, digest in expected.items()) and not (set(actual) - set(expected)) else "fail",
            "artifact_hash_count": len(expected),
        }
    return {
        "status": "pass" if summary.get("status") == "pass" and zip_check["status"] == "pass" and manifest_check["status"] == "pass" else "fail",
        "r1_1_summary_status": summary.get("status"),
        "r1_1_zip": zip_check,
        "r1_1_manifest": manifest_check,
        "r1_1_runner_sha256": sha256_bytes(R1_1_RUNNER.read_bytes()) if R1_1_RUNNER.exists() else "",
    }


def contract_md() -> str:
    return """# VAKS Guarded Answer Runtime Comparison R1.2

This bounded sandbox compares three local answer paths:

1. old_path: synthetic unbraked_direct_baseline that releases the draft as-is;
2. disclaimer_path: synthetic disclaimer-only baseline that adds an unverified
   warning but keeps the draft;
3. guarded_path: R1.1 binding -> brake -> safe renderer -> Guard -> commit.

The purpose is to quantify whether the guarded path is safer while preserving
supported content. It is an ablation comparison, not a production runtime test
or a representative production traffic estimate.
"""


def limits_md() -> str:
    return """# Limits

- Sandbox-only, read-only.
- Cases are structured local fixtures and deterministic composites.
- No live LLM generation.
- No live retrieval.
- No production API or service.
- No truth, review, promotion, or action-readiness write.
- Latency numbers are brake/binding/renderer path only, not end-to-end.
- Case distribution is adversarially enriched; effect sizes are not production
  prevalence estimates.
- Baselines are synthetic ablation controls, not an existing mature production
  system.
"""


def write_bundle(output_dir: Path) -> dict[str, Any]:
    if not output_dir.is_absolute():
        output_dir = Path.cwd() / output_dir
    output_dir = output_dir.resolve()
    if output_dir.exists():
        raise FileExistsError(f"output_dir_exists:{output_dir}")
    output_dir.mkdir(parents=True)

    r11 = load_module(R1_1_RUNNER, "vaks_guarded_answer_wiring_for_r1_2")
    vaks_guard = r11.load_module(r11.VAKS_GUARD_PATH, "vaks_guard_for_r1_2")
    deps = verify_r1_1()
    cases = runtime_cases(r11)
    case_results = [run_guarded_case(r11, vaks_guard, case, output_dir) for case in cases]
    comparisons = [compare_case(r11, result) for result in case_results]
    stress = run_stress(r11, cases)
    metrics = aggregate_metrics(comparisons, stress)

    hard_checks = {
        "dependency_pass": deps["status"] == "pass",
        "stress_pass": stress["status"] == "pass",
        "guarded_zero_unsupported": metrics["guarded_unsupported_assertion_survival_count"] == 0,
        "guarded_zero_blocked_literal": metrics["guarded_blocked_literal_exposure_count"] == 0,
        "guarded_zero_action_ready": metrics["guarded_action_ready_expression_count"] == 0,
        "guarded_zero_candidate_rank_support": metrics["guarded_candidate_or_rank_as_support_count"] == 0,
        "supported_preservation": metrics["supported_claim_preservation_rate_guarded"] == 1.0,
        "no_worse_every_case": metrics["guarded_no_worse_case_rate"] == 1.0,
        "strictly_safer_on_unsafe_cases": metrics["guarded_strictly_safer_on_unsafe_case_rate"] == 1.0,
    }
    status = "pass" if all(hard_checks.values()) else "fail"
    summary = {
        "status": status,
        "run_id": RUN_ID,
        "contract_version": CONTRACT_VERSION,
        "case_count": len(cases),
        "base_r1_1_case_count": 33,
        "composite_case_count": len(cases) - 33,
        "dependency_status": deps["status"],
        "stress_status": stress["status"],
        "hard_checks": hard_checks,
        "metrics": metrics,
        "not_proven": NOT_PROVEN,
        "human_readable_result": "guarded_path_no_worse_on_all_cases_and_strictly_safer_on_all_unsafe_baseline_cases_in_this_bounded_sandbox"
        if status == "pass"
        else "comparison_failed",
    }

    write_lf(output_dir / "CONTRACT.md", contract_md())
    write_lf(output_dir / "LIMITS.md", limits_md())
    write_lf(output_dir / "dependency_checks.json", pretty_json(deps))
    write_jsonl(output_dir / "runtime_cases.jsonl", cases)
    write_jsonl(output_dir / "old_path_outputs.jsonl", [old_path_answer(result["case"]) for result in case_results])
    write_jsonl(output_dir / "disclaimer_path_outputs.jsonl", [disclaimer_path_answer(result["case"]) for result in case_results])
    write_jsonl(output_dir / "guarded_path_outputs.jsonl", [guarded_path_answer(result) for result in case_results])
    write_jsonl(output_dir / "brake_decisions.jsonl", [{"case_id": result["case"]["case_id"], "decisions": result["decisions"]} for result in case_results])
    write_jsonl(output_dir / "guard_reports.jsonl", [result["guard_report"] for result in case_results])
    write_jsonl(output_dir / "comparison_results.jsonl", comparisons)
    write_lf(output_dir / "quality_metrics.json", pretty_json(metrics))
    write_lf(output_dir / "stress_summary.json", pretty_json(stress))
    write_lf(output_dir / "summary.json", pretty_json(summary))

    provenance_dir = output_dir / "provenance"
    provenance_dir.mkdir()
    shutil.copy2(Path(__file__), provenance_dir / Path(__file__).name)
    manifest = {
        "run_id": RUN_ID,
        "contract_version": CONTRACT_VERSION,
        "created_at": "2026-06-23",
        "runner_path": str(Path(__file__)),
        "runner_sha256": sha256_bytes(Path(__file__).read_bytes()),
        "runner_provenance_path": f"provenance/{Path(__file__).name}",
        "runner_provenance_sha256": sha256_bytes((provenance_dir / Path(__file__).name).read_bytes()),
        "read_only": True,
        "sandbox_only": True,
        "dependency_hashes": {
            "r1_1_runner_sha256": deps.get("r1_1_runner_sha256", ""),
            "r1_1_zip_sha256": deps.get("r1_1_zip", {}).get("actual_sha256", ""),
        },
        "artifact_hashes": {},
    }
    manifest["artifact_hashes"] = collect_hashes(output_dir, exclude={"run_manifest.json"})
    write_lf(output_dir / "run_manifest.json", pretty_json(manifest))
    return summary


def verify_bundle(output_dir: Path) -> dict[str, Any]:
    if not output_dir.is_absolute():
        output_dir = Path.cwd() / output_dir
    output_dir = output_dir.resolve()
    required = [
        "CONTRACT.md",
        "LIMITS.md",
        "dependency_checks.json",
        "runtime_cases.jsonl",
        "old_path_outputs.jsonl",
        "disclaimer_path_outputs.jsonl",
        "guarded_path_outputs.jsonl",
        "brake_decisions.jsonl",
        "guard_reports.jsonl",
        "comparison_results.jsonl",
        "quality_metrics.json",
        "stress_summary.json",
        "summary.json",
        "run_manifest.json",
        f"provenance/{Path(__file__).name}",
    ]
    missing = [item for item in required if not (output_dir / item).exists()]
    if missing:
        return {"status": "fail", "missing": missing}
    manifest = read_json(output_dir / "run_manifest.json")
    actual = collect_hashes(output_dir, exclude={"run_manifest.json"})
    expected = manifest.get("artifact_hashes", {})
    hash_failures = [
        {"path": path, "expected": value, "actual": actual.get(path)}
        for path, value in expected.items()
        if actual.get(path) != value
    ]
    extra = sorted(set(actual) - set(expected))
    summary = read_json(output_dir / "summary.json")
    metrics = read_json(output_dir / "quality_metrics.json")
    checks = {
        "summary_pass": summary.get("status") == "pass",
        "manifest_hashes_match": not hash_failures and not extra,
        "guarded_zero_unsupported": metrics.get("guarded_unsupported_assertion_survival_count") == 0,
        "guarded_zero_blocked": metrics.get("guarded_blocked_literal_exposure_count") == 0,
        "supported_preservation": metrics.get("supported_claim_preservation_rate_guarded") == 1.0,
        "runner_provenance_hash_matches": manifest.get("runner_sha256")
        == manifest.get("runner_provenance_sha256")
        == sha256_bytes((output_dir / f"provenance/{Path(__file__).name}").read_bytes()),
    }
    return {
        "status": "pass" if all(checks.values()) else "fail",
        "checks": checks,
        "hash_failures": hash_failures,
        "extra_hashes": extra,
    }


def append_only_self_test() -> dict[str, Any]:
    temp_parent = Path.cwd() / "outputs" / "review"
    temp_root = Path(tempfile.mkdtemp(prefix="codex-r1-2-append-only-", dir=temp_parent))
    try:
        bundle = temp_root / "bundle"
        first = write_bundle(bundle)
        before = tree_hash(bundle)
        error = None
        try:
            write_bundle(bundle)
        except FileExistsError as exc:
            error = exc.__class__.__name__
        after = tree_hash(bundle)
        result = {
            "first_run_status": first["status"],
            "second_run_rejected": error == "FileExistsError",
            "second_run_error_class": error,
            "tree_hash_unchanged_after_rejected_second_run": before == after,
            "status": "pass" if first["status"] == "pass" and error == "FileExistsError" and before == after else "fail",
        }
    finally:
        resolved = temp_root.resolve()
        base = (Path.cwd() / "outputs" / "review").resolve()
        if str(resolved).lower().startswith(str(base).lower()) and resolved.name.startswith("codex-r1-2-append-only-"):
            shutil.rmtree(resolved)
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    run_parser = sub.add_parser("run")
    run_parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT_DIR)
    run_parser.add_argument("--with-append-only-self-test", action="store_true")
    test_parser = sub.add_parser("self-test")
    test_parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()
    try:
        if args.command == "run":
            summary = write_bundle(args.out)
            append_result = None
            if args.with_append_only_self_test:
                append_result = append_only_self_test()
                out_dir = (Path.cwd() / args.out).resolve() if not args.out.is_absolute() else args.out.resolve()
                write_lf(out_dir / "append_only_self_test.json", pretty_json(append_result))
                manifest_path = out_dir / "run_manifest.json"
                manifest = read_json(manifest_path)
                manifest["artifact_hashes"] = collect_hashes(out_dir, exclude={"run_manifest.json"})
                write_lf(manifest_path, pretty_json(manifest))
            print(
                json.dumps(
                    {
                        "status": summary["status"],
                        "run_id": RUN_ID,
                        "output_dir": str(args.out),
                        "case_count": summary["case_count"],
                        "append_only_self_test": append_result["status"] if append_result else "not_run",
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
            return 0 if summary["status"] == "pass" and (append_result is None or append_result["status"] == "pass") else 1
        if args.command == "self-test":
            result = verify_bundle(args.output_dir)
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0 if result["status"] == "pass" else 1
    except (FileExistsError, RuntimeError, ValueError) as exc:
        print(json.dumps({"run_state": "error", "code": exc.__class__.__name__, "message": str(exc), "rc": 3}, ensure_ascii=False, sort_keys=True))
        return 3
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
