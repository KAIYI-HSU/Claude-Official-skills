# theme-factory — 10 套主題＋客製主題工廠

## 一句話定位

提供 10 套精選色彩／字型主題，每套含 4 色調色盤＋字型配對＋使用情境建議；附上一張 PDF showcase 給人類選擇；不滿意還可即時生成客製主題。

## 何時觸發

- "套用主題"、"幫這個 deck 配色"、"make it look professional"
- 簡報、文件、報告、HTML landing page 的視覺整體化
- 不確定該用什麼主題時——直接 show 出 showcase

## 目錄結構速覽

```
skills/theme-factory/
├── SKILL.md                     # 流程說明
├── theme-showcase.pdf           # 🌟 10 主題的視覺索引（給人看）
├── LICENSE.txt
└── themes/                      # 10 個主題檔
    ├── ocean-depths.md          # 海洋深處（企業／金融）
    ├── sunset-boulevard.md      # 日落大道（暖色／活潑）
    ├── forest-canopy.md         # 森林樹冠（自然／沉穩）
    ├── modern-minimalist.md     # 現代極簡（灰階）
    ├── golden-hour.md           # 黃金時刻（秋色／溫暖）
    ├── arctic-frost.md          # 北極寒霜（冷色／清爽）
    ├── desert-rose.md           # 沙漠玫瑰（粉土色）
    ├── tech-innovation.md       # 科技創新（強烈／現代）
    ├── botanical-garden.md      # 植物園（綠色／有機）
    └── midnight-galaxy.md       # 午夜銀河（深色／戲劇）
```

## 核心觀念與工作流

### 4 步驟流程

```
1. 顯示 theme-showcase.pdf（給使用者視覺挑選）
2. 詢問選擇
3. 等待明確確認
4. 套用對應主題的色／字型到 artifact
```

### 主題檔結構（以 Ocean Depths 為例）

```markdown
# Ocean Depths
A professional and calming maritime theme that evokes the serenity of deep ocean waters.

## Color Palette
- **Deep Navy**: #1a2332 - Primary background
- **Teal**: #2d8b8b - Accent
- **Seafoam**: #a8dadc - Secondary accent
- **Cream**: #f1faee - Text/light backgrounds

## Typography
- Headers: DejaVu Sans Bold
- Body: DejaVu Sans

## Best Used For
Corporate presentations, financial reports, professional consulting decks, trust-building content.
```

每套都依此 4 段結構：色票、字型、適用情境。

### 10 主題速查

| 主題 | 適用 | 主色傾向 |
|------|------|----------|
| **Ocean Depths** | 企業／金融／專業諮詢 | 深藍＋青綠 |
| **Sunset Boulevard** | 行銷／活動／創意 | 橘紅／紫 |
| **Forest Canopy** | 永續／自然／非營利 | 深綠＋土棕 |
| **Modern Minimalist** | 任何「乾淨現代」需求 | 灰階 |
| **Golden Hour** | 年度回顧／溫情敘事 | 金黃＋暖紅 |
| **Arctic Frost** | 科技／醫療／純淨感 | 冷藍＋白 |
| **Desert Rose** | 美妝／生活風格 | 粉土＋砂色 |
| **Tech Innovation** | 軟體／新創 | 鮮明＋現代強對比 |
| **Botanical Garden** | 食品／健康／植物 | 多綠層次 |
| **Midnight Galaxy** | 娛樂／戲劇／品牌 launch | 深色＋星光 |

### 客製主題（fallback）

當 10 種都不合適時，依使用者 brief 即時生成：
1. 取一個類似命名（"X + Y"，如 "Mountain Mist"、"Velvet Studio"）
2. 選 4 色（背景 + 強調 + 次強調 + 文字）
3. 選 1 套字型 pair
4. 寫 best-used-for
5. 顯示 review，使用者確認後套用

## 精華 Script 與可提取資源

### 🌟 `theme-showcase.pdf`

> 雖然不是 script，但「視覺索引 PDF」是極具啟發的 pattern——當你的工具有「光看文字選不出來」的選項時，做一張視覺 catalog 比寫 100 行描述有效。

### 📋 主題 .md 檔結構模板

直接套用到自家品牌系統：

```markdown
# {主題名}
{一句話形容氛圍}

## Color Palette
- **{色名}**: #xxxxxx - {用途}
（4 色）

## Typography
- Headers: {字型}
- Body: {字型}

## Best Used For
{適用情境清單}
```

統一這個格式後，前端可寫 parser 把 .md 轉成 CSS variables。

## 可移植到自家專案的模式

1. **「Choose-then-Apply」流程**：先 show 選項、等使用者確認、再執行。比直接「我幫你選了 X」更尊重使用者控制權。

2. **視覺 PDF showcase**：當選項視覺差異大時，PDF 比文字描述好用。可推廣到任何「style 多選一」場景。

3. **4 色調色盤足矣**：別寫 12 色 design system，4 色（主背景 + 強調 + 次強調 + 文字）能撐起多數場景。

4. **「Best Used For」標籤**：每個選項標明適用情境，幫助 LLM 與人類快速配對。

5. **Fallback to Custom**：預設選項不夠時即時生成。比強迫使用者「將就」更靈活。

## 常見陷阱（Gotchas）

- ❌ 不顯示 showcase 直接挑 → 使用者不知差異；✅ 一律先 show
- ❌ 套了主題後忘記檢查對比度 → 文字看不清；✅ 對比 ≥ 4.5:1
- ❌ 同一個 deck 混用兩個主題 → 視覺破碎；✅ 一個 artifact 一個主題
- ❌ DejaVu Sans 沒裝 → 字型 fallback；✅ 預先檢查或用 web font
- ❌ 客製主題無命名 → 之後難複用；✅ 即時取個有意義的名字

## 延伸閱讀

- 官方檔：[`skills/theme-factory/SKILL.md`](../../skills/theme-factory/SKILL.md)
- 主題集：[`skills/theme-factory/themes/`](../../skills/theme-factory/themes/)
- 視覺索引：[`skills/theme-factory/theme-showcase.pdf`](../../skills/theme-factory/theme-showcase.pdf)
- 配對閱讀：[brand-guidelines](./brand-guidelines.md)（Anthropic 自家品牌）、[pptx](../01-document-skills/pptx.md)（也提到 10 套配色）
