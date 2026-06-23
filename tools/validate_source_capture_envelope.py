#!/usr/bin/env python
"""Compatibility wrapper for the Source Capture self-test.

The real self-test entry point is `tools/selftest_source_capture.py`. This file
is kept so older review commands fail soft instead of breaking immediately.
"""

from __future__ import annotations

from selftest_source_capture import main


if __name__ == "__main__":
    raise SystemExit(main())
