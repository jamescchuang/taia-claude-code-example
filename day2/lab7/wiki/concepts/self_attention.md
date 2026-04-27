---
title: Self-Attention（自注意力機制）
type: concept
tags: [Transformer, Attention]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/llm_internals.md]
---

# Self-Attention（自注意力機制）

## 它在做什麼

兩件事（[llm_internals](../sources/llm_internals.md) p47–p55）：

1. **找出 context 中哪些 token 會影響當前 token 的意思**
2. **把這些 token 的資訊加進當前 token**

例：「兩顆青蘋果」中的「果」，要被「青」（顏色）、「蘋」（複合詞）等影響。

## 機制（QKV）

對每個 token 算三個投影：

- `q = W_q · embedding`（query：我想找什麼）
- `k = W_k · embedding`（key：我代表什麼）
- `v = W_v · embedding`（value：我能貢獻什麼資訊）

當前 token 的 `q` 與所有 token 的 `k` 做 dot product 得到 attention score：

```
score_i = q · k_i
weights = softmax(scores)         # 歸一化
output  = Σ weights_i · v_i       # 加權平均所有 value
```

## Multi-head Attention

不只一組 (W_q, W_k, W_v)，而是多組「平行注意力頭」，每組關注不同面向 — 例如一頭找形容詞、另一頭找數量詞（[llm_internals](../sources/llm_internals.md) p56）。最後接 `W_O` 投影合併。

## Positional Embedding

QKV 機制本身沒有位置資訊：「兩顆青蘋果」與「青山綠水紅蘋果」中的「果」會混淆。解法：在 token embedding 上加一個 **Positional Embedding**（[llm_internals](../sources/llm_internals.md) p50）。

## Causal Attention

實作上 LLM 只考慮**左邊（前面）**的 token — 用 mask 把未來位置的 attention score 設成 −∞（[llm_internals](../sources/llm_internals.md) p61）。這保證自迴歸生成時，第 t 個位置看不到 t+1 之後的答案。

## 計算量

每生成一個 token，要對 context 所有 token 重新計算 QKV 與 attention。輸入越長，運算量隨平方成長。**這就是 context 長度有上限的根本原因**，也是 [Context Rot](context_rot.md) 與 [Compression](compression.md) 出現的物理背景。

## 相關頁

- [transformer_architecture](transformer_architecture.md)
- [feed_forward_layer](feed_forward_layer.md)
- [context_rot](context_rot.md)
