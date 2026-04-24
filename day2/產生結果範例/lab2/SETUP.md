# Vector DB Lab — Setup

## 環境需求
- Python 3.10+
- [uv](https://github.com/astral-sh/uv)

## 安裝

```bash
cd day2/lab2
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

## 啟動

```bash
uv run uvicorn app.main:app --reload
```

開啟 http://127.0.0.1:8000

## 功能

- **索引資料夾**：指定本機資料夾，讀取 `.txt/.md/.py/...` 檔案並存入 Milvus Lite。
- **查詢**：可在網頁上調整 collection、embedding 模型、top_k。
- **Collections**：列出與刪除現有 collection。

所有參數（資料夾、collection、embedding 模型、chunk size/overlap、top_k）都可以從網頁調整。

Milvus Lite 檔案位於 `data/milvus_lite.db`。
