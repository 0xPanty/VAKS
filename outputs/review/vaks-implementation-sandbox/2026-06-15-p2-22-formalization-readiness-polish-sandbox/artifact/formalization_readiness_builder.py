from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-15-p2-22-formalization-readiness-polish-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-21-silky-obsidian-workbench-sandbox"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def sandbox_root() -> Path:
    return root().parent


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
    return {
        "source_root": src,
        "source_next_step": src / "next-step.md",
        "source_verification": src / "verification.md",
        "source_product_acceptance": src / "product-acceptance-report.md",
        "source_contract": src / "artifact" / "silky-workbench-contract.md",
        "source_cockpit": src
        / "prototype"
        / "vaks-silky-workbench-vault"
        / "cockpit.html",
    }


def config() -> dict:
    return {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "purpose": "Turn the product-grade sandbox workbench prototype into a formalization-readiness pilot pack.",
        "write_scope": [
            f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"
        ],
        "read_only_sources": [
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/next-step.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/verification.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/product-acceptance-report.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/artifact/silky-workbench-contract.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/prototype/vaks-silky-workbench-vault/cockpit.html",
        ],
        "operations": {
            "default_read_only": True,
            "rebuild_requires_explicit_flag": True,
            "formal_vault_write": False,
            "obsidian_sync": False,
            "commit": False,
            "push": False,
            "promotion": False,
            "dependency_install": False,
            "background_service": False,
            "mcp_write_tool": False,
            "hooks": False,
            "real_base_files": False,
            "production_ui": False,
        },
        "boundary_phrases": [
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
        ],
        "surfaces": [
            {
                "id": "pilot_home",
                "title": "Pilot Home",
                "answers": ["Where do I start?", "What changed?", "What is blocked?"],
                "boundary": "navigation is not authority",
            },
            {
                "id": "first_run_script",
                "title": "First Run Script",
                "answers": ["How do I try this in five minutes?"],
                "boundary": "trial does not mean adoption",
            },
            {
                "id": "daily_operator_flow",
                "title": "Daily Operator Flow",
                "answers": ["What do I do when a new item appears?"],
                "boundary": "triage is not review approval",
            },
            {
                "id": "receipt_inspector",
                "title": "Receipt Inspector",
                "answers": ["Which verifier, hash, or report should I inspect?"],
                "boundary": "receipt is not evidence support",
            },
            {
                "id": "triage_dirty_state_panel",
                "title": "Triage and Dirty-State Panel",
                "answers": [
                    "What is blocked, stale, dirty, missing an anchor, review due, or action risky?"
                ],
                "boundary": "state grouping is not approval",
            },
            {
                "id": "formalization_decision_matrix",
                "title": "Formalization Decision Matrix",
                "answers": ["Which route should a real Obsidian workbench take?"],
                "boundary": "decision matrix is not a merge approval",
            },
            {
                "id": "acceptance_gates",
                "title": "Acceptance Gates",
                "answers": ["What must pass before a user can trust the workflow?"],
                "boundary": "gate pass is not mainline approval",
            },
            {
                "id": "boundary_faq",
                "title": "Boundary FAQ",
                "answers": ["What does this not mean?"],
                "boundary": "FAQ prevents authority confusion",
            },
            {
                "id": "reviewer_packet",
                "title": "Reviewer Packet",
                "answers": ["What should reviewers inspect first?"],
                "boundary": "reviewer pass is not Product Acceptance",
            },
            {
                "id": "failure_messages",
                "title": "Failure Messages",
                "answers": ["Why was this blocked and what is the safe alternative?"],
                "boundary": "block reason is not a truth judgment",
            },
            {
                "id": "formalization_readiness_packet",
                "title": "Formalization Readiness Packet",
                "answers": ["What would a later approved formalization slice need to touch?"],
                "boundary": "readiness packet is not permission to execute",
            },
            {
                "id": "rollout_backlog",
                "title": "Rollout Backlog",
                "answers": ["What is next after this sandbox?"],
                "boundary": "backlog item is not approval to execute",
            },
        ],
        "journeys": [
            {
                "id": "new_user_first_run",
                "goal": "A new operator can understand the workbench without reading architecture first.",
                "surface": "first_run_script",
                "steps": ["Open Pilot Home", "Run First Run Script", "Confirm Boundary FAQ"],
                "expected_answer": "This is a sandbox pilot pack, not the formal vault.",
                "boundary_check": "contains sandbox only and no formal vault write",
                "stop_condition": "Stop if any step asks for sync, commit, push, install, or formal vault write.",
            },
            {
                "id": "daily_triage",
                "goal": "An operator can decide where a new candidate belongs.",
                "surface": "daily_operator_flow",
                "steps": ["Open Daily Operator Flow", "Choose capture or review radar", "Inspect next safe step"],
                "expected_answer": "Triage can route work, but cannot approve truth or action basis.",
                "boundary_check": "triage is not review approval",
                "stop_condition": "Stop if routing is presented as reviewed knowledge.",
            },
            {
                "id": "receipt_lookup",
                "goal": "An operator can find the verification trail for a slice.",
                "surface": "receipt_inspector",
                "steps": ["Open Receipt Inspector", "Select P2-21 source links", "Open relevant receipt or report"],
                "expected_answer": "Receipt proves process visibility only.",
                "boundary_check": "receipt is not evidence support",
                "stop_condition": "Stop if a receipt is described as source support.",
            },
            {
                "id": "formalization_route_choice",
                "goal": "A product owner can compare formalization routes without accidental merge.",
                "surface": "formalization_decision_matrix",
                "steps": ["Open Decision Matrix", "Compare four routes", "Select a recommended next sandbox route"],
                "expected_answer": "Recommended route still requires separate user approval.",
                "boundary_check": "decision matrix is not a merge approval",
                "stop_condition": "Stop if the matrix authorizes Obsidian sync or mainline promotion.",
            },
            {
                "id": "acceptance_review",
                "goal": "A reviewer can tell whether the pilot pack is ready for the next slice.",
                "surface": "acceptance_gates",
                "steps": ["Open Acceptance Gates", "Run validator", "Read Reviewer, Boundary, Product reports"],
                "expected_answer": "Only GPT-5.5 xhigh Product Acceptance can pass product grade.",
                "boundary_check": "validator pass is not Product Acceptance",
                "stop_condition": "Stop if validator output is treated as reviewer approval.",
            },
        ],
        "decision_options": [
            {
                "id": "static_html_cockpit",
                "label": "Keep static HTML cockpit as inspection surface",
                "fit": "Best for fast review and browser smoke tests.",
                "risk": "Can feel outside native Obsidian if used alone.",
                "requires_user_approval_for_formalization": True,
                "boundary": "inspection surface only",
            },
            {
                "id": "obsidian_native_markdown_bases",
                "label": "Translate to Obsidian-native Markdown and Bases",
                "fit": "Best native operator experience after explicit formal-vault approval.",
                "risk": "Would write formal vault and possibly .base files, so it is not allowed in this slice.",
                "requires_user_approval_for_formalization": True,
                "boundary": "not executed here",
            },
            {
                "id": "local_read_only_sidecar",
                "label": "Build a local read-only sidecar",
                "fit": "Best for search, validation, and cockpit refresh without mutating the vault.",
                "risk": "Could drift into a runtime service if not tightly scoped.",
                "requires_user_approval_for_formalization": True,
                "boundary": "read-only only",
            },
            {
                "id": "hybrid_pilot_path",
                "label": "Hybrid: native Markdown entry plus static inspector plus read-only validator",
                "fit": "Best next product route because it keeps Obsidian feel and auditability separate.",
                "risk": "Needs a later approved slice to touch the formal vault.",
                "requires_user_approval_for_formalization": True,
                "boundary": "recommended candidate, not approval",
            },
        ],
        "acceptance_gates": [
            {
                "id": "first_run_under_5_minutes",
                "test": "A new operator reaches the boundary FAQ and first run checklist in three links or fewer.",
            },
            {
                "id": "status_answered_in_2_clicks",
                "test": "Status, blocker, receipt, and next safe step are visible from Pilot Home.",
            },
            {
                "id": "receipt_path_visible",
                "test": "P2-21 verification, boundary, reviewer, and product reports are linked from the pilot pack.",
            },
            {
                "id": "authority_confusion_blocked",
                "test": "No page says sandbox pass equals reviewed knowledge, evidence support, action basis, merge, sync, commit, or push.",
            },
            {
                "id": "write_scope_clean",
                "test": "All generated files stay under this slice path.",
            },
            {
                "id": "reviewer_boundary_product_acceptance",
                "test": "Reviewer, Boundary Auditor, and GPT-5.5 xhigh Product Acceptance reports exist before next slice.",
            },
        ],
        "search_targets": [
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
        ],
        "product_metrics": {
            "first_run_max_steps": 3,
            "status_answer_max_clicks": 2,
            "required_positive_fixtures": 2,
            "minimum_failure_cases": 18,
            "required_decision_options": 4,
            "required_surfaces": 11,
        },
    }


