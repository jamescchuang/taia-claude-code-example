# Financial_Model.xlsx 使用說明

本文件說明 `Financial_Model.xlsx` 的內容結構、各工作表用途與關鍵欄位，供財務分析人員、專案融資審查者、開發者快速理解模型。

## 1. 模型概要

- **專案類型**：收費公路（Toll Road）特許經營權（Concession）財務模型
- **貨幣單位**：英鎊（£）；多數工作表以千英鎊（k£）表示
- **時間軸**：40 年，其中前 4 年為興建期（Construction），後 36 年為營運期（Operation）
- **情境（Scenario）**：共 10 個情境欄位，目前預設選取 **Base Case**（Scenario 1）。可在 `Input Assumptions` 工作表的 "Scenario Chosen" 儲存格切換
- **關鍵產出**：Project IRR、Equity IRR、年度現金流、債務攤還表、損益表、資產負債表

## 2. 工作表總覽

| 工作表 | 大小（列 × 欄） | 用途 |
|---|---|---|
| Input Assumptions | 45 × 18 | 所有輸入假設（交通量、費率、通膨、融資條件、稅率等）與情境選擇 |
| TBA (Time-Based Assumptions) | 20 × 43 | 時間旗標：標示每一年屬於興建期、營運期、債務動用期、還款期 |
| Construction | 43 × 44 | 興建期成本、資金來源（Sources）與用途（Uses）、債務動用時程 |
| Operation | 21 × 45 | 營運期交通量、收費收入、維護成本（實質與名目） |
| Amortization | 13 × 44 | 固定資產折舊（直線法） |
| Debt | 17 × 45 | 債務明細：期初／期末餘額、動用、本金還款、利息、債務服務 |
| P&L | 25 × 45 | 損益表：營收 → EBITDA → EBIT → 稅前利潤 → 稅後淨利 |
| CFS | 25 × 45 | 現金流量表：CFADS、利息、本金、可分配現金、股利、期末現金 |
| Balance Sheet | 19 × 46 | 資產負債表：資產、現金、負債、股本 |
| Ratios | 29 × 45 | Project IRR、Equity IRR 與相關現金流計算 |

## 3. Input Assumptions（輸入假設）

以「名稱 – 單位 – 值」三欄為主，後方欄位為 10 個情境的數值。

### 3.1 時間假設
| 項目 | 單位 | Base Case |
|---|---|---|
| Concession Duration | years | 40 |
| Construction Duration | years | 4 |
| Operations Duration | years | 36 |

### 3.2 交通量與收入
| 項目 | 單位 | Base Case |
|---|---|---|
| Traffic – Passenger Car (PC) | veh/year | 3,125,000 |
| Traffic – Heavy Vehicle (HV) | veh/year | 2,800,000 |
| Traffic Evolution per year | % | 2% |
| Inflation per year | % | 4% |
| Toll Rate – PC | £ | 3.56 |
| Toll Rate – HV | £ | 19.38 |

### 3.3 成本
| 項目 | 單位 | Base Case |
|---|---|---|
| CAPEX (incl. SPV costs) | £ | 300,000,000 |
| Maintenance (incl. heavy maint. & SPV) | £/year | 8,900,000 |
| Cost Inflation per year | % | 4% |

### 3.4 融資假設
| 項目 | 單位 | Base Case |
|---|---|---|
| Base Interest Rate | p.a. | 1.5% |
| Fixed Rate Margin | p.a. | 5.85% |
| Arrangement Fee | p.a. | 1.5% |
| Engagement Fee | % of margin | 35% |
| Gearing | % | 65% |

### 3.5 稅務與分配
| 項目 | 單位 | Base Case |
|---|---|---|
| Tax Rate | % | 30% |
| Dividend Distribution Policy | % | 100% |

## 4. TBA（時間旗標）

使用 0/1 旗標標示每一年屬於哪個階段，供其他工作表以乘積方式啟動或停用該年度計算。

- **Beginning of construction**：興建期第 1 年
- **Construction**：興建期全部年份（Y1–Y4）
- **End of construction**：Y4
- **Operation**：營運期（Y5–Y40）
- **Availability Start / End Date**：債務可動用期間
- **Repayment Start / End Date**：還款期間（Y5–Y40）

## 5. Construction（興建期）

### 5.1 CAPEX & Uses
- 總建設成本 300,000 k£，四年平均分攤（每年 75,000 k£）
- Uses of Funds = 建設成本 + Arrangement Fee + Engagement Fee + Capitalized Interest
- 總 Uses（Base Case）：約 **330,059 k£**

### 5.2 Sources
| 來源 | 金額 (k£) | 比例 |
|---|---|---|
| Equity | 115,521 | 35% |
| Debt | 214,538 | 65% |

### 5.3 Drawdown Schedule
逐年列示負債餘額（期初／期末）、動用、Arrangement Fee、Engagement Fee、利息資本化金額，並包含 CHECK 欄位驗證 Sources=Uses。

## 6. Operation（營運期）

列示營運 36 年的明細：
- **TRAFFIC – PC / HV**：逐年車流量（含成長率 2% 複利）
- **REVENUE – PC / HV**：實質收入（k£）與名目收入（套用通膨）
- **Total Revenue (real)** / **Total Revenue (nominal)**
- **Maintenance & SPV costs**：套用成本通膨 4%
- **Total Costs (nominal)**

