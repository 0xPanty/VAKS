import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent


def run(args):
    subprocess.run([sys.executable, *args], cwd=ROOT, check=True)


def main():
    variants = ["baseline_full", "control_leaky", "candidate_no_version", "candidate_with_version"]
    for variant in variants:
        run([
            "renderer.py",
            "--cases", "cases_input.json",
            "--anchors", "anchors.json",
            "--variant", variant,
            "--out", f"artifacts_{variant}.json",
        ])
        run([
            "checker.py",
            "--artifacts", f"artifacts_{variant}.json",
            "--gold", "gold_oracle.json",
            "--rules", "authority_rules.json",
            "--root", ".",
            "--out", f"checks_{variant}.json",
        ])

    run([
        "aggregator.py",
        "--gold", "gold_oracle.json",
        "--baseline-artifacts", "artifacts_baseline_full.json",
        "--candidate-artifacts", "artifacts_candidate_with_version.json",
        "--candidate-checks", "checks_candidate_with_version.json",
        "--variant", "candidate_with_version",
        "--out-json", "independent_patch_results.json",
        "--out-report", "INDEPENDENT_ORACLE_PATCH_REPORT.md",
    ])

    print((ROOT / "INDEPENDENT_ORACLE_PATCH_REPORT.md").read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
