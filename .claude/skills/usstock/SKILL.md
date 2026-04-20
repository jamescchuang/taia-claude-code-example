---
name: usstock
description: 查詢美國股市即時股價。使用者輸入股票代號（如 AAPL 或 AAPL,MSFT,TSLA），取得當前股價、漲跌幅等資訊。支援逗號分隔一次查詢多支股票。當使用者詢問美國股票價格、報價或提及美股代號時觸發。
---

# 美國股市即時股價查詢

使用 yfinance 套件查詢美國股票即時股價資訊。以 uv 管理 Python 虛擬環境與套件。

## 何時使用此技能

當使用者：

- 詢問美國股票的即時股價（例如「AAPL 現在多少錢」）
- 輸入美股代號查詢行情（例如 TSLA、NVDA、MSFT）
- 提到「查美股」、「美國股票」或輸入美股代號
- 詢問美國股市價格

## 環境準備

使用 uv 執行 Python 腳本，無需事先建立虛擬環境。uv 會自動處理依賴安裝。

確認 uv 已安裝：

```bash
which uv || echo "請先安裝 uv: curl -LsSf https://astral.sh/uv/install.sh | sh"
```

## 執行步驟

### 步驟一：取得股票代號

若使用者未提供股票代號，請詢問：

> 請輸入要查詢的美國股票代號（例如：AAPL，或用逗號分隔多支：AAPL,MSFT,TSLA）

使用者可用逗號分隔多個股票代號（例如 `AAPL,MSFT,TSLA`）。解析輸入時以逗號分割、去除空白，並統一轉為大寫。

### 步驟二：使用 yfinance 查詢股價

美國股票在 Yahoo Finance 的代號即為股票代號本身，無需後綴（例如 `AAPL`、`MSFT`、`TSLA`）。

使用 `uv run --with yfinance` 直接執行 Python 腳本，uv 會自動安裝 yfinance 至臨時環境：

```bash
uv run --with yfinance python3 -c "
import yfinance as yf
import json

symbols = ['AAPL', 'MSFT', 'TSLA']  # 替換為使用者輸入的代號
results = []

for sym in symbols:
    ticker = yf.Ticker(sym)
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
        'currency': info.get('currency', 'USD'),
    })

print(json.dumps(results, ensure_ascii=False))
"
```

### 步驟三：計算漲跌並顯示

從回傳的 JSON 中解析各股票資料，計算：
- **漲跌**：`price - previousClose`
- **漲跌幅**：`((price - previousClose) / previousClose) * 100`%
- **成交量**：`volume`（直接顯示股數，美股無「張」的概念）

### 步驟四：向使用者呈現結果

**單支股票** — 以詳細表格顯示：

```
## {股票名稱} ({股票代號})

| 項目       | 數值        |
|-----------|------------|
| 即時股價    | ${price}   |
| 漲跌       | {change} ({change_pct}%) |
| 開盤價     | ${open}    |
| 最高價     | ${high}    |
| 最低價     | ${low}     |
| 昨收價     | ${previousClose} |
| 成交量     | {volume}   |
```

**多支股票** — 以比較摘要表格顯示，每支股票一列：

```
| 股票       | 即時股價  | 漲跌          | 開盤    | 最高    | 最低    | 昨收    | 成交量 |
|-----------|---------|--------------|--------|--------|--------|--------|-------|
| {name} ({code}) | ${price} | {change} ({change_pct}%) | ${open} | ${high} | ${low} | ${previousClose} | {volume} |
```

漲跌指標：
- 上漲：前綴 ▲
- 下跌：前綴 ▼
- 平盤：顯示「平盤」

貨幣顯示：美股預設以 USD 計價，價格前加 `$` 符號。若 `currency` 非 `USD`，請於顯示時註明幣別。

## 錯誤處理

- 若 `regularMarketPrice` 為 `None`，告知使用者該股票代號可能無效或已下市。
- 若 yfinance 連線失敗，告知使用者 Yahoo Finance 可能暫時無法存取。
- 若非美股交易時段查詢（美東時間 9:30–16:00 以外），yfinance 會回傳最近一次收盤價，應註明資料為上次收盤價格。
- 留意美股有盤前（pre-market）與盤後（after-hours）交易，`regularMarketPrice` 僅為正常交易時段價格。

## 使用範例

**查詢單支股票：**

**使用者：** /usstock AAPL

**執行方式：**

```bash
uv run --with yfinance python3 -c "
import yfinance as yf
import json

ticker = yf.Ticker('AAPL')
info = ticker.info

result = {
    'code': 'AAPL',
    'name': info.get('shortName', info.get('longName', 'AAPL')),
    'price': info.get('regularMarketPrice'),
    'previousClose': info.get('previousClose'),
    'open': info.get('regularMarketOpen'),
    'high': info.get('regularMarketDayHigh'),
    'low': info.get('regularMarketDayLow'),
    'volume': info.get('regularMarketVolume'),
    'currency': info.get('currency', 'USD'),
}
print(json.dumps(result, ensure_ascii=False))
"
```

**查詢多支股票：**

**使用者：** /usstock AAPL,MSFT,TSLA

**執行方式：** 同步驟二，將 symbols 替換為 `['AAPL', 'MSFT', 'TSLA']`，一次查詢所有代號。

## 注意事項

- 使用 `uv run --with yfinance` 執行，無需預先建立虛擬環境或手動安裝套件，uv 會自動處理。
- 美股代號直接使用原始符號（例如 `AAPL`），無需附加交易所後綴。
- 使用者輸入的代號一律轉為大寫（yfinance 大小寫敏感）。
- yfinance 在非交易時段仍可查詢，回傳的是最近收盤價。
- 美股成交量直接以股數顯示，不需換算單位。
- 價格以美元（USD）顯示，前綴 `$` 符號。
