from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path


SLICE_ID = "2026-06-19-p2-99-portable-opus-evidence-bundle-sandbox"
ROOT = Path(__file__).resolve().parents[5]
SLICE_DIR = ROOT / "outputs/review/vaks-implementation-sandbox" / SLICE_ID
ARTIFACT_DIR = SLICE_DIR / "artifact"
SNAPSHOT_DIR = ARTIFACT_DIR / "evidence-snapshots"
FIXTURES_DIR = SLICE_DIR / "fixtures"
FAILURE_DIR = SLICE_DIR / "failure-cases"

BUILD_SCRIPT = ARTIFACT_DIR / "build_portable_opus_evidence_bundle.py"
MANIFEST_JSON = ARTIFACT_DIR / "portable-opus-evidence-bundle-manifest.json"
README_MD = ARTIFACT_DIR / "portable-opus-evidence-bundle-readme.md"
FAILURES_JSON = FAILURE_DIR / "portable-opus-evidence-bundle-failures.json"


def load_build_module():
    spec = importlib.util.spec_from_file_location("p2_99_build", BUILD_SCRIPT)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load build module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def sha256_path(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def split_newline(line: str) -> tuple[str, str]:
    if line.endswith("\r\n"):
        return line[:-2], "\r\n"
    if line.endswith("\n"):
        return line[:-1], "\n"
    return line, ""


def read_status(path: Path) -> str:
    lines = path.read_text(encoding="utf-8").splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return ""
    for line in lines[1:]:
        if line.strip() == "---":
            break
        content, _newline = split_newline(line)
        if content.startswith("status:"):
            return content.split(":", 1)[1].strip()
    return ""


def check_no_cache_files() -> list[str]:
    failures = []
    for path in SLICE_DIR.rglob("*"):
        lowered = path.name.lower()
        if lowered == "__pycache__" or lowered.endswith(".pyc") or lowered.endswith(".tmp") or lowered.endswith(".log"):
            failures.append(f"cache_or_temp_file_present:{path.relative_to(SLICE_DIR)}")
    return failures


def verify(final_gate: bool) -> dict:
    failures: list[str] = []
    required_files = [
        SLICE_DIR / "slice-plan.md",
        SLICE_DIR / "source-map.md",
        SLICE_DIR / "verification.md",
        SLICE_DIR / "reviewer-report.md",
        SLICE_DIR / "boundary-audit.md",
        SLICE_DIR / "product-acceptance-report.md",
        SLICE_DIR / "next-step.md",
        BUILD_SCRIPT,
        Path(__file__),
        MANIFEST_JSON,
        README_MD,
        FAILURES_JSON,
    ]
    for path in required_files:
        if not path.exists():
            failures.append(f"missing_required_file:{path.relative_to(SLICE_DIR)}")

    if not failures:
        build_module = load_build_module()
        expected_sources = build_module.EVIDENCE_SOURCES
        manifest = load_json(MANIFEST_JSON)
        if manifest["summary"].get("snapshot_count") != len(expected_sources):
            failures.append("snapshot_count_mismatch")
        if len(manifest.get("evidence_items", [])) != len(expected_sources):
            failures.append("evidence_items_count_mismatch")
        for item in manifest.get("evidence_items", []):
            source_path = ROOT / item["source_path"]
            snapshot_path = ROOT / item["snapshot_path"]
            if not source_path.exists():
                failures.append(f"source_missing:{item['source_path']}")
                continue
            if not snapshot_path.exists():
                failures.append(f"snapshot_missing:{item['snapshot_path']}")
                continue
            source_hash = sha256_path(source_path)
            snapshot_hash = sha256_path(snapshot_path)
            if item["source_sha256"] != source_hash:
                failures.append(f"source_hash_stale:{item['source_path']}")
            if item["snapshot_sha256"] != snapshot_hash:
                failures.append(f"snapshot_hash_stale:{item['snapshot_path']}")
            if source_hash != snapshot_hash:
                failures.append(f"snapshot_source_hash_mismatch:{item['snapshot_name']}")

        expected_summary = {
            "bundle_ready": True,
            "snapshot_count": len(expected_sources),
            "hash_match_count": len(expected_sources),
            "dossier_ready": True,
            "guard_state": "STOP_WAIT_EXTERNAL_OPUS_REVIEW",
            "actual_opus_result_present": False,
            "opus_approval_claimed": False,
            "mainline_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "goal_complete_now": False,
        }
        for key, expected in expected_summary.items():
            actual = manifest["summary"].get(key)
            if actual != expected:
                failures.append(f"expected_summary_failed:{key}:expected={expected}:actual={actual}")

        fixture_expectations = {
            "snapshots-present-and-hash-matched.json": {"passed": True, "snapshot_count": len(expected_sources), "hash_match_count": len(expected_sources)},
            "dossier-and-guard-carried.json": {"passed": True, "dossier_ready": True, "guard_state": "STOP_WAIT_EXTERNAL_OPUS_REVIEW"},
            "no-opus-or-mainline-claim.json": {"passed": True, "actual_opus_result_present": False, "opus_approval_claimed": False, "mainline_ready": False, "goal_complete_now": False},
            "no-truth-action-authority.json": {"passed": True, "reviewed_knowledge_ready": False, "evidence_support_ready": False, "action_basis_ready": False},
            "source-paths-preserved.json": {"passed": True, "source_path_count": len(expected_sources)},
        }
        for filename, expected_values in fixture_expectations.items():
            path = FIXTURES_DIR / filename
            if not path.exists():
                failures.append(f"missing_fixture:{filename}")
                continue
            payload = load_json(path)
            for key, expected in expected_values.items():
                if payload.get(key) != expected:
                    failures.append(f"fixture_mismatch:{filename}:{key}:expected={expected}:actual={payload.get(key)}")

        failure_payload = load_json(FAILURES_JSON)
        if len(failure_payload.get("failure_cases", [])) != 8:
            failures.append("failure_case_count_not_8")

        readme_text = README_MD.read_text(encoding="utf-8")
        for needle in [
            "Portable Opus Evidence Bundle",
            "not an Opus result",
            "not Opus approval",
            "not mainline readiness",
            "not reviewed knowledge",
            "not evidence support",
            "not action basis",
            "SHA256",
            "later sandbox-only intake slice",
        ]:
            if needle not in readme_text:
                failures.append(f"missing_readme_text:{needle}")

    failures.extend(check_no_cache_files())

    if final_gate:
        expected_statuses = {
            "verification.md": "local_verification_passed",
            "reviewer-report.md": "review_pass_no_blocker",
            "boundary-audit.md": "pass_boundary",
            "product-acceptance-report.md": "pass_product_grade",
            "next-step.md": "pass_product_grade_pending_next_slice",
        }
        for filename, expected in expected_statuses.items():
            actual = read_status(SLICE_DIR / filename)
            if actual != expected:
                failures.append(f"final_gate_status:{filename}:expected={expected}:actual={actual}")

    summary = {}
    if MANIFEST_JSON.exists():
        manifest = load_json(MANIFEST_JSON)
        failure_case_count = len(load_json(FAILURES_JSON).get("failure_cases", [])) if FAILURES_JSON.exists() else 0
        summary = {
            "fixture_count": len(list(FIXTURES_DIR.glob("*.json"))),
            "failure_case_count": failure_case_count,
            "snapshot_count": manifest["summary"].get("snapshot_count"),
            "hash_match_count": manifest["summary"].get("hash_match_count"),
            "bundle_ready": manifest["summary"].get("bundle_ready"),
            "actual_opus_result_present": manifest["summary"].get("actual_opus_result_present"),
            "opus_approval_claimed": manifest["summary"].get("opus_approval_claimed"),
            "mainline_ready": manifest["summary"].get("mainline_ready"),
            "goal_complete_now": manifest["summary"].get("goal_complete_now"),
            "final_gate": final_gate,
        }

    return {"passed": not failures, "failures": failures, "summary": summary}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()
    result = verify(final_gate=args.final_gate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result["passed"] else 1)


if __name__ == "__main__":
    main()