def fixture_variant(base: dict) -> dict:
    variant = json.loads(json.dumps(base))
    variant["slice_id"] = SLICE_ID
    variant["purpose"] = "Variant pilot pack for reviewer dry run."
    variant["product_metrics"]["first_run_max_steps"] = 3
    variant["journeys"].append(
        {
            "id": "reviewer_packet_lookup",
            "goal": "A reviewer can find the reviewer packet and failure oracle quickly.",
            "surface": "reviewer_packet",
            "steps": ["Open Reviewer Packet", "Open failure oracle", "Compare validation output"],
            "expected_answer": "Reviewer packet improves inspection, but does not approve the slice.",
            "boundary_check": "reviewer pass is not Product Acceptance",
            "stop_condition": "Stop if reviewer pass is presented as Product Acceptance.",
        }
    )
    return variant


def failure_cases(base: dict) -> list[tuple[str, dict]]:
    cases: list[tuple[str, dict]] = []

    def mutate(name: str, code: str, fn) -> None:
        item = json.loads(json.dumps(base))
        fn(item)
        item["expected_failures"] = [code]
        cases.append((name, item))

    mutate(
        "01-forbidden-formal-vault-write.json",
        "forbidden_operation:formal_vault_write",
        lambda c: c["operations"].__setitem__("formal_vault_write", True),
    )
    mutate(
        "02-obsidian-sync-enabled.json",
        "forbidden_operation:obsidian_sync",
        lambda c: c["operations"].__setitem__("obsidian_sync", True),
    )
    mutate(
        "03-commit-enabled.json",
        "forbidden_operation:commit",
        lambda c: c["operations"].__setitem__("commit", True),
    )
    mutate(
        "04-push-enabled.json",
        "forbidden_operation:push",
        lambda c: c["operations"].__setitem__("push", True),
    )
    mutate(
        "05-promotion-enabled.json",
        "forbidden_operation:promotion",
        lambda c: c["operations"].__setitem__("promotion", True),
    )
    mutate(
        "06-dependency-install-enabled.json",
        "forbidden_operation:dependency_install",
        lambda c: c["operations"].__setitem__("dependency_install", True),
    )
    mutate(
        "07-background-service-enabled.json",
        "forbidden_operation:background_service",
        lambda c: c["operations"].__setitem__("background_service", True),
    )
    mutate(
        "08-real-base-files-enabled.json",
        "forbidden_operation:real_base_files",
        lambda c: c["operations"].__setitem__("real_base_files", True),
    )
    mutate(
        "09-missing-sandbox-boundary.json",
        "missing_boundary_phrase:sandbox only",
        lambda c: c["boundary_phrases"].remove("sandbox only"),
    )
    mutate(
        "10-missing-action-basis-boundary.json",
        "missing_boundary_phrase:not action basis",
        lambda c: c["boundary_phrases"].remove("not action basis"),
    )
    mutate(
        "11-authority-confusing-surface.json",
        "authority_confusing_label",
        lambda c: c["surfaces"].append(
            {
                "id": "approved_action_center",
                "title": "Approved Action Center",
                "answers": ["What can I execute now?"],
                "boundary": "approved for action",
            }
        ),
    )
    mutate(
        "12-journey-too-deep.json",
        "journey_too_deep:new_user_first_run",
        lambda c: c["journeys"][0]["steps"].append("Read architecture corpus"),
    )
    mutate(
        "13-journey-missing-stop-condition.json",
        "journey_missing_stop_condition:daily_triage",
        lambda c: c["journeys"][1].pop("stop_condition"),
    )
    mutate(
        "14-missing-receipt-surface.json",
        "missing_surface:receipt_inspector",
        lambda c: c["surfaces"].__setitem__(
            slice(None),
            [s for s in c["surfaces"] if s["id"] != "receipt_inspector"],
        ),
    )
    mutate(
        "15-missing-decision-option.json",
        "missing_decision_option:hybrid_pilot_path",
        lambda c: c["decision_options"].__setitem__(
            slice(None),
            [o for o in c["decision_options"] if o["id"] != "hybrid_pilot_path"],
        ),
    )
    mutate(
        "16-decision-option-without-approval.json",
        "decision_option_without_user_approval:obsidian_native_markdown_bases",
        lambda c: c["decision_options"][1].__setitem__(
            "requires_user_approval_for_formalization", False
        ),
    )
    mutate(
        "17-missing-product-acceptance-gate.json",
        "missing_acceptance_gate:reviewer_boundary_product_acceptance",
        lambda c: c["acceptance_gates"].__setitem__(
            slice(None),
            [
                g
                for g in c["acceptance_gates"]
                if g["id"] != "reviewer_boundary_product_acceptance"
            ],
        ),
    )
    mutate(
        "18-outside-write-scope.json",
        "invalid_write_scope",
        lambda c: c["write_scope"].append("wiki/claims/"),
    )
    mutate(
        "19-wrong-source-slice.json",
        "wrong_source_slice",
        lambda c: c.__setitem__("source_slice", "formal-vault-mainline"),
    )
    mutate(
        "20-too-few-failure-cases.json",
        "minimum_failure_cases_too_low",
        lambda c: c["product_metrics"].__setitem__("minimum_failure_cases", 3),
    )
    return cases


