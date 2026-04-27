---
title: 一堂課搞懂 Context Engineering 的概念
type: source
tags: [李宏毅, ContextEngineering, Agent, Prompt]
created: 2026-04-27
updated: 2026-04-27
raw: ../../raw/Agent.pdf
pages: 77
author: 李宏毅
---

# 一堂課搞懂 Context Engineering 的概念

第三講，把鏡頭再拉回使用者，但討論的是「LLM Agent 時代怎麼幫模型準備合適的輸入」。三個大段：context 內容、為何 Agent 時代尤其重要、基本方法。

## 主要章節

1. **Prompt Engineering vs Context Engineering**（p3–p10）：兩者概念相同，但前者偏「輸入格式 / 神奇咒語」，後者偏「自動化管理輸入」。神奇咒語（如 "Let's think step by step"）越新模型越不靈。([prompt_engineering](../concepts/prompt_engineering.md), [context_engineering](../concepts/context_engineering.md))
2. **Context 裡有什麼**（p12–p40）：
   - [User Prompt](../concepts/prompt_engineering.md)：任務、指引、條件、風格、範例
   - [System Prompt](../concepts/system_prompt.md)（Claude Opus 4.1 的官方版有 2516 字）
   - [Dialogue History](../concepts/memory.md)（短期記憶）
   - [Long-term Memory](../concepts/memory.md)（跨對話記憶）
   - [RAG](../concepts/rag.md) 來自其他資料源的相關資訊
   - [Tool Use / Computer Use](../concepts/tool_use.md)
   - [Reasoning](../concepts/reasoning.md) 自己產生的思考過程
   - **核心目標：避免塞爆 context**
3. **AI Agent 為什麼讓 context 爆炸**（p41–p52）：
   - [AI Agent](../concepts/ai_agent.md) 與 Agentic Workflow 的差別 — 前者自主決定步驟。
   - LLM 視角下 Agent 就是 `sys_prompt | obs_1 | act_1 | obs_2 | act_2 | …` 的不斷接龍。
   - 長 context 不等於「讀懂」：[Lost in the Middle](../concepts/context_rot.md)、Lost in Conversation、Context Rot。
4. **三大基本方法**（p53–p76）：
   - **Select**：[RAG](../concepts/rag.md)（資料 / 工具 / 記憶）+ Reranking
   - **Compress**：[摘要壓縮](../concepts/compression.md)，把細節甩到外存（日後 RAG 回來）
   - **[Multi-Agent](../concepts/multi_agent.md)**：每個子 agent 帶乾淨的 sub-context

## 核心 takeaway

- Context Engineering 的一句話定義：**把需要的放進去，不需要的清出來**。
- AI Agent 與一問一答最大差別是「步驟自主」，因此 context 會越滾越長，必須有主動管理。
- 三招 — Select / Compress / Multi-Agent — 是同一個 trade-off 的三種解法：在「資訊完整」與「context 不爆」之間取捨。
- 聊到 [StreamBench](../concepts/memory.md) 的有趣現象：「叫你不要想白熊，反而特別容易想白熊」— 反例 prompting 會反向強化。

## 延伸閱讀

- Claude 官方 system prompt: https://docs.anthropic.com/en/release-notes/system-prompts
- arXiv 2307.03172 — Lost in the Middle
- research.trychroma.com/context-rot — Context Rot
- arXiv 2304.03442 — Generative Agents（記憶外存的代表作）
- arXiv 2406.08747 — StreamBench
- ChatDev / arXiv 2307.07924 — Multi-Agent 程式開發
