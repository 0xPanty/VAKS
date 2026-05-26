---
type: pattern
status: candidate
created: 2026-05-26
source_libraries:
  - ArthurYangX/nano-NotebookLM
related_concepts:
  - qmd-local-hybrid-search-layer
  - source-verification-and-trust-model
related_projects:
  - verified-vault
adoption_status: watch
tags:
  - vector-index
  - embedding
  - cache
  - namespace
  - migration
evidence_count: 1
confidence: high
---

# 设计模式：Embedding Preset Namespaced Index Cache

## 一句话定义

不同 embedding 模型的索引必须写进不同命名空间；切换模型是切路径或后台重建，不是覆盖旧索引。

## 解决的问题

向量索引最容易出现的隐性错误是：

```text
旧模型 384d 向量
新模型 1024d / 3072d 向量
混进同一个 index/cache
```

轻则检索质量下降，重则维度不匹配报错。更危险的是静默错排。

## nano-NotebookLM 的机制

- embedding preset：
  - `local_mini`
  - `openai_large`
  - `bge_m3`
- FAISS 路径：
  - `indices/faiss/<preset>/global`
  - `indices/faiss/<preset>/<course_id>`
- concept embedding：
  - legacy `concept_embedding`
  - per-preset `concept_embeddings[preset_id]`
- 切换 preset 后：
  - 已建过的 preset 直接读旧路径。
  - 没建过的 preset 后台重建。
  - 维度不一致时丢弃 cache 并重算。

## 对我们资料库的意义

如果未来引入 QMD / FAISS / Zilliz / 本地向量库，必须把 embedding 模型当成 index contract 的一部分。

建议未来索引 metadata 至少包含：

- embedding_provider
- embedding_model
- embedding_dimension
- index_scope
- source_snapshot_hash
- built_at
- schema_version

## 来源证据

- `nano_notebooklm/config.py`：`EMBEDDING_PRESETS`、`active_preset_id`。
- `nano_notebooklm/kb/store.py`：`_faiss_root()` 按 preset 路由。
- `nano_notebooklm/kg/graph.py`：`concept_embeddings` per-preset bucket。
- `tests/test_embedding_preset.py`：验证路径命名空间、偏好持久化、legacy migration、per-preset concept embedding。

## 标签与量化

- domain: retrieval_infrastructure
- problem: embedding_model_switch_safety
- maturity: proven-in-repo
- complexity: medium
- problem_fit: 4
- reuse_value: 5
- implementation_cost: 3
- integration_fit: 4
- evidence_strength: 4
- reversibility: 5

## 项目融合建议

短期不实现，因为本资料库还没进入向量检索阶段。

但一旦开始做 vector index，这条应该变成硬规则：

```text
No embedding model identity, no reusable vector cache.
```