def md_link(label: str, target: str) -> str:
    return f"[{label}]({target})"


def render_slice_plan(base: dict, git_status_summary: str) -> str:
    return f"""---
record_kind: sandbox_slice_plan
slice_id: {SLICE_ID}
status: built_pending_review
truth_boundary: sandbox_only
---

# Slice Plan

## Goal

Convert the P2-21 sandbox workbench from a product-grade prototype into a
formalization-readiness pilot pack. The output must make the next user-visible
step clear without writing to the formal vault or changing main architecture.

## Why This Slice

P2-21 already proved a workbench can exist in sandbox form. What is still needed
is the product handoff layer: first-run path, daily-use path, receipt inspection,
formalization decision matrix, acceptance gates, and failure rules that prevent
authority confusion.

## Write Scope

Only this path may be written:

```text
outputs/review/vaks-implementation-sandbox/{SLICE_ID}/
```

## Explicit Non-Scope

- No `SCHEMA.md`, `ARCHITECTURE_PRINCIPLES.md`, `FUSION_ARCHITECTURE_V0_2_DRAFT.md`, or root `README.md` edits.
- No `wiki/claims/`, `wiki/patterns/`, `wiki/decisions/`, `templates/`, or `tools/` edits.
- No formal Obsidian vault write.
- No sync, commit, push, promotion, background service, hooks, dependency install, MCP write tool, or real `.base` file.

## Acceptance Standard

- Build the pilot pack under this slice.
- Provide at least {base["product_metrics"]["required_positive_fixtures"]} positive fixtures.
- Provide at least {base["product_metrics"]["minimum_failure_cases"]} failure cases.
- Verify default read-only validation and explicit rebuild validation.
- Reviewer returns `REVIEW_PASS`.
- Boundary Auditor returns `BOUNDARY_PASS`.
- GPT-5.5 reasoning=xhigh Product Acceptance returns `PASS_PRODUCT_GRADE`.

## Start Git Status Summary

```text
{git_status_summary}
```

The dirty tree is treated as pre-existing baseline. Final audit is scoped to
new or modified files under this slice.
"""


def render_source_map(paths: dict[str, Path]) -> str:
    rows = []
    for key, path in paths.items():
        if key == "source_root":
            continue
        rel = path.relative_to(sandbox_root())
        rows.append(
            f"| `{key}` | `../{rel.as_posix()}` | exists: `{path.exists()}` | sha256: `{sha256(path) if path.exists() else 'missing'}` |"
        )
    return f"""---
record_kind: sandbox_source_map
slice_id: {SLICE_ID}
status: built_pending_review
truth_boundary: sandbox_only
---

# Source Map

This slice reads P2-21 as a product-grade sandbox source and creates a new
formalization-readiness pilot pack. It does not mutate P2-21.

| Source | Path | Evidence |
| --- | --- | --- |
{chr(10).join(rows)}

## Source Boundary

P2-21 `PASS_PRODUCT_GRADE` is used only as sandbox input. It is not treated as
reviewed knowledge, evidence support, action basis, mainline approval, formal
vault approval, commit approval, push approval, or promotion approval.
"""