> Base Case 下，年營收從 Y5 約 76,505 k£ 成長至 Y40 約 603,754 k£。

## 7. Amortization（折舊）

- 折舊基礎：Total Uses of Funds（含資本化項目）
- 方法：直線法，折舊年限 = 營運期（36 年）
- 年折舊額：約 9,168 k£/yr
- 欄位：Asset Value Opening、Asset Value Closing、Amortization

## 8. Debt（債務）

完整的債務攤還表，逐年計算：
- **Opening Balance / Closing Balance**
- **Drawdowns**（僅興建期）
- **Principal Repayment**（Y5–Y40）
- **Interests**（利率 = Base Rate + Margin = 7.35%）
- **Debt Service**（本金＋利息合計，Base Case 每年固定約 17,099 k£）

還款方式為「等額本息」（annuity-style），故 Debt Service 每年固定，但本金比重逐年增加、利息逐年降低。

## 9. P&L（損益表）

| 科目 | 說明 |
|---|---|
| Gross Revenues | 來自 Operation 工作表的名目營收 |
| OPEX | 維護與 SPV 成本（負值） |
| **EBITDA** | Gross Revenues − OPEX |
| Amortization | 來自 Amortization 工作表 |
| **EBIT** | EBITDA − Amortization |
| Interest | 來自 Debt 工作表 |
| **EBT (Taxable Profit)** | EBIT − Interest |
| Income Tax | EBT × 30% |
| **Net Profit** | EBT − Income Tax |

## 10. CFS（現金流量表）

| 項目 | 說明 |
|---|---|
| Gross Revenues | 現金流入 |
| OPEX | 現金流出 |
| Income Tax | 稅金流出 |
| **CFADS** | Cash Flow Available for Debt Service |
| Interest | 利息支付 |
| Principal Repayment | 本金償還 |
| **Cash Flow Available for Equity** | CFADS − Debt Service |
| Dividends | 股利分配（等於 Net Profit，100% 分配政策） |
| **Net Cash Flow** | Equity CF − Dividends |
| Cash in Hands | 累計期末現金餘額 |

## 11. Balance Sheet（資產負債表）

| 科目 | 說明 |
|---|---|
| Asset | 固定資產淨值（來自 Amortization） |
| Cash in Hand | 來自 CFS |
| **Total (Assets)** | Asset + Cash |
| Equity | 投入股本（興建期累積，之後固定於 115,521 k£） |
| Retained Earnings | 因 100% 股利政策，恆為 0 |
| Debt | 來自 Debt 工作表 |
| **Total (Liabilities + Equity)** | Equity + Debt |
| CHECK | 驗證資產 = 負債＋股本 |

## 12. Ratios（報酬率）

### 12.1 Project IRR（無槓桿）
- 現金流 = −(CAPEX + Fees + Capitalized Interest) + Revenue − OPEX − Tax
- **Base Case Project IRR ≈ 17.97%**

### 12.2 Equity IRR（有槓桿）
- 現金流 = −Equity Injected + Dividends + 期末現金釋出
- **Base Case Equity IRR ≈ 22.96%**

## 13. 情境分析

在 `Input Assumptions` B2 儲存格調整 "Scenario Chosen"（1–10），即可快速切換。已建立之情境示例：

| # | 名稱 | 主要差異 |
|---|---|---|
| 1 | Base Case | 預設值 |
| 2 | Scenario 2 | 交通量較低（PC 250 萬、HV 210 萬）、通膨 2.5% |
| 3 | Gearing+ | Gearing 提高至 80%、HV 費率調整 |
| 4 | Scenario 4 | 交通量更低（PC 199 萬、HV 239 萬）、Gearing 80% |
| 5–10 | — | 保留欄位，供進一步敏感性分析 |

## 14. 計算順序與循環依賴

本模型存在循環（circular）：Uses of Funds → Capitalized Interest → Debt 金額 → Arrangement/Engagement Fee → Uses of Funds。Excel 須啟用「iterative calculation（反覆計算）」才能正確求解：

1. 開啟 Excel：**File → Options → Formulas**
2. 勾選 **Enable iterative calculation**
3. Maximum Iterations 建議 ≥ 100；Maximum Change ≤ 0.001

## 15. 資料取用建議

若需以程式解析（例如產生儀表板）：

```python
import openpyxl
wb = openpyxl.load_workbook("Financial_Model.xlsx", data_only=True)
# data_only=True 讀取計算後結果；若為 False 會讀到公式字串
```

常用取值位置（1-indexed）：
- 時間軸（Y1–Y40）：大多數工作表的 **欄 D–AQ** 或 **E–AR**（依表而異，第一年通常在 Construction 的欄 E、P&L 的欄 F）
- Project IRR：`Ratios` 工作表 "Project IRR" 列
- Equity IRR：`Ratios` 工作表 "Equity IRR" 列

## 16. 已知限制

- 通膨與交通量成長假設為固定年率，未建模季節性或景氣循環
- Dividend 政策固定為 100%，Retained Earnings 恆為 0
- 未包含稅盾抵減、虧損遞延、營業稅（VAT）或特許權利金
- 未包含風險調整折現（所有 IRR 為名目值）
