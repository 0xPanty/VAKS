#!/usr/bin/env python3
"""VAKS Runtime Live Wiring Shadow R0.10.

Sandbox-only bridge that runs:

RouteDecision -> live R0.5 local lexical evidence loop -> route-regret check.

It reuses the bounded R0.5 runner in an isolated output subdirectory. It does
not run production services, vector/graph retrieval, LLM generation, writes,
truth promotion, or action readiness.
"""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

CONTRACT_VERSION = "r0.10"
RUN_ID = "vaks-runtime-live-wiring-shadow-r0-10-2026-06-23"
DEFAULT_OUTPUT_DIR = Path("outputs/review") / RUN_ID

R0_5_RUNNER = Path("tools/run_source_intake_real_readonly_evidence_loop_r0_5.py")
R0_7_ROUTER = Path("tools/vaks_routing_robustness.py")
R0_9_REGRET = Path("tools/vaks_runtime_route_regret_r0_9.py")

NOT_PROVEN = [
    "production_control_runtime",
    "production_latency_slo",
    "vector_graph_hybrid_retrieval",
    "live_llm_tool_runtime",
    "reviewed_truth",
    "reviewer_approval",
    "action_readiness",
]


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


def contract_md() -> str:
    return """# VAKS Runtime Live Wiring Shadow R0.10

This sandbox connects adaptive routing to a live rerun of the R0.5 local
Markdown lexical evidence loop.

It proves only that the bounded route -> R0.5 evidence-loop wiring can run in
an isolated sandbox and preserve the known direct / qualified / review answer
policies without route regret.

It does not prove production runtime, vector/graph/hybrid retrieval, reviewed
truth, reviewer approval, or action readiness.
"""


def limits_md() -> str:
    return """# Limits

- Local Markdown lexical retrieval only.
- Uses the existing R0.5 deterministic claim plans.
- Does not call an LLM, vector store, graph retriever, service, API, or DB.
- Does not write truth, reviewed knowledge, Obsidian state, or action state.
- Route regret is tested on the three bounded R0.5 runs, not real traffic.
"""


def run_live_wiring(output_dir: Path) -> dict[str, Any]:
    r0_5 = load_module(R0_5_RUNNER, "r0_5_live_shadow")
    r0_7 = load_module(R0_7_ROUTER, "r0_7_live_shadow")
    r0_9 = load_module(R0_9_REGRET, "r0_9_live_shadow")

    live_dir = output_dir / "live_r0_5_rerun"
    r0_5.OUT_DIR = live_dir
    r0_5.RUNS_DIR = live_dir / "runs"
    r0_5.RUNS_DIR.mkdir(parents=True, exist_ok=True)

    now = datetime.now(timezone.utc).isoformat(timespec="seconds")
    corpus = r0_5.base.collect_corpus()
    snapshot_hash = r0_5.corpus_snapshot_hash(corpus)

    route_rows: list[dict[str, Any]] = []
    run_rows: list[dict[str, Any]] = []
    failures: list[dict[str, Any]] = []

    for plan in r0_5.RUN_PLANS:
        context = r0_9.r0_5_run_context(plan.run_id, plan.expected_answer_policy)
        route_input = r0_9.route_case(
            plan.run_id,
            plan.query,
            context["query_mode"],
            context["intended_use"],
            context["risk_level"],
            context["assurance_floor"],
        )
        decision = r0_7.build_shadow_route_decision(route_input)
        route_rows.append(
            {
                "run_id": plan.run_id,
                "query": plan.query,
                "route_input_features": route_input["inferred_query_features"],
                "route_decision": decision,
                "route_context": context,
            }
        )
        run_summary = r0_5.run_one(plan, corpus, snapshot_hash, now)
        run_rows.append(run_summary)
        regret = r0_9.classify_regret(r0_7, {
            "run_id": plan.run_id,
            "answer_policy": run_summary["answer_policy"],
            "context": context,
        }, decision)
        checks = {
            "route_ok": decision.get("run_state") == "ok",
            "route_shadow_only": decision.get("shadow_only") is True and decision.get("applied_to_runtime") is False,
            "expected_answer_policy_met": run_summary.get("expected_answer_policy_met") is True,
            "no_route_regret": regret["route_regret"] is False,
        }
        if not all(checks.values()):
            failures.append({"run_id": plan.run_id, "checks": checks, "decision": decision, "run_summary": run_summary, "regret": regret})
        route_rows[-1]["live_answer_policy"] = run_summary["answer_policy"]
        route_rows[-1]["live_sufficiency_result"] = run_summary["sufficiency_result"]
        route_rows[-1]["route_regret"] = regret
        route_rows[-1]["checks"] = checks
        route_rows[-1]["status"] = "pass" if all(checks.values()) else "fail"

    completion = r0_5.validate_completion(run_rows)
    r0_5.write_json(live_dir / "r0_5_summary.json", completion)
    r0_5.write_top_level_docs(completion)

    return {
        "status": "pass" if completion["status"] == "pass" and not failures else "fail",
        "route_rows": route_rows,
        "run_rows": run_rows,
        "completion": completion,
        "failure_count": len(failures),
        "first_failures": failures[:5],
        "live_dir": live_dir,
    }


