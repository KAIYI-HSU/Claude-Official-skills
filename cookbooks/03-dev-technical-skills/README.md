# 開發技術類 Skills

這 6 個 skills 是工程師最直接受惠的部分，從 API 整合、MCP 開發、Web 測試、到自製 skill 與前端設計，幾乎涵蓋整個 LLM 應用開發流程。

| Skill | 場景 | 重要程度 |
|-------|------|----------|
| [claude-api](./claude-api.md) | 用任何語言串接 Claude API | ⭐⭐⭐⭐⭐ |
| [mcp-builder](./mcp-builder.md) | 寫 MCP server 給 LLM 用 | ⭐⭐⭐⭐ |
| [skill-creator](./skill-creator.md) | meta：寫／優化／評估 skill | ⭐⭐⭐⭐⭐ |
| [webapp-testing](./webapp-testing.md) | Playwright 測試本地 web app | ⭐⭐⭐ |
| [web-artifacts-builder](./web-artifacts-builder.md) | 建立 React 互動 artifact | ⭐⭐⭐ |
| [frontend-design](./frontend-design.md) | 前端品味指南 | ⭐⭐⭐ |

## 共通模式

### 1. Black-box Script 哲學

`webapp-testing` 與 `web-artifacts-builder` 都明確要求 Claude **「先 `--help` 再用，不要讀原始碼」**。理由：scripts 可能很長，把整個檔案讀進 context 是浪費。
> 這是值得套用到自家 CLI 工具的設計原則。

### 2. Reconnaissance-then-Action

`webapp-testing` 的核心 pattern：先「偵察」（截圖、列 DOM），再「行動」（下指令）。可推廣到任何不確定環境的自動化任務。

### 3. Eval-driven Iteration

`skill-creator` 與 `mcp-builder` 都建構在「跑評估 → 看結果 → 改 → 再跑」的迴圈上。`skill-creator` 甚至自動化此流程到 `run_loop.py` 一鍵跑 5 輪。

## 推薦學習順序

1. **claude-api** — 基本功（怎麼呼叫 Claude）
2. **skill-creator** — meta-skill（怎麼產出新能力）
3. **mcp-builder** — 把 skill 思維延伸到 service 層
4. **webapp-testing** — 自動化驗證
5. **web-artifacts-builder** — 進階前端輸出
6. **frontend-design** — 品味升級
