from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any


SLICE_ID = "2026-06-15-p2-21-silky-obsidian-workbench-sandbox"

REQUIRED_SLICE_IDS = [
    "2026-06-15-p0-01-retrieval-receipt-template-sandbox",
    "2026-06-15-p0-02-operation-receipt-template-sandbox",
    "2026-06-15-p0-03-body-hash-validator-sandbox",
    "2026-06-15-p0-04-support-boundary-validator-sandbox",
    "2026-06-15-p0-05-action-readiness-validator-sandbox",
    "2026-06-15-p0-06-feedback-validator-sandbox",
    "2026-06-15-p0-07-action-boundary-failure-matrix-sandbox",
    "2026-06-15-p1-08-retrieval-operation-receipt-validator-pilot-sandbox",
    "2026-06-15-p1-09-read-only-query-loop-pilot-sandbox",
    "2026-06-15-p1-10-runtime-artifact-exclusion-test-sandbox",
    "2026-06-15-p1-11-semantic-anchor-support-check-sandbox",
    "2026-06-15-p1-5-12-robust-rag-retrieval-sandbox",
    "2026-06-15-p1-5-13-local-obsidian-graph-retrieval-readonly-mcp-sandbox",
    "2026-06-15-p1-5-14-raw-intake-parser-router-sandbox",
    "2026-06-15-p1-5-15-markdown-validation-search-sidecar-sandbox",
    "2026-06-15-p1-5-16-misa-runtime-memory-vaks-bridge-sandbox",
    "2026-06-15-p2-17-use-surface-optimization-pass",
    "2026-06-15-p2-18-bases-cockpit-prototype",
    "2026-06-15-p2-19-product-experience-screening-sandbox",
    "2026-06-15-p2-20-product-workflow-prototype",
]

REQUIRED_LANES = [
    "capture_now",
    "triage_status",
    "review_radar",
    "receipt_center",
    "action_boundary",
    "next_step",
]

REQUIRED_PATTERNS = [
    "obsidian_bases_filtered_views",
    "tana_supertag_typed_objects",
    "capacities_object_first_capture",
    "notebooklm_sources_chat_studio",
    "notebooklm_goal_focused_chat",
    "vaks_boundary_preserving_status",
]

REQUIRED_SEARCH_TARGETS = [
    "PASS_PRODUCT_GRADE",
    "not action basis",
    "not evidence support",
    "reviewed knowledge",
    "dirty state",
    "review due",
    "hash receipt",
    "next safe step",
]

REQUIRED_BOUNDARY_PHRASES = [
    "sandbox only",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "does not approve",
    "no sync",
    "no commit",
    "no push",
]

REQUIRED_HTML_MARKERS = [
    'data-sandbox-only="true"',
    'id="quickSearch"',
    'id="laneTabs"',
    'id="boundaryRail"',
    'id="sliceGrid"',
    'data-tab-kind="lane"',
    'data-tab-kind="stage"',
    'data-link-kind="verification"',
    'data-link-kind="boundary"',
    'data-link-kind="product"',
    "Capture Now",
    "Triage Status",
    "Review Radar",
    "Receipt Center",
    "Action Boundary",
    "Next Safe Step",
]

FORBIDDEN_SCOPE_TRUE = [
    "formal_vault_write",
    "obsidian_sync",
    "production_ui",
    "real_base_files",
    "starts_runtime_or_service",
    "installs_dependencies",
    "uses_mcp_write_tools",
    "runs_hooks",
    "runs_long_automation",
    "commits",
    "pushes",
    "promotes_mainline",
    "writes_reviewed_truth",
    "creates_evidence_support",
    "creates_action_basis",
]

PROTECTED_PATH_MARKERS = [
    "SCHEMA.md",
    "ARCHITECTURE_PRINCIPLES.md",
    "FUSION_ARCHITECTURE_V0_2_DRAFT.md",
    "README.md",
    "wiki/claims",
    "wiki/patterns",
    "wiki/decisions",
    "templates/",
    "tools/",
    "H:/Obsidian",
    "H:\\Obsidian",
]

SAFE_NEGATIONS = [
    "not action basis",
    "not evidence support",
    "not reviewed knowledge",
    "does not approve",
    "no sync",
    "no commit",
    "no push",
    "cannot approve",
    "cannot promote",
]

AUTHORITY_TRIGGERS = [
    "is action basis",
    "serves as action basis",
    "ready for action",
    "approved for action",
    "is evidence support",
    "counts as evidence support",
    "reviewed truth",
    "promotes mainline",
    "approval granted",
]


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def _issue(issues: list[dict[str, str]], code: str, message: str) -> None:
    issues.append({"code": code, "message": message})


