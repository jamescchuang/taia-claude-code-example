# 程式碼安全掃描報告 (Security Code Review Report)

- **掃描日期**：2026-04-24
- **掃描依據**：Project CodeGuard（`.claude/skills/software-security/`）
- **掃描範圍**：`/Users/yellowcc/source/taia-claude-code-example/day2/lab4/`
- **主要受檢檔案**：`flaw_sql.py`（Python + SQLite）
- **其他檔案**：`example.db`（二進位資料庫，未分析內容）、`README.md`、`prompts.txt`（文件）

---

## 1. 執行摘要 (Executive Summary)

| 項目 | 數量 |
|------|------|
| 高風險 (High) | 2 |
| 中風險 (Medium) | 4 |
| 低風險 (Low) | 3 |
| 資訊/良好實踐 (Info/Good) | 2 |

本次掃描在 `flaw_sql.py` 中發現 **9 項** 安全性與程式品質問題。其中：

- **正面發現**：已正確使用「參數化查詢」（`cursor.execute("... WHERE username = ?", (username,))`），避免了傳統 SQL Injection。
- **關鍵風險**：模組層級副作用（module-level `input()`、`print()`）、`SELECT *` 可能外洩敏感欄位、輸入未驗證、缺少例外處理與資源管理、潛在 Log Injection、記錄 PII、資料庫檔案權限未落實。
- **建議**：將互動式程式流程收攏到 `if __name__ == "__main__":` 內；補上輸入驗證、例外處理與 `with` 資源管理；明確指定 SELECT 欄位；對日誌輸入做 CR/LF 消毒；視需要移除或實際使用 `os.chmod`。

---

## 2. 檔案：`flaw_sql.py` 內容快照

```python
import sqlite3
import logging
import os  # This line is kept for reference but will not be used in the code.

def get_user_info(username):
    # 僅供範例，實務上應加強資料庫檔案權限與存放位置
    db_path = 'example.db'
    # 建議：在部署時設定更嚴格的檔案權限
    # os.chmod(db_path, 0o600)  # 僅限擁有者讀寫
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    # 使用參數化查詢以防止 SQL 注入
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    result = cursor.fetchall()
    conn.close()
    # 日誌記錄查詢事件（不記錄敏感資料）
    logging.info("User info lookup attempted for username: %s", username)
    return result

# Example usage (do NOT use unsanitized input in production)
# 實務上應驗證與淨化所有用戶輸入
user_input = input("Enter username: ")
print(get_user_info(user_input))
if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[logging.StreamHandler()]
    )
```

---

## 3. 發現項目詳細列表 (Findings)

### F-01　模組層級副作用（匯入即執行）— **High**
- **對應規則**：`codeguard-0-framework-and-languages`（Python 安全預設）、一般程式品質
- **位置**：`flaw_sql.py:23-24`
- **問題**：
  - `user_input = input(...)` 與 `print(get_user_info(...))` 位於模組頂層（不在 `if __name__ == "__main__":` 區塊內）。
  - 任何 `import flaw_sql` 都會立即阻塞等待使用者輸入，並對資料庫進行查詢，產生非預期副作用。
  - 這使得程式碼無法安全地被測試工具、其他模組或 framework 匯入；亦難以作為 library 使用。
- **風險**：拒絕服務（Import 阻塞）、非預期資料存取、難以進行安全測試。
- **建議修正**：將互動流程移入 `if __name__ == "__main__":` 區塊，並先呼叫 `logging.basicConfig` 再執行業務邏輯。

---

### F-02　`SELECT *` 可能導致敏感欄位外洩 — **High**
- **對應規則**：`codeguard-0-data-storage`（最小權限、欄位層級授權）、`codeguard-0-authorization-access-control`
- **位置**：`flaw_sql.py:14`
- **問題**：`SELECT * FROM users WHERE username = ?` 會回傳該列所有欄位。若 `users` 資料表含有 `password_hash`、`email`、`phone`、`mfa_secret`、`session_token` 等敏感欄位，全部會被 `fetchall()` 一併取出並由 `print()` 輸出到終端，也會在呼叫方被廣為傳遞。
- **風險**：敏感資料洩漏（密碼雜湊、PII、Session Token 等）。
- **建議修正**：明確列出需要的欄位，例如：
  ```python
  cursor.execute(
      "SELECT id, username, display_name FROM users WHERE username = ?",
      (username,),
  )
  ```

