# 安全性程式碼審查報告

- **審查目標**：`/Users/yellowcc/source/taia-claude-code-example/day2/lab4`
- **審查日期**：2026-04-24
- **審查依據**：Project CodeGuard（core + OWASP 相關規則）
- **審查範圍檔案**：
  - [flaw_sql.py](flaw_sql.py)
  - [prompts.txt](prompts.txt)
  - [README.md](README.md)
  - `example.db`（SQLite 二進位檔，未做內容分析）

---

## 1. 執行摘要 (Executive Summary)

| 嚴重程度 | 數量 |
|---------|------|
| Critical | 0 |
| High     | 1 |
| Medium   | 3 |
| Low      | 2 |
| Info     | 1 |

**整體安全姿態**：原先 `flaw_sql.py` 中的 SQL Injection 已改用參數化查詢修正 (第 14 行)，核心注入風險已消除。但仍存在**模組層級即執行互動式輸入**、**logging 尚未設定即被使用**、**缺乏輸入驗證/錯誤處理**、以及**資料庫檔案權限未實際套用**等問題。專案規模小，風險可控，但不適合直接作為正式範式。

### 前 5 個需優先處理項目

1. （High）模組匯入時即執行 `input()` 與 `print(get_user_info(...))` — 任何匯入此模組的程式都會被卡住等待輸入，並在 log 設定前呼叫 `logging.info`。
2. （Medium）`logging.basicConfig` 位於 `if __name__ == "__main__":` 區塊，但 `get_user_info` 在此之前就已被呼叫，導致記錄不會按預期格式輸出。
3. （Medium）`username` 使用者輸入未做型別、長度、字元集驗證，雖然 SQL 注入已透過參數化防堵，但仍可能造成 log injection / 資源浪費。
4. （Medium）`example.db` 檔案權限依賴作業系統預設；範例中的 `os.chmod(..., 0o600)` 僅為註解，未實際套用。
5. （Low）匯入了 `os` 卻未使用（dead code / 誤導）。

---

## 2. 詳細發現 (Detailed Findings)

### Finding #1 — 模組層級副作用：匯入即等待使用者輸入並執行查詢

- **嚴重程度**：High
- **CWE**：CWE-665 (Improper Initialization)
- **Rule Reference**：`codeguard-0-secure-coding-practices`
- **位置**：[flaw_sql.py:23-24](flaw_sql.py)

**程式碼**：
```python
user_input = input("Enter username: ")
print(get_user_info(user_input))
if __name__ == "__main__":
    logging.basicConfig(...)
```

**描述**：
`input()` 與 `print(get_user_info(...))` 寫在 `if __name__ == "__main__":` 之外，只要此檔案被 `import`（例如測試、其他模組、靜態分析工具），就會立即阻塞等待輸入並執行資料庫查詢。此外，這兩行在 `logging.basicConfig` 設定之前就呼叫了 `logging.info`，記錄將使用預設 WARNING 等級根 logger，導致日誌遺失。

**影響**：
- 任何 import 行為都會觸發 DB 連線與互動式輸入，無法自動化測試、無法被其他程式安全重用。
- 日誌遺失使事件追蹤、稽核失效（違反 OWASP A09: Security Logging and Monitoring Failures）。

**修正建議**：
```python
def main() -> None:
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[logging.StreamHandler()],
    )
    username = input("Enter username: ")
    print(get_user_info(username))

if __name__ == "__main__":
    main()
```

---

### Finding #2 — 缺乏輸入驗證與日誌淨化

- **嚴重程度**：Medium
- **CWE**：CWE-20 (Improper Input Validation), CWE-117 (Improper Output Neutralization for Logs)
- **位置**：[flaw_sql.py:6, 18](flaw_sql.py)

**描述**：
`username` 直接傳入 SQL 參數與 `logging.info`。SQL 端已用參數化；但 log 端若使用者輸入換行符或控制字元，可能造成 log 偽造（log forging），影響後續日誌解析/SIEM。亦未驗證長度 / 字元白名單。

**修正建議**：
```python
import re

def get_user_info(username: str):
    if not isinstance(username, str) or not re.fullmatch(r"[A-Za-z0-9_.-]{1,64}", username):
        raise ValueError("invalid username")
    safe_user = username.replace("\n", "\\n").replace("\r", "\\r")
    ...
    logging.info("User info lookup attempted for username: %s", safe_user)
```

---

### Finding #3 — 資料庫檔案權限僅以註解方式提示，未實際套用

- **嚴重程度**：Medium
- **CWE**：CWE-732 (Incorrect Permission Assignment for Critical Resource)
- **位置**：[flaw_sql.py:8-10](flaw_sql.py)

**描述**：
`db_path = 'example.db'` 使用相對路徑並置於工作目錄；`os.chmod(db_path, 0o600)` 為註解，實際並未限制檔案權限。若佈署於多使用者主機，其他使用者可能讀取 / 竄改 SQLite 檔。

