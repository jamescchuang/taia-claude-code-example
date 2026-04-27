# Wiki Index

本檔為知識庫內容索引，每次 ingest 後由 LLM 更新。讀者（與 LLM）查詢時優先讀此檔，再鑽入相關頁面。

## Entities（實體：人物、組織、產品）

- [李宏毅](entities/hung_yi_lee.md) — 台大教授；本知識庫所有來源的作者

## Concepts（概念、理論、方法）

### 基礎與原理

- [Token 與 Autoregressive Generation（文字接龍）](concepts/token_and_autoregressive.md) — LLM 的最小單位與生成框架
- [Embedding](concepts/embedding.md) — Token / Contextualized Embedding 的幾何意義
- [Softmax 與 Temperature](concepts/softmax_and_temperature.md) — Logit 轉機率、抽樣隨機性控制
- [訓練流程：Pre-train → Fine-tune → RLHF](concepts/training_pipeline.md) — 三階段 alignment
- [In-context Learning](concepts/in_context_learning.md) — 範例驅動的「現場學習」
- [幻覺（Hallucination）](concepts/hallucination.md) — 文字接龍的副作用與緩解

### Transformer 內部

- [Transformer 整體架構](concepts/transformer_architecture.md) — 從 token 到下一個 token 的流水線
- [Self-Attention](concepts/self_attention.md) — QKV、Multi-head、Causal Mask、Positional
- [Feed-Forward Layer](concepts/feed_forward_layer.md) — Key-Value Memory 視角
- [Activation Engineering 與 Interpretability 工具](concepts/activation_engineering.md) — Refusal Vector、Logit Lens、Patchscopes

### Prompt / Context 設計

- [Prompt Engineering](concepts/prompt_engineering.md) — 輸入格式與神奇咒語
- [Context Engineering](concepts/context_engineering.md) — 自動化管理輸入（Select / Compress / Multi-Agent）
- [System Prompt 與 Chat Template](concepts/system_prompt.md) — 持久化指令與模板格式

### Agent 應用層

- [AI Agent](concepts/ai_agent.md) — 自主決定步驟的 LLM 應用
- [Tool Use 與 Computer Use](concepts/tool_use.md) — 呼叫外部能力
- [RAG](concepts/rag.md) — 檢索式擴增（含 Tool RAG、Memory RAG）
- [Memory](concepts/memory.md) — Dialogue History 與 Long-term Memory
- [Reasoning](concepts/reasoning.md) — 模型自產的思考過程
- [Multi-Agent](concepts/multi_agent.md) — Context 隔離與分工
- [Context Compression](concepts/compression.md) — 摘要、外存、再 RAG
- [Context Rot 與長 Context 限制](concepts/context_rot.md) — 為何長 context 不是萬靈丹

## Sources（來源摘要，對應 `raw/` 內的素材）

- [一堂課搞懂生成式人工智慧的原理](sources/llm_principles.md) — 李宏毅，38 頁，[raw/LLM.pdf](../raw/LLM.pdf)
- [一堂課看懂語言模型內部運作](sources/llm_internals.md) — 李宏毅，68 頁，[raw/LLMunderstand.pdf](../raw/LLMunderstand.pdf)
- [一堂課搞懂 Context Engineering 的概念](sources/context_engineering.md) — 李宏毅，77 頁，[raw/Agent.pdf](../raw/Agent.pdf)

## Synthesis（綜合、比較、分析）

- [李宏毅三講課程地圖](synthesis/lee_curriculum_map.md) — 三份投影片的關係、概念依賴圖、共同主題
