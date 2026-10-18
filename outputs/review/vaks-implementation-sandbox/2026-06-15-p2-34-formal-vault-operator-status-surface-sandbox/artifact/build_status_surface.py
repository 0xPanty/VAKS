from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path
from typing import Any, Callable

from status_surface_common import (
    NON_CLAIMS,
    OPERATION_KEYS,
    ROOT,
    SLICE_ID,
    SOURCE_SLICES,
    STATUS_CONTROL_EXPECTED,
    STATUS_MODES,
    STATUS_SURFACE_PURPOSE,
    expected_badges,
    expected_operator_chain,
    expected_source_inputs,
    expected_source_statuses,
    expected_stop_lines,
    expected_surface_hash,
    inspect_prototype,
    read_only_sources,
    run_manual_negative_probes,
    validate_config,
    validate_failure_cases,
    validate_prototype_tamper,
    write_json,
    write_text,
)


FailureMutator = Callable[[dict[str, Any]], None]


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
    config["status_surface_hash"] = ""
    if isinstance(config.get("surface_receipt"), dict):
        config["surface_receipt"]["status_surface_hash"] = ""
    surface_hash = expected_surface_hash(config)
    config["status_surface_hash"] = surface_hash
    if isinstance(config.get("surface_receipt"), dict):
        config["surface_receipt"]["status_surface_hash"] = surface_hash


def base_operations() -> dict[str, bool]:
    return {key: False for key in OPERATION_KEYS}


def receipt_for_mode(mode: str) -> dict[str, Any]:
    return {
        "record_kind": "sandbox_formal_vault_operator_status_surface_receipt",
        "slice_id": SLICE_ID,
        "surface_result": STATUS_MODES[mode],
        "source_slice_count": len(SOURCE_SLICES),
        "source_input_count": len(read_only_sources()),
        "badge_count": len(expected_badges(mode)),
        "stop_line_count": len(expected_stop_lines()),
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
        "status_used_as_action_basis": False,
        "dirty_tree_fixed": False,
        "status_surface_hash": "",
        "non_claims": sorted(NON_CLAIMS),
    }


def make_config(mode: str) -> dict[str, Any]:
    config: dict[str, Any] = {
        "slice_id": SLICE_ID,
        "status_surface_version": "p2-34-formal-vault-operator-status-surface-v1",
        "truth_boundary": "sandbox_only_operator_status_not_authority",
        "purpose": STATUS_SURFACE_PURPOSE,
        "surface_mode": mode,
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": read_only_sources(),
        "operations": base_operations(),
        "status_controls": copy.deepcopy(STATUS_CONTROL_EXPECTED),
        "source_inputs": expected_source_inputs(),
        "source_statuses": expected_source_statuses(),
        "operator_chain": expected_operator_chain(),
        "status_badges": expected_badges(mode),
        "stop_lines": expected_stop_lines(),
        "surface_receipt": receipt_for_mode(mode),
        "product_metrics": {
            "required_positive_fixtures": 3,
            "minimum_failure_cases": 100,
            "source_slice_count": len(SOURCE_SLICES),
            "source_input_count": len(read_only_sources()),
            "manual_negative_probes": 12,
            "max_visible_stages": 4,
        },
        "status_surface_hash": "",
    }
    rehash(config)
    return config


def write_fixtures() -> dict[str, dict[str, Any]]:
    fixtures = {
        "valid-chain-overview-status-surface-config.json": make_config("chain_overview_surface"),
        "valid-latest-screening-focus-status-surface-config.json": make_config("latest_screening_focus_surface"),
        "valid-boundary-stop-focus-status-surface-config.json": make_config("boundary_stop_focus_surface"),
    }
    reset_dir(ROOT / "fixtures")
    for name, config in fixtures.items():
        write_json(ROOT / "fixtures" / name, config)
    return fixtures


