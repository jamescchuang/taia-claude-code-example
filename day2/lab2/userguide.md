# Financial_Model.xlsx 使用說明

## 檔案概述

`Financial_Model.xlsx` 是一份**收費道路 (Toll Road) BOT 專案融資財務模型**，用於模擬一個包含建設期 (Construction) 與營運期 (Operation) 的特許權 (Concession) 專案的完整財務表現。

模型以**英鎊 (£)** 為計價單位，金額多以 **k£ (千英鎊)** 表示，特許期間預設為 **40 年**（4 年建設 + 36 年營運），並支援多情境 (Scenario) 切換分析。

---

## 工作表結構（共 10 個分頁）

模型依照「**輸入 → 時間軸 → 模組計算 → 三大財務報表 → 績效指標**」的邏輯設計：

| 順序 | 分頁名稱 | 類型 | 主要功能 |
|------|---------|------|---------|
| 1 | Input Assumptions | 輸入 | 所有假設輸入與情境切換 |
| 2 | TBA (Time-Based Assumptions) | 計算 | 建立年度時間軸與旗標 (Flags) |
| 3 | Construction | 計算 | 建設期資金來源與動用 |
| 4 | Operation | 計算 | 營運期收入與成本 |
| 5 | Amortization | 計算 | 資產折舊攤提 |
| 6 | Debt | 計算 | 債務償還排程 |
| 7 | P&L | 報表 | 損益表 |
| 8 | CFS | 報表 | 現金流量表 |
| 9 | Balance Sheet | 報表 | 資產負債表 |
| 10 | Ratios | 指標 | IRR 等績效指標計算 |

---

## 各分頁詳細說明

### 1. Input Assumptions（輸入假設）

集中管理所有模型輸入。透過 `Scenario Chosen` 儲存格切換情境 (1–7)，下游分頁會自動引用對應情境的值。

主要假設群組：

- **TIME ASSUMPTIONS**：特許期 40 年、建設期 4 年、營運期 36 年
- **TRAFFIC & REVENUE**：
  - 小客車 (PC) 車流量：3,125,000 veh/year
  - 大型車 (HV) 車流量：2,800,000 veh/year
  - 車流量年成長率：2%
  - 通膨率：4%
  - 過路費：PC £3.56、HV £19.38
- **COSTS DURING CONSTRUCTION**：CAPEX £300,000,000
- **COSTS DURING OPERATION**：每年維護費 £8,900,000
- **PROJECT FINANCING**：
  - 基準利率 1.5%、固定利差 5.85%
  - 安排費 1.5%、承諾費 (Engagement fee) 0.35
  - 槓桿比 (Gearing) 65%
- **TAX & ACCOUNTING**：稅率 30%、股利配發率 100%

情境欄位包含：Base Case、Scenario 2、Gearing+、Scenario 4 等。

### 2. TBA — Time-Based Assumptions（時間軸）

建立特許期 40 年的時間骨架，產出 0/1 旗標供其他分頁使用：

- **PROJECT TIMELINE**：建設起始、建設中、建設結束、營運中
- **DEBT TIMELINE**：可動用起日、動用中、動用結束日、還款起日、還款中、還款結束日

下游所有期間分配（CAPEX、收入、利息等）都透過這些 Flags 控制計算邏輯。

### 3. Construction（建設期模組）

模擬 4 年建設期間的資金流：

- **Uses（資金用途）**：建設成本、安排費、承諾費、資本化利息
- **Sources（資金來源）**：股權 (Equity) 與債務 (Debt) 依槓桿比例配置
- **Debt Drawdown Schedule**：年度動用、期末未償餘額
- **CHECK**：Sources = Uses 的勾稽列

> ⚠️ **循環參照 (Circularity)**：資本化利息與債務動用之間存在循環，需啟用 Excel 的 **iterative calculation**。

### 4. Operation（營運期模組）

計算 36 年營運期間的收入與成本：

- **TRAFFIC**：依年成長率複利計算 PC/HV 車流量
- **REVENUE**：以實質 (real) 與名目 (nominal) 兩種口徑呈現，名目值套用 4% 通膨率
- **COSTS**：維護及 SPV 成本，同樣套用通膨率

### 5. Amortization（折舊攤提）

採用**直線折舊法**將總資產 (£330,058k) 在 36 年營運期間攤銷，呈現每年資產期初/期末帳面值與折舊金額。

### 6. Debt（債務還款排程）

呈現營運期內債務本息償還細節：

- 期初餘額、動用、本金償還、期末餘額
- 利息費用與總債務服務 (Debt Service)
- 採等額償還 (annuity-style) 結構，年度 Debt Service 約 £17,099k

### 7. P&L（損益表）

依會計順序：

```
Gross Revenues − OPEX = EBITDA
EBITDA − Amortization = EBIT
EBIT − Interest = EBT
EBT − Income Tax = Net Profit
```

### 8. CFS（現金流量表）

依瀑布式 (Cash Flow Waterfall) 結構：

```
Gross Revenues − OPEX − Tax = CFADS（債務服務可用現金流）
CFADS − Interest − Principal = Cash Flow Available for Equity
減 Dividends = Net Cash Flow
累計 = Cash in Hand
```

`CFADS` 為專案融資中最關鍵的中介數字，用於計算 DSCR 等覆蓋率指標。

### 9. Balance Sheet（資產負債表）

- **Asset 端**：固定資產 (Asset) + 現金 (Cash in hand)
- **Equity & Liability 端**：股本 (Equity) + 保留盈餘 (Retained Earnings) + 債務 (Debt)
- 含 **CHECK 列**：驗證資產 = 負債 + 權益

### 10. Ratios（績效指標）

計算兩大核心報酬率：

- **Project IRR**（專案內部報酬率）：以總投資 vs. 專案層級現金流計算 → **約 17.97%**
- **Equity IRR**（股權內部報酬率）：以股權投入 vs. 股利收回計算 → **約 22.96%**

---

## 使用流程建議

1. **切換情境**：於 `Input Assumptions!D2` 輸入 1–7 選擇情境
2. **修改假設**：直接調整 `Input Assumptions` 中的 `Values` 欄（D 欄）
3. **檢查循環計算**：確認 Excel 已開啟「啟用反覆計算」(File → Options → Formulas)
4. **驗證勾稽**：查看 `Construction!CHECK` 與 `Balance Sheet!CHECK` 是否皆為 `TRUE`
5. **讀取結果**：於 `Ratios` 分頁查看 Project IRR 與 Equity IRR

---

## 命名與單位慣例

- **k£**：千英鎊 (Thousand GBP)
- **veh/year**：每年車輛數
- **PC**：Passenger Car（小客車）
- **HV**：Heavy Vehicle（大型車）
- **CAPEX**：Capital Expenditure（資本支出）
- **OPEX**：Operating Expenditure（營運支出）
- **SPV**：Special Purpose Vehicle（特殊目的公司）
- **CFADS**：Cash Flow Available for Debt Service
- **DSCR**：Debt Service Coverage Ratio
- **IRR**：Internal Rate of Return
- **BoP / EoP**：Beginning / End of Period

---

## 模型關鍵特性

- ✅ **多情境分析**：透過單一儲存格切換 7 種情境
- ✅ **三表勾稽**：P&L、CFS、Balance Sheet 完整連動
- ✅ **動態時間軸**：以 Flag 驅動建設/營運期切換
- ✅ **循環計算**：建設期資本化利息支援自動疊代
- ✅ **內建檢查**：Construction 與 Balance Sheet 皆有 CHECK 列確保模型平衡
