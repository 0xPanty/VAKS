from __future__ import annotations

import json
import shutil
from copy import deepcopy
from pathlib import Path
from typing import Any

from silky_workbench_validator import REQUIRED_SLICE_IDS, SLICE_ID


SLICE_ROOT = Path(__file__).resolve().parents[1]
PROTOTYPE_VAULT = SLICE_ROOT / "prototype" / "vaks-silky-workbench-vault"

SOURCE_PATTERNS = [
    {
        "id": "obsidian_bases_filtered_views",
        "source": "Obsidian Bases views",
        "borrowed": "filtered table/card/list thinking for status surfaces",
        "vaks_boundary": "views display state only; filters are not approval",
    },
    {
        "id": "tana_supertag_typed_objects",
        "source": "Tana Supertags",
        "borrowed": "typed objects with fields and collection views",
        "vaks_boundary": "typed cards do not create reviewed relations",
    },
    {
        "id": "capacities_object_first_capture",
        "source": "Capacities object-first notes",
        "borrowed": "capture as objects instead of forcing folder choice first",
        "vaks_boundary": "capture creates raw/candidate orientation only",
    },
    {
        "id": "notebooklm_sources_chat_studio",
        "source": "NotebookLM Sources/Chat/Studio",
        "borrowed": "three-panel movement between source, question, and generated artifact",
        "vaks_boundary": "generated output is not evidence support by default",
    },
    {
        "id": "notebooklm_goal_focused_chat",
        "source": "NotebookLM goal-focused chat",
        "borrowed": "goal-scoped work modes for different user intents",
        "vaks_boundary": "goal mode cannot override validators",
    },
    {
        "id": "vaks_boundary_preserving_status",
        "source": "VAKS P0-P2 sandbox results",
        "borrowed": "receipts, validators, status, and action boundary as visible product rails",
        "vaks_boundary": "status and receipts do not become authority",
    },
]

LANES = [
    {
        "id": "capture_now",
        "label": "Capture Now",
        "primary_action": "drop source, note, transcript, or repo into quarantine",
        "boundary": "raw/candidate only; not reviewed knowledge",
        "icon": "inbox",
    },
    {
        "id": "triage_status",
        "label": "Triage Status",
        "primary_action": "see blocked, stale, dirty, and missing-anchor states",
        "boundary": "status display only; does not approve",
        "icon": "pulse",
    },
    {
        "id": "review_radar",
        "label": "Review Radar",
        "primary_action": "route candidates with gaps into review pressure",
        "boundary": "review_due is pressure, not truth mutation",
        "icon": "radar",
    },
    {
        "id": "receipt_center",
        "label": "Receipt Center",
        "primary_action": "inspect hash, source, operation, and product acceptance receipts",
        "boundary": "hash receipt is process integrity, not evidence support",
        "icon": "receipt",
    },
    {
        "id": "action_boundary",
        "label": "Action Boundary",
        "primary_action": "stop before action until action readiness and sufficiency pass",
        "boundary": "this workbench is not action basis",
        "icon": "stop",
    },
    {
        "id": "next_step",
        "label": "Next Safe Step",
        "primary_action": "show the one bounded next move",
        "boundary": "next step is guidance only; no commit, no push, no sync",
        "icon": "arrow",
    },
]

BOUNDARY_COPY = [
    "sandbox only",
    "not reviewed knowledge",
    "not evidence support",
    "not action basis",
    "does not approve",
    "no sync",
    "no commit",
    "no push",
]

SEARCH_TARGETS = [
    "PASS_PRODUCT_GRADE",
    "not action basis",
    "not evidence support",
    "reviewed knowledge",
    "dirty state",
    "review due",
    "hash receipt",
    "next safe step",
]


def _stage(slice_id: str) -> str:
    if "-p0-" in slice_id:
        return "P0"
    if "-p1-5-" in slice_id:
        return "P1.5"
    if "-p1-" in slice_id:
        return "P1"
    if "-p2-" in slice_id:
        return "P2"
    return "unknown"


