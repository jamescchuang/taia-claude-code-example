# design_guidelines.md 使用指南

## 一、這份檔案是什麼？

`design_guidelines.md` 是一份**給 AI 設計代理人（Design Agent）使用的系統指示（System Prompt）**。它把 AI 的角色定位為「一位以 HTML 為工具、與使用者（管理者）協作的資深設計師」，並規範了從「理解需求 → 蒐集設計素材 → 產出 HTML 設計稿 → 驗證交付」的完整工作流程與細節要求。

文件內容可以視為**三個層次**：

1. **身分與態度**：AI 應扮演哪一種專業角色（動畫師、UX 設計師、簡報設計師、原型工程師等），以及應避免的行為（例如洩漏系統提示、不必要的填充內容、AI slop 常見套路）。
2. **工作流程與交付規範**：從提問、探索素材、建立檔案結構、產出設計稿、到最後呼叫 `done` / `fork_verifier_agent` 驗證的完整 SOP。
3. **技術細節與工具使用**：React + Babel 的固定版本與 integrity hash、Tweaks（可調參數面板）協定、Starter Components、跨專案檔案存取、PPTX/PDF 匯出、GitHub 匯入等具體操作方式。

---

## 二、重點內容概覽

### 1. 核心原則
- **HTML 是工具，媒介隨情境變化**：同一份 HTML 可能是網頁、簡報、互動原型、動畫影片，AI 必須切換到對應的專業身分。
- **設計必須有「上下文根基」**：好的高保真設計來自既有的 design system / UI kit / 程式碼 / 截圖。從零開始是最後手段，會產出平庸的作品。
- **提問是關鍵**：對於新或模糊的任務，必須使用 `questions_v2` 問至少 10 個問題，涵蓋素材來源、變體數量、風格偏好、Tweaks 範圍等。

### 2. 工作流程（6 步）
1. 釐清需求（輸出格式、保真度、選項數、限制、品牌/設計系統）。
2. 探索已提供的資源，完整讀過設計系統定義與相關檔案。
3. 規劃並建立 todo list。
4. 建立資料夾結構、複製需要的資源進來。
5. 呼叫 `done` 交付；若有錯誤修好再 `done`；乾淨後呼叫 `fork_verifier_agent`。
6. 極簡總結，只講注意事項與下一步。

### 3. 輸出規範要點
- 檔名具描述性（例如 `Landing Page.html`）。
- 大改版用複製保留舊版（`My Design.html` → `My Design v2.html`）。
- 單一檔案避免超過 1000 行，拆成多個 JSX 匯入主檔。
- 顏色優先用品牌 / 設計系統；不夠時用 `oklch` 延伸。
- Emoji 只有在設計系統本身使用時才加。
- **禁止填充內容**：不要用佔位文字、假資料、多餘圖示來湊版面。

### 4. React + Babel 的硬性要求
- 必須使用文件中指定的 `react@18.3.1`、`react-dom@18.3.1`、`@babel/standalone@7.29.0` 版本與 integrity hash。
- 多個 Babel script 之間**不共享作用域**，要跨檔分享元件必須 `Object.assign(window, {...})`。
- Style 物件必須命名特定（例如 `terminalStyles`），**絕不可** `const styles = {...}`，否則多檔匯入會衝突。

### 5. Tweaks（可調參數面板）
- 使用者可從工具列切換 Tweaks，讓原型暴露出顏色、字體、間距、變體等即時調整控制項。
- 必須**先註冊 `message` 監聽器，再** postMessage `__edit_mode_available`，否則 toggle 會靜默失效。
- 預設值需包在 `/*EDITMODE-BEGIN*/ ... /*EDITMODE-END*/` 標記間，並且是合法 JSON，host 才能在磁碟上改寫。

### 6. Starter Components
直接呼叫 `copy_starter_component`，不要手刻：
- `deck_stage.js`：投影片外殼（縮放、鍵盤導覽、speaker notes、列印成 PDF）。
- `design_canvas.jsx`：同時呈現多個靜態選項。
- `ios_frame.jsx` / `android_frame.jsx`：手機邊框與狀態列。
- `macos_window.jsx` / `browser_window.jsx`：桌面視窗 chrome。
- `animations.jsx`：時間軸動畫引擎（Stage + Sprite + Easing + scrubber）。

