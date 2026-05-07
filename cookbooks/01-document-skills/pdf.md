# pdf — PDF 全能武器庫

## 一句話定位

把 PDF 任何操作收斂成「pypdf / pdfplumber / reportlab + 命令列工具」三大武器，並提供現成的表單填寫、OCR、加密、浮水印 script。

## 何時觸發

- 任何 `.pdf` 檔的讀寫、合併、拆解、旋轉、加浮水印
- 建立新 PDF、填表單、加密／解密
- 抽取圖片、表格、文字
- OCR 掃描型 PDF

## 目錄結構速覽

```
skills/pdf/
├── SKILL.md                     # 主指引（速查 + Python 模式）
├── REFERENCE.md                 # 進階：pypdfium2、JavaScript pdf-lib、疑難排解
├── FORMS.md                     # 表單填寫專用指南
├── LICENSE.txt
└── scripts/
    ├── fill_fillable_fields.py       # 填寫 PDF 表單欄位
    ├── extract_form_field_info.py    # 列出所有欄位資訊
    ├── extract_form_structure.py     # 解析欄位階層／類型
    ├── check_fillable_fields.py      # 驗證能否填寫
    ├── check_bounding_boxes.py       # 驗證版面 bbox
    ├── create_validation_image.py    # 產生填寫後預覽圖
    └── convert_pdf_to_images.py      # PDF → JPG/PNG
```

## 核心觀念與工作流

### 任務 → 最佳工具表

| 任務 | 最佳工具 | 說明 |
|------|----------|------|
| 合併 PDF | pypdf | `PdfWriter().add_page()` |
| 拆解 PDF | pypdf | 一頁一檔 |
| 抽文字 | pdfplumber | `page.extract_text()` |
| 抽表格 | pdfplumber | `page.extract_tables()` |
| 建新 PDF | reportlab | Canvas（簡單）或 Platypus（多頁） |
| 命令列合併 | qpdf | `qpdf --empty --pages ...` |
| 掃描 PDF OCR | pytesseract + pdf2image | 先轉圖再辨識 |
| 填表單 | `scripts/fill_fillable_fields.py` | 見 FORMS.md |

### Python 三大武器

```python
# 1. pypdf — 基本操作
from pypdf import PdfReader, PdfWriter
reader = PdfReader("doc.pdf")
text = "".join(p.extract_text() for p in reader.pages)

# 2. pdfplumber — 抽表格保留版面
import pdfplumber
with pdfplumber.open("doc.pdf") as pdf:
    for page in pdf.pages:
        tables = page.extract_tables()

# 3. reportlab — 建立 PDF（Platypus 多頁）
from reportlab.platypus import SimpleDocTemplate, Paragraph, PageBreak
from reportlab.lib.styles import getSampleStyleSheet
doc = SimpleDocTemplate("report.pdf")
styles = getSampleStyleSheet()
story = [Paragraph("Title", styles["Title"]), PageBreak()]
doc.build(story)
```

### 命令列三劍客

```bash
# pdftotext —— 快速抽文字（保留版面）
pdftotext -layout input.pdf output.txt
pdftotext -f 1 -l 5 input.pdf output.txt        # 抽第 1-5 頁

# qpdf —— 合併、拆解、旋轉、解密
qpdf --empty --pages a.pdf b.pdf -- merged.pdf
qpdf in.pdf --pages . 1-5 -- chunk.pdf
qpdf in.pdf out.pdf --rotate=+90:1
qpdf --password=secret --decrypt enc.pdf dec.pdf

# pdfimages —— 抽出所有嵌入圖片
pdfimages -j input.pdf prefix
```

## 精華 Script 與可提取資源

### 🔧 `scripts/fill_fillable_fields.py`

PDF 表單填寫的 production-ready 範本。能：
- 自動偵測欄位（text / checkbox / radio / dropdown）
- 處理座標式填寫
- 輸出填好後的 PDF

> 配套使用：`extract_form_field_info.py`（先看欄位）、`create_validation_image.py`（產生預覽 PNG 確認結果）。

### 🔧 OCR 流程（從 SKILL.md 萃取）

```python
from pdf2image import convert_from_path
import pytesseract

images = convert_from_path("scanned.pdf")
text = "\n".join(
    f"Page {i+1}:\n{pytesseract.image_to_string(img)}"
    for i, img in enumerate(images)
)
```

### 🔧 浮水印模式

```python
from pypdf import PdfReader, PdfWriter

watermark = PdfReader("watermark.pdf").pages[0]
reader = PdfReader("document.pdf")
writer = PdfWriter()
for page in reader.pages:
    page.merge_page(watermark)        # 直接 merge_page 即可疊上
    writer.add_page(page)
writer.write("watermarked.pdf")
```

## 可移植到自家專案的模式

1. **任務 → 工具速查表**：本 skill 把 PDF 操作分解成 8 種任務，每種只用 1 個最佳工具。可直接抄這張表進你專案的 README。

2. **`<sub>`/`<super>` 而非 unicode**（reportlab Platypus）：
   ```python
   chemical = Paragraph("H<sub>2</sub>O", styles["Normal"])
   squared = Paragraph("x<super>2</super> + y<super>2</super>", styles["Normal"])
   ```
   理由：reportlab 內建字型沒有 ₀₁₂₃ ⁰¹²³ 這些字符，會渲染成黑方塊。

3. **加密保護**：
   ```python
   writer.encrypt("user-pwd", "owner-pwd")    # user 開啟用、owner 編輯用
   ```

4. **抽表格直接餵 pandas**：
   ```python
   df = pd.DataFrame(table[1:], columns=table[0])
   df.to_excel("out.xlsx", index=False)
   ```

## 常見陷阱（Gotchas）

- ❌ 在 reportlab 用 `H₂O` Unicode 下標 → 渲染成黑方塊；✅ 用 `<sub>` tag
- ❌ 一律 `pypdf.extract_text()` → 表格會破碎；✅ 表格用 pdfplumber
- ❌ 自寫 PDF 解析 → 直接用 pdfplumber／pypdf
- ❌ 對掃描檔 `extract_text()` 期望抽到字 → 必須先 OCR
- ❌ 忘記 `extract_tables()` 可能回傳 `None` → 加 `if table:` 判空

## 延伸閱讀

- 官方檔：[`skills/pdf/SKILL.md`](../../skills/pdf/SKILL.md)
- 進階：[`skills/pdf/REFERENCE.md`](../../skills/pdf/REFERENCE.md)
- 表單專書：[`skills/pdf/FORMS.md`](../../skills/pdf/FORMS.md)
- 表單腳本：[`skills/pdf/scripts/fill_fillable_fields.py`](../../skills/pdf/scripts/fill_fillable_fields.py)