def _short_value(slice_id: str) -> str:
    value_map = {
        "p0-01": "retrieval has an explicit receipt before anyone treats it as useful context",
        "p0-02": "operations show what ran, what changed, and what stayed blocked",
        "p0-03": "body drift is caught before downstream use",
        "p0-04": "support claims are separated from provenance and background",
        "p0-05": "action basis is blocked until readiness checks pass",
        "p0-06": "feedback creates review pressure without mutating truth",
        "p0-07": "known action-boundary failures become visible test cases",
        "p1-08": "retrieval and operation receipts can be validated together",
        "p1-09": "query loops stay read-only and explain their limits",
        "p1-10": "runtime artifacts are excluded from knowledge surfaces",
        "p1-11": "semantic anchors are checked before support is claimed",
        "p1-5-12": "robust retrieval ranks context without becoming trust",
        "p1-5-13": "local graph retrieval stays read-only and non-authoritative",
        "p1-5-14": "raw intake routes material without premature interpretation",
        "p1-5-15": "markdown validation and search become a sidecar, not a truth layer",
        "p1-5-16": "MISA memory bridge is quarantined from VAKS truth",
        "p2-17": "use surfaces are prioritized around entry, status, and receipts",
        "p2-18": "cockpit prototype gives operator status without authority",
        "p2-19": "product candidates are screened before workflow build",
        "p2-20": "product workflow shows where to go and where to stop",
    }
    for key, value in value_map.items():
        if key in slice_id:
            return value
    return "sandbox value captured"


def _report_ref_for_html(slice_id: str, report_name: str) -> str:
    return f"../../../{slice_id}/{report_name}"


def _report_ref_for_card(slice_id: str, report_name: str) -> str:
    return f"../../../../{slice_id}/{report_name}"


def default_config() -> dict[str, Any]:
    cards = []
    for item in REQUIRED_SLICE_IDS:
        cards.append(
            {
                "slice_id": item,
                "stage": _stage(item),
                "product_status": "pass_product_grade",
                "user_value": _short_value(item),
                "next_safe_step": "open product acceptance, then next-step, before touching any mainline file",
                "verification_ref": _report_ref_for_html(item, "verification.md"),
                "boundary_ref": _report_ref_for_html(item, "boundary-audit.md"),
                "product_ref": _report_ref_for_html(item, "product-acceptance-report.md"),
                "card_verification_ref": _report_ref_for_card(item, "verification.md"),
                "card_boundary_ref": _report_ref_for_card(item, "boundary-audit.md"),
                "card_product_ref": _report_ref_for_card(item, "product-acceptance-report.md"),
            }
        )
    return {
        "record_kind": "vaks_silky_obsidian_workbench_config",
        "slice_id": SLICE_ID,
        "scope": {
            "sandbox_only": True,
            "target_vault_path": "prototype/vaks-silky-workbench-vault",
            "write_targets": [
                "prototype/vaks-silky-workbench-vault/",
                "prototype/vaks-silky-workbench-vault/cockpit.html",
            ],
            "formal_vault_write": False,
            "obsidian_sync": False,
            "production_ui": False,
            "real_base_files": False,
            "starts_runtime_or_service": False,
            "installs_dependencies": False,
            "uses_mcp_write_tools": False,
            "runs_hooks": False,
            "runs_long_automation": False,
            "commits": False,
            "pushes": False,
            "promotes_mainline": False,
            "writes_reviewed_truth": False,
            "creates_evidence_support": False,
            "creates_action_basis": False,
        },
        "boundary_copy": BOUNDARY_COPY,
        "frontier_patterns": SOURCE_PATTERNS,
        "workbench_lanes": LANES,
        "search_targets": SEARCH_TARGETS,
        "journeys": [
            {
                "id": "capture_to_receipt",
                "start": "Capture Now",
                "end": "Receipt Center",
                "max_steps": 3,
                "boundary_check": "raw/candidate only; receipt is not evidence support",
            },
            {
                "id": "status_to_blocker",
                "start": "Home",
                "end": "blocked reason",
                "max_steps": 2,
                "boundary_check": "status does not approve",
            },
            {
                "id": "review_to_evidence",
                "start": "Review Radar",
                "end": "Evidence & Receipts",
                "max_steps": 3,
                "boundary_check": "candidate is not support",
            },
            {
                "id": "action_exit",
                "start": "Action Boundary",
                "end": "not-action-basis stop",
                "max_steps": 1,
                "boundary_check": "workbench is not action basis",
            },
            {
                "id": "return_to_next_step",
                "start": "Any card",
                "end": "Next Safe Step",
                "max_steps": 2,
                "boundary_check": "no commit, no push, no sync",
            },
        ],
        "experience_metrics": {
            "max_clicks_to_status": 2,
            "max_clicks_to_boundary": 2,
            "max_clicks_to_receipt": 2,
            "formal_vault_file_delta_allowed": 0,
            "broken_wikilinks_allowed": 0,
        },
        "slice_cards": cards,
    }


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def _write_if_missing(path: Path, text: str) -> None:
    if not path.exists():
        _write(path, text)