---

### F-03　輸入未驗證與正規化 — **Medium**
- **對應規則**：`codeguard-0-input-validation-injection`（Validation Playbook：Syntactic/Semantic/Normalization）
- **位置**：`flaw_sql.py:23`（`input(...)`）、`flaw_sql.py:6`（`get_user_info` 入口）
- **問題**：
  - 雖已採參數化查詢防止 SQL Injection，但 CodeGuard 要求「在信任邊界進行正向（allow-list）驗證與 canonicalize」。
  - 目前對 `username` 未做：型別檢查、長度上限、字元集合允許清單、Unicode 正規化（NFKC）、去除首尾空白/控制字元。
  - 過長或含控制字元的輸入可能造成下游問題（例如 Log Injection，見 F-04；或 Denial of Wallet / Denial of Log）。
- **建議修正**：
  ```python
  import re, unicodedata
  _USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{1,32}$")

  def _validate_username(raw: str) -> str:
      if not isinstance(raw, str):
          raise ValueError("username must be a string")
      normalized = unicodedata.normalize("NFKC", raw).strip()
      if not _USERNAME_RE.fullmatch(normalized):
          raise ValueError("invalid username")
      return normalized
  ```

---

### F-04　日誌注入（Log Injection）與 PII 記錄 — **Medium**
- **對應規則**：`codeguard-0-logging`（Sanitize all log inputs、redact PII、log injection 防護）
- **位置**：`flaw_sql.py:18`
- **問題**：
  - `logging.info("User info lookup attempted for username: %s", username)` 直接將未消毒的 `username` 寫入 log。若 `username` 含有 CRLF (`\r\n`) 或 log 分隔字元，攻擊者可偽造 log 條目，誤導事件調查。
  - 另外，依據 `codeguard-0-logging` 的「Privacy & Compliance：minimize personal data in logs」，純明文使用者名稱視情境可能屬於 PII；建議僅記錄 hashed/tokenized 或内部 user id。
  - 註解宣稱「不記錄敏感資料」，但實際仍記錄了 username 這項可識別欄位。
- **風險**：日誌偽造、調查結果錯誤、潛在 GDPR/隱私不合規。
- **建議修正**：
  - 記錄前先 `username.replace("\r", "").replace("\n", "")`（或使用 `str(...).encode("unicode_escape").decode()` 等方式）。
  - 採用結構化 JSON logging，避免控制字元污染整行紀錄。
  - 考慮只記錄 user id 或 SHA-256 雜湊後的 username，以降低 PII 曝光。

---

### F-05　缺少例外處理與資源管理 — **Medium**
- **對應規則**：`codeguard-0-framework-and-languages`（Python 安全預設）、`codeguard-0-data-storage`（連線整潔性）
- **位置**：`flaw_sql.py:11-16`
- **問題**：
  - `sqlite3.connect(...)` 未使用 `with` 或 `try/finally`。若 `execute` 或 `fetchall` 丟出例外，`conn.close()` 將不會被呼叫，造成資源洩漏與檔案鎖定。
  - 呼叫端沒有 `try/except`，底層錯誤（例如 `sqlite3.OperationalError`）會原汁原味往外丟到終端，可能揭露內部實作細節（stack trace、DB schema 線索）。
- **建議修正**：
  ```python
  try:
      with sqlite3.connect(db_path) as conn:
          cursor = conn.cursor()
          cursor.execute(
              "SELECT id, username FROM users WHERE username = ?",
              (username,),
          )
          return cursor.fetchall()
  except sqlite3.DatabaseError:
      logger.exception("db lookup failed")
      raise RuntimeError("internal error") from None
  ```

---

