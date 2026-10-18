from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-15-p2-25-formal-vault-write-approval-packet-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-24-formal-vault-write-plan-dry-run-sandbox"


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


def repo_relative(path: Path) -> str:
    return path.relative_to(workspace_root()).as_posix()


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


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
    proto = src / "prototype" / "formal-vault-write-plan-dry-run"
    return {
        "source_root": src,
        "source_next_step": src / "next-step.md",
        "source_product_acceptance": src / "product-acceptance-report.md",
        "source_verification": src / "verification.md",
        "source_reviewer_report": src / "reviewer-report.md",
        "source_boundary_audit": src / "boundary-audit.md",
        "source_map": src / "source-map.md",
        "source_config": src / "fixtures" / "valid-write-plan-config.json",
        "source_contract": src / "artifact" / "formal-vault-write-plan-dry-run-contract.md",
        "source_receipt": proto / "Receipts" / "formal-vault-write-plan-dry-run-receipt.json",
        "source_file_list": proto / "01 Proposed File List.md",
        "source_approval_matrix": proto / "02 Approval Prompt Matrix.md",
        "source_rollback_manifest": proto / "03 Rollback Manifest.md",
        "source_hash_plan": proto / "04 Hash Check Plan.md",
        "source_stop_conditions": proto / "05 Stop Conditions.md",
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
        "approval_collection",
        "user_approval_inference",
        "external_notification",
    ]


def all_scope_ids(scope: list[dict]) -> list[str]:
    return [item["id"] for item in scope]


def packet_hash_material(base: dict) -> dict:
    return {
        "packet_version": base["packet_version"],
        "source_slice": base["source_slice"],
        "source_bundle_hash": base["source_bundle_hash"],
        "scope_hash": base["approval_scope"]["scope_hash"],
        "approval_questions": [
            {
                "id": item["id"],
                "applies_to_scope_ids": item["applies_to_scope_ids"],
                "future_confirmation_phrase": item["future_confirmation_phrase"],
                "default": item["default"],
                "excludes": item["excludes"],
                "blocks_until_answered": item["blocks_until_answered"],
            }
            for item in base["approval_questions"]
        ],
        "decision_record_template": {
            "status": base["decision_record_template"]["status"],
            "default_verdict": base["decision_record_template"]["default_verdict"],
            "future_verdict_values": base["decision_record_template"]["future_verdict_values"],
            "required_future_fields": base["decision_record_template"]["required_future_fields"],
        },
        "non_approval_receipt": {
            "approval_collected_now": base["non_approval_receipt"]["approval_collected_now"],
            "formal_vault_accessed": base["non_approval_receipt"]["formal_vault_accessed"],
            "current_status": base["non_approval_receipt"]["current_status"],
        },
        "stop_conditions": base["stop_conditions"],
    }


def attach_packet_hashes(base: dict) -> dict:
    material = packet_hash_material(base)
    base["packet_hash_material"] = material
    base["packet_hash"] = sha256_json(material)
    for question in base["approval_questions"]:
        question["required_packet_hash"] = base["packet_hash"]
        question["required_source_bundle_hash"] = base["source_bundle_hash"]
        question["required_scope_hash"] = base["approval_scope"]["scope_hash"]
    base["decision_record_template"]["required_packet_hash"] = base["packet_hash"]
    base["decision_record_template"]["required_source_bundle_hash"] = base["source_bundle_hash"]
    base["decision_record_template"]["required_scope_hash"] = base["approval_scope"]["scope_hash"]
    return base