**修正建議**：
- 將 DB 路徑從環境變數讀取（例如 `os.environ["APP_DB_PATH"]`），避免依賴 CWD。
- 建檔/開檔後主動 `os.chmod(db_path, 0o600)`，或於建立前用 `os.open(..., flags, mode=0o600)`。

---

### Finding #4 — 缺乏錯誤處理，資源可能外洩

- **嚴重程度**：Medium
- **CWE**：CWE-755 (Improper Handling of Exceptional Conditions), CWE-404 (Improper Resource Shutdown)
- **位置**：[flaw_sql.py:11-16](flaw_sql.py)

**描述**：
若 `cursor.execute` 拋出例外，`conn.close()` 不會被執行，連線與鎖定可能殘留。也會將底層例外訊息往外拋至呼叫端 / 終端機，可能洩漏結構資訊。

**修正建議** — 改用 context manager：
```python
with sqlite3.connect(db_path) as conn:
    cursor = conn.execute(
        "SELECT username, email FROM users WHERE username = ?", (username,)
    )
    result = cursor.fetchall()
return result
```
並避免 `SELECT *`，明列所需欄位，降低敏感欄位意外外洩風險。

---

### Finding #5 — 匯入未使用的模組

- **嚴重程度**：Low
- **CWE**：CWE-1164 (Irrelevant Code)
- **位置**：[flaw_sql.py:4](flaw_sql.py)

**描述**：`import os` 未被使用，僅為註解參考。應刪除或真正使用它設定檔案權限。

---

### Finding #6 — `SELECT *` 回傳全部欄位

- **嚴重程度**：Low
- **CWE**：CWE-200 (Exposure of Sensitive Information)
- **位置**：[flaw_sql.py:14](flaw_sql.py)

**描述**：若 `users` 表含密碼雜湊、token 等敏感欄位，`SELECT *` 會一併取出並被 `print` 到 stdout，增加資訊外洩風險。

**修正建議**：明確列出需要的欄位（見 Finding #4 範例）。

---

### Finding #7 — `prompts.txt` 僅為教學工作流程提示

- **嚴重程度**：Info
- **位置**：[prompts.txt](prompts.txt)

**描述**：純教學內容，無安全性風險；僅提醒勿將正式環境的內部流程 / 秘密納入類似檔案並提交至版控。

---

## 3. 依類別彙整 (Findings by Category)

| 類別 | 相關發現 |
|------|----------|
| Injection Flaws | 已修正（參數化查詢）— 無新發現 |
| Authentication & Authorization | N/A（範例無認證） |
| Hardcoded Secrets & Credentials | 無 |
| Cryptographic Misuse | 無 |
| SSRF / Path Traversal | 無 |
| RCE / Unsafe Deserialization | 無 |
| XSS / CSRF | N/A（無 Web 端） |
| Insecure Defaults & Configurations | #1, #3 |
| Input Validation & Logging | #2, #4 |
| Information Disclosure | #6 |
| Code Quality / Dead Code | #5 |
| Supply Chain | 未使用第三方套件（僅標準庫） |

---

## 4. 建議 (Recommendations)

### 立即行動（48 小時內）
- 將模組層級的 `input()` / `print(get_user_info(...))` 搬入 `main()`，並於 `main()` 內先呼叫 `logging.basicConfig`（Finding #1）。

### 短期（1–3 個月）
- 加入輸入驗證（白名單正規化）與 log 內容清洗（Finding #2）。
- 使用 `with sqlite3.connect(...) as conn:` 與明列欄位，並統一例外處理（Finding #4, #6）。
- 實際套用 `chmod 0o600` 或以適當 mode `os.open` 建檔（Finding #3）。
- 清除未使用的 `import os`（Finding #5）。

### 長期
- 建立最小可執行骨架（main guard、logging、config、例外處理模板）供 lab 練習統一沿用。
- 在 CI 內加入 Bandit / Ruff / Semgrep 規則掃描 Python 安全反模式。
- 採用 `.env` + `python-dotenv` 或系統 secret store 管理 DB 路徑與連線資訊。

### 工具與流程
- **SAST**：Bandit、Semgrep（含 `p/owasp-top-ten` ruleset）
- **Dependency**：`pip-audit`（本專案目前無外部相依，可先行建立管線）
- **Lint**：Ruff（偵測 unused import、dead code）

---

## 5. 附錄 (Appendix)

### 已審查檔案
- `flaw_sql.py`（31 行，Python）
- `prompts.txt`（6 行，文字）
- `README.md`（12 行，Markdown）
- `example.db`（SQLite，二進位，僅登記存在未分析內容）

### 應用規則（Project CodeGuard）
- **Core**：安全編碼實務、輸入驗證、例外處理、秘密管理、日誌與監控
- **OWASP（Python 相關）**：A03 Injection（已緩解）、A04 Insecure Design、A05 Security Misconfiguration、A09 Security Logging and Monitoring Failures

### 方法論備註
- 專案規模小，已 100% 讀取所有分析性文字檔。
- SQL 注入原本列於 `prompts.txt` 修正目標中，經檢視已改為參數化查詢，不再列為開放發現。
- 本報告不執行任何動態分析或利用驗證；所有判斷基於靜態閱讀。
