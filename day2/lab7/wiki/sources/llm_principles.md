---
title: 一堂課搞懂生成式人工智慧的原理
type: source
tags: [李宏毅, 入門, 生成式AI, 原理]
created: 2026-04-27
updated: 2026-04-27
raw: ../../raw/LLM.pdf
pages: 38
author: 李宏毅
---

# 一堂課搞懂生成式人工智慧的原理

第一講，定位是「使用者視角的 LLM 入門」：解釋 ChatGPT/Gemini/Claude 在做什麼、為什麼會這樣表現、為什麼會出錯。

## 主要章節

1. **語言模型即文字接龍**（p5–p10）：模型以 token 為單位輸出機率分佈，根據分佈擲骰子產生下一個 token，遞迴到 [END]。
2. **參數與學習**（p11–p13）：模型是有大量參數的函式 `f(x)`；學習資料來自三層 — pre-train（網路資料）→ fine-tune（標註資料）→ RLHF（使用者回饋）。
3. **多輪對話的真相**（p14–p20）：所謂「記得對話」其實是把整段歷史塞回 prompt；幻覺、為什麼需要 system prompt、為什麼需要 [Context Engineering](../concepts/context_engineering.md)。
4. **生成圖片與聲音**（p21–p28）：把影像/聲音切 token，沿用同樣的文字接龍框架（[Autoregressive Generation](../concepts/token_and_autoregressive.md)）。
5. **生成式 AI 的通用原理**（p29–p33）：把無窮可能拆成有限選擇、依固定順序逐一產生的分類問題。
6. **開源 vs 閉源**（p34–p38）：以 LLaMA / Gemma / Mistral 與 Hugging Face 為例。

## 核心 takeaway

- **文字接龍**就是 LLM 的全部 — 無論你看到的是聊天、翻譯、寫程式，背後都是同一個動作。([token_and_autoregressive](../concepts/token_and_autoregressive.md))
- 模型回答「不同」是因為從機率分佈抽樣；回答「錯」是因為機率最高 ≠ 事實正確 → [幻覺](../concepts/hallucination.md)。
- 多輪對話沒有魔法，只是 [Chat Template](../concepts/system_prompt.md) 把歷史拼回去；模型不會主動記憶。
- 「現在是人類的責任確保輸入資訊足夠」就是 [Context Engineering](../concepts/context_engineering.md) 的引子，第三講會深講。

## 延伸到其他頁面

- 內部運作細節 → [LLM 內部運作](llm_internals.md)
- 訓練流程 → [training_pipeline](../concepts/training_pipeline.md)
- 為什麼會幻覺 → [hallucination](../concepts/hallucination.md)
- Token 概念 → [token_and_autoregressive](../concepts/token_and_autoregressive.md)
