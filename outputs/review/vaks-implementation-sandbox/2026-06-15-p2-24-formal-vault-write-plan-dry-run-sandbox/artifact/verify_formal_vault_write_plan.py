from __future__ import annotations

import argparse
import html.parser
import importlib.util
import json
import re
import sys
from pathlib import Path


SLICE_ID = "2026-06-15-p2-24-formal-vault-write-plan-dry-run-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-23-native-markdown-entry-readonly-inspector-sandbox"

FORBIDDEN_OPERATIONS = [
    "formal_vault_read",
    "formal_vault_scan",
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
    "formal vault not accessed",
    "dry-run only",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "does not approve",
    "no formal vault write",
    "no formal vault read",
    "no sync",
    "no commit",
    "no push",
    "no promotion",
    "requires separate user approval",
]
AUTHORITY_CONFUSING_PATTERNS = [
    "approves action basis",
    "evidence supported",
    "reviewed truth",
    "merge approved",
    "sync approved",
    "promotion approved",
    "receipt proves evidence support",
]


class PlanHTMLParser(html.parser.HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.sandbox_only = False
        self.dry_run_only = False
        self.no_write = False
        self.no_sync = False
        self.no_authority = False
        self.roles: set[str] = set()
        self.cards: list[dict[str, str]] = []
        self.buttons: list[str] = []
        self.button_texts: list[str] = []
        self.inputs: list[dict[str, str]] = []
        self.anchors: list[dict[str, str]] = []
        self.forms = 0
        self.downloads = 0
        self.contenteditable = 0
        self._current_button: str | None = None
        self._in_script = False
        self.script_text = ""

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attr = {k: v or "" for k, v in attrs}
        if tag == "html":
            self.sandbox_only = attr.get("data-sandbox-only") == "true"
            self.dry_run_only = attr.get("data-dry-run-only") == "true"
            self.no_write = attr.get("data-no-write") == "true"
            self.no_sync = attr.get("data-no-sync") == "true"
            self.no_authority = attr.get("data-no-authority") == "true"
        if "data-role" in attr:
            self.roles.add(attr["data-role"])
        if tag == "article" and "card" in attr.get("class", "").split():
            self.cards.append({"kind": attr.get("data-kind", ""), "search": attr.get("data-search", "")})
        if tag == "button":
            self.buttons.append(attr.get("data-filter", ""))
            self._current_button = ""
        if tag == "input":
            self.inputs.append({"id": attr.get("id", ""), "type": attr.get("type", ""), "name": attr.get("name", "")})
        if tag == "form":
            self.forms += 1
        if tag == "a":
            self.anchors.append({"href": attr.get("href", ""), "download": attr.get("download", "")})
            if "download" in attr:
                self.downloads += 1
        if attr.get("contenteditable", "").lower() == "true":
            self.contenteditable += 1
        if tag == "script" and attr.get("id") == "plan-data":
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


def workspace_root() -> Path:
    return sandbox_root().parents[2]


def sha256(path: Path) -> str:
    h = __import__("hashlib").sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_builder() -> object:
    path = root() / "artifact" / "formal_vault_write_plan_builder.py"
    spec = importlib.util.spec_from_file_location("formal_vault_write_plan_builder", path)
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


def is_bad_target(value: str) -> bool:
    normalized = value.replace("\\", "/")
    return (
        re.match(r"^[A-Za-z]:/", normalized) is not None
        or normalized.startswith("/")
        or ".." in normalized.split("/")
        or normalized.startswith("wiki/")
        or normalized.startswith("templates/")
        or normalized.startswith("tools/")
        or "Obsidian" in value
    )


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

    proposed = cfg.get("proposed_files", [])
    if len(proposed) < cfg.get("product_metrics", {}).get("required_proposed_files", 5):
        errors.append("too_few_proposed_files")
    seen_targets = set()
    expected_source_prefix = f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/"
    for item in proposed:
        fid = item.get("id", "unknown")
        target = item.get("relative_target", "")
        if not target or is_bad_target(target):
            errors.append(f"proposed_file_absolute_or_forbidden:{fid}")
        if target in seen_targets:
            errors.append(f"duplicate_proposed_target:{fid}")
        seen_targets.add(target)
        if item.get("write_enabled") is not False:
            errors.append(f"proposed_file_write_enabled:{fid}")
        if item.get("dry_run_only") is not True:
            errors.append(f"proposed_file_not_dry_run:{fid}")
        if item.get("requires_user_approval") is not True:
            errors.append(f"proposed_file_missing_user_approval:{fid}")
        if item.get("rollback_required") is not True:
            errors.append(f"proposed_file_missing_rollback:{fid}")
        source_path = item.get("source_path", "")
        source_hash = item.get("source_sha256", "")
        if not source_path:
            errors.append(f"proposed_file_source_path_missing:{fid}")
        else:
            normalized_source = source_path.replace("\\", "/")
            if is_bad_target(normalized_source) or not normalized_source.startswith(expected_source_prefix):
                errors.append(f"proposed_file_source_path_invalid:{fid}")
            else:
                source_abs = (workspace_root() / normalized_source).resolve()
                try:
                    source_abs.relative_to(workspace_root())
                except ValueError:
                    errors.append(f"proposed_file_source_path_invalid:{fid}")
                if not source_abs.exists():
                    errors.append(f"proposed_file_source_missing:{fid}")
                elif source_hash != sha256(source_abs):
                    errors.append(f"proposed_file_source_hash_mismatch:{fid}")
        if item.get("content_binding") != "exact_source_sha256":
            errors.append(f"proposed_file_content_binding_missing:{fid}")

    prompts = cfg.get("approval_prompts", [])
    if len(prompts) < cfg.get("product_metrics", {}).get("required_approval_prompts", 3):
        errors.append("too_few_approval_prompts")
    for item in prompts:
        pid = item.get("id", "unknown")
        if item.get("required_response") != "explicit_user_approval":
            errors.append(f"approval_prompt_not_explicit:{pid}")
        if item.get("default") != "deny":
            errors.append(f"approval_prompt_not_deny:{pid}")
        if not item.get("blocks"):
            errors.append(f"approval_prompt_missing_blocks:{pid}")
        if not item.get("applies_to_file_ids"):
            errors.append(f"approval_prompt_missing_file_binding:{pid}")
        if item.get("plan_version_required") != cfg.get("plan_version"):
            errors.append(f"approval_prompt_missing_plan_version:{pid}")
        if item.get("plan_hash_required") is not True:
            errors.append(f"approval_prompt_missing_plan_hash:{pid}")
        phrase = item.get("confirmation_phrase", "")
        if not phrase or phrase != phrase.upper() or len(phrase.split()) < 4:
            errors.append(f"approval_prompt_weak_confirmation_phrase:{pid}")
        excludes = set(item.get("excludes", []))
        for excluded in ["obsidian_sync", "commit", "push", "promotion"]:
            if excluded not in excludes:
                errors.append(f"approval_prompt_missing_exclusion:{pid}:{excluded}")

    rollback = cfg.get("rollback_manifest", {})
    if rollback.get("dry_run_only") is not True:
        errors.append("rollback_not_dry_run")
    if not rollback.get("snapshot_root_label"):
        errors.append("rollback_snapshot_root_missing")
    if not rollback.get("retention_policy"):
        errors.append("rollback_retention_policy_missing")
    if rollback.get("snapshot_before_write_required") is not True:
        errors.append("rollback_snapshot_missing")
    if rollback.get("hash_before_required") is not True:
        errors.append("rollback_hash_before_missing")
    if rollback.get("hash_after_required") is not True:
        errors.append("rollback_hash_after_missing")
    if rollback.get("hash_algorithm") != "sha256":
        errors.append("rollback_hash_algorithm_bad")
    if "json" not in rollback.get("record_format", ""):
        errors.append("rollback_record_format_missing")
    if rollback.get("unexpected_file_abort") is not True:
        errors.append("rollback_unexpected_file_abort_missing")
    if rollback.get("unexpected_hash_drift_abort") is not True:
        errors.append("rollback_hash_drift_abort_missing")
    if rollback.get("dirty_state_abort") is not True:
        errors.append("rollback_dirty_state_abort_missing")
    if rollback.get("rollback_after_verification_required") is not True:
        errors.append("rollback_after_verification_missing")
    file_entries = rollback.get("file_entries", [])
    if len(file_entries) < len(proposed):
        errors.append("rollback_file_entries_missing")
    for entry in file_entries:
        fid = entry.get("file_id", "unknown")
        target = entry.get("relative_target", "")
        if is_bad_target(target):
            errors.append("rollback_target_absolute_or_forbidden")
        if not entry.get("before_state"):
            errors.append(f"rollback_before_state_missing:{fid}")
        if not entry.get("snapshot_location_label"):
            errors.append(f"rollback_snapshot_location_missing:{fid}")
        if entry.get("planned_operation") not in {"create_or_replace", "create", "replace"}:
            errors.append(f"rollback_operation_bad:{fid}")
        if entry.get("rollback_action") not in {"restore_previous_if_existed_else_delete_created_file", "restore_previous", "delete_created_file"}:
            errors.append(f"rollback_action_missing:{fid}")
        if not entry.get("post_rollback_verification"):
            errors.append(f"rollback_post_verification_missing:{fid}")

    hash_plan = cfg.get("hash_check_plan", {})
    if hash_plan.get("dry_run_only") is not True:
        errors.append("hash_plan_not_dry_run")
    if hash_plan.get("algorithm") != "sha256":
        errors.append("hash_algorithm_bad")
    if hash_plan.get("record_format") != "json-lines":
        errors.append("hash_record_format_bad")
    phases = set(hash_plan.get("phases", []))
    for phase in ["before_snapshot", "after_write", "after_rollback_if_needed"]:
        if phase not in phases:
            errors.append(f"hash_phase_missing:{phase}")
    if hash_plan.get("abort_on_missing_before_hash") is not True:
        errors.append("hash_before_missing")
    if hash_plan.get("abort_on_unexpected_after_hash") is not True:
        errors.append("hash_after_guard_missing")
    if hash_plan.get("abort_on_dirty_state") is not True:
        errors.append("hash_dirty_state_abort_missing")
    if hash_plan.get("abort_on_unexpected_file") is not True:
        errors.append("hash_unexpected_file_abort_missing")
    if hash_plan.get("verify_after_rollback") is not True:
        errors.append("hash_rollback_verification_missing")
    if hash_plan.get("per_file_records_required") is not True:
        errors.append("hash_per_file_records_missing")
    records = hash_plan.get("records", [])
    if len(records) < len(proposed):
        errors.append("hash_records_missing")
    for entry in records:
        fid = entry.get("file_id", "unknown")
        target = entry.get("relative_target", "")
        if is_bad_target(target):
            errors.append(f"hash_record_target_forbidden:{fid}")
        for field in ["before_hash_field", "after_hash_field", "rollback_hash_field"]:
            if "sha256" not in entry.get(field, ""):
                errors.append(f"hash_record_field_bad:{fid}:{field}")
    if hash_plan.get("no_executable_commands") is not True:
        errors.append("hash_plan_allows_commands")
    if hash_plan.get("command_templates"):
        errors.append("hash_plan_executable_command")
    command_text = json.dumps(hash_plan.get("command_templates", []))
    if re.search(r"\b(powershell|cmd|git|sync|robocopy|copy|move|remove|del)\b|H:/|H:\\", command_text, flags=re.IGNORECASE):
        errors.append("hash_plan_executable_command")

    stop_text = "\n".join(cfg.get("stop_conditions", [])).lower()
    for required in ["formal vault read", "formal vault write", "obsidian sync", "commit", "push", "promotion", "approval", "rollback", "hash"]:
        if required not in stop_text:
            errors.append(f"missing_stop_condition:{required}")
    if any(pattern in stop_text for pattern in AUTHORITY_CONFUSING_PATTERNS):
        errors.append("authority_confusing_text")

    controls = cfg.get("inspector_controls", {})
    allowed_inputs = {("q", "search")}
    actual_inputs = {(item.get("id", ""), item.get("type", "")) for item in controls.get("inputs", [])}
    if actual_inputs != allowed_inputs:
        errors.append("inspector_inputs_not_allowlisted")
    allowed_buttons = {"all", "files", "approvals", "rollback", "stops"}
    actual_buttons = {item.get("filter", "") for item in controls.get("buttons", [])}
    if actual_buttons != allowed_buttons:
        errors.append("inspector_buttons_not_allowlisted")
    for button in controls.get("buttons", []):
        label = button.get("label", "").strip().lower()
        if label in {"save", "sync", "commit", "push", "write", "approve", "promote", "execute"}:
            errors.append(f"inspector_control_not_allowed:button:{label}")

    max_steps = cfg.get("product_metrics", {}).get("max_journey_steps", 3)
    for journey in cfg.get("journeys", []):
        jid = journey.get("id", "unknown")
        if len(journey.get("steps", [])) > max_steps:
            errors.append(f"journey_too_deep:{jid}")
        if not journey.get("stop_condition"):
            errors.append(f"journey_missing_stop_condition:{jid}")

    if cfg.get("product_metrics", {}).get("minimum_failure_cases", 0) < 30:
        errors.append("minimum_failure_cases_too_low")
    return sorted(set(errors))


def check_failure_cases() -> dict:
    oracle = load_json(root() / "artifact" / "failure-case-oracle.json")
    mismatches = []
    expected_files = {entry["file"] for entry in oracle}
    actual_files = {path.name for path in (root() / "failure-cases").glob("*.json")}
    for name in sorted(expected_files - actual_files):
        mismatches.append({"file": name, "missing": True})
    for name in sorted(actual_files - expected_files):
        mismatches.append({"file": name, "extra": True})
    for entry in oracle:
        path = root() / "failure-cases" / entry["file"]
        if not path.exists():
            continue
        errors = validate_config(load_json(path))
        missing = [code for code in entry["expected_failures"] if code not in errors]
        extra = [code for code in errors if code not in entry["expected_failures"]]
        if missing or extra:
            mismatches.append({"file": entry["file"], "missing_expected": missing, "extra": extra, "actual": errors})
    return {"count": len(oracle), "mismatches": mismatches}


def resolve_markdown_link(page: Path, target: str) -> Path | None:
    if target.startswith("http://") or target.startswith("https://") or target.startswith("#"):
        return None
    clean = target.split("#", 1)[0].replace("%20", " ")
    if not clean:
        return None
    return (page.parent / clean).resolve()


def page_links(page: Path) -> set[str]:
    text = page.read_text(encoding="utf-8")
    links = set()
    for match in re.finditer(r"\[\[([^\]|#]+)", text):
        links.add(match.group(1).strip())
    for match in re.finditer(r"\[[^\]]+\]\(([^)]+)\)", text):
        links.add(match.group(1).strip())
    for name in ["plan-inspector.html", "Receipts/formal-vault-write-plan-dry-run-receipt.json"]:
        if name in text:
            links.add(name)
    return links


def check_wikilinks(proto: Path) -> list[str]:
    issues = []
    pages = {path.stem for path in proto.glob("*.md")}
    pattern = re.compile(r"\[\[([^\]|#]+)")
    for page in proto.glob("*.md"):
        for match in pattern.finditer(page.read_text(encoding="utf-8")):
            target = match.group(1).strip()
            if target not in pages:
                issues.append(f"broken_wikilink:{page.name}->{target}")
    return issues


def check_markdown_links(proto: Path) -> list[str]:
    issues = []
    pattern = re.compile(r"\[[^\]]+\]\(([^)]+)\)")
    for page in proto.rglob("*.md"):
        for match in pattern.finditer(page.read_text(encoding="utf-8")):
            target = resolve_markdown_link(page, match.group(1))
            if target is not None and not target.exists():
                issues.append(f"broken_markdown_link:{page.name}->{match.group(1)}")
    return issues


def check_html(path: Path) -> dict:
    issues = []
    summary = {}
    if not path.exists():
        return {"issues": ["missing_plan_inspector_html"], "summary": summary}
    text = path.read_text(encoding="utf-8")
    parser = PlanHTMLParser()
    parser.feed(text)
    summary = {
        "sandbox_only": parser.sandbox_only,
        "dry_run_only": parser.dry_run_only,
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
        "downloads": parser.downloads,
        "contenteditable": parser.contenteditable,
    }
    if not parser.sandbox_only:
        issues.append("html_missing_sandbox_marker")
    if not parser.dry_run_only:
        issues.append("html_missing_dry_run_marker")
    if not parser.no_write:
        issues.append("html_missing_no_write_marker")
    if not parser.no_sync:
        issues.append("html_missing_no_sync_marker")
    if not parser.no_authority:
        issues.append("html_missing_no_authority_marker")
    for role in ["plan-filter", "plan-cards", "boundary-rail"]:
        if role not in parser.roles:
            issues.append(f"html_missing_role:{role}")
    if parser.forms:
        issues.append("html_form_present")
    if parser.downloads:
        issues.append("html_download_link_present")
    if parser.contenteditable:
        issues.append("html_contenteditable_present")
    if parser.inputs != [{"id": "q", "type": "search", "name": ""}]:
        issues.append("html_inputs_not_allowlisted")
    if parser.buttons != ["all", "files", "approvals", "rollback", "stops"]:
        issues.append("html_buttons_not_allowlisted")
    for text_value in parser.button_texts:
        if text_value.strip().lower() in {"save", "sync", "commit", "push", "write", "approve", "promote", "execute"}:
            issues.append(f"html_write_button_present:{text_value.strip().lower()}")
    if re.search(r"\b(fetch|XMLHttpRequest|sendBeacon|localStorage|sessionStorage)\b", text):
        issues.append("html_network_or_storage_api_present")
    if re.search(r"\b(save|sync|write|commit|push|promote|execute)\s*\(", text, flags=re.IGNORECASE):
        issues.append("html_write_like_function_present")
    for anchor in parser.anchors:
        href = anchor.get("href", "").lower()
        if href.startswith(("http://", "https://", "mailto:", "javascript:")) or anchor.get("download"):
            issues.append("html_forbidden_anchor")
    try:
        data = json.loads(parser.script_text)
        if len(data.get("proposed_files", [])) < 5:
            issues.append("html_embedded_files_missing")
        if len(data.get("approval_prompts", [])) < 3:
            issues.append("html_embedded_prompts_missing")
    except Exception as exc:
        issues.append(f"html_embedded_data_invalid:{exc}")
    lower = text.lower()
    for phrase in ["formal vault not accessed", "dry-run only", "not evidence support", "not action basis", "no formal vault write"]:
        if phrase not in lower:
            issues.append(f"html_missing_boundary_phrase:{phrase}")
    return {"issues": sorted(set(issues)), "summary": summary}


def check_actual_journeys(proto: Path, html_ok: bool) -> dict:
    issues = []
    results = {}
    pages = {
        "home": proto / "00 Dry Run Home.md",
        "files": proto / "01 Proposed File List.md",
        "approval": proto / "02 Approval Prompt Matrix.md",
        "rollback": proto / "03 Rollback Manifest.md",
        "hash": proto / "04 Hash Check Plan.md",
        "stops": proto / "05 Stop Conditions.md",
    }
    for key, path in pages.items():
        if not path.exists():
            issues.append(f"journey_missing_page:{key}")
    if issues:
        return {"results": results, "issues": issues}
    home_links = page_links(pages["home"])
    files_links = page_links(pages["files"])
    approval_links = page_links(pages["approval"])
    rollback_links = page_links(pages["rollback"])
    stops_text = pages["stops"].read_text(encoding="utf-8").lower()
    if "01 Proposed File List" not in home_links or "05 Stop Conditions" not in files_links:
        issues.append("journey_path_missing:scope_review")
    else:
        results["scope_review"] = {"links_verified": True, "max_links": 2}
    if "02 Approval Prompt Matrix" not in home_links or "05 Stop Conditions" not in approval_links:
        issues.append("journey_path_missing:approval_review")
    else:
        results["approval_review"] = {"links_verified": True, "max_links": 2}
    if "03 Rollback Manifest" not in home_links or "04 Hash Check Plan" not in rollback_links:
        issues.append("journey_path_missing:rollback_review")
    else:
        results["rollback_review"] = {"links_verified": True, "max_links": 2}
    if "plan-inspector.html" not in home_links or not html_ok or "formal vault write" not in stops_text:
        issues.append("journey_path_missing:inspector_review")
    else:
        results["inspector_review"] = {"links_verified": True, "max_links": 2, "html_allowlist_ok": html_ok}
    return {"results": results, "issues": issues}


def check_prototype(cfg: dict) -> dict:
    proto = root() / "prototype" / "formal-vault-write-plan-dry-run"
    issues = []
    required = [
        "00 Dry Run Home.md",
        "01 Proposed File List.md",
        "02 Approval Prompt Matrix.md",
        "03 Rollback Manifest.md",
        "04 Hash Check Plan.md",
        "05 Stop Conditions.md",
        "06 Dry Run Results.md",
        "07 Reviewer Packet.md",
        "plan-inspector.html",
        "Receipts/formal-vault-write-plan-dry-run-receipt.json",
    ]
    for file in required:
        if not (proto / file).exists():
            issues.append(f"missing_prototype_file:{file}")
    for path in proto.rglob("*"):
        rel = path.relative_to(proto).as_posix()
        if path.suffix == ".base":
            issues.append(f"real_base_file_present:{rel}")
        if path.name == ".obsidian":
            issues.append("obsidian_config_present")
        if "__pycache__" in path.parts or path.suffix == ".pyc":
            issues.append(f"python_cache_present:{rel}")
    if proto.exists():
        issues.extend(check_wikilinks(proto))
        issues.extend(check_markdown_links(proto))
    text = "\n".join(
        path.read_text(encoding="utf-8", errors="ignore")
        for path in proto.rglob("*")
        if path.is_file() and path.suffix in {".md", ".html", ".json"}
    )
    lower = text.lower()
    for phrase in REQUIRED_BOUNDARY_PHRASES:
        if phrase.lower() not in lower:
            issues.append(f"prototype_missing_boundary_phrase:{phrase}")
    for pattern in AUTHORITY_CONFUSING_PATTERNS:
        if pattern in lower:
            issues.append(f"prototype_authority_confusing_text:{pattern}")
    receipt_summary = {}
    receipt_path = proto / "Receipts" / "formal-vault-write-plan-dry-run-receipt.json"
    if receipt_path.exists():
        receipt = load_json(receipt_path)
        receipt_summary = {
            "slice_id": receipt.get("slice_id"),
            "source_slice": receipt.get("source_slice"),
            "formal_vault_accessed": receipt.get("formal_vault_accessed"),
            "source_hashes": len(receipt.get("source_hashes", {})),
            "proposed_file_source_bindings": len(receipt.get("proposed_file_source_bindings", [])),
        }
        if receipt.get("slice_id") != SLICE_ID:
            issues.append("receipt_wrong_slice_id")
        if receipt.get("source_slice") != SOURCE_SLICE_ID:
            issues.append("receipt_wrong_source_slice")
        if receipt.get("formal_vault_accessed") is not False:
            issues.append("receipt_formal_vault_accessed")
        forbidden = receipt.get("forbidden_operations", {})
        for op in FORBIDDEN_OPERATIONS:
            if op not in forbidden:
                issues.append(f"receipt_missing_forbidden_operation:{op}")
            elif forbidden.get(op) is not False:
                issues.append(f"receipt_forbidden_operation_true:{op}")
        for key, value in receipt.get("source_hashes", {}).items():
            if value == "missing":
                issues.append(f"receipt_missing_source_hash:{key}")
        if len(receipt.get("proposed_file_source_bindings", [])) < len(cfg.get("proposed_files", [])):
            issues.append("receipt_missing_proposed_file_source_bindings")
    html = check_html(proto / "plan-inspector.html")
    issues.extend(html["issues"])
    journeys = check_actual_journeys(proto, html_ok=not html["issues"])
    issues.extend(journeys["issues"])
    return {
        "prototype_path": str(proto),
        "issues": sorted(set(issues)),
        "receipt": receipt_summary,
        "html": html["summary"],
        "actual_journeys": journeys["results"],
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
        actual_next = statuses.get("next-step.md", "missing_status").lower()
        if actual_next != "pass_product_grade_pending_user_next_slice_decision":
            issues.append(f"final_gate_bad_status:next-step.md:{actual_next}:expected:pass_product_grade_pending_user_next_slice_decision")
    return {"statuses": statuses, "issues": issues}


def run(rebuild: bool = False, final_gate: bool = False) -> dict:
    if rebuild:
        builder = load_builder()
        builder.build()
    fixtures = [
        root() / "fixtures" / "valid-write-plan-config.json",
        root() / "fixtures" / "valid-rollback-plan-config.json",
    ]
    fixture_results = []
    for fixture in fixtures:
        fixture_results.append({"file": fixture.name, "errors": validate_config(load_json(fixture))})
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
            "not formal vault approval",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rebuild", action="store_true")
    parser.add_argument("--final-gate", action="store_true")
    args = parser.parse_args()
    result = run(rebuild=args.rebuild, final_gate=args.final_gate)
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
