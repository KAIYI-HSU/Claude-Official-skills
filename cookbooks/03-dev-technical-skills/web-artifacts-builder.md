# web-artifacts-builder — React + shadcn artifact 製作器

## 一句話定位

把「複雜的 React + Tailwind + shadcn/ui artifact」一鍵 init／一鍵 bundle 成單檔 HTML，可貼進 Claude 對話分享；內附 40+ 預裝 shadcn/ui 元件。

## 何時觸發

- 建立**複雜**的 Claude.ai artifact（含狀態管理、routing、shadcn 元件）
- 不適用：簡單單檔 HTML/JSX artifact（直接寫即可）

## 目錄結構速覽

```
skills/web-artifacts-builder/
├── SKILL.md                        # 4 步驟工作流（~75 行）
└── scripts/
    ├── init-artifact.sh            # 🌟 React 專案初始化
    ├── bundle-artifact.sh          # 🌟 打包成單檔 HTML
    └── shadcn-components.tar.gz    # 40+ 預裝元件
```

## 核心觀念與工作流

### 4 步驟

```bash
# Step 1: 初始化
bash scripts/init-artifact.sh my-artifact
cd my-artifact

# Step 2: 開發（編輯生成的檔案）
npm run dev

# Step 3: 打包成單檔 HTML
bash scripts/bundle-artifact.sh
# 產出 bundle.html — 自含所有 JS/CSS

# Step 4: 把 bundle.html 內容貼進 Claude 對話即可分享
```

### Stack 組成

| 層 | 工具 |
|-----|------|
| Framework | React 18 + TypeScript |
| Dev Server | Vite |
| Bundler | Parcel + html-inline |
| 樣式 | Tailwind CSS 3.4.1 |
| UI 元件 | shadcn/ui（40+ 預裝） |
| Path alias | `@/` |

### init-artifact.sh 做了什麼

- 偵測 Node 版本，自動 pin 對應 Vite 版本（Node 18+ 相容）
- 檢查 pnpm（有就用、無則 npm）
- 解壓 `shadcn-components.tar.gz` 進 `src/components/ui/`
- 產 `tailwind.config.js`、`tsconfig.json`、`vite.config.ts`、`.parcelrc`

### bundle-artifact.sh 做了什麼

- 安裝 `parcel`、`@parcel/config-default`、`parcel-resolver-tspaths`、`html-inline`
- 產 `.parcelrc`（含路徑別名解析）
- Parcel build（不出 source map）
- `html-inline` 把所有 `<script>` 與 `<link>` inline 進 HTML
- 輸出 `bundle.html`

## 精華 Script 與可提取資源

### 🌟 `scripts/init-artifact.sh`

`Vite + React + TS + Tailwind + shadcn` 一鍵 scaffold。對任何快速啟動 React 專案的場景都有用，不限於 Claude artifact。

關鍵亮點：
```bash
# Node 版本偵測 + Vite 版本 pinning
NODE_MAJOR=$(node -v | cut -d. -f1 | sed 's/v//')
if [ "$NODE_MAJOR" -lt 20 ]; then
  VITE_VERSION="^5"      # Node 18 用 Vite 5
else
  VITE_VERSION="^6"      # Node 20+ 用 Vite 6
fi
```

### 🌟 `scripts/bundle-artifact.sh`

把 SPA 打成「自帶所有依賴的單檔 HTML」。**對任何「要把 web app 用 email/Slack 分享」的情境都極有用**。

### 🌟 `shadcn-components.tar.gz`

預裝 40+ shadcn/ui 元件 + Radix UI deps。免去 `shadcn-ui add ...` 一個個跑。

> 📍 **解壓出來放自家專案**，立即得到完整 shadcn 元件庫。

## 可移植到自家專案的模式

1. **`init-artifact.sh` 改造**：把 init script 套用到自家 boilerplate（公司內部專案、template repo）。

2. **單檔 HTML 分享思路**：bundle-artifact.sh 的「Parcel + html-inline」組合可解決「不部署也能分享」的需求——做 demo、教學、portfolio。

3. **Node 版本偵測 + 版本 pinning**：Bash script 範例可抄。

4. **預裝元件 tarball**：當你有一組常用 dependency，包成 tarball + script 解壓比 npm install 快上百倍。

## 常見陷阱（Gotchas）

- ❌ 簡單 artifact 也用此流程 → 過度工程；✅ 簡單的就直接 inline HTML
- ❌ Bundle 後沒測 → bundle.html 可能含 dev-only 路徑；✅ 自己開瀏覽器看
- ❌ 用 Inter / 紫漸層 / 圓角 16px → AI slop；✅ 看下面[frontend-design](./frontend-design.md)避雷
- ❌ 把 bundle.html 直接 commit → 檔案太大；✅ gitignore，只 commit src

## 延伸閱讀

- 官方檔：[`skills/web-artifacts-builder/SKILL.md`](../../skills/web-artifacts-builder/SKILL.md)
- init 腳本：[`skills/web-artifacts-builder/scripts/init-artifact.sh`](../../skills/web-artifacts-builder/scripts/init-artifact.sh)
- bundle 腳本：[`skills/web-artifacts-builder/scripts/bundle-artifact.sh`](../../skills/web-artifacts-builder/scripts/bundle-artifact.sh)
- 配對閱讀：[frontend-design](./frontend-design.md)（避免 AI slop 美學）
- shadcn/ui 文件：<https://ui.shadcn.com/docs/components>
