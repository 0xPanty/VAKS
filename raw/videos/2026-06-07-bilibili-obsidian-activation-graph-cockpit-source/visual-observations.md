---
record_kind: visual_observation
status: candidate_observation
knowledge_status: raw
source_ref: raw/videos/2026-06-07-bilibili-obsidian-activation-graph-cockpit-source.md
source_url: https://www.bilibili.com/video/BV1DcEc6KEpw/
captured_at: "2026-06-07 05:47:02 +08:00"
captured_by: Codex
action_basis_allowed: false
truth_mutation_allowed: false
---

# Visual Observations: Obsidian Activation Graph Cockpit Demo

## Boundary

This file records visual observations from a public 44-second Bilibili video.

It is not a transcript, not reviewed evidence, not a reproduction guide, and not
action basis. The video has no public subtitle list, no description, and no
clear oral explanation. Interpretation below is therefore visual-only candidate
comprehension.

## Observed Source Metadata

- Platform: Bilibili
- BV: `BV1DcEc6KEpw`
- Title: `基于obsidian与GPT5.5的自生长自迭代知识库网络`
- Uploader: `乐创科技`
- Published: `2026-06-04 13:21:43 +08:00`
- Duration: `44s`
- Public subtitle list: empty
- Public description: empty

## Visual Notes

The video shows an Obsidian vault named roughly:

```text
paper_writing_obsidian_vault
```

The left sidebar exposes a paper-writing oriented structure:

```text
10_Project_Change_Log
20_Paper_Memories
30_Writing_Rules
35_Workflow_Governance
40_Final_Generalized_Rules
45_Supervision
50_Conflicts
60_Limited_Rules
70_Iterative_Thinking
00_Index
```

The center view is Obsidian Graph View. At first there are fewer nodes and a
small cluster. As the video progresses, more nodes and edges appear, and the
graph becomes denser.

Visible node labels include examples such as:

```text
Paper memory synchronization convention
Paper memory export path convention
Mentor feedback - abstract framing and priority rule
2026-06-01 Introduction first paragraph references
2026-06-03 Mentor revised introduction first paragraph style
Keyword selection high-priority rule
Keyword selection rule - method object morphology mechanism
Introduction material advantage should transition through interface
Abstract rule - interface wave as validation only
Abstract rule - predict layer thickness
Abstract final rule - intermetallic layer thickness and distribution
SCI-memory auto-record convention
SCI-memory workflow rule - record to 10 and 40, refresh 20, iterate to 80
README
TEMPLATE supervision correction
kb_rag_token_savings_latest
Codex_manual_analysis_prompt_latest
```

Color / size coding is visually present but not explained in the video:

```text
green nodes: many ordinary knowledge/rule nodes
yellow nodes: likely important or intermediate nodes
red nodes: large/hub/conflict/index-like nodes
grey node: weak or peripheral node
```

Because the video gives no legend, this color interpretation is only a visual
hypothesis.

## Candidate Interpretation

The demo appears to show a paper-writing knowledge base that grows from local
memories and corrections into connected rules:

```text
project change / mentor feedback / writing memory
-> candidate writing rules
-> conflict / limited / supervision buckets
-> generalized final rules
-> workflow governance / index / future prompt references
```

The strongest observable idea is not "Obsidian graph equals truth". It is:

```text
Use a graph cockpit to make candidate knowledge collisions visible.
```

For VAKS, this is a product / operator-surface reference:

```text
candidate points, conflicts, limited rules, generalized rules, and review_due
markers should be visible as a collision/iteration cockpit.
```

## What Not To Infer

- Do not infer a complete reproducible workflow from this short video.
- Do not treat `GPT5.5` in the title as verified product evidence.
- Do not treat graph position, node size, color, or edge count as truth,
  confidence, support, or reviewed relation strength.
- Do not copy the paper-writing folder structure as a VAKS schema.
- Do not promote visual interpretation into reviewed knowledge without later
  source anchors or implementation evidence.

## Reference Layer Tag

Canonical tag:

```text
ref/activation-graph-cockpit
```

Chinese label:

```text
图谱碰撞驾驶舱
```

Plain meaning:

```text
用图谱/看板展示候选知识如何互相碰撞、冲突、受限、泛化、复查和迭代。
```

This tag is for reference-layer routing only. It is not a truth label.
