# Project CodeGuard 使用者指南

## 專案簡介

**Project CodeGuard** 是由 **Coalition for Secure AI (CoSAI)** 所開發的框架，目的是將安全最佳實務整合進 AI 編碼代理（AI Coding Agent）的工作流程中。

隨著 AI 程式碼生成工具普及，許多常見的安全漏洞也隨之出現，例如：

- 輸入驗證不足
- 硬編碼（Hardcoded）密碼與機密資訊
- 使用弱加密演算法
- 缺少身分驗證檢查

CodeGuard 即是為了解決這些問題而生，協助開發者與 AI 助理一同產出更安全的程式碼。

## 主要特色

CodeGuard 涵蓋完整開發生命週期的三個階段：

| 階段 | 功能說明 |
| --- | --- |
| **生成前（Pre-generation）** | 在規劃階段引導 AI 模型採用安全的設計模式 |
| **生成中（During generation）** | 在程式碼撰寫過程中即時阻止安全問題發生 |
| **生成後（Post-generation）** | 透過整合的規則進行程式碼審查 |

## 涵蓋的安全領域

CodeGuard 針對八大安全領域提供指引：

1. 密碼學（Cryptography）
2. 輸入驗證（Input Validation）
3. 身分驗證（Authentication）
4. 授權（Authorization）
5. 供應鏈安全（Supply Chain Security）
6. 雲端安全（Cloud Security）
7. 平台安全（Platform Security）
8. 資料保護（Data Protection）

## 技術實作方式

CodeGuard 透過四個步驟運作：

1. **撰寫內容**：以統一的 Markdown 格式撰寫安全技能（Skills）與規則（Rules）
2. **格式轉換**：透過轉換工具，將素材適配到不同的 AI 編碼助理
3. **自動化發佈**：將所有內容打包為可下載的發行檔
4. **套用指引**：AI 助理在實際開發工作中自動套用這些安全指引

此外，專案還提供 **MCP Server**，可進行組織層級的集中部署，讓團隊將所有開發者的 AI 助理連接到單一受管實例，便於統一管理與更新。

## 開始使用

使用者可以依照以下步驟開始使用：

1. 前往專案的 **Releases 頁面** 下載安全技能與規則。
2. 將這些檔案整合進自己的專案中。
3. 使用已嵌入安全指引的 AI 助理進行開發工作。

## 參考資源

- 專案 GitHub：<https://github.com/cosai-oasis/project-codeguard>
- 維護單位：Coalition for Secure AI (CoSAI)
