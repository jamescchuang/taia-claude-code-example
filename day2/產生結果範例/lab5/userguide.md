# eliasbiondo/reddit-mcp-server 使用指南

> 一個零設定（zero-config）的 Reddit MCP Server，讓 Claude、Cursor 等 MCP 客戶端可以直接讀取 Reddit 貼文、留言、使用者資料，**不需要 API key、不需要 OAuth、不需要瀏覽器**。

- 專案網址：<https://github.com/eliasbiondo/reddit-mcp-server>
- 授權：MIT
- 作者：eliasbiondo
- 語言：Python（搭配 `uv` 套件管理工具）

---

## 1. 它能做什麼

此 MCP server 以**網頁抓取**（非 Reddit 官方 API）方式取得 Reddit 公開資料，並透過 MCP 協定把下列 6 個工具暴露給 AI 客戶端：

| 工具名稱 | 用途 | 主要參數 |
|---|---|---|
| `search` | 搜尋整個 Reddit | `query`、`limit`、`sort`（relevance / hot / top / new / comments） |
| `search_subreddit` | 在指定 subreddit 內搜尋 | `subreddit`、`query`、`limit`、`sort` |
| `get_subreddit_posts` | 列出 subreddit 的貼文清單 | `subreddit`、`limit`、`category`（hot / top / new / rising）、`time_filter` |
| `get_post` | 取得單篇貼文與完整留言樹 | `permalink` |
| `get_user` | 取得使用者的公開活動 | `username`、`limit` |
| `get_user_posts` | 列出使用者的歷次發文 | `username`、`limit`、`category`、`time_filter`（hour / day / week / month / year / all） |

> **小提醒**：`sort=top` 是依「分數（upvote）」排序，不是依「留言數」。若要找「留言最多」的貼文，需在客戶端自行重排。

---

## 2. 安裝與啟動

### 2.1 系統需求

