from __future__ import annotations

import argparse
import html.parser
import importlib.util
import json
import re
import sys
from pathlib import Path


SLICE_ID = "2026-06-15-p2-22-formalization-readiness-polish-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-21-silky-obsidian-workbench-sandbox"
REQUIRED_BOUNDARY_PHRASES = [
    "sandbox only",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "does not approve",
    "no sync",
    "no commit",
    "no push",
    "no promotion",
    "no formal vault write",
]
FORBIDDEN_OPERATIONS = [
    "formal_vault_write",
    "obsidian_sync",
    "commit",
    "push",
    "promotion",
    "dependency_install",
    "background_service",
    "mcp_write_tool",
    "hooks",
    "real_base_files",
    "production_ui",
]
REQUIRED_SURFACES = [
    "pilot_home",
    "first_run_script",
    "daily_operator_flow",
    "receipt_inspector",
    "triage_dirty_state_panel",
    "formalization_decision_matrix",
    "acceptance_gates",
    "boundary_faq",
    "reviewer_packet",
    "failure_messages",
    "formalization_readiness_packet",
    "rollout_backlog",
]
REQUIRED_DECISION_OPTIONS = [
    "static_html_cockpit",
    "obsidian_native_markdown_bases",
    "local_read_only_sidecar",
    "hybrid_pilot_path",
]
REQUIRED_ACCEPTANCE_GATES = [
    "first_run_under_5_minutes",
    "status_answered_in_2_clicks",
    "receipt_path_visible",
    "authority_confusion_blocked",
    "write_scope_clean",
    "reviewer_boundary_product_acceptance",
]
REQUIRED_SEARCH_TARGETS = [
    "where do I start",
    "formalization route",
    "receipt inspector",
    "dirty state",
    "missing anchor",
    "blocked reason",
    "boundary faq",
    "no formal vault write",
    "not action basis",
    "not evidence support",
    "PASS_PRODUCT_GRADE",
    "next sandbox route",
]
AUTHORITY_CONFUSING_PATTERNS = [
    "approved action",
    "approved for action",
    "action basis approved",
    "evidence supported",
    "reviewed truth",
    "merge approved",
    "sync approved",
    "promotion approved",
]


class ReadinessHTMLParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sandbox_only = False
        self.no_sync = False
        self.no_authority = False
        self.cards: list[dict[str, str]] = []
        self.roles: set[str] = set()
        self._in_script = False
        self.script_text = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: v or "" for k, v in attrs}
        if tag == "html":
            self.sandbox_only = attr.get("data-sandbox-only") == "true"
            self.no_sync = attr.get("data-no-sync") == "true"
            self.no_authority = attr.get("data-no-authority") == "true"
        if "data-role" in attr:
            self.roles.add(attr["data-role"])
        classes = attr.get("class", "").split()
        if tag == "article" and "card" in classes:
            self.cards.append(
                {
                    "surface": attr.get("data-surface", ""),
                    "search": attr.get("data-search", ""),
                }
            )
        if tag == "script" and attr.get("id") == "readiness-data":
            self._in_script = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self._in_script = False

    def handle_data(self, data: str) -> None:
        if self._in_script:
            self.script_text += data


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def sandbox_root() -> Path:
    return root().parent


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_builder() -> object:
    path = root() / "artifact" / "formalization_readiness_builder.py"
    spec = importlib.util.spec_from_file_location("formalization_readiness_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load builder: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def validate_config(cfg: dict) -> list[str]:
    errors: list[str] = []
    if cfg.get("slice_id") != SLICE_ID:
        errors.append("wrong_slice_id")
    if cfg.get("source_slice") != SOURCE_SLICE_ID:
        errors.append("wrong_source_slice")

    write_scope = cfg.get("write_scope", [])
    expected_scope = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"
    if write_scope != [expected_scope]:
        errors.append("invalid_write_scope")
    for scope in write_scope:
        normalized = scope.replace("\\", "/")
        if not normalized.startswith(expected_scope):
            errors.append("invalid_write_scope")
        if any(
            forbidden in normalized
            for forbidden in [
                "wiki/claims",
                "wiki/patterns",
                "wiki/decisions",
                "templates/",
                "tools/",
                "H:/Obsidian",
                "H:\\Obsidian",
            ]
        ):
            errors.append("invalid_write_scope")

    ops = cfg.get("operations", {})
    if ops.get("default_read_only") is not True:
        errors.append("default_not_read_only")
    if ops.get("rebuild_requires_explicit_flag") is not True:
        errors.append("rebuild_not_explicit")
    for op in FORBIDDEN_OPERATIONS:
        if ops.get(op) is not False:
            errors.append(f"forbidden_operation:{op}")

    phrases = cfg.get("boundary_phrases", [])
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase not in phrases:
            errors.append(f"missing_boundary_phrase:{phrase}")

    surfaces = cfg.get("surfaces", [])
    surface_ids = [item.get("id") for item in surfaces]
    for surface in REQUIRED_SURFACES:
        if surface not in surface_ids:
            errors.append(f"missing_surface:{surface}")
    if len(surfaces) < cfg.get("product_metrics", {}).get("required_surfaces", len(REQUIRED_SURFACES)):
        errors.append("too_few_surfaces")
    for surface in surfaces:
        text = " ".join(
            [
                surface.get("id", ""),
                surface.get("title", ""),
                surface.get("boundary", ""),
                " ".join(surface.get("answers", [])),
            ]
        ).lower()
        if any(pattern in text for pattern in AUTHORITY_CONFUSING_PATTERNS):
            errors.append("authority_confusing_label")

    decision_options = cfg.get("decision_options", [])
    decision_ids = [item.get("id") for item in decision_options]
    for option in REQUIRED_DECISION_OPTIONS:
        if option not in decision_ids:
            errors.append(f"missing_decision_option:{option}")
    if len(decision_options) < cfg.get("product_metrics", {}).get("required_decision_options", 4):
        errors.append("too_few_decision_options")
    for option in decision_options:
        option_id = option.get("id", "unknown")
        if option.get("requires_user_approval_for_formalization") is not True:
            errors.append(f"decision_option_without_user_approval:{option_id}")

    gate_ids = [item.get("id") for item in cfg.get("acceptance_gates", [])]
    for gate in REQUIRED_ACCEPTANCE_GATES:
        if gate not in gate_ids:
            errors.append(f"missing_acceptance_gate:{gate}")

    search_targets = cfg.get("search_targets", [])
    for target in REQUIRED_SEARCH_TARGETS:
        if target not in search_targets:
            errors.append(f"missing_search_target:{target}")

    metrics = cfg.get("product_metrics", {})
    if metrics.get("minimum_failure_cases", 0) < 18:
        errors.append("minimum_failure_cases_too_low")
    if metrics.get("first_run_max_steps", 99) > 3:
        errors.append("first_run_too_deep")

    max_steps = metrics.get("first_run_max_steps", 3)
    for journey in cfg.get("journeys", []):
        jid = journey.get("id", "unknown")
        if len(journey.get("steps", [])) > max_steps:
            errors.append(f"journey_too_deep:{jid}")
        if not journey.get("stop_condition"):
            errors.append(f"journey_missing_stop_condition:{jid}")
        if not journey.get("boundary_check"):
            errors.append(f"journey_missing_boundary_check:{jid}")
        expected = journey.get("expected_answer", "").lower()
        if expected and not any(
            phrase in expected
            for phrase in [
                "sandbox",
                "not",
                "cannot",
                "receipt",
                "requires separate user approval",
                "product acceptance",
            ]
        ):
            errors.append(f"journey_expected_answer_weak:{jid}")

    return sorted(set(errors))


def check_failure_cases() -> dict:
    failure_dir = root() / "failure-cases"
    oracle_path = root() / "artifact" / "failure-case-oracle.json"
    oracle = json.loads(oracle_path.read_text(encoding="utf-8"))
    mismatches = []
    for entry in oracle:
        path = failure_dir / entry["file"]
        if not path.exists():
            mismatches.append({"file": entry["file"], "missing": True})
            continue
        cfg = load_json(path)
        errors = validate_config(cfg)
        expected = entry["expected_failures"]
        missing_expected = [code for code in expected if code not in errors]
        if missing_expected:
            mismatches.append(
                {
                    "file": entry["file"],
                    "missing_expected": missing_expected,
                    "actual": errors,
                }
            )
    return {
        "count": len(oracle),
        "mismatches": mismatches,
    }


def resolve_markdown_link(page: Path, target: str) -> Path | None:
    if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
        return None
    clean = target.split("#", 1)[0].replace("%20", " ")
    if not clean:
        return None
    return (page.parent / clean).resolve()


def check_wikilinks(prototype: Path) -> list[str]:
    issues = []
    pages = {path.stem: path for path in prototype.glob("*.md")}
    pattern = re.compile(r"\[\[([^\]|#]+)")
    for page in prototype.glob("*.md"):
        text = page.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            target = match.group(1).strip()
            if target not in pages:
                issues.append(f"broken_wikilink:{page.name}->{target}")
    return issues


def check_markdown_links(prototype: Path) -> list[str]:
    issues = []
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for page in prototype.glob("*.md"):
        text = page.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            resolved = resolve_markdown_link(page, match.group(1))
            if resolved is None:
                continue
            if not resolved.exists():
                issues.append(f"broken_markdown_link:{page.name}->{match.group(1)}")
    return issues


def check_prototype(config: dict) -> dict:
    prototype = root() / "prototype" / "vaks-workbench-formalization-pilot"
    issues: list[str] = []
    required_pages = [
        "00 Pilot Home - VAKS Workbench.md",
        "10 First Run Script.md",
        "20 Daily Operator Flow.md",
        "25 Receipt Inspector.md",
        "30 Formalization Decision Matrix.md",
        "35 Triage and Dirty-State Panel.md",
        "40 Acceptance Gates.md",
        "50 Boundary FAQ.md",
        "55 Failure Messages.md",
        "60 Reviewer Packet.md",
        "65 Formalization Readiness Packet.md",
        "70 Product Rollout Backlog.md",
        "80 Pilot Test Results Template.md",
        "cockpit-readiness.html",
        "Receipts/formalization-readiness-receipt.json",
    ]
    for page in required_pages:
        if not (prototype / page).exists():
            issues.append(f"missing_prototype_file:{page}")

    for path in prototype.rglob("*"):
        rel = path.relative_to(prototype).as_posix()
        if path.suffix == ".base":
            issues.append(f"real_base_file_present:{rel}")
        if "__pycache__" in path.parts:
            issues.append(f"pycache_present:{rel}")

    if prototype.exists():
        issues.extend(check_wikilinks(prototype))
        issues.extend(check_markdown_links(prototype))

    all_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in prototype.rglob("*")
        if path.is_file() and path.suffix in {".md", ".html", ".json"}
    )
    lower = all_text.lower()
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase.lower() not in lower:
            issues.append(f"prototype_missing_boundary_phrase:{phrase}")
    for target in REQUIRED_SEARCH_TARGETS:
        if target.lower() not in lower:
            issues.append(f"prototype_missing_search_target:{target}")

    receipt_page = prototype / "25 Receipt Inspector.md"
    if receipt_page.exists():
        text = receipt_page.read_text(encoding="utf-8").lower()
        for required in [
            "artifact path",
            "source hash",
            "generation time",
            "does not show",
            "formalization readiness caveat",
            "not evidence support",
        ]:
            if required not in text:
                issues.append(f"receipt_inspector_missing:{required}")

    dirty_page = prototype / "35 Triage and Dirty-State Panel.md"
    if dirty_page.exists():
        text = dirty_page.read_text(encoding="utf-8").lower()
        for group in ["blocked", "stale", "dirty", "missing-anchor", "review_due", "action-risk"]:
            if group not in text:
                issues.append(f"dirty_panel_missing_group:{group}")
        if "state grouping is not approval" not in text:
            issues.append("dirty_panel_missing_boundary")

    failure_page = prototype / "55 Failure Messages.md"
    if failure_page.exists():
        text = failure_page.read_text(encoding="utf-8").lower()
        for term in ["plain reason", "safe alternative", "forbidden_operation", "authority_confusing_label"]:
            if term not in text:
                issues.append(f"failure_messages_missing:{term}")

    packet_page = prototype / "65 Formalization Readiness Packet.md"
    if packet_page.exists():
        text = packet_page.read_text(encoding="utf-8").lower()
        for required in [
            "proposed future touch scope",
            "must ask user",
            "test commands",
            "rollback",
            "still not mainline-ready",
            "residual verification-status",
        ]:
            if required not in text:
                issues.append(f"readiness_packet_missing:{required}")

    receipt_path = prototype / "Receipts" / "formalization-readiness-receipt.json"
    receipt = {}
    if receipt_path.exists():
        receipt = load_json(receipt_path)
        if receipt.get("slice_id") != SLICE_ID:
            issues.append("receipt_wrong_slice_id")
        if receipt.get("source_slice") != SOURCE_SLICE_ID:
            issues.append("receipt_wrong_source_slice")
        for op, value in receipt.get("forbidden_operations", {}).items():
            if value is not False:
                issues.append(f"receipt_forbidden_operation_true:{op}")
        for key, value in receipt.get("source_hashes", {}).items():
            if value == "missing":
                issues.append(f"receipt_missing_source_hash:{key}")

    html_path = prototype / "cockpit-readiness.html"
    html_summary = {}
    if html_path.exists():
        parser = ReadinessHTMLParser()
        parser.feed(html_path.read_text(encoding="utf-8"))
        html_summary = {
            "sandbox_only": parser.sandbox_only,
            "no_sync": parser.no_sync,
            "no_authority": parser.no_authority,
            "cards": len(parser.cards),
            "roles": sorted(parser.roles),
        }
        if not parser.sandbox_only:
            issues.append("html_missing_sandbox_marker")
        if not parser.no_sync:
            issues.append("html_missing_no_sync_marker")
        if not parser.no_authority:
            issues.append("html_missing_no_authority_marker")
        for role in [
            "surface-filter",
            "readiness-surfaces",
            "decision-options",
            "acceptance-gates",
            "boundary-rail",
        ]:
            if role not in parser.roles:
                issues.append(f"html_missing_role:{role}")
        if len(parser.cards) < len(REQUIRED_SURFACES):
            issues.append("html_too_few_cards")
        try:
            embedded = json.loads(parser.script_text)
            embedded_errors = validate_config(embedded)
            if embedded_errors:
                issues.append(f"html_embedded_config_invalid:{','.join(embedded_errors)}")
        except Exception as exc:  # pragma: no cover - surfaced in JSON output
            issues.append(f"html_embedded_config_unreadable:{exc}")
        searchable = "\n".join(card.get("search", "") for card in parser.cards).lower()
        for target in [
            "receipt inspector",
            "formalization decision matrix",
            "dirty",
            "no formal vault write",
            "not action basis",
        ]:
            if target not in searchable:
                issues.append(f"html_search_missing:{target}")

    return {
        "prototype_path": str(prototype),
        "issues": sorted(set(issues)),
        "html": html_summary,
        "receipt_keys": sorted(receipt.keys()) if receipt else [],
    }


