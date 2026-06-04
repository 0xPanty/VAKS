import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent
PY = sys.executable
VARIANTS = [
    "baseline_full",
    "shell_core",
    "shell_core_plus_recurrence",
    "leaky_or_unversioned_control",
    "authority_leaky_renderer",
    "fake_precision_feedback_renderer",
]


def run(args):
    print("+", " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def main():
    run([PY, "fetch_data_800.py"])
    run([PY, "build_candidate_cases_800.py"])
    run([PY, "materialize_clickback_snapshots_800.py"])
    run([PY, "freeze_gold_oracle_800.py"])
    for variant in VARIANTS:
        run([PY, "renderer_800.py", "--cases", "candidate_cases.json", "--variant", variant, "--out", f"artifacts_{variant}.json"])
        run([PY, "checker_800.py", "--artifacts", f"artifacts_{variant}.json", "--gold", "gold_oracle_frozen.json", "--rules", "authority_rules_800.json", "--out", f"checks_{variant}.json"])
    aggregate = [
        PY,
        "aggregator_800.py",
        "--gold",
        "gold_oracle_frozen.json",
        "--case-manifest",
        "data/case_build_manifest.json",
        "--baseline-artifacts",
        "artifacts_baseline_full.json",
    ]
    for variant in VARIANTS:
        if variant == "baseline_full":
            continue
        aggregate.extend(["--variant", variant, f"artifacts_{variant}.json", f"checks_{variant}.json"])
    aggregate.extend(["--out-json", "pilot_800_results.json", "--out-report", "reports/PILOT_800_REPORT.md"])
    run(aggregate)
    run([PY, "run_authority_fuzz_800.py"])
    run([PY, "make_human_review_packet.py"])


if __name__ == "__main__":
    main()
