---
title: 李宏毅三講課程地圖
type: synthesis
tags: [李宏毅, 概覽, 課程地圖]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/llm_principles.md, ../sources/llm_internals.md, ../sources/context_engineering.md]
---

# 李宏毅三講課程地圖

三份投影片構成一條完整的學習路徑：使用者視角 → 模型內部 → Agent 應用。

## 三講之間的關係

```
┌──────────────────────────┐    ┌──────────────────────────┐    ┌──────────────────────────┐
│ 第一講：原理              │    │ 第二講：內部運作          │    │ 第三講：Context Engineering│
│ (生成式 AI 入門)          │ →  │ (Transformer 細節)        │ →  │ (Agent 時代的應用層)      │
│                           │    │                            │    │                            │
│ 使用者視角                │    │ 模型內部視角              │    │ 系統設計者視角            │
│ 「LLM 在做什麼」          │    │ 「LLM 內部怎麼動」        │    │ 「怎麼讓 LLM 做好」       │
└──────────────────────────┘    └──────────────────────────┘    └──────────────────────────┘
        │                                  │                                  │
        ▼                                  ▼                                  ▼
   文字接龍                            Transformer                       Context 管理
   訓練流程                            Attention/FFN                     RAG/Tool/Memory
   幻覺成因                            Embedding 幾何                    Multi-Agent
```

## 概念依賴關係（從基礎到應用）

```
[token_and_autoregressive] ──┬─→ [embedding] ──→ [transformer_architecture]
                              │                          │
                              │                          ├─→ [self_attention]
                              │                          ├─→ [feed_forward_layer]
                              │                          └─→ [softmax_and_temperature]
                              │                                  │
                              ▼                                  ▼
                   [training_pipeline]                   [activation_engineering]
                              │
                              ▼
                       [hallucination]
                              │
                              ▼
                  ┌────[context_engineering]────┐
                  │             │                │
                  ▼             ▼                ▼
              [select]      [compress]      [multi_agent]
                  │             │
                  ▼             ▼
            [rag]         [memory]
            [tool_use]    [reasoning]
                  │
                  └─→ [ai_agent] ←─── [system_prompt]
                          │
                          ▼
                    [context_rot]
```

點擊任一節點對應頁面（在 [index](../index.md) 中可找到）。

## 三講共有的核心觀念

| 觀念 | 第一講 | 第二講 | 第三講 |
|------|--------|--------|--------|
| LLM = 文字接龍 | 主軸 | 觀察視角 | Agent 也是接龍（p45） |
| Context 限制 | Chat Template、多輪對話 | Attention 平方成長 | Lost in the Middle、Context Rot |
| 幻覺 | 暗無天日的小房間 | logit lens 看每層猜測 | RAG / Tool / Reasoning 緩解 |
| 不訓練模型 | 重點是「使用」 | 觀察「已訓練好」的模型 | 「只訓練人類」 |

## 一句話串起三講

> **第一講：LLM 不過是文字接龍。**
> **第二講：而文字接龍的內部，是逐層改造的向量幾何。**
> **第三講：所以使用 LLM 的關鍵，是把對的向量素材放進它有限的 context 視窗。**

## 在本知識庫中如何前進

1. 完全新手：依序讀三份 source 摘要 — [llm_principles](../sources/llm_principles.md) → [llm_internals](../sources/llm_internals.md) → [context_engineering](../sources/context_engineering.md)。
2. 想理解某個現象：先在 [index](../index.md) 找 concept 頁；每個 concept 頁底部有相關頁清單可繼續探索。
3. 新增素材時：請考慮這三講已經建立的概念，盡量重用既有 concept 頁、避免另起新頁，保持知識庫的內聚性。
