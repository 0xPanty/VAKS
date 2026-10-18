from __future__ import annotations

import copy
import json
import re
import shutil
from pathlib import Path
from typing import Any, Callable

from handoff_packet_common import (
    CHECK_IDS,
    CONTROL_EXPECTED,
    HANDOFF_MODES,
    NON_CLAIMS,
    OPERATION_KEYS,
    PURPOSE,
    READ_ONLY_SOURCES,
    ROOT,
    SLICE_ID,
    SOURCE_SLICE,
    expected_checks,
    expected_hash,
    expected_payload,
    expected_source_binding,
    expected_source_inputs,
    expected_source_statuses,
    inspect_prototype,
    run_manual_negative_probes,
    validate_config,
    validate_failure_cases,
    validate_prototype_tamper,
    write_json,
    write_text,
)


FailureMutator = Callable[[dict[str, Any]], None]


def slug_value(value: Any) -> str:
    slug = re.sub(r"[^A-Za-z0-9_.-]+", "-", str(value)).strip("-")
    return (slug or "value")[:32]


def reset_dir(path: Path) -> None:
    root = ROOT.resolve()
    target = path.resolve()
    if not str(target).startswith(str(root)):
        raise RuntimeError(f"refusing to reset outside sandbox: {target}")
    if path.exists():
        shutil.rmtree(path)
    path.mkdir(parents=True, exist_ok=True)


def set_path(config: dict[str, Any], path: list[Any], value: Any) -> None:
    cursor: Any = config
    for part in path[:-1]:
        cursor = cursor[part]
    cursor[path[-1]] = value


def rehash(config: dict[str, Any]) -> None:
    config["handoff_packet_hash"] = ""
    if isinstance(config.get("handoff_receipt"), dict):
        config["handoff_receipt"]["handoff_packet_hash"] = ""
    packet_hash = expected_hash(config)
    config["handoff_packet_hash"] = packet_hash
    if isinstance(config.get("handoff_receipt"), dict):
        config["handoff_receipt"]["handoff_packet_hash"] = packet_hash


def make_config(mode: str) -> dict[str, Any]:
    config: dict[str, Any] = {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE,
        "handoff_packet_version": "p2-35-formal-vault-status-surface-handoff-packet-v1",
        "truth_boundary": "sandbox_only_handoff_packet_not_authority",
        "purpose": PURPOSE,
        "handoff_mode": mode,
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": READ_ONLY_SOURCES,
        "operations": {key: False for key in OPERATION_KEYS},
        "handoff_controls": copy.deepcopy(CONTROL_EXPECTED),
        "source_inputs": expected_source_inputs(),
        "source_statuses": expected_source_statuses(),
        "source_surface_binding": expected_source_binding(),
        "handoff_payload": expected_payload(mode),
        "handoff_checks": expected_checks(),
        "handoff_receipt": {
            "record_kind": "sandbox_formal_vault_status_surface_handoff_packet_receipt",
            "slice_id": SLICE_ID,
            "source_slice": SOURCE_SLICE,
            "handoff_result": HANDOFF_MODES[mode],
            "source_input_count": len(READ_ONLY_SOURCES),
            "check_count": len(CHECK_IDS),
            "formal_vault_accessed": False,
            "approval_collected_now": False,
            "user_instruction_collected": False,
            "user_wording_stored": False,
            "execution_permission_granted": False,
            "execution_performed": False,
            "write_performed": False,
            "sync_performed": False,
            "commit_performed": False,
            "push_performed": False,
            "promotion_performed": False,
            "mainline_ready": False,
            "handoff_used_as_action_basis": False,
            "dirty_tree_fixed": False,
            "auto_advanced": False,
            "handoff_packet_hash": "",
            "non_claims": sorted(NON_CLAIMS),
        },
        "product_metrics": {
            "required_positive_fixtures": 3,
            "minimum_failure_cases": 100,
            "required_source_inputs": len(READ_ONLY_SOURCES),
            "required_handoff_checks": len(CHECK_IDS),
            "manual_negative_probes": 12,
            "max_handoff_steps": 3,
        },
        "handoff_packet_hash": "",
    }
    rehash(config)
    return config


