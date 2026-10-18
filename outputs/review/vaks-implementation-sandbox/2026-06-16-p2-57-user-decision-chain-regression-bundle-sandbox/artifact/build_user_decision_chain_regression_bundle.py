from __future__ import annotations

import html
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
RUNNER = ARTIFACT / "run_user_decision_chain_regression_bundle.py"
READOUT = ARTIFACT / "user_decision_chain_regression_readout.md"
PROTOTYPE = ARTIFACT / "user_decision_chain_regression_prototype.html"


def import_runner():
    spec = importlib.util.spec_from_file_location("p2_57_runner_for_build", RUNNER)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load p2-57 runner")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def render_html(result: dict) -> str:
    rows = []
    for report in result["source_reports"]:
        rows.append(
            "<tr>"
            f"<td>{html.escape(report['slice_id'])}</td>"
            f"<td>{'PASS' if report['product_pass'] else 'FAIL'}</td>"
            f"<td>{'PASS' if report['reviewer_pass'] else 'FAIL'}</td>"
            f"<td>{'PASS' if report['boundary_pass'] else 'FAIL'}</td>"
            f"<td>{html.escape(report['verification_status'])}</td>"
            "</tr>"
        )
    must_not = "".join(f"<li>{html.escape(item)}</li>" for item in result["must_not"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>User Decision Chain Regression</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }}
    main {{ max-width: 1080px; margin: 0 auto; }}
    h1 {{ font-size: 28px; margin-bottom: 8px; }}
    .summary {{ display: grid; grid-template-columns: repeat(4, minmax(0, 1fr)); gap: 12px; margin: 20px 0; }}
    .metric {{ background: #fff; border: 1px solid #d1d5db; border-radius: 8px; padding: 14px; }}
    .label {{ font-size: 12px; color: #6b7280; text-transform: uppercase; }}
    .value {{ font-size: 24px; margin-top: 6px; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #d1d5db; padding: 9px; text-align: left; font-size: 14px; }}
    th {{ background: #e5e7eb; }}
    .boundary {{ margin-top: 20px; padding: 14px; border: 1px solid #f59e0b; background: #fffbeb; border-radius: 8px; }}
  </style>
</head>
<body>
<main>
  <h1>User Decision Chain Regression</h1>
  <p>Sandbox-only regression readout. This is not execution authority, mainline approval, promotion approval, Obsidian sync approval, reviewed knowledge, evidence support, or action basis.</p>
  <section class="summary">
    <div class="metric"><div class="label">Source slices</div><div class="value">{len(result['source_reports'])}</div></div>
    <div class="metric"><div class="label">p2-56 gate</div><div class="value">{result['p2_56_final_gate_passed']}</div></div>
    <div class="metric"><div class="label">Demo scenarios</div><div class="value">{result['demo_summary']['scenario_count']}</div></div>
    <div class="metric"><div class="label">Chain passed</div><div class="value">{result['chain_passed']}</div></div>
  </section>
  <table>
    <thead><tr><th>Source slice</th><th>Product</th><th>Reviewer</th><th>Boundary</th><th>Verification</th></tr></thead>
    <tbody>{''.join(rows)}</tbody>
  </table>
  <section class="boundary">
    <strong>must_not</strong>
    <ul>{must_not}</ul>
  </section>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    runner = import_runner()
    result = runner.run_bundle()
    READOUT.write_text(result["readout_markdown"] + "\n", encoding="utf-8")
    PROTOTYPE.write_text(render_html(result), encoding="utf-8")
    print(json.dumps({"passed": result["chain_passed"], "readout": str(READOUT), "prototype": str(PROTOTYPE)}, ensure_ascii=False, indent=2))
    return 0 if result["chain_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
