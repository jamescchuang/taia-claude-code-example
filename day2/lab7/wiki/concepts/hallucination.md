---
title: 幻覺（Hallucination）
type: concept
tags: [基礎, 限制]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/llm_principles.md]
---

# 幻覺（Hallucination）

語言模型自信地產出**不存在或錯誤**的內容。

## 機制成因

LLM 真正做的事就是文字接龍（[token_and_autoregressive](token_and_autoregressive.md)）：

- 模型只在乎「下一個 token 機率高」，不在乎事實。
- 「機率最高 ≠ 事實正確」。例如 [llm_principles](../sources/llm_principles.md) p18 的例子：ChatGPT 4o（關閉搜尋）給出一個**根本不存在**的網址 — 因為符合 URL 格式的 token 序列在訓練資料中很常見。

## 暗無天日的小房間（p19 比喻）

模型像關在小房間，**只能看到使用者輸入**：

- 問「今天是幾月幾號？」時，沒有時間感知 → 隨機接個 X 月 X 日。
- 解法不是「修模型」，而是「**確保輸入資訊足夠**」 → 這就是 [Context Engineering](context_engineering.md) 的緣起。

## 緩解策略

| 策略 | 對應頁 |
|------|--------|
| 把當前時間/地點放進 system prompt | [system_prompt](system_prompt.md) |
| 讓模型查資料再答 | [rag](rag.md), [tool_use](tool_use.md) |
| 顯式 reasoning，鼓勵自我驗證 | [reasoning](reasoning.md) |
| 對輸出做信心估計（投影片未深入） | — |

## 重點

幻覺不是 bug，是 LLM 的本質特性。要靠系統設計（context、tools、verification）來緩解，而不是期待模型「自己學會誠實」。

## 相關頁

- [token_and_autoregressive](token_and_autoregressive.md)
- [softmax_and_temperature](softmax_and_temperature.md)
- [context_engineering](context_engineering.md)
