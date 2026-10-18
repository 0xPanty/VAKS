from __future__ import annotations

import ast
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
WORKSPACE = Path(__file__).resolve().parents[5]
CONTRACT_PATH = ROOT / "artifact" / "static_boundary_scan_regression_contract.json"


COMMAND_SEQUENCES = {
    "git_commit": ("git", "commit"),
    "git_push": ("git", "push"),
    "pip_install": ("pip", "install"),
    "python_pip_install": ("python", "-m", "pip", "install"),
    "npm_install": ("npm", "install"),
    "pnpm_add": ("pnpm", "add"),
    "yarn_add": ("yarn", "add"),
}

STRING_PATTERNS = {
    "start_process": re.compile(r"\bstart-process\b", re.IGNORECASE),
    "register_scheduled_task": re.compile(r"\bregister-scheduledtask\b", re.IGNORECASE),
    "new_service": re.compile(r"\bnew-service\b", re.IGNORECASE),
    "schtasks": re.compile(r"\bschtasks\b", re.IGNORECASE),
    "mcp_write": re.compile(r"\bmcp\s+write\b", re.IGNORECASE),
    "hook_installed": re.compile(r"\bhook\s+installed\b", re.IGNORECASE),
    "remove_item": re.compile(r"\bremove-item\b", re.IGNORECASE),
}

WRITE_MODES = {"w", "a", "x", "w+", "a+", "x+", "r+"}


@dataclass(frozen=True)
class ScanIssue:
    issue_id: str
    line: int
    detail: str

    def to_dict(self) -> dict:
        return {"issue_id": self.issue_id, "line": self.line, "detail": self.detail}


def load_contract() -> dict:
    with CONTRACT_PATH.open("r", encoding="utf-8") as handle:
        payload = json.load(handle)
    if not isinstance(payload, dict):
        raise TypeError("contract must be a JSON object")
    return payload


def normalize_token(token: str) -> str:
    return token.strip().lower()


def sequence_present(tokens: list[str], sequence: tuple[str, ...]) -> bool:
    normalized = [normalize_token(token) for token in tokens]
    needed = [normalize_token(token) for token in sequence]
    for index in range(0, len(normalized) - len(needed) + 1):
        if normalized[index : index + len(needed)] == needed:
            return True
    return False


