---
title: Transformer 整體架構
type: concept
tags: [Transformer, 架構]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/llm_internals.md]
---

# Transformer 整體架構

## 一張圖看完

```
Tokens → Embedding Table → [Layer 1 → Layer 2 → ... → Layer L] → LM head → Logits → softmax → 下一個 token
```

每個 Layer 內部 = [Self-Attention](self_attention.md) + [Feed-Forward](feed_forward_layer.md)（再加 residual + layernorm，投影片簡化掉）。

## 重要視角

- **Many Layers = Deep Learning**：Layer L 接 Layer L-1 接 ... Layer 1，每層都是矩陣運算（[llm_internals](../sources/llm_internals.md) p11）。
- **首尾呼應**：Embedding Table（輸入端）與 LM head（輸出端）共享同一個向量空間（[embedding](embedding.md)）。
- **Transformer 的特殊性**：不是發明 Attention，而是「拿掉 Attention 以外的東西」（Vaswani et al. 2017，[llm_internals](../sources/llm_internals.md) p46）。

## 每層內部

| 子模組 | 功能 |
|--------|------|
| [Self-Attention](self_attention.md) | 從整段 context 挑出相關 token，混合資訊 |
| [Feed-Forward](feed_forward_layer.md) | 對每個位置獨立做非線性變換（可視為 Key-Value Memory） |

## 為什麼可以堆很多層

- Why Deep？淺網雖也能擬合任意函數，但深度提供更高效的參數利用（[llm_internals](../sources/llm_internals.md) p12 投影片內列出多支延伸講解）。
- 每多一層，contextualized embedding 編碼的抽象層級越高（語法 → 語意 → 世界知識）。

## 觀察工具

- [Logit Lens & Patchscopes](activation_engineering.md)：對中間每一層的 representation 作 unembedding，看模型「思考過程」。

## 相關頁

- [self_attention](self_attention.md)
- [feed_forward_layer](feed_forward_layer.md)
- [embedding](embedding.md)
- [softmax_and_temperature](softmax_and_temperature.md)
