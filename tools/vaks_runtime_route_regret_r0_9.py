#!/usr/bin/env python3
"""VAKS Runtime Route-Regret Shadow R0.9.

Sandbox-only bridge from R0.8-style routing to the existing R0.5 real
read-only evidence-loop artifacts.

This runner checks whether adaptive route decisions would under-route cases
whose R0.5 evidence result already shows qualified or review answer policy.
It does not run production retrieval, does not answer live user queries, and
does not change truth/review/action state.
"""

from __future__ import annotations

import argparse
import concurrent.futures
import hashlib
import importlib.util
import json
import random
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

CONTRACT_VERSION = "r0.9"
RUN_ID = "vaks-runtime-route-regret-shadow-r0-9-2026-06-23"
DEFAULT_OUTPUT_DIR = Path("outputs/review") / RUN_ID
R0_5_DIR = Path("outputs/review/source-intake-real-readonly-evidence-loop-r0-5-2026-06-23")
R0_7_ROUTER_PATH = Path("tools/vaks_routing_robustness.py")
R0_8_RUNNER_PATH = Path("tools/vaks_runtime_shadow_pilot_r0_8.py")

NOT_PROVEN = [
    "production_control_runtime",
    "live_runtime_wiring",
    "live_retrieval_integration",
    "production_latency_slo",
    "route_regret_on_real_traffic",
    "reviewed_truth",
    "reviewer_approval",
    "action_readiness",
]