def flatten_literal_strings(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return [node.value]
    if isinstance(node, (ast.List, ast.Tuple)):
        values: list[str] = []
        for element in node.elts:
            values.extend(flatten_literal_strings(element))
        return values
    return []


def literal_string_list(node: ast.AST) -> list[str] | None:
    values = flatten_literal_strings(node)
    if values and isinstance(node, (ast.List, ast.Tuple)):
        return values
    return None


def call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        parent = call_name(node.value)
        return f"{parent}.{node.attr}" if parent else node.attr
    if isinstance(node, ast.Call):
        return call_name(node.func)
    return ""


def collect_string_literals(tree: ast.AST) -> list[tuple[int, str]]:
    values: list[tuple[int, str]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            values.append((getattr(node, "lineno", 0), node.value))
    return values


def detect_shell_true(call: ast.Call) -> bool:
    for keyword in call.keywords:
        if keyword.arg == "shell" and isinstance(keyword.value, ast.Constant) and keyword.value.value is True:
            return True
    return False


def detect_write_mode_open(call: ast.Call) -> str | None:
    name = call_name(call.func)
    if name != "open" and not name.endswith(".open"):
        return None
    if name == "open":
        mode_node = call.args[1] if len(call.args) > 1 else None
    else:
        mode_node = call.args[0] if call.args else None
    for keyword in call.keywords:
        if keyword.arg == "mode":
            mode_node = keyword.value
    if isinstance(mode_node, ast.Constant) and isinstance(mode_node.value, str):
        mode = mode_node.value
        if any(mode.startswith(prefix) for prefix in WRITE_MODES):
            return mode
    return None


def detect_write_bytes(call: ast.Call) -> bool:
    return call_name(call.func).endswith(".write_bytes")


def allowed_write_text_line(line: str, allowed_lines: set[str]) -> bool:
    return line.strip() in allowed_lines


def scan_python_source(source: str, *, allowed_write_lines: list[str] | None = None) -> list[dict]:
    allowed_lines = set(allowed_write_lines or [])
    issues: list[ScanIssue] = []
    try:
        tree = ast.parse(source)
    except SyntaxError as exc:
        return [ScanIssue("syntax_error", exc.lineno or 0, str(exc)).to_dict()]

    lines = source.splitlines()
    assigned_string_lists: dict[str, list[str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            literal_values = literal_string_list(node.value)
            if literal_values is None:
                continue
            for target in node.targets:
                if isinstance(target, ast.Name):
                    assigned_string_lists[target.id] = literal_values
        elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
            literal_values = literal_string_list(node.value) if node.value is not None else None
            if literal_values is not None:
                assigned_string_lists[node.target.id] = literal_values

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            name = call_name(node.func)
            if detect_shell_true(node):
                issues.append(ScanIssue("shell_true", getattr(node, "lineno", 0), "shell=True is forbidden"))
            mode = detect_write_mode_open(node)
            if mode is not None:
                issues.append(ScanIssue("write_mode_open", getattr(node, "lineno", 0), f"open mode {mode} is forbidden"))
            if detect_write_bytes(node):
                issues.append(ScanIssue("unauthorized_write_bytes", getattr(node, "lineno", 0), "write_bytes is forbidden"))
            if name.endswith("write_text"):
                line = lines[getattr(node, "lineno", 1) - 1] if getattr(node, "lineno", 0) else ""
                if not allowed_write_text_line(line, allowed_lines):
                    issues.append(ScanIssue("unauthorized_write_text", getattr(node, "lineno", 0), line.strip()))
            tokens: list[str] = []
            for arg in node.args:
                if isinstance(arg, ast.Name) and arg.id in assigned_string_lists:
                    tokens.extend(assigned_string_lists[arg.id])
                else:
                    tokens.extend(flatten_literal_strings(arg))
            for keyword in node.keywords:
                if isinstance(keyword.value, ast.Name) and keyword.value.id in assigned_string_lists:
                    tokens.extend(assigned_string_lists[keyword.value.id])
                else:
                    tokens.extend(flatten_literal_strings(keyword.value))
            for issue_id, sequence in COMMAND_SEQUENCES.items():
                if sequence_present(tokens, sequence):
                    issues.append(ScanIssue(issue_id, getattr(node, "lineno", 0), " ".join(sequence)))

    for line_number, value in collect_string_literals(tree):
        for issue_id, pattern in STRING_PATTERNS.items():
            if pattern.search(value):
                issues.append(ScanIssue(issue_id, line_number, value.strip()))

    seen = set()
    deduped: list[dict] = []
    for issue in issues:
        key = (issue.issue_id, issue.line, issue.detail)
        if key not in seen:
            deduped.append(issue.to_dict())
            seen.add(key)
    return deduped


def scan_live_source(relative_path: str, allowed_write_lines: list[str] | None = None) -> dict:
    path = WORKSPACE / relative_path
    if not path.exists():
        return {
            "path": relative_path,
            "exists": False,
            "issues": [ScanIssue("source_missing", 0, relative_path).to_dict()],
        }
    source = path.read_text(encoding="utf-8")
    return {
        "path": relative_path,
        "exists": path.exists(),
        "issues": scan_python_source(source, allowed_write_lines=allowed_write_lines),
    }


def run_regression() -> dict:
    contract = load_contract()
    positive_results = []
    for item in contract["live_positive_sources"]:
        positive_results.append(
            scan_live_source(
                item["path"],
                allowed_write_lines=item.get("allowed_write_lines", []),
            )
        )
    return {
        "record_kind": "sandbox_static_boundary_scan_regression_result",
        "slice_id": contract["slice_id"],
        "source_slice_id": contract["source_slice_id"],
        "truth_boundary": "static_scan_regression_not_general_security_or_execution_authority",
        "positive_results": positive_results,
        "scanner_limits": contract["scanner_limits"],
        "automatic_execution": False,
        "mainline_ready": False,
        "promotion_ready": False,
        "action_basis_ready": False,
        "must_not": contract["output_contract"]["must_not"],
    }


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    result = run_regression()
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if all(not item["issues"] for item in result["positive_results"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
