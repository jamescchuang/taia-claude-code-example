---
title: Multi-Agent
type: concept
tags: [Agent, MultiAgent, ContextEngineering]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/context_engineering.md]
---

# Multi-Agent

把任務拆成多個子 agent，每個 agent 帶**乾淨的 sub-context** 工作，主 agent 只看到子 agent 的「成品回報」。

## 為什麼要拆

[context_engineering](../sources/context_engineering.md) p72：

**Single Agent 路線**：
```
組織出遊 → 規劃行程 → 跟餐廳網頁互動（一堆 obs/act）
                  → 跟旅館網頁互動（一堆 obs/act）
```
→ Context 中塞滿訂位細節，互相干擾。

**Multi-Agent 路線**：
```
Lead ──→ Agent1（去訂餐廳）── 子 context 互動 ──→ 「訂好了」
     ──→ Agent2（去訂旅館）── 子 context 互動 ──→ 「訂好了」
```
→ Lead Context 只有「結論」；每個 sub-agent 的 context 只關心自己的子任務。

## 本質

= **Context 隔離**。是 [Context Engineering](context_engineering.md) 三大招（Select / Compress / Multi-Agent）中最大手筆的一招。可視為「分散式 compress」：壓縮的不是字串，而是「整段子任務」變成「結論一句」。

## 案例

- **ChatDev**（[arXiv 2307.07924](https://arxiv.org/abs/2307.07924)，[github](https://github.com/OpenBMB/ChatDev)）：模擬軟體公司，CEO/CTO/工程師/測試各自為 agent，協作開發程式。
- **撰寫 overview paper**（[context_engineering](../sources/context_engineering.md) p74）：拆研究/整理/寫作。
- LangChain 對 multi-agent 架構的 [benchmark 研究](https://blog.langchain.com/benchmarking-multi-agent-architectures/)（[context_engineering](../sources/context_engineering.md) p76）。

## 設計取捨

- **過度拆分** → 子 agent 之間溝通成本爆增、結論失真。
- **拆得太粗** → 等於沒拆，context 還是會爆。
- 子 agent 間的協議（用什麼格式回報、誰能呼叫誰）需要明確設計。

## 相關頁

- [ai_agent](ai_agent.md)
- [context_engineering](context_engineering.md)
- [compression](compression.md)
- [tool_use](tool_use.md)
