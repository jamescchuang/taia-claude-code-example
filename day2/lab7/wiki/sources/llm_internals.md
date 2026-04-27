---
title: 一堂課看懂語言模型內部運作
type: source
tags: [李宏毅, Transformer, Attention, Interpretability]
created: 2026-04-27
updated: 2026-04-27
raw: ../../raw/LLMunderstand.pdf
pages: 68
author: 李宏毅
---

# 一堂課看懂語言模型內部運作

第二講，鏡頭從「使用者」轉到「模型內部」。觀察一個**已訓練好**的模型，從輸入 prompt 到輸出下一個 token 中間每一層在做什麼。

## 主要章節

1. **整體流水線**（p6–p11）：Tokenization → [Embedding](../concepts/embedding.md) Table → Layer 1 … Layer L（每層含 [Self-Attention](../concepts/self_attention.md) + [Feed-Forward](../concepts/feed_forward_layer.md)）→ Unembedding (LM head)。
2. **從 logit 到機率**（p13–p16）：[softmax 與 temperature](../concepts/softmax_and_temperature.md) 控制隨機性；首尾呼應，最後一層的 representation 會被點積回 embedding table。
3. **Embedding 的幾何意義**（p18–p25）：相似 token 距離近；特定方向有特定含意（如「中英翻譯方向」、「冷↔熱方向」）；經過 layers 的 contextualized embedding 已經編碼了句法與世界知識（如國家對應首都）。
4. **Activation Engineering**（p26–p36）：直接修改某一層的 hidden state — 例如抽取「拒絕成分」做 [Refusal Vector](../concepts/activation_engineering.md)，把它加進無害 prompt 會讓模型拒答；減掉則能繞過拒絕。Sycophancy Vector 同理。
5. **Logit Lens 與 Patchscopes**（p37–p43）：把每一層的 representation 都拿去過 LM head，可看到「模型每層的暫定答案」如何演化；[interpretability 工具](../concepts/activation_engineering.md)。
6. **Self-Attention 的細節**（p45–p61）：query/key/value 三組投影、dot product → softmax 得 attention weight、加權求和 value、Multi-head 找不同面向、Causal Mask、Positional Embedding。([self_attention](../concepts/self_attention.md))
7. **Feed-Forward Layer**（p62–p66）：兩層線性 + ReLU；可視為 Key-Value Memories（引用 Geva et al. 2020）。

## 核心 takeaway

- LLM 不是黑盒。Embedding 空間有方向性、可加減；hidden state 可被探針也可被「手術」。
- **Transformer 的特殊之處不是「發明 Attention」，而是「拿掉 Attention 以外的東西」**（p46）。
- Attention 計算量隨輸入平方成長 → context 長度有上限 → 對應到第三講的 [Context Rot](../concepts/context_rot.md)。
- Logit Lens / Patchscopes 是窺探模型「思考過程」的廉價工具，不需要重新訓練。

## 延伸閱讀（投影片內引用）

- Hewitt & Manning 2019 — A Structural Probe for Finding Syntax
- Vaswani et al. 2017 — Attention Is All You Need
- Geva et al. 2020 — Transformer Feed-Forward Layers Are Key-Value Memories
- arXiv 2406.11717 — Refusal Vector
- arXiv 2402.10588 — Do Llamas Work in English?（多語模型的 latent language）
- arXiv 2401.06102 — Patchscopes
