---
title: Memory（Dialogue History、Long-term Memory）
type: concept
tags: [Memory, Context]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/llm_principles.md, ../sources/context_engineering.md]
---

# Memory（Dialogue History、Long-term Memory）

## Dialogue History（短期記憶）

LLM 本身**不會記憶**。所謂「記得對話」其實是把整段歷史塞回 prompt（[llm_principles](../sources/llm_principles.md) p17）：

```
Q1 → A1
Q1 + A1 + Q2 → A2
Q1 + A1 + Q2 + A2 + Q3 → A3
```

對話越長，輸入越長 — 與 [Context Rot](context_rot.md) 直接相關。

> 「以上對話並沒有訓練模型」（[context_engineering](../sources/context_engineering.md) p24）：對話歷史**不會更新模型參數**，新對話開了就消失。

## Long-term Memory（長期記憶）

[context_engineering](../sources/context_engineering.md) p25–p27：2024 年 9 月後 ChatGPT 開始有跨對話記憶——這不是訓練，而是**外存**機制。

```
重要事實 → Long-term Memory store
        ← 下次對話時用 RAG 取回相關片段 → 拼進 context
```

本質是 **Memory RAG**（[rag](rag.md)）。

## Generative Agents（[context_engineering](../sources/context_engineering.md) p61–p62）

[arXiv 2304.03442](https://arxiv.org/abs/2304.03442)：Stanford 的小鎮模擬。每個 agent 可能跑數萬步，全部歷史塞 context 不可行 → 把細節**寫到外部**儲存，需要時才用 RAG 撈回相關片段。架構雛形：observation → reflection → memory store → retrieval。

## StreamBench：記憶選取的反直覺現象

[arXiv 2406.08747](https://arxiv.org/abs/2406.08747)（[context_engineering](../sources/context_engineering.md) p63–p66）：在連續 1000 題 streaming 任務中，根據過去答對/答錯的紀錄調整策略。

> **叫你不要想白熊，反而特別容易想白熊。**

把「過去答錯的反例」放進 context 反而會讓模型重蹈覆轍。→ 記憶該記什麼、怎麼餵，本身就是個設計問題。

## 三種「記憶」對照表

| 種類 | 在哪 | 何時取用 |
|------|------|---------|
| Dialogue History | 當前 context | 永遠在 |
| Long-term Memory | 外部儲存 | 下次對話用 RAG 撈 |
| 模型參數知識 | 權重 | 永遠在但無法即時更新 |

第三種對應到 [training_pipeline](training_pipeline.md) 的 pre-train 階段；前兩種屬於 [Context Engineering](context_engineering.md) 的範疇。

## 相關頁

- [context_engineering](context_engineering.md)
- [rag](rag.md)
- [compression](compression.md) — 壓縮後的歷史也可外存
- [context_rot](context_rot.md)
