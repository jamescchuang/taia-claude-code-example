# Project CodeGuard 安全掃描報告

- **掃描日期**：2026-04-30
- **掃描範圍**：`/Users/yellowcc/source/taia-claude-code-example/day2/產生結果範例/lab5/`
- **掃描來源**：`/software-security` Skill（Project CodeGuard 規則）
- **掃描工具**：Claude Code + CodeGuard rules
- **掃描者**：Claude (Opus 4.7)

---

## 1. 受檢檔案清單

| 檔案 | 語言 / 類型 | 是否為原始碼 |
| --- | --- | --- |
| `flaw_sql.py` | Python | ✅ 原始碼 |
| `example.db` | SQLite 資料庫 | ❌ 二進位資料 |
| `prompts.txt` | 純文字提示詞 | ❌ 文件 |
| `README.md` | Markdown | ❌ 文件 |
| `report.md`, `security_review_report.md` | Markdown 既存報告 | ❌ 文件 |
| `image*.png` | 圖片 | ❌ 資源 |

> 本次掃描的程式碼檔案僅有 **`flaw_sql.py`**（共 26 行），其餘為文件、資源或既有報告。

---

## 2. 套用的 CodeGuard 規則

依據 SKILL 指引，對 Python 原始碼套用：

### Always-Apply（一律檢查）
- `codeguard-1-hardcoded-credentials` — 不得硬編碼憑證
- `codeguard-1-crypto-algorithms` — 必須使用現代加密演算法
- `codeguard-1-digital-certificates` — 數位憑證的驗證與管理

### Python 語言相關
- `codeguard-0-input-validation-injection` ★ 主要規則
- `codeguard-0-additional-cryptography`
- `codeguard-0-api-web-services`
- `codeguard-0-authentication-mfa`
- `codeguard-0-authorization-access-control`
- `codeguard-0-file-handling-and-uploads`
- `codeguard-0-framework-and-languages`
- `codeguard-0-session-management-and-cookies`
- `codeguard-0-xml-and-serialization`

### SQL 相關
- `codeguard-0-data-storage`
- `codeguard-0-input-validation-injection`

---

## 3. 掃描結果摘要

| 嚴重度 | 數量 |
| --- | --- |
| 🔴 Critical | 1 |
| 🟠 High | 1 |
| 🟡 Medium | 2 |
| 🟢 Low / Info | 2 |

---

## 4. 詳細發現

### 🔴 Finding #1：SQL Injection（嚴重 / Critical）

- **規則**：`codeguard-0-input-validation-injection`（SQL Injection Prevention 段落）
- **CWE**：CWE-89 *Improper Neutralization of Special Elements used in an SQL Command*
- **OWASP**：A03:2021 – Injection
- **檔案**：`flaw_sql.py:15-16`

**問題程式碼**
```python
# flaw_sql.py:15
query = "SELECT * FROM users WHERE username = '" + username + "'"
cursor.execute(query)
```

**說明**
使用者輸入 `username` 直接以字串串接的方式組成 SQL 語句，未使用參數化查詢。攻擊者可透過下列輸入完全控制 WHERE 子句：

- `' OR '1'='1` → 略過 WHERE 條件，dump 整張 `users` 資料表
- `'; DROP TABLE users; --` → 視 SQLite 設定而異，可能執行多語句攻擊
- `' UNION SELECT name, sql FROM sqlite_master --` → 取得資料庫結構

**修正建議**
依 CodeGuard：「Use prepared statements and parameterized queries for 100% of data access.」改用 `?` 佔位符並把使用者輸入當作參數傳入：

```python
def get_user_info(username: str):
    with sqlite3.connect(DB_PATH) as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id, username, email FROM users WHERE username = ?",
            (username,),
        )
        return cursor.fetchall()
```

附帶建議：避免 `SELECT *`，只取必要欄位，遵守 least-privilege 原則。

---

### 🟠 Finding #2：缺少輸入驗證（High）

- **規則**：`codeguard-0-input-validation-injection`（Validation Playbook 段落）
- **CWE**：CWE-20 *Improper Input Validation*
- **檔案**：`flaw_sql.py:24`

**問題程式碼**
```python
user_input = input("Enter username: ")
print(get_user_info(user_input))
```

**說明**
即便改為參數化查詢，仍應在信任邊界做語法驗證，包含：
- 型別與長度（如 username 長度 1–32）
- 字元 allow-list（`^[A-Za-z0-9_.-]+$`）
- Unicode 正規化、anchored regex（`^...$`），並避免 ReDoS

**修正建議**
```python
import re
USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{1,32}$")

def validate_username(value: str) -> str:
    value = value.strip()
    if not USERNAME_RE.match(value):
        raise ValueError("invalid username format")
    return value
```

---

### 🟡 Finding #3：資料庫連線與例外處理不足（Medium）

- **規則**：`codeguard-0-framework-and-languages`、`codeguard-0-data-storage`
- **CWE**：CWE-755 *Improper Handling of Exceptional Conditions*、CWE-404 *Improper Resource Shutdown*
- **檔案**：`flaw_sql.py:10-19`

