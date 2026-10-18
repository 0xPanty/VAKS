#!/usr/bin/env python3
"""VAKS Runtime Launch Gate R0.11.

Sandbox-only launch gate for the current runtime evidence ladder.

It answers one narrow question:

- Can the current runtime slice be launched as shadow-only? yes, if R0.8/R0.9/R0.10 evidence passes.
- Can it be launched as production-control? no, because production-control blockers remain.

This tool does not run a server, does not expose an API, does not run retrieval
itself, and does not change truth/review/action state.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

CONTRACT_VERSION = "r0.11"
RUN_ID = "vaks-runtime-launch-gate-r0-11-2026-06-23"
DEFAULT_OUTPUT_DIR = Path("outputs/review") / RUN_ID

EVIDENCE = {
    "r0_8": {
        "dir": Path("outputs/review/vaks-runtime-shadow-pilot-r0-8-2026-06-23"),
        "zip": Path("outputs/review/vaks-runtime-shadow-pilot-r0-8-2026-06-23.zip"),
        "sha": Path("outputs/review/vaks-runtime-shadow-pilot-r0-8-2026-06-23.zip.sha256"),
        "summary": "summary.json",
        "self_test": ["python", "-X", "utf8", "-B", "tools/vaks_runtime_shadow_pilot_r0_8.py", "self-test"],
        "required_gate": "shadow_runtime_pilot_candidate",
    },
    "r0_9": {
        "dir": Path("outputs/review/vaks-runtime-route-regret-shadow-r0-9-2026-06-23"),
        "zip": Path("outputs/review/vaks-runtime-route-regret-shadow-r0-9-2026-06-23.zip"),
        "sha": Path("outputs/review/vaks-runtime-route-regret-shadow-r0-9-2026-06-23.zip.sha256"),
        "summary": "summary.json",
        "self_test": ["python", "-X", "utf8", "-B", "tools/vaks_runtime_route_regret_r0_9.py", "self-test"],
        "required_gate": "route_regret_shadow_passed",
    },
    "r0_10": {
        "dir": Path("outputs/review/vaks-runtime-live-wiring-shadow-r0-10-2026-06-23"),
        "zip": Path("outputs/review/vaks-runtime-live-wiring-shadow-r0-10-2026-06-23.zip"),
        "sha": Path("outputs/review/vaks-runtime-live-wiring-shadow-r0-10-2026-06-23.zip.sha256"),
        "summary": "summary.json",
        "self_test": ["python", "-X", "utf8", "-B", "tools/vaks_runtime_live_wiring_shadow_r0_10.py", "self-test"],
        "required_gate": "live_wiring_shadow_passed",
    },
}

PRODUCTION_BLOCKERS = [
    "no_real_traffic_route_regret_dataset",
    "no_production_latency_slo_evidence",
    "no_production_control_runtime_wiring",
    "no_vector_graph_hybrid_retrieval_validation",
    "no_live_llm_tool_runtime_validation",
    "no_reviewed_truth_or_action_readiness_authority",
]


def pretty_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def stable_json(data: Any) -> str:
    return json.dumps(data, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def write_lf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(text.encode("utf-8"))


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


def verify_zip_hash(zip_path: Path, sha_path: Path) -> dict[str, Any]:
    if not zip_path.exists() or not sha_path.exists():
        return {"status": "fail", "reason": "missing_zip_or_sha", "zip": str(zip_path), "sha": str(sha_path)}
    actual = sha256_bytes(zip_path.read_bytes())
    expected = sha_path.read_text(encoding="ascii").strip().split()[0]
    return {
        "status": "pass" if actual == expected else "fail",
        "actual": actual,
        "expected": expected,
        "match": actual == expected,
    }


def run_self_test(command: list[str], output_dir: Path) -> dict[str, Any]:
    result = subprocess.run([*command, str(output_dir)], text=True, capture_output=True)
    stdout = result.stdout.strip()
    parsed: Any
    try:
        parsed = json.loads(stdout) if stdout else None
    except json.JSONDecodeError:
        parsed = stdout
    return {
        "status": "pass" if result.returncode == 0 and isinstance(parsed, dict) and parsed.get("status") == "pass" else "fail",
        "returncode": result.returncode,
        "stdout": parsed,
        "stderr_tail": result.stderr[-1000:],
    }


def assess_evidence() -> dict[str, Any]:
    rows: dict[str, Any] = {}
    for key, info in EVIDENCE.items():
        output_dir = info["dir"]
        summary_path = output_dir / info["summary"]
        summary = read_json(summary_path) if summary_path.exists() else {"status": "missing"}
        self_test = run_self_test(info["self_test"], output_dir)
        zip_hash = verify_zip_hash(info["zip"], info["sha"])
        gate_ok = summary.get("runtime_gate") == info["required_gate"]
        rows[key] = {
            "output_dir": str(output_dir),
            "summary_status": summary.get("status"),
            "runtime_gate": summary.get("runtime_gate"),
            "required_gate": info["required_gate"],
            "runtime_gate_ok": gate_ok,
            "self_test": self_test,
            "zip_hash": zip_hash,
            "status": "pass"
            if summary.get("status") == "pass" and gate_ok and self_test["status"] == "pass" and zip_hash["status"] == "pass"
            else "fail",
        }
    return rows


def launch_decision(mode: str, evidence: dict[str, Any]) -> dict[str, Any]:
    evidence_passed = all(row["status"] == "pass" for row in evidence.values())
    if mode == "shadow-only":
        allowed = evidence_passed
        blockers: list[str] = [] if allowed else ["shadow_evidence_not_passing"]
    elif mode == "production-control":
        allowed = False
        blockers = PRODUCTION_BLOCKERS
    else:
        allowed = False
        blockers = [f"invalid_launch_mode:{mode}"]
    return {
        "mode": mode,
        "allowed": allowed,
        "status": "pass" if (mode == "shadow-only" and allowed) or (mode == "production-control" and not allowed) else "fail",
        "blockers": blockers,
        "does_not_grant": ["reviewed_truth", "reviewer_approval", "promotion", "action_readiness"],
    }


def contract_md() -> str:
    return """# VAKS Runtime Launch Gate R0.11

