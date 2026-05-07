# 創意設計類 Skills

這 3 個 skills 展示 Anthropic 在「視覺創作」領域的設計哲學。共通主題：**先寫設計宣言（philosophy），再執行**。這個「Philosophy-First」雙步驟法值得套用到任何設計任務。

| Skill | 產物 | 主要技術 |
|-------|------|----------|
| [canvas-design](./canvas-design.md) | 靜態 .pdf / .png 海報 | PIL + 30+ 字型 + 設計 manifesto |
| [algorithmic-art](./algorithmic-art.md) | 互動 .html (p5.js) | seeded randomness + 參數控制 |
| [slack-gif-creator](./slack-gif-creator.md) | 動畫 .gif | PIL + GIFBuilder + easing |

## 共通設計模式：Philosophy-First 雙步驟

canvas-design 與 algorithmic-art 都採用：

### Step 1: 寫設計宣言（4–6 段，~300 字）
- 命名一個運動／流派（如 "Concrete Poetry"、"Quantum Harmonics"）
- 描述美學主張：form / space / color / composition
- 強調工匠精神：用 "meticulously crafted"、"painstaking attention" 等語彙
- 埋入低調概念線索（不大聲宣告）

### Step 2: 用具體媒介實現
- canvas-design：PIL 畫到 PDF/PNG
- algorithmic-art：p5.js 寫成 HTML

> **為什麼有效**：先想清楚「美學是什麼」再下筆，能避免「亂試一通」的隨機輸出。

## 推薦學習順序

1. **slack-gif-creator** — 最務實，提供大量可重用 Python utilities
2. **canvas-design** — 學「設計宣言」這個元 pattern
3. **algorithmic-art** — 學 viewer.html 模板與參數設計
