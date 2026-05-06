# pptx — 簡報製作與視覺 QA 高手

## 一句話定位

用 `pptxgenjs`（JS）建立、用 unpack/pack 編輯 `.pptx`，並提供「色彩 + 字型配對 + 視覺 QA」一整套設計知識，避免 AI 簡報常見的「一張白底配普通藍 bullet」醜樣。

## 何時觸發

- 製作簡報、pitch deck
- 編輯既有 `.pptx`、抽取內容
- 合併或拆解投影片、處理 layout 與 speaker notes

## 目錄結構速覽

```
skills/pptx/
├── SKILL.md           # 主指引（速查 + 工作流）
├── editing.md         # 編輯既有簡報的詳細流程
├── pptxgenjs.md       # 從零建立簡報的 pptxgenjs 完整指南
├── LICENSE.txt
└── scripts/
    ├── thumbnail.py        # 產出投影片格狀縮圖（給 Claude 視覺檢查）
    ├── add_slide.py        # 程式化插入新投影片
    ├── clean.py            # 編輯後清理 XML
    └── office/             # 共享 unpack/pack/validate（同 docx）
```

## 核心觀念與工作流

### 三條路徑

| 任務 | 路徑 |
|------|------|
| 讀取內容 | `python -m markitdown deck.pptx` |
| 編輯既有 | unpack → 改 slide XML → clean → pack |
| 從零建立 | `pptxgenjs`（JS） |

### 視覺 QA 工作流（Anthropic 招牌做法）

1. 用 LibreOffice 把 pptx 轉 PDF：`soffice --headless --convert-to pdf deck.pptx`
2. PDF 轉成投影片縮圖：`pdftoppm -jpeg deck.pdf slide`
3. 用 `scripts/thumbnail.py` 拼成格狀大圖
4. 啟動 **subagent**（fresh eyes）審視，列出：重疊、文字溢出、對齊、對比、留白問題
5. 修正 → 重複 QA

> 這個 fresh-eyes subagent QA pattern 在 [`doc-coauthoring`](./doc-coauthoring.md) 也用，是值得抄到自家專案的精華。

### 設計哲學（從 SKILL.md 萃取）

- **色彩主導 60–70%**：選一個主色佔大面積，避免「處處是藍 bullet」
- **Dark/Light 三明治**：開場深色 → 中段淺色 → 結尾深色，建立節奏
- **視覺母題**：每張投影片有一個「圖形語彙」貫穿（如圓、線條、幾何）
- **配色遠離通用藍**：依主題挑色（金融用 Forest & Moss、科技用 Coral Energy 等 10 種預設）
- **字型配對**：標題用粗壯字（Arial Black、Georgia）配內文（Calibri、Arial），不要全用同字型
- **尺寸標準**：標題 36–44pt、內文 14–16pt

## 精華 Script 與可提取資源

### 🔧 `scripts/thumbnail.py`

把多張投影片拼成一張總覽 PNG，丟給 subagent 做整體視覺審查。**這個概念可以類推到任何「需要全局審視」的 UI 開發**（例如把網站每個頁面截圖拼成一張）。

### 🔧 `scripts/add_slide.py`

程式化插入新投影片並繼承 layout，避免從零拚 XML。

### 🎨 10 套預設配色（從 pptxgenjs.md）

| 主題 | 適用 |
|------|------|
| Midnight Executive | 高階主管簡報 |
| Forest & Moss | 永續、自然議題 |
| Coral Energy | 新創、科技產品 |
| ...（共 10 種）| |

> 📍 **可直接挪用**：複製 hex 碼到自家簡報模板。

### 🔧 編輯既有簡報的 unpack/pack 流程

```bash
python scripts/office/unpack.py deck.pptx unpacked/
# 編輯 unpacked/ppt/slides/slide1.xml
python scripts/clean.py unpacked/                  # 清掉殘留亂碼
python scripts/office/pack.py unpacked/ out.pptx
```

## 可移植到自家專案的模式

1. **Visual QA via subagent**：把產物截圖、丟給另一個 LLM 做新眼睛審查。可寫成 CI step。

2. **配色決策框架**：別問「想要什麼顏色」，改問「主題是什麼／受眾是誰」，再從預設配色挑。

3. **`thumbnail.py` 拼圖思路**：用 PIL 把多張圖排成 grid，加邊框與索引號。50 行可寫完，極實用。

4. **避雷清單**：
   ```
   ❌ 整張投影片只有文字
   ❌ 文字色與背景對比不足（< 4.5:1）
   ❌ 每張投影片都用同一 layout
   ❌ "Click to edit" placeholder 殘留
   ```

## 常見陷阱（Gotchas）

- ❌ 直接用 markitdown 編輯 → 會 lose formatting；✅ 編輯走 unpack/pack
- ❌ 字型沒嵌入 → 別人開啟字會跑掉
- ❌ 用 emoji 當圖示 → 不同平台字型差異大；✅ 用 SVG 或形狀
- ❌ 17pt 內文 → 後排看不到；✅ ≥ 14pt（最好 16pt）
- ❌ 全簡報用同一張 layout → 視覺單調；✅ 變化 layout，但保持母題

## 延伸閱讀

- 官方檔：[`skills/pptx/SKILL.md`](../../skills/pptx/SKILL.md)
- 從零建立詳述：[`skills/pptx/pptxgenjs.md`](../../skills/pptx/pptxgenjs.md)
- 編輯流程詳述：[`skills/pptx/editing.md`](../../skills/pptx/editing.md)
- 視覺 QA 腳本：[`skills/pptx/scripts/thumbnail.py`](../../skills/pptx/scripts/thumbnail.py)
