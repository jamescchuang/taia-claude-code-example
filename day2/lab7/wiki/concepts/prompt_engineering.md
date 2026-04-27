---
title: Prompt Engineering
type: concept
tags: [Prompt, UserPrompt]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/context_engineering.md]
---

# Prompt Engineering

關注**輸入格式**與**神奇咒語**這類細節，藉以提升 LLM 表現。是 [Context Engineering](context_engineering.md) 的子集（兩者概念相同，關注重點不同）。

## User Prompt 結構（[context_engineering](../sources/context_engineering.md) p13）

李宏毅推薦的好 prompt 結構：

| 元素 | 範例 |
|------|------|
| 任務說明 | 「寫一封信跟老師說 meeting 要請假」 |
| 詳細指引（optional） | 「先道歉、說明遲到理由（身體不適）、最後說會再找時間更新進度」 |
| 額外條件 | 「100 字以內」 |
| 輸出風格 | 「非常嚴肅」 |
| 範例（few-shot） | 給幾個輸入/輸出對 |

提醒：**語言模型不會讀心術**，所有前提都要寫出來。

## 給範例 = In-context Learning

少量範例就能讓模型模仿格式或推理風格，這是著名的 [In-context Learning](in_context_learning.md)（GPT-3 論文 [arXiv 2005.14165](https://arxiv.org/abs/2005.14165)）。

## 神奇咒語（Magic Spells）

歷史上有效但越新模型越不靈的招數（[context_engineering](../sources/context_engineering.md) p6–p9）：

- 「Let's think step by step」（Chain-of-Thought）
- 「我會給你 100 美金」、「這對我母親很重要」
- 「請給最長的回答」

GPT-3.5 解數學應用題：
- 2023/6 舊版：沒咒語 72%、加咒語 88%
- 2024/2 新版：沒咒語 85%、加咒語 89%

→ **模型內化了基本提示技巧**，咒語的邊際效益遞減。李宏毅評：「模型應該要隨時使出全力，怎麼可以要求思考才思考……」

## 與 Context Engineering 的差別

[context_engineering](../sources/context_engineering.md) p5、p10：

- **Prompt Engineering**：人為手工調整輸入字串。
- **Context Engineering**：自動化管理整個 context（用 LLM 自己挑/壓縮/路由）。

兩者交集大，常被混用；但 Agent 時代，後者是必備。

## 相關頁

- [context_engineering](context_engineering.md)
- [in_context_learning](in_context_learning.md)
- [system_prompt](system_prompt.md)
