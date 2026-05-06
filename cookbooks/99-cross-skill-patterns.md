# 跨 Skill 共通模式與設計哲學

讀完 17 個 skills 後，可歸納出 Anthropic 在設計 skill 時反覆使用的**元 pattern**。把這些 pattern 內化，能讓你做出更系統化、可維護的 skills。

---

## Pattern 1: Office Unpack/Pack/Validate 共享基建

**出現於**：docx、pptx、xlsx

三者底層是同一套 ZIP+XML 結構，所以共用 `scripts/office/`：
- `unpack.py` — 拆解 + 美化 + 智慧引號實體化
- `pack.py` — 重組 + 自動修正 durableId 與 xml:space
- `validate.py` — OOXML schema 驗證
- `soffice.py` — LibreOffice headless 包裝

**啟示**：當多個 skill 處理結構相近的格式時，**抽出共享 utilities**，每個 skill 用 symlink 或 import 引用。

---

## Pattern 2: Philosophy-First 雙步驟設計法

**出現於**：canvas-design、algorithmic-art

兩者都要求：
1. **Step 1：寫 4–6 段美學宣言**（命名一個流派、描述 form/space/color/composition）
2. **Step 2：用具體技術實現**（PIL 畫到 PDF、p5.js 寫到 HTML）

**啟示**：任何「主觀美學任務」都該強迫先寫宣言再執行，避免「先動手，再調整」的隨機輸出。可推廣：
- 寫部落格文章前先寫「角度宣言」
- 寫程式前先寫「設計目標宣言」
- UI 重設計前先選 tone（見 [frontend-design](./03-dev-technical-skills/frontend-design.md)）

---

## Pattern 3: Black-box Script 哲學

**出現於**：webapp-testing、web-artifacts-builder、skill-creator

明確要求：**先 `--help` 再用，除非絕對必要否則不要讀原始碼**。

引用原文：
> These scripts can be very large and thus pollute your context window. They exist to be called directly as black-box scripts rather than ingested into your context window.

**啟示**：寫給 LLM 用的 CLI 工具，一定要：
- 完善 `--help` 輸出
- 命令列接口穩定
- 預設值合理
- 錯誤訊息 actionable

---

## Pattern 4: Reconnaissance-then-Action（偵察後行動）

**出現於**：webapp-testing（明確）、pdf 表單填寫（隱含）、pptx 視覺 QA（隱含）

```
1. 先「偵察」現況（截圖、列 DOM、抽 schema）
2. 從偵察結果決定 selector / 行動 / 參數
3. 再「執行」
```

**啟示**：不確定環境的自動化任務都該分這兩階段，避免假設失誤導致整體失敗。

---

## Pattern 5: Fresh-Eyes Subagent QA

**出現於**：doc-coauthoring、pptx、skill-creator

派一個**沒有對話歷史**的 subagent 來：
- 讀文件並提問（doc-coauthoring）
- 看簡報截圖找視覺問題（pptx）
- 評分 skill 輸出（skill-creator 的 grader）

**啟示**：作者／執行者有盲點。把「審查」工作交給冷讀者 subagent，是 LLM 應用獨有且強大的 pattern。

---

## Pattern 6: Eval-Driven Iteration

**出現於**：skill-creator（核心）、mcp-builder（4-Phase 的 Phase 4）

迴圈：
```
寫測試 → 跑測試 → 看結果 → 改 → 重跑
```

skill-creator 甚至自動化此流程到 `run_loop.py`：5 輪自動優化 description。

**啟示**：任何「LLM 輔助開發」工具都該有客觀題庫，避免「看起來會用了」的主觀錯覺。

---

## Pattern 7: Progressive Disclosure（漸進式揭露）

**出現於**：claude-api、mcp-builder、pdf

主 SKILL.md 簡潔，把細節推到子目錄：
- `references/`、`shared/`、`reference/`
- 子目錄按主題或語言切分

```
mcp-builder/
├── SKILL.md                      # ~200 行：路由 + 4 phase
└── reference/
    ├── mcp_best_practices.md     # 通用規範
    ├── node_mcp_server.md        # ~550 行：TS 詳解
    ├── python_mcp_server.md      # ~550 行：Py 詳解
    └── evaluation.md
```

**啟示**：別把所有資訊塞進 SKILL.md。Claude 是動態載入的，**根據觸發情境只讀需要的**才能省 token。

---

## Pattern 8: Type Router + Examples 子目錄

**出現於**：internal-comms（4 種 comms 類型）、theme-factory（10 套主題）

