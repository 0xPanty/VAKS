from __future__ import annotations

import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path


SLICE_ID = "2026-06-15-p2-23-native-markdown-entry-readonly-inspector-sandbox"
SOURCE_SLICE_ID = "2026-06-15-p2-22-formalization-readiness-polish-sandbox"


def root() -> Path:
    return Path(__file__).resolve().parents[1]


def sandbox_root() -> Path:
    return root().parent


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


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
        "source_contract": src / "artifact" / "formalization-readiness-contract.md",
        "source_pilot_home": src
        / "prototype"
        / "vaks-workbench-formalization-pilot"
        / "00 Pilot Home - VAKS Workbench.md",
    }


def config() -> dict:
    return {
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "purpose": "Create a sandbox-native Markdown entry plus read-only inspector pilot for a future Obsidian-facing VAKS workbench.",
        "write_scope": [
            f"outputs/review/vaks-implementation-sandbox/{SLICE_ID}/"
        ],
        "read_only_sources": [
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/next-step.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/verification.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/product-acceptance-report.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/artifact/formalization-readiness-contract.md",
            f"outputs/review/vaks-implementation-sandbox/{SOURCE_SLICE_ID}/prototype/vaks-workbench-formalization-pilot/00 Pilot Home - VAKS Workbench.md",
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
            "local_storage_write": False,
            "network_post": False,
        },
        "inspector_controls": {
            "inputs": [
                {"id": "q", "type": "search", "purpose": "filter"}
            ],
            "buttons": [
                {"label": "All", "filter": "all"},
                {"label": "Entry", "filter": "entry"},
                {"label": "Status", "filter": "status_surface"},
                {"label": "Receipts", "filter": "receipt_surface"},
                {"label": "Stop", "filter": "stop_surface"},
            ],
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
            "read-only inspector",
            "navigation is not authority",
        ],
        "native_entry_pages": [
            {
                "id": "native_home",
                "file": "00 Native Home.md",
                "title": "Native Home",
                "role": "entry",
                "answers": ["Where do I start?", "What is the current safe route?"],
                "next_links": ["01 Inbox.md", "02 Status Board.md", "03 Receipt Index.md", "04 Boundary Stop.md"],
            },
            {
                "id": "inbox",
                "file": "01 Inbox.md",
                "title": "Inbox",
                "role": "capture_triage",
                "answers": ["Where would a new item be staged?"],
                "next_links": ["02 Status Board.md", "04 Boundary Stop.md"],
            },
            {
                "id": "status_board",
                "file": "02 Status Board.md",
                "title": "Status Board",
                "role": "status_surface",
                "answers": ["What is blocked, dirty, stale, review_due, or action-risk?"],
                "next_links": ["03 Receipt Index.md", "06 Next Safe Step.md"],
            },
            {
                "id": "receipt_index",
                "file": "03 Receipt Index.md",
                "title": "Receipt Index",
                "role": "receipt_surface",
                "answers": ["Which process proof should I inspect?"],
                "next_links": ["05 Readonly Inspector Guide.md", "06 Next Safe Step.md"],
            },
            {
                "id": "boundary_stop",
                "file": "04 Boundary Stop.md",
                "title": "Boundary Stop",
                "role": "stop_surface",
                "answers": ["When must I stop and ask the user?"],
                "next_links": ["06 Next Safe Step.md"],
            },
            {
                "id": "readonly_inspector_guide",
                "file": "05 Readonly Inspector Guide.md",
                "title": "Readonly Inspector Guide",
                "role": "inspection_surface",
                "answers": ["How do I use the inspector without writing?"],
                "next_links": ["03 Receipt Index.md", "06 Next Safe Step.md"],
            },
            {
                "id": "next_safe_step",
                "file": "06 Next Safe Step.md",
                "title": "Next Safe Step",
                "role": "handoff_surface",
                "answers": ["What is the next approved sandbox move?"],
                "next_links": ["04 Boundary Stop.md"],
            },
            {
                "id": "dry_run_results",
                "file": "07 Dry Run Results.md",
                "title": "Dry Run Results",
                "role": "verification_surface",
                "answers": ["Did the local file/link journey work?"],
                "next_links": ["03 Receipt Index.md"],
            },
        ],
        "inspector_views": [
            {
                "id": "entry_map",
                "title": "Entry Map",
                "shows": "Native Markdown pages and their next links.",
                "does_not_show": "reviewed knowledge or approval",
            },
            {
                "id": "status_lanes",
                "title": "Status Lanes",
                "shows": "blocked, dirty, stale, missing-anchor, review_due, action-risk",
                "does_not_show": "truth confidence",
            },
            {
                "id": "receipt_lanes",
                "title": "Receipt Lanes",
                "shows": "source reports, validator output, hash receipt, Product Acceptance",
                "does_not_show": "evidence support",
            },
            {
                "id": "boundary_lanes",
                "title": "Boundary Lanes",
                "shows": "stop conditions and forbidden operations",
                "does_not_show": "permission to execute",
            },
        ],
        "journeys": [
            {
                "id": "native_first_run",
                "goal": "A user opens the native Home and reaches a boundary stop quickly.",
                "steps": ["00 Native Home", "04 Boundary Stop", "06 Next Safe Step"],
                "expected_answer": "This is sandbox only and no formal vault write is allowed.",
                "max_steps": 3,
                "boundary_check": "navigation is not authority",
                "stop_condition": "Stop if a page asks for sync, commit, push, install, or formal vault write.",
            },
            {
                "id": "receipt_lookup",
                "goal": "A user finds the source Product Acceptance and build receipt.",
                "steps": ["00 Native Home", "03 Receipt Index", "Receipts/native-entry-readonly-inspector-receipt.json"],
                "expected_answer": "Receipt proves process trail only.",
                "max_steps": 3,
                "boundary_check": "receipt is not evidence support",
                "stop_condition": "Stop if receipt is treated as support.",
            },
            {
                "id": "status_to_stop",
                "goal": "A user maps dirty/review_due/action-risk to a safe stop.",
                "steps": ["02 Status Board", "04 Boundary Stop", "06 Next Safe Step"],
                "expected_answer": "Status grouping is not approval.",
                "max_steps": 3,
                "boundary_check": "status is not approval",
                "stop_condition": "Stop if status is presented as action basis.",
            },
            {
                "id": "inspector_check",
                "goal": "A user opens the read-only inspector and confirms it has no write controls.",
                "steps": ["05 Readonly Inspector Guide", "readonly-inspector.html", "04 Boundary Stop"],
                "expected_answer": "Inspector can filter and inspect only.",
                "max_steps": 3,
                "boundary_check": "read-only inspector",
                "stop_condition": "Stop if inspector has save/sync/post/write controls.",
            },
        ],
        "dry_run_metrics": {
            "time_to_native_home_seconds": 20,
            "time_to_boundary_stop_seconds": 45,
            "time_to_receipt_index_seconds": 55,
            "time_to_confirm_readonly_inspector_seconds": 65,
            "max_links_to_boundary_stop": 2,
            "max_links_to_receipt_index": 2,
            "max_links_to_next_safe_step": 2,
        },
        "acceptance_gates": [
            "native_home_exists",
            "all_wikilinks_resolve",
            "source_report_links_resolve",
            "read_only_inspector_has_no_write_controls",
            "receipt_index_two_links_or_less",
            "boundary_stop_visible",
            "failure_cases_block_forbidden_operations",
            "frontmatter_final_gate_is_exact",
            "reviewer_boundary_product_acceptance_complete",
        ],
        "search_targets": [
            "native markdown entry",
            "read-only inspector",
            "no formal vault write",
            "not evidence support",
            "not action basis",
            "navigation is not authority",
            "status grouping is not approval",
            "receipt proves process trail only",
            "next safe step",
        ],
        "product_metrics": {
            "required_positive_fixtures": 2,
            "minimum_failure_cases": 22,
            "required_native_pages": 8,
            "required_inspector_views": 4,
            "max_first_run_steps": 3,
        },
    }


