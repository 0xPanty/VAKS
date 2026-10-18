---
type: visual_observation
status: source-artifact
source_id: bilibili-BV1iSVG6eEsj
source_card: raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source.md
created_at: 2026-06-04
created_by: Codex
visual_method: public video frame sampling
frame_sampling: every 30 seconds
frame_resolution: 852x480
truth_boundary: candidate observation, not reviewed knowledge
---

# Visual Observations

## Artifacts

- Contact sheet: `raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source/visual/contact-sheet-30s-480p.jpg`
- Frames: `raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source/visual/frames-480p/`
- Dropdown crop: `raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source/visual/frame_0780s_dropdown_full_crop_x4.jpg`
- Frame metadata: `raw/videos/2026-06-04-bilibili-raglab-17-rag-visual-canvas-source/visual/visual-frames-480p.json`

## Boundary

These observations come from public video frames. They are candidate observations used to compensate for visual information that ASR cannot capture.

They do not create reviewed knowledge, evidence support, reviewed relations, truth confidence, or action basis.

## Key Visual Findings

1. RAGLab is the central visual workbench.

The video repeatedly shows a RAGLab canvas with nodes and directed edges. Nodes include document loading, text splitting, embedding, vector database, retrieval, Prompt assembly, LLM answer, RAGAS evaluation, GraphRAG/entity extraction, BM25 search, RRF fusion, PageIndex construction, and PageIndex query.

2. The source fixture is structured, not plain text.

At 01:00, a PDF-like document titled `喵星球宠物店 - 品种登记册 v2024` is shown. It contains tables and sectioned breed records. The video uses this to demonstrate why tables, identifiers, and multi-perspective naming matter.

3. The Simple RAG canvas is a pipeline.

At 02:00-05:30, the canvas shows:

```text
文档加载
-> 文本切块
-> Embedding
-> 向量数据库
-> 向量检索
-> Prompt 拼接
-> LLM 生成
-> RAGAS 评估
```

The right panel shows chunk text, retrieval hits, generated answer, and evaluation output.

4. Mechanical chunking can break tables.

At 03:00, a Markdown table is shown. The speaker points at a line where chunking may split a table and lose the table-wide header/context.

5. Fusion Retrieval visibly adds BM25 and RRF.

At 07:30-08:00, the canvas title reads `Fusion Retrieval (混合检索)`. The visual pipeline includes vector retrieval, BM25 retrieval, and `RRF 融合`.

6. Query transform variants are separate nodes.

At 10:00, `Query Rewriting` is a distinct node between question input and retrieval.

At 10:30, `HyDE` is a distinct node between question input and retrieval.

7. Context enrichment is a chunk expansion node.

At 11:30-12:00, `Context Enrichment Window` appears as a separate node that expands retrieved chunk context before prompt assembly.

8. The 17-item list is visually confirmed.

At 13:00, the dropdown includes:

```text
Simple RAG
Fusion Retrieval
Chunk Size
Semantic Chunking
Query Rewriting
HyDE
Reranking
Context Enrichment Window
RAPTOR
Self-RAG
CRAG
Adaptive RAG
Agentic RAG
RAG + RAGAS
GraphRAG
PageIndex
TreeIndex
```

9. GraphRAG is shown as entity/relation/graph structure.

At 00:00-00:30 and 13:30-15:00, the canvas title and graph preview show GraphRAG-style entity/relation extraction and graph layout. The right panel shows node descriptions and graph results.

10. PageIndex is shown as document hierarchy navigation.

At 15:30-16:10, the canvas title reads `PageIndex`. The speaker explains using titles/sections to locate source passages, and the right panel shows query parameters such as `pageindex_id`.

11. Source preview / trace appears at the end.

At 16:30, a modal displays a source section and surrounding text. This visually supports source preview / clickback as a UI pattern, not as automatic evidence support.

## VAKS-Relevant Observations

- The visual interface makes retrieval pathways inspectable.
- The same question can route through different retrieval/context strategies.
- The UI collapses source, retrieval, answer, and evaluation into one workbench, which is good for learning and debugging but dangerous if interpreted as truth authority.
- A VAKS workbench should visually separate:
  - source provenance
  - raw/source text
  - candidate retrieval
  - candidate comprehension
  - evidence-aware review
  - reviewed knowledge
  - action basis
  - feedback/use ledger

## Visual Quality Notes

- Public 480p stream was the highest available through no-cookie public access.
- Large labels and structure are readable.
- Some small Chinese text and exact numeric evaluation values are not reliable from frames.
- Exact UI labels should be user-checked if they become important.