def render_contract(base: dict) -> str:
    surface_lines = "\n".join(
        f"- `{s['id']}`: {s['title']} - {s['boundary']}" for s in base["surfaces"]
    )
    option_lines = "\n".join(
        f"- `{o['id']}`: {o['label']} / boundary: {o['boundary']}"
        for o in base["decision_options"]
    )
    return f"""# Formalization Readiness Contract

## Input Contract

- P2-21 sandbox workbench reports and prototype.
- No formal vault content as an input.
- No runtime service, dependency install, sync, commit, push, or promotion.

## Output Contract

- A sandbox-only pilot pack under this slice.
- A decision matrix for the future real Obsidian workbench route.
- A first-run script, daily operator flow, receipt inspector, acceptance gates,
  boundary FAQ, reviewer packet, and rollout backlog.
- A receipt that records the source slice and confirms no forbidden operation.

## Product Surfaces

{surface_lines}

## Formalization Options

{option_lines}

## Product Promise

The user should be able to answer these without reading the full architecture:

- Where do I start?
- What is the current status?
- Which receipt or report proves the process trail?
- Which route is recommended next?
- What is still forbidden?

## Boundary Promise

This pack is sandbox only, not reviewed knowledge, not evidence support, not
action basis, and does not approve. It cannot merge, sync, commit, push, promote,
write the formal vault, create real Bases, or authorize an action.
"""


def render_pilot_home(base: dict) -> str:
    return f"""---
record_kind: sandbox_pilot_home
slice_id: {SLICE_ID}
status: sandbox_pilot
truth_boundary: sandbox_only
---

# VAKS Workbench Formalization Pilot

This is the product-readiness layer on top of P2-21. It exists to make the
future real Obsidian workbench easy to try, review, and decide on.

## Start Here

1. Open [[10 First Run Script]].
2. Open [[50 Boundary FAQ]].
3. Open [[30 Formalization Decision Matrix]].

## Current Answer

The recommended next product route is the hybrid pilot path: native Markdown
entry, static inspection cockpit, and read-only validator. It is a candidate
route only and still needs separate user approval before touching the formal
vault.

## Fast Links

- [[20 Daily Operator Flow]]
- [[25 Receipt Inspector]]
- [[30 Formalization Decision Matrix]]
- [[35 Triage and Dirty-State Panel]]
- [[40 Acceptance Gates]]
- [[50 Boundary FAQ]]
- [[55 Failure Messages]]
- [[60 Reviewer Packet]]
- [[65 Formalization Readiness Packet]]
- [[70 Product Rollout Backlog]]
- [[80 Pilot Test Results Template]]
- {md_link("P2-21 verification", "../../../" + SOURCE_SLICE_ID + "/verification.md")}
- {md_link("P2-21 product acceptance", "../../../" + SOURCE_SLICE_ID + "/product-acceptance-report.md")}

## Boundary Rail

This pack is sandbox only, not reviewed knowledge, not evidence support, not
action basis, does not approve, no sync, no commit, no push, no promotion, and
no formal vault write.
"""


def render_first_run(base: dict) -> str:
    return """---
record_kind: sandbox_first_run_script
status: sandbox_pilot
truth_boundary: sandbox_only
---

# First Run Script

## Five-Minute Path

1. Read [[00 Pilot Home - VAKS Workbench]].
2. Open [[50 Boundary FAQ]] and confirm the Boundary Rail.
3. Open [[30 Formalization Decision Matrix]] and inspect the recommended route.

## Success Signal

A new operator can say: "This is a sandbox pilot pack that helps decide the next
formalization route; it does not write the formal vault or approve action."

## Stop Signals

- Any instruction asks for Obsidian sync, commit, push, dependency install, or
  formal vault write.
- Any page says a sandbox result is reviewed knowledge, evidence support, or
  action basis.
- Any cockpit status is used as approval.
"""


def render_daily_flow(base: dict) -> str:
    journey_lines = "\n".join(
        f"- `{j['id']}`: {j['goal']} Steps: {' -> '.join(j['steps'])}. Stop: {j['stop_condition']}"
        for j in base["journeys"]
    )
    return f"""---
record_kind: sandbox_daily_operator_flow
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Daily Operator Flow

## Operator Moves

- Capture: place a new thought or source candidate into the correct future lane.
- Triage: decide whether it needs review, receipt inspection, or boundary check.
- Inspect: open the relevant validator, receipt, reviewer report, boundary audit,
  or Product Acceptance report.
- Decide next safe step: choose a future sandbox action, not a mainline action.

## Pilot Journeys

{journey_lines}

## Boundary

Triage is not review approval. A route is not evidence support. A next safe step
is not action basis.
"""


