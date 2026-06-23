# VAKS Guarded Answer Brake Pressure R1.0

This package tests whether the VAKS answer brake is useful.

It compares an intentionally unsafe baseline answer path with a guarded answer
path across enterprise-style user simulations.

Measured questions:

- Does the brake remove unsupported strong claims?
- Does it qualify partial/scope-limited claims?
- Does it abstain or review missing-anchor, candidate-only, stale, and conflict cases?
- Does it preserve supported useful claims?
- Does it avoid granting action readiness?
- Does the deterministic brake add acceptable local latency?

It is sandbox-only and does not write truth/review/action state.