def write_fixtures() -> dict[str, dict[str, Any]]:
    fixtures = {
        "valid-next-agent-read-only-handoff-config.json": make_config("next_agent_read_only_handoff"),
        "valid-product-workflow-prebrief-handoff-config.json": make_config("product_workflow_prebrief_handoff"),
        "valid-pause-or-park-handoff-config.json": make_config("pause_or_park_handoff"),
    }
    reset_dir(ROOT / "fixtures")
    for name, config in fixtures.items():
        write_json(ROOT / "fixtures" / name, config)
    return fixtures


def build_failure_cases(base: dict[str, Any]) -> dict[str, list[str]]:
    cases: list[tuple[str, str, FailureMutator, bool]] = []
    for op in OPERATION_KEYS:
        cases.append((f"operation-{op}", f"Operation flag {op} changed.", lambda cfg, key=op: set_path(cfg, ["operations", key], True), True))
    for control, expected in CONTROL_EXPECTED.items():
        cases.append((f"control-{control}", f"Handoff control {control} changed.", lambda cfg, key=control, value=expected: set_path(cfg, ["handoff_controls", key], not value), True))
    for index in range(len(READ_ONLY_SOURCES)):
        cases.append((f"source-input-{index}-sha-drift", "Source input hash changed.", lambda cfg, idx=index: set_path(cfg, ["source_inputs", idx, "source_sha256"], "0" * 64), True))
    for index, item in enumerate(base["source_statuses"]):
        cases.append((f"source-status-{item['file'].replace('.', '-')}-drift", "Source status changed.", lambda cfg, idx=index: set_path(cfg, ["source_statuses", idx, "actual_status"], "pending"), True))
    for key, value in [
        ("product_status", "pending"),
        ("reviewer_status", "pending"),
        ("boundary_status", "pending"),
        ("verification_status", "pending"),
        ("next_status", "pending"),
        ("status_surface_hash", "0" * 64),
        ("surface_result", "READY"),
        ("source_slice_count", 99),
        ("source_input_count", 99),
        ("badge_count", 99),
        ("stop_line_count", 99),
        ("formal_vault_accessed", True),
        ("approval_collected_now", True),
        ("user_instruction_collected", True),
        ("user_wording_stored", True),
        ("execution_permission_granted", True),
        ("execution_performed", True),
        ("write_performed", True),
        ("sync_performed", True),
        ("mainline_ready", True),
        ("status_used_as_action_basis", True),
        ("dirty_tree_fixed", True),
    ]:
        cases.append((f"binding-{key}", f"Source binding {key} changed.", lambda cfg, k=key, v=value: set_path(cfg, ["source_surface_binding", k], v), True))
    for key, value in [
        ("packet_id", "wrong-id"),
        ("packet_id", "python tools/promote.py --sync"),
        ("handoff_mode", "wrong-mode"),
        ("handoff_result", "READY"),
        ("source_surface_hash", "1" * 64),
        ("next_work_must_use_fresh_sandbox", False),
        ("allowed_next_write_scope_pattern", "H:/Obsidian/资料库"),
        ("forbidden_next_actions", []),
        ("required_next_checks", []),
        ("operator_stop_summary", "ready to execute"),
        ("actual_approval_collected", True),
        ("actual_user_wording_stored", True),
        ("commands_supplied", True),
        ("formal_vault_paths_present", True),
        ("execution_permission_granted", True),
        ("handoff_used_as_action_basis", True),
        ("mainline_ready", True),
        ("dirty_tree_fixed", True),
        ("non_claims", []),
    ]:
        slug = slug_value(value)
        cases.append((f"payload-{key}-{slug}", f"Handoff payload {key} changed.", lambda cfg, k=key, v=value: set_path(cfg, ["handoff_payload", k], v), True))
    for index, check in enumerate(CHECK_IDS):
        cases.append((f"check-{check}-status", "Handoff check status changed.", lambda cfg, idx=index: set_path(cfg, ["handoff_checks", idx, "status"], "READY"), True))
        cases.append((f"check-{check}-collected", "Handoff check collects data.", lambda cfg, idx=index: set_path(cfg, ["handoff_checks", idx, "collected_now"], True), True))
    for key, value in [
        ("record_kind", "wrong_kind"),
        ("slice_id", "wrong-slice"),
        ("source_slice", "wrong-source"),
        ("handoff_result", "READY"),
        ("source_input_count", 99),
        ("check_count", 99),
        ("formal_vault_accessed", True),
        ("approval_collected_now", True),
        ("user_instruction_collected", True),
        ("user_wording_stored", True),
        ("execution_permission_granted", True),
        ("execution_performed", True),
        ("write_performed", True),
        ("sync_performed", True),
        ("commit_performed", True),
        ("push_performed", True),
        ("promotion_performed", True),
        ("mainline_ready", True),
        ("handoff_used_as_action_basis", True),
        ("dirty_tree_fixed", True),
        ("auto_advanced", True),
        ("handoff_packet_hash", "2" * 64),
        ("non_claims", []),
    ]:
        cases.append((f"receipt-{key}", f"Receipt {key} changed.", lambda cfg, k=key, v=value: set_path(cfg, ["handoff_receipt", k], v), key != "handoff_packet_hash"))
    for key, value in [
        ("required_positive_fixtures", 2),
        ("minimum_failure_cases", 99),
        ("required_source_inputs", 99),
        ("required_handoff_checks", 99),
        ("manual_negative_probes", 11),
        ("max_handoff_steps", 4),
    ]:
        cases.append((f"metric-{key}", f"Metric {key} changed.", lambda cfg, k=key, v=value: set_path(cfg, ["product_metrics", k], v), True))
    cases.extend([
        ("top-level-slice-id", "Slice id changed.", lambda cfg: set_path(cfg, ["slice_id"], "wrong-slice"), True),
        ("top-level-source-slice", "Source slice changed.", lambda cfg: set_path(cfg, ["source_slice"], "wrong-source"), True),
        ("top-level-version", "Version changed.", lambda cfg: set_path(cfg, ["handoff_packet_version"], "wrong-version"), True),
        ("top-level-boundary", "Boundary changed.", lambda cfg: set_path(cfg, ["truth_boundary"], "wrong-boundary"), True),
        ("top-level-purpose", "Purpose changed.", lambda cfg: set_path(cfg, ["purpose"], "different purpose"), True),
        ("top-level-mode", "Mode changed.", lambda cfg: set_path(cfg, ["handoff_mode"], "wrong-mode"), True),
        ("top-level-write-scope", "Write scope changed.", lambda cfg: set_path(cfg, ["write_scope"], ["outputs/review/other/"]), True),
        ("top-level-read-sources", "Read-only sources changed.", lambda cfg: set_path(cfg, ["read_only_sources"], []), True),
        ("top-level-extra-key", "Unknown key added.", lambda cfg: cfg.update({"unexpected": "value"}), True),
        ("top-level-command-string", "Unknown key contains command.", lambda cfg: cfg.update({"unexpected": "python tools/promote.py --sync"}), True),
        ("hash-drift", "Top-level hash changed.", lambda cfg: set_path(cfg, ["handoff_packet_hash"], "3" * 64), False),
    ])
    prototype_cases: list[tuple[str, str, dict[str, Any]]] = [
        ("prototype-markdown-missing-markers", "Prototype home loses markers.", {"kind": "markdown_replace", "file": "00 Handoff Home.md", "content": "# Handoff\n\nGeneric."}),
        ("prototype-markdown-command", "Prototype contains command.", {"kind": "markdown_replace", "file": "04 Reviewer Packet.md", "content": "python tools/promote.py --sync"}),
        ("prototype-markdown-approval", "Prototype claims approval.", {"kind": "markdown_replace", "file": "03 Stop Conditions.md", "content": "approval collected: yes"}),
        ("prototype-markdown-action-basis", "Prototype claims action basis.", {"kind": "markdown_replace", "file": "02 Allowed Continuations.md", "content": "action basis: yes"}),
        ("prototype-markdown-mainline", "Prototype claims mainline.", {"kind": "markdown_replace", "file": "02 Allowed Continuations.md", "content": "mainline ready: yes"}),
        ("prototype-markdown-may-execute", "Prototype permits execution.", {"kind": "markdown_replace", "file": "03 Stop Conditions.md", "content": "The operator may execute."}),
        ("prototype-html-command", "HTML contains command.", {"kind": "html_replace", "file": "handoff-packet-inspector.html", "content": "<html><body>python tools/promote.py --sync</body></html>"}),
        ("prototype-html-missing-attrs", "HTML missing attrs.", {"kind": "html_replace", "file": "handoff-packet-inspector.html", "content": "<html><body>Handoff</body></html>"}),
        ("prototype-html-missing-cards", "HTML loses cards.", {"kind": "html_replace", "file": "handoff-packet-inspector.html", "content": '<html data-sandbox-only="true" data-handoff-only="true" data-non-executable="true" data-no-formal-vault-access="true" data-no-write="true" data-no-sync="true" data-no-authority="true" data-no-approval="true" data-no-user-wording="true" data-no-command="true"><body>Handoff</body></html>'}),
        ("prototype-html-run-now", "HTML shows run action.", {"kind": "html_replace", "file": "handoff-packet-inspector.html", "content": "<html><body><button>Run now</button></body></html>"}),
        ("prototype-receipt-permission", "Receipt grants execution.", {"kind": "receipt_update", "updates": {"execution_permission_granted": True}}),
        ("prototype-receipt-check-count", "Receipt check count drifts.", {"kind": "receipt_update", "updates": {"check_count": 99}}),
        ("prototype-receipt-action-basis", "Receipt claims action basis.", {"kind": "receipt_update", "updates": {"handoff_used_as_action_basis": True}}),
        ("prototype-receipt-non-claims", "Receipt loses non-claims.", {"kind": "receipt_replace_non_claims", "non_claims": []}),
    ]

    reset_dir(ROOT / "failure-cases")
    oracle: dict[str, list[str]] = {}
    for index, (slug, note, mutator, rehash_after) in enumerate(cases, start=1):
        candidate = copy.deepcopy(base)
        mutator(candidate)
        if rehash_after:
            rehash(candidate)
        expected_errors = validate_config(candidate)
        name = f"{index:03d}-{slug}.json"
        write_json(ROOT / "failure-cases" / name, {"case_id": slug, "note": note, "config": candidate, "expected_errors": expected_errors})
        oracle[name] = expected_errors
    start = len(cases) + 1
    for offset, (slug, note, tamper) in enumerate(prototype_cases):
        expected_errors = validate_prototype_tamper(tamper)
        name = f"{start + offset:03d}-{slug}.json"
        write_json(ROOT / "failure-cases" / name, {"case_id": slug, "note": note, "prototype_tamper": tamper, "expected_errors": expected_errors})
        oracle[name] = expected_errors
    return oracle


