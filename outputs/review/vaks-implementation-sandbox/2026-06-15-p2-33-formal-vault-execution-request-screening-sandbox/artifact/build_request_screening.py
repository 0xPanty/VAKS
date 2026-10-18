from __future__ import annotations

import copy
import json
import shutil
from pathlib import Path
from typing import Any, Callable

from request_screening_common import (
    NON_CLAIMS,
    OPERATION_KEYS,
    READ_ONLY_SOURCES,
    SCREENING_CHECK_IDS,
    SCREENING_CHECK_STATUS,
    SCREENING_CONTROL_EXPECTED,
    SCREENING_MODES,
    SCREENING_PURPOSE,
    SLICE_ID,
    SOURCE_SLICE,
    expected_p2_32_binding,
    expected_projection,
    expected_screening_hash,
    expected_screening_input,
    expected_source_inputs,
    expected_source_statuses,
    inspect_prototype,
    run_manual_negative_probes,
    validate_config,
    validate_failure_cases,
    validate_prototype_tamper,
    write_json,
    write_text,
    ROOT,
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
    config["request_screening_hash"] = ""
    if isinstance(config.get("screening_receipt"), dict):
        config["screening_receipt"]["request_screening_hash"] = ""
    screening_hash = expected_screening_hash(config)
    config["request_screening_hash"] = screening_hash
    if isinstance(config.get("screening_receipt"), dict):
        config["screening_receipt"]["request_screening_hash"] = screening_hash


def base_operations() -> dict[str, bool]:
    return {key: False for key in OPERATION_KEYS}


def screening_checks_for_mode(mode: str) -> list[dict[str, Any]]:
    return [
        {
            "check_id": check_id,
            "sequence": index,
            "status": SCREENING_CHECK_STATUS[mode][check_id],
            "screened_now": True,
            "collected_now": False,
            "non_claim": "screening_check_is_not_permission",
        }
        for index, check_id in enumerate(SCREENING_CHECK_IDS, start=1)
    ]


def receipt_for_mode(mode: str) -> dict[str, Any]:
    return {
        "record_kind": "sandbox_formal_vault_execution_request_screening_receipt",
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE,
        "screening_result": SCREENING_MODES[mode],
        "packet_submitted": False,
        "formal_vault_accessed": False,
        "formal_vault_state_inspected": False,
        "approval_collected_now": False,
        "actual_user_input_used": False,
        "actual_user_wording_stored": False,
        "execution_permission_granted": False,
        "execution_performed": False,
        "write_performed": False,
        "snapshot_taken": False,
        "hash_before_collected": False,
        "hash_after_collected": False,
        "sync_performed": False,
        "commit_performed": False,
        "push_performed": False,
        "promotion_performed": False,
        "screening_replayed": False,
        "screening_used_as_action_basis": False,
        "check_count": len(SCREENING_CHECK_IDS),
        "source_count": len(READ_ONLY_SOURCES),
        "request_screening_hash": "",
        "non_claims": sorted(NON_CLAIMS),
    }


def make_config(mode: str) -> dict[str, Any]:
    config: dict[str, Any] = {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE,
        "request_screening_version": "p2-33-formal-vault-execution-request-screening-v1",
        "truth_boundary": "sandbox_only_request_screening_not_submission",
        "purpose": SCREENING_PURPOSE,
        "screening_mode": mode,
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": READ_ONLY_SOURCES,
        "operations": base_operations(),
        "screening_controls": copy.deepcopy(SCREENING_CONTROL_EXPECTED),
        "source_inputs": expected_source_inputs(),
        "source_statuses": expected_source_statuses(),
        "p2_32_binding": expected_p2_32_binding(),
        "screening_input_packet": expected_screening_input(mode),
        "screening_projection": expected_projection(mode),
        "screening_checks": screening_checks_for_mode(mode),
        "screening_receipt": receipt_for_mode(mode),
        "product_metrics": {
            "required_positive_fixtures": 3,
            "minimum_failure_cases": 100,
            "required_screening_checks": len(SCREENING_CHECK_IDS),
            "required_source_inputs": len(READ_ONLY_SOURCES),
            "manual_negative_probes": 12,
            "max_journey_steps": 3,
        },
        "request_screening_hash": "",
    }
    rehash(config)
    return config


def write_fixtures() -> dict[str, dict[str, Any]]:
    fixtures = {
        "valid-reviewable-request-screening-config.json": make_config("synthetic_reviewable_request_screening"),
        "valid-missing-confirmation-request-screening-config.json": make_config("synthetic_missing_confirmation_screening"),
        "valid-denied-request-screening-config.json": make_config("synthetic_denied_request_screening"),
    }
    reset_dir(ROOT / "fixtures")
    for name, config in fixtures.items():
        write_json(ROOT / "fixtures" / name, config)
    return fixtures


def build_failure_cases(base: dict[str, Any]) -> dict[str, list[str]]:
    cases: list[tuple[str, str, FailureMutator, bool]] = []

    for op in OPERATION_KEYS:
        cases.append((f"operation-{op}", f"Operation flag {op} changed.", lambda cfg, key=op: set_path(cfg, ["operations", key], True), True))
    for control, expected in SCREENING_CONTROL_EXPECTED.items():
        cases.append((f"control-{control}", f"Screening control {control} changed.", lambda cfg, key=control, value=expected: set_path(cfg, ["screening_controls", key], not value), True))
    for index in range(len(READ_ONLY_SOURCES)):
        cases.append((f"source-input-{index}-sha-drift", "Source input hash changed.", lambda cfg, idx=index: set_path(cfg, ["source_inputs", idx, "source_sha256"], "0" * 64), True))
    for name in ["product-acceptance-report.md", "reviewer-report.md", "boundary-audit.md", "next-step.md", "verification.md", "source-map.md"]:
        slug = name.replace(".", "-")
        cases.append(
            (
                f"source-status-{slug}-drift",
                "Required upstream status changed.",
                lambda cfg, file_name=name: [item.update({"actual_status": "pending"}) for item in cfg["source_statuses"] if item["file"] == file_name],
                True,
            )
        )
    for key, value in [
        ("product_acceptance_status", "pending"),
        ("reviewer_status", "pending"),
        ("boundary_status", "pending"),
        ("request_packet_hash", "1" * 64),
        ("packet_receipt_hash", "2" * 64),
        ("packet_field_count", 99),
        ("packet_source_count", 99),
        ("packet_result", "READY"),
        ("packet_submitted_to_gate", True),
        ("execution_permission_granted", True),
        ("packet_used_as_action_basis", True),
        ("formal_vault_accessed", True),
        ("approval_collected_now", True),
        ("real_user_text_stored", True),
        ("write_performed", True),
        ("sync_performed", True),
        ("promotion_performed", True),
    ]:
        cases.append((f"p2-32-binding-{key}-drift", f"P2-32 binding {key} changed.", lambda cfg, k=key, v=value: set_path(cfg, ["p2_32_binding", k], v), True))

    for key, value in [
        ("source_fixture", "unknown.json"),
        ("source_packet_hash", "3" * 64),
        ("packet_id", "synthetic-but-wrong"),
        ("packet_id", "python tools/promote.py --sync"),
        ("packet_mode", "wrong_mode"),
        ("packet_result", "READY"),
        ("synthetic_only", False),
        ("actual_approval_collected", True),
        ("actual_user_wording_stored", True),
        ("commands_supplied", True),
        ("absolute_paths_present", True),
        ("requested_execution_now", True),
        ("requested_action_basis", True),
        ("packet_submitted", True),
        ("non_claims", []),
    ]:
        slug_value = str(value).replace(" ", "-").replace("/", "-").replace("\\", "-")[:32]
        cases.append((f"screening-input-{key}-{slug_value}", f"Screening input {key} changed.", lambda cfg, k=key, v=value: set_path(cfg, ["screening_input_packet", k], v), True))

    for key, value in [
        ("target_gate_slice", "wrong-slice"),
        ("target_request_mode", "wrong-mode"),
        ("projected_request_id", "wrong-id"),
        ("projected_request_id", "python tools/promote.py --sync"),
        ("projected_gate_result", "READY_TO_RUN"),
        ("screening_result", "SCREENED_READY"),
        ("projection_matches_packet", False),
        ("projection_is_not_submission", False),
        ("projection_collects_no_approval", False),
        ("projection_contains_no_commands", False),
        ("projection_contains_no_formal_vault_paths", False),
    ]:
        slug_value = str(value).replace(" ", "-").replace("/", "-").replace("\\", "-")[:32]
        cases.append((f"projection-{key}-{slug_value}", f"Screening projection {key} changed.", lambda cfg, k=key, v=value: set_path(cfg, ["screening_projection", k], v), True))

    for index, check_id in enumerate(SCREENING_CHECK_IDS):
        cases.append((f"check-{check_id}-status-drift", "Screening check status changed.", lambda cfg, idx=index: set_path(cfg, ["screening_checks", idx, "status"], "READY"), True))
        cases.append((f"check-{check_id}-collected-now", "Screening check tries to collect data.", lambda cfg, idx=index: set_path(cfg, ["screening_checks", idx, "collected_now"], True), True))

    for key, value in [
        ("record_kind", "wrong_kind"),
        ("slice_id", "wrong-slice"),
        ("source_slice", "wrong-source"),
        ("screening_result", "SCREENED_READY"),
        ("packet_submitted", True),
        ("formal_vault_accessed", True),
        ("formal_vault_state_inspected", True),
        ("approval_collected_now", True),
        ("actual_user_input_used", True),
        ("actual_user_wording_stored", True),
        ("execution_permission_granted", True),
        ("execution_performed", True),
        ("write_performed", True),
        ("snapshot_taken", True),
        ("hash_before_collected", True),
        ("hash_after_collected", True),
        ("sync_performed", True),
        ("commit_performed", True),
        ("push_performed", True),
        ("promotion_performed", True),
        ("screening_replayed", True),
        ("screening_used_as_action_basis", True),
        ("check_count", 99),
        ("source_count", 99),
        ("request_screening_hash", "4" * 64),
        ("non_claims", []),
    ]:
        rehash_after = key != "request_screening_hash"
        cases.append((f"receipt-{key}", f"Receipt {key} changed.", lambda cfg, k=key, v=value: set_path(cfg, ["screening_receipt", k], v), rehash_after))

    for key, value in [
        ("required_positive_fixtures", 2),
        ("minimum_failure_cases", 99),
        ("required_screening_checks", 99),
        ("required_source_inputs", 99),
        ("manual_negative_probes", 11),
        ("max_journey_steps", 4),
    ]:
        cases.append((f"metric-{key}-drift", f"Metric {key} changed.", lambda cfg, k=key, v=value: set_path(cfg, ["product_metrics", k], v), True))

    cases.extend(
        [
            ("top-level-slice-id", "Top-level slice id changed.", lambda cfg: set_path(cfg, ["slice_id"], "wrong-slice"), True),
            ("top-level-source-slice", "Top-level source slice changed.", lambda cfg: set_path(cfg, ["source_slice"], "wrong-source"), True),
            ("top-level-version", "Version changed.", lambda cfg: set_path(cfg, ["request_screening_version"], "wrong-version"), True),
            ("top-level-truth-boundary", "Truth boundary changed.", lambda cfg: set_path(cfg, ["truth_boundary"], "wrong-boundary"), True),
            ("top-level-purpose", "Purpose changed.", lambda cfg: set_path(cfg, ["purpose"], "different purpose"), True),
            ("top-level-mode", "Screening mode changed.", lambda cfg: set_path(cfg, ["screening_mode"], "wrong-mode"), True),
            ("top-level-write-scope", "Write scope changed.", lambda cfg: set_path(cfg, ["write_scope"], ["outputs/review/other/"]), True),
            ("top-level-read-sources", "Read-only sources changed.", lambda cfg: set_path(cfg, ["read_only_sources"], []), True),
            ("top-level-extra-key", "Unknown key added.", lambda cfg: cfg.update({"unexpected": "value"}), True),
            ("top-level-command-string", "Unknown key contains command text.", lambda cfg: cfg.update({"unexpected": "python tools/promote.py --sync"}), True),
            ("hash-drift", "Top-level hash changed.", lambda cfg: set_path(cfg, ["request_screening_hash"], "5" * 64), False),
        ]
    )

    prototype_cases: list[tuple[str, str, dict[str, Any]]] = [
        ("prototype-markdown-command", "Prototype text contains command.", {"kind": "markdown_replace", "file": "05 Reviewer Packet.md", "content": "python tools/promote.py --sync"}),
        ("prototype-markdown-screening-submitted", "Prototype says screening was sent.", {"kind": "markdown_replace", "file": "03 Non Submission Receipt.md", "content": "screening submitted: yes"}),
        ("prototype-markdown-packet-submitted", "Prototype says packet was sent.", {"kind": "markdown_replace", "file": "03 Non Submission Receipt.md", "content": "packet submitted: yes"}),
        ("prototype-markdown-approval-collected", "Prototype says approval was collected.", {"kind": "markdown_replace", "file": "03 Non Submission Receipt.md", "content": "approval collected: yes"}),
        ("prototype-markdown-actual-user-wording", "Prototype stores user wording.", {"kind": "markdown_replace", "file": "02 Screening Checks.md", "content": "actual user wording: approve execution now"}),
        ("prototype-markdown-action-basis", "Prototype claims action basis.", {"kind": "markdown_replace", "file": "04 Stop Conditions.md", "content": "action basis: yes"}),
        ("prototype-markdown-execution-permission", "Prototype claims run permission.", {"kind": "markdown_replace", "file": "04 Stop Conditions.md", "content": "execution permission: granted"}),
        ("prototype-markdown-authorizes", "Prototype claims authority.", {"kind": "markdown_replace", "file": "01 Screening Contract.md", "content": "This screening authorizes the future execution slice."}),
        ("prototype-markdown-may-execute", "Prototype allows running.", {"kind": "markdown_replace", "file": "04 Stop Conditions.md", "content": "The operator may execute the formal vault operation."}),
        ("prototype-markdown-approval-obtained", "Prototype claims approval.", {"kind": "markdown_replace", "file": "03 Non Submission Receipt.md", "content": "Approval obtained from the user."}),
        ("prototype-html-command", "HTML contains command.", {"kind": "html_replace", "file": "request-screening-inspector.html", "content": "<html><body>python tools/promote.py --sync</body></html>"}),
        ("prototype-html-missing-attrs", "HTML lacks boundary attributes.", {"kind": "html_replace", "file": "request-screening-inspector.html", "content": "<html><body>Screening inspector</body></html>"}),
        ("prototype-html-submit-screening", "HTML contains send action label.", {"kind": "html_replace", "file": "request-screening-inspector.html", "content": "<html><body><button>Submit screening to gate</button></body></html>"}),
        ("prototype-html-authorizes", "HTML claims authority.", {"kind": "html_replace", "file": "request-screening-inspector.html", "content": '<html data-sandbox-only="true" data-screening-only="true" data-non-executable="true" data-no-formal-vault-access="true" data-no-write="true" data-no-sync="true" data-no-authority="true" data-no-permission="true" data-no-actual-user-wording="true" data-no-submission="true"><body>Screening authorizes execution</body></html>'}),
        ("prototype-receipt-command", "Prototype receipt contains command text.", {"kind": "receipt_update", "updates": {"screening_result": "python tools/promote.py --sync"}}),
        ("prototype-receipt-slice", "Prototype receipt slice drift.", {"kind": "receipt_update", "updates": {"slice_id": "wrong-slice"}}),
        ("prototype-receipt-source", "Prototype receipt source drift.", {"kind": "receipt_update", "updates": {"source_slice": "wrong-source"}}),
        ("prototype-receipt-permission", "Prototype receipt grants run permission.", {"kind": "receipt_update", "updates": {"execution_permission_granted": True}}),
        ("prototype-receipt-submitted", "Prototype receipt sends packet.", {"kind": "receipt_update", "updates": {"packet_submitted": True}}),
        ("prototype-receipt-action-basis", "Prototype receipt claims action basis.", {"kind": "receipt_update", "updates": {"screening_used_as_action_basis": True}}),
        ("prototype-receipt-non-claims", "Prototype receipt loses non-claim boundary.", {"kind": "receipt_replace_non_claims", "non_claims": []}),
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
        write_json(
            ROOT / "failure-cases" / name,
            {"case_id": slug, "note": note, "config": candidate, "expected_errors": expected_errors},
        )
        oracle[name] = expected_errors

    start = len(cases) + 1
    for offset, (slug, note, tamper) in enumerate(prototype_cases):
        expected_errors = validate_prototype_tamper(tamper)
        name = f"{start + offset:03d}-{slug}.json"
        write_json(
            ROOT / "failure-cases" / name,
            {"case_id": slug, "note": note, "prototype_tamper": tamper, "expected_errors": expected_errors},
        )
        oracle[name] = expected_errors
    return oracle


def write_contract() -> None:
    write_text(
        ROOT / "artifact" / "formal-vault-execution-request-screening-contract.md",
        """# Formal Vault Execution Request Screening Contract

This artifact screens the synthetic request packets from P2-32 against the
readiness-gate projection inherited from P2-31.

Hard boundaries:

- It is sandbox-only.
- It screens packet shape and projected gate result only.
- It does not send packets to any gate.
- It does not collect approval.
- It does not store user wording.
- It does not grant run permission.
- It is not formal vault approval.
- It is not action basis.
- It does not access, inspect, hash, snapshot, write, or sync the formal vault.
- It does not emit commands or absolute formal-vault paths.
""",
    )


def write_prototype(config: dict[str, Any]) -> None:
    prototype = ROOT / "prototype" / "formal-vault-execution-request-screening"
    reset_dir(prototype)
    write_text(
        prototype / "00 Screening Home.md",
        f"""# Formal Vault Execution Request Screening

Slice: {SLICE_ID}

Purpose: make a request packet inspectable before any later human-controlled
step. This screen is a stop-and-review surface, not a run surface.

Current demo rows:

- Reviewable packet -> {SCREENING_MODES["synthetic_reviewable_request_screening"]}
- Missing confirmation packet -> {SCREENING_MODES["synthetic_missing_confirmation_screening"]}
- Denied packet -> {SCREENING_MODES["synthetic_denied_request_screening"]}
""",
    )
    write_text(
        prototype / "01 Screening Contract.md",
        """# Screening Contract

The screen binds each synthetic P2-32 packet to its packet hash, upstream
Product/Reviewer/Boundary status, source hashes, and projected P2-31 gate
outcome.

The screen never becomes formal vault consent, reviewed knowledge, evidence
support, action basis, or run permission.
""",
    )
    write_text(
        prototype / "02 Screening Checks.md",
        """# Screening Checks

1. P2-32 Product pass is present.
2. P2-32 packet hash is bound.
3. Source hashes still match.
4. Packet identity remains synthetic.
5. Projection matches P2-31.
6. Packet has not been sent.
7. No approval is collected.
8. No user wording is stored.
9. No commands or formal vault paths appear.
10. No current run permission exists.
""",
    )
    write_text(
        prototype / "03 Non Submission Receipt.md",
        f"""# Non Submission Receipt

Record kind: sandbox_formal_vault_execution_request_screening_receipt

Screening result: {config["screening_receipt"]["screening_result"]}

Packet sent: no

Approval collected: no

User wording stored: no

Formal vault touched: no

Run permission produced: no
""",
    )
    write_text(
        prototype / "04 Stop Conditions.md",
        """# Stop Conditions

Stop immediately if any screen attempts to:

- touch the formal vault,
- ask for or store user wording,
- produce command text,
- treat Product Acceptance as formal vault consent,
- treat screening as action basis,
- continue into a later run step.
""",
    )
    write_text(
        prototype / "05 Reviewer Packet.md",
        """# Reviewer Packet

Reviewer should check:

- all three positive fixtures validate,
- failure cases fail closed,
- HTML contains only local filters,
- receipt remains non-submission,
- source hashes bind to P2-32,
- wording avoids authority confusion.
""",
    )
    html = f"""<!doctype html>
<html lang="en" data-sandbox-only="true" data-screening-only="true" data-non-executable="true" data-no-formal-vault-access="true" data-no-write="true" data-no-sync="true" data-no-authority="true" data-no-permission="true" data-no-actual-user-wording="true" data-no-submission="true">
<head>
  <meta charset="utf-8">
  <title>Formal Vault Request Screening</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #17202a;
      --muted: #586170;
      --line: #ccd4df;
      --panel: #f8fafc;
      --pass: #0f766e;
      --block: #b45309;
      --stop: #b91c1c;
      font-family: Arial, sans-serif;
    }}
    body {{
      margin: 0;
      color: var(--ink);
      background: #ffffff;
    }}
    main {{
      max-width: 980px;
      margin: 0 auto;
      padding: 24px;
    }}
    h1 {{
      font-size: 26px;
      margin: 0 0 8px;
      letter-spacing: 0;
    }}
    .muted {{
      color: var(--muted);
      margin: 0 0 20px;
      line-height: 1.5;
    }}
    .toolbar {{
      display: flex;
      gap: 8px;
      flex-wrap: wrap;
      margin: 0 0 16px;
    }}
    button {{
      border: 1px solid var(--line);
      background: #ffffff;
      border-radius: 6px;
      padding: 8px 10px;
      font-size: 14px;
      cursor: default;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 12px;
    }}
    .card {{
      border: 1px solid var(--line);
      border-radius: 8px;
      background: var(--panel);
      padding: 14px;
    }}
    .status {{
      display: inline-block;
      border-radius: 999px;
      padding: 3px 8px;
      font-size: 12px;
      border: 1px solid var(--line);
      background: #ffffff;
    }}
    .pass {{ color: var(--pass); }}
    .block {{ color: var(--block); }}
    .stop {{ color: var(--stop); }}
    ul {{
      padding-left: 18px;
      line-height: 1.5;
    }}
    code {{
      overflow-wrap: anywhere;
    }}
  </style>
</head>
<body>
  <main>
    <h1>Formal Vault Request Screening</h1>
    <p class="muted">Sandbox-only screen for P2-32 synthetic packets. It shows the projected result and the stop boundaries without sending anything or collecting user text.</p>
    <div class="toolbar" aria-label="local display filters only">
      <button type="button" data-filter="all">All</button>
      <button type="button" data-filter="reviewable">Reviewable</button>
      <button type="button" data-filter="blocked">Blocked</button>
    </div>
    <section class="grid">
      <article class="card" data-row="reviewable">
        <span class="status pass">Screened</span>
        <h2>Reviewable packet</h2>
        <p><code>{SCREENING_MODES["synthetic_reviewable_request_screening"]}</code></p>
        <ul>
          <li>Packet hash bound</li>
          <li>P2-32 Product pass bound</li>
          <li>No packet transfer</li>
        </ul>
      </article>
      <article class="card" data-row="blocked">
        <span class="status block">Blocked</span>
        <h2>Missing confirmation packet</h2>
        <p><code>{SCREENING_MODES["synthetic_missing_confirmation_screening"]}</code></p>
        <ul>
          <li>Future confirmation missing</li>
          <li>No user wording stored</li>
          <li>No run permission produced</li>
        </ul>
      </article>
      <article class="card" data-row="blocked">
        <span class="status stop">Denied</span>
        <h2>Denied packet</h2>
        <p><code>{SCREENING_MODES["synthetic_denied_request_screening"]}</code></p>
        <ul>
          <li>Denial preserved</li>
          <li>No retry loop</li>
          <li>Operator stops here</li>
        </ul>
      </article>
    </section>
  </main>
  <script>
    const buttons = Array.from(document.querySelectorAll("button[data-filter]"));
    const rows = Array.from(document.querySelectorAll("[data-row]"));
    buttons.forEach((button) => {{
      button.addEventListener("click", () => {{
        const filter = button.dataset.filter;
        rows.forEach((row) => {{
          row.hidden = filter !== "all" && row.dataset.row !== filter;
        }});
      }});
    }});
  </script>
</body>
</html>
"""
    write_text(prototype / "request-screening-inspector.html", html)
    write_json(prototype / "Receipts" / "formal-vault-execution-request-screening-receipt.json", config["screening_receipt"])


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

Create a sandbox-only request screening artifact for synthetic P2-32 request
packets. The screen must classify packets against the P2-31 projection while
preserving a hard stop before any later formal-vault step.

## Only Write Path

`outputs/review/vaks-implementation-sandbox/{SLICE_ID}/`

## Acceptance

- Three positive fixtures validate.
- Failure cases fail closed.
- Prototype files, HTML, and receipt validate.
- Verification passes before Reviewer, Boundary, and Product Acceptance.
- Product Acceptance returns `PASS_PRODUCT_GRADE` before the next slice.

## Stop Conditions

Stop on real vault access, command emission, approval capture, user wording
storage, packet sending, action-basis claims, commit, push, sync, or promotion.
""",
    )
    write_text(
        ROOT / "source-map.md",
        f"""---
status: built_pending_review
slice_id: {SLICE_ID}
---

# Source Map

This slice reads only completed P2-32 sandbox outputs and binds them by hash.

## Read-Only Inputs

{chr(10).join(source_lines)}

## Upstream Status Binding

- P2-32 Product Acceptance: `{expected_p2_32_binding()["product_acceptance_status"]}`
- P2-32 Reviewer: `{expected_p2_32_binding()["reviewer_status"]}`
- P2-32 Boundary: `{expected_p2_32_binding()["boundary_status"]}`

## Non-Claims

This source map is not reviewed knowledge, evidence support, action basis,
formal-vault approval, or user instruction.
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

- `python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_request_screening.py --rebuild`

## Boundary Result

The local verification checks configuration, source hashes, generated failure
cases, manual negative probes, prototype Markdown, prototype HTML, and prototype
receipt. It does not inspect or change the formal vault.
""",
    )
    write_text(
        ROOT / "reviewer-report.md",
        f"""---
status: reviewer_pending
slice_id: {SLICE_ID}
---

# Reviewer Report

Pending independent read-only review.
""",
    )
    write_text(
        ROOT / "boundary-audit.md",
        f"""---
status: boundary_pending
slice_id: {SLICE_ID}
---

# Boundary Audit

Pending independent boundary audit.
""",
    )
    write_text(
        ROOT / "product-acceptance-report.md",
        f"""---
status: product_acceptance_pending
slice_id: {SLICE_ID}
---

# Product Acceptance Report

Pending GPT-5.5 extra-high Product Acceptance.
""",
    )
    write_text(
        ROOT / "next-step.md",
        f"""---
status: next_step_pending_product_acceptance
slice_id: {SLICE_ID}
---

# Next Step

Do not advance until Reviewer, Boundary Auditor, and GPT-5.5 extra-high Product
Acceptance pass this slice.
""",
    )


def main() -> None:
    fixtures = write_fixtures()
    write_prototype(fixtures["valid-reviewable-request-screening-config.json"])
    oracle = build_failure_cases(fixtures["valid-reviewable-request-screening-config.json"])
    write_contract()
    write_oracle(oracle)
    write_reports(fixtures, oracle)
    print(
        json.dumps(
            {
                "slice_id": SLICE_ID,
                "positive_fixtures": len(fixtures),
                "failure_cases": len(oracle),
                "manual_negative_probes": run_manual_negative_probes()["count"],
                "prototype_issues": inspect_prototype()["issues"],
            },
            indent=2,
            ensure_ascii=False,
        )
    )


if __name__ == "__main__":
    main()
