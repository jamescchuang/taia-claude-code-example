---
title: AI Agent
type: concept
tags: [Agent, 核心]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/context_engineering.md]
---

# AI Agent

> **自主決定步驟、靈活調整計畫的 LLM 應用。**

## Agentic Workflow vs AI Agent（[context_engineering](../sources/context_engineering.md) p42）

| | Agentic Workflow | AI Agent |
|---|---|---|
| 步驟 | 固定 SOP | 自主決定 |
| 範例 | 批改作業（檢查→評分→複核） | 解開放性研究問題 |
| 一問一答 vs 多輪自主行動 | 偏一問一答 | 多輪 |

兩者都用 LLM，差別在「誰決定下一步」。

## Agent 的三件事（[context_engineering](../sources/context_engineering.md) p43）

```
        Goal
         │
         ▼
   ┌──────────┐    Action     ┌──────┐
   │          │ ────────────▶ │ 工具 │ / 使用者
   │   LLM    │ ◀──────────── │      │
   └──────────┘  Observation  └──────┘
```

近乎無限的可能 + 用人類語言提供回饋。

## 從 LLM 角度看 Agent

[context_engineering](../sources/context_engineering.md) p45：

```
sys_prompt | obs_1 | act_1 | obs_2 | act_2 | obs_3 | act_3 | …
```

**還是文字接龍**（[token_and_autoregressive](token_and_autoregressive.md)）。Agent 的能力**完全倚靠語言模型既有的能力**，沒有什麼新東西。

## 挑戰：輸入過長

跑到 obs_9999 怎麼辦？（[context_engineering](../sources/context_engineering.md) p46）

- 物理上：Attention 計算量平方成長（[self_attention](self_attention.md)）。
- 認知上：[Context Rot](context_rot.md)、Lost in the Middle。

→ 必須做 [Context Engineering](context_engineering.md)，採用 [Select](rag.md) / [Compress](compression.md) / [Multi-Agent](multi_agent.md)。

## 構成元件

| 元件 | 對應頁 |
|------|--------|
| 思考過程 | [reasoning](reasoning.md) |
| 呼叫工具 | [tool_use](tool_use.md) |
| 記得歷史 | [memory](memory.md) |
| 取資料 | [rag](rag.md) |

## 範例：Gemini CLI

[context_engineering](../sources/context_engineering.md) p44：[github.com/google-gemini/gemini-cli](https://github.com/google-gemini/gemini-cli)。命令列形式的 coding agent，本知識庫使用的 Claude Code 是同類型產品。

## 相關頁

- [context_engineering](context_engineering.md)
- [multi_agent](multi_agent.md)
- [tool_use](tool_use.md)
- [reasoning](reasoning.md)
