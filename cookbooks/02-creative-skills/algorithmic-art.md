# algorithmic-art — 程式生成藝術

## 一句話定位

用 p5.js 生成可互動的演算法藝術作品，內建 Anthropic 品牌化 viewer.html 模板（含 seed 控制、參數滑桿），輸出單一 self-contained HTML 檔。

## 何時觸發

- "generative art"、"algorithmic art"、"code art"
- 流場（flow field）、粒子系統、L-system、Voronoi、circle packing
- 需要「同樣 seed 產出同樣畫面」的可重現作品
- 不適用：靜態海報（用 canvas-design）

## 目錄結構速覽

```
skills/algorithmic-art/
├── SKILL.md                       # 主指引（雙步驟 + p5.js 實作指南）
├── LICENSE.txt
└── templates/
    ├── viewer.html                # 🌟 必用模板（21KB，含 Anthropic 品牌 sidebar）
    └── generator_template.js      # 演算法組織範本（seeded、參數結構、類別）
```

## 核心觀念與工作流

### 雙步驟法（同 canvas-design）

#### Step 1: 寫演算法宣言（4–6 段）

不同於 canvas-design 著重靜態美學，這裡描述**計算過程**：
- Noise functions（Perlin / Simplex）
- Particle behaviors（速度、力場、生命週期）
- Field dynamics（向量場）
- Parametric variation
- Emergent complexity（局部規則 → 整體湧現）

#### Step 2: 用 p5.js 實作

**🚨 CRITICAL Step 0**：先讀 `templates/viewer.html`，**直接當起點檔**，不要當靈感參考。

### viewer.html 結構

固定區域（**禁止修改**）：
- Layout 框架
- Sidebar 結構
- Anthropic 品牌（Poppins 標題 + Lora 內文字型）
- Seed input 與按鈕
- Action buttons（Save、Regenerate）

可變區域（**自由客製**）：
- p5.js 演算法（`setup()` + `draw()`）
- 參數定義
- UI 控制（滑桿、下拉選單）
- 顏色區段（選用）

### Seeded Randomness（Art Blocks 模式）

```javascript
function setup() {
  createCanvas(800, 800);
  randomSeed(seed);     // 控制 random()
  noiseSeed(seed);      // 控制 noise()
  // ...
}
```

> 同一個 seed 永遠產同一張畫——這是「演算法藝術 vs 一次性圖片」的關鍵區分。

### 參數設計原則

❌ **錯**：列一份「常見參數選單」（amplitude、frequency、speed...）

✅ **對**：從**演算法本身需要什麼**衍生：
- 量（粒子數、線條數）
- 尺度（網格大小、雜訊頻率）
- 機率（分裂率、消亡率）
- 比例（黃金比例變形、網格密度）
- 閾值（合併距離、分支條件）

### 演算法宣言範例（從 SKILL.md）

| 流派 | 核心 |
|------|------|
| **Organic Turbulence** | 自然法則約束的混沌、Perlin 流場、數千粒子 |
| **Quantum Harmonics** | 離散個體的相位干涉、形成 mandala |
| **Recursive Whispers** | 跨尺度自相似、黃金比例分支、L-system |
| **Field Dynamics** | 透過粒子軌跡可見的不可見力場 |
| **Stochastic Crystallization** | 隨機過程結晶為秩序、Voronoi、circle packing |

## 精華 Script 與可提取資源

### 🌟 `templates/viewer.html`（極度推薦複製）

這個 21KB 模板已封裝：
- 響應式 sidebar layout
- Seed 輸入 + 隨機按鈕
- 參數 group（label + slider + value display）
- Save canvas 按鈕（直接下載 PNG）
- Anthropic 字型內嵌

> 📍 **可挪用情境**：你要做任何「使用者調整參數即時生成視覺」的網頁工具（音波視覺化、資料藝術、教學 demo）。

### 🌟 `templates/generator_template.js`

示範良好的演算法程式組織：
```javascript
const PARAMS = { count: 1000, scale: 0.01, speed: 1.0 };

class Particle { /* ... */ }
const particles = [];

function setup() { /* seed + create */ }
function draw() { /* update + render */ }
```

把 PARAMS、類別、生命週期分離，比一坨 globals 好維護。

## 可移植到自家專案的模式

1. **viewer.html 模板複用**：把它當成「所有互動 demo」的基礎，改 `draw()` 即可。

2. **Seeded reproducibility**：任何「隨機輸出」的工具都應提供 seed，讓使用者能複現某次結果。

3. **參數從演算法衍生**：寫工具時別堆 settings panel，問自己「這個演算法本質上需要哪些可調？」

4. **Save canvas 一鍵下載**：
   ```javascript
   function saveImage() {
     saveCanvas('artwork-' + seed, 'png');
   }
   ```

5. **Easing functions 給動畫**：可從 [`slack-gif-creator/core/easing.py`](../../skills/slack-gif-creator/core/easing.py) 借過來改 JS。

## 常見陷阱（Gotchas）

- ❌ 改 `viewer.html` 的固定區域（layout、sidebar、品牌）→ 失去設計一致性
- ❌ 不設 `randomSeed/noiseSeed` → 每次 reload 畫面不同，無法分享
- ❌ 用 `Math.random()` → 不受 p5 seed 控制；✅ 一律用 `random()`、`noise()`
- ❌ 把 noise 頻率硬寫 0.01 → 應該是參數
- ❌ 動畫 loop 不停 → CPU 飆高；視覺穩定後 `noLoop()`
- ❌ 把所有 logic 塞 draw() → 難維護；✅ 分類別、分函式

## 延伸閱讀

- 官方檔：[`skills/algorithmic-art/SKILL.md`](../../skills/algorithmic-art/SKILL.md)
- viewer 模板：[`skills/algorithmic-art/templates/viewer.html`](../../skills/algorithmic-art/templates/viewer.html)
- generator 模板：[`skills/algorithmic-art/templates/generator_template.js`](../../skills/algorithmic-art/templates/generator_template.js)
- 配對閱讀：[canvas-design](./canvas-design.md)（靜態版本）