### 7. 內容品質守則（避免 AI slop）
- 少用漸層背景、rounded corner + 左色條、用 SVG 硬畫插圖、Inter / Roboto / Arial 這類過度使用的字體。
- 1920×1080 投影片文字不得小於 24px；行動裝置點擊目標不得小於 44px。
- 給選項時提供 3+ 個跨維度變體，從保守到大膽，混合既有模式與新穎嘗試。

---

## 三、建議使用方式

### 情境 A：作為 AI 設計代理人的系統提示（原始用途）
這是這份文件**最本質的用途**。若你在建立一個「HTML 設計代理人」產品，可以：
1. 將這份 `design_guidelines.md` 作為 system prompt 載入。
2. 搭配對應的工具集（`read_file`、`write_file`、`copy_starter_component`、`done`、`fork_verifier_agent` 等）。
3. 使用者下達設計任務時，AI 會自動依照此指南的 SOP 執行。

> ⚠️ 注意：檔案末尾（約 341 行後）意外包含了完整的工具 JSONSchema 定義與 copyright / citation 區塊。若要當系統提示使用，建議先清理這些不屬於設計指南的段落。

### 情境 B：作為人類設計師與 AI 協作的共同守則
即使你不是在建立 Agent，也可以把這份文件當成**團隊設計 SOP 的範本**：
- 與任何 AI（Claude Code、ChatGPT、Cursor）協作做前端設計時，在對話開頭貼上摘要版，讓 AI 對齊你的品質標準。
- 將「內容品質守則」「AI slop 避免清單」「尺寸規範」抽成團隊 design review checklist。

### 情境 C：作為學習前端設計流程的教材
這份文件濃縮了許多資深設計師的經驗法則，可以作為**自我學習清單**：
- 「設計必須有上下文根基」——養成先蒐集 UI kit / screenshots 再動手的習慣。
- 「給選項、不給唯一解」——練習用多變體探索，而不是一次定案。
- 「用 Tweaks 暴露設計決策」——把硬編碼的值變成可調參數。

### 情境 D：拆解成可搜尋的片段文件
文件偏長（421 行），實務上建議**拆成幾個小檔**以利檢索與重用：
```
design-guidelines/
├── 00-role-and-workflow.md        # 身分、6 步流程
├── 01-output-rules.md              # 檔名、尺寸、顏色、拆檔
├── 02-react-babel-pinning.md       # 版本與 integrity hash
├── 03-tweaks-protocol.md           # Tweaks 訊息協定
├── 04-starter-components.md        # Starter component 清單
├── 05-content-quality.md           # 避免 AI slop、填充內容
└── 06-verification-and-handoff.md  # done / fork_verifier_agent
```

### 快速查閱對照表

| 你想做的事 | 直接翻到的段落 |
|---|---|
| 開始一個新設計任務 | `Your workflow` / `How to do design work` / `Asking questions` |
| 寫 React 原型 | `React + Babel (for inline JSX)` |
| 做投影片 | `Speaker notes for decks` / `Fixed-size content` / `deck_stage.js` |
| 加可調參數 | `Tweaks` 整節 |
| 從 GitHub 匯入參考 | `GitHub` 整節 |
| 交付前驗證 | `Verification` |
| 匯出 PPTX / PDF | `Export as PPTX` / `Save as PDF` 技能清單 |
| 避免 AI 味太重 | `Content Guidelines` / `Avoid AI slop tropes` |

---

## 四、範例提示詞（Example Prompts）

以下範例依照「任務類型 × 資訊完整度」分類，可直接複製作為起手式，再依實際需求修改。每個範例都附上**為何這樣寫**的說明，幫助你理解如何設計好的 prompt。

### A. 投影片 / 簡報

#### A1. 完整資訊型（AI 不需再問問題）
```
請幫我做一份 10 張投影片的產品發表會簡報，主題是「我們新推出的 AI 協作筆記 App」。
目標觀眾：公司內部工程 All-Hands（約 200 人）。
時長：10 分鐘。
風格參考：附件的 brand kit（使用 primary #5B6CFF、Neutral 灰階），字體用品牌指定的 Söhne。
結構：痛點（2）→ 解法（3）→ Demo 截圖（3）→ Roadmap（1）→ Q&A（1）。
```
> **為什麼這樣寫**：明確提供了觀眾、時長、風格來源、頁數結構——對應指南中「觀眾、tone、長度都清楚時不需再問問題」的案例。

