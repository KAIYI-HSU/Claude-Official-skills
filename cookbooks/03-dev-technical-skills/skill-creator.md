# skill-creator — 寫 Skill 的 Skill（Meta）

## 一句話定位

製作、評估、最佳化 skill 本身的 meta-skill。提供完整的「draft → 評估 → 迭代 → 描述優化」迴圈，含 grader/comparator/analyzer 三個 subagent 與 React-based 評估檢視器。

## 何時觸發

- 「我想做一個 skill 來幫我...」
- 已有 skill 草稿、要跑評估
- 想優化 skill 的 description 觸發準確率
- benchmark 多個 skill 版本比較

## 目錄結構速覽

```
skills/skill-creator/
├── SKILL.md                # 完整迭代迴圈（~486 行）
├── scripts/
│   ├── aggregate_benchmark.py   # 合併多次跑分為 benchmark.json
│   ├── run_loop.py              # 🌟 描述優化迴圈（5 輪 60/40 分割）
│   ├── run_eval.py              # 觸發單次評估
│   ├── generate_report.py       # 產 HTML 報表
│   ├── package_skill.py         # 打包成 .skill 檔
│   ├── quick_validate.py        # 語法 sanity check
│   ├── improve_description.py   # 單次描述修訂
│   └── utils.py
├── agents/                  # subagent 提示
│   ├── grader.md            # 評分員：assertion 對輸出
│   ├── comparator.md        # 比對員：盲測 A/B
│   └── analyzer.md          # 分析員：找 outlier、無辨識度的 assertion
├── eval-viewer/             # 瀏覽器評估檢視器
│   ├── generate_review.py
│   └── viewer.html          # 🌟 React-based 比較介面
├── references/
│   └── schemas.md           # evals.json 等 schema 參考
└── assets/
    └── eval_review.html     # 互動式 query 編輯模板
```

## 核心觀念與工作流

### 完整迴圈

```
意圖捕捉 → 草稿 SKILL.md → 撰寫測試 → 跑評估 → 看結果 →
   ↓                                                ↓
   ←—————————— 修改 SKILL.md ←——————————————————————
                    ↓
              描述優化（run_loop.py）
                    ↓
                打包 .skill
```

### Step 1: 意圖捕捉（4 題訪談）

```
1. 這個 skill 應該讓 Claude 做什麼？
2. 何時該觸發？（user 的什麼話／情境）
3. 期望輸出格式？
4. 要不要建測試？（客觀可驗證的→建議要；主觀如寫作/藝術→可選）
```

### Step 2: 寫 SKILL.md

關鍵建議（直接抄）：
- **description 寫得「有點 pushy」**：因為 Claude 傾向 undertrigger
- 反例：`How to build a dashboard.`
- 正例：`How to build a dashboard. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'`

### Step 3: 評估架構

**並行跑兩組 subagent**：
- **with-skill**：載入此 skill
- **baseline**：沒有 skill

每個輸出由 `agents/grader.md` 配方的評分員針對 assertion 評分，產出：
```json
{
  "assertions": [
    {"text": "輸出包含 TOC", "passed": true, "evidence": "見第 3 行"},
    {"text": "使用 #FF0000 色碼", "passed": false, "evidence": "用了 #FF1234"}
  ]
}
```

### Step 4: Benchmark

`aggregate_benchmark.py` 對多次 run 取統計：
- pass_rate ± stddev
- token usage delta（vs baseline）
- time delta
- 分析員觀察（見 `agents/analyzer.md`）

### Step 5: 描述優化迴圈（殺手鐧）

`run_loop.py` 自動跑：
1. 把 trigger eval 切 60/40（train/test）
2. 對當前 description 跑 3 次，量觸發準確率
3. 用 `improve_description.py` 提出修改版本
4. 重新評估
5. 重複 5 輪，挑 test set 表現最好的版本

**準備材料**：
- 8–10 個「該觸發」的 query（positive）
- 8–10 個「不該觸發但接近」的 query（near-miss negative）

## 精華 Script 與可提取資源

### 🌟 `scripts/run_loop.py`（必看）

封裝完整的「LLM-as-judge + 反覆迭代」框架。可挪用到任何「想自動優化 prompt」的場景：A/B 測試 prompt → 評分 → 用另一個 LLM 提改進 → 重跑。

### 🌟 `eval-viewer/viewer.html`

React-based 比較介面，分頁顯示：
- **Outputs tab**：每個 eval 的 with-skill / baseline 並列
- **Benchmark tab**：統計圖表（pass_rate、token、time）
- 內建 user feedback 收集

> 📍 **可挪用**：任何「需要肉眼比對 LLM 輸出」的場景都可以複製這個 viewer。

### 🌟 `agents/grader.md`、`comparator.md`、`analyzer.md`

3 個 subagent 提示詞範本：
- **grader**：給定 assertion + output，判 passed 並給 evidence
- **comparator**：盲測 A/B，給出哪個更好 + 理由
- **analyzer**：看完一輪 benchmark，找出無辨識度的 assertion（不管哪個版本都通過＝無價值）

### 🔧 `scripts/package_skill.py`

把整個 skill 資料夾打包成 `.skill` 分發檔。

## 可移植到自家專案的模式

1. **「Description 寫得 pushy」**：自家工具的描述也別客氣，明確列舉觸發情境。

2. **Trigger Eval（pos + near-miss）**：寫 8 個「該用」+ 8 個「不該用」query 是測試任何 router／classifier 的好方法。

3. **Subagent 評分架構**：把「執行任務的 agent」與「評分的 agent」分開，避免自我評估偏誤。

4. **Schema 標準化**（見 `references/schemas.md`）：
   - `evals.json`：題目庫
   - `grading.json`：每次評分結果
   - `benchmark.json`：跨多次 run 的統計

5. **HTML viewer 複製**：把 `viewer.html` 改成你自己工具的結果檢視器，不必每次重寫。

## 常見陷阱（Gotchas）

- ❌ description 寫太短／含糊 → undertrigger；✅ 列具體 trigger 字眼
- ❌ assertion 太籠統（"輸出要好"）→ 沒辨識度；✅ 「包含特定字串/格式」
- ❌ 只跑一次評估就下結論 → variance 大；✅ 跑 ≥ 3 次取平均
- ❌ 沒準備 near-miss negatives → 描述會 overtrigger；✅ 8 個負例不能省
- ❌ 把 grader 用同個對話 context 評分 → 偏誤；✅ 用獨立 subagent

## 延伸閱讀

- 官方檔：[`skills/skill-creator/SKILL.md`](../../skills/skill-creator/SKILL.md)
- 描述優化迴圈：[`skills/skill-creator/scripts/run_loop.py`](../../skills/skill-creator/scripts/run_loop.py)
- Schema 參考：[`skills/skill-creator/references/schemas.md`](../../skills/skill-creator/references/schemas.md)
- Subagent 提示：[`skills/skill-creator/agents/`](../../skills/skill-creator/agents/)
- 評估檢視器：[`skills/skill-creator/eval-viewer/viewer.html`](../../skills/skill-creator/eval-viewer/viewer.html)
