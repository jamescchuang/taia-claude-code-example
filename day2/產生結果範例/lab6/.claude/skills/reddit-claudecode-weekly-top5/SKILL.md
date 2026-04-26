---
name: reddit-claudecode-weekly-top5
description: 列出 r/ClaudeCode 本週留言數最多的 5 篇貼文，並以 Markdown 表格呈現。當使用者詢問「Claude Code 本週熱門討論」、「r/claudecode 本週留言最多」、「這週 Claude Code 社群在吵什麼」等相關問題時觸發。
---

# r/ClaudeCode 本週留言數 Top 5

此 skill 會呼叫本專案設定的 `reddit` MCP server（見 `day2/lab5/.mcp.json`），抓取 r/ClaudeCode 本週 top 貼文，依 `num_comments` 重新排序後取前 5 名，並輸出 Markdown 表格。

## 觸發時機

- 使用者想知道 r/ClaudeCode 本週討論最熱烈（留言最多）的貼文
- 使用者提到「claudecode 這週」、「本週熱門討論」、「社群在聊什麼」且上下文跟 Claude Code 有關

## 前置條件

- `day2/lab5/.mcp.json` 已設定好 `reddit` MCP server（`reddit-mcp` 專案）
- 在 `day2/lab5/` 目錄下啟動 Claude Code，`reddit` server 會被載入
- 可用工具：`mcp__reddit__get_subreddit_posts`（以及其他 5 個 reddit 工具）

## 執行步驟

1. 呼叫 `mcp__reddit__get_subreddit_posts`：
   - `subreddit`: `claudecode`
   - `sort`: `top`
   - `time`: `week`
   - `limit`: `100`
2. 收到結果後，於本機將清單依 `num_comments` 由大到小排序，取前 5 名。
   - 注意：Reddit 的 `top` 是按「分數」排序，不是按「留言數」。必須在客戶端重排。
3. 輸出一張 Markdown 表格，欄位固定如下（不要增減）：

   | # | 留言數 | 分數 | 標題 | 作者 |

   - 「標題」欄位需用 Markdown 連結：`[title](permalink)`
   - 數字加千分位逗號（例如 `1,901`）
   - 標題保留原文語言，不要翻譯
4. 表格下方加一行註記，說明「抓 top/week 前 100 篇再依留言數重排」。

## 錯誤處理

- 若 `reddit` MCP server 未連線，提示使用者：在 `day2/lab5/` 重啟 Claude Code，或檢查 `.mcp.json`。
- 若 Reddit 回 403：通常是 UA 被擋，提醒使用者檢查 `reddit-mcp/src/reddit_mcp/reddit.py` 的 `UA` 常數是否被改動。

## 不要做的事

- 不要自己用 WebFetch 去抓 reddit.com。一律走 `reddit` MCP server。
- 不要翻譯標題。
- 不要額外加欄位（如摘要、時間戳）除非使用者明確要求。