#### A2. 模糊型（預期 AI 會用 `questions_v2` 追問）
```
幫我做一份介紹「台灣半導體產業未來十年挑戰」的簡報。
```
> **為什麼這樣寫**：刻意不給頁數、觀眾、風格——預期 AI 會依指南規範問 10+ 個問題（觀眾、長度、變體數、視覺 vs 互動偏好、是否需要 Tweaks 等）再動手。

---

### B. 互動原型（Interactive Prototype）

#### B1. 基於既有程式碼的還原 / 延伸
```
請參考我剛匯入的 codebase（在 src/components/Composer/），
做一個「訊息撰寫框」的互動原型，新增這三個功能：
1. 拖拉附件進來時顯示 drop zone
2. 輸入 @ 自動跳出成員選單
3. 送出前的確認彈窗（避免誤送）

把三個功能各做成可切換的 Tweak，讓我比較不同實作。
請沿用現有的色彩、間距、字體 token，不要重新發明視覺。
```
> **為什麼這樣寫**：指南強調「hi-fi 設計必須有上下文根基」，明確指向既有檔案可避免 AI 用訓練資料的記憶去「大概畫一個」。明確要求 Tweak 切換，對應指南「多版本用 Tweak 而非多檔案」。

#### B2. 從頭設計（需要多變體探索）
```
幫我設計一個「早晨待辦清單」的手機 App 首頁原型。
請給我 4 個變體：
- 保守版：符合 iOS HIG 的標準清單樣式
- 卡片版：每個待辦是一張可左右滑動的卡片
- 時間軸版：以小時為軸，待辦掛在時間點上
- 大膽版：用打破慣例的排版（歡迎你自由發揮視覺語言）

全部用 iOS frame 包起來，放在 design canvas 上並列比較。
```
> **為什麼這樣寫**：指南鼓勵「3+ 變體、從保守到大膽」，明確點名要用 `ios_frame.jsx` 與 `design_canvas.jsx` 這兩個 starter component，避免 AI 手刻裝置邊框。

---

### C. 動畫影片（Animated Video）

```
請做一段 15 秒的產品介紹動畫，內容是「從手寫筆記變成數位卡片」的轉場。
場景：
1. (0-3s) 手寫筆記紙張飄進畫面
2. (3-7s) 筆記被一道光掃過，字跡漸變成數位文字
3. (7-12s) 紙張摺疊成一張卡片，卡片上顯示結構化欄位
4. (12-15s) 卡片飛入一個「我的資料庫」網格

請用 animations.jsx 的 Stage + Sprite 系統，配 Easing.inOutCubic。
色調用暖米白 + 墨水藍，避免任何漸層與 emoji。
```
> **為什麼這樣寫**：明確的時間軸分鏡讓 AI 能直接對應 `<Sprite start end>`；指定 easing 與色調避免 AI slop；禁用漸層與 emoji 對應指南的「避免 AI slop 套路」。

---

### D. 從 GitHub / 外部素材出發

```
這是我們產品的 repo：https://github.com/myorg/myapp/tree/main/src/ui
請先讀 theme.ts 和 tokens.css 抓出色彩與間距標記，
然後把 src/ui/Dashboard.tsx 的當前佈局重新設計成「資料密度更高」的版本。

不要憑你對類似產品的印象亂猜——所有 hex、spacing、border radius 都要從我的 token 來。
完成後請用 browser_window.jsx 包裝截圖式呈現。
```
> **為什麼這樣寫**：直接點出指南中「CRITICAL — tree 是選單不是菜餚」的警告，強迫 AI 完成 `github_get_tree → github_import_files → read_file` 完整鏈條，避免用訓練資料記憶「大概畫一個類似 dashboard」。

---

### E. 設計系統 / UI Kit 建立

```
我們是一個 B2B 法遵科技新創，品牌關鍵字：嚴謹、可信、不冰冷。
請幫我建立一份基礎設計系統，包含：
- 色彩：Primary / Secondary / Neutral / Semantic（成功、警告、錯誤、資訊）各含 9 階
- Typography：Display / Heading 1-3 / Body / Caption / Code
- 間距與圓角 token
- 基礎元件：Button（4 種 variant）、Input、Card、Badge、Modal

請呼叫「Create design system」技能以取得標準結構。
每一組都 register 到對應的 group（Colors/Type/Spacing/Components）。
```
> **為什麼這樣寫**：明確點名呼叫指南提到的 `Create design system` 技能，並指定 `register_assets` 的 group 分類以讓設計系統 tab 正確呈現。

