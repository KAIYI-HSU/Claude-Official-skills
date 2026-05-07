# Cookbook Web — 離線可部署的 Claude Skills 學習網站

把倉庫根目錄的 [`cookbooks/`](../cookbooks/) 繁中手冊渲染成可在企業內網運作的網頁學習介面，並內建 chatbot 助教，能透過 RAG 跨頁面檢索 cookbook 內容回答問題。

## 特色

- 🌐 **可離線部署**：image build 完成後 runtime 不需網路（embedding model 已 prefetch）
- 🔌 **LLM 格式 agnostic**：靠後端 proxy 適配 OpenAI 或 Anthropic 格式，前端不需感知差異
- 📚 **RAG 跨頁面檢索**：用 `intfloat/multilingual-e5-small`（118MB，支援繁中）embedding 全部 cookbook，chatbot 自動引用相關段落
- 🐳 **單一 Docker image**：`docker compose up` 一行起動
- 🎨 **Anthropic 品牌設計**：整合 `brand-guidelines` 的 7 色 + Poppins/Lora 字型
- 🧠 **智慧 context**：當使用者正在閱讀某頁時，該頁內容會自動加進 system prompt

## 架構

```
┌─────────────── Browser ───────────────┐
│  React SPA (Vite + TS + Tailwind)    │
│  ├─ Sidebar（24 個 cookbook 分類）   │
│  ├─ MarkdownView（react-markdown）   │
│  └─ ChatPanel（SSE 串流）           │
└──────────────── ▲ ─────────────────────┘
                  │ /api/*
┌──────────── FastAPI 後端 ──────────────┐
│  /api/cookbook/tree  目錄樹           │
│  /api/cookbook/page  頁面內容         │
│  /api/chat (SSE)     ─┐               │
└────────────────────────│──────────────┘
                          ▼
                    LLMProxy（格式適配）
                    ├─ openai → POST /chat/completions
                    └─ anthropic → POST /messages
                          ▼
                  企業內地端 LLM endpoint
                   (Ollama / vLLM / 自建...)
```

## 快速開始

### 0. 前置需求

- Docker + Docker Compose v2
- 企業內已存在 LLM endpoint（OpenAI 或 Anthropic 格式）

### 1. 設定 .env

```bash
cd cookbook-web
cp .env.example .env
# 編輯 .env，填入你的地端 LLM endpoint
```

### 2. 啟動

```bash
docker compose up -d --build
```

首次 build 約需 5–10 分鐘（下載 Python 套件 + embedding model），之後啟動秒開。

### 3. 開啟瀏覽器

訪問 <http://localhost:8000> 即可。

---

## 環境變數

| 變數 | 說明 | 範例 |
|------|------|------|
| `LLM_FORMAT` | `openai` 或 `anthropic` | `openai` |
| `LLM_ENDPOINT` | LLM endpoint base URL（不含 `/chat/completions`） | `http://internal-llm.corp:8000/v1` |
| `LLM_API_KEY` | API key；不需驗證可填任意值 | `sk-internal-xxx` |
| `LLM_MODEL` | 模型名稱 | `llama3-70b-instruct` |
| `LLM_TIMEOUT_SECONDS` | 串流逾時（秒） | `120` |

---

## 端點

| Method | Path | 說明 |
|--------|------|------|
| GET | `/api/health` | 健康檢查 |
| GET | `/api/cookbook/tree` | 目錄樹 JSON |
| GET | `/api/cookbook/page?path=01-document-skills/docx.md` | 單頁 markdown |
| POST | `/api/chat` | 串流 chat（SSE） |
| GET | `/` | SPA 入口 |

### Chat API 範例

請求：
```json
POST /api/chat
{
  "messages": [
    {"role": "user", "content": "easing.py 提供了什麼？"}
  ],
  "current_page": "02-creative-skills/slack-gif-creator.md"
}
```

回應（SSE）：
```
event: sources
data: [{"file_path":"02-creative-skills/slack-gif-creator.md","heading":"精華 Script 與可提取資源","score":0.84}, ...]

data: "easing.py"
data: " 提供"
data: " 14 種"
...
event: done
data: {}
```

---

## 開發模式（不需 Docker）