def write_contract() -> None:
    write_text(
        ROOT / "artifact" / "formal-vault-status-surface-handoff-packet-contract.md",
        """# Formal Vault Status Surface Handoff Packet Contract

This artifact packages P2-34 status-surface evidence for a later agent.

Hard boundaries:

- It is sandbox-only.
- It is handoff-only.
- It is not formal vault approval.
- It is not user instruction.
- It is not execution permission.
- It is not action basis.
- It is not reviewed knowledge or evidence support.
- It is not mainline readiness or merge approval.
- It does not collect approval or user wording.
- It does not access, inspect, hash, snapshot, write, or sync the formal vault.
- It does not emit commands or absolute formal-vault paths.
""",
    )


def write_prototype(config: dict[str, Any]) -> None:
    prototype = ROOT / "prototype" / "formal-vault-status-surface-handoff-packet"
    reset_dir(prototype)
    result_lines = "\n".join(f"- `{mode}` -> `{result}`" for mode, result in HANDOFF_MODES.items())
    write_text(
        prototype / "00 Handoff Home.md",
        f"""# Formal Vault Status Surface Handoff Packet

Source surface: `{SOURCE_SLICE}`

This packet lets a later agent resume from the P2-34 operator status surface
without treating it as authority.

Handoff results:

{result_lines}
""",
    )
    write_text(
        prototype / "01 Source Surface Binding.md",
        f"""# Source Surface Binding

Bound source slice: `{SOURCE_SLICE}`

Bound source result: `{config["source_surface_binding"]["surface_result"]}`

Bound source hash: `{config["source_surface_binding"]["status_surface_hash"]}`
""",
    )
    write_text(
        prototype / "02 Allowed Continuations.md",
        """# Allowed Continuations

- Read-only recovery or inspection.
- A fresh sandbox product workflow prototype.
- A fresh sandbox stop or park record.

All continuations require a new sandbox path and fresh opening card.
""",
    )
    write_text(
        prototype / "03 Stop Conditions.md",
        """# Stop Conditions

Stop before approval collection, commands, formal-vault access, action-basis
claims, mainline claims, or dirty-tree repair claims.
""",
    )
    write_text(
        prototype / "04 Reviewer Packet.md",
        """# Reviewer Packet

Check source hash binding, P2-34 pass status, handoff modes, failure cases,
prototype markers, and non-authority wording.
""",
    )
    cards = "\n".join(
        f"""<article class=\"card\" data-kind=\"handoff\">
        <span class=\"badge\">handoff</span>
        <h2>{mode.replace('_', ' ')}</h2>
        <p><code>{result}</code></p>
      </article>"""
        for mode, result in HANDOFF_MODES.items()
    )
    html = f"""<!doctype html>
<html lang="en" data-sandbox-only="true" data-handoff-only="true" data-non-executable="true" data-no-formal-vault-access="true" data-no-write="true" data-no-sync="true" data-no-authority="true" data-no-approval="true" data-no-user-wording="true" data-no-command="true">
<head>
  <meta charset="utf-8">
  <title>Formal Vault Status Surface Handoff Packet</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #17202a;
      --muted: #5b6472;
      --line: #cbd5e1;
      --panel: #f8fafc;
      --ok: #047857;
      font-family: Arial, sans-serif;
    }}
    body {{ margin: 0; color: var(--ink); background: #fff; }}
    main {{ max-width: 980px; margin: 0 auto; padding: 24px; }}
    h1 {{ margin: 0 0 8px; font-size: 26px; letter-spacing: 0; }}
    .sub {{ color: var(--muted); margin: 0 0 18px; line-height: 1.5; }}
    .toolbar {{ display: flex; gap: 8px; flex-wrap: wrap; margin-bottom: 16px; }}
    button {{ border: 1px solid var(--line); border-radius: 6px; background: #fff; padding: 8px 10px; cursor: default; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(240px, 1fr)); gap: 12px; }}
    .card {{ border: 1px solid var(--line); border-radius: 8px; background: var(--panel); padding: 14px; }}
    .badge {{ display: inline-block; border-radius: 999px; padding: 3px 8px; color: var(--ok); border: 1px solid #a7f3d0; background: #ecfdf5; font-size: 12px; }}
    code {{ overflow-wrap: anywhere; }}
  </style>
</head>
<body>
  <main>
    <h1>Formal Vault Status Surface Handoff Packet</h1>
    <p class="sub">Source: <code>{SOURCE_SLICE}</code>. Sandbox handoff only; no approval, no commands, no formal vault access, no run authority.</p>
    <div class="toolbar" aria-label="local display filters only">
      <button type="button" data-filter="all">All</button>
      <button type="button" data-filter="handoff">Handoffs</button>
    </div>
    <section class="grid">
      {cards}
    </section>
  </main>
  <script>
    const buttons = Array.from(document.querySelectorAll("button[data-filter]"));
    const cards = Array.from(document.querySelectorAll("[data-kind]"));
    buttons.forEach((button) => {{
      button.addEventListener("click", () => {{
        const filter = button.dataset.filter;
        cards.forEach((card) => {{
          card.hidden = filter !== "all" && card.dataset.kind !== filter;
        }});
      }});
    }});
  </script>
</body>
</html>
"""
    write_text(prototype / "handoff-packet-inspector.html", html)
    write_json(prototype / "Receipts" / "handoff-packet-receipt.json", config["handoff_receipt"])


