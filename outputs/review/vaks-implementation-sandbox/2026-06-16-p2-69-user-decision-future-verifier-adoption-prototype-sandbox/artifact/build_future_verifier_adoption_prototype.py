from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True


SLICE_ID = "2026-06-16-p2-69-user-decision-future-verifier-adoption-prototype-sandbox"
SOURCE_SLICE_ID = "2026-06-16-p2-68-user-decision-strict-status-adoption-screen-sandbox"
PACKAGE_SLICE_ID = "2026-06-16-p2-67-user-decision-strict-status-package-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
SOURCE_ROOT = SANDBOX_ROOT / SOURCE_SLICE_ID
PACKAGE_ROOT = SANDBOX_ROOT / PACKAGE_SLICE_ID
PACKAGE_PATH = PACKAGE_ROOT / "artifact" / "strict_status_package.py"
ARTIFACT = ROOT / "artifact"

OUTPUT_JSON = ARTIFACT / "future_verifier_adoption_prototype.json"
OUTPUT_MD = ARTIFACT / "future_verifier_adoption_prototype.md"
OUTPUT_HTML = ARTIFACT / "future_verifier_adoption_prototype.html"

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
    "do_not_edit_tools",
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


def load_package():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package", PACKAGE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-67 strict status package")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def source_statuses() -> dict:
    package = load_package()
    result = {}
    for name, path in SOURCE_REPORTS.items():
        parsed = package.parse_strict_frontmatter_status(read_text(path))
        expected = EXPECTED_SOURCE_STATUSES[name]
        result[name] = {
            "path": relative(path),
            "valid": parsed["valid"],
            "status": parsed["status"],
            "expected_status": expected,
            "matches_expected": parsed["valid"] is True and parsed["status"] == expected,
        }
    return result


def package_self_check() -> dict:
    package = load_package()
    package_api_available = callable(getattr(package, "parse_strict_frontmatter_status", None)) and callable(
        getattr(package, "status_matches", None)
    )
    if not package_api_available:
        return {
            "package_path": relative(PACKAGE_PATH),
            "package_exists": PACKAGE_PATH.exists(),
            "uses_package_slice": PACKAGE_SLICE_ID in relative(PACKAGE_PATH),
            "package_api_available": False,
            "body_override_preserved": False,
            "missing_frontmatter_rejected": False,
            "status_matches_positive": False,
        }
    body_override = "---\nstatus: product_acceptance_pending\n---\n\nstatus: pass_product_grade\nPASS_PRODUCT_GRADE"
    missing = "status: pass_product_grade\nBody."
    return {
        "package_path": relative(PACKAGE_PATH),
        "package_exists": PACKAGE_PATH.exists(),
        "uses_package_slice": PACKAGE_SLICE_ID in relative(PACKAGE_PATH),
        "package_api_available": package_api_available,
        "body_override_preserved": package.parse_strict_frontmatter_status(body_override)["status"] == "product_acceptance_pending",
        "missing_frontmatter_rejected": package.parse_strict_frontmatter_status(missing)["valid"] is False,
        "status_matches_positive": package.status_matches("---\nstatus: pass_boundary\n---\n", "pass_boundary") is True,
    }


def build_prototype() -> dict:
    statuses = source_statuses()
    package_check = package_self_check()
    prototype_ready = all(item["matches_expected"] for item in statuses.values()) and all(
        value is True for key, value in package_check.items() if key != "package_path"
    )
    return {
        "record_kind": "sandbox_future_verifier_adoption_prototype",
        "slice_id": SLICE_ID,
        "source_slice_id": SOURCE_SLICE_ID,
        "package_slice_id": PACKAGE_SLICE_ID,
        "purpose": "prototype strict status package adoption in a future new sandbox verifier",
        "prototype_ready": prototype_ready,
        "adoption_contract": {
            "package_source": relative(PACKAGE_PATH),
            "adoption_scope": "future new sandbox verifier only",
            "old_slice_backfill": False,
            "package_only_adoption": False,
            "shared_helper_created": False,
            "tools_edited": False,
            "mainline_edited": False,
            "verifier_uses_package_api": True,
        },
        "source_statuses": statuses,
        "package_self_check": package_check,
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
        "# Future Verifier Adoption Prototype",
        "",
        "Sandbox-only prototype showing how a future new verifier can use the p2-67 strict status package.",
        "",
        f"- prototype ready: `{payload['prototype_ready']}`",
        f"- package source: `{payload['adoption_contract']['package_source']}`",
        f"- adoption scope: `{payload['adoption_contract']['adoption_scope']}`",
        "",
        "## Package Self Check",
        "",
    ]
    lines.extend(f"- `{key}`: `{value}`" for key, value in payload["package_self_check"].items())
    lines.extend(["", "## Hard No", ""])
    lines.extend(f"- `{item}`" for item in payload["hard_no"])
    return "\n".join(lines)


def render_html(payload: dict) -> str:
    checks = "".join(f"<li>{key}: {value}</li>" for key, value in payload["package_self_check"].items())
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Future Verifier Adoption Prototype</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }}
    main {{ max-width: 980px; margin: 0 auto; }}
  </style>
</head>
<body>
<main>
  <h1>Future Verifier Adoption Prototype</h1>
  <p>Sandbox-only prototype. It does not approve old-slice edits, shared helper edits, tools edits, merge, promotion, sync, reviewed knowledge, evidence support, action basis, or user approval.</p>
  <p><strong>Prototype ready:</strong> {payload['prototype_ready']}</p>
  <ul>{checks}</ul>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    payload = build_prototype()
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(payload) + "\n", encoding="utf-8")
    OUTPUT_HTML.write_text(render_html(payload), encoding="utf-8")
    print(
        json.dumps(
            {
                "prototype_ready": payload["prototype_ready"],
                "package_slice_id": payload["package_slice_id"],
                "package_source": payload["adoption_contract"]["package_source"],
                "audit": str(OUTPUT_JSON),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if payload["prototype_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
