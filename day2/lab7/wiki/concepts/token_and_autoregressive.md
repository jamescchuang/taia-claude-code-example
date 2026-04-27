---
title: Token 與 Autoregressive Generation（文字接龍）
type: concept
tags: [基礎, Token, 生成]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/llm_principles.md, ../sources/llm_internals.md]
---

# Token 與 Autoregressive Generation（文字接龍）

## Token

- **Token** 是 LLM 的最小單位，常被翻成「代幣」；可以是字、詞片段、字元，甚至圖片 patch 或聲音取樣段。
- Vocabulary（詞彙表）是固定大小，需「覆蓋所有可能的輸出需求」（[llm_principles](../sources/llm_principles.md) p7）。
- 同一個 token 永遠對應同一個初始 token embedding；經過 layer 後變成 contextualized embedding（[embedding](embedding.md)）。
- 中文不一定一字一 token，實際分法由 tokenizer 決定。

## Autoregressive Generation（文字接龍）

策略：把「產生一段任意長序列」拆成「每次只產生一個 token，遞迴地給回模型再產生下一個」。

```
x → y1
x, y1 → y2
x, y1, y2 → y3
...
x, y1...y_{T-1} → y_T
x, y1...y_T → [END]
```

- 每一步是有限選擇的**分類問題**（從 vocabulary 中挑一個），由模型輸出機率分佈後抽樣。
- 抽樣引入隨機性 → 每次回答不同（[llm_principles](../sources/llm_principles.md) p9）；溫度控制隨機程度見 [softmax_and_temperature](softmax_and_temperature.md)。
- 圖片、聲音也用同框架：把它們切 token，再做接龍（[llm_principles](../sources/llm_principles.md) p21–28）。1024×1024 的圖約需 100 萬次接龍。

## 為什麼這個框架重要

- 它是 LLM 一切行為的底層 — 對話、推理、Tool Use、Multi-Agent，從模型角度都是 token 接龍（[ai_agent](ai_agent.md) p45）。
- 它解釋了幻覺（[hallucination](hallucination.md)）：模型只在乎「下一個 token 機率高」，不在乎事實。
- 它解釋了 context 長度限制：每接一個 token，前面所有 token 都要重新算 attention（[self_attention](self_attention.md)）。

## 相關頁

- [embedding](embedding.md) — token 怎麼變成向量
- [softmax_and_temperature](softmax_and_temperature.md) — 機率分佈與抽樣
- [hallucination](hallucination.md) — 文字接龍的副作用
