---
title: Embedding（Token / Contextualized）
type: concept
tags: [基礎, Embedding, Representation]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/llm_internals.md]
---

# Embedding（Token / Contextualized）

## Token Embedding

- 進入模型的第一步：透過 **Embedding Table**（一個 `Vocabulary × dim` 的矩陣）把每個 token id 轉成向量。
- 「同一個 token 永遠有同一個 token embedding」、「意思相近的 token 距離相近」（[llm_internals](../sources/llm_internals.md) p18）。

## Contextualized Embedding

經過 Layer 1 ... Layer L 後，每個位置的向量會根據**上下文**改變：

- 「使用蘋果」中的「果」與「來吃蘋果」中的「果」，token embedding 相同，但 contextualized embedding 不同（[llm_internals](../sources/llm_internals.md) p19）。
- 也叫 hidden representation 或 latent representation。

## 幾何意義（向量空間方向性）

- 特定方向有特定含意：例如有「中英翻譯方向」、「冷↔熱方向」。
- 經典例子：`Emb(冷) − Emb(cold) + Emb(small) ≈ Emb(小)`（[llm_internals](../sources/llm_internals.md) p21）。
- 投影到低維空間可看出語法結構（Hewitt & Manning, NAACL 2019）；國家對應的首都會在空間中形成可預測的位移（arXiv 2310.02207，分析 LLaMA）。

## 與 Unembedding 的首尾呼應

- 最後一層 representation 透過 LM head 點積回 embedding table，挑出對應 token 的 logit（[llm_internals](../sources/llm_internals.md) p16）。
- 也就是說：模型最後的輸出空間，跟最開始的輸入空間，是「同一個」embedding 空間。

## 相關頁

- [transformer_architecture](transformer_architecture.md) — embedding 在整體架構中的位置
- [activation_engineering](activation_engineering.md) — 對 hidden representation 動手腳
- [token_and_autoregressive](token_and_autoregressive.md) — 為什麼需要 embedding
