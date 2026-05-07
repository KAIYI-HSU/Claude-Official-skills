# mcp-builder — MCP Server 開發指南

## 一句話定位

把「為 LLM 寫 MCP server」拆成 4 個 phase（研究 → 實作 → 審查 → 評估），預設 TypeScript + Streamable HTTP，內建 10 題 Q&A 評估框架。

## 何時觸發

- 建立 MCP server，整合外部 API／服務
- 用 Python（FastMCP）或 Node/TypeScript（MCP SDK）
- 包裝公司內部服務給 Claude／其他 LLM 使用

## 目錄結構速覽

```
skills/mcp-builder/
├── SKILL.md                      # 4 phase 工作流
├── scripts/
│   ├── connections.py            # API client 測試輔助
│   ├── evaluation.py             # 跑 Q&A 評估
│   ├── example_evaluation.xml    # 評估格式範本
│   └── requirements.txt
└── reference/
    ├── mcp_best_practices.md     # 命名、傳輸、分頁、錯誤處理規範
    ├── node_mcp_server.md        # 🌟 TypeScript SDK + Zod 完整範例（~550 行）
    ├── python_mcp_server.md      # 🌟 FastMCP + Pydantic 完整範例（~550 行）
    └── evaluation.md             # 評估設計指南
```

## 核心觀念與工作流

### 4 Phase 工作流

#### Phase 1: 研究與規劃

- 讀 MCP spec：`https://modelcontextprotocol.io/sitemap.xml` → 加 `.md` 後綴抓 markdown
- 讀目標服務的 API 文件
- 推薦 stack：**TypeScript + Streamable HTTP**（無狀態 JSON）

#### Phase 2: 實作

**專案結構**（見 `reference/node_mcp_server.md` 或 `python_mcp_server.md` 完整範例）：
- 共享 utilities：API client + auth、錯誤處理、回應格式化、分頁
- 每個 tool 用 Zod（TS）或 Pydantic（Py）定義 input/output schema

```typescript
// TypeScript with Zod
server.registerTool({
  name: "github_create_issue",
  description: "Create a GitHub issue.",
  inputSchema: z.object({
    repo: z.string().describe("Format: owner/name"),
    title: z.string(),
    body: z.string().optional(),
  }),
  outputSchema: z.object({
    number: z.number(),
    url: z.string(),
  }),
  annotations: { destructiveHint: false, idempotentHint: false },
}, async (input) => { /* ... */ });
```

#### Phase 3: 審查與測試

- DRY 原則、一致的錯誤處理、完整 type 覆蓋
- TypeScript：`npm run build`、`npx @modelcontextprotocol/inspector`
- Python：`python -m py_compile`、用 MCP Inspector 互動測試

#### Phase 4: 建立評估

寫 **10 個 Q&A pair**，每題要：
- ✅ Independent（不依賴前題）
- ✅ Read-only（不變更資料）
- ✅ Complex（需多次工具呼叫）
- ✅ Realistic（真實使用情境）
- ✅ Verifiable（單一明確答案）
- ✅ Stable（答案不會隨時間變）

XML 格式：
```xml
<evaluation>
  <qa_pair>
    <question>找出含 ASL-X 安全標示的 AI 模型討論，名字像「斑點野貓」的模型其 X 值為何？</question>
    <answer>3</answer>
  </qa_pair>
</evaluation>
```

## 精華 Script 與可提取資源

### 🔧 `scripts/evaluation.py`

跑 XML 中的 Q&A，把答案餵給有 MCP server 的 Claude，比對結果並給分數。**這是「客觀衡量 LLM 工具品質」的範本**——你做任何 dev tool 都該有類似評估。

### 📚 `reference/mcp_best_practices.md`

精華規範清單：
- 工具命名：`{service}_{action}_{resource}` 例如 `github_list_repos`
- 回應格式：JSON 給結構化、Markdown 給給人類閱讀
- 分頁預設 limit；超過用 `next_token` cursor
- 傳輸：本地 stdio、遠端 streamable HTTP（無狀態優先）

### 📚 `reference/node_mcp_server.md` & `python_mcp_server.md`

**~550 行的完整範例**，從 `package.json` 到實際 tool function 都有，能直接拷貝為起點。

## 可移植到自家專案的模式

1. **4-Phase 流程**（研究 → 實作 → 審查 → 評估）：套用到任何「為 LLM 設計 API」的工作。

2. **Tool 命名規範**：在自家工具集統一 `{service}_{action}_{resource}`，提升 LLM 找到正確工具的機率。

3. **Annotation 標籤**：
   ```
   readOnlyHint: true        # 不會改資料
   destructiveHint: true     # 會刪除東西
   idempotentHint: true      # 多次呼叫結果一致
   openWorldHint: true       # 與外部世界互動（網路）
   ```
   這 4 個布林值幫助 LLM 決定何時可以放心呼叫。

4. **Actionable 錯誤訊息**：別只寫 `"Error: 404"`，要寫 `"Issue #123 not found in repo X. Use github_list_issues to find existing IDs."`。

5. **10 題 Q&A 評估**：任何工具集都該有客觀題庫，避免「LLM 看起來會用了」這種主觀判斷。

## 常見陷阱（Gotchas）

- ❌ 工具名混用 camelCase / snake_case → LLM 困惑；✅ 一致命名
- ❌ 把全部 API 端點都包成 tool → context 爆炸；✅ 包常用的 + 預留 `code execution`
- ❌ 回應只丟整顆 JSON → token 浪費；✅ 預設只回必要欄位、加 `?fields=` 參數
- ❌ 沒寫 evaluation.xml → 不知道改動有沒有變更好；✅ 一定要建立 baseline
- ❌ 把 stateful session 用在 streamable HTTP server → 難 scale；✅ 預設無狀態 JSON

## 延伸閱讀

- 官方檔：[`skills/mcp-builder/SKILL.md`](../../skills/mcp-builder/SKILL.md)
- TypeScript 範例：[`skills/mcp-builder/reference/node_mcp_server.md`](../../skills/mcp-builder/reference/node_mcp_server.md)
- Python 範例：[`skills/mcp-builder/reference/python_mcp_server.md`](../../skills/mcp-builder/reference/python_mcp_server.md)
- 評估指南：[`skills/mcp-builder/reference/evaluation.md`](../../skills/mcp-builder/reference/evaluation.md)
- MCP 官方規範：<https://modelcontextprotocol.io/sitemap.xml>