def _yaml(value: str) -> str:
    return json.dumps(value, ensure_ascii=False)


def _card_name(slice_id: str) -> str:
    return f"Cards/{slice_id}"


def _frontmatter(lines: dict[str, Any]) -> str:
    body = ["---"]
    for key, value in lines.items():
        if isinstance(value, bool):
            body.append(f"{key}: {str(value).lower()}")
        else:
            body.append(f"{key}: {_yaml(str(value))}")
    body.append("---")
    return "\n".join(body)


def build_vault(config: dict[str, Any], vault_root: Path = PROTOTYPE_VAULT) -> None:
    if vault_root.exists():
        shutil.rmtree(vault_root)
    (vault_root / ".obsidian").mkdir(parents=True, exist_ok=True)
    (vault_root / "Cards").mkdir(parents=True, exist_ok=True)
    (vault_root / "Receipts").mkdir(parents=True, exist_ok=True)

    _write(
        vault_root / ".obsidian" / "app.json",
        json.dumps(
            {
                "alwaysUpdateLinks": True,
                "newFileLocation": "current",
                "showUnsupportedFiles": True,
                "attachmentFolderPath": "Attachments",
            },
            indent=2,
        ),
    )

    home_links = "\n".join(
        f"- [[{_card_name(card['slice_id'])}|{card['stage']} {card['slice_id']}]] - {card['user_value']}"
        for card in config["slice_cards"]
    )
    lane_cards = "\n".join(
        f"### {lane['label']}\n\n- Primary action: {lane['primary_action']}\n- Boundary: {lane['boundary']}\n"
        for lane in config["workbench_lanes"]
    )
    _write(
        vault_root / "00 Home - VAKS Workbench.md",
        f"""{_frontmatter({"record_kind": "vaks_silky_home", "sandbox_only": True, "not_action_basis": True})}

# VAKS Silky Workbench

## Now

- [[10 Capture Now|Capture Now]]
- [[20 Review Radar|Review Radar]]
- [[30 Evidence & Receipts|Evidence & Receipts]]
- [[40 Action Boundary|Action Boundary]]
- [[50 Slice Map|Slice Map]]
- [[60 Frontier Principles|Frontier Principles]]

## Workbench Lanes

{lane_cards}

## Slice Cards

{home_links}

## Boundary

This workbench is sandbox only, not reviewed knowledge, not evidence support,
not action basis, and does not approve. There is no sync, no commit, and no push.
""",
    )

    _write(
        vault_root / "10 Capture Now.md",
        f"""{_frontmatter({"record_kind": "vaks_capture_surface", "sandbox_only": True})}

# Capture Now

Use this page as the low-friction front door. The intended product behavior is:

1. Paste material into a raw/candidate quarantine.
2. Generate a retrieval or operation receipt.
3. Show the next safe step.

Boundary: capture is sandbox only, not reviewed knowledge, not evidence support,
not action basis, and does not approve.

Jump to [[30 Evidence & Receipts]] or [[20 Review Radar]].
""",
    )

    _write(
        vault_root / "20 Review Radar.md",
        f"""{_frontmatter({"record_kind": "vaks_review_radar", "sandbox_only": True})}

# Review Radar

Review due means pressure, not truth mutation. The radar prioritizes:

- missing evidence;
- stale scope;
- negative feedback;
- dirty state;
- anchor mismatch;
- action boundary risk.

Next safe step: open the relevant card, then read its verification, reviewer
report, boundary audit, product acceptance, and next-step file.

{home_links}
""",
    )

    _write(
        vault_root / "30 Evidence & Receipts.md",
        f"""{_frontmatter({"record_kind": "vaks_receipt_surface", "sandbox_only": True})}

# Evidence & Receipts

Receipts make process integrity visible. They are not evidence support.

Search targets:

{chr(10).join(f"- {target}" for target in config["search_targets"])}

Receipt center links:

- [[00 Home - VAKS Workbench|Home]]
- [[40 Action Boundary|Action Boundary]]
- [[50 Slice Map|Slice Map]]
""",
    )

    _write(
        vault_root / "40 Action Boundary.md",
        f"""{_frontmatter({"record_kind": "vaks_action_boundary_surface", "sandbox_only": True, "not_action_basis": True})}

# Action Boundary

Stop here before action.

This workbench is not action basis. Later action use requires separate action
readiness and evidence sufficiency gates. Pretty navigation, status, receipt,
badge, or search success does not approve anything.

No sync. No commit. No push. No promotion.

Return to [[00 Home - VAKS Workbench]] or inspect [[30 Evidence & Receipts]].
""",
    )

    slice_rows = "\n".join(
        f"| [[{_card_name(card['slice_id'])}|{card['slice_id']}]] | {card['stage']} | {card['product_status']} | {card['next_safe_step']} |"
        for card in config["slice_cards"]
    )
    _write(
        vault_root / "50 Slice Map.md",
        f"""{_frontmatter({"record_kind": "vaks_slice_map", "sandbox_only": True})}

# Slice Map

| Slice | Stage | Product status | Next safe step |
|---|---|---|---|
{slice_rows}

Boundary: map navigation is not reviewed knowledge, not evidence support, not
action basis, and does not approve.
""",
    )

    pattern_rows = "\n".join(
        f"| {item['id']} | {item['borrowed']} | {item['vaks_boundary']} |"
        for item in config["frontier_patterns"]
    )
    _write(
        vault_root / "60 Frontier Principles.md",
        f"""{_frontmatter({"record_kind": "vaks_frontier_principles", "sandbox_only": True})}

# Frontier Principles

| Pattern | Borrowed product move | VAKS boundary |
|---|---|---|
{pattern_rows}

These are design references only. They are not reviewed knowledge, not evidence
support, not action basis, and do not approve mainline changes.
""",
    )

    for card in config["slice_cards"]:
        _write(
            vault_root / "Cards" / f"{card['slice_id']}.md",
            f"""{_frontmatter({"record_kind": "vaks_slice_card", "slice_id": card["slice_id"], "stage": card["stage"], "sandbox_only": True})}

# {card['slice_id']}

## User Value

{card['user_value']}

## Product Status

{card['product_status']}

## Required Reading

- [[00 Home - VAKS Workbench|Home]]
- [[30 Evidence & Receipts|Evidence & Receipts]]
- [[40 Action Boundary|Action Boundary]]
- [[50 Slice Map|Slice Map]]

## Verification Trail

- [verification]({card['card_verification_ref']})
- [boundary audit]({card['card_boundary_ref']})
- [product acceptance]({card['card_product_ref']})

## Next Safe Step

{card['next_safe_step']}

## Boundary

This card is sandbox only, not reviewed knowledge, not evidence support, not action basis, and does not approve. No sync, no commit, no push.

## Search Cues

PASS_PRODUCT_GRADE; dirty state; review due; hash receipt; next safe step; not action basis; not evidence support.
""",
        )

    receipt = {
        "record_kind": "vaks_silky_workbench_build_receipt",
        "slice_id": SLICE_ID,
        "generated_vault": str(vault_root.relative_to(SLICE_ROOT)),
        "slice_cards": len(config["slice_cards"]),
        "formal_vault_write": False,
        "obsidian_sync": False,
        "commit": False,
        "push": False,
    }
    _write(vault_root / "Receipts" / "sandbox-workbench-build-receipt.json", json.dumps(receipt, indent=2))
    _write(vault_root / "cockpit.html", _cockpit_html(config))