### F-06　日誌設定時機錯誤（basicConfig 發生在首次 log 之後）— **Medium**
- **對應規則**：`codeguard-0-logging`（Structured logging、telemetry 可用性）、一般程式品質
- **位置**：`flaw_sql.py:25-31` vs `flaw_sql.py:18,24`
- **問題**：
  - 目前執行順序為：模組層級 → `input()` → `get_user_info()` → `logging.info(...)` → 才輪到 `if __name__ == "__main__":` 中的 `logging.basicConfig(...)`。
  - 首次 `logging.info` 觸發時，Python `logging` 會自動建立預設 handler（WARNING 等級），導致 `INFO` 訊息被丟棄；之後的 `basicConfig` 也會因為 root logger 已有 handler 而被忽略（除非加 `force=True`）。
  - 結論：在正常執行流程下，這筆 log **根本不會輸出**，偵測/稽核價值歸零。
- **風險**：失效的稽核軌跡（audit trail）。
- **建議修正**：`basicConfig(...)` 必須在任何 `logging.*` 呼叫之前執行；將互動流程整合入 `__main__`，並把 `basicConfig` 放在 main block 最前端（或模組頂端）。

---

### F-07　資料庫檔案權限與路徑未強制 — **Low**
- **對應規則**：`codeguard-0-data-storage`（Backend Database Protection、Credential/Data file permissions）
- **位置**：`flaw_sql.py:8-10`
- **問題**：
  - `db_path = 'example.db'` 使用相對路徑，結果隨 `cwd` 而異，可能被放在 web root 或版控目錄內。
  - 註解建議 `os.chmod(db_path, 0o600)` 但被註解掉；`import os` 也因此變成死程式碼。
  - 在 Unix 多使用者主機上，若檔案權限為預設 0644，其他本機使用者可讀取整個 `users` 表。
- **建議修正**：
  - 以絕對路徑或環境變數指定資料庫位置（例：`os.environ["APP_DB_PATH"]`），並確保存放於 web root 之外。
  - 部署腳本或應用啟動時實際執行 `os.chmod(db_path, 0o600)`；若程式內不需要 `os`，則移除該 import。

---

### F-08　缺少認證/授權層（任意查詢任意使用者）— **Low**（視使用場景可升為 Medium/High）
- **對應規則**：`codeguard-0-authentication-mfa`（Account enumeration、generic errors）、`codeguard-0-authorization-access-control`（最小權限）
- **位置**：`flaw_sql.py:6-19`
- **問題**：
  - `get_user_info(username)` 對呼叫端沒有任何身分/權限檢查。任何能執行此 CLI 的人都能查詢任何帳號的資料。
  - 若資料表包含敏感欄位（F-02），此設計等同「公開使用者目錄」。
  - 回傳值「找得到 / 找不到」的差異亦可被用於帳號列舉（account enumeration）。
- **建議修正**：
  - 將此函式置於受認證保護的服務層後面；對呼叫者做授權檢查（例如只能查自己或具備管理者角色）。
  - 對外部錯誤訊息採用統一格式，不直接洩漏「使用者不存在」資訊。

---

### F-09　未使用的 import / 死程式碼 — **Low**
- **對應規則**：一般程式碼品質（降低攻擊面、降低誤用）
- **位置**：`flaw_sql.py:4`
- **問題**：`import os` 僅為「參考用」但未實際使用；註解指示了「建議做 `os.chmod`」但沒有真正執行。
- **建議修正**：要嘛刪除 import，要嘛實作 `os.chmod(db_path, 0o600)`。留著死程式碼容易造成誤解。

---

## 4. 正面觀察 (Good Practices)

| 編號 | 項目 | 說明 |
|------|------|------|
| G-01 | 使用參數化查詢 | `cursor.execute("... WHERE username = ?", (username,))` 正確分離 code 與 data，符合 `codeguard-0-input-validation-injection` 的 SQL Injection 防禦核心策略。 |
| G-02 | 沒有硬式編碼憑證 | 檔案中未發現 `password`, `secret`, `api_key`, `token` 等硬編碼字串；符合 `codeguard-1-hardcoded-credentials`（always-apply）。`example.db` 僅為本機範例檔，不屬於憑證。 |

