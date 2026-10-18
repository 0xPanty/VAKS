from __future__ import annotations

import argparse
import html.parser
import importlib.util
import json
import re
import sys
from pathlib import Path


SLICE_ID = "2026-06-15-p2-23-native-markdown-entry-readonly-inspector-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-22-formalization-readiness-polish-sandbox"

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
    "local_storage_write",
    "network_post",
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
    "no promotion",
    "no formal vault write",
    "read-only inspector",
    "navigation is not authority",
]
REQUIRED_NATIVE_PAGES = [
    "native_home",
    "inbox",
    "status_board",
    "receipt_index",
    "boundary_stop",
    "readonly_inspector_guide",
    "next_safe_step",
    "dry_run_results",
]
REQUIRED_INSPECTOR_VIEWS = [
    "entry_map",
    "status_lanes",
    "receipt_lanes",
    "boundary_lanes",
]
REQUIRED_SEARCH_TARGETS = [
    "native markdown entry",
    "read-only inspector",
    "no formal vault write",
    "not evidence support",
    "not action basis",
    "navigation is not authority",
    "status grouping is not approval",
    "receipt proves process trail only",
    "next safe step",
]
AUTHORITY_CONFUSING_PATTERNS = [
    "approved action",
    "approved actions",
    "approves action basis",
    "action basis approved",
    "evidence supported",
    "reviewed truth",
    "merge approved",
    "sync approved",
    "promotion approved",
]


class InspectorParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sandbox_only = False
        self.read_only = False
        self.no_write = False
        self.no_sync = False
        self.no_authority = False
        self.roles: set[str] = set()
        self.cards: list[dict[str, str]] = []
        self.buttons: list[str] = []
        self.button_texts: list[str] = []
        self._current_button: str | None = None
        self.inputs: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.contenteditable = 0
        self.downloads = 0
        self.forms = 0
        self._in_script = False
        self.script_text = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: v or "" for k, v in attrs}
        if tag == "html":
            self.sandbox_only = attr.get("data-sandbox-only") == "true"
            self.read_only = attr.get("data-read-only-inspector") == "true"
            self.no_write = attr.get("data-no-write") == "true"
            self.no_sync = attr.get("data-no-sync") == "true"
            self.no_authority = attr.get("data-no-authority") == "true"
        if tag == "form":
            self.forms += 1
        if attr.get("contenteditable", "").lower() == "true":
            self.contenteditable += 1
        if tag == "a":
            self.anchors.append({"href": attr.get("href", ""), "download": attr.get("download", "")})
            if "download" in attr:
                self.downloads += 1
        if tag == "input":
            self.inputs.append({"id": attr.get("id", ""), "type": attr.get("type", ""), "name": attr.get("name", "")})
        if tag == "button":
            self.buttons.append(attr.get("data-filter", ""))
            self._current_button = ""
        if "data-role" in attr:
            self.roles.add(attr["data-role"])
        if tag == "article" and "card" in attr.get("class", "").split():
            self.cards.append({"kind": attr.get("data-kind", ""), "search": attr.get("data-search", "")})
        if tag == "script" and attr.get("id") == "inspector-data":
            self._in_script = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script":
            self._in_script = False
        if tag == "button" and self._current_button is not None:
            self.button_texts.append(self._current_button.strip())
            self._current_button = None

    def handle_data(self, data: str) -> None:
        if self._in_script:
            self.script_text += data
        if self._current_button is not None:
            self._current_button += data


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def sandbox_root() -> Path:
    return root().parent


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_builder() -> object:
    path = root() / "artifact" / "native_entry_readonly_inspector_builder.py"
    spec = importlib.util.spec_from_file_location("native_entry_readonly_inspector_builder", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Cannot load builder: {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def frontmatter_status(text: str) -> str:
    if not text.startswith("---\n"):
        return "missing_frontmatter"
    end = text.find("\n---", 4)
    if end == -1:
        return "missing_frontmatter_end"
    for line in text[4:end].splitlines():
        if line.startswith("status:"):
            return line.split(":", 1)[1].strip()
    return "missing_status"


def validate_config(cfg: dict) -> list[str]:
    errors: list[str] = []
    if cfg.get("slice_id") != SLICE_ID:
        errors.append("wrong_slice_id")
    if cfg.get("source_slice") != SOURCE_SLICE_ID:
        errors.append("wrong_source_slice")
    expected_scope = f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"
    if cfg.get("write_scope") != [expected_scope]:
        errors.append("invalid_write_scope")
    for scope in cfg.get("write_scope", []):
        normalized = scope.replace("\\", "/")
        if not normalized.startswith(expected_scope):
            errors.append("invalid_write_scope")
        if any(bad in normalized for bad in ["wiki/claims", "wiki/patterns", "wiki/decisions", "templates/", "tools/", "H:/Obsidian"]):
            errors.append("invalid_write_scope")

    ops = cfg.get("operations", {})
    if ops.get("default_read_only") is not True:
        errors.append("default_not_read_only")
    if ops.get("rebuild_requires_explicit_flag") is not True:
        errors.append("rebuild_not_explicit")
    for op in FORBIDDEN_OPERATIONS:
        if ops.get(op) is not False:
            errors.append(f"forbidden_operation:{op}")

    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase not in cfg.get("boundary_phrases", []):
            errors.append(f"missing_boundary_phrase:{phrase}")

    page_ids = [page.get("id") for page in cfg.get("native_entry_pages", [])]
    for page in REQUIRED_NATIVE_PAGES:
        if page not in page_ids:
            errors.append(f"missing_native_page:{page}")
    if len(page_ids) < cfg.get("product_metrics", {}).get("required_native_pages", 8):
        errors.append("too_few_native_pages")
    for page in cfg.get("native_entry_pages", []):
        text = " ".join([page.get("id", ""), page.get("title", ""), page.get("role", ""), " ".join(page.get("answers", []))]).lower()
        if any(pattern in text for pattern in AUTHORITY_CONFUSING_PATTERNS):
            errors.append("authority_confusing_text")

    view_ids = [view.get("id") for view in cfg.get("inspector_views", [])]
    for view in REQUIRED_INSPECTOR_VIEWS:
        if view not in view_ids:
            errors.append(f"missing_inspector_view:{view}")
    if len(view_ids) < cfg.get("product_metrics", {}).get("required_inspector_views", 4):
        errors.append("too_few_inspector_views")

    controls = cfg.get("inspector_controls", {})
    allowed_inputs = {("q", "search")}
    actual_inputs = {
        (item.get("id", ""), item.get("type", ""))
        for item in controls.get("inputs", [])
    }
    if actual_inputs != allowed_inputs:
        errors.append("inspector_inputs_not_allowlisted")
    allowed_buttons = {"all", "entry", "status_surface", "receipt_surface", "stop_surface"}
    actual_buttons = {
        item.get("filter", "")
        for item in controls.get("buttons", [])
    }
    for control in controls.get("buttons", []):
        label = control.get("label", "").strip().lower()
        filt = control.get("filter", "").strip().lower()
        if filt not in allowed_buttons:
            errors.append(f"inspector_control_not_allowed:button:{filt or label}")
        if label in {"save", "sync", "commit", "push", "write", "promote", "approve"}:
            errors.append(f"inspector_control_not_allowed:button:{label}")
    if actual_buttons != allowed_buttons:
        errors.append("inspector_buttons_not_allowlisted")

    max_steps = cfg.get("product_metrics", {}).get("max_first_run_steps", 3)
    for journey in cfg.get("journeys", []):
        jid = journey.get("id", "unknown")
        if len(journey.get("steps", [])) > max_steps:
            errors.append(f"journey_too_deep:{jid}")
        if not journey.get("stop_condition"):
            errors.append(f"journey_missing_stop_condition:{jid}")
        if not journey.get("boundary_check"):
            errors.append(f"journey_missing_boundary_check:{jid}")
        expected = journey.get("expected_answer", "").lower()
        if expected and not any(marker in expected for marker in ["sandbox", "receipt", "status", "inspector"]):
            errors.append(f"journey_expected_answer_weak:{jid}")

    metrics = cfg.get("dry_run_metrics", {})
    metric_limits = {
        "time_to_native_home_seconds": 60,
        "time_to_boundary_stop_seconds": 90,
        "time_to_receipt_index_seconds": 90,
        "time_to_confirm_readonly_inspector_seconds": 90,
        "max_links_to_boundary_stop": 2,
        "max_links_to_receipt_index": 2,
        "max_links_to_next_safe_step": 2,
    }
    for key, limit in metric_limits.items():
        value = metrics.get(key)
        if not isinstance(value, int):
            errors.append(f"dry_run_metric_missing:{key}")
        elif value > limit:
            errors.append(f"dry_run_metric_too_high:{key}")

    gates = set(cfg.get("acceptance_gates", []))
    for gate in [
        "native_home_exists",
        "all_wikilinks_resolve",
        "source_report_links_resolve",
        "read_only_inspector_has_no_write_controls",
        "frontmatter_final_gate_is_exact",
        "reviewer_boundary_product_acceptance_complete",
    ]:
        if gate not in gates:
            errors.append(f"missing_acceptance_gate:{gate}")

    for target in REQUIRED_SEARCH_TARGETS:
        if target not in cfg.get("search_targets", []):
            errors.append(f"missing_search_target:{target}")

    if cfg.get("product_metrics", {}).get("minimum_failure_cases", 0) < 22:
        errors.append("minimum_failure_cases_too_low")
    return sorted(set(errors))


def check_failure_cases() -> dict:
    oracle = load_json(root() / "artifact" / "failure-case-oracle.json")
    mismatches = []
    for entry in oracle:
        path = root() / "failure-cases" / entry["file"]
        if not path.exists():
            mismatches.append({"file": entry["file"], "missing": True})
            continue
        errors = validate_config(load_json(path))
        missing = [code for code in entry["expected_failures"] if code not in errors]
        if missing:
            mismatches.append({"file": entry["file"], "missing_expected": missing, "actual": errors})
    return {"count": len(oracle), "mismatches": mismatches}


def resolve_markdown_link(page: Path, target: str) -> Path | None:
    if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
        return None
    clean = target.split("#", 1)[0].replace("%20", " ")
    if not clean:
        return None
    return (page.parent / clean).resolve()


def check_wikilinks(vault: Path) -> list[str]:
    issues = []
    pages = {path.stem: path for path in vault.glob("*.md")}
    pattern = re.compile(r"\[\[([^\]|#]+)")
    for page in vault.glob("*.md"):
        text = page.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            target = match.group(1).strip()
            if target not in pages:
                issues.append(f"broken_wikilink:{page.name}->{target}")
    return issues


def check_markdown_links(vault: Path) -> list[str]:
    issues = []
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for page in vault.rglob("*.md"):
        text = page.read_text(encoding="utf-8")
        for match in pattern.finditer(text):
            target = resolve_markdown_link(page, match.group(1))
            if target is not None and not target.exists():
                issues.append(f"broken_markdown_link:{page.name}->{match.group(1)}")
    return issues


def page_links(page: Path) -> set[str]:
    text = page.read_text(encoding="utf-8")
    links = set()
    for match in re.finditer(r"\[\[([^\]|#]+)", text):
        links.add(match.group(1).strip())
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        links.add(match.group(1).strip())
    for filename in ["readonly-inspector.html", "Receipts/native-entry-readonly-inspector-receipt.json"]:
        if filename in text:
            links.add(filename)
    return links


def check_actual_journeys(vault: Path, html_ok: bool) -> dict:
    issues = []
    results = {}
    required_pages = {
        "home": vault / "00 Native Home.md",
        "status": vault / "02 Status Board.md",
        "receipt": vault / "03 Receipt Index.md",
        "boundary": vault / "04 Boundary Stop.md",
        "guide": vault / "05 Readonly Inspector Guide.md",
        "next": vault / "06 Next Safe Step.md",
    }
    for key, path in required_pages.items():
        if not path.exists():
            issues.append(f"journey_missing_page:{key}")
    if issues:
        return {"results": results, "issues": issues}

    home_links = page_links(required_pages["home"])
    status_links = page_links(required_pages["status"])
    receipt_links = page_links(required_pages["receipt"])
    boundary_links = page_links(required_pages["boundary"])
    guide_links = page_links(required_pages["guide"])

    native_first_run = "[[04 Boundary Stop]]" not in home_links and "04 Boundary Stop" not in home_links
    if native_first_run:
        issues.append("journey_path_missing:native_first_run:home_to_boundary")
    next_from_boundary = "[[06 Next Safe Step]]" not in boundary_links and "06 Next Safe Step" not in boundary_links
    if next_from_boundary:
        issues.append("journey_path_missing:native_first_run:boundary_to_next")
    results["native_first_run"] = {
        "path": ["00 Native Home", "04 Boundary Stop", "06 Next Safe Step"],
        "links_verified": not native_first_run and not next_from_boundary,
        "max_links": 2,
    }

    receipt_path_ok = ("03 Receipt Index" in home_links) and (
        "Receipts/native-entry-readonly-inspector-receipt.json" in receipt_links
    )
    if not receipt_path_ok:
        issues.append("journey_path_missing:receipt_lookup")
    results["receipt_lookup"] = {
        "path": ["00 Native Home", "03 Receipt Index", "receipt json"],
        "links_verified": receipt_path_ok,
        "max_links": 2,
    }

    status_stop_ok = ("04 Boundary Stop" in status_links) and ("06 Next Safe Step" in boundary_links)
    if not status_stop_ok:
        issues.append("journey_path_missing:status_to_stop")
    results["status_to_stop"] = {
        "path": ["02 Status Board", "04 Boundary Stop", "06 Next Safe Step"],
        "links_verified": status_stop_ok,
        "max_links": 2,
    }

    inspector_ok = ("readonly-inspector.html" in guide_links) and ("04 Boundary Stop" in guide_links) and html_ok
    if not inspector_ok:
        issues.append("journey_path_missing:inspector_check")
    results["inspector_check"] = {
        "path": ["05 Readonly Inspector Guide", "readonly-inspector.html", "04 Boundary Stop"],
        "links_verified": inspector_ok,
        "max_links": 2,
        "html_allowlist_ok": html_ok,
    }

    return {"results": results, "issues": issues}


def check_html(html_path: Path, cfg: dict) -> dict:
    issues = []
    summary = {}
    if not html_path.exists():
        return {"issues": ["missing_html_inspector"], "summary": summary}
    text = html_path.read_text(encoding="utf-8")
    parser = InspectorParser()
    parser.feed(text)
    summary = {
        "sandbox_only": parser.sandbox_only,
        "read_only": parser.read_only,
        "no_write": parser.no_write,
        "no_sync": parser.no_sync,
        "no_authority": parser.no_authority,
        "cards": len(parser.cards),
        "roles": sorted(parser.roles),
        "forms": parser.forms,
        "buttons": parser.buttons,
        "button_texts": parser.button_texts,
        "inputs": parser.inputs,
        "anchors": len(parser.anchors),
        "contenteditable": parser.contenteditable,
        "downloads": parser.downloads,
    }
    if not parser.sandbox_only:
        issues.append("html_missing_sandbox_marker")
    if not parser.read_only:
        issues.append("html_missing_readonly_marker")
    if not parser.no_write:
        issues.append("html_missing_no_write_marker")
    if not parser.no_sync:
        issues.append("html_missing_no_sync_marker")
    if not parser.no_authority:
        issues.append("html_missing_no_authority_marker")
    if parser.forms:
        issues.append("html_form_present")
    if parser.contenteditable:
        issues.append("html_contenteditable_present")
    if parser.downloads:
        issues.append("html_download_link_present")
    for anchor in parser.anchors:
        href = anchor.get("href", "").lower()
        if href.startswith(("http://", "https://", "mailto:", "javascript:")):
            issues.append(f"html_external_or_script_href:{href[:40]}")
    allowed_inputs = [{"id": "q", "type": "search", "name": ""}]
    normalized_inputs = [
        {"id": item.get("id", ""), "type": item.get("type", ""), "name": item.get("name", "")}
        for item in parser.inputs
    ]
    if normalized_inputs != allowed_inputs:
        issues.append("html_inputs_not_allowlisted")
    allowed_buttons = ["all", "entry", "status_surface", "receipt_surface", "stop_surface"]
    if parser.buttons != allowed_buttons:
        issues.append("html_buttons_not_allowlisted")
    for text_value in parser.button_texts:
        if text_value.strip().lower() in {"save", "sync", "commit", "push", "write", "promote", "approve"}:
            issues.append(f"html_write_button_present:{text_value.strip().lower()}")
    for role in ["readonly-filter", "native-entry-cards", "inspector-views", "boundary-rail"]:
        if role not in parser.roles:
            issues.append(f"html_missing_role:{role}")
    if len(parser.cards) < len(REQUIRED_NATIVE_PAGES):
        issues.append("html_too_few_cards")
    if re.search(r"\b(fetch|XMLHttpRequest|sendBeacon)\s*\(", text):
        issues.append("html_network_write_api_present")
    if re.search(r"\b(localStorage|sessionStorage)\s*\.", text):
        issues.append("html_storage_write_api_present")
    if re.search(r"\b(save|sync|write|commit|push|promote)\s*\(", text, flags=re.IGNORECASE):
        issues.append("html_write_like_function_present")
    try:
        embedded = json.loads(parser.script_text)
        if len(embedded.get("pages", [])) < len(REQUIRED_NATIVE_PAGES):
            issues.append("html_embedded_pages_missing")
        if len(embedded.get("views", [])) < len(REQUIRED_INSPECTOR_VIEWS):
            issues.append("html_embedded_views_missing")
    except Exception as exc:
        issues.append(f"html_embedded_data_invalid:{exc}")
    searchable = "\n".join(card.get("search", "") for card in parser.cards).lower() + "\n" + text.lower()
    for target in REQUIRED_SEARCH_TARGETS:
        if target.lower() not in searchable:
            issues.append(f"html_missing_search_target:{target}")
    return {"issues": sorted(set(issues)), "summary": summary}


def check_prototype(cfg: dict) -> dict:
    vault = root() / "prototype" / "vaks-native-entry-readonly-inspector"
    issues = []
    required_files = [
        "00 Native Home.md",
        "01 Inbox.md",
        "02 Status Board.md",
        "03 Receipt Index.md",
        "04 Boundary Stop.md",
        "05 Readonly Inspector Guide.md",
        "06 Next Safe Step.md",
        "07 Dry Run Results.md",
        "Cards/Source P2-22.md",
        "Cards/Native Entry Contract.md",
        "Cards/Readonly Inspector Contract.md",
        "Receipts/native-entry-readonly-inspector-receipt.json",
        "readonly-inspector.html",
    ]
    for file in required_files:
        if not (vault / file).exists():
            issues.append(f"missing_prototype_file:{file}")
    for path in vault.rglob("*"):
        rel = path.relative_to(vault).as_posix()
        if path.suffix == ".base":
            issues.append(f"real_base_file_present:{rel}")
        if path.name == ".obsidian":
            issues.append("obsidian_config_present")
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            issues.append(f"python_cache_present:{rel}")
    if vault.exists():
        issues.extend(check_wikilinks(vault))
        issues.extend(check_markdown_links(vault))
    all_text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in vault.rglob("*")
        if path.is_file() and path.suffix in {".md", ".html", ".json"}
    )
    lower = all_text.lower()
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase.lower() not in lower:
            issues.append(f"prototype_missing_boundary_phrase:{phrase}")
    for target in REQUIRED_SEARCH_TARGETS:
        if target.lower() not in lower:
            issues.append(f"prototype_missing_search_target:{target}")
    for pattern in AUTHORITY_CONFUSING_PATTERNS:
        if pattern in lower:
            # Failure-case fixtures may contain bad wording; prototype must not.
            issues.append(f"prototype_authority_confusing_text:{pattern}")
    dry = vault / "07 Dry Run Results.md"
    dry_metrics = {}
    if dry.exists():
        text = dry.read_text(encoding="utf-8")
        for key, max_value in {
            "time_to_native_home_seconds": 60,
            "time_to_boundary_stop_seconds": 90,
            "time_to_receipt_index_seconds": 90,
            "time_to_confirm_readonly_inspector_seconds": 90,
            "max_links_to_boundary_stop": 2,
            "max_links_to_receipt_index": 2,
            "max_links_to_next_safe_step": 2,
        }.items():
            match = re.search(rf"{key}:\s*(\d+)", text)
            if not match:
                issues.append(f"dry_run_metric_missing:{key}")
            else:
                value = int(match.group(1))
                dry_metrics[key] = value
                if value > max_value:
                    issues.append(f"dry_run_metric_too_high:{key}")
        for task in ["Native first run", "Receipt lookup", "Status to stop", "Inspector check"]:
            row = re.search(rf"\|\s*{re.escape(task)}\s*\|([^\n]+)", text)
            if not row or "PASS" not in row.group(0):
                issues.append(f"dry_run_task_missing_or_failed:{task}")
    receipt_path = vault / "Receipts" / "native-entry-readonly-inspector-receipt.json"
    receipt_summary = {}
    if receipt_path.exists():
        receipt = load_json(receipt_path)
        receipt_summary = {
            "slice_id": receipt.get("slice_id"),
            "source_slice": receipt.get("source_slice"),
            "source_hashes": len(receipt.get("source_hashes", {})),
        }
        if receipt.get("slice_id") != SLICE_ID:
            issues.append("receipt_wrong_slice_id")
        if receipt.get("source_slice") != SOURCE_SLICE_ID:
            issues.append("receipt_wrong_source_slice")
        forbidden_receipt = receipt.get("forbidden_operations", {})
        for op in FORBIDDEN_OPERATIONS:
            if op not in forbidden_receipt:
                issues.append(f"receipt_missing_forbidden_operation:{op}")
        for op, value in forbidden_receipt.items():
            if value is not False:
                issues.append(f"receipt_forbidden_operation_true:{op}")
        for key, value in receipt.get("source_hashes", {}).items():
            if value == "missing":
                issues.append(f"receipt_missing_source_hash:{key}")
    html_result = check_html(vault / "readonly-inspector.html", cfg)
    issues.extend(html_result["issues"])
    journey_result = check_actual_journeys(vault, html_ok=not html_result["issues"])
    issues.extend(journey_result["issues"])
    return {
        "prototype_path": str(vault),
        "issues": sorted(set(issues)),
        "dry_run_metrics": dry_metrics,
        "actual_journeys": journey_result["results"],
        "receipt": receipt_summary,
        "html": html_result["summary"],
    }


def check_source_status() -> dict:
    src = sandbox_root() / SOURCE_SLICE_ID
    product = src / "product-acceptance-report.md"
    next_step = src / "next-step.md"
    issues = []
    product_status = frontmatter_status(product.read_text(encoding="utf-8")) if product.exists() else "missing"
    next_status = frontmatter_status(next_step.read_text(encoding="utf-8")) if next_step.exists() else "missing"
    if product_status != "pass_product_grade":
        issues.append(f"source_product_not_pass:{product_status}")
    if next_status != "pass_product_grade_pending_user_next_slice_decision":
        issues.append(f"source_next_step_unexpected:{next_status}")
    return {"product_status": product_status, "next_status": next_status, "issues": issues}


def check_required_reports(final_gate: bool = False) -> dict:
    statuses = {}
    issues = []
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
        statuses[name] = frontmatter_status(path.read_text(encoding="utf-8"))
    if final_gate:
        required = {
            "reviewer-report.md": "reviewer_pass",
            "boundary-audit.md": "boundary_pass",
            "product-acceptance-report.md": "pass_product_grade",
        }
        for name, expected in required.items():
            actual = statuses.get(name, "missing_status").lower()
            if actual != expected:
                issues.append(f"final_gate_bad_status:{name}:{actual}:expected:{expected}")
        allowed_next = {"pass_product_grade_pending_user_next_slice_decision"}
        actual_next = statuses.get("next-step.md", "missing_status").lower()
        if actual_next not in allowed_next:
            issues.append(f"final_gate_bad_status:next-step.md:{actual_next}:expected_one_of:{','.join(sorted(allowed_next))}")
    return {"statuses": statuses, "issues": issues}


def run(rebuild: bool = False, final_gate: bool = False) -> dict:
    if rebuild:
        builder = load_builder()
        builder.build()
    fixtures = [
        root() / "fixtures" / "valid-native-entry-config.json",
        root() / "fixtures" / "valid-readonly-inspector-config.json",
    ]
    fixture_results = []
    for fixture in fixtures:
        errors = validate_config(load_json(fixture))
        fixture_results.append({"file": fixture.name, "errors": errors})
    main_cfg = load_json(fixtures[0])
    failure_results = check_failure_cases()
    prototype_results = check_prototype(main_cfg)
    source_results = check_source_status()
    report_results = check_required_reports(final_gate=final_gate)

    failures = []
    if any(item["errors"] for item in fixture_results):
        failures.append("positive_fixture_failed")
    if failure_results["mismatches"]:
        failures.append("failure_case_mismatch")
    if prototype_results["issues"]:
        failures.append("prototype_issues")
    if source_results["issues"]:
        failures.append("source_status_issues")
    if report_results["issues"]:
        failures.append("required_report_issues")
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
        "source_status": source_results,
        "required_reports": report_results,
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
    parser.add_argument("--final-gate", action="store_true", help="Require final Reviewer, Boundary, Product Acceptance, and next-step statuses.")
    args = parser.parse_args()
    result = run(rebuild=args.rebuild, final_gate=args.final_gate)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
