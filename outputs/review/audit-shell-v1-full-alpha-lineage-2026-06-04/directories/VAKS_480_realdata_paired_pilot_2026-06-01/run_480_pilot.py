import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PY = sys.executable
VARIANTS = [
    "baseline_full",
    "shell_core",
    "shell_core_plus_recurrence",
    "shell_core_plus_unversioned_control",
]


def run(args):
    print("+", " ".join(str(arg) for arg in args))
    subprocess.run(args, cwd=ROOT, check=True)


def main():
    run([PY, "fetch_real_rows.py"])
    run([PY, "build_480_cases.py"])
    for variant in VARIANTS:
        run([PY, "renderer_480.py", "--cases", "cases_input.json", "--variant", variant, "--out", f"artifacts_{variant}.json"])
        run(
            [
                PY,
                "checker_480.py",
                "--artifacts",
                f"artifacts_{variant}.json",
                "--gold",
                "gold_oracle.json",
                "--authority-rules",
                "authority_rules.json",
                "--out",
                f"checks_{variant}.json",
            ]
        )
    run(
        [
            PY,
            "aggregator_480.py",
            "--gold",
            "gold_oracle.json",
            "--dataset-manifest",
            "data/case_build_manifest.json",
            "--baseline-artifacts",
            "artifacts_baseline_full.json",
            "--variant",
            "shell_core",
            "artifacts_shell_core.json",
            "checks_shell_core.json",
            "--variant",
            "shell_core_plus_recurrence",
            "artifacts_shell_core_plus_recurrence.json",
            "checks_shell_core_plus_recurrence.json",
            "--variant",
            "shell_core_plus_unversioned_control",
            "artifacts_shell_core_plus_unversioned_control.json",
            "checks_shell_core_plus_unversioned_control.json",
            "--out-json",
            "pilot_480_results.json",
            "--out-report",
            "reports/PILOT_480_REPORT.md",
        ]
    )


if __name__ == "__main__":
    main()
