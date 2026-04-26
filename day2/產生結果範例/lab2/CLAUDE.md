# CLAUDE.md

本文件為 Claude Code (claude.ai/code) 在此儲存庫中作業時的指引。

## 用途

本 lab 將 `Financial_Model.xlsx`（一個 40 年期收費公路特許經營權財務模型）轉為**單一、完全離線運作的 HTML 儀表板**。沒有 Web server、沒有建置工具鏈、沒有測試——整個交付物就是一個 `dashboard.html` 檔，加上產生它的 Python 腳本。

## 常用指令

Python 以 `uv` 管理（不使用 pip/venv）。相依套件透過 `--with` 內嵌宣告：

```bash
# 從 Excel 檔重新產生 data.json
uv run --with openpyxl python build_dashboard.py

# 從 data.json 重新輸出 dashboard.html
uv run python build_html.py

# 在本地開啟儀表板（macOS）
open dashboard.html
```

兩個腳本都是冪等的。若 `Financial_Model.xlsx` 或 HTML 模板有變動，請依上述順序重新執行。

## 架構

兩階段 pipeline，嚴格分離，使 Excel 解析永遠不觸碰渲染邏輯：

1. **`build_dashboard.py`** — 以 `openpyxl` 讀取 `Financial_Model.xlsx`（使用 `data_only=True` 讀取公式計算後的結果，而非公式字串）。它透過**欄 B 的標籤名稱**而非固定儲存格位址走訪每個工作表，因為各工作表的欄位偏移不同（例如年度 1 在 `Construction` 是欄 E，在 `P&L` 是欄 F）。輸出為 `data.json`。

2. **`build_html.py`** — 讀取 `data.json`，將其作為 `<script type="application/json">` 區塊內嵌到以 Python raw string 保存的 HTML 模板中，並寫出 `dashboard.html`。模板以 `__DATA__` 佔位字串，透過 `str.replace` 進行取代。

### 為什麼要單一檔案、不使用 CDN

規格要求完全離線運作。所有圖表皆為 HTML 內以純 JavaScript **手刻 SVG** 產生（`lineChart`、`stackedArea`、`barLineChart`、`donut` 函式）。無 Chart.js、無外部腳本、無 Web 字型。響應式由 `viewBox` + `preserveAspectRatio` 處理——切勿引入圖表函式庫或 CDN 相依。

### 設計限制（非顯而易見）

- **紅色金融科技色盤**定義於 `:root` CSS 變數（`--red-1..4`、`--bg-0..3`）。新增 UI 應從這些變數取色，不要自創顏色。
- **任何視窗寬度下都不可出現水平捲軸。** 在 1100px 以下，grid 透過 `.span-*` media query 收合為單欄。圖表必須以 `viewBox` 縮放，而非固定寬度。
- **Scenario 僅使用 Base Case。** Excel 中有 10 個情境欄位，但儀表板只讀取 Base Case 的值。若要擴充為多情境，`build_dashboard.py` 的擷取邏輯需加上 `Input Assumptions` 第 2 列的情境選擇器。

### 擷取時需注意的 Excel 模型眉角

- 此活頁簿存在**循環相依**（Capitalized Interest ↔ Debt Drawdown ↔ Fees）。務必以 `data_only=True` 載入；讀取公式字串會得到字串而非數值。詳見 `userguide.md §14`。
- 列標籤包含拼字錯誤，必須逐字精確比對：`Input Assumptions` 中是 `"Traffic - Heavy Vehicule (HV)"`，但 `Operation` 中卻是 `"TRAFFIC - Heavy Vehicle (HV)"`（拼字與大小寫皆不同）。
- 各工作表的年度 1 欄位起始位置：`Operation`／`Amortization`／`Construction` 從 index 4 開始；`Debt`／`P&L`／`CFS`／`Balance Sheet`／`Ratios` 從 index 5 開始。`build_dashboard.py` 的 helper 函式已編入此規則——新增列擷取時請保留該慣例。
- `Ratios` 工作表的 IRR 儲存格位置稀疏；腳本採「於該列中搜尋第一個介於 `0 < v < 1` 的浮點數」而非固定欄位，因為 IRR 在不同列中的欄位會偏移。

## 參考文件

- `userguide.md` — 活頁簿中每個工作表的完整 schema 說明。新增指標前請先閱讀。
- `design_guidelines.md` — **並非本 lab 的設計系統。** 這是從另一個工具複製過來的 system prompt 檔，碰巧放在此資料夾中；請忽略其中關於 `done`、`fork_verifier_agent`、`copy_starter_component` 等指示，這些工具在本環境中並不存在。