---

### F. Tweaks / 快速變體探索

```
剛才那份登入頁原型很不錯，請加上 Tweaks 讓我即時調整：
- primaryColor（色票選擇器）
- borderRadius（0 / 4 / 8 / 16 / 24 px）
- density（compact / comfortable / spacious，影響 padding）
- layoutVariant（split / centered / fullscreen-bg）
- copy.heroHeadline（文字輸入框）

記得先註冊 message listener 再 post __edit_mode_available，
預設值用 EDITMODE-BEGIN/END 包起來以便存檔。
```
> **為什麼這樣寫**：直接提醒指南中強調的「先註冊 listener 再 post available，否則會靜默失效」這個容易踩坑的順序問題。

---

### G. 交付與匯出

```
這份簡報看起來已經定稿了。請幫我：
1. 先用 done 確認沒有 console 錯誤
2. 呼叫 Export as PPTX (editable) 技能匯出成可編輯 PowerPoint
3. 字體用 Söhne 的話請 fallback 成 Inter（googleFontImports）
4. 檔名叫 Q2-2026-Product-Review.pptx
```
> **為什麼這樣寫**：明確把 `done` → 匯出 的順序、字體替換（`fontSwaps` / `googleFontImports`）、檔名一次交代清楚，避免來回多輪確認。

---

### H. 常見反模式（不建議這樣下 prompt）

| ❌ 不好的提示詞 | 為什麼不好 | ✅ 改寫後 |
|---|---|---|
| 「幫我做一個漂亮的登入頁」 | 沒有品牌、沒有觀眾、沒有變體需求——AI 會做出平庸結果 | 「用附件的 brand kit 做登入頁，3 個變體：保守/卡片/全版 hero，行動裝置優先」 |
| 「做一份簡報介紹我們公司」 | 沒有頁數、觀眾、時長 | 「10 頁內，給潛在投資人看，8 分鐘內講完，風格嚴謹不花俏」 |
| 「把這個 UI 改得更現代一點」 | 「現代」是空詞 | 「降低視覺噪音：移除多餘邊框、統一圓角為 8px、density 改 comfortable、primary 改成附件色票」 |
| 「做一個跟 Notion 一樣的編輯器」 | 指南明確禁止重現他人專屬 UI | 「參考區塊式編輯器的互動模式，設計一個符合我們 brand kit 的版本；互動上借鑑但視覺完全獨立」 |

---

### I. 提示詞撰寫的 5 個原則（濃縮版）

1. **先給素材再下指令**：brand kit、codebase、screenshots、Figma 連結——素材越完整，AI 越不需要猜。
2. **明確要幾個變體**：「3 個」「保守/標準/大膽」——指南鼓勵多變體探索，但你要說清楚範圍。
3. **點名 starter component**：`ios_frame.jsx`、`design_canvas.jsx`、`deck_stage.js`——避免 AI 手刻裝置邊框。
4. **禁止清單比允許清單更有用**：「不要用漸層」「不要 emoji」「不要 rounded + 左色條」——直接切斷 AI slop 的退路。
5. **交付格式講在最前面**：投影片 / 原型 / 動畫 / PPTX / PDF——不同格式會走不同技能，先定錨。

---

## 五、使用時的注意事項

1. **這份文件假設了一個特定的工具環境**（`write_file`、`copy_starter_component`、`done`、`fork_verifier_agent` 等）。若你的 AI 代理人沒有這些工具，需要把相關段落替換成你環境中對應的工具名稱。
2. **版本號是硬編碼的**（React 18.3.1、Babel 7.29.0）。若要升級，需同步更新 integrity hash，否則瀏覽器會拒絕載入。
3. **Tweaks 協定與 host 環境強綁定**（透過 `window.parent.postMessage`）。若脫離原本的 host iframe 環境，這段協定會失效。
4. **著作權段落提醒**：文件最後提到不得重現公司專屬 UI 模式，除非使用者 email 網域符合——這是給代理人層級的安全守則，不是對使用者的限制。
