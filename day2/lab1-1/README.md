# Day2, Lab 1：建立自己的Claude Design

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