This package is the launch gate over R0.8, R0.9, and R0.10.

It allows only `shadow-only` runtime launch when all evidence packages pass.
It rejects `production-control` launch because production blockers remain.

It is not a service, API, runtime daemon, truth authority, reviewer, or action
approval system.
"""


def limits_md() -> str:
    return """# Limits

- `shadow-only` means observe and record only; it must not alter the user-facing answer path.
- `production-control` is explicitly blocked.
- R0.11 checks evidence packages; it does not create new retrieval evidence.
- It does not prove production latency, real traffic route regret, vector/graph/hybrid retrieval, reviewed truth, or action readiness.
"""


def write_bundle(output_dir: Path) -> dict[str, Any]:
    if not output_dir.is_absolute():
        output_dir = Path.cwd() / output_dir
    output_dir = output_dir.resolve()
    if output_dir.exists():
        raise FileExistsError(f"output_dir_exists:{output_dir}")
    output_dir.mkdir(parents=True)

    evidence = assess_evidence()
    decisions = [
        launch_decision("shadow-only", evidence),
        launch_decision("production-control", evidence),
    ]
    summary = {
        "status": "pass" if all(row["status"] == "pass" for row in evidence.values()) and all(d["status"] == "pass" for d in decisions) else "fail",
        "contract_version": CONTRACT_VERSION,
        "run_id": RUN_ID,
        "shadow_only_launch": next(d for d in decisions if d["mode"] == "shadow-only"),
        "production_control_launch": next(d for d in decisions if d["mode"] == "production-control"),
        "evidence_statuses": {key: row["status"] for key, row in evidence.items()},
        "not_proven": PRODUCTION_BLOCKERS,
    }

    write_lf(output_dir / "CONTRACT.md", contract_md())
    write_lf(output_dir / "LIMITS.md", limits_md())
    write_lf(output_dir / "evidence_checks.json", pretty_json(evidence))
    write_lf(output_dir / "launch_decisions.json", pretty_json(decisions))
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
        "shadow_only_allowed": summary["shadow_only_launch"]["allowed"],
        "production_control_allowed": summary["production_control_launch"]["allowed"],
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
        "evidence_checks.json",
        "launch_decisions.json",
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
    checks = {
        "manifest_hashes_match": not hash_failures and not extra_hashes,
        "summary_pass": summary.get("status") == "pass",
        "shadow_only_allowed": summary.get("shadow_only_launch", {}).get("allowed") is True,
        "production_control_blocked": summary.get("production_control_launch", {}).get("allowed") is False,
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
    temp_parent = Path.cwd() / "outputs" / "review"
    temp_root = Path(tempfile.mkdtemp(prefix="codex-r0-11-append-only-", dir=temp_parent))
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
        temp_base = (Path.cwd() / "outputs" / "review").resolve()
        if str(resolved).lower().startswith(str(temp_base).lower()) and resolved.name.startswith("codex-r0-11-append-only-"):
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
                append_result = append_only_self_test((Path.cwd() / args.out).resolve() if not args.out.is_absolute() else args.out)
                manifest_path = ((Path.cwd() / args.out).resolve() if not args.out.is_absolute() else args.out.resolve()) / "run_manifest.json"
                manifest = read_json(manifest_path)
                manifest["artifact_hashes"] = collect_hashes(manifest_path.parent, exclude={"run_manifest.json"})
                write_lf(manifest_path, pretty_json(manifest))
            print(json.dumps({"status": summary["status"], "run_id": RUN_ID, "output_dir": str(args.out), "shadow_only_allowed": summary["shadow_only_launch"]["allowed"], "production_control_allowed": summary["production_control_launch"]["allowed"], "append_only_self_test": append_result["status"] if append_result else "not_run"}, ensure_ascii=False, sort_keys=True))
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
