# Lab 4 "Rules"：在Claude Code中，執行程式碼安全性檢查

## 知識點

- 記憶
- Skill
- Rules

## Project CodeGuard

**Project CodeGuard** 是由 **Coalition for Secure AI (CoSAI)** 所開發的框架，目的是將安全最佳實務整合進 AI 編碼代理（AI Coding Agent）的工作流程中。

隨著 AI 程式碼生成工具普及，許多常見的安全漏洞也隨之出現，例如：

- 輸入驗證不足
- 硬編碼（Hardcoded）密碼與機密資訊
- 使用弱加密演算法
- 缺少身分驗證檢查

CodeGuard 即是為了解決這些問題而生，協助開發者與 AI 助理一同產出更安全的程式碼。

## 用 Project CodeGuard 提供的 Skill 檢查程式碼是否安全

### 1. 下載並複製 Project CodeGuard 到專案目錄中

### 2. 執行 Skill，或是用自然語言，輸入提示詞

```
掃描專案程式碼，並將掃描結果儲存到 report.md
```
或
```
/security-review
```

![alt text](image-1.png)



---

## 免責聲明

本文件及所有相關程式碼、圖片、操作步驟均為**示範用途**，僅供教學與學習參考。

- 本範例不保證適用於正式生產環境，使用者應自行評估風險。
- 所有內容均以「現狀」提供，不附帶任何明示或暗示的保證。
- 引用外部之資訊，版權屬原著作人所有。
