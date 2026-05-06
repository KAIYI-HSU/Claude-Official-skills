# claude-api — Claude API / SDK 開發指南

## 一句話定位

把「在 Python / TypeScript / Java / Go / Ruby / PHP / C# / cURL 任一語言串接 Claude API」的所有最佳實務（模型選擇、prompt caching、tool use、Managed Agents、模型遷移）打包成一份多語言參考手冊。

## 何時觸發

- 程式碼出現 `import anthropic` 或 `@anthropic-ai/sdk`
- 使用者問 Claude API、Anthropic SDK、Managed Agents
- 加入／調整 caching、thinking、compaction、tool use、batch、files、citations、memory
- 模型遷移（4.5 → 4.6 → 4.7、退役模型替換）

❌ **不要**用於：`import openai`、檔名 `*-openai.py`、provider-neutral 程式碼。

## 目錄結構速覽

```
skills/claude-api/
├── SKILL.md                  # 路由與決策樹（~325 行）
├── shared/                   # 跨語言共享文件
│   ├── managed-agents-*.md   # 9 份 Managed Agents 文件
│   ├── prompt-caching.md
│   ├── tool-use-concepts.md
│   ├── agent-design.md
│   ├── model-migration.md    # 🌟 4.5→4.6→4.7 遷移指南
│   ├── error-codes.md
│   ├── models.md
│   └── live-sources.md       # 🌟 官方 SDK repo URL 清單
├── python/claude-api/        # Python 範例（streaming、tool-use、batches、files-api）
├── typescript/claude-api/    # 同上
├── java/、go/、ruby/、php/、csharp/、curl/    # 各語言實作
└── managed-agents/           # 各語言的 Managed Agents 範例
```

## 核心觀念與工作流

### Step 0: 語言偵測

| 檔案類型 | 對應目錄 |
|----------|----------|
| `*.py`、`requirements.txt` | `python/` |
| `*.ts`、`*.tsx`、`package.json` | `typescript/` |
| `*.js`（無 `.ts`） | `typescript/` |
| `*.java`、`*.kt`、`pom.xml` | `java/` |
| `*.go` | `go/` |
| `*.rb` | `ruby/` |
| `*.cs` | `csharp/` |
| `*.php` | `php/` |
| 其他 / 純 shell | `curl/` |

### Step 1: Surface 選擇

| 任務 | Surface | 理由 |
|------|---------|------|
| 分類、摘要、抽取、Q&A | **單次 API call** | 最簡單 |
| 批次處理、Embedding | **Claude API + Batches** | 專屬 endpoint |
| 多步流程、自寫 loop | **API + Tool Use** | 你掌控 loop |
| 開放式探索、agent 行為 | **Managed Agents** | 託管狀態 |

### 預設值（除非使用者明說否則照這套）

```python
import anthropic
client = anthropic.Anthropic()

response = client.messages.create(
    model="claude-opus-4-7",                           # 預設最新最強模型
    thinking={"type": "adaptive"},                      # 4.7 起推薦的 adaptive thinking
    max_tokens=4096,
    messages=[{"role": "user", "content": "..."}],
)
```

任何長輸入、長輸出、或大 `max_tokens` 一律用 streaming：
```python
with client.messages.stream(...) as stream:
    final = stream.get_final_message()    # 不需要逐 chunk 處理時的便利方法
```

### Prompt Caching（必用）

```python
response = client.messages.create(
    model="claude-opus-4-7",
    system=[
        {"type": "text", "text": "Long instructions ...",
         "cache_control": {"type": "ephemeral"}}        # 標記此區塊可被快取
    ],
    messages=[{"role": "user", "content": "Question 1"}],
)
```

> 同一個 system prompt 重用多次時，從第二次起 cache hit，token 計費大幅折扣。詳見 `shared/prompt-caching.md`。

### Managed Agents（4.7 新東西）

關鍵概念：**Agent 是持久的（建一次→重複使用 ID），Session 才是短暫的**。

```python
# 一次性：建立 agent 並存下 ID
agent = client.beta.agents.create(name="my-helper", ...)
agent_id = agent.id
# ... 寫進 config

# 每次互動：用 agent_id 開新 session
session = client.beta.agents.sessions.create(agent_id=agent_id, ...)
```

❌ 千萬不要在 request path 裡呼叫 `agents.create`。

### 模型遷移

| 升級 | 主要變化 |
|------|----------|
| 4.5 → 4.6 | Sonnet 4.6 大幅性能提升 |
| 4.6 → 4.7 | `thinking={type: "adaptive"}` 取代 `budget_tokens`；新 Managed Agents |

詳細對照表見 `shared/model-migration.md`。

## 精華 Script 與可提取資源

### 📚 `shared/live-sources.md`

官方 SDK repo 的權威 URL 清單。**遇到不確定的 binding 時，先 WebFetch 此檔列出的 repo README**，不要憑感覺寫。

### 📚 `shared/model-migration.md`

跨版本升級的 cheat sheet——每個版本變了什麼參數、什麼方法被刪除、什麼推薦新做法。

### 📚 `shared/managed-agents-*.md`（9 份）

涵蓋 overview、core、tools、events、memory、client-patterns、onboarding、environments、api-reference。要用 Managed Agents 時，**這份文件比直接看 SDK 程式碼更系統化**。

## 可移植到自家專案的模式

1. **語言偵測表**：套用到任何「多語言 SDK 文件」場景。

2. **Default-best 配置**：永遠用最新模型 + adaptive thinking + streaming + caching，把這 4 項當預設。

3. **Agent ID 持久化**：把 LLM agent 視為 service object（建一次、長存），不要每次呼叫都重建。

4. **不混用 SDK 與 raw HTTP**：在同一檔案裡選一個就堅持下去，避免 `requests.post` 與 `client.messages.create` 混用。

## 常見陷阱（Gotchas）

- ❌ 在 OpenAI 程式碼裡硬塞 Anthropic SDK 呼叫 → skill 明文禁止；先問使用者要哪邊
- ❌ 自己猜其他語言的 binding（從 cURL 形狀推 Java method）→ 一律 WebFetch 官方 README
- ❌ `agents.create` 寫在 request handler 裡 → 每次請求都建新 agent，浪費資源
- ❌ 預設 `thinking={"type": "enabled", "budget_tokens": 1024}` → 這是 4.6 寫法，4.7 用 `adaptive`
- ❌ 長輸出不開 streaming → 容易 timeout

## 延伸閱讀

- 官方檔：[`skills/claude-api/SKILL.md`](../../skills/claude-api/SKILL.md)
- 多語言子目錄：[`skills/claude-api/python/`](../../skills/claude-api/python/) 等
- Managed Agents：[`skills/claude-api/shared/managed-agents-overview.md`](../../skills/claude-api/shared/managed-agents-overview.md)
- 模型遷移：[`skills/claude-api/shared/model-migration.md`](../../skills/claude-api/shared/model-migration.md)
- 官方 SDK：見 `shared/live-sources.md`
