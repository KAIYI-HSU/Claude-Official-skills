# 文件處理類 Skills

這 5 個 skills 構成 Anthropic 在 Claude.ai 內提供「建立／編輯文件」能力的核心。其中 docx/pdf/pptx/xlsx 是 source-available（非 Apache 2.0），因為它們正在生產環境運行。

| Skill | 主要產物 | 必裝依賴 |
|-------|----------|----------|
| [docx](./docx.md) | `.docx` | `npm install -g docx`、pandoc、LibreOffice |
| [pdf](./pdf.md) | `.pdf` | `pip install pypdf pdfplumber reportlab`、qpdf、poppler |
| [pptx](./pptx.md) | `.pptx` | `npm install pptxgenjs`、LibreOffice、markitdown |
| [xlsx](./xlsx.md) | `.xlsx` | `pip install openpyxl pandas`、LibreOffice |
| [doc-coauthoring](./doc-coauthoring.md) | 任意文件 | 純流程，無依賴 |

## 共通設計模式

### 1. ZIP-XML Unpack/Pack 三步驟（docx + pptx + xlsx）

`.docx`、`.pptx`、`.xlsx` 本質上都是 ZIP 內含 XML 檔。三者共用 `scripts/office/` 工具集：

```bash
python scripts/office/unpack.py document.docx unpacked/   # 1. 拆解
# 編輯 unpacked/word/document.xml ...                     # 2. 編輯 XML
python scripts/office/pack.py unpacked/ output.docx        # 3. 重組
python scripts/office/validate.py output.docx              # 驗證
```

### 2. Pandoc 與 markitdown 作為 Reader

讀取現成文件不要自己解析，用工具：
- `pandoc --track-changes=all document.docx -o output.md`
- `python -m markitdown presentation.pptx`

### 3. LibreOffice 作為「最後手段」

複雜的計算（xlsx 公式重算、tracked changes 接受、PDF 轉換）統一用 `soffice` headless 模式：

```bash
python scripts/office/soffice.py --headless --convert-to pdf document.docx
```

---

## 推薦學習順序

1. **doc-coauthoring** — 純流程概念，先理解「如何結構化共筆」
2. **pdf** — 最容易上手，Python 一條龍
3. **docx** — 進入 XML 操作的入門款
4. **xlsx** — 公式邏輯重要，學「絕對不要硬編碼數字」
5. **pptx** — 集大成，含視覺 QA 與設計哲學
