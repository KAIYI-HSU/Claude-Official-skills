# 企業溝通類 Skills

這 3 個 skills 處理「公司內部標準化輸出」——從文字（內部溝通）到視覺（品牌與主題），是 enterprise 場景最常用的能力。

| Skill | 解決問題 | 主要資產 |
|-------|----------|----------|
| [internal-comms](./internal-comms.md) | 各種內部溝通文件範本 | 4 份格式指南 |
| [brand-guidelines](./brand-guidelines.md) | 套用 Anthropic 品牌色與字型 | 7 色 + 2 字型規範 |
| [theme-factory](./theme-factory.md) | 10 套預設主題 + 客製主題 | 10 個 .md 主題定義 + 視覺 PDF |

## 共通設計模式

### 1. Examples / Themes 資料夾的「複數選擇」結構

3 個 skills 都把「多種選項」放在子資料夾各成一檔：
- `internal-comms/examples/` 裡放 4 種文件類型範本
- `theme-factory/themes/` 裡放 10 套主題

**好處**：Claude 可依使用者選擇只載入相關檔案，省 context。

### 2. 視覺索引（PDF showcase）

`theme-factory/theme-showcase.pdf` 是給人類看的、不給 Claude 改的視覺索引。

> 套用啟示：當你的工具有「視覺差異性高」的選項時，做一張 showcase 比寫 100 行描述更有效。

### 3. Brand-as-Skill 模式

`brand-guidelines` 完全是「規範文件」型 skill——沒有 script、沒有 examples，只有色碼與字型指示。但因為 Claude 會把這份規範當「執行指令」遵循，**比一般 brand book PDF 更可被 enforce**。

## 推薦學習順序

1. **internal-comms** — 學「example-based」skill 怎麼寫
2. **theme-factory** — 學「多選項 + 視覺 showcase」怎麼組織
3. **brand-guidelines** — 學「pure-instruction」型 skill 的極簡形態