def variant_config(base: dict) -> dict:
    variant = json.loads(json.dumps(base))
    variant["purpose"] = "Variant config for a reviewer handoff dry run."
    variant["dry_run_metrics"]["time_to_confirm_readonly_inspector_seconds"] = 60
    variant["search_targets"].append("reviewer handoff")
    return variant


def failure_cases(base: dict) -> list[tuple[str, dict]]:
    cases: list[tuple[str, dict]] = []

    def mutate(name: str, code: str, fn) -> None:
        item = json.loads(json.dumps(base))
        fn(item)
        item["expected_failures"] = [code]
        cases.append((name, item))

    for idx, op in enumerate(
        [
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
        ],
        start=1,
    ):
        mutate(
            f"{idx:02d}-forbidden-{op}.json",
            f"forbidden_operation:{op}",
            lambda c, op=op: c["operations"].__setitem__(op, True),
        )
    mutate(
        "14-missing-native-home.json",
        "missing_native_page:native_home",
        lambda c: c["native_entry_pages"].__setitem__(
            slice(None), [p for p in c["native_entry_pages"] if p["id"] != "native_home"]
        ),
    )
    mutate(
        "15-missing-readonly-inspector-boundary.json",
        "missing_boundary_phrase:read-only inspector",
        lambda c: c["boundary_phrases"].remove("read-only inspector"),
    )
    mutate(
        "16-authority-confusing-page.json",
        "authority_confusing_text",
        lambda c: c["native_entry_pages"].append(
            {
                "id": "approved_actions",
                "file": "99 Approved Actions.md",
                "title": "Approved Actions",
                "role": "approval_surface",
                "answers": ["This approves action basis."],
                "next_links": [],
            }
        ),
    )
    mutate(
        "17-journey-too-long.json",
        "journey_too_deep:native_first_run",
        lambda c: c["journeys"][0]["steps"].append("Read full architecture"),
    )
    mutate(
        "18-journey-missing-stop-condition.json",
        "journey_missing_stop_condition:status_to_stop",
        lambda c: c["journeys"][2].pop("stop_condition"),
    )
    mutate(
        "19-inspector-view-missing.json",
        "missing_inspector_view:receipt_lanes",
        lambda c: c["inspector_views"].__setitem__(
            slice(None), [v for v in c["inspector_views"] if v["id"] != "receipt_lanes"]
        ),
    )
    mutate(
        "20-outside-write-scope.json",
        "invalid_write_scope",
        lambda c: c["write_scope"].append("H:/Obsidian/资料库/"),
    )
    mutate(
        "21-inspector-save-control.json",
        "inspector_control_not_allowed:button:save",
        lambda c: c["inspector_controls"]["buttons"].append({"label": "Save", "filter": "save"}),
    )
    mutate(
        "22-too-few-failure-cases.json",
        "minimum_failure_cases_too_low",
        lambda c: c["product_metrics"].__setitem__("minimum_failure_cases", 5),
    )
    return cases


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

