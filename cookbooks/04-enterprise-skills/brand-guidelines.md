# brand-guidelines — Anthropic 品牌規範

## 一句話定位

最簡潔的 skill 之一——只列出 Anthropic 的 7 種品牌色 + 2 種字型，當 Claude 偵測到「需要套品牌」時自動套用。是「pure-instruction」型 skill 的範本。

## 何時觸發

- 套用品牌色、企業視覺識別、視覺格式化、公司設計標準
- 「apply Anthropic brand styling」、「make it look corporate」

## 目錄結構速覽

```
skills/brand-guidelines/
├── SKILL.md      # 唯一檔案（~75 行）— 純規範
└── LICENSE.txt
```

> **沒有 script、沒有 example、沒有 asset**。極簡 skill 的代表。

## 核心觀念與工作流

### Anthropic 品牌色（7 色）

#### 主色調（4 色）

| 角色 | Hex | 用途 |
|------|-----|------|
| **Dark** | `#141413` | 主要文字、深色背景 |
| **Light** | `#faf9f5` | 淺色背景、深色上的文字 |
| **Mid Gray** | `#b0aea5` | 次要元素 |
| **Light Gray** | `#e8e6dc` | 細微背景 |

#### 強調色（3 色）

| 角色 | Hex | 用途 |
|------|-----|------|
| **Orange** | `#d97757` | 主要強調 |
| **Blue** | `#6a9bcc` | 次要強調 |
| **Green** | `#788c5d` | 第三強調 |

### 字型配對

| 用途 | 字型 | Fallback |
|------|------|----------|
| **標題（24pt+）** | Poppins | Arial |
| **內文** | Lora | Georgia |

### 套用規則

- 字型：標題 ≥ 24pt 用 Poppins，其餘用 Lora
- 沒裝字型 → 自動退回 Arial / Georgia（不阻擋輸出）
- 形狀／非文字元素：循環使用 Orange → Blue → Green
- 文字顏色根據背景對比智慧選擇

### 技術細節

```python
from pptx.dml.color import RGBColor

ORANGE = RGBColor(0xd9, 0x77, 0x57)
BLUE   = RGBColor(0x6a, 0x9b, 0xcc)
GREEN  = RGBColor(0x78, 0x8c, 0x5d)

shape.fill.solid()
shape.fill.fore_color.rgb = ORANGE
```

## 精華 Script 與可提取資源

### 📋 7 色 hex 表

直接複製到自家專案的 `theme.css`：

```css
:root {
  /* Main */
  --brand-dark: #141413;
  --brand-light: #faf9f5;
  --brand-mid-gray: #b0aea5;
  --brand-light-gray: #e8e6dc;

  /* Accent */
  --brand-orange: #d97757;
  --brand-blue: #6a9bcc;
  --brand-green: #788c5d;
}
```

### 📋 Poppins + Lora 字型搭配

兩者皆免費（Google Fonts），可直接：
```html
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600&family=Lora&display=swap" rel="stylesheet">
```

> 配對哲學：Poppins（無襯線、現代、結構感）對比 Lora（襯線、古典、人文感）——典型「現代 vs 古典」對比配對法。

## 可移植到自家專案的模式

1. **「Pure Instruction」skill 模板**：當你只有規範要傳達、沒有複雜流程，就學這支——SKILL.md 寫清楚規則即可，不必硬塞 script。

2. **Smart Fallback 思維**：字型沒裝就 fallback、不阻擋輸出。任何依賴外部資源的工具都該有 fallback。

3. **Accent Cycle**：3 色循環使用，比「全用 orange」有層次。可推廣到 chart 配色：循環 N 色而不重複。

4. **24pt 為標題分界**：簡單明確的數字規則，比「heading 比 body 大」這種模糊規則容易執行。

## 常見陷阱（Gotchas）

- ❌ 強迫使用者裝 Poppins / Lora → 阻擋；✅ 預設 fallback Arial/Georgia
- ❌ 把全部元素都用 Orange → 失去層次；✅ 主色＋3 種 accent 循環
- ❌ Mid Gray (#b0aea5) 當主要文字色 → 對比不足；✅ 主文用 Dark
- ❌ 套品牌套到失去內容識別度 → 過度品牌化

## 延伸閱讀

- 官方檔：[`skills/brand-guidelines/SKILL.md`](../../skills/brand-guidelines/SKILL.md)
- 配對閱讀：[theme-factory](./theme-factory.md)（10 種其他主題）、[canvas-design](../02-creative-skills/canvas-design.md)（更廣的視覺設計）
