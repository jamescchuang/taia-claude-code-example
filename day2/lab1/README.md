# Lab 1：建立自己的Claude Design

## 知識點

| 功能名稱 | 一句話簡介 |
| --- | --- |
| 系統提示詞 (System Prompt) | 在對話開始前定義 AI 的角色、行為準則與工作流程，是塑造 AI 表現的核心設定。 |


## 簡介

本 Lab 以近期受關注的 **Claude Design** 為起點，帶領學員理解其背後外流的 **系統提示詞（System Prompt）**，並親手以 Claude Code 建立屬於自己的設計系統：

- **認識系統提示詞**：說明 System Prompt 如何定義 AI 的角色、規範與工作流，是 Claude Design 之所以能扮演「資深設計師」的關鍵。
- **解析 Claude Design 提示詞**：拆解其「理解需求 → 蒐集素材 → 產出 HTML 設計稿 → 驗證交付」的完整工作流程。
- **動手實作**：以「B2B 法遵科技新創」為品牌情境，透過提示詞要求 Claude Code 產出包含色彩、Typography、間距、元件等的完整設計系統，並呼叫 `Create design system` Skill 確保產出符合標準結構。

完成本 Lab 後，學員將理解系統提示詞與 Skill 在塑造 AI 行為上的力量，並能仿效 Claude Design 的模式打造自己的領域代理人。

## 最近的新創殺手：Claude Design

![source: https://inews.gtimg.com/om_bt/O9U_DO7YVV1c23UYbwzLZh5ifOx3ZWpQKfD1hXTfuYdecAA/641](image.png)

Claude Design 網址：[https://claude.ai/design](https://claude.ai/design)

## 網傳外流的 Claude Design 系統提示詞

### 什麼是系統提示詞

系統提示詞（System Prompt）是給 AI 模型的背景指示，用來定義 AI 應如何行為、思考和回應。它是在實際對話開始之前就被設定的「規則集」或「角色定義」。

1. 定義 AI 的角色和身份
2. 設定行為準則
3. 提供上下文和範圍

### 這份系統提示詞包含的重點

> 是給 AI 設計代理人（Design Agent）使用的系統指示（System Prompt）。它把 AI 的角色定位為「一位以 HTML 為工具、與使用者（管理者）協作的資深設計師」，並規範了從「理解需求 → 蒐集設計素材 → 產出 HTML 設計稿 → 驗證交付」的完整工作流程與細節要求。

### 完整的系統提示詞

[](design_guidelines.md)

## 試試看：用 Claude Code 生成設計稿

```
我們是一個 B2B 法遵科技新創，品牌關鍵字：嚴謹、可信、不冰冷。
  請幫我建立一份基礎設計系統，包含：
  - 色彩：Primary / Secondary / Neutral / Semantic（成功、警告、錯誤、資訊）各含 9 階
  - Typography：Display / Heading 1-3 / Body / Caption / Code
  - 間距與圓角 token
  - 基礎元件：Button（4 種 variant）、Input、Card、Badge、Modal

  請呼叫「Create design system」技能以取得標準結構。
  每一組都 register 到對應的 group（Colors/Type/Spacing/Components）。
```

---

## 參考資料

- https://github.com/elder-plinius/CL4R1T4S/blob/main/ANTHROPIC/Claude-Design-Sys-Prompt.txt

- https://gist.github.com/hqman/f46d5479a5b663c282c94faa8be866de

---

## 免責聲明

本文件及所有相關程式碼、圖片、操作步驟均為**示範用途**，僅供教學與學習參考。

- 本範例不保證適用於正式生產環境，使用者應自行評估風險。
- 所有內容均以「現狀」提供，不附帶任何明示或暗示的保證。
- 引用外部之資訊，版權屬原著作人所有。
