---
title: Context Engineering
type: concept
tags: [Context, Agent, 核心]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/context_engineering.md, ../sources/llm_principles.md]
---

# Context Engineering

> **把需要的放進去，不需要的清出來。** ([context_engineering](../sources/context_engineering.md) p54)

不訓練模型，而是替既有模型**準備合適的輸入**。是 [Prompt Engineering](prompt_engineering.md) 的廣義化：除了人手寫的 prompt，更涵蓋對 dialogue history、memory、外部資料、工具結果、reasoning 軌跡的**自動化管理**。

## Context 包含什麼（[context_engineering](../sources/context_engineering.md) p40）

1. [User Prompt](prompt_engineering.md)（含範例）
2. [System Prompt](system_prompt.md)（人格、行為規則）
3. [Dialogue History](memory.md)（短期記憶）
4. [Long-term Memory](memory.md)
5. [RAG](rag.md) 來自外部資料源的相關資訊
6. [Tool Use](tool_use.md) 的 query 與輸出
7. [Reasoning](reasoning.md) 思考過程

**問題**：全部塞進去 → very long → context 爆炸 + [Context Rot](context_rot.md)。

## 核心目標

避免塞爆 context。把握這個目標時，所有設計決策都會更清晰。

## 三大基本方法（[context_engineering](../sources/context_engineering.md) p55）

| 方法 | 概念 | 細節頁 |
|------|------|--------|
| **Select** | 動態挑選需要的內容 | [rag](rag.md) |
| **Compress** | 摘要、外存、再 RAG 回來 | [compression](compression.md) |
| **Multi-Agent** | 拆任務，每個 sub-agent 帶乾淨 sub-context | [multi_agent](multi_agent.md) |

三者不互斥，常組合使用。

## 為什麼 Agent 時代尤其重要

[ai_agent](ai_agent.md) 自主決定步驟，會不斷產生新的 obs/action 對。沒有主動管理 context，幾步就會超出限制；即使沒超出，也會掉進 [Context Rot](context_rot.md)。

## 它的源頭

- 第一講 [llm_principles](../sources/llm_principles.md) p19 的「暗無天日小房間」 — 模型只看到輸入；確保輸入資訊足夠是「人類的責任」。
- 此即 Context Engineering 的引子。

## 相關頁

- [prompt_engineering](prompt_engineering.md)
- [ai_agent](ai_agent.md)
- [context_rot](context_rot.md)
- [compression](compression.md)