def _cockpit_html(config: dict[str, Any]) -> str:
    data = json.dumps(config, ensure_ascii=False)
    return f"""<!doctype html>
<html lang=\"en\" data-sandbox-only=\"true\">
<head>
  <meta charset=\"utf-8\">
  <meta name=\"viewport\" content=\"width=device-width, initial-scale=1\">
  <title>VAKS Silky Workbench Sandbox</title>
  <style>
    :root {{
      --ink:#17202a; --muted:#5d6673; --line:#d9dee7; --soft:#f7f8fa;
      --blue:#2563eb; --green:#16825d; --red:#b42318; --amber:#a15c07;
      --panel:#ffffff; --violet:#6d43c2;
    }}
    * {{ box-sizing:border-box; }}
    body {{ margin:0; font-family:Inter,Segoe UI,Arial,sans-serif; color:var(--ink); background:#f2f4f8; letter-spacing:0; }}
    header {{ display:flex; gap:16px; align-items:center; justify-content:space-between; padding:18px 24px; background:var(--panel); border-bottom:1px solid var(--line); position:sticky; top:0; z-index:2; }}
    h1 {{ font-size:20px; margin:0; font-weight:700; }}
    button {{ border:1px solid var(--line); background:#fff; color:var(--ink); padding:8px 10px; border-radius:6px; cursor:pointer; }}
    button.active {{ background:#e9f0ff; border-color:#8eb1ff; color:#123f9a; }}
    main {{ display:grid; grid-template-columns:260px 1fr 310px; gap:16px; padding:16px; max-width:1440px; margin:0 auto; }}
    section, aside {{ background:var(--panel); border:1px solid var(--line); border-radius:8px; min-width:0; }}
    .panel-title {{ padding:12px 14px; border-bottom:1px solid var(--line); font-weight:700; }}
    #laneTabs {{ display:grid; gap:8px; padding:12px; }}
    #quickSearch {{ width:100%; border:1px solid var(--line); border-radius:6px; padding:10px; font-size:14px; }}
    .search-wrap {{ padding:12px; border-bottom:1px solid var(--line); }}
    #sliceGrid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(260px,1fr)); gap:10px; padding:12px; }}
    .card {{ border:1px solid var(--line); border-radius:8px; padding:12px; background:#fff; min-height:196px; display:flex; flex-direction:column; gap:8px; }}
    .stage {{ font-size:12px; font-weight:700; color:#fff; border-radius:4px; padding:3px 6px; display:inline-block; width:max-content; }}
    .P0 {{ background:var(--blue); }} .P1 {{ background:var(--green); }} .P15 {{ background:var(--violet); }} .P2 {{ background:var(--amber); }}
    .status {{ color:var(--green); font-size:12px; font-weight:700; }}
    .muted {{ color:var(--muted); font-size:13px; line-height:1.4; }}
    #boundaryRail {{ padding:12px; display:grid; gap:10px; }}
    .rail-item {{ border-left:4px solid var(--red); background:#fff7f6; padding:10px; border-radius:6px; }}
    .metric {{ display:flex; justify-content:space-between; border-bottom:1px solid var(--line); padding:8px 0; font-size:13px; }}
    .links {{ display:flex; flex-wrap:wrap; gap:6px; margin-top:auto; }}
    .links a {{ color:#123f9a; text-decoration:none; border:1px solid #c8d8ff; border-radius:5px; padding:4px 6px; font-size:12px; background:#f5f8ff; }}
    @media (max-width:980px) {{ main {{ grid-template-columns:1fr; }} header {{ position:static; flex-direction:column; align-items:stretch; }} }}
  </style>
</head>
<body>
  <header>
    <div>
      <h1>VAKS Silky Workbench</h1>
      <div class=\"muted\">Sandbox product prototype. Not reviewed knowledge, not evidence support, not action basis.</div>
    </div>
    <button id=\"commandButton\" title=\"Open command palette\">Command</button>
  </header>
  <main>
    <aside>
      <div class=\"panel-title\">Lanes</div>
      <div id=\"laneTabs\"></div>
    </aside>
    <section>
      <div class=\"search-wrap\"><input id=\"quickSearch\" placeholder=\"Search slice, stage, blocker, receipt, action boundary\" aria-label=\"Search slices\"></div>
      <div id=\"sliceGrid\"></div>
    </section>
    <aside>
      <div class=\"panel-title\">Boundary Rail</div>
      <div id=\"boundaryRail\"></div>
    </aside>
  </main>
  <script type=\"application/json\" id=\"workbenchData\">{data}</script>
  <script>
    const data = JSON.parse(document.getElementById('workbenchData').textContent);
    const grid = document.getElementById('sliceGrid');
    const tabs = document.getElementById('laneTabs');
    const rail = document.getElementById('boundaryRail');
    const search = document.getElementById('quickSearch');
    let stageFilter = 'all';
    function stageClass(stage) {{ return stage === 'P1.5' ? 'P15' : stage; }}
    function renderTabs() {{
      const stages = '<button class=\"active\" data-tab-kind=\"stage\" data-filter=\"all\">All stages</button>' + ['P0','P1','P1.5','P2'].map(s => `<button data-tab-kind=\"stage\" data-filter=\"${{s}}\">${{s}}</button>`).join('');
      const lanes = data.workbench_lanes.map(lane => `<button data-tab-kind=\"lane\" data-filter=\"${{lane.id}}\" title=\"${{lane.boundary}}\">${{lane.label}}</button>`).join('');
      tabs.innerHTML = stages + '<div class=\"muted\">Workbench lanes</div>' + lanes;
      tabs.querySelectorAll('button').forEach(btn => btn.onclick = () => {{
        stageFilter = btn.dataset.filter;
        tabs.querySelectorAll('button').forEach(x => x.classList.remove('active'));
        btn.classList.add('active');
        renderCards();
      }});
    }}
    function renderCards() {{
      const q = search.value.toLowerCase();
      const laneText = JSON.stringify(data.workbench_lanes).toLowerCase();
      const cards = data.slice_cards.filter(card => {{
        const haystack = (JSON.stringify(card) + ' ' + laneText + ' dirty state review due hash receipt action boundary not action basis not evidence support').toLowerCase();
        const filterOk = stageFilter === 'all' || card.stage === stageFilter || haystack.includes(stageFilter.replaceAll('_',' '));
        return filterOk && haystack.includes(q);
      }});
      grid.innerHTML = cards.map(card => `<article class=\"card\"><span class=\"stage ${{stageClass(card.stage)}}\">${{card.stage}}</span><strong>${{card.slice_id}}</strong><span class=\"status\">${{card.product_status}}</span><p class=\"muted\">${{card.user_value}}</p><p class=\"muted\"><b>Next:</b> ${{card.next_safe_step}}</p><div class=\"links\"><a data-link-kind=\"verification\" href=\"${{card.verification_ref}}\">verification</a><a data-link-kind=\"boundary\" href=\"${{card.boundary_ref}}\">boundary</a><a data-link-kind=\"product\" href=\"${{card.product_ref}}\">product</a></div></article>`).join('');
    }}
    function renderRail() {{
      rail.innerHTML = data.boundary_copy.map(item => `<div class=\"rail-item\">${{item}}</div>`).join('') +
        Object.entries(data.experience_metrics).map(([k,v]) => `<div class=\"metric\"><span>${{k}}</span><b>${{v}}</b></div>`).join('');
    }}
    document.getElementById('commandButton').onclick = () => {{ search.focus(); search.select(); }};
    search.addEventListener('input', renderCards);
    renderTabs(); renderCards(); renderRail();
  </script>
</body>
</html>"""


