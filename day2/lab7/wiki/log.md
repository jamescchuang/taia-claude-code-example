# Wiki Log

Append-only 時序紀錄。每筆開頭固定 `## [YYYY-MM-DD] <op> | <subject>`，方便 `grep "^## \[" log.md | tail` 查最近動態。

## [2026-04-27] note | 知識庫初始化
- 依 Karpathy LLM Wiki 模式建立資料夾結構與 schema (CLAUDE.md)
- 目前 raw/ 與 wiki/ 皆為空，等待第一筆素材

## [2026-04-27] ingest | 李宏毅 — 一堂課搞懂生成式人工智慧的原理 (LLM.pdf, 38p)
- 來源：sources/llm_principles.md
- 重點：LLM 即文字接龍、訓練三階段（pre-train/fine-tune/RLHF）、幻覺成因、Context Engineering 的引子

## [2026-04-27] ingest | 李宏毅 — 一堂課看懂語言模型內部運作 (LLMunderstand.pdf, 68p)
- 來源：sources/llm_internals.md
- 重點：Transformer 結構、Embedding 幾何、Self-Attention QKV 機制、FFN 即 KV memory、Activation Engineering（Refusal Vector）、Logit Lens / Patchscopes

## [2026-04-27] ingest | 李宏毅 — 一堂課搞懂 Context Engineering 的概念 (Agent.pdf, 77p)
- 來源：sources/context_engineering.md
- 重點：Context 七大組件、AI Agent vs Agentic Workflow、Context Rot 三現象（Lost in Middle/Conversation/Context Rot）、三大方法 Select/Compress/Multi-Agent

## [2026-04-27] synthesis | 李宏毅三講課程地圖
- 頁面：synthesis/lee_curriculum_map.md
- 內容：三講關係圖、概念依賴關係、跨講共有主題對照表

## [2026-04-27] note | ingest 批次完成
- 新建 wiki 頁面總計 25：3 sources + 1 entity + 20 concepts + 1 synthesis
- 概念覆蓋：基礎(6) / Transformer 內部(4) / Prompt-Context 設計(3) / Agent 應用(7)
- index.md 已重建，分四大類別組織