def build_failure_cases(base: dict[str, Any]) -> dict[str, list[str]]:
    cases: list[tuple[str, str, FailureMutator, bool]] = []
    for op in OPERATION_KEYS:
        cases.append((f"operation-{op}", f"Operation flag {op} changed.", lambda cfg, key=op: set_path(cfg, ["operations", key], True), True))
    for control, expected in STATUS_CONTROL_EXPECTED.items():
        cases.append((f"control-{control}", f"Status control {control} changed.", lambda cfg, key=control, value=expected: set_path(cfg, ["status_controls", key], not value), True))
    for index in range(len(read_only_sources())):
        cases.append((f"source-input-{index}-sha-drift", "Source input hash changed.", lambda cfg, idx=index: set_path(cfg, ["source_inputs", idx, "source_sha256"], "0" * 64), True))
    for index in range(len(base["source_statuses"])):
        source_status = base["source_statuses"][index]
        slug = f"{source_status['slice_id']}-{source_status['file']}".replace(".", "-")
        cases.append((f"source-status-{slug}-drift", "Source status changed.", lambda cfg, idx=index: set_path(cfg, ["source_statuses", idx, "actual_status"], "pending"), True))
    for stage_index, stage in enumerate(base["operator_chain"]):
        for key, value in [
            ("product_status", "pending"),
            ("reviewer_status", "pending"),
            ("boundary_status", "pending"),
            ("verification_status", "pending"),
            ("next_status", "pending"),
            ("result_hash", "0" * 64),
            ("receipt_sha256", "1" * 64),
            ("formal_vault_accessed", True),
            ("approval_collected_now", True),
            ("user_wording_stored", True),
            ("execution_permission_granted", True),
            ("execution_performed", True),
            ("write_performed", True),
            ("sync_performed", True),
            ("promotion_performed", True),
            ("used_as_action_basis", True),
            ("submitted", True),
            ("non_claims", []),
        ]:
            cases.append((f"chain-{stage['stage_id']}-{key}", f"Operator chain {stage['stage_id']} {key} changed.", lambda cfg, idx=stage_index, k=key, v=value: set_path(cfg, ["operator_chain", idx, k], v), True))
    for index, badge in enumerate(base["status_badges"]):
        cases.append((f"badge-{badge['badge_id']}-status", "Badge status changed.", lambda cfg, idx=index: set_path(cfg, ["status_badges", idx, "status"], "READY"), True))
        cases.append((f"badge-{badge['badge_id']}-authority", "Badge becomes authority.", lambda cfg, idx=index: set_path(cfg, ["status_badges", idx, "non_authority"], False), True))
    for index, stop in enumerate(base["stop_lines"]):
        cases.append((f"stop-line-{stop['stop_id']}-not-stop", "Stop line no longer stops.", lambda cfg, idx=index: set_path(cfg, ["stop_lines", idx, "must_stop"], False), True))
        cases.append((f"stop-line-{stop['stop_id']}-reason-command", "Stop line reason contains command.", lambda cfg, idx=index: set_path(cfg, ["stop_lines", idx, "reason"], "python tools/promote.py --sync"), True))
    for key, value in [
        ("record_kind", "wrong_kind"),
        ("slice_id", "wrong-slice"),
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
        ("commit_performed", True),
        ("push_performed", True),
        ("promotion_performed", True),
        ("mainline_ready", True),
        ("status_used_as_action_basis", True),
        ("dirty_tree_fixed", True),
        ("status_surface_hash", "2" * 64),
        ("non_claims", []),
    ]:
        rehash_after = key != "status_surface_hash"
        cases.append((f"receipt-{key}", f"Receipt {key} changed.", lambda cfg, k=key, v=value: set_path(cfg, ["surface_receipt", k], v), rehash_after))
    for key, value in [
        ("required_positive_fixtures", 2),
        ("minimum_failure_cases", 99),
        ("source_slice_count", 99),
        ("source_input_count", 99),
        ("manual_negative_probes", 11),
        ("max_visible_stages", 5),
    ]:
        cases.append((f"metric-{key}", f"Metric {key} changed.", lambda cfg, k=key, v=value: set_path(cfg, ["product_metrics", k], v), True))
    cases.extend(
        [
            ("top-level-slice-id", "Slice id changed.", lambda cfg: set_path(cfg, ["slice_id"], "wrong-slice"), True),
            ("top-level-version", "Version changed.", lambda cfg: set_path(cfg, ["status_surface_version"], "wrong-version"), True),
            ("top-level-boundary", "Truth boundary changed.", lambda cfg: set_path(cfg, ["truth_boundary"], "wrong-boundary"), True),
            ("top-level-purpose", "Purpose changed.", lambda cfg: set_path(cfg, ["purpose"], "different purpose"), True),
            ("top-level-mode", "Mode changed.", lambda cfg: set_path(cfg, ["surface_mode"], "wrong-mode"), True),
            ("top-level-write-scope", "Write scope changed.", lambda cfg: set_path(cfg, ["write_scope"], ["outputs/review/other/"]), True),
            ("top-level-read-sources", "Read-only sources changed.", lambda cfg: set_path(cfg, ["read_only_sources"], []), True),
            ("top-level-extra-key", "Unknown key added.", lambda cfg: cfg.update({"unexpected": "value"}), True),
            ("top-level-command-string", "Unknown key contains command.", lambda cfg: cfg.update({"unexpected": "python tools/promote.py --sync"}), True),
            ("hash-drift", "Top-level hash changed.", lambda cfg: set_path(cfg, ["status_surface_hash"], "3" * 64), False),
        ]
    )
    prototype_cases: list[tuple[str, str, dict[str, Any]]] = [
        ("prototype-markdown-command", "Prototype contains command.", {"kind": "markdown_replace", "file": "04 Reviewer Packet.md", "content": "python tools/promote.py --sync"}),
        ("prototype-markdown-execution-permission", "Prototype grants execution.", {"kind": "markdown_replace", "file": "03 Stop Lines.md", "content": "execution permission: granted"}),
        ("prototype-markdown-formal-vault-approval", "Prototype grants formal approval.", {"kind": "markdown_replace", "file": "02 Status Badges.md", "content": "formal vault approval: yes"}),
        ("prototype-markdown-action-basis", "Prototype claims action basis.", {"kind": "markdown_replace", "file": "01 Evidence Chain.md", "content": "action basis: yes"}),
        ("prototype-markdown-mainline-ready", "Prototype claims mainline readiness.", {"kind": "markdown_replace", "file": "00 Operator Status Home.md", "content": "mainline ready: yes"}),
        ("prototype-markdown-user-wording", "Prototype stores user wording.", {"kind": "markdown_replace", "file": "04 Reviewer Packet.md", "content": "actual user wording: approve now"}),
        ("prototype-markdown-may-execute", "Prototype permits execution.", {"kind": "markdown_replace", "file": "03 Stop Lines.md", "content": "The operator may execute."}),
        ("prototype-markdown-missing-chain", "Prototype home loses displayed chain.", {"kind": "markdown_replace", "file": "00 Operator Status Home.md", "content": "# Formal Vault Operator Status Surface\n\nOnly a generic status page.\n"}),
        ("prototype-html-command", "HTML contains command.", {"kind": "html_replace", "file": "operator-status-surface.html", "content": "<html><body>python tools/promote.py --sync</body></html>"}),
        ("prototype-html-missing-attrs", "HTML missing boundary attrs.", {"kind": "html_replace", "file": "operator-status-surface.html", "content": "<html><body>Status</body></html>"}),
        ("prototype-html-missing-chain", "HTML loses displayed chain.", {"kind": "html_replace", "file": "operator-status-surface.html", "content": '<html data-sandbox-only="true" data-status-only="true" data-non-executable="true" data-no-formal-vault-access="true" data-no-write="true" data-no-sync="true" data-no-authority="true" data-no-approval="true" data-no-user-wording="true" data-no-command="true"><body>Status surface</body></html>'}),
        ("prototype-html-start-execution", "HTML shows run action.", {"kind": "html_replace", "file": "operator-status-surface.html", "content": "<html><body><button>Start execution</button></body></html>"}),
        ("prototype-receipt-badge-count", "Receipt badge count drifts.", {"kind": "receipt_update", "updates": {"badge_count": 99}}),
        ("prototype-receipt-stop-line-count", "Receipt stop line count drifts.", {"kind": "receipt_update", "updates": {"stop_line_count": 99}}),
        ("prototype-receipt-permission", "Receipt grants execution.", {"kind": "receipt_update", "updates": {"execution_permission_granted": True}}),
        ("prototype-receipt-action-basis", "Receipt claims action basis.", {"kind": "receipt_update", "updates": {"status_used_as_action_basis": True}}),
        ("prototype-receipt-mainline", "Receipt claims mainline readiness.", {"kind": "receipt_update", "updates": {"mainline_ready": True}}),
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
        ROOT / "artifact" / "formal-vault-operator-status-surface-contract.md",
        """# Formal Vault Operator Status Surface Contract

This artifact is a sandbox-only status and navigation surface for P2-30 through
P2-33 formal-vault safety artifacts.

Hard boundaries:

- It displays status only.
- It is not formal vault approval.
- It is not user instruction.
- It is not execution permission.
- It is not action basis.
- It is not reviewed knowledge.
- It is not evidence support.
- It is not mainline readiness.
- It does not collect approval or user wording.
- It does not access, inspect, hash, snapshot, write, or sync the formal vault.
- It does not emit commands or absolute formal-vault paths.
""",
    )