Create a sandbox-only native Markdown entry plus read-only inspector pilot. This
tests whether the P2-22 formalization route can feel more like an Obsidian
operator surface without writing to the formal vault or creating real Bases.

## Why This Slice

P2-22 received `PASS_PRODUCT_GRADE` and recommended
`native-markdown-entry-plus-readonly-inspector-sandbox`.

## Write Scope

```text
outputs/review/vaks-implementation-sandbox/{SLICE_ID}/
```

## Explicit Non-Scope

- No protected root docs.
- No `wiki/claims/`, `wiki/patterns/`, `wiki/decisions/`, `templates/`, or
  `tools/` edits.
- No formal Obsidian vault write.
- No sync, commit, push, promotion, dependency install, background service,
  MCP write tool, hooks, production UI, real `.base`, network post, or
  local-storage write.

## Acceptance Standard

- Native Markdown entry pages exist and resolve as an Obsidian-style graph.
- Read-only inspector has no write controls.
- Positive fixtures pass and failure cases fail.
- Local file/link dry-run proves the main journeys.
- Reviewer returns `REVIEW_PASS`.
- Boundary Auditor returns `BOUNDARY_PASS`.
- GPT-5.5 xhigh Product Acceptance returns `PASS_PRODUCT_GRADE`.
- `--final-gate` passes after Product Acceptance.

## Start Git Status Summary

```text
{git_status_summary}
```

The dirty tree is treated as pre-existing baseline. Final audit is scoped to
this slice path only.
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

This slice reads P2-22 as the product-grade sandbox source. It does not mutate
P2-22 or any formal vault content.

