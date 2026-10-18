from __future__ import annotations

import importlib.util
import json
import re
import sys
from collections import Counter
from pathlib import Path

sys.dont_write_bytecode = True


SLICE_ID = "2026-06-16-p2-70-product-grade-coverage-index-sandbox"
STRICT_PACKAGE_SLICE_ID = "2026-06-16-p2-67-user-decision-strict-status-package-sandbox"

ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
SANDBOX_ROOT = WORKSPACE / "outputs" / "review" / "vaks-implementation-sandbox"
PACKAGE_PATH = SANDBOX_ROOT / STRICT_PACKAGE_SLICE_ID / "artifact" / "strict_status_package.py"
ARTIFACT = ROOT / "artifact"

OUTPUT_JSON = ARTIFACT / "product_grade_coverage_index.json"
OUTPUT_MD = ARTIFACT / "product_grade_coverage_index.md"
OUTPUT_HTML = ARTIFACT / "product_grade_coverage_index.html"

REPORTS = {
    "verification": "verification.md",
    "reviewer": "reviewer-report.md",
    "boundary": "boundary-audit.md",
    "product": "product-acceptance-report.md",
    "next_step": "next-step.md",
}

PLAN_ITEMS = [
    ("P0-01", "retrieval receipt template sandbox"),
    ("P0-02", "operation receipt template sandbox"),
    ("P0-03", "body hash validator sandbox"),
    ("P0-04", "support boundary validator sandbox"),
    ("P0-05", "action readiness validator sandbox"),
    ("P0-06", "feedback validator sandbox"),
    ("P0-07", "action-boundary failure matrix"),
    ("P1-08", "retrieval/operation receipt validator pilot"),
    ("P1-09", "read-only query loop pilot"),
    ("P1-10", "runtime artifact exclusion test"),
    ("P1-11", "semantic anchor support check"),
    ("P1.5-12", "robust RAG retrieval sandbox"),
    ("P1.5-13", "local Obsidian graph retrieval read-only MCP sandbox"),
    ("P1.5-14", "raw intake parser router sandbox"),
    ("P1.5-15", "markdown validation/search sidecar sandbox"),
    ("P1.5-16", "MISA runtime memory / VAKS bridge sandbox"),
    ("P2-17", "use-surface optimization pass"),
    ("P2-18", "Bases cockpit prototype"),
    ("P2-19", "product experience screening sandbox"),
    ("P2-20", "product workflow prototype"),
]

CANONICAL = {
    "verification": "local_verification_passed",
    "reviewer": "review_pass_no_blocker",
    "boundary": "pass_boundary",
    "product": "pass_product_grade",
    "next_step": "pass_product_grade_pending_next_slice",
}


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8") if path.exists() else ""


def relative(path: Path) -> str:
    return path.relative_to(WORKSPACE).as_posix()


