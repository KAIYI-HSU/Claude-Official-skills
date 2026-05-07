# Claude 官方 Skills 繁體中文秘笈手冊

> 本手冊為 Anthropic 官方 [Claude Skills](https://github.com/anthropics/skills) 的繁體中文導覽與精華萃取，協助開發者快速翻閱所需能力、提取可重用 script、並了解 Anthropic 設計團隊的 best practices。

## 為什麼需要這本秘笈？

官方 17 個 skills 散落於不同子資料夾，每個 SKILL.md 動輒上千行英文，新手很難一次掌握全貌。本手冊將每個 skill 濃縮成 **150–300 行繁中說明**，並依據以下原則組織：

- **可快速翻閱**：八大段固定格式，5 分鐘讀懂一個 skill
- **可直接提取**：每個 skill 列出最有重用價值的 script 與檔案路徑
- **跨 skill 視角**：在 [99-cross-skill-patterns.md](./99-cross-skill-patterns.md) 歸納共通設計哲學

---

## 17 個 Skills 全覽

### 📄 文件處理類（5）
| Skill | 中文簡介 | 主要技術 |
|-------|----------|----------|
| [docx](./01-document-skills/docx.md) | Word 文件建立、編輯、追蹤修訂、註解 | docx-js + XML unpack/pack |
| [pdf](./01-document-skills/pdf.md) | PDF 讀寫、合併、表單填寫、OCR | pypdf / pdfplumber / reportlab |
| [pptx](./01-document-skills/pptx.md) | 簡報製作、編修、視覺 QA | pptxgenjs + LibreOffice |
| [xlsx](./01-document-skills/xlsx.md) | 試算表、財務模型、公式運算 | openpyxl + LibreOffice recalc |
| [doc-coauthoring](./01-document-skills/doc-coauthoring.md) | 結構化共筆流程 | 三階段協作法 |

### 🎨 創意設計類（3）
| Skill | 中文簡介 | 主要技術 |
|-------|----------|----------|
| [canvas-design](./02-creative-skills/canvas-design.md) | 海報、視覺藝術 .pdf/.png | 設計哲學優先 + 30+ 字型 |
| [algorithmic-art](./02-creative-skills/algorithmic-art.md) | 程式生成藝術 | p5.js + 種子隨機 + 互動參數 |
| [slack-gif-creator](./02-creative-skills/slack-gif-creator.md) | Slack 動畫 GIF | PIL + GIFBuilder + easing |

### 🛠️ 開發技術類（6）
| Skill | 中文簡介 | 主要技術 |
|-------|----------|----------|
| [claude-api](./03-dev-technical-skills/claude-api.md) | Claude API / SDK 開發 | 多語言 + Managed Agents + 快取 |
| [mcp-builder](./03-dev-technical-skills/mcp-builder.md) | MCP Server 開發 | TypeScript / Python + 評估 |
| [skill-creator](./03-dev-technical-skills/skill-creator.md) | 撰寫 Skill 的 Skill（meta） | Eval / Benchmark / 描述優化 |
| [webapp-testing](./03-dev-technical-skills/webapp-testing.md) | Playwright Web 測試 | with_server.py 多伺服器管理 |
| [web-artifacts-builder](./03-dev-technical-skills/web-artifacts-builder.md) | React + shadcn artifact | Vite + Parcel + 內聯打包 |
| [frontend-design](./03-dev-technical-skills/frontend-design.md) | 前端設計品質指南 | 反 AI slop 設計清單 |

### 🏢 企業溝通類（3）
| Skill | 中文簡介 | 主要技術 |
|-------|----------|----------|
| [internal-comms](./04-enterprise-skills/internal-comms.md) | 內部溝通文件 | 3P 更新 / 週報 / FAQ |
| [brand-guidelines](./04-enterprise-skills/brand-guidelines.md) | Anthropic 品牌規範 | 6 色 + Poppins/Lora |
| [theme-factory](./04-enterprise-skills/theme-factory.md) | 主題化樣式工廠 | 10 套預設主題 |

---

## 推薦閱讀路徑

### 我是 Claude Skills 新手
1. 先讀 [00-skills-spec-and-template.md](./00-skills-spec-and-template.md) 了解 Skill 是什麼
2. 看 [skill-creator](./03-dev-technical-skills/skill-creator.md) — meta-skill，了解 skill 開發全流程
3. 挑一個最貼近你工作的 skill 細讀（如後端工程師看 mcp-builder、設計師看 canvas-design）
4. 最後讀 [99-cross-skill-patterns.md](./99-cross-skill-patterns.md) 看設計大圖

### 我想直接抓 script 來用
最有重用價值的 script TOP 5：
1. **`skills/slack-gif-creator/core/easing.py`** — 9 種緩動函式，立即可用
2. **`skills/webapp-testing/scripts/with_server.py`** — 多 server 生命週期管理
3. **`skills/skill-creator/scripts/run_loop.py`** — Skill 描述自動優化迴圈
4. **`skills/docx/scripts/office/unpack.py`** + `pack.py` — Office 文件 ZIP 拆解／重組
5. **`skills/pdf/scripts/fill_fillable_fields.py`** — PDF 表單填寫

### 我要做特定任務
- **產生 Word 報告** → [docx](./01-document-skills/docx.md)
- **PPT 自動化** → [pptx](./01-document-skills/pptx.md)
- **整合外部 API 給 LLM 用** → [mcp-builder](./03-dev-technical-skills/mcp-builder.md)
- **建立可分享的 React artifact** → [web-artifacts-builder](./03-dev-technical-skills/web-artifacts-builder.md)
- **建立公司內部 chatbot 文件樣板** → [internal-comms](./04-enterprise-skills/internal-comms.md)

---

## 每篇 Skill 文件的固定結構

```
1. 一句話定位
2. 何時觸發
3. 目錄結構速覽
4. 核心觀念與工作流
5. 精華 Script 與可提取資源
6. 可移植到自家專案的模式
7. 常見陷阱（Gotchas）
8. 延伸閱讀
```

---

## 授權

本手冊為對官方 skills 的繁中導讀，原始 skills 的授權見各 skill 資料夾下的 `LICENSE.txt`：
- 多數 example skills 為 Apache 2.0
- 文件類（docx/pdf/pptx/xlsx）為 Anthropic 自有授權（source-available）

請務必檢視各 skill 自身授權後再轉用。

---

## 維護資訊

- 製作日期：2026-05-06
- 對應 skills 倉庫 commit：見 git log
- 若官方 skills 有重大更新，本手冊需同步修訂