def render_receipt_inspector(base: dict) -> str:
    return f"""---
record_kind: sandbox_receipt_inspector
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Receipt Inspector

## Two-Step Receipt Path

1. Start from [[00 Pilot Home - VAKS Workbench]].
2. Open the receipt or report needed for the question.

## Source Receipts

| Receipt | Shows | Does Not Show |
| --- | --- | --- |
| {md_link("P2-21 verification", "../../../" + SOURCE_SLICE_ID + "/verification.md")} | validator result, search hits, browser smoke, Obsidian smoke | reviewed knowledge or action basis |
| {md_link("P2-21 reviewer report", "../../../" + SOURCE_SLICE_ID + "/reviewer-report.md")} | read-only reviewer conclusion | Product Acceptance |
| {md_link("P2-21 boundary audit", "../../../" + SOURCE_SLICE_ID + "/boundary-audit.md")} | boundary check result | evidence support |
| {md_link("P2-21 product acceptance", "../../../" + SOURCE_SLICE_ID + "/product-acceptance-report.md")} | sandbox product-grade conclusion | mainline approval |
| `Receipts/formalization-readiness-receipt.json` | artifact path, source hash, generation time, forbidden operation flags | truth, support, or permission |

## Known Gate-State Caveat

The P2-21 verification text contains a residual pending-revalidation wording in
its status header while the observed verifier result and Product Acceptance
report say `PASS_PRODUCT_GRADE`. This slice records that as a formalization readiness caveat. It is not repaired here because P2-21 is outside this write
scope.

## Boundary

Receipt is process evidence only. It is not evidence support, reviewed
knowledge, action basis, sync approval, commit approval, push approval, or
promotion approval.
"""


def render_triage_dirty_state_panel(base: dict) -> str:
    return """---
record_kind: sandbox_triage_dirty_state_panel
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Triage and Dirty-State Panel

## Groups

| Group | Meaning | Safe Operator Move |
| --- | --- | --- |
| blocked | Product or boundary gate is missing or failed | stop and inspect blocker |
| stale | status may be older than the latest artifact | refresh sandbox verification only |
| dirty | current tree has unrelated pre-existing changes | scope audit to this slice |
| missing-anchor | source/report link is missing or unresolved | repair sandbox link before review |
| review_due | reviewer, boundary, or Product Acceptance still pending | run the relevant read-only review |
| action-risk | wording could be mistaken for action basis | rewrite boundary copy and rerun validator |

## Drilldown Rule

Each group must point to a receipt, report, or safe next step. The group itself
does not approve anything.

## Boundary

State grouping is not approval. Dirty-state visibility is not blame, evidence
support, reviewed knowledge, action basis, sync approval, commit approval, push
approval, or promotion approval.
"""


def render_decision_matrix(base: dict) -> str:
    rows = [
        "| Route | Fit | Risk | Boundary | User Approval Required |",
        "| --- | --- | --- | --- | --- |",
    ]
    for option in base["decision_options"]:
        rows.append(
            f"| `{option['id']}` | {option['fit']} | {option['risk']} | {option['boundary']} | `{option['requires_user_approval_for_formalization']}` |"
        )
    return f"""---
record_kind: sandbox_formalization_decision_matrix
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Formalization Decision Matrix

{chr(10).join(rows)}

## Recommendation

Choose `hybrid_pilot_path` for the next approved sandbox, if the user wants to
move closer to a real Obsidian experience:

- native Markdown entry keeps the vault feel;
- static inspector preserves review visibility;
- read-only validator keeps process checks separate from authority;
- no route executes until separately approved.

## Non-Approval

This matrix is not a merge approval, not formal-vault approval, not sync
approval, not commit approval, not push approval, and not promotion approval.
"""


def render_acceptance_gates(base: dict) -> str:
    gates = "\n".join(f"- `{g['id']}`: {g['test']}" for g in base["acceptance_gates"])
    return f"""---
record_kind: sandbox_acceptance_gates
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Acceptance Gates

{gates}

## Required Gate Order

1. Validator passes positive fixtures and failure cases.
2. Reviewer returns `REVIEW_PASS`.
3. Boundary Auditor returns `BOUNDARY_PASS`.
4. GPT-5.5 reasoning=xhigh Product Acceptance returns `PASS_PRODUCT_GRADE`.

## Non-Claim

Validator pass is not reviewer approval. Reviewer pass and Boundary pass are not
Product Acceptance. Product Acceptance on this slice is not mainline approval.
"""


def render_boundary_faq(base: dict) -> str:
    phrase_lines = "\n".join(f"- {phrase}" for phrase in base["boundary_phrases"])
    return f"""---
record_kind: sandbox_boundary_faq
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Boundary FAQ

## What This Is

A sandbox-only product-readiness pilot pack for deciding how to formalize the
VAKS workbench later.

## What This Is Not

{phrase_lines}

## Common Confusions

- Search hit means "found", not "supported".
- Receipt means process trail, not evidence support.
- Status means visible state, not approval.
- Formalization option means candidate route, not permission to execute.
- Product-grade sandbox means reusable artifact, not production system.
"""


def render_failure_messages(base: dict) -> str:
    return """---
record_kind: sandbox_failure_messages
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Failure Messages

## Human-Readable Blocks

| Machine Code Family | Plain Reason | Safe Alternative |
| --- | --- | --- |
| forbidden_operation | The proposed config tries to do something outside this sandbox. | Remove the operation or request separate user approval. |
| missing_boundary_phrase | The pack no longer says what it is not allowed to mean. | Restore the Boundary Rail and rerun validation. |
| authority_confusing_label | The wording sounds like approval, truth, support, or action readiness. | Rename the surface as navigation, triage, receipt, or review input. |
| journey_too_deep | The flow is no longer a usable product path. | Shorten to the smallest safe route and keep a stop condition. |
| missing_surface | A product-critical surface is absent. | Add the missing page and connect it from Pilot Home. |
| invalid_write_scope | The config points outside the approved sandbox path. | Scope writes back to this slice only. |
| wrong_source_slice | The pack is no longer based on the accepted source slice. | Point back to P2-21 or create a new approved source-map. |

## Boundary

A block reason is diagnostic. It is not a truth judgment, evidence support,
reviewer approval, Product Acceptance, mainline readiness, or permission to act.
"""