def write_prototype(config: dict[str, Any]) -> None:
    prototype = ROOT / "prototype" / "formal-vault-operator-status-surface"
    reset_dir(prototype)
    chain_lines = "\n".join(
        f"- {item['label']}: `{item['slice_id']}` / {item['product_status']} / {item['result_label']}" for item in config["operator_chain"]
    )
    write_text(
        prototype / "00 Operator Status Home.md",
        f"""# Formal Vault Operator Status Surface

Slice: {SLICE_ID}

This surface shows the sandbox product-grade chain from P2-30 to P2-33. It is a
read-only operator view and a stop surface.

Visible chain:

{chain_lines}
""",
    )
    write_text(
        prototype / "01 Evidence Chain.md",
        """# Evidence Chain

The surface binds each displayed stage to its Product Acceptance report,
Reviewer report, Boundary audit, verification file, next-step file, contract,
and receipt by SHA256.

Every displayed stage remains sandbox-only and non-executing.
""",
    )
    write_text(
        prototype / "02 Status Badges.md",
        """# Status Badges

- Sandbox product-grade chain: displayed stages passed Product Acceptance.
- Formal vault untouched: displayed receipts record no vault touch.
- No approval collected: displayed receipts record no approval capture.
- Not mainline-ready: this is status/navigation only.

Badges explain state. Badges do not grant authority.
""",
    )
    write_text(
        prototype / "03 Stop Lines.md",
        """# Stop Lines

- Stop before execution.
- Stop before approval collection.
- Stop before formal vault access.
- Stop before mainline merge.

The next agent must open a fresh approved sandbox slice for any further work.
""",
    )
    write_text(
        prototype / "04 Reviewer Packet.md",
        """# Reviewer Packet

Check that the surface:

- reads only P2-30 through P2-33 sandbox artifacts,
- binds source hashes,
- validates all visible statuses,
- has no form, download, storage, network, command, or vault action,
- never turns status into authority.
""",
    )
    cards = "\n".join(
        f"""<article class=\"card\" data-kind=\"stage\">
        <span class=\"badge\">{item['product_status']}</span>
        <h2>{item['label']}</h2>
        <p><code>{item['slice_id']}</code></p>
        <dl>
          <dt>Result</dt><dd>{item['result_label']}</dd>
          <dt>Reviewer</dt><dd>{item['reviewer_status']}</dd>
          <dt>Boundary</dt><dd>{item['boundary_status']}</dd>
        </dl>
      </article>"""
        for item in config["operator_chain"]
    )
    html = f"""<!doctype html>
<html lang="en" data-sandbox-only="true" data-status-only="true" data-non-executable="true" data-no-formal-vault-access="true" data-no-write="true" data-no-sync="true" data-no-authority="true" data-no-approval="true" data-no-user-wording="true" data-no-command="true">
<head>
  <meta charset="utf-8">
  <title>Formal Vault Operator Status Surface</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #18212f;
      --muted: #5b6472;
      --line: #cbd5e1;
      --panel: #f8fafc;
      --ok: #047857;
      --stop: #b91c1c;
      --warn: #92400e;
      font-family: Arial, sans-serif;
    }}
    body {{
      margin: 0;
      background: #ffffff;
      color: var(--ink);
    }}
    main {{
      max-width: 1080px;
      margin: 0 auto;
      padding: 24px;
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 26px;
      letter-spacing: 0;
    }}
    .sub {{
      margin: 0 0 20px;
      color: var(--muted);
      line-height: 1.5;
    }}
    .toolbar {{
      display: flex;
      flex-wrap: wrap;
      gap: 8px;
      margin-bottom: 16px;
    }}
    button {{
      border: 1px solid var(--line);
      border-radius: 6px;
      background: #fff;
      padding: 8px 10px;
      font-size: 14px;
      cursor: default;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
      gap: 12px;
    }}
    .card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      background: var(--panel);
    }}
    .badge {{
      display: inline-block;
      border: 1px solid #a7f3d0;
      color: var(--ok);
      background: #ecfdf5;
      border-radius: 999px;
      padding: 3px 8px;
      font-size: 12px;
    }}
    .stop {{
      border-color: #fecaca;
      color: var(--stop);
      background: #fef2f2;
    }}
    h2 {{
      font-size: 18px;
      margin: 10px 0 8px;
    }}
    code {{
      overflow-wrap: anywhere;
    }}
    dl {{
      margin: 10px 0 0;
      display: grid;
      grid-template-columns: 72px 1fr;
      gap: 6px;
    }}
    dt {{
      color: var(--muted);
    }}
    dd {{
      margin: 0;
    }}
  </style>
</head>
<body>
  <main>
    <h1>Formal Vault Operator Status Surface</h1>
    <p class="sub">Read-only sandbox surface for P2-30 through P2-33. It displays status and stop lines only; it does not collect approval, send packets, touch the formal vault, or create run authority.</p>
    <div class="toolbar" aria-label="local display filters only">
      <button type="button" data-filter="all">All</button>
      <button type="button" data-filter="stage">Stages</button>
      <button type="button" data-filter="stop">Stops</button>
    </div>
    <section class="grid">
      {cards}
      <article class="card" data-kind="stop">
        <span class="badge stop">Stop</span>
        <h2>Execution remains closed</h2>
        <p>No displayed artifact grants run authority, formal-vault access, action basis, or mainline readiness.</p>
      </article>
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
    write_text(prototype / "operator-status-surface.html", html)
    write_json(prototype / "Receipts" / "operator-status-surface-receipt.json", config["surface_receipt"])


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
    source_lines = [
        f"- `{item['id']}`: `{item['source_path']}` sha256 `{item['source_sha256']}`"
        for item in expected_source_inputs()
    ]
    write_text(
        ROOT / "slice-plan.md",
        f"""---
