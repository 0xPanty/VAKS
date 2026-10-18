from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path


SLICE_ID = "2026-06-16-p2-60-user-decision-index-freeze-checksum-sandbox"
SOURCE_SLICE_IDS = [
    "2026-06-16-p2-51-user-decision-request-packet-sandbox",
    "2026-06-16-p2-52-user-decision-no-auto-advance-guard-sandbox",
    "2026-06-16-p2-53-user-response-classifier-dry-run-sandbox",
    "2026-06-16-p2-54-safe-user-response-renderer-dry-run-sandbox",
    "2026-06-16-p2-55-user-decision-e2e-dry-run-simulator-sandbox",
    "2026-06-16-p2-56-user-decision-demo-transcript-smoke-runner-sandbox",
    "2026-06-16-p2-57-user-decision-chain-regression-bundle-sandbox",
    "2026-06-16-p2-58-user-decision-static-boundary-scan-regression-sandbox",
    "2026-06-16-p2-59-user-decision-operator-handoff-index-sandbox",
]

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
ARTIFACT = ROOT / "artifact"
MANIFEST_PATH = ARTIFACT / "user_decision_index_freeze_checksum_manifest.json"
READOUT_PATH = ARTIFACT / "user_decision_index_freeze_checksum_readout.md"
PROTOTYPE_PATH = ARTIFACT / "user_decision_index_freeze_checksum_prototype.html"

LATEST_SOURCE_ROOT = SANDBOX_ROOT / "2026-06-16-p2-59-user-decision-operator-handoff-index-sandbox"
LATEST_SOURCE_STATUS_PATHS = [
    LATEST_SOURCE_ROOT / "verification.md",
    LATEST_SOURCE_ROOT / "reviewer-report.md",
    LATEST_SOURCE_ROOT / "boundary-audit.md",
    LATEST_SOURCE_ROOT / "product-acceptance-report.md",
    LATEST_SOURCE_ROOT / "next-step.md",
]

MUST_NOT = [
    "execute_option",
    "merge_mainline",
    "promote",
    "sync_obsidian",
    "commit",
    "push",
    "install_dependencies",
    "start_background_service",
    "install_hooks",
    "use_mcp_write_tool",
    "write_reviewed_knowledge",
    "create_evidence_support",
    "create_action_basis",
    "start_future_slice_by_inference",
]

REQUIRED_ROOT_FILES = [
    "slice-plan.md",
    "source-map.md",
    "verification.md",
    "reviewer-report.md",
    "boundary-audit.md",
    "product-acceptance-report.md",
    "next-step.md",
]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def frontmatter_status(path: Path) -> str:
    for line in read_text(path).splitlines():
        if line.lower().startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def tracked_files_for_slice(slice_id: str) -> list[Path]:
    root = SANDBOX_ROOT / slice_id
    files: list[Path] = []
    for name in REQUIRED_ROOT_FILES:
        files.append(root / name)
    for folder in ["artifact", "fixtures", "failure-cases"]:
        base = root / folder
        if base.exists():
            files.extend(path for path in sorted(base.rglob("*")) if path.is_file())
    return sorted(files)


def read_latest_source_status() -> dict:
    verification = LATEST_SOURCE_ROOT / "verification.md"
    reviewer = LATEST_SOURCE_ROOT / "reviewer-report.md"
    boundary = LATEST_SOURCE_ROOT / "boundary-audit.md"
    product = LATEST_SOURCE_ROOT / "product-acceptance-report.md"
    next_step = LATEST_SOURCE_ROOT / "next-step.md"
    payload: dict = {
        "status_method": "read_existing_reports_no_script_execution",
        "status_paths": [path.relative_to(WORKSPACE).as_posix() for path in LATEST_SOURCE_STATUS_PATHS],
        "verification_status": frontmatter_status(verification),
        "reviewer_passed": "REVIEW_PASS_NO_BLOCKER" in read_text(reviewer),
        "boundary_passed": "PASS_BOUNDARY" in read_text(boundary),
        "product_acceptance_passed": "PASS_PRODUCT_GRADE" in read_text(product),
        "next_step_status": frontmatter_status(next_step),
    }
    payload["passed"] = (
        payload["verification_status"] == "local_verification_passed"
        and payload["reviewer_passed"] is True
        and payload["boundary_passed"] is True
        and payload["product_acceptance_passed"] is True
        and payload["next_step_status"] == "pass_product_grade_pending_next_slice"
    )
    return payload