def check_source_gate_caveat() -> dict:
    src = sandbox_root() / SOURCE_SLICE_ID
    verification = (src / "verification.md").read_text(encoding="utf-8")
    product = (src / "product-acceptance-report.md").read_text(encoding="utf-8")
    caveats = []
    if "pending_revalidation" in verification and "PASS_PRODUCT_GRADE" in product:
        caveats.append("source_verification_header_residual_pending_revalidation")
    handled_text = ""
    for path in [
        root() / "prototype" / "vaks-workbench-formalization-pilot" / "25 Receipt Inspector.md",
        root() / "prototype" / "vaks-workbench-formalization-pilot" / "65 Formalization Readiness Packet.md",
    ]:
        if path.exists():
            handled_text += "\n" + path.read_text(encoding="utf-8")
    handled = all(caveat in handled_text.replace("-", "_") for caveat in [])
    if caveats:
        handled = (
            "residual pending-revalidation" in handled_text.lower()
            or "residual verification-status" in handled_text.lower()
            or "formalization readiness caveat" in handled_text.lower()
        )
    return {
        "caveats": caveats,
        "handled_in_this_slice": handled,
        "issue": bool(caveats and not handled),
    }


def frontmatter_status(text: str) -> str:
    if not text.startswith("---\n"):
        return "missing_frontmatter"
    end = text.find("\n---", 4)
    if end == -1:
        return "missing_frontmatter_end"
    frontmatter = text[4:end].splitlines()
    for line in frontmatter:
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def check_required_reports(final_gate: bool = False) -> dict:
    statuses = {}
    issues = []
    text_by_name = {}
    for name in [
        "slice-plan.md",
        "source-map.md",
        "verification.md",
        "reviewer-report.md",
        "boundary-audit.md",
        "product-acceptance-report.md",
        "next-step.md",
    ]:
        path = root() / name
        if not path.exists():
            issues.append(f"missing_required_report:{name}")
            continue
        text = path.read_text(encoding="utf-8")
        text_by_name[name] = text
        statuses[name] = frontmatter_status(text)
    if final_gate:
        required_final = {
            "reviewer-report.md": "reviewer_pass",
            "boundary-audit.md": "boundary_pass",
            "product-acceptance-report.md": "pass_product_grade",
        }
        for name, expected_status in required_final.items():
            actual_status = statuses.get(name, "missing_status").lower()
            if actual_status != expected_status:
                issues.append(f"final_gate_bad_status:{name}:{actual_status}:expected:{expected_status}")
        next_status = statuses.get("next-step.md", "missing_status").lower()
        allowed_next_statuses = {
            "pass_product_grade_pending_user_mainline_decision",
            "pass_product_grade_pending_user_next_slice_decision",
        }
        if next_status not in allowed_next_statuses:
            issues.append(f"final_gate_bad_status:next-step.md:{next_status}:expected_one_of:{','.join(sorted(allowed_next_statuses))}")
    return {"statuses": statuses, "issues": issues}