def config() -> dict:
    paths = source_paths()
    source_cfg = load_json(paths["source_config"])
    source_inputs = [source_input(key, path) for key, path in paths.items() if key != "source_root"]
    scope = []
    for item in source_cfg["proposed_files"]:
        scope.append(
            {
                "id": item["id"],
                "relative_target": item["relative_target"],
                "p2_24_source_path": item["source_path"],
                "p2_24_source_sha256": item["source_sha256"],
                "content_binding": item["content_binding"],
                "future_write_requires_user_approval": True,
                "approval_status": "not_requested",
                "write_enabled_now": False,
                "dry_run_only": True,
            }
        )
    scope_ids = all_scope_ids(scope)
    source_bundle_hash = sha256_json(source_inputs)
    scope_hash = sha256_json(scope)
    base = {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "packet_version": "p2-25-approval-packet-v1",
        "purpose": "Prepare a future formal-vault write approval packet without collecting approval or accessing the formal vault.",
        "formal_vault_path_label": "formal Obsidian vault path is a label only; it is not accessed in this slice",
        "write_scope": [f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"],
        "read_only_sources": [entry["source_path"] for entry in source_inputs],
        "operations": {op: False for op in forbidden_operations()}
        | {"default_read_only": True, "rebuild_requires_explicit_flag": True},
        "boundary_phrases": [
            "sandbox only",
            "approval packet draft only",
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
        "source_packet_inputs": source_inputs,
        "source_bundle_hash": source_bundle_hash,
        "approval_scope": {
            "source_plan_version": source_cfg["plan_version"],
            "source_scope_hash": source_cfg.get("scope_hash", "not_present_in_source"),
            "scope_hash": scope_hash,
            "items": scope,
        },
        "approval_questions": [
            {
                "id": "future_approve_exact_scope",
                "question": "In a future separately approved slice, do you approve writing exactly the listed relative targets to the formal vault?",
                "applies_to_scope_ids": scope_ids,
                "collects_approval_now": False,
                "approval_status": "not_requested",
                "default": "deny",
                "future_confirmation_phrase": "APPROVE EXACT P2 25 PACKET SCOPE FOR FUTURE WRITE ONLY",
                "requires_future_user_turn": True,
                "requires_packet_hash": True,
                "requires_source_bundle_hash": True,
                "requires_scope_hash": True,
                "blocks_until_answered": ["formal_vault_write"],
                "excludes": ["obsidian_sync", "commit", "push", "promotion"],
            },
            {
                "id": "future_approve_source_bindings",
                "question": "In a future separately approved slice, do you accept the exact source SHA256 bindings as the only allowed content basis?",
                "applies_to_scope_ids": scope_ids,
                "collects_approval_now": False,
                "approval_status": "not_requested",
                "default": "deny",
                "future_confirmation_phrase": "APPROVE EXACT SOURCE HASH BINDINGS FOR FUTURE WRITE ONLY",
                "requires_future_user_turn": True,
                "requires_packet_hash": True,
                "requires_source_bundle_hash": True,
                "requires_scope_hash": True,
                "blocks_until_answered": ["formal_vault_write"],
                "excludes": ["obsidian_sync", "commit", "push", "promotion"],
            },
            {
                "id": "future_approve_rollback_hash_checks",
                "question": "In a future separately approved slice, do you approve requiring snapshot, rollback, and hash-before/hash-after checks before any write?",
                "applies_to_scope_ids": scope_ids,
                "collects_approval_now": False,
                "approval_status": "not_requested",
                "default": "deny",
                "future_confirmation_phrase": "APPROVE ROLLBACK AND HASH GATES FOR FUTURE WRITE ONLY",
                "requires_future_user_turn": True,
                "requires_packet_hash": True,
                "requires_source_bundle_hash": True,
                "requires_scope_hash": True,
                "blocks_until_answered": ["formal_vault_write"],
                "excludes": ["obsidian_sync", "commit", "push", "promotion"],
            },
            {
                "id": "future_approve_no_sync_commit_push_promotion",
                "question": "In a future separately approved slice, do you confirm that write approval still excludes sync, commit, push, and promotion unless separately approved?",
                "applies_to_scope_ids": scope_ids,
                "collects_approval_now": False,
                "approval_status": "not_requested",
                "default": "deny",
                "future_confirmation_phrase": "APPROVE NO SYNC COMMIT PUSH OR PROMOTION FOR FUTURE WRITE",
                "requires_future_user_turn": True,
                "requires_packet_hash": True,
                "requires_source_bundle_hash": True,
                "requires_scope_hash": True,
                "blocks_until_answered": ["obsidian_sync", "commit", "push", "promotion"],
                "excludes": ["obsidian_sync", "commit", "push", "promotion"],
            },
        ],
        "decision_record_template": {
            "status": "template_only",
            "approved_now": False,
            "blank_fields_only": True,
            "must_not_prefill_approval": True,
            "default_verdict": "NEEDS_REVISION",
            "future_verdict_values": ["APPROVED_BY_USER", "DENIED_BY_USER", "NEEDS_REVISION"],
            "required_future_fields": [
                "user_exact_text",
                "timestamp_utc",
                "packet_hash",
                "source_bundle_hash",
                "scope_hash",
                "operator_or_agent_id",
                "explicit_denials",
                "rollback_ack",
                "hash_ack",
            ],
        },
        "non_approval_receipt": {
            "approval_collected_now": False,
            "user_approval_text_present": False,
            "formal_vault_accessed": False,
            "current_status": "packet_ready_for_future_user_decision",
            "non_claims": [
                "not actual approval",
                "not formal vault approval",
                "not sync approval",
                "not commit approval",
                "not push approval",
                "not promotion approval",
                "not action basis",
            ],
        },
        "ambiguity_blockers": [
            "future user response missing exact confirmation phrase",
            "future response does not cite packet hash",
            "future response does not cite source bundle hash",
            "future response does not cite scope hash",
            "future response asks for extra files",
            "future response asks for sync, commit, push, or promotion",
            "source hash mismatch",
            "scope hash mismatch",
            "dirty tree or unexpected formal vault file state",
        ],
        "stop_conditions": [
            "formal vault read requested",
            "formal vault scan requested",
            "formal vault write requested before future approval",
            "absolute vault path requested",
            "Obsidian sync requested",
            "commit or push requested",
            "promotion requested",
            "approval collection requested in this slice",
            "approval inferred from silence or prior PASS",
            "missing exact future confirmation phrase",
            "packet hash missing",
            "source bundle hash missing",
            "scope hash missing",
            "source hash mismatch",
            "scope mismatch",
            "rollback or hash gate removed",
        ],
        "inspector_controls": {
            "inputs": [{"id": "q", "type": "search", "purpose": "filter"}],
            "buttons": [
                {"label": "All", "filter": "all"},
                {"label": "Scope", "filter": "scope"},
                {"label": "Questions", "filter": "questions"},
                {"label": "Receipt", "filter": "receipt"},
                {"label": "Stops", "filter": "stops"},
            ],
        },
        "product_metrics": {
            "required_positive_fixtures": 2,
            "minimum_failure_cases": 48,
            "required_scope_items": 5,
            "required_approval_questions": 4,
            "max_journey_steps": 3,
        },
    }
    return attach_packet_hashes(base)


def variant_config(base: dict) -> dict:
    variant = json.loads(json.dumps(base))
    variant["purpose"] = "Variant packet for denial-first future approval rehearsal."
    variant["packet_mode"] = "denial_first_rehearsal"
    variant["non_approval_receipt"]["current_status"] = "packet_ready_for_future_denial_or_revision"
    return attach_packet_hashes(variant)


def failure_cases(base: dict) -> list[tuple[str, dict]]:
    cases: list[tuple[str, dict]] = []

    def expected_list(codes: str | list[str]) -> list[str]:
        return [codes] if isinstance(codes, str) else codes

    def refresh_packet_hash(item: dict) -> None:
        material = packet_hash_material(item)
        item["packet_hash_material"] = material
        item["packet_hash"] = sha256_json(material)
        for question in item["approval_questions"]:
            question["required_packet_hash"] = item["packet_hash"]
            question["required_source_bundle_hash"] = item["source_bundle_hash"]
            question["required_scope_hash"] = item["approval_scope"]["scope_hash"]
        item["decision_record_template"]["required_packet_hash"] = item["packet_hash"]
        item["decision_record_template"]["required_source_bundle_hash"] = item["source_bundle_hash"]
        item["decision_record_template"]["required_scope_hash"] = item["approval_scope"]["scope_hash"]

    def refresh_source_bundle_hash(item: dict) -> None:
        item["source_bundle_hash"] = sha256_json(item["source_packet_inputs"])

    def refresh_scope_hash(item: dict) -> None:
        item["approval_scope"]["scope_hash"] = sha256_json(item["approval_scope"]["items"])

    def refresh_all_hashes(item: dict) -> None:
        refresh_source_bundle_hash(item)
        refresh_scope_hash(item)
        refresh_packet_hash(item)

    def mutate(name: str, codes: str | list[str], fn) -> None:
        item = json.loads(json.dumps(base))
        fn(item)
        item["expected_failures"] = expected_list(codes)
        cases.append((name, item))

    for idx, op in enumerate(forbidden_operations(), start=1):
        mutate(
            f"{idx:02d}-forbidden-{op}.json",
            f"forbidden_operation:{op}",
            lambda c, op=op: c["operations"].__setitem__(op, True),
        )

    mutate("19-absolute-scope-target.json", "scope_target_absolute_or_forbidden:native_home", lambda c: (c["approval_scope"]["items"][0].__setitem__("relative_target", "H:/Obsidian/vault/00 Native Home.md"), refresh_scope_hash(c), refresh_packet_hash(c)))
    mutate("20-scope-write-enabled-now.json", "scope_write_enabled_now:native_home", lambda c: (c["approval_scope"]["items"][0].__setitem__("write_enabled_now", True), refresh_scope_hash(c), refresh_packet_hash(c)))
    mutate("21-scope-already-approved.json", "scope_approval_status_not_requested:native_home", lambda c: (c["approval_scope"]["items"][0].__setitem__("approval_status", "approved"), refresh_scope_hash(c), refresh_packet_hash(c)))
    mutate("22-scope-missing-user-approval.json", "scope_missing_future_user_approval:native_home", lambda c: (c["approval_scope"]["items"][0].__setitem__("future_write_requires_user_approval", False), refresh_scope_hash(c), refresh_packet_hash(c)))
    mutate("23-source-input-path-missing.json", "source_input_path_missing:source_config", lambda c: (c["source_packet_inputs"][6].__setitem__("source_path", ""), refresh_source_bundle_hash(c), refresh_packet_hash(c)))
    mutate("24-source-input-hash-mismatch.json", "source_input_hash_mismatch:source_config", lambda c: (c["source_packet_inputs"][6].__setitem__("source_sha256", "deadbeef"), refresh_source_bundle_hash(c), refresh_packet_hash(c)))
    mutate("25-scope-source-hash-mismatch.json", "scope_source_hash_mismatch:native_home", lambda c: (c["approval_scope"]["items"][0].__setitem__("p2_24_source_sha256", "deadbeef"), refresh_scope_hash(c), refresh_packet_hash(c)))
    mutate("26-question-collects-approval-now.json", "approval_question_collects_now:future_approve_exact_scope", lambda c: c["approval_questions"][0].__setitem__("collects_approval_now", True))
    mutate("27-question-default-approve.json", "approval_question_not_deny:future_approve_exact_scope", lambda c: (c["approval_questions"][0].__setitem__("default", "approve"), refresh_packet_hash(c)))
    mutate("28-question-missing-scope-ids.json", "approval_question_missing_scope_binding:future_approve_exact_scope", lambda c: (c["approval_questions"][0].__setitem__("applies_to_scope_ids", []), refresh_packet_hash(c)))
    mutate("29-question-missing-packet-hash.json", "approval_question_missing_packet_hash:future_approve_exact_scope", lambda c: c["approval_questions"][0].__setitem__("requires_packet_hash", False))
    mutate("30-question-missing-source-bundle-hash.json", "approval_question_missing_source_bundle_hash:future_approve_exact_scope", lambda c: c["approval_questions"][0].__setitem__("requires_source_bundle_hash", False))
    mutate("31-question-missing-scope-hash.json", "approval_question_missing_scope_hash:future_approve_exact_scope", lambda c: c["approval_questions"][0].__setitem__("requires_scope_hash", False))
    mutate("32-question-weak-phrase.json", "approval_question_weak_confirmation_phrase:future_approve_exact_scope", lambda c: (c["approval_questions"][0].__setitem__("future_confirmation_phrase", "ok"), refresh_packet_hash(c)))
    mutate("33-question-missing-sync-exclusion.json", "approval_question_missing_exclusion:future_approve_exact_scope:obsidian_sync", lambda c: (c["approval_questions"][0].__setitem__("excludes", ["commit", "push", "promotion"]), refresh_packet_hash(c)))
    mutate("34-decision-template-not-blank.json", "decision_template_not_blank_only", lambda c: c["decision_record_template"].__setitem__("blank_fields_only", False))
    mutate("35-decision-template-approved-now.json", "decision_template_approved_now", lambda c: c["decision_record_template"].__setitem__("approved_now", True))
    mutate("36-decision-template-prefill-approval.json", "decision_template_prefills_approval", lambda c: c["decision_record_template"].__setitem__("must_not_prefill_approval", False))
    mutate("37-nonapproval-receipt-claims-approval.json", "non_approval_receipt_claims_approval", lambda c: (c["non_approval_receipt"].__setitem__("approval_collected_now", True), refresh_packet_hash(c)))
    mutate("38-receipt-formal-vault-accessed.json", "non_approval_receipt_formal_vault_accessed", lambda c: (c["non_approval_receipt"].__setitem__("formal_vault_accessed", True), refresh_packet_hash(c)))
    mutate("39-missing-stop-formal-vault-write.json", "missing_stop_condition:formal vault write", lambda c: (c["stop_conditions"].remove("formal vault write requested before future approval"), refresh_packet_hash(c)))
    mutate("40-authority-confusing-text.json", "authority_confusing_text", lambda c: c["ambiguity_blockers"].append("this packet approved by this packet"))
    mutate("41-too-few-failure-cases.json", "minimum_failure_cases_too_low", lambda c: c["product_metrics"].__setitem__("minimum_failure_cases", 5))
    mutate("42-inspector-approve-button.json", "inspector_control_not_allowed:button:approve", lambda c: c["inspector_controls"]["buttons"][1].__setitem__("label", "Approve"))
    mutate("43-source-path-outside-source-slice.json", "source_input_path_invalid:source_config", lambda c: (c["source_packet_inputs"][6].__setitem__("source_path", f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/fake.md"), refresh_source_bundle_hash(c), refresh_packet_hash(c)))
    mutate("44-packet-hash-missing.json", "packet_hash_missing", lambda c: c.__setitem__("packet_hash", ""))
    mutate("45-packet-hash-mismatch.json", "packet_hash_mismatch", lambda c: (c.__setitem__("packet_hash", "deadbeef"), [q.__setitem__("required_packet_hash", "deadbeef") for q in c["approval_questions"]], c["decision_record_template"].__setitem__("required_packet_hash", "deadbeef")))
    mutate("46-source-bundle-hash-mismatch.json", "source_bundle_hash_mismatch", lambda c: (c.__setitem__("source_bundle_hash", "deadbeef"), refresh_packet_hash(c)))
    mutate("47-scope-hash-mismatch.json", "scope_hash_mismatch", lambda c: (c["approval_scope"].__setitem__("scope_hash", "deadbeef"), refresh_packet_hash(c)))
    mutate("48-question-required-packet-hash-mismatch.json", "approval_question_packet_hash_value_mismatch:future_approve_exact_scope", lambda c: c["approval_questions"][0].__setitem__("required_packet_hash", "deadbeef"))
    mutate("49-inferred-approval-text.json", "authority_confusing_text", lambda c: c["ambiguity_blockers"].append("prior PASS or user silence counts as approval"))
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

Build a sandbox-only approval packet for a future formal vault write decision.
This slice does not collect approval and does not read, scan, write, sync, hash,
or mutate the formal vault.

## Why This Slice

P2-24 received `PASS_PRODUCT_GRADE` and recommended a
`formal-vault-write-approval-packet-sandbox`.

## Write Scope

```text
outputs/review/vaks-implementation-sandbox/{SLICE_ID}/
```

## Acceptance Standard

- Approval packet remains draft-only and does not collect current approval.
- Every scope item is relative, write-disabled now, and approval status
  `not_requested`.
- Every source input and scope item has exact SHA256 binding.
- Future approval questions default to deny and require packet/source/scope hash.
- Non-approval receipt proves no approval was collected.
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
    scope_rows = []
    for item in base["approval_scope"]["items"]:
        scope_rows.append(f"| `{item['id']}` | `{item['relative_target']}` | `{item['p2_24_source_path']}` | `{item['p2_24_source_sha256']}` | `{item['approval_status']}` |")
    return f"""---
record_kind: sandbox_source_map
slice_id: {SLICE_ID}
status: built_pending_review
truth_boundary: sandbox_only
---

# Source Map

This slice reads P2-24 as the product-grade sandbox source. It does not read or
write the formal Obsidian vault.

| Source | Path | Evidence |
| --- | --- | --- |
{chr(10).join(rows)}

## Scope Bindings

| Scope ID | Relative Target | P2-24 Source Path | P2-24 Source SHA256 | Approval Status |
| --- | --- | --- | --- | --- |
{chr(10).join(scope_rows)}

## Packet Hashes

- source_bundle_hash: `{base['source_bundle_hash']}`
- scope_hash: `{base['approval_scope']['scope_hash']}`
- packet_hash: `{base['packet_hash']}`

## Boundary

P2-24 `PASS_PRODUCT_GRADE` is a sandbox input only. It is not reviewed
knowledge, evidence support, action basis, mainline approval, formal vault
approval, sync approval, commit approval, push approval, or promotion approval.
"""


def render_contract(base: dict) -> str:
    return f"""# Formal Vault Write Approval Packet Contract

## Input Contract

- P2-24 product-grade dry-run plan, reports, fixture, receipt, and prototype
  pages.
- No formal vault read, scan, write, sync, hash, snapshot, or mutation.

## Output Contract

- Future approval scope dossier.
- Future approval questions.
- Non-approval receipt.
- Decision record template.
- Source/hash binding packet.
- Stop condition register.
- Static packet inspector with no write or approval-collection controls.

## Product Promise

A future agent can ask for a precise user approval without inventing scope,
silently collecting approval, or treating this packet as permission to write.

## Boundary Promise

This is an approval packet draft only. Approval is not collected. The formal
vault is not accessed. The packet does not approve action basis, evidence
support, reviewed knowledge, sync, commit, push, promotion, or formal vault
write.

## Hashes

- source_bundle_hash: `{base['source_bundle_hash']}`
- scope_hash: `{base['approval_scope']['scope_hash']}`
- packet_hash: `{base['packet_hash']}`
"""


def render_home(base: dict) -> str:
    return f"""{frontmatter("sandbox_formal_vault_approval_packet_home", "sandbox_pilot")}

# Approval Packet Home

This sandbox prepares a future approval packet without asking for or collecting
approval now.

## Start

1. Open [[01 Scope Dossier]].
2. Open [[02 Future Approval Questions]].
3. Open [[03 Non Approval Receipt]].
4. Open [[06 Stop Conditions]] before any action-facing move.

## Fast Links

- [[01 Scope Dossier]]
- [[02 Future Approval Questions]]
- [[03 Non Approval Receipt]]
- [[04 Decision Record Template]]
- [[05 Source And Hash Binding]]
- [[06 Stop Conditions]]
- [[07 Reviewer Packet]]
- `approval-packet-inspector.html`
- {md_link("P2-24 next-step", "../../../" + SOURCE_SLICE_ID + "/next-step.md")}
- {md_link("P2-24 product acceptance", "../../../" + SOURCE_SLICE_ID + "/product-acceptance-report.md")}

## Boundary Rail

Sandbox only. Approval packet draft only. Not actual approval. Approval not
collected. Formal vault not accessed. Dry-run only. Not reviewed knowledge. Not
evidence support. Not action basis. Does not approve. No formal vault read. No
formal vault write. No sync. No commit. No push. No promotion. Requires separate user approval.
"""


def render_scope(base: dict) -> str:
    rows = ["| ID | Relative Target | P2-24 Source SHA256 | Status |", "| --- | --- | --- | --- |"]
    for item in base["approval_scope"]["items"]:
        rows.append(f"| `{item['id']}` | `{item['relative_target']}` | `{item['p2_24_source_sha256']}` | `{item['approval_status']}` |")
    return f"""{frontmatter("sandbox_approval_scope_dossier", "sandbox_pilot")}

# Scope Dossier

| Packet Field | Value |
| --- | --- |
| source_bundle_hash | `{base['source_bundle_hash']}` |
| scope_hash | `{base['approval_scope']['scope_hash']}` |
| source_plan_version | `{base['approval_scope']['source_plan_version']}` |

## Scope Items

{chr(10).join(rows)}

## Boundary

These are proposed future scope items only. Every item is write-disabled now and
approval status is `not_requested`.

## Next

- [[02 Future Approval Questions]]
- [[06 Stop Conditions]]
"""


def render_questions(base: dict) -> str:
    rows = [
        "| Question ID | Future Confirmation Phrase | Required Packet Hash | Default | Status | Excludes |",
        "| --- | --- | --- | --- | --- | --- |",
    ]
    for item in base["approval_questions"]:
        rows.append(f"| `{item['id']}` | `{item['future_confirmation_phrase']}` | `{item['required_packet_hash']}` | `{item['default']}` | `{item['approval_status']}` | {', '.join(item['excludes'])} |")
    return f"""{frontmatter("sandbox_future_approval_questions", "sandbox_pilot")}

# Future Approval Questions

{chr(10).join(rows)}

## Boundary

These questions are not being asked now. They are future prompts only. They
collect no approval in this slice and cannot authorize sync, commit, push, or
promotion.

## Next

- [[03 Non Approval Receipt]]
- [[06 Stop Conditions]]
"""


def render_non_approval_receipt(base: dict) -> str:
    receipt = base["non_approval_receipt"]
    claims = "\n".join(f"- {item}" for item in receipt["non_claims"])
    return f"""{frontmatter("sandbox_non_approval_receipt", "sandbox_pilot")}

# Non Approval Receipt

| Field | Value |
| --- | --- |
| approval_collected_now | `{receipt['approval_collected_now']}` |
| user_approval_text_present | `{receipt['user_approval_text_present']}` |
| formal_vault_accessed | `{receipt['formal_vault_accessed']}` |
| current_status | `{receipt['current_status']}` |

## Non Claims

{claims}

## Next

- [[04 Decision Record Template]]
- [[06 Stop Conditions]]
"""


def render_decision_template(base: dict) -> str:
    template = base["decision_record_template"]
    fields = "\n".join(f"- `{item}`" for item in template["required_future_fields"])
    verdicts = ", ".join(f"`{item}`" for item in template["future_verdict_values"])
    return f"""{frontmatter("sandbox_decision_record_template", "sandbox_pilot")}

# Decision Record Template

| Field | Value |
| --- | --- |
| status | `{template['status']}` |
| approved_now | `{template['approved_now']}` |
| blank_fields_only | `{template['blank_fields_only']}` |
| must_not_prefill_approval | `{template['must_not_prefill_approval']}` |
| default_verdict | `{template['default_verdict']}` |
| future_verdict_values | {verdicts} |
| required_packet_hash | `{template['required_packet_hash']}` |
| required_source_bundle_hash | `{template['required_source_bundle_hash']}` |
| required_scope_hash | `{template['required_scope_hash']}` |

## Required Future Fields

{fields}

## Boundary

This is a blank template only. It must not be prefilled by an agent and does not
create approval in this slice.
"""


def render_source_binding(base: dict) -> str:
    source_rows = ["| Source ID | Source Path | SHA256 |", "| --- | --- | --- |"]
    for item in base["source_packet_inputs"]:
        source_rows.append(f"| `{item['id']}` | `{item['source_path']}` | `{item['source_sha256']}` |")
    return f"""{frontmatter("sandbox_source_hash_binding", "sandbox_pilot")}

# Source And Hash Binding

| Packet Field | Value |
| --- | --- |
| source_bundle_hash | `{base['source_bundle_hash']}` |
| scope_hash | `{base['approval_scope']['scope_hash']}` |
| packet_hash | `{base['packet_hash']}` |

## Source Inputs

{chr(10).join(source_rows)}

## Boundary

These hashes are process integrity checks only. They are not evidence support,
reviewed knowledge, action basis, or formal vault approval.
"""


def render_stop_conditions(base: dict) -> str:
    rows = "\n".join(f"- {item}" for item in base["stop_conditions"])
    blockers = "\n".join(f"- {item}" for item in base["ambiguity_blockers"])
    return f"""{frontmatter("sandbox_approval_packet_stop_conditions", "sandbox_pilot")}

# Stop Conditions

{rows}

## Ambiguity Blockers

{blockers}

## Safe Alternative

Record the request as a future user decision item and stop. Do not perform the
operation in this slice.
"""


def render_reviewer_packet(base: dict) -> str:
    return f"""{frontmatter("sandbox_reviewer_packet", "sandbox_pilot")}

# Reviewer Packet

## Inspect First

- `artifact/formal-vault-write-approval-packet-contract.md`
- `fixtures/valid-approval-packet-config.json`
- `fixtures/valid-denial-packet-config.json`
- `artifact/failure-case-oracle.md`
- `prototype/formal-vault-write-approval-packet/`
- `artifact/verify_approval_packet.py`

## Review Questions

- Does the packet avoid collecting approval now?
- Does every future approval question default to deny?
- Does each question require packet, source bundle, and scope hashes?
- Are scope items relative and write-disabled now?
- Does the inspector remain read-only and non-approval-collecting?
"""


def render_inspector_html(base: dict) -> str:
    cards = []
    for item in base["approval_scope"]["items"]:
        cards.append(
            f"""<article class=\"card\" data-kind=\"scope\" data-search=\"{item['id']} {item['relative_target']} {item['approval_status']} no formal vault write\">
  <p class=\"eyebrow\">scope</p>
  <h3>{item['id']}</h3>
  <p>{item['relative_target']}</p>
  <strong>{item['approval_status']}</strong>
</article>"""
        )
    for item in base["approval_questions"]:
        cards.append(
            f"""<article class=\"card\" data-kind=\"questions\" data-search=\"{item['id']} future question default deny not requested\">
  <p class=\"eyebrow\">questions</p>
  <h3>{item['id']}</h3>
  <p>{item['question']}</p>
  <strong>default={item['default']}</strong>
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
  <p>Stop on approval collection, formal vault access, sync, commit, push, promotion, or missing hashes.</p>
  <strong>does not approve</strong>
</article>"""
    )
    button_parts = []
    for control in base["inspector_controls"]["buttons"]:
        active = ' class="active"' if control["filter"] == "all" else ""
        button_parts.append(f"<button type=\"button\"{active} data-filter=\"{control['filter']}\">{control['label']}</button>")
    return f"""<!doctype html>
<html lang=\"en\" data-sandbox-only=\"true\" data-approval-packet-draft-only=\"true\" data-no-approval=\"true\" data-no-write=\"true\" data-no-sync=\"true\" data-no-authority=\"true\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>Formal Vault Write Approval Packet</title>
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
    <h1>Formal Vault Write Approval Packet</h1>
    <p>Sandbox-only packet inspector. It cannot collect approval, write, sync, approve, or execute commands.</p>
  </header>
  <div class=\"layout\">
    <main>
      <div class=\"toolbar\" data-role=\"packet-filter\">
        <input id=\"q\" type=\"search\" placeholder=\"Search scope, questions, receipt, stops\">
        {' '.join(button_parts)}
      </div>
      <div class=\"grid\" data-role=\"packet-cards\">
        {chr(10).join(cards)}
      </div>
    </main>
    <aside data-role=\"boundary-rail\">
      <h2>Boundary Rail</h2>
      <ul>
        <li>sandbox only</li>
        <li>approval packet draft only</li>
        <li>not actual approval</li>
        <li>approval not collected</li>
        <li>formal vault not accessed</li>
        <li>not evidence support / not action basis</li>
        <li>no formal vault read / no formal vault write</li>
        <li>no sync / no commit / no push / no promotion</li>
      </ul>
    </aside>
  </div>
  <script type=\"application/json\" id=\"packet-data\">
{json.dumps({"approval_scope": base["approval_scope"], "approval_questions": base["approval_questions"], "non_approval_receipt": base["non_approval_receipt"], "stop_conditions": base["stop_conditions"]}, indent=2)}
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


def render_receipt(base: dict, paths: dict[str, Path]) -> dict:
    source_hashes = {}
    for key, path in paths.items():
        if key == "source_root":
            continue
        source_hashes[key] = sha256(path) if path.exists() else "missing"
    return {
        "record_kind": "sandbox_formal_vault_write_approval_packet_receipt",
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "formal_vault_accessed": False,
        "approval_collected_now": False,
        "write_scope": base["write_scope"],
        "source_hashes": source_hashes,
        "source_bundle_hash": base["source_bundle_hash"],
        "scope_hash": base["approval_scope"]["scope_hash"],
        "packet_hash": base["packet_hash"],
        "scope_items": len(base["approval_scope"]["items"]),
        "future_approval_questions": len(base["approval_questions"]),
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
        raise FileNotFoundError("Missing required P2-24 source files: " + "; ".join(missing))
    base = config()
    git_status_summary = "pre-existing dirty tree recorded before build; final audit scoped to this slice path"

    safe_write("slice-plan.md", render_slice_plan(git_status_summary))
    safe_write("source-map.md", render_source_map(paths, base))
    safe_write("artifact/formal-vault-write-approval-packet-contract.md", render_contract(base))
    safe_write("fixtures/valid-approval-packet-config.json", json.dumps(base, indent=2, ensure_ascii=False))
    safe_write("fixtures/valid-denial-packet-config.json", json.dumps(variant_config(base), indent=2, ensure_ascii=False))

    cases = failure_cases(base)
    for name, item in cases:
        safe_write(f"failure-cases/{name}", json.dumps(item, indent=2, ensure_ascii=False))
    safe_write("artifact/failure-case-oracle.json", json.dumps([{"file": name, "expected_failures": item["expected_failures"]} for name, item in cases], indent=2, ensure_ascii=False))
    safe_write("artifact/failure-case-oracle.md", render_failure_oracle_md(cases))

    proto = "prototype/formal-vault-write-approval-packet"
    safe_write(f"{proto}/00 Approval Packet Home.md", render_home(base))
    safe_write(f"{proto}/01 Scope Dossier.md", render_scope(base))
    safe_write(f"{proto}/02 Future Approval Questions.md", render_questions(base))
    safe_write(f"{proto}/03 Non Approval Receipt.md", render_non_approval_receipt(base))
    safe_write(f"{proto}/04 Decision Record Template.md", render_decision_template(base))
    safe_write(f"{proto}/05 Source And Hash Binding.md", render_source_binding(base))
    safe_write(f"{proto}/06 Stop Conditions.md", render_stop_conditions(base))
    safe_write(f"{proto}/07 Reviewer Packet.md", render_reviewer_packet(base))
    safe_write(f"{proto}/approval-packet-inspector.html", render_inspector_html(base))
    safe_write(f"{proto}/Receipts/formal-vault-write-approval-packet-receipt.json", json.dumps(render_receipt(base, paths), indent=2, ensure_ascii=False))

    safe_write("verification.md", render_verification_pending(), overwrite=False)
    safe_write("reviewer-report.md", render_pending("sandbox_reviewer_report", "Reviewer Report"), overwrite=False)
    safe_write("boundary-audit.md", render_pending("sandbox_boundary_audit", "Boundary Audit"), overwrite=False)
    safe_write("product-acceptance-report.md", render_pending("sandbox_product_acceptance_report", "Product Acceptance Report"), overwrite=False)
    safe_write("next-step.md", render_pending("sandbox_next_step", "Next Step"), overwrite=False)


if __name__ == "__main__":
    build()