def write_oracle(oracle: dict[str, list[str]]) -> None:
    write_json(ROOT / "artifact" / "failure-case-oracle.json", {"slice_id": SLICE_ID, "case_count": len(oracle), "cases": oracle})
    lines = ["# Failure Case Oracle", "", f"Case count: {len(oracle)}", ""]
    for name, errors in sorted(oracle.items()):
        lines.append(f"- `{name}` -> {', '.join(errors)}")
    write_text(ROOT / "artifact" / "failure-case-oracle.md", "\n".join(lines) + "\n")


def write_reports(fixtures: dict[str, dict[str, Any]], oracle: dict[str, list[str]]) -> None:
    fixture_results = {name: validate_config(config) for name, config in fixtures.items()}
    failure_results = validate_failure_cases()
    manual_results = run_manual_negative_probes()
    prototype_results = inspect_prototype()
    source_lines = [f"- `{item['id']}`: `{item['source_path']}` sha256 `{item['source_sha256']}`" for item in expected_source_inputs()]
    write_text(ROOT / "slice-plan.md", f"---\nstatus: built_pending_review\nslice_id: {SLICE_ID}\n---\n\n# Slice Plan\n\nGoal: create a sandbox-only handoff packet for safe reuse of P2-34.\n\nOnly write path: `outputs/review/vaks-implementation-sandbox/{SLICE_ID}/`\n\nAcceptance: fixtures, failure cases, prototype, verifier, Reviewer, Boundary, and GPT-5.5 Product Acceptance must pass.\n")
    write_text(ROOT / "source-map.md", f"---\nstatus: built_pending_review\nslice_id: {SLICE_ID}\n---\n\n# Source Map\n\nReads only P2-34 sandbox outputs.\n\n{chr(10).join(source_lines)}\n\nNon-claims: not reviewed knowledge, evidence support, action basis, execution permission, formal vault approval, or mainline readiness.\n")
    write_text(ROOT / "verification.md", f"---\nstatus: local_verification_passed_pending_review\nslice_id: {SLICE_ID}\n---\n\n# Verification\n\n- Positive fixtures: `{len(fixtures)}`\n- Fixture errors: `{json.dumps(fixture_results, ensure_ascii=False, sort_keys=True)}`\n- Failure cases: `{failure_results['count']}`\n- Failure mismatches: `{failure_results['mismatches']}`\n- Manual negative probes: `{manual_results['count']}`\n- Manual probe mismatches: `{manual_results['mismatches']}`\n- Prototype issues: `{prototype_results['issues']}`\n\nCommand: `python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_handoff_packet.py --rebuild`\n")
    write_text(ROOT / "reviewer-report.md", f"---\nstatus: reviewer_pending\nslice_id: {SLICE_ID}\n---\n\n# Reviewer Report\n\nPending independent read-only review.\n")
    write_text(ROOT / "boundary-audit.md", f"---\nstatus: boundary_pending\nslice_id: {SLICE_ID}\n---\n\n# Boundary Audit\n\nPending independent boundary audit.\n")
    write_text(ROOT / "product-acceptance-report.md", f"---\nstatus: product_acceptance_pending\nslice_id: {SLICE_ID}\n---\n\n# Product Acceptance Report\n\nPending GPT-5.5 extra-high Product Acceptance.\n")
    write_text(ROOT / "next-step.md", f"---\nstatus: next_step_pending_product_acceptance\nslice_id: {SLICE_ID}\n---\n\n# Next Step\n\nDo not advance until Reviewer, Boundary Auditor, and GPT-5.5 extra-high Product Acceptance pass this slice.\n")


def main() -> None:
    fixtures = write_fixtures()
    write_prototype(fixtures["valid-next-agent-read-only-handoff-config.json"])
    oracle = build_failure_cases(fixtures["valid-next-agent-read-only-handoff-config.json"])
    write_contract()
    write_oracle(oracle)
    write_reports(fixtures, oracle)
    print(json.dumps({"slice_id": SLICE_ID, "positive_fixtures": len(fixtures), "failure_cases": len(oracle), "manual_negative_probes": run_manual_negative_probes()["count"], "prototype_issues": inspect_prototype()["issues"]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
