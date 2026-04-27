---
title: Reasoning（模型自產的思考過程）
type: concept
tags: [Reasoning, CoT]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/context_engineering.md]
---

# Reasoning（模型自產的思考過程）

ChatGPT o 系列、DeepSeek R 系列、Gemini Deep Think 等模型，會在輸出最終答案前先**自己產生一段「思考過程」**（[context_engineering](../sources/context_engineering.md) p38）。

## 內容形式

```
我們先看 A 解法 → 驗證一下 → 不對
我們再試 B 解法 → 驗證一下 → 好像對
還可以嘗試 C 解法 → 看起來不好
使用 B 方法給最終答案
```

= 規劃、嘗試、驗證、自我糾錯（腦內小劇場）。

## 與 Chain-of-Thought 的關係

CoT prompting（"Let's think step by step"）是**人為要求**模型寫出步驟；現代 reasoning 模型則是**訓練成預設就這樣做**。把 CoT 從「[Prompt Engineering](prompt_engineering.md) 神奇咒語」內化進模型本體。

## 對 Context 的影響

Reasoning trace 是 [Context Engineering](context_engineering.md) 中**自動長出來**的部分：

- 使用者**選擇不看（甚至不能看）** — 例如 OpenAI o 系列的 reasoning 通常被遮蔽。
- 但 reasoning token **仍佔用 context 預算**，影響後續 attention 與成本。
- 長 reasoning + 大 context → [Context Rot](context_rot.md) 風險加劇。

## 與其他 context 來源的對照

| 來源 | 誰產生 |
|------|--------|
| User Prompt | 使用者 |
| System Prompt | 應用開發者 |
| RAG | 外部資料源 |
| Tool Use | 外部工具 |
| **Reasoning** | **模型自己** |

→ Reasoning 是唯一「context 中由模型自己生成」的部分，這也讓它最難管理。

## 相關頁

- [prompt_engineering](prompt_engineering.md) — CoT 咒語的歷史
- [context_engineering](context_engineering.md)
- [hallucination](hallucination.md) — reasoning 也可能幻覺，且更難察覺
