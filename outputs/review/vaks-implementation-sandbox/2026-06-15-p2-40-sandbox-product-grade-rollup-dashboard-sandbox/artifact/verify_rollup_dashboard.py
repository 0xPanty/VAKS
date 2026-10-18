from __future__ import annotations

import argparse
import json
import sys

from rollup_common import validate_all


def main() -> int:
    parser = argparse.ArgumentParser(description="Verify P2-40 sandbox product-grade rollup dashboard.")
    parser.add_argument("--rebuild", action="store_true", help="Rebuild sandbox artifacts before verification.")
    parser.add_argument("--final-gate", action="store_true", help="Require review, boundary, product, and next-step reports to be closed.")
    args = parser.parse_args()
    if args.rebuild:
        from build_rollup_dashboard import build

        build()
    result = validate_all(final_gate=args.final_gate)
    result["rebuild"] = args.rebuild
    result["final_gate"] = args.final_gate
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["passed"] else 1


if __name__ == "__main__":
    sys.exit(main())