def check_journey_results() -> dict:
    path = root() / "prototype" / "vaks-workbench-formalization-pilot" / "80 Pilot Test Results Template.md"
    issues = []
    metrics = {}
    if not path.exists():
        return {"metrics": metrics, "issues": ["missing_pilot_test_results"]}
    text = path.read_text(encoding="utf-8")
    required_rows = {
        "First run": ["Boundary FAQ", "PASS"],
        "Daily triage": ["state grouping is not approval", "PASS"],
        "Receipt lookup": ["P2-21 verification", "PASS"],
        "Decision route": ["hybrid_pilot_path", "PASS"],
        "Failure message": ["safe alternative", "PASS"],
    }
    for label, tokens in required_rows.items():
        if label not in text:
            issues.append(f"journey_result_missing:{label}")
            continue
        row_re = re.compile(rf"\|\s*{re.escape(label)}\s*\|([^\n]+)")
        match = row_re.search(text)
        row = match.group(0) if match else ""
        for token in tokens:
            if token not in row:
                issues.append(f"journey_result_weak:{label}:{token}")
    metric_patterns = {
        "time_to_first_correct_boundary_statement_seconds": 120,
        "time_to_find_receipt_path_seconds": 120,
        "time_to_compare_formalization_routes_seconds": 180,
        "max_links_to_boundary_faq": 3,
        "max_links_to_receipt_inspector": 2,
    }
    for key, max_value in metric_patterns.items():
        match = re.search(rf"{key}:\s*(\d+)", text)
        if not match:
            issues.append(f"journey_metric_missing:{key}")
            continue
        value = int(match.group(1))
        metrics[key] = value
        if value > max_value:
            issues.append(f"journey_metric_too_high:{key}")
    return {"metrics": metrics, "issues": issues}


