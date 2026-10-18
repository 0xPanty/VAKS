from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-15-p2-26-formal-vault-write-decision-rehearsal-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox"


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def sandbox_root() -> Path:
    return root().parent


def workspace_root() -> Path:
    return sandbox_root().parents[2]


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_json(data: object) -> str:
    raw = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def repo_relative(path: Path) -> str:
    return path.relative_to(workspace_root()).as_posix()


def safe_write(rel_path: str, content: str, *, overwrite: bool = True) -> None:
    base = root().resolve()
    target = (base / rel_path).resolve()
    if base != target and base not in target.parents:
        raise ValueError(f"Refusing to write outside slice root: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists() and not overwrite:
        return
    target.write_text(content.rstrip() + "\n", encoding="utf-8")


def source_paths() -> dict[str, Path]:
    src = sandbox_root() / SOURCE_SLICE_ID
    proto = src / "prototype" / "formal-vault-write-approval-packet"
    return {
        "source_root": src,
        "source_next_step": src / "next-step.md",
        "source_product_acceptance": src / "product-acceptance-report.md",
        "source_verification": src / "verification.md",
        "source_reviewer_report": src / "reviewer-report.md",
        "source_boundary_audit": src / "boundary-audit.md",
        "source_map": src / "source-map.md",
        "source_config": src / "fixtures" / "valid-approval-packet-config.json",
        "source_contract": src / "artifact" / "formal-vault-write-approval-packet-contract.md",
        "source_receipt": proto / "Receipts" / "formal-vault-write-approval-packet-receipt.json",
        "source_scope_dossier": proto / "01 Scope Dossier.md",
        "source_questions": proto / "02 Future Approval Questions.md",
        "source_non_approval_receipt": proto / "03 Non Approval Receipt.md",
        "source_decision_template": proto / "04 Decision Record Template.md",
        "source_hash_binding": proto / "05 Source And Hash Binding.md",
        "source_stop_conditions": proto / "06 Stop Conditions.md",
    }


def source_input(key: str, path: Path) -> dict:
    return {
        "id": key,
        "source_path": repo_relative(path),
        "source_sha256": sha256(path) if path.exists() else "missing",
        "content_binding": "exact_source_sha256",
    }


def forbidden_operations() -> list[str]:
    return [
        "formal_vault_read",
        "formal_vault_scan",
        "formal_vault_write",
        "formal_vault_hash",
        "formal_vault_snapshot",
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
        "actual_approval_collection",
        "actual_user_approval",
        "user_approval_inference",
        "action_basis_creation",
        "reviewed_knowledge_creation",
        "external_notification",
    ]


def all_question_ids(packet: dict) -> list[str]:
    return [item["id"] for item in packet["approval_questions"]]


def base_scenarios(packet: dict) -> list[dict]:
    qids = all_question_ids(packet)
    common_hashes = {
        "packet_hash": packet["packet_hash"],
        "source_bundle_hash": packet["source_bundle_hash"],
        "scope_hash": packet["approval_scope"]["scope_hash"],
    }
    common_boundaries = {
        "formal_vault_write_allowed_now": False,
        "formal_vault_accessed": False,
        "approval_collected_now": False,
        "action_basis_created": False,
        "reviewed_knowledge_created": False,
        "mainline_merge_allowed": False,
        "sync_allowed": False,
        "commit_allowed": False,
        "push_allowed": False,
        "promotion_allowed": False,
    }
    return [
        {
            "id": "synthetic_approve_exact_packet",
            "decision_verdict": "APPROVED_BY_USER",
            "synthetic_only": True,
            "actual_user_input": False,
            "user_approval_text_present": False,
            "synthetic_user_text": "SYNTHETIC ONLY: all required future confirmation phrases, packet hash, source bundle hash, and scope hash are present.",
            "confirmed_question_ids": qids,
            "hash_claims": dict(common_hashes),
            "explicit_exclusions_ack": ["obsidian_sync", "commit", "push", "promotion"],
            "extra_files_requested": False,
            "rollback_ack": True,
            "hash_ack": True,
            "dirty_state_ack": True,
            "expected_result": "SIMULATED_APPROVAL_VALID_BUT_NOT_ACTIONABLE",
            "next_gate": "future_separately_approved_write_slice_required",
            **common_boundaries,
        },
        {
            "id": "synthetic_deny_write",
            "decision_verdict": "DENIED_BY_USER",
            "synthetic_only": True,
            "actual_user_input": False,
            "user_approval_text_present": False,
            "synthetic_user_text": "SYNTHETIC ONLY: user denies the write request.",
            "confirmed_question_ids": [],
            "hash_claims": dict(common_hashes),
            "explicit_exclusions_ack": ["obsidian_sync", "commit", "push", "promotion"],
            "extra_files_requested": False,
            "rollback_ack": False,
            "hash_ack": False,
            "dirty_state_ack": False,
            "expected_result": "BLOCKED_BY_SYNTHETIC_DENIAL",
            "next_gate": "stop_and_record_denial_only",
            **common_boundaries,
        },
        {
            "id": "synthetic_needs_revision",
            "decision_verdict": "NEEDS_REVISION",
            "synthetic_only": True,
            "actual_user_input": False,
            "user_approval_text_present": False,
            "synthetic_user_text": "SYNTHETIC ONLY: user asks to revise scope before any future write.",
            "confirmed_question_ids": [],
            "hash_claims": dict(common_hashes),
            "explicit_exclusions_ack": ["obsidian_sync", "commit", "push", "promotion"],
            "extra_files_requested": False,
            "rollback_ack": False,
            "hash_ack": False,
            "dirty_state_ack": False,
            "expected_result": "BLOCKED_PENDING_PACKET_REVISION",
            "next_gate": "revise_packet_in_future_sandbox_only",
            **common_boundaries,
        },
    ]


def decision_rules(packet: dict) -> dict:
    return {
        "synthetic_only": True,
        "actual_user_input_disallowed": True,
        "actual_approval_collection_disallowed": True,
        "approved_outcome_not_actionable": True,
        "requires_packet_hash": packet["packet_hash"],
        "requires_source_bundle_hash": packet["source_bundle_hash"],
        "requires_scope_hash": packet["approval_scope"]["scope_hash"],
        "requires_all_question_ids_for_approved": all_question_ids(packet),
        "deny_always_blocks_write": True,
        "revise_always_blocks_write": True,
        "extra_files_always_block": True,
        "sync_commit_push_promotion_always_block": True,
        "dirty_state_blocks_write": True,
        "rollback_and_hash_ack_required_for_approved": True,
    }


def rehearsal_material(base: dict) -> dict:
    scenarios = []
    for scenario in base["decision_scenarios"]:
        item = dict(scenario)
        item.pop("required_rehearsal_hash", None)
        scenarios.append(item)
    receipt = dict(base["non_approval_receipt"])
    receipt.pop("rehearsal_hash", None)
    return {
        "rehearsal_version": base["rehearsal_version"],
        "source_slice": base["source_slice"],
        "source_input_bundle_hash": base["source_input_bundle_hash"],
        "source_packet_hash": base["source_packet_hash"],
        "source_packet_source_bundle_hash": base["source_packet_source_bundle_hash"],
        "source_packet_scope_hash": base["source_packet_scope_hash"],
        "decision_rules": base["decision_rules"],
        "decision_scenarios": scenarios,
        "non_approval_receipt": receipt,
        "stop_conditions": base["stop_conditions"],
    }


def attach_rehearsal_hash(base: dict) -> dict:
    material = rehearsal_material(base)
    base["rehearsal_hash_material"] = material
    base["rehearsal_hash"] = sha256_json(material)
    for scenario in base["decision_scenarios"]:
        scenario["required_rehearsal_hash"] = base["rehearsal_hash"]
    base["non_approval_receipt"]["rehearsal_hash"] = base["rehearsal_hash"]
    return base


def config() -> dict:
    paths = source_paths()
    packet = load_json(paths["source_config"])
    inputs = [source_input(key, path) for key, path in paths.items() if key != "source_root"]
    base = {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "rehearsal_version": "p2-26-decision-rehearsal-v1",
        "purpose": "Simulate approve, deny, and revise outcomes against the P2-25 approval packet without collecting approval or accessing the formal vault.",
        "formal_vault_path_label": "formal Obsidian vault path is a label only; it is not accessed in this slice",
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": [item["source_path"] for item in inputs],
        "operations": {op: False for op in forbidden_operations()}
        | {"default_read_only": True, "rebuild_requires_explicit_flag": True},
        "boundary_phrases": [
            "sandbox only",
            "decision rehearsal only",
            "synthetic decisions only",
            "not actual approval",
            "approval not collected",
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
        ],
        "source_inputs": inputs,
        "source_input_bundle_hash": sha256_json(inputs),
        "source_packet_hash": packet["packet_hash"],
        "source_packet_source_bundle_hash": packet["source_bundle_hash"],
        "source_packet_scope_hash": packet["approval_scope"]["scope_hash"],
        "source_packet_version": packet["packet_version"],
        "decision_rules": decision_rules(packet),
        "decision_scenarios": base_scenarios(packet),
        "non_approval_receipt": {
            "approval_collected_now": False,
            "actual_user_input_used": False,
            "formal_vault_accessed": False,
            "current_status": "synthetic_decision_rehearsal_complete_pending_review",
            "non_claims": [
                "not actual approval",
                "not formal vault approval",
                "not sync approval",
                "not commit approval",
                "not push approval",
                "not promotion approval",
                "not action basis",
                "not reviewed knowledge",
                "not evidence support",
            ],
        },
        "stop_conditions": [
            "actual user approval collection requested",
            "formal vault read requested",
            "formal vault scan requested",
            "formal vault write requested",
            "formal vault hash or snapshot requested",
            "absolute vault path requested",
            "Obsidian sync requested",
            "commit or push requested",
            "promotion requested",
            "decision inferred from silence or prior PASS",
            "packet hash mismatch",
            "source bundle hash mismatch",
            "scope hash mismatch",
            "rehearsal hash mismatch",
            "approved synthetic scenario treated as action basis",
            "denied or revise scenario allows write",
            "extra files requested",
            "rollback or hash acknowledgement missing for synthetic approval",
        ],
        "inspector_controls": {
            "inputs": [{"id": "q", "type": "search", "purpose": "filter"}],
            "buttons": [
                {"label": "All", "filter": "all"},
                {"label": "Scenarios", "filter": "scenarios"},
                {"label": "Rules", "filter": "rules"},
                {"label": "Receipt", "filter": "receipt"},
                {"label": "Stops", "filter": "stops"},
            ],
        },
        "product_metrics": {
            "required_positive_fixtures": 3,
            "minimum_failure_cases": 54,
            "required_decision_scenarios": 3,
            "max_journey_steps": 3,
        },
    }
    return attach_rehearsal_hash(base)


def variant_config(base: dict, verdict: str) -> dict:
    variant = json.loads(json.dumps(base))
    if verdict == "deny":
        variant["purpose"] = "Variant fixture focused on denial-only rehearsal."
        variant["fixture_focus"] = "deny"
    elif verdict == "revise":
        variant["purpose"] = "Variant fixture focused on revise-only rehearsal."
        variant["fixture_focus"] = "revise"
    return attach_rehearsal_hash(variant)


def refresh_source_input_bundle_hash(item: dict) -> None:
    item["source_input_bundle_hash"] = sha256_json(item["source_inputs"])


def refresh_rehearsal_hash(item: dict) -> None:
    material = rehearsal_material(item)
    item["rehearsal_hash_material"] = material
    item["rehearsal_hash"] = sha256_json(material)
    for scenario in item["decision_scenarios"]:
        scenario["required_rehearsal_hash"] = item["rehearsal_hash"]
    item["non_approval_receipt"]["rehearsal_hash"] = item["rehearsal_hash"]


def refresh_all_hashes(item: dict) -> None:
    refresh_source_input_bundle_hash(item)
    refresh_rehearsal_hash(item)


def refresh_packet_claims(item: dict) -> None:
    item["decision_rules"]["requires_packet_hash"] = item["source_packet_hash"]
    item["decision_rules"]["requires_source_bundle_hash"] = item["source_packet_source_bundle_hash"]
    item["decision_rules"]["requires_scope_hash"] = item["source_packet_scope_hash"]
    for scenario in item["decision_scenarios"]:
        scenario["hash_claims"]["packet_hash"] = item["source_packet_hash"]
        scenario["hash_claims"]["source_bundle_hash"] = item["source_packet_source_bundle_hash"]
        scenario["hash_claims"]["scope_hash"] = item["source_packet_scope_hash"]


def failure_cases(base: dict) -> list[tuple[str, dict]]:
    cases: list[tuple[str, dict]] = []

    def expected_list(codes: str | list[str]) -> list[str]:
        return [codes] if isinstance(codes, str) else codes

    def mutate(name: str, codes: str | list[str], fn) -> None:
        item = json.loads(json.dumps(base))
        fn(item)
        item["expected_failures"] = expected_list(codes)
        cases.append((name, item))

    for idx, op in enumerate(forbidden_operations(), start=1):
        mutate(f"{idx:02d}-forbidden-{op}.json", f"forbidden_operation:{op}", lambda c, op=op: c["operations"].__setitem__(op, True))

    mutate("24-source-input-path-missing.json", "source_input_path_missing:source_config", lambda c: (c["source_inputs"][6].__setitem__("source_path", ""), refresh_source_input_bundle_hash(c), refresh_rehearsal_hash(c)))
    mutate("25-source-input-hash-mismatch.json", "source_input_hash_mismatch:source_config", lambda c: (c["source_inputs"][6].__setitem__("source_sha256", "deadbeef"), refresh_source_input_bundle_hash(c), refresh_rehearsal_hash(c)))
    mutate("26-source-input-bundle-hash-mismatch.json", "source_input_bundle_hash_mismatch", lambda c: (c.__setitem__("source_input_bundle_hash", "deadbeef"), refresh_rehearsal_hash(c)))
    mutate("27-source-packet-hash-mismatch.json", "source_packet_hash_mismatch", lambda c: (c.__setitem__("source_packet_hash", "deadbeef"), refresh_packet_claims(c), refresh_rehearsal_hash(c)))
    mutate("28-source-packet-source-bundle-hash-mismatch.json", "source_packet_source_bundle_hash_mismatch", lambda c: (c.__setitem__("source_packet_source_bundle_hash", "deadbeef"), refresh_packet_claims(c), refresh_rehearsal_hash(c)))
    mutate("29-source-packet-scope-hash-mismatch.json", "source_packet_scope_hash_mismatch", lambda c: (c.__setitem__("source_packet_scope_hash", "deadbeef"), refresh_packet_claims(c), refresh_rehearsal_hash(c)))
    mutate("30-rehearsal-hash-missing.json", "rehearsal_hash_missing", lambda c: c.__setitem__("rehearsal_hash", ""))
    mutate("31-rehearsal-hash-mismatch.json", ["rehearsal_hash_mismatch", "non_approval_receipt_rehearsal_hash_mismatch"], lambda c: c.__setitem__("rehearsal_hash", "deadbeef"))
    mutate("32-missing-approve-scenario.json", ["missing_decision_scenario:synthetic_approve_exact_packet", "too_few_decision_scenarios"], lambda c: (c.__setitem__("decision_scenarios", [s for s in c["decision_scenarios"] if s["id"] != "synthetic_approve_exact_packet"]), refresh_rehearsal_hash(c)))
    mutate("33-scenario-not-synthetic.json", "scenario_not_synthetic:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0].__setitem__("synthetic_only", False), refresh_rehearsal_hash(c)))
    mutate("34-scenario-actual-user-input.json", "scenario_uses_actual_user_input:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0].__setitem__("actual_user_input", True), refresh_rehearsal_hash(c)))
    mutate("35-scenario-user-text-present.json", "scenario_has_actual_user_text:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0].__setitem__("user_approval_text_present", True), refresh_rehearsal_hash(c)))
    mutate("36-approve-missing-packet-hash.json", "scenario_packet_hash_mismatch:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0]["hash_claims"].__setitem__("packet_hash", ""), refresh_rehearsal_hash(c)))
    mutate("37-approve-wrong-source-bundle-hash.json", "scenario_source_bundle_hash_mismatch:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0]["hash_claims"].__setitem__("source_bundle_hash", "deadbeef"), refresh_rehearsal_hash(c)))
    mutate("38-approve-wrong-scope-hash.json", "scenario_scope_hash_mismatch:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0]["hash_claims"].__setitem__("scope_hash", "deadbeef"), refresh_rehearsal_hash(c)))
    mutate("39-approve-missing-question.json", "approved_missing_required_question:synthetic_approve_exact_packet:future_approve_exact_scope", lambda c: (c["decision_scenarios"][0].__setitem__("confirmed_question_ids", c["decision_scenarios"][0]["confirmed_question_ids"][1:]), refresh_rehearsal_hash(c)))
    mutate("40-approve-allows-write-now.json", "scenario_allows_formal_vault_write_now:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0].__setitem__("formal_vault_write_allowed_now", True), refresh_rehearsal_hash(c)))
    mutate("41-approve-creates-action-basis.json", "scenario_creates_action_basis:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0].__setitem__("action_basis_created", True), refresh_rehearsal_hash(c)))
    mutate("42-approve-actionable-result.json", ["approved_scenario_result_actionable:synthetic_approve_exact_packet", "approved_scenario_result_bad:synthetic_approve_exact_packet"], lambda c: (c["decision_scenarios"][0].__setitem__("expected_result", "READY_TO_WRITE"), refresh_rehearsal_hash(c)))
    mutate("43-deny-allows-write.json", "denied_scenario_allows_write:synthetic_deny_write", lambda c: (c["decision_scenarios"][1].__setitem__("formal_vault_write_allowed_now", True), refresh_rehearsal_hash(c)))
    mutate("44-deny-wrong-result.json", "denied_scenario_result_bad:synthetic_deny_write", lambda c: (c["decision_scenarios"][1].__setitem__("expected_result", "READY_TO_WRITE"), refresh_rehearsal_hash(c)))
    mutate("45-revise-allows-write.json", "revise_scenario_allows_write:synthetic_needs_revision", lambda c: (c["decision_scenarios"][2].__setitem__("formal_vault_write_allowed_now", True), refresh_rehearsal_hash(c)))
    mutate("46-revise-wrong-result.json", "revise_scenario_result_bad:synthetic_needs_revision", lambda c: (c["decision_scenarios"][2].__setitem__("expected_result", "READY_TO_WRITE"), refresh_rehearsal_hash(c)))
    mutate("47-extra-files-requested.json", "scenario_extra_files_requested:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0].__setitem__("extra_files_requested", True), refresh_rehearsal_hash(c)))
    mutate("48-sync-allowed.json", "scenario_allows_sync:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0].__setitem__("sync_allowed", True), refresh_rehearsal_hash(c)))
    mutate("49-commit-allowed.json", "scenario_allows_commit:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0].__setitem__("commit_allowed", True), refresh_rehearsal_hash(c)))
    mutate("50-push-allowed.json", "scenario_allows_push:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0].__setitem__("push_allowed", True), refresh_rehearsal_hash(c)))
    mutate("51-promotion-allowed.json", "scenario_allows_promotion:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0].__setitem__("promotion_allowed", True), refresh_rehearsal_hash(c)))
    mutate("52-approved-missing-rollback-ack.json", "approved_missing_rollback_ack:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0].__setitem__("rollback_ack", False), refresh_rehearsal_hash(c)))
    mutate("53-approved-missing-hash-ack.json", "approved_missing_hash_ack:synthetic_approve_exact_packet", lambda c: (c["decision_scenarios"][0].__setitem__("hash_ack", False), refresh_rehearsal_hash(c)))
    mutate("54-rule-allows-actual-user-input.json", "rule_allows_actual_user_input", lambda c: (c["decision_rules"].__setitem__("actual_user_input_disallowed", False), refresh_rehearsal_hash(c)))
    mutate("55-rule-approve-actionable.json", "rule_allows_approved_outcome_actionable", lambda c: (c["decision_rules"].__setitem__("approved_outcome_not_actionable", False), refresh_rehearsal_hash(c)))
    mutate("56-rule-missing-packet-hash.json", "rule_packet_hash_mismatch", lambda c: (c["decision_rules"].__setitem__("requires_packet_hash", "deadbeef"), refresh_rehearsal_hash(c)))
    mutate("57-receipt-claims-approval.json", "non_approval_receipt_claims_approval", lambda c: (c["non_approval_receipt"].__setitem__("approval_collected_now", True), refresh_rehearsal_hash(c)))
    mutate("58-receipt-formal-vault-accessed.json", "non_approval_receipt_formal_vault_accessed", lambda c: (c["non_approval_receipt"].__setitem__("formal_vault_accessed", True), refresh_rehearsal_hash(c)))
    mutate("59-authority-confusing-text.json", "authority_confusing_text", lambda c: (c["stop_conditions"].append("synthetic approval creates action basis"), refresh_rehearsal_hash(c)))
    mutate("60-too-few-failure-cases.json", "minimum_failure_cases_too_low", lambda c: c["product_metrics"].__setitem__("minimum_failure_cases", 5))
    mutate("61-inspector-approve-button.json", "inspector_control_not_allowed:button:approve", lambda c: c["inspector_controls"]["buttons"][1].__setitem__("label", "Approve"))
    return cases


def frontmatter(record_kind: str, status: str) -> str:
    return "\n".join(
        [
            "---",
            f"record_kind: {record_kind}",
            f"slice_id: {SLICE_ID}",
            f"status: {status}",
            "sandbox_only: true",
            "truth_boundary: sandbox_only",
            "---",
        ]
    )


def md_link(label: str, target: str) -> str:
    return f"[{label}]({target})"


def render_slice_plan(git_status_summary: str) -> str:
    return f"""---
record_kind: sandbox_slice_plan
slice_id: {SLICE_ID}
status: built_pending_review
truth_boundary: sandbox_only
---

# Slice Plan

## Goal

Build a sandbox-only decision rehearsal for approve, deny, and revise outcomes
against the P2-25 approval packet. This slice uses synthetic decisions only and
does not collect approval or access the formal vault.

## Why This Slice

P2-25 received `PASS_PRODUCT_GRADE` and recommended a
`formal-vault-write-decision-rehearsal-sandbox`.

## Write Scope

```text
outputs/review/vaks-implementation-sandbox/{SLICE_ID}/
```

## Acceptance Standard

- Approve, deny, and revise outcomes are represented as synthetic scenarios.
- Synthetic approval remains not actionable.
- Deny and revise outcomes block write.
- Packet, source bundle, scope, and rehearsal hashes are verified.
- No scenario creates actual approval, action basis, reviewed knowledge, or
  formal vault access.
- Reviewer, Boundary, and GPT-5.5 xhigh Product Acceptance pass.
- Final gate passes after Product Acceptance.

## Start Git Status Summary

```text
{git_status_summary}
```

The dirty tree is treated as pre-existing baseline. Final audit is scoped to
this slice path only.
"""


def render_source_map(paths: dict[str, Path], base: dict) -> str:
    rows = []
    for key, path in paths.items():
        if key == "source_root":
            continue
        rel = path.relative_to(sandbox_root())
        rows.append(f"| `{key}` | `../{rel.as_posix()}` | exists: `{path.exists()}` | sha256: `{sha256(path) if path.exists() else 'missing'}` |")
    return f"""---
record_kind: sandbox_source_map
slice_id: {SLICE_ID}
status: built_pending_review
truth_boundary: sandbox_only
---

# Source Map

This slice reads P2-25 as the product-grade sandbox source. It does not read or
write the formal Obsidian vault.

| Source | Path | Evidence |
| --- | --- | --- |
{chr(10).join(rows)}

## Hash Inputs

- source_input_bundle_hash: `{base['source_input_bundle_hash']}`
- source_packet_hash: `{base['source_packet_hash']}`
- source_packet_source_bundle_hash: `{base['source_packet_source_bundle_hash']}`
- source_packet_scope_hash: `{base['source_packet_scope_hash']}`
- rehearsal_hash: `{base['rehearsal_hash']}`

## Boundary

P2-25 `PASS_PRODUCT_GRADE` is a sandbox input only. It is not actual approval,
reviewed knowledge, evidence support, action basis, mainline approval, formal
vault approval, sync approval, commit approval, push approval, or promotion
approval.
"""


def render_contract(base: dict) -> str:
    return f"""# Formal Vault Write Decision Rehearsal Contract

## Input Contract

- P2-25 product-grade approval packet and hashes.
- No actual user approval, formal vault read, scan, write, sync, snapshot, hash,
  or mutation.

## Output Contract

- Synthetic approve/deny/revise scenarios.
- Decision rule matrix.
- Non-approval rehearsal receipt.
- Stop condition register.
- Static decision inspector with no approval or write controls.

## Product Promise

A future agent can understand how a real future decision should be classified,
without treating this rehearsal as the decision itself.

## Boundary Promise

This is decision rehearsal only. Synthetic approval is not actionable. Deny and
revise block write. Nothing in this slice approves formal vault write, sync,
commit, push, promotion, reviewed knowledge, evidence support, or action basis.

## Hashes

- source_input_bundle_hash: `{base['source_input_bundle_hash']}`
- source_packet_hash: `{base['source_packet_hash']}`
- source_packet_source_bundle_hash: `{base['source_packet_source_bundle_hash']}`
- source_packet_scope_hash: `{base['source_packet_scope_hash']}`
- rehearsal_hash: `{base['rehearsal_hash']}`
"""


def render_home(base: dict) -> str:
    return f"""{frontmatter("sandbox_decision_rehearsal_home", "sandbox_pilot")}

# Decision Rehearsal Home

This sandbox rehearses approve, deny, and revise outcomes using synthetic
decisions only.

## Start

1. Open [[01 Scenario Matrix]].
2. Open [[05 Decision Rules]].
3. Open [[06 Non Approval Receipt]].
4. Open [[07 Stop Conditions]] before any action-facing move.

## Fast Links

- [[01 Scenario Matrix]]
- [[02 Synthetic Approval Rehearsal]]
- [[03 Synthetic Denial Rehearsal]]
- [[04 Synthetic Revision Rehearsal]]
- [[05 Decision Rules]]
- [[06 Non Approval Receipt]]
- [[07 Stop Conditions]]
- [[08 Reviewer Packet]]
- `decision-rehearsal-inspector.html`
- {md_link("P2-25 next-step", "../../../" + SOURCE_SLICE_ID + "/next-step.md")}
- {md_link("P2-25 product acceptance", "../../../" + SOURCE_SLICE_ID + "/product-acceptance-report.md")}

## Boundary Rail

Sandbox only. Decision rehearsal only. Synthetic decisions only. Not actual
approval. Approval not collected. Formal vault not accessed. Dry-run only. Not
reviewed knowledge. Not evidence support. Not action basis. Does not approve.
No formal vault read. No formal vault write. No sync. No commit. No push. No
promotion. Requires separate user approval.
"""


def render_scenario_matrix(base: dict) -> str:
    rows = ["| Scenario | Verdict | Expected Result | Write Allowed Now | Next Gate |", "| --- | --- | --- | --- | --- |"]
    for item in base["decision_scenarios"]:
        rows.append(f"| `{item['id']}` | `{item['decision_verdict']}` | `{item['expected_result']}` | `{item['formal_vault_write_allowed_now']}` | `{item['next_gate']}` |")
    return f"""{frontmatter("sandbox_decision_scenario_matrix", "sandbox_pilot")}

# Scenario Matrix

{chr(10).join(rows)}

## Hashes

- rehearsal_hash: `{base['rehearsal_hash']}`

## Boundary

All decisions here are synthetic. The approval scenario is valid only as a
rehearsal and remains not actionable.

## Next

- [[02 Synthetic Approval Rehearsal]]
- [[07 Stop Conditions]]
"""


def render_scenario(base: dict, scenario_id: str, title: str, next_link: str) -> str:
    item = next(s for s in base["decision_scenarios"] if s["id"] == scenario_id)
    confirmations = "\n".join(f"- `{qid}`" for qid in item["confirmed_question_ids"]) or "- none"
    return f"""{frontmatter("sandbox_decision_rehearsal_scenario", "sandbox_pilot")}

# {title}

| Field | Value |
| --- | --- |
| decision_verdict | `{item['decision_verdict']}` |
| synthetic_only | `{item['synthetic_only']}` |
| actual_user_input | `{item['actual_user_input']}` |
| user_approval_text_present | `{item['user_approval_text_present']}` |
| expected_result | `{item['expected_result']}` |
| formal_vault_write_allowed_now | `{item['formal_vault_write_allowed_now']}` |
| action_basis_created | `{item['action_basis_created']}` |
| reviewed_knowledge_created | `{item['reviewed_knowledge_created']}` |
| next_gate | `{item['next_gate']}` |
| required_rehearsal_hash | `{item['required_rehearsal_hash']}` |

## Hash Claims

- packet_hash: `{item['hash_claims']['packet_hash']}`
- source_bundle_hash: `{item['hash_claims']['source_bundle_hash']}`
- scope_hash: `{item['hash_claims']['scope_hash']}`

## Confirmed Questions

{confirmations}

## Boundary

This is not actual approval, not formal vault approval, not action basis, and
not permission to write.

## Next

- [[{next_link}]]
- [[07 Stop Conditions]]
"""


def render_rules(base: dict) -> str:
    rules = base["decision_rules"]
    rows = "\n".join(f"| `{key}` | `{value}` |" for key, value in rules.items() if not isinstance(value, list))
    qids = "\n".join(f"- `{qid}`" for qid in rules["requires_all_question_ids_for_approved"])
    return f"""{frontmatter("sandbox_decision_rules", "sandbox_pilot")}

# Decision Rules

| Rule | Value |
| --- | --- |
{rows}

## Required Question IDs For Synthetic Approval

{qids}

## Boundary

The rules classify synthetic scenarios only. They do not ask the user and do
not approve any formal vault operation.
"""


def render_receipt(base: dict) -> str:
    receipt = base["non_approval_receipt"]
    claims = "\n".join(f"- {item}" for item in receipt["non_claims"])
    return f"""{frontmatter("sandbox_non_approval_rehearsal_receipt", "sandbox_pilot")}

# Non Approval Receipt

| Field | Value |
| --- | --- |
| approval_collected_now | `{receipt['approval_collected_now']}` |
| actual_user_input_used | `{receipt['actual_user_input_used']}` |
| formal_vault_accessed | `{receipt['formal_vault_accessed']}` |
| current_status | `{receipt['current_status']}` |
| rehearsal_hash | `{receipt['rehearsal_hash']}` |

## Non Claims

{claims}

## Next

- [[07 Stop Conditions]]
"""


def render_stops(base: dict) -> str:
    rows = "\n".join(f"- {item}" for item in base["stop_conditions"])
    return f"""{frontmatter("sandbox_decision_rehearsal_stop_conditions", "sandbox_pilot")}

# Stop Conditions

{rows}

## Safe Alternative

Record the requested move as a future user decision or future sandbox item and
stop. Do not perform the operation in this slice.
"""


def render_reviewer_packet(base: dict) -> str:
    return f"""{frontmatter("sandbox_reviewer_packet", "sandbox_pilot")}

# Reviewer Packet

## Inspect First

- `artifact/formal-vault-write-decision-rehearsal-contract.md`
- `fixtures/valid-decision-rehearsal-config.json`
- `fixtures/valid-denial-rehearsal-config.json`
- `fixtures/valid-revision-rehearsal-config.json`
- `artifact/failure-case-oracle.md`
- `prototype/formal-vault-write-decision-rehearsal/`
- `artifact/verify_decision_rehearsal.py`

## Review Questions

- Does synthetic approval stay non-actionable?
- Do deny and revise outcomes block write?
- Are packet, source bundle, scope, and rehearsal hashes verified?
- Does any scenario collect actual user approval?
- Does the inspector remain read-only and non-approval-collecting?
"""


def render_inspector_html(base: dict) -> str:
    cards = []
    for item in base["decision_scenarios"]:
        cards.append(
            f"""<article class=\"card\" data-kind=\"scenarios\" data-search=\"{item['id']} {item['decision_verdict']} {item['expected_result']} synthetic only no formal vault write\">
  <p class=\"eyebrow\">scenarios</p>
  <h3>{item['id']}</h3>
  <p>{item['expected_result']}</p>
  <strong>write_allowed_now={item['formal_vault_write_allowed_now']}</strong>
</article>"""
        )
    cards.append(
        f"""<article class=\"card\" data-kind=\"rules\" data-search=\"decision rules packet hash source bundle scope rehearsal no action basis\">
  <p class=\"eyebrow\">rules</p>
  <h3>Decision Rules</h3>
  <p>Approved synthetic scenario is valid but not actionable. Deny and revise block write.</p>
  <strong>{base['rehearsal_hash']}</strong>
</article>"""
    )
    cards.append(
        """<article class=\"card\" data-kind=\"receipt\" data-search=\"non approval receipt approval not collected formal vault not accessed\">
  <p class=\"eyebrow\">receipt</p>
  <h3>Non Approval Receipt</h3>
  <p>Approval is not collected and the formal vault is not accessed.</p>
  <strong>not actual approval</strong>
</article>"""
    )
    cards.append(
        """<article class=\"card\" data-kind=\"stops\" data-search=\"stop conditions no sync no commit no push no promotion no formal vault read no formal vault write\">
  <p class=\"eyebrow\">stops</p>
  <h3>Stop Conditions</h3>
  <p>Stop on actual approval collection, formal vault access, action basis creation, sync, commit, push, or promotion.</p>
  <strong>does not approve</strong>
</article>"""
    )
    buttons = []
    for control in base["inspector_controls"]["buttons"]:
        active = ' class="active"' if control["filter"] == "all" else ""
        buttons.append(f"<button type=\"button\"{active} data-filter=\"{control['filter']}\">{control['label']}</button>")
    return f"""<!doctype html>
<html lang=\"en\" data-sandbox-only=\"true\" data-decision-rehearsal-only=\"true\" data-synthetic-only=\"true\" data-no-approval=\"true\" data-no-write=\"true\" data-no-sync=\"true\" data-no-authority=\"true\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Formal Vault Write Decision Rehearsal</title>
  <style>
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; color: #172026; background: #f7faf8; }}
    header {{ padding: 24px 28px 16px; background: #fff; border-bottom: 1px solid #d8dee4; }}
    h1 {{ margin: 0 0 8px; font-size: 30px; letter-spacing: 0; }}
    .layout {{ display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 18px; padding: 18px 28px 32px; }}
    .toolbar {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 14px; }}
    input {{ min-width: 280px; height: 40px; padding: 0 12px; border: 1px solid #d8dee4; border-radius: 6px; }}
    button {{ height: 40px; border: 1px solid #d8dee4; background: #fff; border-radius: 6px; padding: 0 12px; font-weight: 700; }}
    button.active {{ border-color: #256f68; color: #256f68; }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px; }}
    .card, aside {{ background: #fff; border: 1px solid #d8dee4; border-radius: 8px; padding: 14px; }}
    .card h3 {{ margin: 4px 0 8px; font-size: 18px; }}
    .card p, aside li {{ color: #52616b; line-height: 1.45; }}
    .eyebrow {{ margin: 0; color: #256f68; text-transform: uppercase; font-size: 12px; font-weight: 700; }}
    aside {{ align-self: start; position: sticky; top: 16px; }}
    @media (max-width: 860px) {{ .layout {{ grid-template-columns: 1fr; padding: 16px; }} input {{ min-width: 100%; }} }}
  </style>
</head>
<body>
  <header>
    <h1>Formal Vault Write Decision Rehearsal</h1>
    <p>Sandbox-only decision rehearsal. It cannot collect approval, write, sync, approve, or execute commands.</p>
  </header>
  <div class=\"layout\">
    <main>
      <div class=\"toolbar\" data-role=\"rehearsal-filter\">
        <input id=\"q\" type=\"search\" placeholder=\"Search scenarios, rules, receipt, stops\">
        {' '.join(buttons)}
      </div>
      <div class=\"grid\" data-role=\"rehearsal-cards\">
        {chr(10).join(cards)}
      </div>
    </main>
    <aside data-role=\"boundary-rail\">
      <h2>Boundary Rail</h2>
      <ul>
        <li>sandbox only</li>
        <li>decision rehearsal only</li>
        <li>synthetic decisions only</li>
        <li>not actual approval</li>
        <li>approval not collected</li>
        <li>formal vault not accessed</li>
        <li>not evidence support / not action basis</li>
        <li>no formal vault read / no formal vault write</li>
        <li>no sync / no commit / no push / no promotion</li>
      </ul>
    </aside>
  </div>
  <script type=\"application/json\" id=\"rehearsal-data\">
{json.dumps({"decision_scenarios": base["decision_scenarios"], "decision_rules": base["decision_rules"], "non_approval_receipt": base["non_approval_receipt"], "stop_conditions": base["stop_conditions"]}, indent=2)}
  </script>
  <script>
    const input = document.getElementById('q');
    const cards = Array.from(document.querySelectorAll('.card'));
    const buttons = Array.from(document.querySelectorAll('button[data-filter]'));
    let filter = 'all';
    function applyFilter() {{
      const query = input.value.toLowerCase();
      cards.forEach(card => {{
        const okFilter = filter === 'all' || card.dataset.kind === filter;
        const okQuery = !query || card.dataset.search.toLowerCase().includes(query) || card.textContent.toLowerCase().includes(query);
        card.hidden = !(okFilter && okQuery);
      }});
    }}
    buttons.forEach(btn => btn.addEventListener('click', () => {{
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filter = btn.dataset.filter;
      applyFilter();
    }}));
    input.addEventListener('input', applyFilter);
  </script>
</body>
</html>
"""


def render_receipt_json(base: dict, paths: dict[str, Path]) -> dict:
    source_hashes = {}
    for key, path in paths.items():
        if key == "source_root":
            continue
        source_hashes[key] = sha256(path) if path.exists() else "missing"
    return {
        "record_kind": "sandbox_formal_vault_decision_rehearsal_receipt",
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "formal_vault_accessed": False,
        "approval_collected_now": False,
        "actual_user_input_used": False,
        "write_scope": base["write_scope"],
        "source_hashes": source_hashes,
        "source_input_bundle_hash": base["source_input_bundle_hash"],
        "source_packet_hash": base["source_packet_hash"],
        "rehearsal_hash": base["rehearsal_hash"],
        "scenario_count": len(base["decision_scenarios"]),
        "forbidden_operations": {op: False for op in forbidden_operations()},
        "non_claims": base["non_approval_receipt"]["non_claims"],
    }


def render_failure_oracle_md(cases: list[tuple[str, dict]]) -> str:
    rows = ["# Failure Case Oracle", "", "| File | Expected failure |", "| --- | --- |"]
    for name, item in cases:
        rows.append(f"| `{name}` | `{', '.join(item['expected_failures'])}` |")
    return "\n".join(rows)


def render_pending(kind: str, title: str) -> str:
    return f"""---
record_kind: {kind}
slice_id: {SLICE_ID}
status: pending
truth_boundary: sandbox_only
---

# {title}

Pending.
"""


def render_verification_pending() -> str:
    return f"""---
record_kind: sandbox_verification
slice_id: {SLICE_ID}
status: pending
truth_boundary: sandbox_verification_only
---

# Verification

Pending.
"""


def build() -> None:
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required P2-25 source files: " + "; ".join(missing))
    base = config()
    git_status_summary = "pre-existing dirty tree recorded before build; final audit scoped to this slice path"

    safe_write("slice-plan.md", render_slice_plan(git_status_summary))
    safe_write("source-map.md", render_source_map(paths, base))
    safe_write("artifact/formal-vault-write-decision-rehearsal-contract.md", render_contract(base))
    safe_write("fixtures/valid-decision-rehearsal-config.json", json.dumps(base, indent=2, ensure_ascii=False))
    safe_write("fixtures/valid-denial-rehearsal-config.json", json.dumps(variant_config(base, "deny"), indent=2, ensure_ascii=False))
    safe_write("fixtures/valid-revision-rehearsal-config.json", json.dumps(variant_config(base, "revise"), indent=2, ensure_ascii=False))

    cases = failure_cases(base)
    for name, item in cases:
        safe_write(f"failure-cases/{name}", json.dumps(item, indent=2, ensure_ascii=False))
    safe_write("artifact/failure-case-oracle.json", json.dumps([{"file": name, "expected_failures": item["expected_failures"]} for name, item in cases], indent=2, ensure_ascii=False))
    safe_write("artifact/failure-case-oracle.md", render_failure_oracle_md(cases))

    proto = "prototype/formal-vault-write-decision-rehearsal"
    safe_write(f"{proto}/00 Decision Rehearsal Home.md", render_home(base))
    safe_write(f"{proto}/01 Scenario Matrix.md", render_scenario_matrix(base))
    safe_write(f"{proto}/02 Synthetic Approval Rehearsal.md", render_scenario(base, "synthetic_approve_exact_packet", "Synthetic Approval Rehearsal", "03 Synthetic Denial Rehearsal"))
    safe_write(f"{proto}/03 Synthetic Denial Rehearsal.md", render_scenario(base, "synthetic_deny_write", "Synthetic Denial Rehearsal", "04 Synthetic Revision Rehearsal"))
    safe_write(f"{proto}/04 Synthetic Revision Rehearsal.md", render_scenario(base, "synthetic_needs_revision", "Synthetic Revision Rehearsal", "05 Decision Rules"))
    safe_write(f"{proto}/05 Decision Rules.md", render_rules(base))
    safe_write(f"{proto}/06 Non Approval Receipt.md", render_receipt(base))
    safe_write(f"{proto}/07 Stop Conditions.md", render_stops(base))
    safe_write(f"{proto}/08 Reviewer Packet.md", render_reviewer_packet(base))
    safe_write(f"{proto}/decision-rehearsal-inspector.html", render_inspector_html(base))
    safe_write(f"{proto}/Receipts/formal-vault-write-decision-rehearsal-receipt.json", json.dumps(render_receipt_json(base, paths), indent=2, ensure_ascii=False))

    safe_write("verification.md", render_verification_pending(), overwrite=False)
    safe_write("reviewer-report.md", render_pending("sandbox_reviewer_report", "Reviewer Report"), overwrite=False)
    safe_write("boundary-audit.md", render_pending("sandbox_boundary_audit", "Boundary Audit"), overwrite=False)
    safe_write("product-acceptance-report.md", render_pending("sandbox_product_acceptance_report", "Product Acceptance Report"), overwrite=False)
    safe_write("next-step.md", render_pending("sandbox_next_step", "Next Step"), overwrite=False)


if __name__ == "__main__":
    build()
