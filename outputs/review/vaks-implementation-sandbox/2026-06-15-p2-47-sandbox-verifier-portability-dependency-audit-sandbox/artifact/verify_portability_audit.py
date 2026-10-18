from __future__ import annotations

import argparse
import json

from portability_audit import build, validate_all


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify the sandbox verifier portability/dependency audit.")
    parser.add_argument("--rebuild", action="store_true", help="Regenerate slice-local generated artifacts before verifying.")
    parser.add_argument("--final-gate", action="store_true", help="Require reviewer, boundary, product, and next-step statuses.")
    args = parser.parse_args()
    if args.rebuild:
        build()
    result = validate_all(final_gate=args.final_gate)
    result["rebuild"] = args.rebuild
    result["final_gate"] = args.final_gate
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