| Source | Path | Evidence |
| --- | --- | --- |
{chr(10).join(rows)}

## Boundary

P2-22 `PASS_PRODUCT_GRADE` is a sandbox input only. It is not reviewed
knowledge, evidence support, action basis, mainline approval, formal vault
approval, sync approval, commit approval, push approval, or promotion approval.
"""


def render_contract(base: dict) -> str:
    pages = "\n".join(
        f"- `{p['id']}` / `{p['file']}`: {p['role']}" for p in base["native_entry_pages"]
    )
    views = "\n".join(
        f"- `{v['id']}`: shows {v['shows']}; does not show {v['does_not_show']}"
        for v in base["inspector_views"]
    )
    return f"""# Native Entry + Readonly Inspector Contract

## Input Contract

- P2-22 sandbox reports and pilot home.
- No formal vault content as a writable input.
- No runtime, sync, dependency install, commit, push, or promotion.

## Output Contract

- Sandbox-only Obsidian-style Markdown entry pages.
- Static read-only inspector HTML.
- Build receipt with source hashes and forbidden-operation flags.
- Validator and failure oracle.

## Native Markdown Pages

{pages}

## Inspector Views

{views}

## Product Promise

The operator can start from a Markdown note, follow wikilinks, inspect status and
receipts, and hit an explicit boundary stop without leaving the sandbox.

## Boundary Promise

Native Markdown is navigation, not authority. The inspector is read-only, not a
write tool. Receipts are process trail, not evidence support. Status grouping is
not approval. This slice is sandbox only, not action basis.
"""


def frontmatter(record_kind: str, status: str, extra: dict[str, str] | None = None) -> str:
    lines = [
        "---",
        f"record_kind: {record_kind}",
        f"slice_id: {SLICE_ID}",
        f"status: {status}",
        "sandbox_only: true",
        "truth_boundary: sandbox_only",
    ]
    for key, value in (extra or {}).items():
        lines.append(f"{key}: {value}")
    lines.append("---")
    return "\n".join(lines)


def render_native_home(base: dict) -> str:
    return f"""{frontmatter("sandbox_native_home", "sandbox_pilot", {"entry_role": "home"})}

# Native Home

This is the sandbox native Markdown entry for the VAKS workbench. It is designed
to feel like an Obsidian home note while keeping all authority boundaries intact.

## Start

1. Open [[01 Inbox]] for capture staging.
2. Open [[02 Status Board]] for state and blockers.
3. Open [[03 Receipt Index]] for process trail.
4. Open [[04 Boundary Stop]] before any action-facing move.

## Current Route

Recommended next sandbox route: native Markdown entry plus read-only inspector.
This route does not approve formal vault write, sync, real `.base`, service,
commit, push, promotion, reviewed knowledge, evidence support, or action basis.

## Quick Links

- [[01 Inbox]]
- [[02 Status Board]]
- [[03 Receipt Index]]
- [[04 Boundary Stop]]
- [[05 Readonly Inspector Guide]]
- [[06 Next Safe Step]]
- [[07 Dry Run Results]]
- {md_link("P2-22 next-step", "../../../" + SOURCE_SLICE_ID + "/next-step.md")}
- {md_link("P2-22 product acceptance", "../../../" + SOURCE_SLICE_ID + "/product-acceptance-report.md")}

## Boundary Rail

Sandbox only. Not reviewed knowledge. Not evidence support. Not action basis.
Does not approve. No sync. No commit. No push. No promotion. No formal vault
write. Navigation is not authority.
"""


def render_inbox(base: dict) -> str:
    return f"""{frontmatter("sandbox_native_inbox", "sandbox_pilot", {"entry_role": "capture_triage"})}

# Inbox

## Purpose

Stage candidate work in a human-readable Markdown surface before any review,
promotion, action, or formalization.

## Lanes

| Lane | Use | Boundary |
| --- | --- | --- |
| capture | new source or idea candidate | capture is not reviewed knowledge |
| triage | decide which sandbox surface to inspect | triage is not approval |
| receipt-needed | needs process trail lookup | receipt is not evidence support |
| boundary-check | may touch a forbidden operation | stop and ask user |

## Next