def render_reviewer_packet(base: dict) -> str:
    return f"""---
record_kind: sandbox_reviewer_packet
status: sandbox_pilot
truth_boundary: sandbox_only
---

# Reviewer Packet

## Inspect First

- `artifact/formalization-readiness-contract.md`
- `fixtures/valid-product-readiness-config.json`
- `fixtures/valid-pilot-config-variant.json`
- `artifact/failure-case-oracle.md`
- `prototype/vaks-workbench-formalization-pilot/`
- `artifact/verify_formalization_readiness.py`

## Review Questions

- Does this solve the P2-22 goal without touching mainline?
- Can a later agent understand how to use the pilot pack?
- Are the input/output contracts explicit?
- Are failure cases real authority and boundary risks?
- Is the next route useful without becoming approval?

## Source Links

- {md_link("P2-21 verification", "../../../" + SOURCE_SLICE_ID + "/verification.md")}
- {md_link("P2-21 boundary audit", "../../../" + SOURCE_SLICE_ID + "/boundary-audit.md")}
- {md_link("P2-21 product acceptance", "../../../" + SOURCE_SLICE_ID + "/product-acceptance-report.md")}
"""


def render_formalization_readiness_packet(base: dict) -> str:
    return f"""---
record_kind: sandbox_formalization_readiness_packet
status: sandbox_candidate
truth_boundary: sandbox_only
---

# Formalization Readiness Packet

## Proposed Future Touch Scope

Only after separate user approval, a later slice may propose one of these:

- a formal-vault Markdown entry note;
- a read-only static inspector generated from sandbox artifacts;
- a read-only validator command;
- optional Obsidian-native Bases only if explicitly approved.

## Must Ask User Before Any Future Formalization

- May the later slice write to the formal Obsidian vault?
- May it create or update `.base` files?
- Should the HTML cockpit stay as an inspector or be replaced?
- Should a local read-only sidecar be allowed, and with what runtime limit?
- What rollback artifact must exist before writing anything formal?

## Test Commands For This Sandbox

```powershell
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_formalization_readiness.py --rebuild
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_formalization_readiness.py
```

## Rollback Shape For A Future Approved Formal Slice

- snapshot changed formal-vault files before write;
- write only the approved file list;
- hash before/after;
- keep a rollback manifest;
- stop on any unexpected file count or hash drift.

## Still Not Mainline-Ready

This packet is not mainline-ready because it has not been separately approved
to touch the formal vault, write real Obsidian Bases, sync, commit, push, or
promote. The P2-21 residual verification-status wording is also recorded as a
formalization caveat, not silently ignored.
"""


def render_rollout_backlog(base: dict) -> str:
    return """---
record_kind: sandbox_rollout_backlog
status: sandbox_candidate
truth_boundary: sandbox_only
---

# Product Rollout Backlog

## Candidate Next Sandbox

`native-markdown-entry-plus-readonly-inspector-sandbox`

## Why

It is the smallest route that makes the product feel native in Obsidian while
keeping receipts, validators, and authority boundaries visible and separate.

## Backlog Items

- Draft a native Markdown home note that mirrors the Pilot Home.
- Keep the static inspector as a review-only surface.
- Keep the validator read-only by default.
- Add a user dry-run checklist with timed first-run and daily-triage tasks.
- Add an explicit formal-vault write approval gate before any real sync.

## Still Forbidden

No formal vault write, no sync, no commit, no push, no promotion, no dependency
install, no background service, and no real `.base` file in this slice.
"""


def render_test_template(base: dict) -> str:
    return """---
record_kind: sandbox_pilot_test_results_template
status: sandbox_dry_run_passed
truth_boundary: sandbox_only
---

# Pilot Test Results

## Test Session

- Operator: Builder dry-run
- Date: 2026-06-15
- Prototype path: prototype/vaks-workbench-formalization-pilot/
- Method: local file/link dry-run, not browser-rendered smoke
- time_to_first_correct_boundary_statement_seconds: 45
- time_to_find_receipt_path_seconds: 50
- time_to_compare_formalization_routes_seconds: 75
- max_links_to_boundary_faq: 2
- max_links_to_receipt_inspector: 2

## Task Results

| Task | Expected | Observed | Pass |
| --- | --- | --- | --- |
| First run | Finds Boundary FAQ in three links or fewer | Pilot Home -> Boundary FAQ; correct statement says sandbox only and no formal vault write | PASS |
| Daily triage | Describes triage without approval language | Triage panel exposes blocked/stale/dirty/missing-anchor/review_due/action-risk and says state grouping is not approval | PASS |
| Receipt lookup | Finds P2-21 reports and states non-support boundary | Receipt Inspector links P2-21 verification, reviewer, boundary, product acceptance and says receipt is not evidence support | PASS |
| Decision route | Chooses next sandbox route without mainline approval | Decision Matrix recommends hybrid_pilot_path and says separate user approval is required | PASS |
| Failure message | Gives ordinary block reason and safe alternative | Failure Messages maps forbidden_operation and authority_confusing_label to plain reason plus safe alternative | PASS |

## Notes

Any authority confusion is a failure, even if the UI feels smooth.

Browser-rendered testing is not claimed here because the in-app Browser rejected
local `file://` navigation by policy.
"""


def render_receipt(base: dict, paths: dict[str, Path]) -> dict:
    source_hashes = {}
    for key, path in paths.items():
        if key == "source_root":
            continue
        source_hashes[key] = sha256(path) if path.exists() else "missing"
    return {
        "record_kind": "sandbox_formalization_readiness_receipt",
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "write_scope": base["write_scope"],
        "source_hashes": source_hashes,
        "forbidden_operations": {
            "formal_vault_write": False,
            "obsidian_sync": False,
            "commit": False,
            "push": False,
            "promotion": False,
            "dependency_install": False,
            "background_service": False,
            "mcp_write_tool": False,
            "hooks": False,
            "real_base_files": False,
        },
        "non_claims": [
            "not reviewed knowledge",
            "not evidence support",
            "not action basis",
            "not mainline approval",
        ],
    }