**問題說明**
- `sqlite3.connect()` 未使用 context manager（`with` 區塊）；若 `cursor.execute` 拋出例外，`conn.close()` 不會執行，可能造成資源洩漏。
- 缺少例外處理，原始錯誤訊息可能被 `print` 或上游記錄，洩漏 SQL/結構資訊。

**修正建議**
```python
import logging
log = logging.getLogger(__name__)

def get_user_info(username: str):
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email FROM users WHERE username = ?",
                (username,),
            )
            return cursor.fetchall()
    except sqlite3.Error:
        log.exception("database error during get_user_info")
        return []  # 不要把原始錯誤回傳給呼叫端
```

---

### 🟡 Finding #4：缺乏安全相關日誌紀錄（Medium）

- **規則**：`codeguard-0-logging`
- **CWE**：CWE-778 *Insufficient Logging*
- **檔案**：`flaw_sql.py`（整檔）

**問題說明**
完全沒有 logging。對使用者查詢這類具安全意義的動作，至少應記錄：
- 失敗的查詢（含時間戳、來源、操作）
- 例外與錯誤
- ⚠ 切勿記錄 PII / 密碼 / token 原文。

**修正建議**
```python
import logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(name)s %(message)s")
log = logging.getLogger(__name__)
```
並在查詢前後加上 `log.info("user lookup attempted")` 等不含敏感資料的記錄。

---

### 🟢 Finding #5：硬編碼資料庫路徑（Low / Info）

- **規則**：`codeguard-1-hardcoded-credentials`（相關，但本案非機密）
- **檔案**：`flaw_sql.py:6`

```python
DB_PATH = "example.db"
```

**說明**
`example.db` 為示範用，**不是憑證**，因此不違反硬編碼憑證規則。但實務上路徑應由環境變數或設定檔提供，方便部署：
```python
import os
DB_PATH = os.environ.get("APP_DB_PATH", "example.db")
```

---

### 🟢 Finding #6：缺少身分驗證與授權（Info）

- **規則**：`codeguard-0-authentication-mfa`、`codeguard-0-authorization-access-control`
- **檔案**：`flaw_sql.py`（整檔）

**說明**
本檔為示範腳本，無認證/授權層。在實際應用中對 `users` 資料表的存取必須要有：
- 已驗證的呼叫者身分
- 最小權限的資料庫帳號（不要用 admin）
- 對「查詢自己以外的使用者」做授權檢查（例如 RBAC / ABAC）

CodeGuard 引文：「Prefer least-privilege DB users and views; never grant admin to app accounts.」

---

## 5. 規則對照矩陣

| Finding | Rule ID | Severity | 行號 |
| --- | --- | --- | --- |
| #1 SQL Injection | codeguard-0-input-validation-injection | Critical | flaw_sql.py:15 |
| #2 缺少輸入驗證 | codeguard-0-input-validation-injection | High | flaw_sql.py:24 |
| #3 連線/例外處理 | codeguard-0-framework-and-languages, codeguard-0-data-storage | Medium | flaw_sql.py:10-19 |
| #4 缺乏 logging | codeguard-0-logging | Medium | flaw_sql.py（整檔） |
| #5 硬編碼路徑 | codeguard-1-hardcoded-credentials（資訊性） | Low | flaw_sql.py:6 |
| #6 缺少 AuthN/AuthZ | codeguard-0-authentication-mfa, codeguard-0-authorization-access-control | Info | flaw_sql.py（整檔） |

---

## 6. 已通過項目

| 項目 | 結果 |
| --- | --- |
| 硬編碼密碼 / API Key / Token | ✅ 未發現 |
| 弱加密演算法（MD5/SHA-1/DES） | ✅ 未使用 |
| 不安全的反序列化（`pickle.loads` 等） | ✅ 未使用 |
| 危險函式（`eval`, `exec`, `os.system`） | ✅ 未使用 |
| 不安全 XML 解析 | ✅ 不適用 |

---

## 7. 修補後的建議版本（完整範例）

```python
"""User lookup demo — secured version."""
import logging
import os
import re
import sqlite3

DB_PATH = os.environ.get("APP_DB_PATH", "example.db")
USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{1,32}$")

log = logging.getLogger(__name__)


def validate_username(value: str) -> str:
    value = value.strip()
    if not USERNAME_RE.match(value):
        raise ValueError("invalid username format")
    return value


def get_user_info(username: str):
    username = validate_username(username)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, email FROM users WHERE username = ?",
                (username,),
            )
            return cursor.fetchall()
    except sqlite3.Error:
        log.exception("database error during get_user_info")
        return []


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        user_input = input("Enter username: ")
        print(get_user_info(user_input))
    except ValueError as exc:
        print(f"Invalid input: {exc}")
```

---

## 8. 結論

- 本專案僅含一個示範用 Python 檔，主要風險集中在 **SQL Injection**（Critical）。
- 該漏洞為刻意保留的教學案例，但若改寫為實際應用，必須優先修補。
- 同時建議補強：輸入驗證、連線/例外管理、安全日誌、認證授權四項面向。
- 修補完成後可再以 `/software-security` 重新掃描以確認。