```bash
# 終端 1：後端
cd backend
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
COOKBOOK_DIR=$(pwd)/../../cookbooks \
  DATA_DIR=$(pwd)/.data \
  EMBEDDING_CACHE=$(pwd)/.models \
  FRONTEND_DIST=$(pwd)/../frontend/dist \
  LLM_ENDPOINT=http://localhost:11434/v1 \
  LLM_FORMAT=openai \
  LLM_MODEL=llama3 \
  uvicorn app.main:app --reload --port 8000

# 終端 2：前端
cd frontend
npm install
npm run dev   # http://localhost:5173 (透過 Vite proxy 接到 :8000)
```

---

## 部署到企業內網

### 步驟 1：在有網路的環境 build image

```bash
docker compose build
docker save cookbook-web:latest -o cookbook-web.tar
```

### 步驟 2：搬運 image 到企業內網

把 `cookbook-web.tar` + `docker-compose.yml` + `.env`（已設好內網 LLM endpoint）+ 整個 `cookbooks/` 拷貝進去。

### 步驟 3：在企業內網載入 image 並啟動

```bash
docker load -i cookbook-web.tar
docker compose up -d
```

完全不需要對外網路。

---

## 常見問題

### Q1: 第一次啟動 chat 慢？

第一次需要對 ~150 個 chunk 做 embedding（~10 秒）。結果會持久化到 `cookbook-data` volume，之後啟動秒開。

### Q2: 換了 LLM endpoint 但 chat 沒回應？

1. 確認 endpoint base URL **不含** `/chat/completions` 或 `/messages` 後綴
2. 檢查 `docker compose logs cookbook-web`，常見錯誤是 connection refused（網路）或 401（API key）
3. 用 `curl http://localhost:8000/api/health` 確認後端起來
4. 直接打 LLM endpoint 試試：`curl -H "Authorization: Bearer $LLM_API_KEY" -d '{"model":"...","messages":[{"role":"user","content":"hi"}]}' $LLM_ENDPOINT/chat/completions`

### Q3: cookbook 內容更新了，要重啟嗎？

- 頁面內容：唯讀掛載，**重新整理瀏覽器**即可
- RAG embedding：當 manifest 偵測到 chunk 改動時會自動重新 embed。若要強制重算，刪除 volume：`docker compose down && docker volume rm cookbook-web_cookbook-data && docker compose up -d`

### Q4: 想換 embedding model？

修改 `backend/app/config.py` 的 `EMBEDDING_MODEL`，並調整 Dockerfile 第二階段預下載的模型名稱。重 build。

### Q5: 想接 Claude Code Sonnet/Opus？

```bash
LLM_FORMAT=anthropic
LLM_ENDPOINT=https://api.anthropic.com/v1
LLM_API_KEY=sk-ant-xxx
LLM_MODEL=claude-opus-4-5
```

需要外網時不適合純離線部署，但若企業有 Anthropic 私有 endpoint 即可使用。

---

## 專案結構

```
cookbook-web/
├── README.md                # 本檔
├── .env.example
├── .gitignore
├── .dockerignore
├── Dockerfile               # 多階段（Node build → Python runtime + 預下載 model）
├── docker-compose.yml
├── frontend/                # Vite + React + TS + Tailwind
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   ├── postcss.config.js
│   ├── tsconfig.json
│   ├── tsconfig.node.json
│   ├── index.html
│   ├── public/
│   │   └── favicon.svg
│   └── src/
│       ├── main.tsx
│       ├── App.tsx
│       ├── components/
│       │   ├── Sidebar.tsx
│       │   ├── MarkdownView.tsx
│       │   ├── ChatPanel.tsx
│       │   ├── ChatMessage.tsx
│       │   └── CodeBlock.tsx
│       ├── hooks/
│       │   └── useStreamChat.ts
│       ├── lib/
│       │   └── api.ts
│       └── styles/
│           └── index.css
└── backend/                 # FastAPI
    ├── requirements.txt
    └── app/
        ├── __init__.py
        ├── main.py          # 路由 + SPA fallback
        ├── config.py        # pydantic-settings
        ├── llm_proxy.py     # 格式適配器
        ├── cookbook.py      # markdown 掃描 / 切 chunk
        ├── embeddings.py    # 啟動時 embed + 持久化
        └── rag.py           # 檢索 + system prompt 組裝
```

---

## 授權

本專案的程式碼採用與本倉庫相同的授權，請參閱根目錄 `THIRD_PARTY_NOTICES.md`。內嵌的 cookbook 內容延續原始 skills 的授權。
