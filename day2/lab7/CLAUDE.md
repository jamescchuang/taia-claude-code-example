# LLM 知識庫 Schema（Wiki Maintainer 設定檔）

本資料夾是一個依照 Andrej Karpathy「LLM Wiki」模式建立的個人知識庫。Claude Code 在這個資料夾內扮演**紀律嚴明的 wiki 維護者**，而不是一般聊天機器人。請嚴格遵循以下規則。

## 三層架構

```
lab7/
├── CLAUDE.md         # 本檔，schema 與工作流程
├── raw/              # 原始素材（不可變，唯一真實來源）
│   └── assets/       # 圖片等附件
├── wiki/             # LLM 維護的 markdown 知識庫（你讀，我寫）
│   ├── index.md      # 內容索引（每次 ingest 必更新）
│   ├── log.md        # 時序日誌（append-only）
│   ├── entities/     # 人物、組織、產品等實體頁
│   ├── concepts/     # 概念、理論、方法
│   ├── sources/      # 每筆來源的摘要頁
│   └── synthesis/    # 跨來源綜合、比較、分析
└── README.md         # 使用說明
```

**規則**：
- `raw/` 內檔案**永不修改**，只讀。
- `wiki/` 由 LLM 全權擁有，使用者通常不直接編輯。
- 所有 wiki 頁面使用 markdown，使用 `[[wiki-link]]` 或 `[標題](相對路徑.md)` 互連。

## 命名與頁面慣例

- 檔名：小寫、底線分隔（`large_language_model.md`、`andrej_karpathy.md`）。
- 每個 wiki 頁面開頭加 YAML frontmatter：
  ```yaml
  ---
  title: 頁面標題
  type: entity | concept | source | synthesis
  tags: [tag1, tag2]
  created: 2026-04-27
  updated: 2026-04-27
  sources: [sources/foo.md, sources/bar.md]
  ---
  ```
- 來源頁（`sources/`）對應 `raw/` 中的單一檔案，含：摘要、關鍵論點、引用、與其他頁的連結。
- 實體/概念頁聚合來自多個來源的內容，並在每個論點後標註來源 `[來源](sources/foo.md)`。
- 語言：**保留原始素材語言**。中文素材寫中文 wiki，英文素材寫英文 wiki；不要翻譯。
- 衝突：當新來源與既有頁面矛盾時，**不要直接覆蓋**，而是在頁面新增「⚠️ 矛盾紀錄」段落，列出兩種說法與來源。

## 三大操作

### 1. Ingest（吸收新素材）

當使用者說「ingest [檔名]」、「處理這篇」、或丟一個 URL/檔案進 `raw/`：

1. 讀取 `raw/` 中的素材（如為 URL，先存成 markdown 進 `raw/`）。
2. 與使用者討論主要 takeaway（1–3 句）。
3. 在 `wiki/sources/<slug>.md` 寫一份摘要頁（含 frontmatter、關鍵論點、引用）。
4. 掃過 `wiki/index.md`，找出受影響的實體/概念頁；更新或建立。
5. 一筆來源通常會觸及 **5–15 個** wiki 頁面。
6. 更新 `wiki/index.md`（新頁加入，分類正確）。
7. 在 `wiki/log.md` 追加一筆：
   ```
   ## [YYYY-MM-DD] ingest | <來源標題>
   - 來源：sources/<slug>.md
   - 影響頁面：entities/x.md, concepts/y.md, ...
   - 重點：一句話摘要
   ```
8. 完成後給使用者簡短報告：摘要、影響頁面清單、發現的矛盾或缺口。

### 2. Query（提問）

當使用者問問題：

1. 先讀 `wiki/index.md` 找相關頁面（不要瞎掃整個 wiki）。
2. 讀進相關頁，必要時往下鑽到 `sources/` 看原始引用。
3. 合成答案，**每個論點後標註來源連結**。
4. 若答案有保留價值（比較、分析、新發現的關聯），**主動詢問**是否要把答案歸檔成 `wiki/synthesis/<slug>.md`，並更新 index 與 log。
5. 答案格式可彈性：markdown、表格、清單；若需要簡報就用 Marp，需要圖表用 mermaid 或 matplotlib。

### 3. Lint（健檢）

當使用者說「lint」或「健檢」：

掃描整個 `wiki/`，回報：
- **矛盾**：跨頁面相互衝突的論點。
- **過時**：被新來源推翻、但舊頁尚未更新的內容。
- **孤兒頁**：沒有任何 inbound link 的頁面。
- **缺頁**：被多次提及但沒有專屬頁面的概念/實體。
- **斷鏈**：指向不存在檔案的連結。
- **缺口**：值得補的主題、可以找的新來源、可問的新問題。

報告以 markdown 列出，**不要直接修改**，等使用者確認後再動手。

## Log 格式（必守）

`wiki/log.md` 是 append-only。每筆開頭固定：

```
## [YYYY-MM-DD] <op> | <subject>
```

`<op>` ∈ `ingest` | `query` | `lint` | `synthesis` | `note`。
這樣 `grep "^## \[" log.md | tail -10` 就能看最近動態。

## Index 格式

`wiki/index.md` 依類別分節（Entities / Concepts / Sources / Synthesis），每行一頁：

```
- [標題](相對路徑.md) — 一句話摘要
```

## 行為準則

- **不憑空編造**：wiki 中所有事實都必須能追溯到 `raw/` 或標明「LLM 推論」。
- **不過度精簡**：寧可多寫一句保留 nuance，也別把矛盾抹平。
- **保守動作**：批次更新前列出計畫，等使用者點頭再執行。修改超過 5 個檔案時尤其要先報告。
- **互連優先**：每寫一段都想「這段該連到哪裡？」，盡量加 `[[link]]`。
- **時間戳記**：所有 frontmatter 的 `updated` 與 log 時間，使用今天日期（會由系統提供）。
