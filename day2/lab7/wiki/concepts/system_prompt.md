---
title: System Prompt 與 Chat Template
type: concept
tags: [Prompt, SystemPrompt]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/llm_principles.md, ../sources/context_engineering.md]
---

# System Prompt 與 Chat Template

## Chat Template

LLM 看到的不是「使用者問了什麼」，而是經過模板包裝的字串（[llm_principles](../sources/llm_principles.md) p15）。每家模型模板格式不同，常含特殊 role 標記如 `<|user|>`、`<|assistant|>`、`<|system|>`。**用錯模板會嚴重劣化效果**。

模板來自 [training_pipeline](training_pipeline.md) 的 fine-tune 階段。

## System Prompt

系統端注入、使用者通常看不到的提示，每次對話都會用到（[llm_principles](../sources/llm_principles.md) p20）。內容例如：

- 「今天是 2025 年 9 月 6 日」（補時間感知 → 緩解 [hallucination](hallucination.md)）
- 「你叫 OOO」（人格設定）

## 真實規模：Claude Opus 4.1 的 System Prompt

Anthropic 公開的 [system prompt](https://docs.anthropic.com/en/release-notes/system-prompts) 約 **2516 字**（[context_engineering](../sources/context_engineering.md) p22–p23），涵蓋：

- 基本身分與產品資訊（"The assistant is Claude, created by Anthropic"）
- 使用說明與限制（API 文件指引）
- 互動態度與使用者回饋（不滿意提示按 thumbs down）
- 安全與禁止事項（不協助化武/核武）
- 回應風格與格式（never starts with 'good question'）
- 知識與事實性（knowledge cutoff: Jan 2025）
- 自我定位與哲學原則（不主張自己是人類或有意識）
- 錯誤處理與互動細節（被糾正時先思考再承認）

## 在 Context Engineering 中的位置

System prompt 是 [context_engineering](context_engineering.md) 的「最固定」那一層，屬於每次對話都進 context 的高優先資訊。同時也是 [Activation Engineering](activation_engineering.md) 中許多「行為向量」的源頭——RLHF 與 system prompt 共同形塑模型人格。

## 相關頁

- [prompt_engineering](prompt_engineering.md)
- [memory](memory.md)
- [training_pipeline](training_pipeline.md)