def write_docs(config: dict[str, Any]) -> None:
    _write(
        SLICE_ROOT / "slice-plan.md",
        f"""---
record_kind: sandbox_slice_plan
slice_id: {SLICE_ID}
status: built_pending_verification
truth_boundary: sandbox_plan_only
---

# Slice Plan

## Goal

Build a world-frontier, boundary-preserving, sandbox-only Obsidian workbench that
makes VAKS feel smoother without making navigation, search, status, or receipts
look like truth authority.

## Why This Slice Exists

The first 20 slices proved the safety and product workflow layers. The isolated
Obsidian smoke test showed the next bottleneck: the artifacts are useful but
still too engineering-shaped. This slice turns them into a reusable product
surface: home, lanes, slice cards, receipt center, review radar, and action
boundary exit.

## Only Written Path

`outputs/review/vaks-implementation-sandbox/{SLICE_ID}/`

## Not Touched

Root architecture docs, `wiki/claims`, `wiki/patterns`, `wiki/decisions`,
`templates`, `tools`, formal Obsidian vault, commit, push, sync, hooks, and
runtime services.

## Acceptance

- config, builder, validator, fixtures, failure cases, and generated prototype
  exist;
- prototype opens as an isolated Obsidian-style vault and as static HTML;
- validation covers navigation, search, boundary copy, path containment, and
  authority confusion;
- Reviewer, Boundary Auditor, and GPT-5.5 xhigh Product Acceptance pass.
""",
    )
    _write(
        SLICE_ROOT / "source-map.md",
        """---
record_kind: sandbox_source_map
truth_boundary: source_map_only
---

# Source Map

## Current VAKS Sources

- P2-17 use-surface optimization pass.
- P2-18 Bases cockpit prototype.
- P2-19 product experience screening sandbox.
- P2-20 product workflow prototype.
- Prior isolated Obsidian smoke test: 20 slice cards, 240 wikilinks, 0 broken
  links, formal vault unchanged.

## External Product References

- Obsidian Bases views: filtered views and view-local filters as a model for
  status surfaces. Source:
  https://obsidian.md/help/bases/views
- Tana Supertags: typed nodes, fields, and searchable table-style collections.
  Source:
  https://outliner.tana.inc/learn/features/supertags
- Capacities: object-first capture and connected objects reduce filing
  overhead. Source:
  https://capacities.io/
- NotebookLM Sources/Chat/Studio: unified movement between source management,
  questions, and generated outputs. Source:
  https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-new-features-december-2024/
- NotebookLM goal-focused chat: mode/goal selection improves answer fit.
  Source:
  https://blog.google/innovation-and-ai/models-and-research/google-labs/notebooklm-custom-personas-engine-upgrade/
- Read-only product UX scout agent: recommended prioritizing Home Command
  Center, Raycast-style quick entry, Quick Capture Inbox, Operator Status
  Cockpit, Dirty-State Shield, and Receipt Ledger Inspector.

## Borrowed, Not Adopted

These are product references only. They do not create reviewed knowledge,
evidence support, action basis, mainline readiness, or a new VAKS authority
layer.
""",
    )
    _write(
        SLICE_ROOT / "artifact" / "silky-workbench-contract.md",
        """# Silky Workbench Contract

## Input Contract

- Existing P0-P2 sandbox slice reports.
- A workbench config with lanes, slice cards, frontier patterns, boundary copy,
  journeys, and experience metrics.

## Output Contract

- Isolated Obsidian-style vault under this sandbox slice.
- Static `cockpit.html` for quick inspection.
- Build receipt proving no formal vault write, no sync, no commit, no push.

## Product Promise

The user should be able to answer these in two clicks or fewer:

- Where do I put this?
- What state is it in?
- What blocks review or action?
- What receipt or validator should I inspect?
- What is the next safe step?

## Boundary Promise

The workbench is sandbox only, not reviewed knowledge, not evidence support, not
action basis, and does not approve. Status, badges, links, search hits, and hash
receipts stay display/process surfaces only.
""",
    )
    _write_if_missing(SLICE_ROOT / "reviewer-report.md", "---\nrecord_kind: sandbox_reviewer_report\nstatus: pending_reviewer\n---\n\n# Reviewer Report\n\nPending independent read-only review.\n")
    _write_if_missing(SLICE_ROOT / "boundary-audit.md", "---\nrecord_kind: sandbox_boundary_audit\nstatus: pending_boundary_audit\n---\n\n# Boundary Audit\n\nPending independent read-only boundary audit.\n")
    _write_if_missing(SLICE_ROOT / "product-acceptance-report.md", "---\nrecord_kind: sandbox_product_acceptance_report\nstatus: pending_product_acceptance\nagent_requirement: GPT-5.5 reasoning=xhigh\n---\n\n# Product Acceptance Report\n\nPending GPT-5.5 extra-high product acceptance.\n")
    _write_if_missing(SLICE_ROOT / "next-step.md", "---\nrecord_kind: sandbox_next_step\nstatus: pending_acceptance\n---\n\n# Next Step\n\nIf Product Acceptance passes, this slice may be considered the candidate product wrapper for a future formal VAKS workbench slice. It still cannot be merged, synced, committed, pushed, or promoted without separate user approval.\n")


