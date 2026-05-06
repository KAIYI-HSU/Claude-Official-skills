# Agent Skills 規範與 Template 速覽

## 一句話定位

**Skill** 是一個資料夾，內含 `SKILL.md`（必要）與選擇性的 scripts、references、examples、assets，讓 Claude 在偵測到觸發條件時動態載入並執行特定任務。

## SKILL.md 最小結構（template/SKILL.md）

```markdown
---
name: my-skill-name
description: A clear description of what this skill does and when to use it
---

# My Skill Name

[在此撰寫 Claude 啟用此 skill 時應遵循的指示]
```

只有兩個必要欄位：
- `name`：唯一識別碼，使用 kebab-case（小寫＋連字符）
- `description`：明確描述這個 skill 做什麼、何時該觸發

> 完整官方規範位於 <https://agentskills.io/specification>，倉庫內 `spec/agent-skills-spec.md` 僅為轉址說明。

---

## Skill 資料夾常見子目錄

| 子目錄 | 用途 | 範例 |
|--------|------|------|
| `scripts/` | 可執行 Python/Shell 工具，Claude 把它當 black box 呼叫 | `webapp-testing/scripts/with_server.py` |
| `references/` | 補充參考文件（不必每次載入），用於 progressive disclosure | `mcp-builder/reference/python_mcp_server.md` |
| `shared/` | 多語言共享文件 | `claude-api/shared/managed-agents-*.md` |
| `examples/` | 範例輸入／輸出，方便 Claude 模仿 | `internal-comms/examples/3p-updates.md` |
| `assets/` | 字型、圖片、模板等靜態資源 | `canvas-design/canvas-fonts/` |
| `agents/` | 子 agent 的角色提示 | `skill-creator/agents/grader.md` |
| `templates/` | 完整模板檔（HTML/JS/XML） | `algorithmic-art/templates/viewer.html` |

---

## 設計哲學三原則

### 1. Progressive Disclosure（漸進式揭露）

SKILL.md 主檔案盡量精簡（< 500 行），把細節放到 `references/`，讓 Claude 在需要時才讀取。例如：
- `pdf/SKILL.md`（簡潔速查）vs `pdf/REFERENCE.md`（pypdfium2 等深度內容）
- `pptx/SKILL.md`（總覽）vs `pptx/pptxgenjs.md`（從零建立詳細指南）

### 2. Script as Black Box（腳本即黑箱）

Claude 應把 script 當作 `--help` 後直接使用的 CLI 工具，**不必逐行讀原始碼**。這降低 token 消耗、減少誤解。
- 反例：在每次寫 GIF 前都把 `frame_composer.py` 讀一遍
- 正例：先 `python script.py --help` 看接口，直接呼叫

### 3. YAML Frontmatter 嚴格性

`description` 欄位的措辭直接影響觸發準確率。`skill-creator` 還提供 `run_loop.py` 自動優化此欄位（詳見 [skill-creator 章節](./03-dev-technical-skills/skill-creator.md)）。

---

## 倉庫的 marketplace.json

`/.claude-plugin/marketplace.json` 把 17 個 skills 分成 3 個 plugin bundle：

```json
{
  "plugins": [
    {"name": "document-skills", "skills": ["./skills/xlsx", "./skills/docx", "./skills/pptx", "./skills/pdf"]},
    {"name": "example-skills", "skills": [/* 12 個 example */]},
    {"name": "claude-api", "skills": ["./skills/claude-api"]}
  ]
}
```

在 Claude Code 裡可透過 `/plugin marketplace add anthropics/skills` 註冊，再選擇 bundle 安裝。

---

## 自製 Skill 的最簡步驟

1. `cp -r template/ my-skill/`
2. 編輯 `my-skill/SKILL.md` 的 frontmatter（name + description）
3. 撰寫指示主文（範例、規範、流程）
4. 視需求新增 `scripts/`、`references/`、`examples/`
5. 用 `skill-creator` 跑評估，根據 `run_loop.py` 結果優化 description

---

## 延伸閱讀

- 官方規範：<https://agentskills.io/specification>
- 官方 Skills 倉庫：<https://github.com/anthropics/skills>
- 本倉庫 `template/SKILL.md`：最簡可用模板
- 本倉庫 `skills/skill-creator/SKILL.md`：完整 skill 開發流程（含評估迴圈）