- Python 3.10 以上
- [`uv`](https://docs.astral.sh/uv/) 套件管理工具  
  安裝方式：`curl -LsSf https://astral.sh/uv/install.sh | sh`

### 2.2 方法一：uvx 一行啟動（推薦）

不需要 clone 專案，`uvx` 會自動下載並執行：

```bash
uvx reddit-no-auth-mcp-server
```

### 2.3 方法二：從原始碼啟動

適合想要修改程式碼或看內部實作的使用者：

```bash
git clone https://github.com/eliasbiondo/reddit-mcp-server.git
cd reddit-mcp-server
uv sync
uv run reddit-no-auth-mcp-server
```

---

## 3. 在 MCP 客戶端中設定

### 3.1 Claude Desktop

編輯 `claude_desktop_config.json`：

```json
{
  "mcpServers": {
    "reddit": {
      "command": "uvx",
      "args": ["reddit-no-auth-mcp-server"]
    }
  }
}
```

設定檔位置：

- macOS：`~/Library/Application Support/Claude/claude_desktop_config.json`
- Windows：`%APPDATA%\Claude\claude_desktop_config.json`

### 3.2 Claude Code

在專案根目錄建立 `.mcp.json`：

```json
{
  "mcpServers": {
    "reddit": {
      "command": "uvx",
      "args": ["reddit-no-auth-mcp-server"]
    }
  }
}
```

在該目錄下啟動 Claude Code 即會自動載入。

### 3.3 Cursor

編輯 `.cursor/mcp.json`：

```json
{
  "mcpServers": {
    "reddit": {
      "command": "uvx",
      "args": ["reddit-no-auth-mcp-server"]
    }
  }
}
```

### 3.4 從原始碼（任何 MCP 客戶端）

```json
{
  "mcpServers": {
    "reddit": {
      "command": "uv",
      "args": [
        "--directory",
        "/path/to/reddit-mcp-server",
        "run",
        "reddit-no-auth-mcp-server"
      ]
    }
  }
}
```

---

## 4. 傳輸模式（Transport）

| 模式 | 使用情境 |
|---|---|
| `stdio`（預設） | Claude Desktop、Cursor、Claude Code 等本機 MCP 客戶端 |
| `streamable-http` | 把 server 以 HTTP 服務的形式跑在本機或遠端，多個客戶端共用 |

HTTP 模式範例：

```bash
# HTTP 傳輸，預設埠 8000
uv run reddit-no-auth-mcp-server \
  --transport streamable-http \
  --port 8000

# 開啟 DEBUG 日誌
uv run reddit-no-auth-mcp-server \
  --transport streamable-http \
  --port 9000 \
  --log-level DEBUG
```

---

## 5. 環境變數

CLI 參數優先於環境變數。

| 變數 | 預設值 | 用途 |
|---|---|---|
| `REDDIT_TRANSPORT` | `stdio` | MCP 傳輸模式 |
| `REDDIT_HOST` | `127.0.0.1` | HTTP 模式的綁定主機 |
| `REDDIT_PORT` | `8000` | HTTP 模式的監聽埠 |
| `REDDIT_PATH` | `/mcp` | HTTP 模式的路徑 |
| `REDDIT_LOG_LEVEL` | `WARNING` | 日誌等級 |
| `REDDIT_PROXY` | — | HTTP/HTTPS proxy URL |
| `REDDIT_TIMEOUT` | `10.0` | 請求逾時（秒） |
| `REDDIT_THROTTLE_MIN` | `1.0` | 分頁請求之間的最小延遲（秒） |
| `REDDIT_THROTTLE_MAX` | `2.0` | 分頁請求之間的最大延遲（秒） |

---

## 6. 使用範例（Prompt）

設定完成後，可以直接在 Claude / Cursor 中以自然語言觸發：

- 「搜尋 r/claudecode，列出本週留言最多的 5 篇貼文」
- 「把這個 Reddit 貼文的前三則熱門留言翻成中文：<url>」
- 「看看 u/spez 最近發了什麼」
- 「r/LocalLLaMA 今天有哪些熱門討論」

客戶端會自動挑選適當的工具（例如 `get_subreddit_posts`、`get_post`），並把 JSON 結果回傳給模型整理。

---

## 7. 注意事項與限制

1. **沒有官方 API key** —— 所有資料來自公開網頁抓取。若 Reddit 調整網頁結構或加強反爬蟲，可能需要等待專案更新。
2. **Rate limit** —— 預設 `REDDIT_THROTTLE_MIN/MAX` 已放慢分頁請求；若大量連續呼叫仍可能被暫時封鎖（HTTP 403 / 429）。必要時調高延遲或設定 `REDDIT_PROXY`。
3. **只能讀、不能寫** —— 此 server 設計為唯讀，不支援發文、留言、投票等動作。
4. **私有內容** —— 無法存取需要登入才能看的 subreddit 或帳號內容。
5. **授權** —— 專案採 MIT 授權，可自由修改與散布，但不附帶任何保證。

---

## 8. 與自製 MCP Server 的對照

若你有隱私、客製化或學習需求，也可以參考本專案，改用 Reddit 官方的 `.json` 端點自己寫一個。實作範例可見：`day2/lab5/reddit-mcp/`（本倉庫內建的簡化版）。主要差異：

| 面向 | eliasbiondo/reddit-mcp-server | `day2/lab5/reddit-mcp/`（自製） |
|---|---|---|
| 取資料方式 | 網頁抓取（redd 套件） | Reddit `.json` 端點 |
| 工具數 | 6 | 6 |
| 傳輸模式 | stdio + streamable-http | stdio |
| 架構 | 六角架構（Hexagonal） | 扁平（client + server 各一檔） |
| 適合對象 | 直接使用、即插即用 | 教學、示範、二次開發 |

---

## 9. 延伸閱讀

- Model Context Protocol：<https://modelcontextprotocol.io/>
- uv 套件管理工具：<https://docs.astral.sh/uv/>
- Reddit 資料政策：<https://www.redditinc.com/policies/data-api-terms>

---

## 免責聲明

本文件為示範與教學用途，所有資訊彙整自專案公開 README 及實際測試結果。使用前請自行確認 Reddit 的使用條款與該專案授權；作者與本倉庫對因使用本工具造成的任何後果不負責任。
