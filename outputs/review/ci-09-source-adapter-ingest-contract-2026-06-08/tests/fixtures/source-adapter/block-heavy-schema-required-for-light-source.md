---
case_id: block-heavy-schema-required-for-light-source
expected: BLOCK
adapter:
  name: manual-note
  source_type: manual_note
  input_identity: "local:note.md"
  adapter_status: ok
required_for_light_source:
  full_prov_ontology: true
  exhaustive_line_ranges: true
  reviewed_evidence_packet: true
---

# BLOCK: Heavy Schema Required For Light Source

Light source capture must not be blocked by a heavy universal adapter schema.
