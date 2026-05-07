# Repo Page — 純靜態單檔 HTML 瀏覽器

把 [`cookbooks/`](../cookbooks/) 的 24 個繁中 skill 手冊打包成**單一 self-contained HTML**，使用者不需任何安裝、不需後端、可直接雙擊開啟，也可放 GitHub Pages 作為 repo 入口。

## 三種使用方式

### 1. 直接開啟（最簡單）

下載 [`docs/index.html`](./index.html)，雙擊即可在瀏覽器看：

```bash
# Linux
xdg-open docs/index.html
# macOS
open docs/index.html
# Windows
start docs/index.html
```

完全離線運作，瀏覽器 DevTools 的 Network tab 不會有任何外部請求。

### 2. GitHub Pages

在 GitHub repo 的 **Settings → Pages**：
- **Source**：`Deploy from a branch`
- **Branch**：`repo-page`（或 merge 到 `main` 後選 `main`）
- **Folder**：`/docs`

等 1–2 分鐘後訪問：
```
https://<your-username>.github.io/Claude-Official-skills/
```

### 3. 本地 HTTP server

```bash
cd docs
python3 -m http.server 8000
# 開 http://localhost:8000
```

---

## 檔案結構

```
docs/
├── README.md          # 本檔
├── build.py           # 從 ../cookbooks/ 重新生成 index.html
├── template.html      # HTML 模板（含 CSS + JS placeholder）
├── _vendor/           # 預先下載的第三方 lib（已 commit，build 時無需網路）
│   ├── marked.min.js      (~35 KB)
│   └── highlight.min.js   (~125 KB)
└── index.html         # ⭐ 產出物 — 使用者打開的就是這個（~250 KB）
```

---

## 重新 build（cookbook 內容更新時）

```bash
cd docs
python3 build.py
```

預期輸出：
```
📂 scanning /home/user/Claude-Official-skills/cookbooks
  ✓ 24 markdown files
📦 ensuring vendor libs ...
  ✓ marked.min.js   (35,479 bytes)
  ✓ highlight.min.js (124,980 bytes)
✅ wrote index.html — 249.5 KB
```

`build.py` 純用 Python 標準庫，無需任何依賴。`_vendor/` 已被 commit，所以即使在離線環境也能重 build。

---

## 功能

- ✅ Sidebar 自動分組：3 個 root 入口（README、規範、跨 skill 模式）+ 4 個分類（文件／創意／開發／企業）
- ✅ Markdown 渲染：用 [marked.js](https://github.com/markedjs/marked)（~35 KB）
- ✅ 程式碼語法高亮：用 [highlight.js](https://highlightjs.org/)（~125 KB，內建多語言）
- ✅ 全文搜尋：頂部搜尋框即時 filter sidebar，含關鍵字片段預覽
- ✅ Hash routing：`#01-document-skills/docx.md` 可分享連結
- ✅ Markdown 內相對連結會自動轉為 hash route（點 `[xxx](../docx.md)` 會跳到對應頁）
- ✅ 響應式：手機上 sidebar 變成上方折疊區
- ✅ Anthropic 配色：ink + cream + orange 三色

---

## 與其他兩個分支的關係

| 分支 | 適合場景 | 部署方式 |
|------|----------|----------|
| `cookbooks` | 純文字、最原生格式 | GitHub 直接看 |
| `repo-page`（本分支） | 雙擊開啟 / GitHub Pages | 0 部署 |
| `cookbook-web` | 含 RAG chatbot 的完整版 | Docker compose |

三者並列、互補。

---

## 客製化

### 換 Markdown / 高亮 lib

修改 `build.py` 的 `MARKED_URL` / `HIGHLIGHT_URL`，刪掉 `_vendor/` 對應檔案再重 build。

### 改樣式

直接編輯 `template.html` 的 `<style>` 區塊，重 build。

### 增加功能（如暗色模式 / TOC）

編輯 `template.html` 的 `<script>` 區塊（最後一個 `<script>`），加入新邏輯。

---

## 授權

本目錄的程式碼採用與本倉庫相同的授權，請參閱根目錄 `THIRD_PARTY_NOTICES.md`。
- `marked.min.js` ：MIT License (markedjs/marked)
- `highlight.min.js`：BSD-3-Clause (highlightjs/highlight.js)
- 內嵌的 cookbook 內容延續原始 skills 的授權。