def build_manifest() -> dict:
    entries = []
    missing = []
    for slice_id in SOURCE_SLICE_IDS:
        for path in tracked_files_for_slice(slice_id):
            relative = path.relative_to(WORKSPACE).as_posix()
            if not path.exists():
                missing.append(relative)
                continue
            entries.append(
                {
                    "path": relative,
                    "source_slice_id": slice_id,
                    "sha256": sha256_file(path),
                    "bytes": path.stat().st_size,
                }
            )
    latest_status = read_latest_source_status()
    return {
        "record_kind": "sandbox_user_decision_index_freeze_checksum_manifest",
        "slice_id": SLICE_ID,
        "source_slice_ids": SOURCE_SLICE_IDS,
        "truth_boundary": "checksum_freeze_not_user_decision_or_execution_authority",
        "hash_algorithm": "sha256_bytes",
        "entry_count": len(entries),
        "missing_count": len(missing),
        "missing_paths": missing,
        "entries": entries,
        "latest_source_status_method": latest_status["status_method"],
        "latest_source_status_paths": latest_status["status_paths"],
        "latest_source_final_gate_passed": latest_status.get("passed") is True,
        "latest_source_recorded_status": latest_status,
        "freeze_ready": len(missing) == 0 and latest_status.get("passed") is True,
        "automatic_execution": False,
        "mainline_ready": False,
        "promotion_ready": False,
        "action_basis_ready": False,
        "must_not": MUST_NOT,
        "required_non_claims": [
            "This checksum manifest is not a user decision.",
            "This checksum manifest is not execution authority.",
            "This checksum manifest is not mainline approval.",
            "This checksum manifest is not promotion approval.",
            "This checksum manifest is not Obsidian sync approval.",
            "This checksum manifest is not reviewed knowledge.",
            "This checksum manifest is not evidence support.",
            "This checksum manifest is not action basis.",
        ],
    }


def render_markdown(manifest: dict) -> str:
    by_slice: dict[str, int] = {}
    for entry in manifest["entries"]:
        by_slice[entry["source_slice_id"]] = by_slice.get(entry["source_slice_id"], 0) + 1
    lines = [
        "# User Decision Index Freeze Checksum",
        "",
        "Sandbox-only checksum freeze. It detects drift in p2-51 through p2-59 user-decision guard artifacts. It is not a user decision, execution authority, mainline approval, promotion approval, Obsidian sync approval, reviewed knowledge, evidence support, or action basis.",
        "",
        f"- hash algorithm: `{manifest['hash_algorithm']}`",
        f"- source slice count: `{len(manifest['source_slice_ids'])}`",
        f"- entry count: `{manifest['entry_count']}`",
        f"- missing count: `{manifest['missing_count']}`",
        f"- latest source final gate passed: `{manifest['latest_source_final_gate_passed']}`",
        f"- freeze ready: `{manifest['freeze_ready']}`",
        "",
        "| Source slice | Frozen files |",
        "| --- | --- |",
    ]
    for slice_id in manifest["source_slice_ids"]:
        lines.append(f"| `{slice_id}` | `{by_slice.get(slice_id, 0)}` |")
    lines.extend(["", "## must_not", ""])
    lines.extend(f"- `{item}`" for item in manifest["must_not"])
    return "\n".join(lines)


def render_html(manifest: dict) -> str:
    by_slice: dict[str, int] = {}
    for entry in manifest["entries"]:
        by_slice[entry["source_slice_id"]] = by_slice.get(entry["source_slice_id"], 0) + 1
    rows = "".join(
        f"<tr><td>{slice_id}</td><td>{by_slice.get(slice_id, 0)}</td></tr>"
        for slice_id in manifest["source_slice_ids"]
    )
    must_not = "".join(f"<li>{item}</li>" for item in manifest["must_not"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>User Decision Index Freeze Checksum</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }}
    main {{ max-width: 1080px; margin: 0 auto; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #d1d5db; padding: 8px; text-align: left; }}
    th {{ background: #e5e7eb; }}
  </style>
</head>
<body>
<main>
  <h1>User Decision Index Freeze Checksum</h1>
  <p>Sandbox-only checksum freeze. Not a user decision, execution authority, mainline approval, promotion approval, reviewed knowledge, evidence support, or action basis.</p>
  <p><strong>Freeze ready:</strong> {manifest['freeze_ready']}<br><strong>Entry count:</strong> {manifest['entry_count']}<br><strong>Latest gate passed:</strong> {manifest['latest_source_final_gate_passed']}</p>
  <table><thead><tr><th>Source slice</th><th>Frozen files</th></tr></thead><tbody>{rows}</tbody></table>
  <section><h2>must_not</h2><ul>{must_not}</ul></section>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    manifest = build_manifest()
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    READOUT_PATH.write_text(render_markdown(manifest) + "\n", encoding="utf-8")
    PROTOTYPE_PATH.write_text(render_html(manifest), encoding="utf-8")
    print(
        json.dumps(
            {
                "freeze_ready": manifest["freeze_ready"],
                "entry_count": manifest["entry_count"],
                "missing_count": manifest["missing_count"],
                "latest_source_final_gate_passed": manifest["latest_source_final_gate_passed"],
                "manifest": str(MANIFEST_PATH),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if manifest["freeze_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