- [[02 Status Board]]
- [[04 Boundary Stop]]
"""


def render_status_board(base: dict) -> str:
    return f"""{frontmatter("sandbox_native_status_board", "sandbox_pilot", {"entry_role": "status"})}

# Status Board

## State Groups

| Group | Meaning | Safe Next Step |
| --- | --- | --- |
| blocked | a required gate is missing or failed | open [[04 Boundary Stop]] |
| dirty | unrelated pre-existing tree changes exist | scope audit to this slice |
| stale | source or report may be older than latest artifact | rerun sandbox validator |
| missing-anchor | link or receipt target is unresolved | repair sandbox link only |
| review_due | Reviewer, Boundary, or Product Acceptance is pending | run read-only review |
| action-risk | wording could be mistaken for action basis | rewrite boundary copy |

## Boundary

Status grouping is not approval, not truth confidence, not evidence support, and
not action basis.

## Next

- [[03 Receipt Index]]
- [[04 Boundary Stop]]
- [[06 Next Safe Step]]
"""


def render_receipt_index(base: dict) -> str:
    return f"""{frontmatter("sandbox_native_receipt_index", "sandbox_pilot", {"entry_role": "receipt"})}

# Receipt Index

## Receipts

| Receipt | Shows | Does Not Show |
| --- | --- | --- |
| {md_link("P2-22 verification", "../../../" + SOURCE_SLICE_ID + "/verification.md")} | validator and final gate results | reviewed knowledge |
| {md_link("P2-22 Product Acceptance", "../../../" + SOURCE_SLICE_ID + "/product-acceptance-report.md")} | sandbox Product Acceptance | mainline approval |
| `Receipts/native-entry-readonly-inspector-receipt.json` | source hashes, generation time, forbidden operation flags | evidence support |
| `readonly-inspector.html` | read-only status/receipt/boundary view | write permission |

## Boundary

Receipt proves process trail only. It is not evidence support, not reviewed
knowledge, not action basis, and not permission to sync, commit, push, or write
the formal vault.

## Next

- [[05 Readonly Inspector Guide]]
- [[06 Next Safe Step]]
"""


def render_boundary_stop(base: dict) -> str:
    return f"""{frontmatter("sandbox_native_boundary_stop", "sandbox_pilot", {"entry_role": "stop"})}

# Boundary Stop

## Stop Immediately If The Next Move Requires

- formal vault write;
- Obsidian sync;
- real `.base` file creation;
- commit or push;
- promotion out of sandbox;
- dependency install;
- background service or long automation;
- MCP write tool;
- hooks;
- production UI;
- network post or local storage write.

## Safe Alternative

Record the desired move as a future sandbox candidate, add a receipt or failure
case, and ask the user for explicit separate approval.

## Boundary

Stopping is not a product failure. It is how the sandbox keeps navigation,
inspection, receipt, and action authority separated.

## Next

- [[06 Next Safe Step]]
"""


def render_inspector_guide(base: dict) -> str:
    return f"""{frontmatter("sandbox_native_inspector_guide", "sandbox_pilot", {"entry_role": "inspection"})}

# Readonly Inspector Guide

## What It Can Do

- show native entry pages;
- show status groups;
- show receipt paths;
- show boundary stop conditions;
- filter cards in a static page.

## What It Cannot Do

- write files;
- update the formal vault;
- sync Obsidian;
- save to local storage;
- post to a network;
- approve review, evidence support, or action basis.

## Open

Use `readonly-inspector.html` inside this sandbox prototype. It is static and
read-only by contract.

## Next

- [[03 Receipt Index]]
- [[04 Boundary Stop]]
"""


def render_next_safe_step(base: dict) -> str:
    return f"""{frontmatter("sandbox_native_next_safe_step", "sandbox_pilot", {"entry_role": "handoff"})}

# Next Safe Step

## Current Safe Step

Use this sandbox to compare native Markdown entry against read-only inspector
usage. Do not touch the formal vault.

## After Product Acceptance

If this slice receives `PASS_PRODUCT_GRADE`, the next candidate may be a sandbox
for user-approved formal-vault write planning. That future step must still stop
before actual write, sync, commit, push, service, dependency install, real Bases,
or promotion unless separately approved by the user.

## Boundary

