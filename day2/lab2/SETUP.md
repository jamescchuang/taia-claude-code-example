# 安裝與啟動

## 1. 建立虛擬環境並安裝套件（使用 uv）

```bash
uv venv --python 3.11
uv pip install -r requirements.txt
```

## 2. 啟動 FastAPI 服務

```bash
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

開啟瀏覽器 http://localhost:8000 即可使用。

## 3. 使用流程

1. 在「參數設定」調整 DB 路徑、Collection、Embedding Model、Chunk Size / Overlap，按「儲存參數」。
2. 在「索引資料夾」輸入資料夾路徑（預設 `./data/docs`），按「開始索引」。
3. 在「查詢」輸入查詢字串與 `top_k`，查看最相近的段落。

## 支援的檔案副檔名
`.txt` `.md` `.pdf` `.py` `.json` `.csv` `.log`

## 資料位置
Milvus Lite 資料庫檔案預設寫入 `./milvus_data/vector.db`（已加入 `.gitignore`）。