status: built_pending_review
slice_id: {SLICE_ID}
---

# Slice Plan

## Goal

Create a sandbox-only operator status surface for the P2-30 through P2-33
formal-vault safety chain.

## Only Write Path

`outputs/review/vaks-implementation-sandbox/{SLICE_ID}/`

## Acceptance

- Three positive fixtures validate.
- Failure cases fail closed.
- Prototype HTML, Markdown, and receipt validate.
- P2-30 through P2-33 statuses and source hashes are bound.
- Reviewer, Boundary, and GPT-5.5 extra-high Product Acceptance pass.

## Stop Conditions

Stop on formal-vault access, approval capture, user wording storage, command
emission, action-basis claims, execution permission claims, mainline readiness
claims, commit, push, sync, or promotion.
""",
    )
    write_text(
        ROOT / "source-map.md",
        f"""---
status: built_pending_review
slice_id: {SLICE_ID}
---

# Source Map

This slice reads only sandbox outputs from P2-30 through P2-33.

## Read-Only Inputs

{chr(10).join(source_lines)}

## Non-Claims

This source map is not reviewed knowledge, evidence support, action basis,
formal-vault approval, execution permission, mainline readiness, or user
instruction.
""",
    )
    write_text(
        ROOT / "verification.md",
        f"""---