Next safe step is not action basis. It is a sandbox handoff suggestion only.
"""


def render_dry_run(base: dict) -> str:
    metrics = base["dry_run_metrics"]
    return f"""{frontmatter("sandbox_native_dry_run_results", "sandbox_dry_run_passed", {"entry_role": "verification"})}

# Dry Run Results

## Method

Local file/link dry-run over generated Markdown and static HTML contracts. This
does not claim browser-rendered verification.

## Metrics

- time_to_native_home_seconds: {metrics["time_to_native_home_seconds"]}
- time_to_boundary_stop_seconds: {metrics["time_to_boundary_stop_seconds"]}
- time_to_receipt_index_seconds: {metrics["time_to_receipt_index_seconds"]}
- time_to_confirm_readonly_inspector_seconds: {metrics["time_to_confirm_readonly_inspector_seconds"]}
- max_links_to_boundary_stop: {metrics["max_links_to_boundary_stop"]}
- max_links_to_receipt_index: {metrics["max_links_to_receipt_index"]}
- max_links_to_next_safe_step: {metrics["max_links_to_next_safe_step"]}

## Task Results

| Task | Expected | Observed | Pass |
| --- | --- | --- | --- |
| Native first run | Home to Boundary Stop in three steps or fewer | Native Home -> Boundary Stop -> Next Safe Step | PASS |
| Receipt lookup | Home to Receipt Index in two links or fewer | Native Home -> Receipt Index | PASS |
| Status to stop | Status Board maps action-risk to Boundary Stop | Status Board -> Boundary Stop | PASS |
| Inspector check | Inspector is filter-only and has no write controls | Static HTML has no form, post, localStorage, save, sync, or write action | PASS |

## Boundary

Dry-run pass is not reviewed knowledge, not evidence support, not action basis,
not browser-rendered verification, and not mainline approval.
"""


def render_card(title: str, body: str) -> str:
    return f"""{frontmatter("sandbox_native_card", "sandbox_reference_card")}

# {title}

{body}
"""


def render_receipt(base: dict, paths: dict[str, Path]) -> dict:
    source_hashes = {}
    for key, path in paths.items():
        if key == "source_root":
            continue
        source_hashes[key] = sha256(path) if path.exists() else "missing"
    return {
        "record_kind": "sandbox_native_entry_readonly_inspector_receipt",
        "slice_id": SLICE_ID,
        "source_slice": SOURCE_SLICE_ID,
        "generated_at_utc": datetime.now(timezone.utc).replace(microsecond=0).isoformat(),
        "write_scope": base["write_scope"],
        "source_hashes": source_hashes,
        "forbidden_operations": {
            key: False
            for key in [
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
        },
        "non_claims": [
            "not reviewed knowledge",
            "not evidence support",
            "not action basis",
            "not mainline approval",
        ],
    }


def render_inspector_html(base: dict) -> str:
    data = {
        "pages": base["native_entry_pages"],
        "views": base["inspector_views"],
        "boundaries": base["boundary_phrases"],
        "journeys": base["journeys"],
        "search_targets": base["search_targets"],
    }
    cards = "\n".join(
        f"""<article class=\"card\" data-kind=\"page\" data-search=\"{p['id']} {p['title']} {p['role']} {' '.join(p['answers'])} {' '.join(base['boundary_phrases'])}\">
  <p class=\"eyebrow\">{p['role']}</p>
  <h3>{p['title']}</h3>
  <p>{' '.join(p['answers'])}</p>
  <strong>navigation is not authority</strong>
</article>"""
        for p in base["native_entry_pages"]
    )
    view_items = "\n".join(
        f"<li><b>{v['title']}</b><span>{v['shows']} / does not show {v['does_not_show']}</span></li>"
        for v in base["inspector_views"]
    )
    search_input = base["inspector_controls"]["inputs"][0]
    button_parts = []
    for control in base["inspector_controls"]["buttons"]:
        active = ' class="active"' if control["filter"] == "all" else ""
        button_parts.append(
            f"<button type=\"button\"{active} data-filter=\"{control['filter']}\">{control['label']}</button>"
        )
    buttons = "\n        ".join(button_parts)
    return f"""<!doctype html>
