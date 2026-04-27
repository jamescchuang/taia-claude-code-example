---
title: Context Rot 與長 Context 的限制
type: concept
tags: [Context, 限制, ContextRot]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/context_engineering.md]
---

# Context Rot 與長 Context 的限制

> **能讀上百萬個 token，並不代表能讀「懂」上百萬個 token。** ([context_engineering](../sources/context_engineering.md) p48)

## 主要現象

### 1. RAG 的甜蜜點

[Databricks 研究](https://www.databricks.com/blog/long-context-rag-performance-llms)（[context_engineering](../sources/context_engineering.md) p49）：在某閾值以下，多塞文件確實有幫助；超過後**反而下降**。資料太多 → 模型「看不下去」。

### 2. Lost in the Middle

[arXiv 2307.03172](https://arxiv.org/abs/2307.03172)（[context_engineering](../sources/context_engineering.md) p50）：把關鍵資訊放在 context 開頭或結尾，模型回答正確率高；放中間 → 顯著下降。「比較記得開頭跟結尾」。

### 3. Lost in Conversation

[arXiv 2505.06120](https://arxiv.org/pdf/2505.06120v1)（p51）：多輪對話下，早期對話內容也會被遺忘或誤用。

### 4. Context Rot

Chroma research 的 [Context Rot 報告](https://research.trychroma.com/context-rot)（p52）：**輸入 tokens 越多，模型表現越差** — 即使內容相關，也會劣化。

## 為什麼會這樣

物理層面：[Self-Attention](self_attention.md) 計算量隨輸入平方成長；訓練時也很少看到極長序列，分佈外行為難預測。

認知層面：模型 attention weight 是有限資源，過多 token 互搶 → 訊雜比下降。

## 緩解：對應到 Context Engineering

[Context Engineering](context_engineering.md) 三招都是針對 context rot 的解法：

| 招 | 怎麼解 |
|---|--------|
| [Select / RAG](rag.md) | 只塞最相關的 |
| [Compress](compression.md) | 把長歷史摘要成短的 |
| [Multi-Agent](multi_agent.md) | 把長 context 隔到子 agent 裡 |

## 重點

長 context window 不是萬靈丹。**Context 品質 > Context 長度**。設計 LLM 應用時要主動瘦身 context，不能仰賴模型「自己會挑」。

## 相關頁

- [self_attention](self_attention.md)
- [context_engineering](context_engineering.md)
- [rag](rag.md)
- [compression](compression.md)