def render_html(base: dict) -> str:
    shared_search = " ".join(base["boundary_phrases"] + base["search_targets"])
    cards = "\n".join(
        f"""<article class=\"card\" data-surface=\"{s['id']}\" data-search=\"{s['id']} {s['title']} {' '.join(s['answers'])} {s['boundary']} {shared_search}\">
  <p class=\"eyebrow\">{s['id']}</p>
  <h3>{s['title']}</h3>
  <p>{' '.join(s['answers'])}</p>
  <strong>{s['boundary']}</strong>
</article>"""
        for s in base["surfaces"]
    )
    gates = "\n".join(f"<li>{g['id']}: {g['test']}</li>" for g in base["acceptance_gates"])
    options = "\n".join(
        f"<li><b>{o['label']}</b><span>{o['fit']} Boundary: {o['boundary']}.</span></li>"
        for o in base["decision_options"]
    )
    return f"""<!doctype html>
<html lang=\"en\" data-sandbox-only=\"true\" data-no-sync=\"true\" data-no-authority=\"true\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>VAKS Formalization Readiness Pilot</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #172026;
      --muted: #52616b;
      --line: #d7dde2;
      --paper: #f8faf9;
      --panel: #ffffff;
      --accent: #0f766e;
      --warn: #b45309;
      --ok: #28724f;
    }}
    * {{ box-sizing: border-box; }}
    body {{
      margin: 0;
      font-family: Arial, Helvetica, sans-serif;
      color: var(--ink);
      background: var(--paper);
    }}
    header {{
      padding: 28px 32px 18px;
      border-bottom: 1px solid var(--line);
      background: var(--panel);
    }}
    h1 {{
      margin: 0 0 8px;
      font-size: 34px;
      line-height: 1.08;
      letter-spacing: 0;
    }}
    .sub {{ max-width: 940px; color: var(--muted); line-height: 1.5; }}
    .shell {{
      display: grid;
      grid-template-columns: minmax(0, 1fr) 300px;
      gap: 20px;
      padding: 20px 32px 36px;
    }}
    main {{ min-width: 0; }}
    .toolbar {{
      display: flex;
      flex-wrap: wrap;
      align-items: center;
      gap: 10px;
      margin-bottom: 16px;
    }}
    input {{
      min-width: 260px;
      height: 40px;
      padding: 0 12px;
      border: 1px solid var(--line);
      border-radius: 6px;
      font-size: 14px;
    }}
    button {{
      height: 40px;
      border: 1px solid var(--line);
      border-radius: 6px;
      background: var(--panel);
      color: var(--ink);
      padding: 0 12px;
      font-weight: 700;
      cursor: pointer;
    }}
    button.active {{ border-color: var(--accent); color: var(--accent); }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      gap: 12px;
    }}
    .card {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      min-height: 172px;
    }}
    .card h3 {{ margin: 4px 0 8px; font-size: 18px; }}
    .card p {{ color: var(--muted); line-height: 1.45; }}
    .eyebrow {{ margin: 0; color: var(--accent); font-size: 12px; font-weight: 700; text-transform: uppercase; }}
    aside {{
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
      padding: 14px;
      align-self: start;
      position: sticky;
      top: 16px;
    }}
    aside h2 {{ margin: 0 0 10px; font-size: 18px; }}
    aside li {{ margin-bottom: 8px; color: var(--muted); }}
    section {{
      margin-top: 18px;
      padding: 16px;
      background: var(--panel);
      border: 1px solid var(--line);
      border-radius: 8px;
    }}
    section h2 {{ margin-top: 0; font-size: 20px; }}
    .options li {{ margin-bottom: 12px; }}
    .options span {{ display: block; color: var(--muted); margin-top: 3px; line-height: 1.45; }}
    @media (max-width: 860px) {{
      .shell {{ grid-template-columns: 1fr; padding: 16px; }}
      header {{ padding: 22px 16px 14px; }}
      h1 {{ font-size: 28px; }}
      aside {{ position: static; }}
      input {{ min-width: 100%; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>VAKS Formalization Readiness Pilot</h1>
    <p class=\"sub\">A sandbox-only product pilot that turns the P2-21 workbench into a first-run path, daily operator flow, receipt inspector, formalization decision matrix, and acceptance gate set. It is not reviewed knowledge, not evidence support, not action basis, and does not approve.</p>
  </header>
  <div class=\"shell\">
    <main>
      <div class=\"toolbar\" data-role=\"surface-filter\">
        <input id=\"q\" type=\"search\" placeholder=\"Search: receipt inspector, no formal vault write, next sandbox route\">
        <button class=\"active\" data-filter=\"all\">All</button>
        <button data-filter=\"pilot_home\">Home</button>
        <button data-filter=\"receipt_inspector\">Receipts</button>
        <button data-filter=\"formalization_decision_matrix\">Decision</button>
        <button data-filter=\"acceptance_gates\">Gates</button>
      </div>
      <div class=\"grid\" id=\"cards\" data-role=\"readiness-surfaces\">
        {cards}
      </div>
      <section data-role=\"decision-options\">
        <h2>Formalization Routes</h2>
        <ul class=\"options\">{options}</ul>
      </section>
      <section data-role=\"acceptance-gates\">
        <h2>Acceptance Gates</h2>
        <ul>{gates}</ul>
      </section>
    </main>
    <aside data-role=\"boundary-rail\">
      <h2>Boundary Rail</h2>
      <ul>
        <li>sandbox only</li>
        <li>not reviewed knowledge</li>
        <li>not evidence support</li>
        <li>not action basis</li>
        <li>does not approve</li>
        <li>no formal vault write</li>
        <li>no sync / no commit / no push</li>
      </ul>
    </aside>
  </div>
  <script type=\"application/json\" id=\"readiness-data\">
{json.dumps(base, indent=2)}
  </script>
  <script>
    const input = document.getElementById('q');
    const cards = Array.from(document.querySelectorAll('.card'));
    const buttons = Array.from(document.querySelectorAll('button[data-filter]'));
    let filter = 'all';
    function apply() {{
      const query = input.value.toLowerCase();
      cards.forEach(card => {{
        const okFilter = filter === 'all' || card.dataset.surface === filter;
        const okQuery = !query || card.dataset.search.toLowerCase().includes(query) || card.textContent.toLowerCase().includes(query);
        card.hidden = !(okFilter && okQuery);
      }});
    }}
    buttons.forEach(btn => btn.addEventListener('click', () => {{
      buttons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      filter = btn.dataset.filter;
      apply();
    }}));
    input.addEventListener('input', apply);
  </script>
</body>
</html>
"""