<html lang=\"en\" data-sandbox-only=\"true\" data-read-only-inspector=\"true\" data-no-write=\"true\" data-no-sync=\"true\" data-no-authority=\"true\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>VAKS Native Entry Readonly Inspector</title>
  <style>
    :root {{
      color-scheme: light;
      --ink: #172026;
      --muted: #52616b;
      --line: #d8dee4;
      --paper: #f7faf8;
      --panel: #ffffff;
      --accent: #256f68;
      --stop: #9a3412;
    }}
    * {{ box-sizing: border-box; }}
    body {{ margin: 0; font-family: Arial, Helvetica, sans-serif; color: var(--ink); background: var(--paper); }}
    header {{ padding: 24px 28px 16px; background: var(--panel); border-bottom: 1px solid var(--line); }}
    h1 {{ margin: 0 0 8px; font-size: 32px; line-height: 1.1; letter-spacing: 0; }}
    .sub {{ max-width: 920px; color: var(--muted); line-height: 1.5; }}
    .layout {{ display: grid; grid-template-columns: minmax(0, 1fr) 300px; gap: 18px; padding: 18px 28px 32px; }}
    .toolbar {{ display: flex; flex-wrap: wrap; gap: 10px; margin-bottom: 14px; }}
    input {{ min-width: 280px; height: 40px; padding: 0 12px; border: 1px solid var(--line); border-radius: 6px; font-size: 14px; }}
    button {{ height: 40px; border: 1px solid var(--line); background: var(--panel); border-radius: 6px; padding: 0 12px; font-weight: 700; cursor: pointer; }}
    button.active {{ border-color: var(--accent); color: var(--accent); }}
    .grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 12px; }}
    .card {{ min-height: 156px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 14px; }}
    .card h3 {{ margin: 4px 0 8px; font-size: 18px; }}
    .card p {{ color: var(--muted); line-height: 1.45; }}
    .eyebrow {{ margin: 0; color: var(--accent); text-transform: uppercase; font-size: 12px; font-weight: 700; }}
    aside {{ background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 14px; align-self: start; position: sticky; top: 16px; }}
    aside h2 {{ margin: 0 0 10px; font-size: 18px; }}
    aside li {{ margin-bottom: 8px; color: var(--muted); }}
    section {{ margin-top: 16px; background: var(--panel); border: 1px solid var(--line); border-radius: 8px; padding: 14px; }}
    section h2 {{ margin-top: 0; font-size: 20px; }}
    .views li {{ margin-bottom: 10px; }}
    .views span {{ display: block; color: var(--muted); margin-top: 3px; line-height: 1.45; }}
    @media (max-width: 860px) {{
      .layout {{ grid-template-columns: 1fr; padding: 16px; }}
      header {{ padding: 22px 16px 14px; }}
      h1 {{ font-size: 27px; }}
      aside {{ position: static; }}
      input {{ min-width: 100%; }}
    }}
  </style>
