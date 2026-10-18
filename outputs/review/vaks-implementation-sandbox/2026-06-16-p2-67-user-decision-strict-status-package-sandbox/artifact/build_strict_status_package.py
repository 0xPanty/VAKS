from __future__ import annotations

import json
import sys
from pathlib import Path

from strict_status_package import parse_strict_frontmatter_status, status_matches


SLICE_ID = "2026-06-16-p2-67-user-decision-strict-status-package-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-66-user-decision-chain-hardening-readiness-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
SOURCE_ROOT = SANDBOX_ROOT / SOURCE_SLICE_ID
ARTIFACT = ROOT / "artifact"

OUTPUT_JSON = ARTIFACT / "strict_status_package_manifest.json"
OUTPUT_MD = ARTIFACT / "strict_status_package_manifest.md"
OUTPUT_HTML = ARTIFACT / "strict_status_package_manifest.html"

SOURCE_REPORTS = {
    "verification": SOURCE_ROOT / "verification.md",
    "reviewer": SOURCE_ROOT / "reviewer-report.md",
    "boundary": SOURCE_ROOT / "boundary-audit.md",
    "product": SOURCE_ROOT / "product-acceptance-report.md",
    "next_step": SOURCE_ROOT / "next-step.md",
}

EXPECTED_SOURCE_STATUSES = {
    "verification": "local_verification_passed",
    "reviewer": "review_pass_no_blocker",
    "boundary": "pass_boundary",
    "product": "pass_product_grade",
    "next_step": "pass_product_grade_pending_next_slice",
}

HARD_NO = [
    "do_not_modify_old_slices",
    "do_not_create_shared_helper",
    "do_not_merge_mainline",
    "do_not_promote",
    "do_not_sync_obsidian",
    "do_not_commit",
    "do_not_push",
    "do_not_install_dependencies",
    "do_not_start_background_service",
    "do_not_use_mcp_write_tool",
    "do_not_create_reviewed_knowledge",
    "do_not_create_evidence_support",
    "do_not_create_action_basis",
    "do_not_collect_user_approval_by_inference",
]


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def relative(path: Path) -> str:
    return path.relative_to(WORKSPACE).as_posix()


def source_statuses() -> dict:
    result = {}
    for name, path in SOURCE_REPORTS.items():
        parsed = parse_strict_frontmatter_status(read_text(path))
        expected = EXPECTED_SOURCE_STATUSES[name]
        result[name] = {
            "path": relative(path),
            "valid": parsed["valid"],
            "status": parsed["status"],
            "expected_status": expected,
            "matches_expected": parsed["valid"] is True and parsed["status"] == expected,
        }
    return result


def self_tests() -> dict:
    valid_doc = "---\nslice_id: sample\nstatus: pass_product_grade\n---\nBody."
    body_override_doc = "---\nslice_id: sample\nstatus: product_acceptance_pending\n---\nstatus: pass_product_grade\nPASS_PRODUCT_GRADE"
    duplicate_doc = "---\nstatus: one\nstatus: two\n---\nBody."
    missing_doc = "status: pass_product_grade\nBody."
    return {
        "valid_status_matches": status_matches(valid_doc, "pass_product_grade"),
        "body_override_does_not_match": not status_matches(body_override_doc, "pass_product_grade"),
        "body_override_preserves_frontmatter": parse_strict_frontmatter_status(body_override_doc)["status"] == "product_acceptance_pending",
        "duplicate_rejected": parse_strict_frontmatter_status(duplicate_doc)["valid"] is False,
        "missing_opening_rejected": parse_strict_frontmatter_status(missing_doc)["valid"] is False,
    }


def build_manifest() -> dict:
    statuses = source_statuses()
    tests = self_tests()
    ready = all(item["matches_expected"] for item in statuses.values()) and all(tests.values())
    return {
        "record_kind": "sandbox_strict_status_package_manifest",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "purpose": "package strict frontmatter status parsing for sandbox reuse",
        "package_ready": ready,
        "package_files": [
            "artifact/strict_status_package.py",
            "artifact/build_strict_status_package.py",
            "artifact/verify_strict_status_package.py",
            "artifact/strict_status_package_contract.json",
        ],
        "package_api": {
            "parse_strict_frontmatter_status": {
                "input": "markdown text",
                "output": "dict(valid, status, errors, body_status_mentions)",
                "authority": "parser result only; not reviewer or Product Acceptance",
            },
            "status_matches": {
                "input": "markdown text and expected status",
                "output": "bool",
                "authority": "status comparison only; not action approval",
            },
        },
        "behavior_contract": {
            "builder_writes_manifest_outputs": True,
            "builder_write_scope": relative(ARTIFACT),
            "verifier_read_only": True,
        },
        "source_statuses": statuses,
        "self_tests": tests,
        "readiness_flags": {
            "dependency_install_required": False,
            "network_required": False,
            "mcp_required": False,
            "background_service_required": False,
            "automatic_execution": False,
            "mainline_ready": False,
            "promotion_ready": False,
            "formal_vault_ready": False,
            "obsidian_sync_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "user_approval_collected": False,
        },
        "hard_no": HARD_NO,
    }


def render_markdown(payload: dict) -> str:
    lines = [
        "# Strict Status Package Manifest",
        "",
        "Sandbox-local package for strict frontmatter status parsing.",
        "",
        f"- package ready: `{payload['package_ready']}`",
        f"- source slice: `{payload['source_slice_id']}`",
        "",
        "## Package API",
        "",
    ]
    for name, spec in payload["package_api"].items():
        lines.extend([f"### `{name}`", "", f"- input: `{spec['input']}`", f"- output: `{spec['output']}`", f"- authority: {spec['authority']}", ""])
    lines.extend(["## Self Tests", ""])
    lines.extend(f"- `{name}`: `{value}`" for name, value in payload["self_tests"].items())
    lines.extend(["", "## Hard No", ""])
    lines.extend(f"- `{item}`" for item in payload["hard_no"])
    return "\n".join(lines)


def render_html(payload: dict) -> str:
    tests = "".join(f"<li>{name}: {value}</li>" for name, value in payload["self_tests"].items())
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Strict Status Package Manifest</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }}
    main {{ max-width: 980px; margin: 0 auto; }}
  </style>
</head>
<body>
<main>
  <h1>Strict Status Package Manifest</h1>
  <p>Sandbox-local package. It does not approve old-slice edits, shared helper edits, merge, promotion, sync, reviewed knowledge, evidence support, action basis, or user approval.</p>
  <p><strong>Package ready:</strong> {payload['package_ready']}</p>
  <h2>Self tests</h2>
  <ul>{tests}</ul>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    payload = build_manifest()
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(payload) + "\n", encoding="utf-8")
    OUTPUT_HTML.write_text(render_html(payload), encoding="utf-8")
    print(
        json.dumps(
            {
                "package_ready": payload["package_ready"],
                "source_slice_id": payload["source_slice_id"],
                "self_test_count": len(payload["self_tests"]),
                "audit": str(OUTPUT_JSON),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if payload["package_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
