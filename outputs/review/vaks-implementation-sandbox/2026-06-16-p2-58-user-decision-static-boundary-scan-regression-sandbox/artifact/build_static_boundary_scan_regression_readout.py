from __future__ import annotations

import html
import importlib.util
import json
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
ARTIFACT = ROOT / "artifact"
SCANNER_PATH = ARTIFACT / "static_boundary_scan_regression.py"
READOUT = ARTIFACT / "static_boundary_scan_regression_readout.md"
PROTOTYPE = ARTIFACT / "static_boundary_scan_regression_prototype.html"


def import_scanner():
    spec = importlib.util.spec_from_file_location("p2_58_scanner_for_build", SCANNER_PATH)
    if spec is None or spec.loader is None:
        raise RuntimeError("cannot load scanner")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module


def render_markdown(result: dict) -> str:
    lines = [
        "# Static Boundary Scan Regression Readout",
        "",
        "Sandbox-only scanner regression. This is not a general security sandbox, execution authority, mainline approval, promotion approval, reviewed knowledge, evidence support, or action basis.",
        "",
        "| Live source | Issues |",
        "| --- | --- |",
    ]
    for item in result["positive_results"]:
        lines.append(f"| `{item['path']}` | `{len(item['issues'])}` |")
    lines.extend(["", "## Scanner Limits", ""])
    lines.extend(f"- {limit}" for limit in result["scanner_limits"])
    lines.extend(["", "## must_not", ""])
    lines.extend(f"- `{item}`" for item in result["must_not"])
    return "\n".join(lines)


def render_html(result: dict) -> str:
    rows = "".join(
        f"<tr><td>{html.escape(item['path'])}</td><td>{len(item['issues'])}</td></tr>"
        for item in result["positive_results"]
    )
    limits = "".join(f"<li>{html.escape(limit)}</li>" for limit in result["scanner_limits"])
    must_not = "".join(f"<li>{html.escape(item)}</li>" for item in result["must_not"])
    return f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Static Boundary Scan Regression</title>
  <style>
    body {{ font-family: Arial, sans-serif; margin: 32px; color: #1f2937; background: #f8fafc; }}
    main {{ max-width: 980px; margin: 0 auto; }}
    table {{ width: 100%; border-collapse: collapse; background: #fff; }}
    th, td {{ border: 1px solid #d1d5db; padding: 9px; text-align: left; }}
    th {{ background: #e5e7eb; }}
    section {{ margin-top: 22px; }}
  </style>
</head>
<body>
<main>
  <h1>Static Boundary Scan Regression</h1>
  <p>Sandbox-only scanner regression. This is not a general security sandbox, execution authority, mainline approval, promotion approval, reviewed knowledge, evidence support, or action basis.</p>
  <table><thead><tr><th>Live source</th><th>Issues</th></tr></thead><tbody>{rows}</tbody></table>
  <section><h2>Scanner Limits</h2><ul>{limits}</ul></section>
  <section><h2>must_not</h2><ul>{must_not}</ul></section>
</main>
</body>
</html>
"""


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    scanner = import_scanner()
    result = scanner.run_regression()
    READOUT.write_text(render_markdown(result) + "\n", encoding="utf-8")
    PROTOTYPE.write_text(render_html(result), encoding="utf-8")
    print(json.dumps({"passed": all(not item["issues"] for item in result["positive_results"]), "readout": str(READOUT), "prototype": str(PROTOTYPE)}, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