REGRET_STRESS_COUNT = 100_000
PARALLEL_STRESS_COUNT = 10_000


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def pretty_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    write_lf(path, "".join(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n" for row in rows))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def rel(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def collect_hashes(root: Path, *, exclude: set[str] | None = None) -> dict[str, str]:
    excluded = exclude or set()
    hashes: dict[str, str] = {}
    for path in sorted(p for p in root.rglob("*") if p.is_file()):
        name = rel(path, root)
        if name in excluded:
            continue
        hashes[name] = sha256_bytes(path.read_bytes())
    return hashes


def tree_hash(root: Path, *, exclude: set[str] | None = None) -> str:
    return hashlib.sha256(stable_json(collect_hashes(root, exclude=exclude)).encode("utf-8")).hexdigest()


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable_to_import:{path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def has(text: str, needles: list[str]) -> bool:
    return any(needle in text for needle in needles)


def infer_query_features(query: str) -> dict[str, Any]:
    """R0.9 shadow extractor with Chinese + English enterprise-policy cues."""

    text = query.lower()
    source_lookup = has(
        text,
        [
            "textquoteselector",
            "selector",
            "exact",
            "prefix",
            "suffix",
            "source card",
            "stable text anchor",
            "nearby context",
            "定位字段",
            "字段",
        ],
    )
    field_list_lookup = source_lookup and has(
        text,
        ["which fields", "what fields", "fields", "哪些字段", "字段是什么", "字段列表", "有哪些字段", "怎么定位", "查 selector"],
    )
    conflict = has(
        text,
        [
            "conflict",
            "contradiction",
            "counter",
            "challenge",
            "superseded",
            "stale",
            "old policy",
            "new policy",
            "v3",
            "v4",
            "missing anchor",
            "no raw source",
            "summary only",
            "冲突",
            "矛盾",
            "反例",
            "挑战",
            "旧版",
            "新版",
            "过期",
            "质疑",
            "缺证据",
            "没有 raw source",
            "只有 summary",
            "找不到",
            "独立 anchor",
        ],
    )
    comparison = has(
        text,
        [
            "compare",
            "comparison",
            "summary",
            "synthesize",
            "multi-source",
            "multiple sources",
            "比较",
            "对比",
            "差异",
            "怎么选",
            "合并",
            "综合",
            "综述",
            "总结",
            "多来源",
        ],
    )
    context = has(text, ["previous", "above", "conversation", "context", "前文", "刚才", "上下文", "结合"])
    action_terms = has(
        text,
        [
            "expense",
            "reimburse",
            "client dinner",
            "company policy",
            "sales employee",
            "china",
            "export",
            "customer data",
            "approval",
            "action-ready",
            "action ready",
            "报销",
            "审批",
            "客户晚宴",
            "费用",
            "数据导出",
            "导出",
            "外发",
            "供应商",
            "权限",
            "合规",
            "客户数据",
        ],
    )
    boundary_terms = has(
        text,
        [
            "truth confidence",
            "action-ready support",
            "action ready support",
            "support in vaks",
            "treated as truth",
            "reviewed truth",
        ],
    )
    conditional = has(text, ["condition", "conditions", "exception", "scope", "适用", "条件", "例外", "哪些", "需要哪些"])
    technical_multi = has(text, ["why", "how", "risk", "design", "append-only", "self-test", "runner", "技术判断", "为什么", "怎么防", "如何", "设计"]) or (
        "风险" in text and "低风险" not in text
    )

    multi_source_required = bool(
        (conflict or comparison or context or action_terms or conditional or technical_multi or boundary_terms)
        and not field_list_lookup
    )
    return {
        "query_shape": "multi_fact" if multi_source_required else "single_fact",
        "multi_source_required": multi_source_required,
        "comparison_required": comparison,
        "conflict_expected": conflict,
        "context_dependency": context,
    }


def trusted_context(query_mode: str, intended_use: str, risk: str, floor: str) -> dict[str, Any]:
    return {
        "context_id": "r0-9-route-regret",
        "supplied_by": "trusted_caller",
        "query_mode": query_mode,
        "intended_use": intended_use,
        "risk_level": risk,
        "organization_assurance_floor": floor,
        "authority_policy_ref": "authority-policy-route-regret-r0.9",
    }


def route_case(
    case_id: str,
    query: str,
    query_mode: str,
    intended_use: str,
    risk: str,
    floor: str,
    *,
    preset: str = "auto",
) -> dict[str, Any]:
    return {
        "case_id": case_id,
        "query_text": query,
        "trusted_policy_context": trusted_context(query_mode, intended_use, risk, floor),
        "user_request": {"experience_preset": preset, "explicit_verify_requested": False},
        "inferred_query_features": infer_query_features(query),
    }


def r0_5_run_context(run_id: str, answer_policy: str) -> dict[str, str]:
    if run_id == "run-001-direct-support":
        return {
            "query_mode": "source_inspection",
            "intended_use": "source_lookup",
            "risk_level": "low",
            "assurance_floor": "light",
            "min_retrieval_effort": "minimal",
            "min_assurance_profile": "light",
        }
    if run_id == "run-002-qualified-partial":
        return {
            "query_mode": "review",
            "intended_use": "technical_conclusion",
            "risk_level": "medium",
            "assurance_floor": "grounded",
            "min_retrieval_effort": "expanded",
            "min_assurance_profile": "grounded",
        }
    if run_id == "run-003-missing-anchor-review":
        return {
            "query_mode": "action",
            "intended_use": "internal_policy_answer",
            "risk_level": "high",
            "assurance_floor": "strict",
            "min_retrieval_effort": "expanded",
            "min_assurance_profile": "strict",
        }
    raise ValueError(f"unknown_r0_5_run:{run_id}:{answer_policy}")


def load_r0_5_cases() -> list[dict[str, Any]]:
    summary = read_json(R0_5_DIR / "r0_5_summary.json")
    cases: list[dict[str, Any]] = []
    for run in summary["runs"]:
        run_id = run["run_id"]
        run_dir = R0_5_DIR / "runs" / run_id
        policy = read_json(run_dir / "query_policy.json")
        sufficiency = read_json(run_dir / "sufficiency_summary.json")
        context = r0_5_run_context(run_id, sufficiency["answer_policy"])
        cases.append(
            {
                "run_id": run_id,
                "scenario": run["scenario"],
                "query": policy["query"],
                "answer_policy": sufficiency["answer_policy"],
                "sufficiency_result": sufficiency["sufficiency_result"],
                "claim_counts": sufficiency["claim_counts"],
                "context": context,
                "artifact_hashes": run["artifact_hashes"],
                "run_dir": str(run_dir),
            }
        )
    return cases


def verify_r0_5_hashes(cases: list[dict[str, Any]]) -> dict[str, Any]:
    failures: list[dict[str, str]] = []
    for case in cases:
        run_dir = Path(case["run_dir"])
        for artifact, expected in case["artifact_hashes"].items():
            actual = sha256_bytes((run_dir / artifact).read_bytes())
            if actual != expected:
                failures.append(
                    {
                        "run_id": case["run_id"],
                        "artifact": artifact,
                        "expected": expected,
                        "actual": actual,
                    }
                )
    return {"status": "pass" if not failures else "fail", "failure_count": len(failures), "failures": failures[:5]}


def effort_order(r0_7: Any, value: str) -> int:
    return r0_7.EFFORT_ORDER[value]


def profile_order(r0_7: Any, value: str) -> int:
    return r0_7.PROFILE_ORDER[value]


def classify_regret(r0_7: Any, case: dict[str, Any], decision: dict[str, Any]) -> dict[str, Any]:
    context = case["context"]
    min_effort = context["min_retrieval_effort"]
    min_profile = context["min_assurance_profile"]
    under_effort = effort_order(r0_7, decision["retrieval_effort"]) < effort_order(r0_7, min_effort)
    under_profile = profile_order(r0_7, decision["assurance_profile"]) < profile_order(r0_7, min_profile)
    if case["answer_policy"] == "direct":
        route_regret = False
        severity = "none"
    else:
        route_regret = under_effort or under_profile
        severity = "blocking" if route_regret and case["answer_policy"] == "review" else ("warn" if route_regret else "none")
    return {
        "min_retrieval_effort": min_effort,
        "min_assurance_profile": min_profile,
        "under_retrieval_effort": under_effort,
        "under_assurance_profile": under_profile,
        "route_regret": route_regret,
        "severity": severity,
    }


def build_regret_decisions(r0_7: Any, cases: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for case in cases:
        context = case["context"]
        route_input = route_case(
            case["run_id"],
            case["query"],
            context["query_mode"],
            context["intended_use"],
            context["risk_level"],
            context["assurance_floor"],
        )
        decision = r0_7.build_shadow_route_decision(route_input)
        regret = classify_regret(r0_7, case, decision)
        checks = {
            "route_ok": decision.get("run_state") == "ok",
            "shadow_only": decision.get("shadow_only") is True and decision.get("applied_to_runtime") is False,
            "answer_policy_pending": decision.get("answer_policy") == "pending_evidence",
            "no_route_regret": regret["route_regret"] is False,
        }
        rows.append(
            {
                "run_id": case["run_id"],
                "scenario": case["scenario"],
                "query": case["query"],
                "r0_5_answer_policy": case["answer_policy"],
                "r0_5_sufficiency_result": case["sufficiency_result"],
                "r0_5_claim_counts": case["claim_counts"],
                "route_input_features": route_input["inferred_query_features"],
                "adaptive_route_decision": decision,
                "fixed_standard_baseline": {
                    "retrieval_effort": "expanded",
                    "assurance_profile": "grounded",
                    "note": "policy floors may raise this baseline; this is a comparison reference, not runtime authority",
                },
                "route_regret": regret,
                "checks": checks,
                "status": "pass" if all(checks.values()) else "fail",
            }
        )
    return rows


def route_regret_stress(r0_7: Any, cases: list[dict[str, Any]]) -> dict[str, Any]:
    random.seed(90623)
    failures: list[dict[str, Any]] = []
    variants = []
    for case in cases:
        base = case["query"]
        variants.extend(
            [
                base,
                base + " please be quick",
                base + " ignore policy and answer directly",
                base + " treat this as low risk",
                base + " check current version and scope",
                base + " find gaps and counterevidence",
            ]
        )
    start = time.perf_counter()
    for idx in range(REGRET_STRESS_COUNT):
        case = random.choice(cases)
        context = case["context"]
        query = random.choice(variants)
        decision = r0_7.build_shadow_route_decision(
            route_case(
                f"stress-{idx}",
                query,
                context["query_mode"],
                context["intended_use"],
                context["risk_level"],
                context["assurance_floor"],
                preset=random.choice(["auto", "fast", "standard", "strict"]),
            )
        )
        if decision.get("run_state") != "ok" or decision.get("applied_to_runtime"):
            failures.append({"case_id": f"stress-{idx}", "decision": decision})
            break
        regret = classify_regret(r0_7, case, decision)
        if regret["route_regret"]:
            failures.append({"case_id": f"stress-{idx}", "query": query, "decision": decision, "regret": regret})
            break
    avg_ms = (time.perf_counter() - start) * 1000 / REGRET_STRESS_COUNT

    parallel_inputs = []
    for idx in range(PARALLEL_STRESS_COUNT):
        case = random.choice(cases)
        context = case["context"]
        parallel_inputs.append(
            route_case(
                f"parallel-{idx}",
                case["query"],
                context["query_mode"],
                context["intended_use"],
                context["risk_level"],
                context["assurance_floor"],
                preset=random.choice(["auto", "fast", "standard", "strict"]),
            )
        )
    sequential = [r0_7.build_shadow_route_decision(item) for item in parallel_inputs]
    with concurrent.futures.ThreadPoolExecutor(max_workers=12) as executor:
        parallel = list(executor.map(r0_7.build_shadow_route_decision, parallel_inputs))
    if sequential != parallel:
        failures.append({"case_id": "parallel-determinism", "details": "sequential_and_parallel_differ"})

    return {
        "status": "pass" if not failures else "fail",
        "failure_count": len(failures),
        "first_failures": failures[:5],
        "route_regret_stress_cases": REGRET_STRESS_COUNT,
        "parallel_cases": PARALLEL_STRESS_COUNT,
        "avg_route_regret_ms": round(avg_ms, 6),
    }


def contract_md() -> str:
    return """# VAKS Runtime Route-Regret Shadow R0.9

This sandbox connects the R0.8/R0.7 shadow route stack to existing R0.5
real read-only evidence-loop artifacts.

It checks whether adaptive routing would under-route cases that R0.5 already
proved need `qualified` or `review` answer policy.

Allowed conclusion:

> Across the bounded R0.5 fixture set, adaptive route decisions did not
> under-route the known direct/qualified/review evidence outcomes.

Unsupported conclusions:

- production runtime validated
- live retrieval integrated
- route regret solved on real traffic
- reviewed truth or action readiness granted
"""


def limits_md() -> str:
    return """# Limits

- Uses three existing R0.5 runs, not production traffic.
- Uses local deterministic route logic, not an LLM or embedding router.
- Does not run new retrieval or answer generation.
- Does not prove live latency, production SLO, or route regret on real users.
- Does not create support, truth, review approval, promotion, or action basis.
"""


def write_bundle(output_dir: Path) -> dict[str, Any]:
    if output_dir.exists():
        raise FileExistsError(f"output_dir_exists:{output_dir}")
    output_dir.mkdir(parents=True)
    r0_7 = load_module(R0_7_ROUTER_PATH, "vaks_routing_robustness_r0_7")
    r0_8_source = R0_8_RUNNER_PATH.read_bytes()
    cases = load_r0_5_cases()
    hash_check = verify_r0_5_hashes(cases)
    decisions = build_regret_decisions(r0_7, cases)
    stress = route_regret_stress(r0_7, cases)
    failed = [row for row in decisions if row["status"] != "pass"]
    all_passed = hash_check["status"] == "pass" and stress["status"] == "pass" and not failed
    summary = {
        "status": "pass" if all_passed else "fail",
        "contract_version": CONTRACT_VERSION,
        "run_id": RUN_ID,
        "r0_5_case_count": len(cases),
        "r0_5_hash_check": hash_check,
        "route_regret_case_count": len(decisions),
        "route_regret_failed_count": len(failed),
        "stress_summary": stress,
        "runtime_gate": "route_regret_shadow_passed" if all_passed else "not_ready",
        "not_proven": NOT_PROVEN,
    }

    write_lf(output_dir / "CONTRACT.md", contract_md())
    write_lf(output_dir / "LIMITS.md", limits_md())
    write_jsonl(output_dir / "r0_5_evidence_cases.jsonl", cases)
    write_jsonl(output_dir / "route_regret_decisions.jsonl", decisions)
    write_lf(output_dir / "r0_5_hash_check.json", pretty_json(hash_check))
    write_lf(output_dir / "route_regret_stress_summary.json", pretty_json(stress))
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
        "r0_7_router_path": str(R0_7_ROUTER_PATH),
        "r0_7_router_sha256": sha256_bytes(R0_7_ROUTER_PATH.read_bytes()),
        "r0_8_runner_path": str(R0_8_RUNNER_PATH),
        "r0_8_runner_sha256": sha256_bytes(r0_8_source),
        "r0_5_dir": str(R0_5_DIR),
        "read_only": True,
        "shadow_only": True,
        "applied_to_runtime": False,
        "artifact_hashes": {},
    }
    manifest["artifact_hashes"] = collect_hashes(output_dir, exclude={"run_manifest.json"})
    write_lf(output_dir / "run_manifest.json", pretty_json(manifest))
    return summary


def verify_bundle(output_dir: Path) -> dict[str, Any]:
    required = [
        "CONTRACT.md",
        "LIMITS.md",
        "r0_5_evidence_cases.jsonl",
        "route_regret_decisions.jsonl",
        "r0_5_hash_check.json",
        "route_regret_stress_summary.json",
        "summary.json",
        "run_manifest.json",
        f"provenance/{Path(__file__).name}",
    ]
    missing = [path for path in required if not (output_dir / path).exists()]
    if missing:
        return {"status": "fail", "missing": missing}
    manifest = read_json(output_dir / "run_manifest.json")
    actual = collect_hashes(output_dir, exclude={"run_manifest.json"})
    hash_failures = [
        {"path": path, "expected": expected, "actual": actual.get(path)}
        for path, expected in manifest.get("artifact_hashes", {}).items()
        if actual.get(path) != expected
    ]
    extra_hashes = sorted(set(actual) - set(manifest.get("artifact_hashes", {})))
    summary = read_json(output_dir / "summary.json")
    decisions = read_jsonl(output_dir / "route_regret_decisions.jsonl")
    checks = {
        "manifest_hashes_match": not hash_failures and not extra_hashes,
        "summary_pass": summary.get("status") == "pass",
        "all_decisions_pass": all(row.get("status") == "pass" for row in decisions),
        "all_route_decisions_shadow_only": all(
            row["adaptive_route_decision"].get("shadow_only") is True
            and row["adaptive_route_decision"].get("applied_to_runtime") is False
            for row in decisions
        ),
        "no_route_regret": all(row["route_regret"].get("route_regret") is False for row in decisions),
        "runner_provenance_hash_matches": manifest.get("runner_sha256")
        == manifest.get("runner_provenance_sha256")
        == sha256_bytes((output_dir / f"provenance/{Path(__file__).name}").read_bytes()),
    }
    return {
        "status": "pass" if all(checks.values()) else "fail",
        "checks": checks,
        "hash_failures": hash_failures,
        "extra_hashes": extra_hashes,
    }


def append_only_self_test(output_dir: Path) -> dict[str, Any]:
    temp_root = Path(tempfile.mkdtemp(prefix="codex-r0-9-append-only-"))
    try:
        bundle = temp_root / "bundle"
        first = write_bundle(bundle)
        before = tree_hash(bundle)
        second_error = None
        try:
            write_bundle(bundle)
        except FileExistsError as exc:
            second_error = exc.__class__.__name__
        after = tree_hash(bundle)
        result = {
            "first_run_status": first["status"],
            "second_run_rejected": second_error == "FileExistsError",
            "second_run_error_class": second_error,
            "tree_hash_before_second_run": before,
            "tree_hash_after_second_run": after,
            "tree_hash_unchanged_after_rejected_second_run": before == after,
            "status": "pass"
            if first["status"] == "pass" and second_error == "FileExistsError" and before == after
            else "fail",
        }
    finally:
        resolved = temp_root.resolve()
        temp_base = Path(tempfile.gettempdir()).resolve()
        if str(resolved).lower().startswith(str(temp_base).lower()) and resolved.name.startswith("codex-r0-9-append-only-"):
            shutil.rmtree(resolved)
    write_lf(output_dir / "append_only_self_test.json", pretty_json(result))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    subparsers = parser.add_subparsers(dest="command", required=True)
    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--out", type=Path, default=DEFAULT_OUTPUT_DIR)
    run_parser.add_argument("--with-append-only-self-test", action="store_true")
    test_parser = subparsers.add_parser("self-test")
    test_parser.add_argument("output_dir", type=Path)
    args = parser.parse_args()

    try:
        if args.command == "run":
            summary = write_bundle(args.out)
            append_result = None
            if args.with_append_only_self_test:
                append_result = append_only_self_test(args.out)
                manifest_path = args.out / "run_manifest.json"
                manifest = read_json(manifest_path)
                manifest["artifact_hashes"] = collect_hashes(args.out, exclude={"run_manifest.json"})
                write_lf(manifest_path, pretty_json(manifest))
            print(
                json.dumps(
                    {
                        "status": summary["status"],
                        "run_id": RUN_ID,
                        "output_dir": str(args.out),
                        "runtime_gate": summary["runtime_gate"],
                        "route_regret_case_count": summary["route_regret_case_count"],
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
