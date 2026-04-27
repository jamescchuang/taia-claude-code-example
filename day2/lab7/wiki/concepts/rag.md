---
title: RAG（Retrieval Augmented Generation）
type: concept
tags: [RAG, Context, Select]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/context_engineering.md]
---

# RAG（Retrieval Augmented Generation）

從外部資料源動態檢索相關內容，注入 context 後再生成。是 [Context Engineering](context_engineering.md) **Select** 招式的代表（[context_engineering](../sources/context_engineering.md) p28–p30、p56）。

## 基本流程

```
User Prompt → 抽 keywords → Search Engine → 候選文件
            → Reranking（小 LLM）→ 精選 sentence/段落
            → 拼接到 Context → 主 LLM 生成
```

## 反例：AI Overview「加膠水」事件

Google AI Overview 從 Reddit 笑話檢索到「在 pizza 上加膠水避免起司滑落」，照單全收（[context_engineering](../sources/context_engineering.md) p29）。→ **檢索到的內容不一定可信**；需要來源信譽過濾與 reranking。

## RAG 的擴充：不只資料

**所有「太多塞不進 context」的東西都可以 RAG**：

| 對象 | 對應頁 |
|------|--------|
| 文件 / 知識 | （傳統 RAG） |
| 工具說明（Tool RAG） | [tool_use](tool_use.md) |
| 過去經驗 / 記憶（Memory RAG） | [memory](memory.md) |
| 範例（Example Selection） | [in_context_learning](in_context_learning.md) |

代表論文：[arXiv 2310.03128](https://arxiv.org/abs/2310.03128)、[arXiv 2502.11271](https://arxiv.org/abs/2502.11271)、[arXiv 2505.03275](https://arxiv.org/abs/2505.03275)、Provence [arXiv 2501.16214](https://arxiv.org/abs/2501.16214)。

## 不是檢索越多越好

[context_engineering](../sources/context_engineering.md) p49 引用 Databricks：超過某閾值後，「資料越多反而看不下去」。 → 與 [Context Rot](context_rot.md)、[Lost in the Middle](context_rot.md) 直接相關。

## 與 LLM Wiki 模式的對照

[Karpathy 的 LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) 觀點：傳統 RAG 是「每次重新從原始文件找」，知識沒累積；LLM Wiki 則「先把知識編譯到 wiki，再從 wiki 找」。本知識庫採用後者。

## 相關頁

- [context_engineering](context_engineering.md)
- [memory](memory.md)
- [tool_use](tool_use.md)
- [context_rot](context_rot.md)
