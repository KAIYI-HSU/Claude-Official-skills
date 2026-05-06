# xlsx — 試算表與財務模型

## 一句話定位

用 `openpyxl` + `pandas` 建立 `.xlsx`，並透過 LibreOffice headless 重新計算公式；強制要求「**所有計算都用 Excel 公式表達，絕對不要在 Python 裡硬編碼結果**」。

## 何時觸發

- 建立、編輯、讀取 `.xlsx` / `.xlsm` / `.csv`
- 加入公式、格式、圖表
- 清理混亂的表格資料
- 產出財務模型、預算、儀表板

## 目錄結構速覽

```
skills/xlsx/
├── SKILL.md                # 主指引（含財務模型配色規範）
├── LICENSE.txt
└── scripts/
    ├── recalc.py           # LibreOffice 重算公式 + 錯誤偵測
    └── office/             # 共享 unpack/pack/validate（含 Excel schemas）
```

## 核心觀念與工作流

### 工具分工

| 任務 | 工具 |
|------|------|
| 純資料分析、批次處理 | `pandas` |
| 公式、格式、Excel 專屬功能 | `openpyxl` |
| 重新計算公式（讓 `=SUM` 真正算出值） | `python scripts/recalc.py` |

### 核心鐵律：用公式，不用硬編碼

**❌ 反例**（Python 直接算結果填值）：
```python
ws["B5"] = sum(ws[f"B{i}"].value for i in range(1, 5))    # ❌ 寫死數字
```

**✅ 正例**（Python 寫公式字串）：
```python
ws["B5"] = "=SUM(B1:B4)"                                   # ✅ 真正的 Excel 公式
```

理由：使用者打開 Excel 改動上游數字時，公式會自動更新；硬編碼數字則永遠不變，這是嚴重 bug。

### 重新計算流程

```bash
# 1. 用 openpyxl 建立檔案 + 寫入公式字串
python my_script.py
# 2. recalc.py 用 LibreOffice 開檔並計算所有公式
python scripts/recalc.py model.xlsx
# 3. 同時偵測 #REF! / #DIV/0! / #VALUE! / #NAME? / #N/A 並回報位置
```

`recalc.py` 會輸出 JSON：
```json
{"errors": [{"sheet": "Inputs", "cell": "C7", "type": "#DIV/0!"}]}
```

### 財務模型配色規範（金融業共識）

| 顏色 | 用途 |
|------|------|
| 🔵 藍字 | 輸入值（使用者要改的） |
| ⚫ 黑字 | 公式（自動計算） |
| 🟢 綠字 | 內部 sheet 連結 |
| 🔴 紅字 | 外部檔案連結 |
| 🟡 黃底 | 關鍵假設 cell |

### 數字格式標準

| 類型 | 格式 |
|------|------|
| 貨幣 | `$#,##0` 或 `$#,##0.00` |
| 百分比 | `0.0%` |
| 倍數 | `0.0"x"` |
| 負數 | `(#,##0)` 用括號表示 |

## 精華 Script 與可提取資源

### 🔧 `scripts/recalc.py`（極具重用價值）

把 openpyxl 寫的「死」公式跑成「活」結果。背後是 `soffice --headless --calc`，並掃描所有 cell 找錯誤。

**可直接抄到自家專案**：當你的工具產 Excel 時，跑一次 recalc 確保結果正確。

### 🔧 完整建模樣板

```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment

wb = Workbook()
ws = wb.active
ws.title = "Model"

# 1. 輸入值（藍字）
ws["B1"] = 1000
ws["B1"].font = Font(color="0000FF")

# 2. 公式（黑字）
ws["B5"] = "=B1*$D$1"            # 用 $ 鎖住假設
ws["B5"].number_format = "$#,##0.00"

# 3. 關鍵假設 cell（黃底）
ws["D1"] = 0.15
ws["D1"].fill = PatternFill("solid", fgColor="FFFF00")
ws["D1"].number_format = "0.0%"

wb.save("model.xlsx")
# 然後跑 recalc.py 讓公式真的算出來
```

## 可移植到自家專案的模式

1. **「公式優先」rule**：寫一條 lint 規則，禁止在 cell 寫純數字結果，必須是 `=...` 公式。

2. **錯誤類型對照表**：把 `#REF!` 等 6 種錯誤的常見原因寫進專案 wiki：
   - `#REF!` — 引用了被刪除的 cell
   - `#DIV/0!` — 除以 0 或空值
   - `#VALUE!` — 型別錯（數值算文字）
   - `#NAME?` — 函式名拼錯
   - `#N/A` — 查找失敗
   - `#NULL!` — range 交集為空

3. **資料來源備註格式**：
   ```
   Source: Company 10-K, FY2024, Page 45, "Revenue by Segment" table
   ```
   養成在每個輸入值的相鄰 cell 寫來源的習慣。

4. **絕對引用 vs 相對引用**：假設 cell 用 `$D$1`，可被 fill-down 不變動。

## 常見陷阱（Gotchas）

- ❌ openpyxl 寫公式後不重算 → 開檔時 cell 顯示 0；✅ 跑 `recalc.py`
- ❌ 用 Python 算結果寫死 → 上游改值不會更新
- ❌ 整列複製公式忘記用 `$` → 引用錯欄
- ❌ 金額沒設 number_format → 顯示成 `1234.567`
- ❌ 大型模型沒分 sheet → 公式跨 sheet 連結混亂；✅ 分 Inputs / Calcs / Outputs

## 延伸閱讀

- 官方檔：[`skills/xlsx/SKILL.md`](../../skills/xlsx/SKILL.md)
- 重算腳本：[`skills/xlsx/scripts/recalc.py`](../../skills/xlsx/scripts/recalc.py)
- 共享 office 工具：[`skills/xlsx/scripts/office/`](../../skills/xlsx/scripts/office/)