def write_bundle(output_dir: Path) -> dict[str, Any]:
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    output_dir = output_dir.resolve()
    if output_dir.exists():
        raise FileExistsError(f"output_dir_exists:{output_dir}")
    output_dir.mkdir(parents=True)
    result = run_live_wiring(output_dir)
    summary = {
        "status": result["status"],
        "contract_version": CONTRACT_VERSION,
        "run_id": RUN_ID,
        "live_r0_5_run_count": len(result["run_rows"]),
        "route_regret_failed_count": result["failure_count"],
        "r0_5_completion_status": result["completion"]["status"],
        "runtime_gate": "live_wiring_shadow_passed" if result["status"] == "pass" else "not_ready",
        "not_proven": NOT_PROVEN,
    }
    write_lf(output_dir / "CONTRACT.md", contract_md())
    write_lf(output_dir / "LIMITS.md", limits_md())
    write_jsonl(output_dir / "route_to_live_evidence_decisions.jsonl", result["route_rows"])
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
        "r0_5_runner_path": str(R0_5_RUNNER),
        "r0_5_runner_sha256": sha256_bytes(R0_5_RUNNER.read_bytes()),
        "r0_7_router_path": str(R0_7_ROUTER),
        "r0_7_router_sha256": sha256_bytes(R0_7_ROUTER.read_bytes()),
        "r0_9_runner_path": str(R0_9_REGRET),
        "r0_9_runner_sha256": sha256_bytes(R0_9_REGRET.read_bytes()),
        "read_only": True,
        "shadow_only": True,
        "applied_to_runtime": False,
        "artifact_hashes": {},
    }
    manifest["artifact_hashes"] = collect_hashes(output_dir, exclude={"run_manifest.json"})
    write_lf(output_dir / "run_manifest.json", pretty_json(manifest))
    return summary


def verify_bundle(output_dir: Path) -> dict[str, Any]:
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    output_dir = output_dir.resolve()
    required = [
        "CONTRACT.md",
        "LIMITS.md",
        "route_to_live_evidence_decisions.jsonl",
        "summary.json",
        "run_manifest.json",
        f"provenance/{Path(__file__).name}",
        "live_r0_5_rerun/r0_5_summary.json",
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
    decisions = [json.loads(line) for line in (output_dir / "route_to_live_evidence_decisions.jsonl").read_text(encoding="utf-8").splitlines() if line.strip()]
    checks = {
        "manifest_hashes_match": not hash_failures and not extra_hashes,
        "summary_pass": summary.get("status") == "pass",
        "live_r0_5_summary_pass": read_json(output_dir / "live_r0_5_rerun/r0_5_summary.json").get("status") == "pass",
        "all_route_rows_pass": all(row.get("status") == "pass" for row in decisions),
        "all_route_rows_shadow_only": all(
            row["route_decision"].get("shadow_only") is True and row["route_decision"].get("applied_to_runtime") is False
            for row in decisions
        ),
        "runner_provenance_hash_matches": manifest.get("runner_sha256")
        == manifest.get("runner_provenance_sha256")
        == sha256_bytes((output_dir / f"provenance/{Path(__file__).name}").read_bytes()),
    }
    return {"status": "pass" if all(checks.values()) else "fail", "checks": checks, "hash_failures": hash_failures, "extra_hashes": extra_hashes}


def append_only_self_test(output_dir: Path) -> dict[str, Any]:
    temp_parent = ROOT / "outputs" / "review"
    temp_root = Path(tempfile.mkdtemp(prefix="codex-r0-10-append-only-", dir=temp_parent))
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
            "tree_hash_unchanged_after_rejected_second_run": before == after,
            "status": "pass" if first["status"] == "pass" and second_error == "FileExistsError" and before == after else "fail",
        }
    finally:
        resolved = temp_root.resolve()
        temp_base = (ROOT / "outputs" / "review").resolve()
        if str(resolved).lower().startswith(str(temp_base).lower()) and resolved.name.startswith("codex-r0-10-append-only-"):
            shutil.rmtree(resolved)
    write_lf(output_dir / "append_only_self_test.json", pretty_json(result))
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
                append_result = append_only_self_test(args.out)
                manifest_path = args.out / "run_manifest.json"
                manifest = read_json(manifest_path)
                manifest["artifact_hashes"] = collect_hashes(args.out, exclude={"run_manifest.json"})
                write_lf(manifest_path, pretty_json(manifest))
            print(json.dumps({"status": summary["status"], "run_id": RUN_ID, "output_dir": str(args.out), "runtime_gate": summary["runtime_gate"], "append_only_self_test": append_result["status"] if append_result else "not_run"}, ensure_ascii=False, sort_keys=True))
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
