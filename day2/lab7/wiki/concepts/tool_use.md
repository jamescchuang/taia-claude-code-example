---
title: Tool Use 與 Computer Use
type: concept
tags: [ToolUse, Agent, ComputerUse]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/context_engineering.md]
---

# Tool Use 與 Computer Use

讓 LLM 在生成過程中「呼叫外部工具」並接收結果，再繼續接龍。

## 通用機制（[context_engineering](../sources/context_engineering.md) p31–p34）

System prompt 告訴模型可用的工具與呼叫格式：

```
如果遇到根據你的知識無法回答的問題，使用工具。
把指令放在 <tool> 和 </tool> 中間，工具輸出會在 <output> 和 </output> 中間。
可用工具：
  Temperature(location, time)
  Search(query)
  ...
```

**關鍵理解**：模型輸出 `<tool>...</tool>` 只是一串文字，**模型本身呼叫不到任何東西**。是執行框架（agent runtime）攔截這段字串、實際執行、把結果作為新 token 餵回模型，模型再繼續接龍。

## 流程

```
Q → LLM → "<tool>Temperature('高雄', '2025.03.10 14:00')</tool>"
       ← runtime 執行 → "<output>32度</output>"
LLM ← Q + tool_call + output → 「2025/3/10 高雄氣溫 32 度」
```

工具呼叫文字通常**不會呈現給使用者**，使用者只看到最終答案。

## Tool RAG

當工具數量大（數百個），全塞 system prompt 不切實際 → 用 [RAG](rag.md) 動態挑出與當前任務相關的工具說明（[context_engineering](../sources/context_engineering.md) p59）。

## Computer Use

Tool Use 的極致：把「鍵盤、滑鼠、螢幕截圖」當成工具（[context_engineering](../sources/context_engineering.md) p35–p37）。Anthropic Claude、OpenAI ChatGPT Agent 已商品化。

> 人類能用電腦做的事情，語言模型也能做。

## 與其他 context 來源的對照

Tool Use 的**輸出**是動態加入 context 的一種來源；如同 [RAG](rag.md) 是檢索式來源、[reasoning](reasoning.md) 是模型自產來源。所有來源最終都會被 [Context Engineering](context_engineering.md) 納入管理。

## 相關頁

- [ai_agent](ai_agent.md) — Tool Use 是 Agent 的基本構件
- [rag](rag.md)
- [compression](compression.md) — Computer Use 會產生大量瑣碎中間 obs，需要壓縮