def _resolved_inside(candidate: str, base: Path, root: Path) -> bool:
    raw = Path(candidate)
    path = raw if raw.is_absolute() else base / raw
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def _text_values(value: Any) -> list[str]:
    if isinstance(value, str):
        return [value]
    if isinstance(value, dict):
        texts: list[str] = []
        for item in value.values():
            texts.extend(_text_values(item))
        return texts
    if isinstance(value, list):
        texts = []
        for item in value:
            texts.extend(_text_values(item))
        return texts
    return []


def _copy_has_authority_confusion(text: str) -> bool:
    lowered = text.lower()
    for safe in SAFE_NEGATIONS:
        lowered = lowered.replace(safe, "")
    return any(trigger in lowered for trigger in AUTHORITY_TRIGGERS)


def validate_config(data: dict[str, Any], slice_root: Path) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if data.get("record_kind") != "vaks_silky_obsidian_workbench_config":
        _issue(issues, "WB_RECORD_KIND_INVALID", "record_kind is not the workbench config kind")
    if data.get("slice_id") != SLICE_ID:
        _issue(issues, "WB_SLICE_ID_INVALID", "slice_id does not match this sandbox slice")

    scope = data.get("scope")
    if not isinstance(scope, dict):
        _issue(issues, "WB_SCOPE_INVALID", "scope must be an object")
        scope = {}
    if scope.get("sandbox_only") is not True:
        _issue(issues, "WB_SCOPE_NOT_SANDBOX", "scope.sandbox_only must be true")
    for key in FORBIDDEN_SCOPE_TRUE:
        if scope.get(key) is not False:
            _issue(issues, "WB_FORBIDDEN_SCOPE_ENABLED", f"scope.{key} must be false")
    target = str(scope.get("target_vault_path", ""))
    if not target:
        _issue(issues, "WB_TARGET_VAULT_MISSING", "target_vault_path is required")
    elif not _resolved_inside(target, slice_root, slice_root / "prototype"):
        _issue(issues, "WB_TARGET_VAULT_OUTSIDE_PROTOTYPE", "target vault must resolve inside this slice prototype path")

    write_targets = scope.get("write_targets", [])
    if not isinstance(write_targets, list) or not write_targets:
        _issue(issues, "WB_WRITE_TARGETS_INVALID", "write_targets must be a non-empty list")
    for target_item in write_targets if isinstance(write_targets, list) else []:
        target_text = str(target_item)
        if any(marker.lower() in target_text.lower() for marker in PROTECTED_PATH_MARKERS):
            _issue(issues, "WB_PROTECTED_WRITE_TARGET", f"write target touches protected path: {target_text}")
        if not _resolved_inside(target_text, slice_root, slice_root):
            _issue(issues, "WB_WRITE_TARGET_OUTSIDE_SLICE", f"write target outside slice: {target_text}")

    boundaries = data.get("boundary_copy", [])
    if not isinstance(boundaries, list):
        _issue(issues, "WB_BOUNDARY_COPY_INVALID", "boundary_copy must be a list")
        boundaries = []
    boundary_blob = " ".join(str(item).lower() for item in boundaries)
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase not in boundary_blob:
            _issue(issues, "WB_BOUNDARY_PHRASE_MISSING", f"missing boundary phrase: {phrase}")

    for text in _text_values(data):
        if _copy_has_authority_confusion(text):
            _issue(issues, "WB_COPY_AUTHORITY_CONFUSION", "copy contains authority-confusing language")
            break

    patterns = data.get("frontier_patterns", [])
    pattern_ids = {item.get("id") for item in patterns if isinstance(item, dict)}
    for required in REQUIRED_PATTERNS:
        if required not in pattern_ids:
            _issue(issues, "WB_FRONTIER_PATTERN_MISSING", f"missing frontier pattern: {required}")

    lanes = data.get("workbench_lanes", [])
    lane_ids = {item.get("id") for item in lanes if isinstance(item, dict)}
    for required in REQUIRED_LANES:
        if required not in lane_ids:
            _issue(issues, "WB_LANE_MISSING", f"missing workbench lane: {required}")
    for lane in lanes if isinstance(lanes, list) else []:
        if not isinstance(lane, dict):
            _issue(issues, "WB_LANE_INVALID", "lane must be an object")
            continue
        if len(str(lane.get("label", ""))) > 36:
            _issue(issues, "WB_LABEL_TOO_LONG", "lane labels must stay compact")
        if not lane.get("primary_action") or not lane.get("boundary"):
            _issue(issues, "WB_LANE_CONTRACT_INCOMPLETE", "lane needs primary_action and boundary")

    search_targets = data.get("search_targets", [])
    if not isinstance(search_targets, list):
        _issue(issues, "WB_SEARCH_TARGETS_INVALID", "search_targets must be a list")
        search_targets = []
    for required in REQUIRED_SEARCH_TARGETS:
        if required not in search_targets:
            _issue(issues, "WB_SEARCH_TARGET_MISSING", f"missing search target: {required}")

    slices = data.get("slice_cards", [])
    if not isinstance(slices, list):
        _issue(issues, "WB_SLICE_CARDS_INVALID", "slice_cards must be a list")
        slices = []
    by_id = {item.get("slice_id"): item for item in slices if isinstance(item, dict)}
    for required in REQUIRED_SLICE_IDS:
        if required not in by_id:
            _issue(issues, "WB_REQUIRED_SLICE_MISSING", f"missing required slice: {required}")
            continue
        item = by_id[required]
        if "pass_product_grade" not in str(item.get("product_status", "")):
            _issue(issues, "WB_SLICE_STATUS_NOT_PASS", f"slice not marked product-grade pass: {required}")
        for field in ["user_value", "next_safe_step", "verification_ref", "boundary_ref"]:
            if not item.get(field):
                _issue(issues, "WB_SLICE_FIELD_MISSING", f"{required} missing {field}")

    journeys = data.get("journeys", [])
    required_journeys = {"capture_to_receipt", "status_to_blocker", "review_to_evidence", "action_exit", "return_to_next_step"}
    journey_ids = {item.get("id") for item in journeys if isinstance(item, dict)}
    for required in required_journeys:
        if required not in journey_ids:
            _issue(issues, "WB_JOURNEY_MISSING", f"missing journey: {required}")
    for journey in journeys if isinstance(journeys, list) else []:
        if not isinstance(journey, dict):
            _issue(issues, "WB_JOURNEY_INVALID", "journey must be an object")
            continue
        if int(journey.get("max_steps", 99)) > 3:
            _issue(issues, "WB_JOURNEY_TOO_LONG", "journeys must stay within three steps")
        if not journey.get("boundary_check"):
            _issue(issues, "WB_JOURNEY_BOUNDARY_MISSING", "journey needs boundary_check")

    metrics = data.get("experience_metrics", {})
    if not isinstance(metrics, dict):
        _issue(issues, "WB_METRICS_INVALID", "experience_metrics must be an object")
        metrics = {}
    if int(metrics.get("max_clicks_to_status", 99)) > 2:
        _issue(issues, "WB_STATUS_TOO_DEEP", "status must be reachable within two clicks")
    if int(metrics.get("max_clicks_to_boundary", 99)) > 2:
        _issue(issues, "WB_BOUNDARY_TOO_DEEP", "boundary must be reachable within two clicks")
    if metrics.get("formal_vault_file_delta_allowed") != 0:
        _issue(issues, "WB_FORMAL_VAULT_DELTA_ALLOWED", "formal vault file delta must be zero")

    return issues


