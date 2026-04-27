---
title: Activation Engineering 與 Interpretability 工具
type: concept
tags: [Interpretability, RepresentationEngineering]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/llm_internals.md]
---

# Activation Engineering 與 Interpretability 工具

針對**已訓練好的模型**，直接操作或觀察其中間層 representation，不需重新訓練。投影片把這類技術統稱為 Representation / Activation Engineering / Activation Steering（[llm_internals](../sources/llm_internals.md) p26）。

## 1. Refusal Vector（拒絕向量）

[llm_internals](../sources/llm_internals.md) p27–p35，原始論文 [arXiv 2406.11717](https://arxiv.org/abs/2406.11717)。

- 假設「拒絕成分」出現在第 10 層的 hidden state。
- 收集多筆「會被拒絕」（教做炸藥、寫詐騙信）與「不會被拒絕」（教機器學習、寫詩）的範例。
- 兩組第 10 層 representation 各自取平均，相減 → 得到一個「拒絕方向向量」。
- **加** 到無害輸入的 hidden state → 模型開始拒答。
- **減** 掉 → 模型對有害請求停止拒絕。
- 第幾層才是關鍵層？每層都試一遍找最有效的那一層。

## 2. Sycophancy Vector（諂媚向量）

[llm_internals](../sources/llm_internals.md) p36，Anthropic [scaling-monosemanticity](https://transformer-circuits.pub/2024/scaling-monosemanticity/)。同樣手法可分離出「順著使用者說」的成分。

## 3. Logit Lens

[llm_internals](../sources/llm_internals.md) p37–p39，[arXiv 2001.09309](https://arxiv.org/abs/2001.09309)。

- 對**中間每一層**的 representation 都套上 LM head 做 unembedding。
- 看每一層「目前認為下一個 token 是什麼」。
- 例：給 LLaMA 2 看 `Français: "fleur" - 中文: "`，中間某一層的 logit lens 顯示「花」 — 揭示模型內部以英語為中介語（[arXiv 2402.10588](https://arxiv.org/abs/2402.10588)，*Do Llamas Work in English?*）。

## 4. Patchscopes

[llm_internals](../sources/llm_internals.md) p40–p43，[arXiv 2401.06102](https://arxiv.org/pdf/2401.06102)。

- 把 prompt A 在某層的 representation **移植**到 prompt B 對應位置。
- 用「請簡單介紹 [X]」這類 probe prompt，可以「採訪」模型對某 representation 的理解 — 即便該 representation 來自完全不同的 context。
- 比 logit lens 更靈活的觀察工具。

## 為什麼重要

- 證明 LLM 不是黑盒：**特定行為對應特定方向**（拒絕、諂媚、語言切換…）。
- 安全與對齊研究的重要工具：可定位、可操控。
- 對應 [training_pipeline](training_pipeline.md) 的 RLHF 階段——這些「行為向量」很多是 RLHF 注入的。

## 相關頁

- [embedding](embedding.md)
- [transformer_architecture](transformer_architecture.md)
- [feed_forward_layer](feed_forward_layer.md)
