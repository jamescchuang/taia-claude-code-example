---
title: In-context Learning（ICL）
type: concept
tags: [Prompt, ICL]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/context_engineering.md]
---

# In-context Learning（ICL）

在 prompt 中提供少量範例（few-shot examples），讓模型「現場學會」新任務。**模型參數沒有被改變**，只是被範例推到了正確的接龍機率分佈。

## 原始發現

GPT-3 論文 [arXiv 2005.14165](https://arxiv.org/abs/2005.14165)（[context_engineering](../sources/context_engineering.md) p18）。同一個模型，加幾筆範例就能解新任務 — 從翻譯、算術到分類。

## 為什麼算「學習」

打引號的「學習」：與 fine-tune 不同，這裡沒有梯度更新。但對使用者而言效果類似——多給範例、表現變好。

## 極長 context 下的 ICL

[Gemini 1.5](https://storage.googleapis.com/deepmind-media/gemini/gemini_v1_5_report.pdf)（[context_engineering](../sources/context_engineering.md) p19–p21）：把整本語法書塞進 context，模型可以翻譯訓練資料中沒看過的低資源語言。

> "Almost all improvements stem from the book's parallel examples rather than its grammatical explanations."

→ **範例比規則更有效**。這呼應 ICL 的本質：模型靠模式匹配，不靠演繹。

## 與 Prompt Engineering 的關係

[Prompt Engineering](prompt_engineering.md) 中「給範例」這一招，本質就是 ICL。

## 局限

- 範例越多 → context 越長 → [Context Rot](context_rot.md) 風險。
- 範例選得不好會誤導；對應到 [RAG](rag.md) 中 reranking 的重要性。
- 範例表現有上限，真正困難或新穎的任務仍需 fine-tune。

## 相關頁

- [prompt_engineering](prompt_engineering.md)
- [training_pipeline](training_pipeline.md)
- [context_rot](context_rot.md)
