---
title: Context Compression（壓縮 Context）
type: concept
tags: [Context, Compression]
created: 2026-04-27
updated: 2026-04-27
sources: [../sources/context_engineering.md]
---

# Context Compression（壓縮 Context）

[Context Engineering](context_engineering.md) 三大招中的「Compress」（[context_engineering](../sources/context_engineering.md) p67–p70）。

## 核心動作

把舊的 obs/act 對摘要成一段短結論，再放回 context：

```
舊：obs_100, act_100, obs_101, act_101, …, obs_102
新：history_summary, obs_102
```

## Computer Use 的典型場景

[context_engineering](../sources/context_engineering.md) p69，引用 Anthropic 的 [summarization-for-monitoring](https://alignment.anthropic.com/2025/summarization-for-monitoring/)：

```
原始：移動滑鼠到 [34, 78] → 點擊 → 彈出廣告 → 按 x → 移動到 [550, 65] → ...
摘要：A 餐廳訂位成功，9/19 下午 6:00，10 人。
```

訂完位後，Context 不需要訂位的詳細過程。**摘要就是一種對細節的勇敢遺忘**。

## 與 RAG 的合作

[context_engineering](../sources/context_engineering.md) p70：壓縮後的細節**不是丟掉**，而是放進可長期儲存的空間（檔案/資料庫），日後**用 [RAG](rag.md) 撈回**。

```
…… 詳細內容請開啟 C:\...\那年夏天的美好回憶.txt
```

→ Compression + Memory RAG 是同一個工作流的兩面。

## 與 Multi-Agent 的關係

[Multi-Agent](multi_agent.md) 也可以視為「結構化壓縮」：把整段子任務壓縮成一個 sub-agent 的回報語句。

```
Sub-context（細節爆炸） ──壓縮成一句──▶ Lead context
```

## 風險

[context_engineering](../sources/context_engineering.md) p68：「遙遠的記憶就逐漸隨風而逝」。壓縮過度會丟掉關鍵細節；摘要時的失真本身也是一種幻覺風險（[hallucination](hallucination.md)）。

## 何時觸發

實務常見策略：
- Context token 接近模型上限 → 自動壓縮較舊段落
- 某個子任務完成 → 把該任務的中間 obs/act 壓成結論
- 階段切換（如做完規劃進入執行）→ 整段壓縮

## 相關頁

- [context_engineering](context_engineering.md)
- [memory](memory.md)
- [multi_agent](multi_agent.md)
- [context_rot](context_rot.md)
