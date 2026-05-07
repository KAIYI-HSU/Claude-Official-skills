# docx — Word 文件全能助手

## 一句話定位

用 `docx-js`（JavaScript）建立、用 `unpack/pack` XML 工具編輯 `.docx` 檔，涵蓋追蹤修訂、註解、TOC、頁首頁尾、多欄排版、嵌入圖片等所有 Word 進階特性。

## 何時觸發

- 使用者提到 "Word doc"、"word document"、"`.docx`"、"備忘錄"、"報告"、"信件"
- 要求製作含 TOC、頁碼、頁首／頁尾的專業文件
- 需要處理 tracked changes 或 comments
- 從 `.docx` 抽取或重組內容、做 find-and-replace、嵌入圖片

不適用於：PDF、試算表、Google Docs、與文件無關的程式任務。

## 目錄結構速覽

```
skills/docx/
├── SKILL.md                 # 主指引（~600 行）
├── LICENSE.txt              # Anthropic 自有授權
└── scripts/
    ├── comment.py           # 自動產生 comments.xml + 標記
    ├── accept_changes.py    # 接受所有追蹤修訂（用 LibreOffice）
    ├── templates/           # comments / commentsExtended / people 範本
    └── office/              # 共享工具（與 pptx/xlsx 共用）
        ├── unpack.py        # .docx → 解壓 + 美化 XML + 智慧引號實體化
        ├── pack.py          # 資料夾 → .docx + 自動修正
        ├── validate.py      # 驗證 OOXML schema
        ├── soffice.py       # LibreOffice headless 包裝
        └── helpers/
            ├── merge_runs.py
            └── simplify_redlines.py
```

## 核心觀念與工作流

### 任務 → 工具對應表

| 任務 | 方案 |
|------|------|
| 讀取／分析內容 | `pandoc` 或 `unpack.py` 看原始 XML |
| 建立新文件 | `docx-js`（JavaScript） |
| 編輯既有文件 | unpack → 編輯 XML → pack |

### 建立新文件（docx-js 樣板）

```javascript
const { Document, Packer, Paragraph, TextRun, PageOrientation } = require('docx');

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 24 } } }, // 12pt
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },  // US Letter（DXA）
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    children: [
      new Paragraph({ children: [new TextRun("Hello")] })
    ]
  }]
});

Packer.toBuffer(doc).then(buf => fs.writeFileSync("doc.docx", buf));
```

**DXA 單位換算**：1440 DXA = 1 inch；US Letter 是 12240×15840、A4 是 11906×16838（docx-js 預設是 A4，務必明寫）。

### 編輯既有文件（三步驟）

```bash
# 1) 拆解：自動美化 XML、合併相鄰 run、智慧引號→XML 實體
python scripts/office/unpack.py document.docx unpacked/

# 2) 編輯 unpacked/word/document.xml（直接用 Edit tool 替換字串，不要寫 Python 腳本）

# 3) 重組：自動驗證、修正 durableId、補 xml:space="preserve"
python scripts/office/pack.py unpacked/ output.docx --original document.docx
```

## 精華 Script 與可提取資源

### 🔧 `scripts/office/unpack.py`（極具重用價值）

把任何 `.docx` / `.pptx` / `.xlsx` 拆成可編輯的 XML 樹，且：
- 自動美化排版
- 合併連續 `<w:r>` runs（讓 find-replace 更可靠）
- 智慧引號 (' ' " ") 自動轉成 `&#x2019;` 等 XML 實體，避免編輯時被破壞

### 🔧 `scripts/office/pack.py`

逆操作。額外提供 **auto-repair**：
- `durableId >= 0x7FFFFFFF` → 自動重新生成
- `<w:t>` 含前後空白 → 自動補 `xml:space="preserve"`
- 失敗時清楚告訴你哪裡 schema violation

### 🔧 `scripts/comment.py`

封裝增加註解的 boilerplate（要寫 `comments.xml`、`commentsExtended.xml`、`people.xml` 三個檔）：

```bash
python scripts/comment.py unpacked/ 0 "Comment text with &amp; and &#x2019;"
python scripts/comment.py unpacked/ 1 "Reply text" --parent 0    # 回覆
python scripts/comment.py unpacked/ 0 "Text" --author "Custom"
```

### 🔧 `scripts/accept_changes.py`

```bash
python scripts/accept_changes.py input.docx output.docx
```

底層用 LibreOffice 把追蹤修訂全部接受，輸出乾淨檔。

## 可移植到自家專案的模式

1. **DXA 常數表**：1440 DXA = 1 inch，content width = page width − 左右 margin。建議自家專案內也建一個 `constants.js` 集中管理。

2. **Smart Quote XML 實體對照**：
   ```
   &#x2018;  ‘   左單引號
   &#x2019;  ’   右單引號（撇號）
   &#x201C;  "   左雙引號
   &#x201D;  "   右雙引號
   ```

3. **追蹤修訂 minimal-edit pattern**：
   ```xml
   <w:r><w:t>The term is </w:t></w:r>
   <w:del w:id="1" w:author="Claude" w:date="...">
     <w:r><w:delText>30</w:delText></w:r>
   </w:del>
   <w:ins w:id="2" w:author="Claude" w:date="...">
     <w:r><w:t>60</w:t></w:r>
   </w:ins>
   <w:r><w:t> days.</w:t></w:r>
   ```
   只標記變動的部分，保留前後文，避免「整段被刪重寫」。

4. **Bullet List 正確做法**（非 unicode 字元）：
   ```javascript
   numbering: { config: [
     { reference: "bullets",
       levels: [{ level: 0, format: LevelFormat.BULLET, text: "•" }] }
   ]}
   ```

## 常見陷阱（Gotchas）

⚠️ **以下是 SKILL.md 明確警告的雷區**，可直接複製到自家 docx 專案的 lint 規則：

- ❌ 不要設 `WidthType.PERCENTAGE`（在 Google Docs 會壞）→ ✅ 一律 `WidthType.DXA`
- ❌ 不要直接打 `•` 或 `•` 當 bullet → ✅ 用 `LevelFormat.BULLET` + numbering config
- ❌ 不要用 `\n` 換行 → ✅ 拆成多個 `Paragraph`
- ❌ 不要把 `PageBreak` 獨立成 child → ✅ 必須包在 `Paragraph` 內
- ❌ 不要用 table 當分隔線 → ✅ 用 `Paragraph` 的 `border.bottom`
- ❌ TOC 的 heading 不要套自訂 style → ✅ 只能用內建的 `HeadingLevel.HEADING_1` 等
- ❌ Heading 漏寫 `outlineLevel` → TOC 抓不到
- ❌ Tables 只設 `columnWidths` 不設 cell `width` → 部分平台渲染錯誤
- ❌ `ImageRun` 漏 `type: "png"` → 直接報錯

## 延伸閱讀

- 官方檔：[`skills/docx/SKILL.md`](../../skills/docx/SKILL.md)
- 註解範本：[`skills/docx/scripts/templates/`](../../skills/docx/scripts/templates/)
- 共享 office 工具：[`skills/docx/scripts/office/`](../../skills/docx/scripts/office/)
- 跨 skill office 共通模式：[../99-cross-skill-patterns.md](../99-cross-skill-patterns.md)
