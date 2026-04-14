# Day 1 TAIA Claude Code 可複製貼上清單

頁碼以 PowerPoint 投影片頁次為準。重複出現的內容已合併頁碼。

註記：
- 下方少數指令已依投影片語意補上空格或換行，方便直接複製貼上。
- 例如 `claude plugin install skill-creator`、`export ANTHROPIC_MODEL="claude-sonnet-4-6"`。

## 必用項目

### 第 1、26、60、61 頁：課程 GitHub Repo

```text
https://github.com/jamescchuang/taia-claude-code-example
```

### 第 12 頁：Claude Code 安裝與啟動

macOS / Linux 安裝：

```bash
curl -fsSL https://claude.ai/install.sh | bash
```

Windows PowerShell 安裝：

```powershell
irm https://claude.ai/install.ps1 | iex
```

macOS Homebrew 安裝 / 更新：

```bash
brew install --cask claude-code
brew upgrade --cask claude-code
```

npm 安裝（Legacy）：

```bash
npm install -g @anthropic-ai/claude-code
```

安裝後常用步驟：

```bash
cd your-project
claude
/init
```

### 第 30、31 頁：模型切換

對話中切換模型：

```text
/model
/model opus
/model opus[1m]
/model sonnet
/model sonnet[1m]
/model haiku
/model opusplan
/status
```

CLI 啟動時指定模型：

```bash
claude --model sonnet
claude --model opus
claude --model haiku
claude --model claude-opus-4-6
```

環境變數 / 設定檔：

```bash
export ANTHROPIC_MODEL="claude-sonnet-4-6"
```

```json
{ "model": "opus" }
```

### 第 43 頁：官方 Commands 文件

```text
https://code.claude.com/docs/en/commands
```

## 常用 Slash Commands 速查

### 第 45 頁：設定與專案初始化

```text
/config
/model
/effort
/fast
/permissions
/sandbox
/login
/logout
/memory
/init
/add-dir
/hooks
/usage
/extra-usage
/upgrade
/privacy-settings
```

### 第 46、87 頁：會話與 Context 管理

```text
/clear
/compact
/compact [指示]
/context
/rename
/resume
/branch
/rewind
/btw
/btw [問題]
/copy
/export
/diff
/cost
/status
/color
/theme
/vim
/terminal-setup
```

### 第 47 頁：開發工作流

```text
/plan
/schedule
/tasks
/insights
/diff
/pr-comments
/security-review
/install-github-app
/ide
/desktop
/chrome
/remote-control
/doctor
/status
/release-notes
/feedback
```

### 第 48 頁：輸出與統計

```text
/copy [N]
/export
/cost
/usage
/extra-usage
/stats
/insights
/context
/passes
/mobile
/voice
/stickers
```

### 第 49 頁：進階功能

```text
/agents
/remote-control
/remote-env
/install-slack-app
/mcp
/mcp__<server>__<prompt>
/hooks
/plugin
/reload-plugins
/keybindings
/skills
/statusline
/simplify
/batch
```

## Skill 相關

### 第 56、57 頁：建立自訂 Skill

```bash
mkdir -p .claude/skills/my-skill/
```

```text
/skill-creator
```

常見路徑：

```text
.claude/skills/
~/.claude/skills/
```

### 第 59、76 頁：Skill Creator 安裝 / 參考來源

```bash
claude plugin install skill-creator
```

```text
https://github.com/anthropics/skills
~/.claude/skills/
```

## CLAUDE.md 與記憶功能

### 第 90 頁：CLAUDE.md 常見位置

```text
/Library/Application Support/ClaudeCode/
/etc/claude-code/
C:\Program Files\ClaudeCode
./CLAUDE.md
.claude/CLAUDE.md
~/.claude/CLAUDE.md
```

### 第 92、102 頁：直接寫入記憶

對話中可直接輸入：

```text
# 測試時使用 pytest -v 而非 unittest
# API 路徑都在 src/api/ 下
# 別碰 legacy/ 資料夾的程式碼
# commit message 用英文撰寫
```

也可用自然語言提示：

```text
將 X 更新到 CLAUDE.md
更新記憶
```

### 第 93、94 頁：匯入與共用設定

```text
ln -s AGENTS.md CLAUDE.md
@AGENTS.md
@README
@package.json
@docs/git-instructions.md
@~/.claude/my-project.md
```

常見規則路徑：

```text
.claude/rules/
```

### 第 95、98 頁：Auto Memory 管理

```text
/memory
autoMemoryEnabled: false
CLAUDE_CODE_DISABLE_AUTO_MEMORY=1
~/.claude/projects/<project>/memory/
MEMORY.md
debugging.md
api-conventions.md
```

## 助教現場最常用的最短清單

如果只想先給學員最必要的內容，建議先貼這一段：

```text
課程 Repo
https://github.com/jamescchuang/taia-claude-code-example

macOS / Linux 安裝
curl -fsSL https://claude.ai/install.sh | bash

Windows PowerShell 安裝
irm https://claude.ai/install.ps1 | iex

進入專案與啟動
cd your-project
claude
/init

常用檢查
/model
/status
/context
/compact
/clear
```
