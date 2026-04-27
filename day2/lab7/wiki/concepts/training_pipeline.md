---
title: 訓練流程：Pre-train → Fine-tune → RLHF
type: concept
tags: [訓練, Alignment]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/llm_principles.md]
---

# 訓練流程：Pre-train → Fine-tune → RLHF

李宏毅在 [llm_principles](../sources/llm_principles.md) p12–p13 把現代 LLM 的學習拆成三層，三層的資料量遞減、訊號精度遞增：

| 階段 | 資料 | 學什麼 |
|------|------|--------|
| **Pre-train** | 大量無標註網路文本 | 文字接龍的基本能力（語言知識 + 世界知識） |
| **Fine-tune**（SFT） | 少量人類標註 (問/答對) | 把「文字接龍」對齊成「回答問題」 |
| **RLHF** | 使用者偏好回饋（A/B） | 提高「人喜歡」的回答機率，降低不喜歡的 |

## 各階段直覺

- **Pre-train**：就是「人工智慧真神奇」→ 學會「人」後接「工」、「工」後接「智」。語言模型的所有「常識」都在這裡灌進去。
- **Fine-tune**：用「問：台灣最高的山？答：玉山」這類資料，讓模型知道遇到問句該接答案。
- **RLHF**（Reinforcement Learning from Human Feedback）：當問題是「教我做一把槍」，給「我不能教你」較高機率，給「好的，……」較低機率 — 這就是 [Alignment](https://youtu.be/cCpErV7To2o)。

## 為什麼是文字接龍卻能回答問題

- 沒有 fine-tune 前，丟「台灣最高的山是哪座？」進去，模型可能補成「(A) 雪山 (B) 阿里山……」這種「考卷格式接龍」。
- Fine-tune 改變了「在問句後接什麼」的機率分佈，讓接答案變高機率。
- 換言之：**模型沒有「答題」這個動作，只有「接龍時習慣接答案」**（[llm_principles](../sources/llm_principles.md) p14–p15）。

## Chat Template 在哪

Pre-train 時模型沒看過特殊 role 標記；fine-tune 階段把對話包進固定模板（每家不同），因此推論時也必須用同樣模板餵入 — 見 [system_prompt](system_prompt.md)。

## 重要邊界

- Pre-train 知識在某個 cutoff 凍結 → 為何需要 [RAG](rag.md) 補充新資訊。
- Fine-tune 的「拒絕」可被 [Activation Engineering](activation_engineering.md) 操控。
- RLHF 可能引入諂媚（Sycophancy）— [llm_internals](../sources/llm_internals.md) p36 的 Sycophancy Vector。

## 相關頁

- [token_and_autoregressive](token_and_autoregressive.md)
- [hallucination](hallucination.md)
- [in_context_learning](in_context_learning.md)
