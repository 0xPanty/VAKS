---
case_id: block-silent-title-collision
expected: BLOCK
adapter:
  name: file
  source_type: file
  input_identity: "local:two.md"
  output_source_path: "raw/articles/same-title.md"
  adapter_status: ok
collision_handling: silent_overwrite
---

# BLOCK: Silent Title Collision

Same title but different source must use collision-safe output or review pressure.
