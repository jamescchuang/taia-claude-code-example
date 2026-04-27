---
title: Softmax 與 Temperature
type: concept
tags: [基礎, 抽樣, 機率]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/llm_internals.md, ../sources/llm_principles.md]
---

# Softmax 與 Temperature

## Logit → Probability

LM head 對最後一層 representation 做點積，輸出每個 token 的 **logit**（任意實數）。透過 softmax 變成 0-1、加總 1 的機率分佈：

```
P(i) = exp(s_i) / Σ exp(s_j)
```

數字大 → 機率大（[llm_internals](../sources/llm_internals.md) p14）。

## Temperature

引入溫度 `T`：

```
P(i) = exp(s_i / T) / Σ exp(s_j / T)
```

- `T → 0`：分佈塌縮到最大者，輸出變確定性（greedy）。
- `T = 1`：原始 softmax。
- `T` 越大：分佈越平均，輸出越「有創意」也越混亂（[llm_internals](../sources/llm_internals.md) p15）。

## 為什麼每次回答不同

- 模型輸出**機率分佈**而非單一答案。
- 真正選 token 是「擲骰子」（抽樣）— 即便 temperature=0，也只是把骰子改成偏的（[llm_principles](../sources/llm_principles.md) p9）。
- 這也是為什麼模型常常自信地給出錯誤答案（[hallucination](hallucination.md)）：機率高 ≠ 事實正確。

## 與其他抽樣策略

投影片只提到 temperature，但實務上常搭配 top-k、top-p（nucleus）截斷，效果疊加。

## 相關頁

- [token_and_autoregressive](token_and_autoregressive.md)
- [transformer_architecture](transformer_architecture.md)
- [hallucination](hallucination.md)