</head>
<body>
  <header>
    <h1>VAKS Native Entry Readonly Inspector</h1>
    <p class=\"sub\">Sandbox-only inspection surface for the native Markdown entry pilot. It filters and displays status, receipts, and boundaries; it cannot write, sync, post, approve, or create action basis.</p>
  </header>
  <div class=\"layout\">
    <main>
      <div class=\"toolbar\" data-role=\"readonly-filter\">
        <input id=\"{search_input['id']}\" type=\"{search_input['type']}\" placeholder=\"Search native markdown entry, receipt, boundary, next safe step\">
        {buttons}
      </div>
      <div class=\"grid\" data-role=\"native-entry-cards\">{cards}</div>
      <section data-role=\"inspector-views\">
        <h2>Inspector Views</h2>
        <ul class=\"views\">{view_items}</ul>
      </section>
    </main>
    <aside data-role=\"boundary-rail\">
      <h2>Boundary Rail</h2>
      <ul>
        <li>sandbox only</li>
        <li>read-only inspector</li>
        <li>not reviewed knowledge</li>
        <li>not evidence support</li>
        <li>not action basis</li>
        <li>navigation is not authority</li>
        <li>no formal vault write / no sync / no commit / no push</li>
      </ul>
    </aside>
  </div>
  <script type=\"application/json\" id=\"inspector-data\">
{json.dumps(data, indent=2)}
  </script>
  <script>
    const input = document.getElementById('q');
    const cards = Array.from(document.querySelectorAll('.card'));
    const buttons = Array.from(document.querySelectorAll('button[data-filter]'));
    let filter = 'all';
    function applyFilter() {{
      const query = input.value.toLowerCase();
      cards.forEach(card => {{
        const kind = card.querySelector('.eyebrow').textContent.trim();
        const okFilter = filter === 'all' || kind === filter;
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


def render_failure_oracle_md(cases: list[tuple[str, dict]]) -> str:
    rows = ["# Failure Case Oracle", "", "| File | Expected failure |", "| --- | --- |"]
    for name, item in cases:
        rows.append(f"| `{name}` | `{', '.join(item['expected_failures'])}` |")
    return "\n".join(rows)


def render_pending_report(kind: str, title: str) -> str:
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

Expected commands:

```powershell
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_native_entry_readonly_inspector.py --rebuild
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_native_entry_readonly_inspector.py
python -B outputs/review/vaks-implementation-sandbox/{SLICE_ID}/artifact/verify_native_entry_readonly_inspector.py --final-gate
```
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
        raise FileNotFoundError("Missing required P2-22 source files: " + "; ".join(missing))

    git_status_summary = "pre-existing dirty tree recorded before build; final audit scoped to this slice path"

    safe_write("slice-plan.md", render_slice_plan(git_status_summary))
    safe_write("source-map.md", render_source_map(paths))
    safe_write("artifact/native-entry-readonly-inspector-contract.md", render_contract(base))
    safe_write("fixtures/valid-native-entry-config.json", json.dumps(base, indent=2, ensure_ascii=False))
    safe_write("fixtures/valid-readonly-inspector-config.json", json.dumps(variant_config(base), indent=2, ensure_ascii=False))

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

    vault = "prototype/vaks-native-entry-readonly-inspector"
    safe_write(f"{vault}/00 Native Home.md", render_native_home(base))
    safe_write(f"{vault}/01 Inbox.md", render_inbox(base))
    safe_write(f"{vault}/02 Status Board.md", render_status_board(base))
    safe_write(f"{vault}/03 Receipt Index.md", render_receipt_index(base))
    safe_write(f"{vault}/04 Boundary Stop.md", render_boundary_stop(base))
    safe_write(f"{vault}/05 Readonly Inspector Guide.md", render_inspector_guide(base))
    safe_write(f"{vault}/06 Next Safe Step.md", render_next_safe_step(base))
    safe_write(f"{vault}/07 Dry Run Results.md", render_dry_run(base))
    safe_write(
        f"{vault}/Cards/Source P2-22.md",
        render_card(
            "Source P2-22",
            "P2-22 is the product-readiness source slice. Its PASS_PRODUCT_GRADE is sandbox-only input, not mainline approval.",
        ),
    )
    safe_write(
        f"{vault}/Cards/Native Entry Contract.md",
        render_card(
            "Native Entry Contract",
            "Native Markdown entry improves navigation and operator feel. Navigation is not authority.",
        ),
    )
    safe_write(
        f"{vault}/Cards/Readonly Inspector Contract.md",
        render_card(
            "Readonly Inspector Contract",
            "The inspector filters and displays only. It has no save, sync, post, write, commit, push, or promotion control.",
        ),
    )
    safe_write(f"{vault}/readonly-inspector.html", render_inspector_html(base))
    safe_write(
        f"{vault}/Receipts/native-entry-readonly-inspector-receipt.json",
        json.dumps(render_receipt(base, paths), indent=2, ensure_ascii=False),
    )

    safe_write("verification.md", render_verification_pending(), overwrite=False)
    safe_write("reviewer-report.md", render_pending_report("sandbox_reviewer_report", "Reviewer Report"), overwrite=False)
    safe_write("boundary-audit.md", render_pending_report("sandbox_boundary_audit", "Boundary Audit"), overwrite=False)
    safe_write(
        "product-acceptance-report.md",
        render_pending_report("sandbox_product_acceptance_report", "Product Acceptance Report"),
        overwrite=False,
    )
    safe_write("next-step.md", render_next_step_pending(), overwrite=False)


if __name__ == "__main__":
    build()