主 SKILL.md 是路由：「判斷類型 → 載入對應子檔」。

**啟示**：當 skill 處理多個子類型時，這個結構讓：
- Claude 只載入相關 example，省 context
- 新增類型不影響既有
- 結構自我說明（資料夾即文件）

---

## Pattern 9: Pushy Description（有點推銷感的描述）

**出現於**：skill-creator 明確建議；docx、pdf 等實際採用

skill-creator 直接點名：
> 反例：`How to build a dashboard.`
> 正例：`How to build a dashboard. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'`

**啟示**：因為 Claude 傾向 undertrigger，描述要：
- 列具體觸發字眼
- 多舉幾個情境
- 用 "Make sure to use" 等強烈語彙

但要**配對 near-miss negatives**確認沒 overtrigger（見 skill-creator 的 trigger eval 流程）。

---

## Pattern 10: 視覺索引（Showcase）

**出現於**：theme-factory（PDF）、algorithmic-art（viewer.html）、pptx（thumbnail.py 拼圖）

當「光看文字選不出來」時，提供視覺 catalog。

**啟示**：UI 工具、設計工具、樣式選擇——任何視覺差異敏感的場景都該有 showcase。

---

## Pattern 11: Validator/Linter 前置檢查

**出現於**：docx（validate.py）、xlsx（recalc.py 報錯）、slack-gif-creator（validators.py）、pptx（validate.py）

每個產出檔案的 skill 都附驗證器，輸出前自動檢查：
- Schema 合規
- 規格限制（GIF 大小、Slack 限制）
- 公式錯誤（#REF! 等）

**啟示**：任何工具的最後一步都該有 lint/validate，不要把問題推給 end user 去發現。

---

## Pattern 12: 最簡可用形態（Minimum Viable Skill）

**出現於**：brand-guidelines（純文字規範）、frontend-design（純設計思考）、doc-coauthoring（純流程）

證明：**Skill 不一定要有 script**。當核心價值是「規範／流程／思維框架」時，純文字 instruction 已足夠。

**啟示**：別過度工程。問自己「這個 skill 真的需要程式碼嗎？」很多時候一份好寫的 SKILL.md 就贏了。

---

## Pattern 13: Smart Fallback

**出現於**：brand-guidelines（字型 fallback）、claude-api（語言偵測 fallback 到 Python）

當依賴條件不滿足，**降級而非阻擋**：
- 字型沒裝 → 用 Arial/Georgia
- 語言難判斷 → 預設 Python 並提示

**啟示**：工具不該因為「環境不完美」就罷工，要 graceful degrade。

---

## Pattern 14: 跨 Skill 互相引用

**出現於**：多個 skill SKILL.md 內

例如：
- `web-artifacts-builder` 提醒避免 AI slop → 推薦讀 `frontend-design`
- `pptx` 的視覺 QA 概念 → 與 `doc-coauthoring` 的 reader test 同源
- `theme-factory` 與 `brand-guidelines` 互補

**啟示**：Skill 之間應該有引用網絡，不要互相孤立。在自家 skill ecosystem 裡建立交叉引用，提升可發現性。

---

## 總結：12 條 Skill 設計鐵律

1. ✅ 共享基建抽 utilities，不重複實作
2. ✅ 主觀任務先寫宣言再執行
3. ✅ Script 設計成 black box（`--help` 友善）
4. ✅ 不確定環境先偵察再行動
5. ✅ 用 fresh-eyes subagent 做 QA
6. ✅ Eval-driven 迭代，不憑感覺
7. ✅ Progressive disclosure，分層揭露
8. ✅ 多子類型用 router + examples 結構
9. ✅ Description 寫得 pushy 但要 negative test
10. ✅ 視覺差異大就做 showcase
11. ✅ 最後一步必驗證
12. ✅ 最簡可用：能不寫 script 就別寫
13. ✅ Smart fallback，不要阻擋使用者
14. ✅ Skill 互相引用，建立網絡

---

## 推薦進一步閱讀

- 官方 spec：<https://agentskills.io/specification>
- 原始 SKILL.md 之最佳範本：[`skills/skill-creator/SKILL.md`](../skills/skill-creator/SKILL.md)（meta，最完整）
- 哲學優先範本：[`skills/algorithmic-art/SKILL.md`](../skills/algorithmic-art/SKILL.md)
- 簡潔風範本：[`skills/brand-guidelines/SKILL.md`](../skills/brand-guidelines/SKILL.md)
- 4-Phase 工作流範本：[`skills/mcp-builder/SKILL.md`](../skills/mcp-builder/SKILL.md)
