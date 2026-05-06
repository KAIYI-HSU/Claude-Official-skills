# canvas-design — 視覺藝術與海報設計

## 一句話定位

把「畫一張漂亮海報」這種模糊任務，拆成「先寫設計宣言（.md）→ 再執行於畫布（.pdf/.png）」兩步驟，並提供 30+ 精選字型與美術館級美學指南。

## 何時觸發

- 製作海報、視覺藝術、靜態設計品
- 需要 .pdf 或 .png 的視覺輸出
- 要求「有設計感」、「不要一般 AI 生成風格」的視覺
- 不適用：演算法生成藝術（用 algorithmic-art）、簡報（用 pptx）

## 目錄結構速覽

```
skills/canvas-design/
├── SKILL.md                  # 主指引（雙步驟方法 + 美學要求）
├── LICENSE.txt
└── canvas-fonts/             # 30+ 精選字型
    ├── ArsenalSC/
    ├── BigShoulders/
    ├── BricolageGrotesque/
    ├── CrimsonPro/
    ├── DMMono/
    ├── EricaOne/
    ... (共 30+ 個字型家族)
```

## 核心觀念與工作流

### 雙步驟法（Philosophy → Canvas）

#### Step 1: 寫設計宣言（4–6 段繁中或英文）

宣言必須涵蓋（**不要**只列 layout 或 template）：
- **Form**：輪廓、邊角、線條粗細
- **Space**：留白比例、密度節奏
- **Color**：色相階層、情緒氛圍
- **Composition**：對稱／不對稱、視覺重心
- **Visual Hierarchy**：主／次／細節

並重複以下精神語彙（非雞湯，是 SKILL.md 明確要求）：
- "meticulously crafted"
- "painstaking attention"
- "master-level execution"

並埋入**低調概念線索**——例如做一張關於「等待」的海報，可暗藏砂漏意象，但不直白寫「砂漏」。

#### Step 2: 在畫布實現

用 PIL（Python Imaging Library）或同等工具，輸出 PDF/PNG。要求：
- 元素須完全收容於畫布內（最少 0.5" margin）
- 沒有任何重疊（非設計性重疊）
- 字距、字級、對齊都精準
- 字型用 `canvas-fonts/` 內的 30+ 選擇

### 設計宣言範例（從 SKILL.md）

| 流派名 | 美學特徵 |
|--------|----------|
| **Concrete Poetry** | 紀念碑形式、Brutalist 空間切割、文字當稀有強烈手勢 |
| **Chromatic Language** | 色彩作為主要資訊系統、幾何精準、Josef Albers 風 |
| **Analog Meditation** | 安靜冥想、紋理、留白、日本攝影集美學 |
| **Geometric Silence** | 純粹秩序、grid-based、Swiss formalism、戲劇性負空間 |

## 精華 Script 與可提取資源

### 🎨 `canvas-fonts/` — 30+ 字型

這是這個 skill 最直接可挪用的資產。包含：
- **Display 類**：Big Shoulders（粗壯）、Erica One、Arsenal SC
- **Serif 類**：Crimson Pro（學院氣）、Bricolage Grotesque（現代襯線）
- **Mono 類**：DM Mono（程式碼／技術感）

> 📍 **直接複製整個 `canvas-fonts/` 到自家專案的 `assets/fonts/`** 立刻升級設計品味，不必再用 Helvetica。

### 📋 設計宣言範本

雖然不是 script，但可作為 prompt template 使用：

```
你是一位為 [主題] 設計海報的視覺工匠。

請先寫一份 4–6 段的設計宣言：
- 為這個美學取一個名字（運動／流派風格）
- 描述：form, space, color, composition, hierarchy
- 強調 meticulous craftsmanship 與 painstaking attention
- 暗藏一個與主題相關的低調概念線索

寫完後，開始用 PIL 在 [尺寸] 畫布上實現此宣言。
所有元素須在畫布內、無重疊、字距精準。
從 canvas-fonts/ 挑 1–2 個字型。
```

## 可移植到自家專案的模式

1. **Philosophy-First 雙步驟**：套用到任何設計輸出（網頁、UI、簡報、影片開場）。先逼自己／逼 AI 寫 200 字宣言再動手，品質會明顯提升。

2. **30+ 字型清單**：把這套字型納入自家設計系統。

3. **「博物館 / 雜誌品質」mental model**：問自己「這張作品如果掛在 MoMA 或登 Wallpaper* 雜誌會怎樣？」當作品質檢驗。

4. **概念線索 vs 直白宣告**：海報不要寫「孤獨」兩字，而是用一張空椅、一個拉長陰影暗示。應用到任何敘事性內容。

## 常見陷阱（Gotchas）

- ❌ 跳過設計宣言直接畫 → 產出 generic 海報；✅ 強迫先寫
- ❌ 元素貼齊邊緣 / 出血 → 印刷／顯示會被切；✅ 保留 0.5" margin
- ❌ 字型混用 5 種以上 → 視覺混亂；✅ 1–2 個字型家族
- ❌ 用 stock photo 直接貼 → 沒設計味；✅ 自己畫幾何或抽象元素
- ❌ 概念說太白 → 沒留思考空間；✅ 暗示而非宣告

## 延伸閱讀

- 官方檔：[`skills/canvas-design/SKILL.md`](../../skills/canvas-design/SKILL.md)
- 字型庫：[`skills/canvas-design/canvas-fonts/`](../../skills/canvas-design/canvas-fonts/)
- 對照閱讀：[`algorithmic-art`](./algorithmic-art.md)（同採 Philosophy-First 模式）
