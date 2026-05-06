# frontend-design — 反 AI slop 前端品味指南

## 一句話定位

純粹的「設計思維 prompt」，沒有 script 也沒有元件——強迫 Claude 在寫前端前先選擇一個極端美學方向（10+ 種風格選一），避免「Inter + 紫漸層 + 全置中」的 AI 通用美學。

## 何時觸發

- 任何「建 web 元件／頁面／應用／landing page／dashboard」請求
- 「美化這個 UI」、「重設計」
- 不適用：純後端、無 UI 工作

## 目錄結構速覽

```
skills/frontend-design/
└── SKILL.md     # 唯一檔案（~85 行）— 純設計思維指南
```

## 核心觀念與工作流

### Step 0: 設計思考（**寫程式之前**）

用以下 4 題逼自己選定方向：

1. **Purpose**：這 UI 解決什麼問題？誰用？
2. **Tone**：選一個**極端**：
   - brutally minimal（極簡野獸派）
   - maximalist chaos（最大化混沌）
   - retro-futuristic（復古未來）
   - organic/natural（有機自然）
   - luxury/refined（奢華精緻）
   - playful/toy-like（玩具感）
   - editorial/magazine（雜誌編排）
   - brutalist/raw（粗野原始）
   - art deco/geometric（裝飾藝術）
   - soft/pastel（柔和粉彩）
   - industrial/utilitarian（工業實用）
3. **Constraints**：framework、效能、無障礙
4. **Differentiation**：什麼讓這 UI 令人 **UNFORGETTABLE**？讓人記得的「那一點」是什麼？

### 五大美學軸

#### 1. Typography（字型）

- **避免**：Arial、Inter、Roboto、system fonts
- **追求**：獨特展示字 + 精緻內文字配對
- 範例：Big Shoulders（粗壯）+ Crimson Pro（古典）

#### 2. Color & Theme（色彩與主題）

- 用 CSS variables 統一管理
- **主色佔大面積 + sharp accents**，比「均勻分佈」有力
- ❌ 避免紫漸層配白底（已成 AI 通病）

#### 3. Motion（動態）

- HTML：CSS-only（`@keyframes`、`transition`）
- React：Motion library（前 framer-motion）
- 重點：**少而精**——一次完美編排的 page load（staggered reveal）勝過 10 個零碎 micro-interaction
- Hover、scroll-trigger 給驚喜

#### 4. Spatial Composition（空間構圖）

- **不對稱**、**斜流**、**重疊**、**破格**（grid-breaking）
- 大量負空間 OR 受控密度
- 不要永遠 max-width: 1200px 置中

#### 5. Backgrounds & Details（背景與細節）

- 別只用 solid color
- 加：gradient mesh、noise texture、幾何 pattern、layered transparency、戲劇陰影、裝飾邊框、custom cursor、grain overlay

### 核心原則

> **Bold maximalism 與 refined minimalism 都行——關鍵是 intentionality（意圖性），不是 intensity（強度）**

> **Match implementation complexity to the aesthetic vision**：極簡風格需要克制與精準（spacing、typography、subtle details）；最大化風格需要 elaborate code 與大量 effects。

## 精華 Script 與可提取資源

雖然沒有 script，但這份「avoid list」可直接抄到專案的 UI guidelines：

### ❌ AI Slop 黑名單

```
NEVER use:
- Inter / Roboto / Arial / system-ui
- 紫漸層配白底（purple gradient on white）
- 全置中 layout（重複 max-width: 1200px; mx-auto）
- 統一 16px 圓角（uniform rounded-xl）
- Stock illustration（cookie-cutter 插畫）
- "Sleek modern" 通用形容詞
- Space Grotesk（已被 AI 過度使用）
```

### ✅ 11 種美學方向選單

把上面 11 種 tone 印成一張卡片，貼在牆上 / 加進 design system 文件。每次新專案抽一張，**強迫不重複**。

## 可移植到自家專案的模式

1. **「Pick an extreme tone」習慣**：別開會討論「要簡約還是現代」，直接從 11 種選一個極端。

2. **CSS variables 主題系統**：
   ```css
   :root {
     --color-primary: ...;
     --color-accent-1: ...;
     --color-accent-2: ...;
     --font-display: ...;
     --font-body: ...;
   }
   ```

3. **One well-orchestrated moment > 10 micro-interactions**：把動畫預算集中在 page load 或關鍵互動，不要處處有效果。

4. **Light/Dark + 字型 + 美學三維輪換**：團隊做多個產品時，刻意每次組合不同，避免「公司產品全長一樣」。

## 常見陷阱（Gotchas）

- ❌ 沒選 tone 就開寫 → 默認 AI slop；✅ 強迫先選一個極端
- ❌ Motion 用太多 → 視覺嘈雜；✅ 集中 1–2 個高影響時刻
- ❌ Text 全置中 + 全白底 → 雜誌都不會這樣排；✅ 大膽留白／不對稱
- ❌ 統一 `rounded-xl` → 缺少節奏；✅ 不同元件用不同邊角策略（鋒利／圓潤／半圓）
- ❌ 把 minimalism 當作「省事的藉口」→ 變寡淡；✅ 極簡需要更精準的細節雕琢

## 延伸閱讀

- 官方檔：[`skills/frontend-design/SKILL.md`](../../skills/frontend-design/SKILL.md)
- 配對閱讀：[web-artifacts-builder](./web-artifacts-builder.md)（實作層）
- 相關靈感：[canvas-design](../02-creative-skills/canvas-design.md)（設計宣言模式）