def load_package():
    sys.dont_write_bytecode = True
    spec = importlib.util.spec_from_file_location("p2_67_strict_status_package_for_coverage", PACKAGE_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load strict status package")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def plan_key_from_dir(name: str) -> str | None:
    match = re.search(r"-(p1-5|p0|p1|p2)-(\d+)-", name)
    if not match:
        return None
    tier = match.group(1).upper().replace("P1-5", "P1.5")
    number = int(match.group(2))
    return f"{tier}-{number:02d}"


def report_statuses(path: Path, package) -> dict:
    statuses = {}
    for report_name, filename in REPORTS.items():
        report_path = path / filename
        parsed = package.parse_strict_frontmatter_status(read_text(report_path))
        statuses[report_name] = {
            "path": relative(report_path),
            "exists": report_path.exists(),
            "valid_frontmatter": parsed.get("valid") is True,
            "status": parsed.get("status"),
            "canonical_expected": CANONICAL[report_name],
            "matches_canonical": parsed.get("valid") is True and parsed.get("status") == CANONICAL[report_name],
        }
    return statuses


def classify_slice(path: Path, package) -> dict:
    statuses = report_statuses(path, package)
    product_status = statuses["product"]["status"]
    next_status = statuses["next_step"]["status"]
    canonical_strict_pass = all(item["matches_canonical"] for item in statuses.values())
    legacy_pass_variant = isinstance(product_status, str) and product_status.startswith("pass_product_grade") and product_status != "pass_product_grade"
    product_frontmatter_pass = product_status == "pass_product_grade"
    pending_product = product_status in {"product_acceptance_pending", "pending_product_acceptance", None}
    pending_next = next_status not in {CANONICAL["next_step"]}
    return {
        "slice_id": path.name,
        "path": relative(path),
        "plan_key": plan_key_from_dir(path.name),
        "statuses": statuses,
        "classification": {
            "canonical_strict_pass": canonical_strict_pass,
            "product_frontmatter_pass": product_frontmatter_pass,
            "legacy_pass_variant": legacy_pass_variant,
            "pending_product": pending_product,
            "pending_next_step_closeout": pending_next,
            "needs_followup_before_current_strict_claim": not canonical_strict_pass,
        },
    }


def literal_hits() -> tuple[list[dict], int]:
    hits: list[dict] = []
    total_count = 0
    for directory in sorted(SANDBOX_ROOT.iterdir()):
        if not directory.is_dir() or directory.name == SLICE_ID:
            continue
        for subdir in ["artifact", "fixtures", "failure-cases"]:
            root = directory / subdir
            if not root.exists():
                continue
            for path in root.rglob("*"):
                if path.is_file() and path.suffix.lower() in {".py", ".json", ".md", ".html"}:
                    text = read_text(path)
                    count = text.count("PASS_PRODUCT_GRADE") + text.count("pass_product_grade")
                    if count:
                        total_count += count
                        if len(hits) < 200:
                            hits.append({"path": relative(path), "count": count, "counted_as_report_status": False})
    return hits, total_count


def build_index() -> dict:
    package = load_package()
    slices = [
        classify_slice(path, package)
        for path in sorted(SANDBOX_ROOT.iterdir())
        if path.is_dir() and path.name != SLICE_ID
    ]
    by_plan = {item["plan_key"]: item for item in slices if item["plan_key"]}
    planned_items = []
    for key, label in PLAN_ITEMS:
        item = by_plan.get(key)
        planned_items.append(
            {
                "plan_key": key,
                "label": label,
                "slice_id": item["slice_id"] if item else None,
                "found": item is not None,
                "canonical_strict_pass": item["classification"]["canonical_strict_pass"] if item else False,
                "product_frontmatter_pass": item["classification"]["product_frontmatter_pass"] if item else False,
                "legacy_pass_variant": item["classification"]["legacy_pass_variant"] if item else False,
                "pending_next_step_closeout": item["classification"]["pending_next_step_closeout"] if item else True,
            }
        )
    product_status_counts = Counter(item["statuses"]["product"]["status"] or "missing" for item in slices)
    current_strict_pass_count = sum(1 for item in slices if item["classification"]["canonical_strict_pass"])
    plan_current_strict_pass_count = sum(1 for item in planned_items if item["canonical_strict_pass"])
    hits, literal_count = literal_hits()
    return {
        "record_kind": "sandbox_product_grade_coverage_index",
        "slice_id": SLICE_ID,
        "strict_status_package": relative(PACKAGE_PATH),
        "parser_contract": {
            "status_source": "strict_yaml_frontmatter_only",
            "ignore_body_literals": True,
            "ignore_code_literals": True,
        },
        "rules": {
            "pending_product_counts_as_pass": False,
            "legacy_variants_count_as_canonical": False,
            "next_step_required_for_canonical": True,
            "reviewer_required_for_canonical": True,
            "boundary_required_for_canonical": True,
        },
        "authority_flags": {
            "mainline_ready": False,
            "promotion_ready": False,
            "reviewed_knowledge_ready": False,
            "evidence_support_ready": False,
            "action_basis_ready": False,
            "user_approval_collected": False,
        },
        "summary": {
            "slices_scanned": len(slices),
            "planned_items_total": len(PLAN_ITEMS),
            "planned_items_found": sum(1 for item in planned_items if item["found"]),
            "all_planned_items_found": all(item["found"] for item in planned_items),
            "all_planned_items_current_strict_pass": all(item["canonical_strict_pass"] for item in planned_items),
            "plan_current_strict_pass_count": plan_current_strict_pass_count,
            "current_strict_pass_count": current_strict_pass_count,
            "product_status_counts": dict(sorted(product_status_counts.items())),
            "literal_hit_files_sampled": len(hits),
            "literal_pass_token_count_not_counted": literal_count,
            "literal_scan_scope": "artifact/fixtures/failure-cases files with .py/.json/.md/.html extensions; sample retained at 25 rows in JSON output",
        },
        "planned_items": planned_items,
        "followup_items": [
            {
                "plan_key": item["plan_key"],
                "slice_id": item["slice_id"],
                "reason": "not current strict canonical pass",
                "product_frontmatter_pass": item["product_frontmatter_pass"],
                "legacy_pass_variant": item["legacy_pass_variant"],
                "pending_next_step_closeout": item["pending_next_step_closeout"],
            }
            for item in planned_items
            if not item["canonical_strict_pass"]
        ],
        "literal_hits_sample": hits[:25],
        "scanned_slices": slices,
    }


def render_markdown(payload: dict) -> str:
    summary = payload["summary"]
    lines = [
        "# Product Grade Coverage Index",
        "",
        "Sandbox-only coverage index. It reads report frontmatter statuses; code, fixture, and body literals are not acceptance.",
        "",
        "## Summary",
        "",
        f"- slices scanned: `{summary['slices_scanned']}`",
        f"- planned items found: `{summary['planned_items_found']}/{summary['planned_items_total']}`",
        f"- planned items current strict pass: `{summary['plan_current_strict_pass_count']}/{summary['planned_items_total']}`",
        f"- all planned items current strict pass: `{summary['all_planned_items_current_strict_pass']}`",
        f"- literal PASS token count ignored: `{summary['literal_pass_token_count_not_counted']}`",
        f"- literal hit files sampled: `{summary['literal_hit_files_sampled']}`",
        f"- literal scan scope: `{summary['literal_scan_scope']}`",
        "",
        "## Planned Items",
        "",
        "| Plan | Slice | Current strict pass | Product pass | Legacy pass variant | Pending next-step |",
        "|---|---|---:|---:|---:|---:|",
    ]
    for item in payload["planned_items"]:
        lines.append(
            f"| {item['plan_key']} | {item['slice_id'] or 'missing'} | {item['canonical_strict_pass']} | "
            f"{item['product_frontmatter_pass']} | {item['legacy_pass_variant']} | {item['pending_next_step_closeout']} |"
        )
    lines.extend(["", "## Boundary", ""])
    lines.append("This index is not mainline readiness, promotion approval, reviewed knowledge, evidence support, action basis, or user approval.")
    return "\n".join(lines) + "\n"


def render_html(payload: dict) -> str:
    rows = "\n".join(
        "<tr>"
        f"<td>{item['plan_key']}</td>"
        f"<td>{item['slice_id'] or 'missing'}</td>"
        f"<td>{item['canonical_strict_pass']}</td>"
        f"<td>{item['product_frontmatter_pass']}</td>"
        f"<td>{item['legacy_pass_variant']}</td>"
        f"<td>{item['pending_next_step_closeout']}</td>"
        "</tr>"
        for item in payload["planned_items"]
    )
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Product Grade Coverage Index</title>
  <style>
    body {{ font-family: Arial, sans-serif; color: #172033; background: #f7f7f4; margin: 24px; }}
    main {{ max-width: 1120px; margin: 0 auto; }}
    table {{ border-collapse: collapse; width: 100%; background: #ffffff; }}
    th, td {{ border: 1px solid #d4d7dd; padding: 8px; text-align: left; font-size: 14px; }}
    th {{ background: #eceff3; }}
  </style>
</head>
<body>
<main>
  <h1>Product Grade Coverage Index</h1>
  <p>Sandbox-only status index. Report frontmatter only; literals are ignored.</p>
  <table>
    <thead><tr><th>Plan</th><th>Slice</th><th>Strict pass</th><th>Product pass</th><th>Legacy variant</th><th>Pending next-step</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    payload = build_index()
    OUTPUT_JSON.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    OUTPUT_MD.write_text(render_markdown(payload), encoding="utf-8")
    OUTPUT_HTML.write_text(render_html(payload), encoding="utf-8")
    print(json.dumps(payload["summary"], ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
