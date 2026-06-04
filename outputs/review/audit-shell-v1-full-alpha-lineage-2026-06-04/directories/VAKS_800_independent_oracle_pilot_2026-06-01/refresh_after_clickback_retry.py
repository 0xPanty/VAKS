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
    run([PY, "evaluate_clickback_semantic_landing.py"])
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
    run([PY, "make_risk_tiered_reviewer_preflight_24.py"])
    run([PY, "lint_forbidden_wording_zh.py", "--out", "review_packet_risk_tiered_24/forbidden_wording_lint_zh.json", "review_packet_risk_tiered_24/RISK_TIERED_REVIEWER_CARDS_ZH.md"])
    run([PY, "make_operator_adjudication_packet.py"])
    run([PY, "evaluate_quality_gates_800.py"])
    run([PY, "run_codex_operator_preflight_dry_run.py"])


if __name__ == "__main__":
    main()