---

## 5. Always-Apply 規則審查結果

| 規則 | 檢查結果 |
|------|----------|
| `codeguard-1-hardcoded-credentials` | ✅ 未在原始碼中發現密碼、API Key、Token、私鑰、AWS/Stripe/GitHub/Google API 特徵字串或 JWT。 |
| `codeguard-1-crypto-algorithms` | ➖ 本檔案未涉及加解密、雜湊或簽章；無適用對象。若未來要處理密碼驗證，請採 Argon2id / bcrypt / scrypt / PBKDF2（見 `codeguard-0-authentication-mfa`）。 |
| `codeguard-1-digital-certificates` | ➖ 本檔案未涉及 TLS/憑證驗證；SQLite 為本機檔案。 |

---

## 6. 建議的修正後程式碼（Reference Fix）

> 下列為套用 F-01 ~ F-09 建議後的參考版本，供修復時對照。實作細節請依專案需求調整。

```python
import logging
import os
import re
import sqlite3
import sys
import unicodedata

logger = logging.getLogger(__name__)

_USERNAME_RE = re.compile(r"^[A-Za-z0-9_.-]{1,32}$")
_DB_PATH = os.environ.get("APP_DB_PATH", os.path.join(os.path.dirname(__file__), "example.db"))


def _validate_username(raw: str) -> str:
    if not isinstance(raw, str):
        raise ValueError("username must be a string")
    normalized = unicodedata.normalize("NFKC", raw).strip()
    if not _USERNAME_RE.fullmatch(normalized):
        raise ValueError("invalid username format")
    return normalized


def _sanitize_for_log(value: str) -> str:
    return value.replace("\r", "\\r").replace("\n", "\\n")


def get_user_info(username: str):
    username = _validate_username(username)
    try:
        with sqlite3.connect(_DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id, username, display_name FROM users WHERE username = ?",
                (username,),
            )
            rows = cursor.fetchall()
    except sqlite3.DatabaseError:
        logger.exception("db lookup failed")
        raise RuntimeError("internal error") from None

    logger.info("user_info_lookup username=%s hits=%d",
                _sanitize_for_log(username), len(rows))
    return rows


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(name)s %(message)s',
        handlers=[logging.StreamHandler()],
    )
    try:
        os.chmod(_DB_PATH, 0o600)
    except OSError:
        logger.warning("unable to tighten db file permissions on %s", _DB_PATH)

    try:
        raw = input("Enter username: ")
        print(get_user_info(raw))
    except ValueError as e:
        logger.warning("invalid input: %s", _sanitize_for_log(str(e)))
        sys.exit(2)
```

---

## 7. 優先處理順序 (Remediation Priority)

1. **立即**：F-01（模組層級副作用）、F-02（`SELECT *`）
2. **短期**：F-03（輸入驗證）、F-04（Log Injection/PII）、F-05（例外處理與 `with`）、F-06（logging 設定時機）
3. **中期**：F-07（檔案權限/路徑）、F-08（認證/授權）、F-09（死程式碼清理）

---

## 8. 附註

- 本報告僅靜態檢視 `flaw_sql.py`。`example.db` 為二進位檔，其 schema 與內容未納入分析；若要進一步評估 F-02 的實際影響範圍，建議提供 `users` 表的欄位定義。
- 本次掃描套用之 CodeGuard 規則（Python + SQL 相關）：
  - `codeguard-1-hardcoded-credentials`（always-apply）
  - `codeguard-1-crypto-algorithms`（always-apply）
  - `codeguard-1-digital-certificates`（always-apply）
  - `codeguard-0-input-validation-injection`
  - `codeguard-0-data-storage`
  - `codeguard-0-framework-and-languages`
  - `codeguard-0-logging`
  - `codeguard-0-authentication-mfa`
  - `codeguard-0-authorization-access-control`（部份引用）