status: local_verification_passed_pending_review
slice_id: {SLICE_ID}
---

# Verification

## Local Build Result

- Positive fixtures: `{len(fixtures)}`
- Fixture validation errors: `{json.dumps(fixture_results, ensure_ascii=False, sort_keys=True)}`
- Failure cases: `{failure_results["count"]}`
- Failure mismatches: `{failure_results["mismatches"]}`
- Manual negative probes: `{manual_results["count"]}`
- Manual probe mismatches: `{manual_results["mismatches"]}`
- Prototype issues: `{prototype_results["issues"]}`

## Commands Used

- `python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_status_surface.py --rebuild`

## Boundary Result

The local verification checks source hashes, upstream statuses, generated
failure cases, manual negative probes, prototype Markdown, prototype HTML, and
prototype receipt. It does not inspect or change the formal vault.
""",
    )
    write_text(ROOT / "reviewer-report.md", f"---\nstatus: reviewer_pending\nslice_id: {SLICE_ID}\n---\n\n# Reviewer Report\n\nPending independent read-only review.\n")
    write_text(ROOT / "boundary-audit.md", f"---\nstatus: boundary_pending\nslice_id: {SLICE_ID}\n---\n\n# Boundary Audit\n\nPending independent boundary audit.\n")
    write_text(ROOT / "product-acceptance-report.md", f"---\nstatus: product_acceptance_pending\nslice_id: {SLICE_ID}\n---\n\n# Product Acceptance Report\n\nPending GPT-5.5 extra-high Product Acceptance.\n")
    write_text(ROOT / "next-step.md", f"---\nstatus: next_step_pending_product_acceptance\nslice_id: {SLICE_ID}\n---\n\n# Next Step\n\nDo not advance until Reviewer, Boundary Auditor, and GPT-5.5 extra-high Product Acceptance pass this slice.\n")


def main() -> None:
    fixtures = write_fixtures()
    write_prototype(fixtures["valid-chain-overview-status-surface-config.json"])
    oracle = build_failure_cases(fixtures["valid-chain-overview-status-surface-config.json"])
    write_contract()
    write_oracle(oracle)
    write_reports(fixtures, oracle)
    print(json.dumps({"slice_id": SLICE_ID, "positive_fixtures": len(fixtures), "failure_cases": len(oracle), "manual_negative_probes": run_manual_negative_probes()["count"], "prototype_issues": inspect_prototype()["issues"]}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
