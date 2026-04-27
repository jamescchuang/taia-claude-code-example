---
title: Feed-Forward Layer
type: concept
tags: [Transformer, FFN]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/llm_internals.md]
---

# Feed-Forward Layer

每層 Transformer 中位於 [Self-Attention](self_attention.md) 之後的子模組。對**每個位置獨立**做非線性變換（不跨位置混合資訊）。

## 數學式

```
h = ReLU(W · x + b)
y = ReLU'(W' · h + b')
```

兩層全連接 + 非線性激活（ReLU 或變體）。每個 neuron 計算 `y = ReLU(w1·x1 + w2·x2 + ... + b)`（[llm_internals](../sources/llm_internals.md) p65）。

## 解讀：Key-Value Memory 視角

Geva et al. 2020 的 [Transformer Feed-Forward Layers Are Key-Value Memories](https://arxiv.org/abs/2012.14913)（[llm_internals](../sources/llm_internals.md) p64）提出：

- 第一層權重的列 = key（偵測某種輸入模式）
- 第二層權重的行 = value（被觸發後寫入的資訊）

→ FFN 可視為一個**可微的查表系統**，存放模型的「事實知識」與模式記憶。Attention 負責「混合」，FFN 負責「儲存」。

## 為什麼重要

- 大多數模型參數其實在 FFN（不是 Attention）。
- [Activation Engineering](activation_engineering.md) 操作的「拒絕成分」、「諂媚成分」很多就是 FFN 的輸出方向。
- FFN 是**位置獨立**的，這是它與 Attention 的關鍵差異。

## 相關頁

- [self_attention](self_attention.md)
- [transformer_architecture](transformer_architecture.md)
- [activation_engineering](activation_engineering.md)
