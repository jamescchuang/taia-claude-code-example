---
name: twstock
description: 查詢台灣股市即時股價。使用者輸入股票代號（如 2330 或 2330,2317,2454），取得當前股價、漲跌幅等資訊。支援逗號分隔一次查詢多支股票。當使用者詢問台灣股票價格、報價或提及台灣股票代號時觸發。
---

# 台灣股市即時股價查詢

使用 yfinance 套件查詢台灣股票即時股價資訊。以 uv 管理 Python 虛擬環境與套件。

## 何時使用此技能

當使用者：

- 詢問台灣股票的即時股價（例如「2330 現在多少錢」）
- 輸入台灣股票代號查詢行情
- 提到「查股價」、「股票」、「台股」或輸入台灣股票代號
- 詢問台灣股市價格

## 環境準備

使用 uv 執行 Python 腳本，無需事先建立虛擬環境。uv 會自動處理依賴安裝。

確認 uv 已安裝：

```bash
which uv || echo "請先安裝 uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
```

## 執行步驟

### 步驟一：取得股票代號

若使用者未提供股票代號，請詢問：

> 請輸入要查詢的台灣股票代號（例如：2330，或用逗號分隔多支：2330,2317,2454）

使用者可用逗號分隔多個股票代號（例如 `2330,2317,2454`）。解析輸入時以逗號分割並去除空白。

### 步驟二：使用 yfinance 查詢股價

台灣股票在 Yahoo Finance 的代號格式：
- 上市（TWSE）：`{代號}.TW`（例如 `2330.TW`）
- 上櫃（OTC）：`{代號}.TWO`（例如 `6547.TWO`）

使用 `uv run --with yfinance` 直接執行 Python 腳本，uv 會自動安裝 yfinance 至臨時環境：

```bash
uv run --with yfinance python3 -c "
import yfinance as yf
import json

symbols = ['2330', '2317', '2454']  # 替換為使用者輸入的代號
results = []

for sym in symbols:
    # 先嘗試上市 .TW
    ticker = yf.Ticker(f'{sym}.TW')
    info = ticker.info
    # 若無法取得有效資料，嘗試上櫃 .TWO
    if info.get('regularMarketPrice') is None:
        ticker = yf.Ticker(f'{sym}.TWO')
        info = ticker.info

    results.append({
        'code': sym,
        'name': info.get('shortName', info.get('longName', sym)),
        'price': info.get('regularMarketPrice'),
        'previousClose': info.get('previousClose'),
        'open': info.get('regularMarketOpen'),
        'high': info.get('regularMarketDayHigh'),
        'low': info.get('regularMarketDayLow'),
        'volume': info.get('regularMarketVolume'),
    })

print(json.dumps(results, ensure_ascii=False))
"
```

### 步驟三：計算漲跌並顯示

從回傳的 JSON 中解析各股票資料，計算：
- **漲跌**：`price - previousClose`
- **漲跌幅**：`((price - previousClose) / previousClose) * 100`%
- **成交量（張）**：`volume / 1000`（Yahoo Finance 回傳的是股數，台股一張 = 1000 股）

### 步驟四：向使用者呈現結果

**單支股票** — 以詳細表格顯示：

```
## {股票名稱} ({股票代號})

| 項目       | 數值        |
|-----------|------------|
| 即時股價    | {price}    |
| 漲跌       | {change} ({change_pct}%) |
| 開盤價     | {open}     |
| 最高價     | {high}     |
| 最低價     | {low}      |
| 昨收價     | {previousClose} |
| 成交量(張) | {volume/1000} |
```

**多支股票** — 以比較摘要表格顯示，每支股票一列：

```
| 股票       | 即時股價  | 漲跌          | 開盤    | 最高    | 最低    | 昨收    | 成交量(張) |
|-----------|---------|--------------|--------|--------|--------|--------|-----------|
| {name} ({code}) | {price} | {change} ({change_pct}%) | {open} | {high} | {low} | {previousClose} | {volume/1000} |
```

漲跌指標：
- 上漲：前綴 ▲
- 下跌：前綴 ▼
- 平盤：顯示「平盤」

## 錯誤處理

- 若 `regularMarketPrice` 為 `None`（`.TW` 和 `.TWO` 皆無資料），告知使用者該股票代號可能無效。
- 若 yfinance 連線失敗，告知使用者 Yahoo Finance 可能暫時無法存取。
- 若非交易時段查詢，yfinance 會回傳最近一次收盤價，應註明資料為上次收盤價格。

## 使用範例

**查詢單支股票：**

**使用者：** /twstock 2330

**執行方式：**

```bash
uv run --with yfinance python3 -c "
import yfinance as yf
import json

ticker = yf.Ticker('2330.TW')
info = ticker.info
if info.get('regularMarketPrice') is None:
    ticker = yf.Ticker('2330.TWO')
    info = ticker.info

result = {
    'code': '2330',
    'name': info.get('shortName', info.get('longName', '2330')),
    'price': info.get('regularMarketPrice'),
    'previousClose': info.get('previousClose'),
    'open': info.get('regularMarketOpen'),
    'high': info.get('regularMarketDayHigh'),
    'low': info.get('regularMarketDayLow'),
    'volume': info.get('regularMarketVolume'),
}
print(json.dumps(result, ensure_ascii=False))
"
```

**查詢多支股票：**

**使用者：** /twstock 2330,2317,2454

**執行方式：** 同步驟二，將 symbols 替換為 `['2330', '2317', '2454']`，一次查詢所有代號。

## 注意事項

- 使用 `uv run --with yfinance` 執行，無需預先建立虛擬環境或手動安裝套件，uv 會自動處理。
- 台灣上市股票代號格式為 `{代號}.TW`，上櫃為 `{代號}.TWO`，一律先嘗試 `.TW`，無資料再試 `.TWO`。
- yfinance 在非交易時段仍可查詢，回傳的是最近收盤價。
- 成交量需除以 1000 換算為「張」。