def write_fixtures_and_failures(config: dict[str, Any]) -> None:
    fixtures = SLICE_ROOT / "fixtures"
    failures = SLICE_ROOT / "failure-cases"
    fixtures.mkdir(parents=True, exist_ok=True)
    failures.mkdir(parents=True, exist_ok=True)
    _write(fixtures / "valid-silky-workbench-config.json", json.dumps(config, indent=2, ensure_ascii=False))
    minimal = deepcopy(config)
    minimal["experience_metrics"]["max_clicks_to_receipt"] = 2
    _write(fixtures / "valid-silky-workbench-config-variant.json", json.dumps(minimal, indent=2, ensure_ascii=False))

    cases: dict[str, tuple[str, dict[str, Any]]] = {}

    def add(name: str, code: str, mutate) -> None:
        data = deepcopy(config)
        mutate(data)
        cases[name] = (code, data)

    add("formal-vault-write-enabled.json", "WB_FORBIDDEN_SCOPE_ENABLED", lambda d: d["scope"].update({"formal_vault_write": True}))
    add("formal-vault-target-path.json", "WB_TARGET_VAULT_OUTSIDE_PROTOTYPE", lambda d: d["scope"].update({"target_vault_path": "H:/Obsidian/资料库"}))
    add("sync-enabled.json", "WB_FORBIDDEN_SCOPE_ENABLED", lambda d: d["scope"].update({"obsidian_sync": True}))
    add("real-base-file-enabled.json", "WB_FORBIDDEN_SCOPE_ENABLED", lambda d: d["scope"].update({"real_base_files": True}))
    add("starts-service.json", "WB_FORBIDDEN_SCOPE_ENABLED", lambda d: d["scope"].update({"starts_runtime_or_service": True}))
    add("installs-dependencies.json", "WB_FORBIDDEN_SCOPE_ENABLED", lambda d: d["scope"].update({"installs_dependencies": True}))
    add("mcp-write-enabled.json", "WB_FORBIDDEN_SCOPE_ENABLED", lambda d: d["scope"].update({"uses_mcp_write_tools": True}))
    add("commit-push-enabled.json", "WB_FORBIDDEN_SCOPE_ENABLED", lambda d: d["scope"].update({"commits": True, "pushes": True}))
    add("protected-write-target.json", "WB_PROTECTED_WRITE_TARGET", lambda d: d["scope"]["write_targets"].append("templates/workbench.md"))
    add("missing-boundary-copy.json", "WB_BOUNDARY_PHRASE_MISSING", lambda d: d.update({"boundary_copy": ["sandbox only"]}))
    add("copy-claims-action-basis.json", "WB_COPY_AUTHORITY_CONFUSION", lambda d: d["boundary_copy"].append("This workbench is action basis."))
    add("copy-claims-evidence-support.json", "WB_COPY_AUTHORITY_CONFUSION", lambda d: d["boundary_copy"].append("This receipt is evidence support."))
    add("missing-frontier-pattern.json", "WB_FRONTIER_PATTERN_MISSING", lambda d: d.update({"frontier_patterns": d["frontier_patterns"][1:]}))
    add("missing-lane.json", "WB_LANE_MISSING", lambda d: d.update({"workbench_lanes": d["workbench_lanes"][1:]}))
    add("missing-search-target.json", "WB_SEARCH_TARGET_MISSING", lambda d: d.update({"search_targets": d["search_targets"][:-1]}))
    add("missing-required-slice.json", "WB_REQUIRED_SLICE_MISSING", lambda d: d.update({"slice_cards": d["slice_cards"][:-1]}))
    add("slice-not-pass.json", "WB_SLICE_STATUS_NOT_PASS", lambda d: d["slice_cards"][0].update({"product_status": "pending"}))
    add("journey-too-long.json", "WB_JOURNEY_TOO_LONG", lambda d: d["journeys"][0].update({"max_steps": 7}))
    add("journey-boundary-missing.json", "WB_JOURNEY_BOUNDARY_MISSING", lambda d: d["journeys"][0].update({"boundary_check": ""}))
    add("status-too-deep.json", "WB_STATUS_TOO_DEEP", lambda d: d["experience_metrics"].update({"max_clicks_to_status": 5}))
    add("formal-vault-delta-allowed.json", "WB_FORMAL_VAULT_DELTA_ALLOWED", lambda d: d["experience_metrics"].update({"formal_vault_file_delta_allowed": 1}))

    oracle = {}
    for name, (code, data) in cases.items():
        _write(failures / name, json.dumps(data, indent=2, ensure_ascii=False))
        oracle[name] = {"expected_valid": False, "expected_codes": [code]}
    _write(SLICE_ROOT / "artifact" / "failure-case-oracle.json", json.dumps(oracle, indent=2, ensure_ascii=False))
    lines = ["# Failure Case Oracle", ""]
    for name, value in sorted(oracle.items()):
        lines.append(f"- `{name}` -> `{', '.join(value['expected_codes'])}`")
    _write(SLICE_ROOT / "artifact" / "failure-case-oracle.md", "\n".join(lines))


def write_package() -> dict[str, Any]:
    config = default_config()
    write_docs(config)
    write_fixtures_and_failures(config)
    build_vault(config)
    return {
        "slice_id": SLICE_ID,
        "prototype_vault": str(PROTOTYPE_VAULT.relative_to(SLICE_ROOT)),
        "slice_cards": len(config["slice_cards"]),
        "lanes": len(config["workbench_lanes"]),
    }


if __name__ == "__main__":
    print(json.dumps(write_package(), indent=2, ensure_ascii=False))
