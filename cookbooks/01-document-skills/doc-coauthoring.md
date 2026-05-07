# doc-coauthoring — 結構化共筆流程

## 一句話定位

不是工具型 skill，而是**流程型** skill：把「Claude 幫使用者寫一份正式文件」拆成三階段（資訊蒐集 → 精煉 → 讀者測試），避免一次性產出冗長文章卻句句不到位。

## 何時觸發

- "幫我寫提案"、"draft a proposal"、"create a spec"、"撰寫 RFC"
- 任何結構化、有受眾、有目的的長文（決策文件、技術設計文件、年度回顧）

## 目錄結構速覽

```
skills/doc-coauthoring/
└── SKILL.md     # 唯一檔案，~16KB，純流程描述
```

> 沒有 scripts、沒有 examples——這是「方法論」型 skill 的代表作。

## 核心觀念與工作流

### 三階段流程

#### 🎯 Stage 1: Context Gathering（資訊蒐集）

**目標**：在落筆前把使用者腦中的隱性知識全榨出來。

操作：
1. **Meta-context 提問**：受眾是誰？影響什麼決策？有沒有公司常用範本？
2. **Info dumping**：請使用者貼 Slack 訊息、Drive 文件、email 內容、會議摘要
3. **Clarifying questions**：根據 gap 主動問「我注意到你沒提到 X，這部分你怎麼想？」

**為什麼重要**：80% 的失敗草稿是因為 Claude 一開始就沒搞清楚「文件存在的目的」。

#### ✏️ Stage 2: Refinement & Structure（精煉與結構化）

**目標**：以 section 為單位反覆迭代，避免一次重寫整篇。

操作：
1. 為每個 section 提 clarifying questions
2. **Brainstorm 5–20 點**（別只給 3 點，要遍歷可能性）
3. **Curation**：保留／移除／合併
4. **Gap check**：「漏了什麼？」
5. **Drafting with surgical edits**：用 Edit tool 改局部，**永遠不要 reprint 整篇**
6. **Iterative refinement**：使用者反饋 → 局部修

#### 🔍 Stage 3: Reader Testing（讀者測試）

**目標**：用「全新眼睛」確認冷讀者也能看懂。

操作：
1. 預測讀者會問哪些問題
2. **Spawn fresh Claude subagent**（沒有任何上下文）讀文件並提問
3. 或請使用者貼到 Claude.ai 新對話
4. 找出 ambiguity，回頭修
5. 確認後才 release

> **這個 fresh-eyes 模式**也出現在 `pptx`、`skill-creator`，是 Anthropic 官方愛用的元 pattern。

## 精華 Script 與可提取資源

雖然此 skill 沒有 script，但它的**流程模板**極具重用價值：

### 📝 Stage 1 提問模板

```
- 這份文件的主要受眾是誰？（執行長／工程同事／外部客戶？）
- 讀完後你希望他們做什麼決定／行動？
- 有沒有公司常用的格式或範例可以參考？
- 有相關的 Slack 討論串、Drive 文件、email 紀錄可以提供嗎？
- 截止日期？篇幅期望？
```

### 📝 Stage 2 Section 開展模板

```
For each section:
1. "這段要回答什麼核心問題？"
2. "幫我列 10 個可能的論點"
3. "哪 3 個最重要？哪些可以合併？"
4. "還有什麼角度沒考慮？"
5. <draft>
6. "這段哪裡卡？"
```

### 📝 Stage 3 Reader Test 模板

```
你是第一次看到這份文件的 [角色]。
請完整讀過，然後告訴我：
1. 你看完後的主要 takeaway 是什麼？
2. 哪 3 個地方你需要重看才懂？
3. 你會問作者哪些問題？
4. 哪些段落讓你想跳過？
```

## 可移植到自家專案的模式

1. **三階段框架**：Context → Refinement → Reader Test，可以套用到：
   - 寫 README
   - 寫 PR description
   - 寫部落格文章
   - 寫產品 spec

2. **Surgical Edit 原則**：迭代時用 `Edit` 工具改局部，不要 `Write` 整檔重來。理由：
   - 使用者可一目了然看到改動
   - Token 消耗少
   - 不會誤刪好句

3. **Brainstorm 5–20 點**：強制廣度搜索，比起「給我 3 個點子」更能避免淺薄。

4. **Subagent 冷讀者**：用 `Agent({subagent_type: "general-purpose"})` 啟動沒有對話歷史的 Claude，模擬真實讀者。

## 常見陷阱（Gotchas）

- ❌ 直接開始寫 → 沒搞清楚受眾與目的，產出泛泛之談
- ❌ 一次重寫整篇 → 浪費 token、改壞好段落；✅ 用 Edit 局部改
- ❌ 跳過 reader test → 作者盲點留到 release；✅ 一定要 fresh eyes 過
- ❌ 用「我覺得這樣寫好」替代用戶意圖 → 文件變成 Claude 的而非使用者的

## 延伸閱讀

- 官方檔：[`skills/doc-coauthoring/SKILL.md`](../../skills/doc-coauthoring/SKILL.md)
- 相似的 fresh-eyes 模式：[`skills/pptx/SKILL.md`](../../skills/pptx/SKILL.md)（視覺 QA）、[`skills/skill-creator/SKILL.md`](../../skills/skill-creator/SKILL.md)（grader subagent）