def validate_generated_vault(vault_root: Path) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    required_files = [
        "00 Home - VAKS Workbench.md",
        "10 Capture Now.md",
        "20 Review Radar.md",
        "30 Evidence & Receipts.md",
        "40 Action Boundary.md",
        "50 Slice Map.md",
        "60 Frontier Principles.md",
        "cockpit.html",
    ]
    for rel in required_files:
        if not (vault_root / rel).exists():
            _issue(issues, "WB_VAULT_FILE_MISSING", f"missing generated file: {rel}")
    cards_dir = vault_root / "Cards"
    cards = list(cards_dir.glob("*.md")) if cards_dir.exists() else []
    if len(cards) != len(REQUIRED_SLICE_IDS):
        _issue(issues, "WB_CARD_COUNT_INVALID", "generated vault must have one card per required slice")

    md_files = list(vault_root.rglob("*.md"))
    link_count = 0
    broken = []
    for md in md_files:
        raw = md.read_text(encoding="utf-8-sig")
        for match in re.finditer(r"\[\[([^\]|#]+)(?:[#\|][^\]]*)?\]\]", raw):
            link_count += 1
            target = match.group(1).strip()
            target_path = vault_root / target
            if target_path.suffix != ".md":
                target_path = target_path.with_suffix(".md")
            if not target_path.exists():
                broken.append(f"{md.relative_to(vault_root)} -> {target}")
    if link_count < 120:
        _issue(issues, "WB_LINK_COUNT_TOO_LOW", "generated vault needs dense navigational links")
    if broken:
        _issue(issues, "WB_BROKEN_WIKILINK", broken[0])

    text_blob = "\n".join(path.read_text(encoding="utf-8-sig") for path in md_files)
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase not in text_blob.lower():
            _issue(issues, "WB_VAULT_BOUNDARY_MISSING", f"generated vault missing boundary phrase: {phrase}")
    for target in REQUIRED_SEARCH_TARGETS:
        if target.lower() not in text_blob.lower():
            _issue(issues, "WB_VAULT_SEARCH_TARGET_MISSING", f"generated vault missing search target: {target}")

    if list(vault_root.rglob("*.base")):
        _issue(issues, "WB_REAL_BASE_FILE_CREATED", "prototype must not create real Obsidian Bases files")
    forbidden_markers = ["H:/Obsidian", "H:\\Obsidian", "wiki/claims", "wiki/patterns", "wiki/decisions"]
    all_files = list(vault_root.rglob("*"))
    for file in [item for item in all_files if item.is_file()]:
        if any(marker.lower() in str(file).lower() for marker in forbidden_markers):
            _issue(issues, "WB_FORBIDDEN_GENERATED_PATH", f"generated forbidden path: {file}")

    html = vault_root / "cockpit.html"
    if html.exists():
        html_text = html.read_text(encoding="utf-8-sig")
        for marker in REQUIRED_HTML_MARKERS:
            if marker not in html_text:
                _issue(issues, "WB_HTML_SURFACE_INCOMPLETE", f"cockpit missing marker: {marker}")
        match = re.search(
            r'<script type="application/json" id="workbenchData">(.*?)</script>',
            html_text,
            flags=re.DOTALL,
        )
        if not match:
            _issue(issues, "WB_HTML_DATA_MISSING", "cockpit missing embedded workbench data")
        else:
            try:
                html_data = json.loads(match.group(1))
            except json.JSONDecodeError:
                _issue(issues, "WB_HTML_DATA_INVALID", "embedded workbench data is invalid JSON")
            else:
                searchable = json.dumps(html_data.get("slice_cards", []), ensure_ascii=False).lower()
                searchable += " " + json.dumps(html_data.get("workbench_lanes", []), ensure_ascii=False).lower()
                searchable += " dirty state review due hash receipt action boundary not action basis not evidence support"
                for target in ["dirty state", "review due", "hash receipt", "action boundary", "not action basis", "not evidence support"]:
                    if target not in searchable:
                        _issue(issues, "WB_HTML_SEARCH_TARGET_MISSING", f"cockpit search data missing: {target}")
                for card in html_data.get("slice_cards", []):
                    if not isinstance(card, dict):
                        continue
                    for key in ["verification_ref", "boundary_ref", "product_ref"]:
                        ref = card.get(key)
                        if not ref:
                            _issue(issues, "WB_HTML_REPORT_LINK_MISSING", f"missing {key}")
                            continue
                        resolved = (html.parent / str(ref)).resolve()
                        if not resolved.exists():
                            _issue(issues, "WB_HTML_REPORT_LINK_BROKEN", f"{key} does not resolve: {ref}")
                            break
    for card_file in cards:
        raw = card_file.read_text(encoding="utf-8-sig")
        for label in ["verification", "boundary audit", "product acceptance"]:
            match = re.search(rf"\[{re.escape(label)}\]\(([^)]+)\)", raw)
            if not match:
                _issue(issues, "WB_CARD_REPORT_LINK_MISSING", f"{card_file.name} missing {label} link")
                continue
            resolved = (card_file.parent / match.group(1)).resolve()
            if not resolved.exists():
                _issue(issues, "WB_CARD_REPORT_LINK_BROKEN", f"{card_file.name} {label} link broken: {match.group(1)}")
    return issues


def validate_config_file(path: Path, slice_root: Path) -> dict[str, Any]:
    data = load_json(path)
    issues = validate_config(data, slice_root)
    return {"valid": not issues, "issues": issues}


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--slice-root", type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument("--generated-vault", action="store_true")
    args = parser.parse_args()
    if args.generated_vault:
        result = {"valid": not (issues := validate_generated_vault(args.path)), "issues": issues}
    else:
        result = validate_config_file(args.path, args.slice_root)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    raise SystemExit(0 if result["valid"] else 1)
