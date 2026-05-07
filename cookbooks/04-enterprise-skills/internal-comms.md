# internal-comms — 公司內部溝通文件樣板

## 一句話定位

把「內部溝通」拆成 4 種常見類型（3P 更新／週報／FAQ／一般），每種放一份格式指南到 `examples/` 資料夾，Claude 依使用者請求載入對應檔案。

## 何時觸發

- "幫我寫狀態報告"、"draft a leadership update"、"3P update"
- 公司週報（newsletter）、FAQ、事件報告（incident report）
- 任何「內部溝通」相關文件

## 目錄結構速覽

```
skills/internal-comms/
├── SKILL.md
├── LICENSE.txt
└── examples/
    ├── 3p-updates.md          # Progress / Plans / Problems 團隊週報
    ├── company-newsletter.md  # 公司週報
    ├── faq-answers.md         # FAQ 撰寫
    └── general-comms.md       # 其他類型（fallback）
```

## 核心觀念與工作流

### Skill 主流程（從 SKILL.md）

```
1. 從使用者請求判斷溝通類型
2. 載入 examples/ 內對應的 .md 指南
3. 依指南指示蒐集資訊、撰寫、格式化
4. 若不符合任何類型 → 詢問使用者期望格式
```

### 4 種文件類型

#### 1️⃣ 3P Updates（Progress / Plans / Problems）

- 適用：團隊週報、跨部門更新、scrum 周會輸出
- 風格：30–60 秒讀完的執行摘要
- 格式：emoji 開頭 + 團隊名 + 三段式
- 數據優先：用具體數字而非「進展順利」這種模糊用語

#### 2️⃣ Company Newsletter（公司週報）

- 適用：全公司週報、月報
- 結構：20–25 個 bullet，分區（Announcements / Progress / Leadership）
- 語氣：用 "we" 第一人稱複數
- 整合連結：Slack thread、Drive 文件、email 串、行事曆

#### 3️⃣ FAQ Answers

- 適用：對全公司常見疑惑的官方回答
- 結構：Q-A pair，根據實際 Slack/email/文件中觀察到的疑問
- 不要編造問題——必須是真有人問過

#### 4️⃣ General Comms（fallback）

未明確指定格式時的備用，會反問使用者目標、受眾、長度期望。

## 精華 Script 與可提取資源

雖然沒有 script，但 4 份範本檔本身就是極具參考價值的格式知識：

### 📋 套用到自家專案的「example-based skill」結構

```
my-skill/
├── SKILL.md      # 路由：判斷類型 → 載入對應 example
└── examples/
    ├── type-a.md
    ├── type-b.md
    └── fallback.md
```

當你的 skill 處理「多種子類型」（如不同類型的報告、不同程式語言、不同產業客戶），這個結構讓 Claude 只載入相關的，省 context、不混淆。

### 📋 資訊整合策略

`internal-comms` 預設 Claude 應主動詢問可否取得：
- Slack 訊息與 thread
- Google Drive 文件
- email 串
- Calendar 事件

這個「source-gathering checklist」可以套用到任何「總結散落資訊」的工具。

## 可移植到自家專案的模式

1. **Type Router 模式**：SKILL.md 當 router、examples 當 handler——這是非常可推廣的 skill 設計模式。

2. **「30–60 秒讀完」的限制**：把 3P update 限制在這個時間內，強迫精煉。可推廣到所有寫作任務的 budget 概念。

3. **數字 > 形容詞**：別寫「進度良好」，寫「完成 8/10 sprint stories」。

4. **第一人稱複數 "we"**：公司溝通用 we，不用 I 也不用第三人稱。

5. **只 quote 真實問題**：FAQ 的 Q 必須有人真的問過，避免 strawman。

## 常見陷阱（Gotchas）

- ❌ 寫成「萬字長文」報告 → 沒人讀；✅ 60 秒可掃完
- ❌ 「進展順利、團隊努力」這種空話 → 沒資訊；✅ 用數字或具體事件
- ❌ 一個 newsletter 涵蓋所有事 → 重點稀釋；✅ 分節 + 每節 5–7 點
- ❌ FAQ 自己造問題 → 戰略稻草人；✅ 從 Slack 找實際對話
- ❌ 不問受眾就寫 → 高層 vs 同事用詞不同；✅ 永遠先問 audience

## 延伸閱讀

- 官方檔：[`skills/internal-comms/SKILL.md`](../../skills/internal-comms/SKILL.md)
- 4 份格式範本：[`skills/internal-comms/examples/`](../../skills/internal-comms/examples/)
- 配對閱讀：[doc-coauthoring](../01-document-skills/doc-coauthoring.md)（更通用的協作文件流程）