def run(rebuild: bool = False, final_gate: bool = False) -> dict:
    if rebuild:
        builder = load_builder()
        builder.build()

    fixtures = [
        root() / "fixtures" / "valid-product-readiness-config.json",
        root() / "fixtures" / "valid-pilot-config-variant.json",
    ]
    fixture_results = []
    for fixture in fixtures:
        cfg = load_json(fixture)
        errors = validate_config(cfg)
        fixture_results.append({"file": fixture.name, "errors": errors})

    main_config = load_json(fixtures[0])
    failure_results = check_failure_cases()
    prototype_results = check_prototype(main_config)
    source_caveat = check_source_gate_caveat()
    report_results = check_required_reports(final_gate=final_gate)
    journey_results = check_journey_results()

    failures = []
    for item in fixture_results:
        if item["errors"]:
            failures.append(f"positive_fixture_failed:{item['file']}")
    if failure_results["mismatches"]:
        failures.append("failure_case_mismatch")
    if prototype_results["issues"]:
        failures.append("prototype_issues")
    if source_caveat["issue"]:
        failures.append("unhandled_source_gate_caveat")
    if report_results["issues"]:
        failures.append("required_report_missing")
    if journey_results["issues"]:
        failures.append("journey_results_missing_or_weak")

    return {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "rebuild": rebuild,
        "final_gate": final_gate,
        "passed": not failures,
        "failures": failures,
        "positive_fixtures": fixture_results,
        "failure_cases": failure_results,
        "prototype": prototype_results,
        "source_gate_caveat": source_caveat,
        "required_reports": report_results,
        "journey_results": journey_results,
        "non_claims": [
            "sandbox verification only",
            "not reviewed knowledge",
            "not evidence support",
            "not action basis",
            "not mainline approval",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true", help="Regenerate sandbox artifacts before validating.")
    parser.add_argument("--final-gate", action="store_true", help="Require Reviewer, Boundary, Product Acceptance, and next-step final statuses.")
    args = parser.parse_args()
    result = run(rebuild=args.rebuild, final_gate=args.final_gate)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