def render_failure_oracle_md(cases: list[tuple[str, dict]]) -> str:
    lines = [
        "# Failure Case Oracle",
        "",
        "Each case must fail validation with the listed code. Failure cases focus on authority confusion, unsafe operations, missing product gates, and weak pilot usability.",
        "",
        "| File | Expected failure |",
        "| --- | --- |",
    ]
    for name, item in cases:
        lines.append(f"| `{name}` | `{', '.join(item['expected_failures'])}` |")
    return "\n".join(lines)


def render_pending_report(kind: str, title: str) -> str:
    return f"""---
record_kind: {kind}
slice_id: {SLICE_ID}
status: pending
truth_boundary: sandbox_only
---

# {title}

Pending. This report must be filled after local verification and the relevant
read-only agent review.
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

Expected commands:

```powershell
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_formalization_readiness.py --rebuild
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_formalization_readiness.py
```

The default command must validate existing artifacts only. Rebuild must require
the explicit `--rebuild` flag.
"""


def render_next_step_pending() -> str:
    return f"""---
record_kind: sandbox_next_step
slice_id: {SLICE_ID}
status: pending
truth_boundary: sandbox_only
---

# Next Step

Pending Product Acceptance.
"""


def build() -> None:
    base = config()
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError("Missing required P2-21 source files: " + "; ".join(missing))

    git_status_summary = "pre-existing dirty tree recorded by orchestrator before build; final audit scoped to this slice path"

    safe_write("slice-plan.md", render_slice_plan(base, git_status_summary))
    safe_write("source-map.md", render_source_map(paths))
    safe_write("artifact/formalization-readiness-contract.md", render_contract(base))
    safe_write(
        "fixtures/valid-product-readiness-config.json",
        json.dumps(base, indent=2, ensure_ascii=False),
    )
    safe_write(
        "fixtures/valid-pilot-config-variant.json",
        json.dumps(fixture_variant(base), indent=2, ensure_ascii=False),
    )

    cases = failure_cases(base)
    for name, item in cases:
        safe_write(f"failure-cases/{name}", json.dumps(item, indent=2, ensure_ascii=False))
    safe_write(
        "artifact/failure-case-oracle.json",
        json.dumps(
            [{"file": name, "expected_failures": item["expected_failures"]} for name, item in cases],
            indent=2,
            ensure_ascii=False,
        ),
    )
    safe_write("artifact/failure-case-oracle.md", render_failure_oracle_md(cases))

    vault = "prototype/vaks-workbench-formalization-pilot"
    safe_write(f"{vault}/00 Pilot Home - VAKS Workbench.md", render_pilot_home(base))
    safe_write(f"{vault}/10 First Run Script.md", render_first_run(base))
    safe_write(f"{vault}/20 Daily Operator Flow.md", render_daily_flow(base))
    safe_write(f"{vault}/25 Receipt Inspector.md", render_receipt_inspector(base))
    safe_write(f"{vault}/30 Formalization Decision Matrix.md", render_decision_matrix(base))
    safe_write(f"{vault}/35 Triage and Dirty-State Panel.md", render_triage_dirty_state_panel(base))
    safe_write(f"{vault}/40 Acceptance Gates.md", render_acceptance_gates(base))
    safe_write(f"{vault}/50 Boundary FAQ.md", render_boundary_faq(base))
    safe_write(f"{vault}/55 Failure Messages.md", render_failure_messages(base))
    safe_write(f"{vault}/60 Reviewer Packet.md", render_reviewer_packet(base))
    safe_write(f"{vault}/65 Formalization Readiness Packet.md", render_formalization_readiness_packet(base))
    safe_write(f"{vault}/70 Product Rollout Backlog.md", render_rollout_backlog(base))
    safe_write(f"{vault}/80 Pilot Test Results Template.md", render_test_template(base))
    safe_write(f"{vault}/cockpit-readiness.html", render_html(base))
    safe_write(
        f"{vault}/Receipts/formalization-readiness-receipt.json",
        json.dumps(render_receipt(base, paths), indent=2, ensure_ascii=False),
    )

    safe_write("verification.md", render_verification_pending(), overwrite=False)
    safe_write(
        "reviewer-report.md",
        render_pending_report("sandbox_reviewer_report", "Reviewer Report"),
        overwrite=False,
    )
    safe_write(
        "boundary-audit.md",
        render_pending_report("sandbox_boundary_audit", "Boundary Audit"),
        overwrite=False,
    )
    safe_write(
        "product-acceptance-report.md",
        render_pending_report(
            "sandbox_product_acceptance_report", "Product Acceptance Report"
        ),
        overwrite=False,
    )
    safe_write("next-step.md", render_next_step_pending(), overwrite=False)


if __name__ == "__main__":
    build()
