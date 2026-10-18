from __future__ import annotations

import html
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
RUNNER = ARTIFACT / "run_user_decision_operator_handoff_index.py"
READOUT = ARTIFACT / "user_decision_operator_handoff_index_readout.md"
PROTOTYPE = ARTIFACT / "user_decision_operator_handoff_index_prototype.html"


def import_runner():
    spec = importlib.util.spec_from_file_location("p2_59_runner", RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-59 runner")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def render_html(index: dict) -> str:
    rows = "".join(
        "<tr>"
        f"<td>{html.escape(entry['slice_id'])}</td>"
        f"<td>{'PASS' if entry['product_pass'] else 'FAIL'}</td>"
        f"<td>{'PASS' if entry['reviewer_pass'] else 'FAIL'}</td>"
        f"<td>{'PASS' if entry['boundary_pass'] else 'FAIL'}</td>"
        f"<td>{html.escape(entry['verification_status'])}</td>"
        f"<td>{html.escape(entry['final_gate_command'])}</td>"
        f"<td>{html.escape(entry['operator_use'])}</td>"
        "</tr>"
        for entry in index["entries"]
    )
    must_not = "".join(f"<li>{html.escape(item)}</li>" for item in index["must_not"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>User Decision Operator Handoff Index</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }}
    main {{ max-width: 1120px; margin: 0 auto; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #d1d5db; padding: 8px; text-align: left; font-size: 14px; }}
    th {{ background: #e5e7eb; }}
    .summary {{ margin: 18px 0; padding: 14px; background: #fff; border: 1px solid #d1d5db; border-radius: 8px; }}
  </style>
</head>
<body>
<main>
  <h1>User Decision Operator Handoff Index</h1>
  <p>Sandbox-only routing surface. It is not a user decision, execution authority, mainline approval, promotion approval, Obsidian sync approval, reviewed knowledge, evidence support, or action basis.</p>
  <section class="summary">
    <strong>Latest gate passed:</strong> {index['latest_source_final_gate_passed']}<br>
    <strong>Source chain ready:</strong> {index['source_chain_ready']}<br>
    <strong>Self reports passed:</strong> {index['self_report_gate']['overall_pass']}<br>
    <strong>Handoff ready:</strong> {index['handoff_ready']}<br>
    <strong>Entries:</strong> {index['entry_count']}
  </section>
  <table>
    <thead><tr><th>Slice</th><th>Product</th><th>Reviewer</th><th>Boundary</th><th>Verification</th><th>Gate command</th><th>Operator use</th></tr></thead>
    <tbody>{rows}</tbody>
  </table>
  <section><h2>must_not</h2><ul>{must_not}</ul></section>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    runner = import_runner()
    index = runner.run_index()
    READOUT.write_text(index["handoff_markdown"] + "\n", encoding="utf-8")
    PROTOTYPE.write_text(render_html(index), encoding="utf-8")
    print(
        json.dumps(
            {
                "source_chain_ready": index["source_chain_ready"],
                "handoff_ready": index["handoff_ready"],
                "readout": str(READOUT),
                "prototype": str(PROTOTYPE),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0 if index["source_chain_ready"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
