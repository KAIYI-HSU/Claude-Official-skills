# webapp-testing — Playwright 自動化測試

## 一句話定位

用 Playwright 測試本地 web app（靜態 HTML 或動態 server-rendered），核心提供 `with_server.py` 多伺服器生命週期管理 + reconnaissance-then-action 互動模式。

## 何時觸發

- 驗證前端功能、debug UI 行為
- 截圖、看 browser console log
- 對 localhost web app 做自動化操作

## 目錄結構速覽

```
skills/webapp-testing/
├── SKILL.md                       # 決策樹 + pattern
├── scripts/
│   └── with_server.py             # 🌟 多 server 生命週期管理
└── examples/
    ├── static_html_automation.py  # file:// URL 模式
    ├── element_discovery.py       # 元素搜尋策略
    └── console_logging.py         # 抓 browser log
```

## 核心觀念與工作流

### 決策樹

```
是否為靜態 HTML？
├─ 是 → 直接讀 HTML 找 selector → 寫 Playwright script
│
└─ 否（動態 webapp） → server 已啟動？
    ├─ 否 → 用 with_server.py
    └─ 是 → reconnaissance-then-action：
        1. goto + 等 networkidle
        2. 截圖 / 看 DOM
        3. 從渲染後的 DOM 找 selector
        4. 執行操作
```

### Reconnaissance-then-Action（核心模式）

```python
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)        # 一律 headless
    page = browser.new_page()
    page.goto('http://localhost:5173')
    page.wait_for_load_state('networkidle')           # ← 重要！

    # 偵察階段
    page.screenshot(path='/tmp/inspect.png', full_page=True)
    print(page.content()[:2000])
    buttons = page.locator('button').all()

    # 行動階段（已知 selector 後才下手）
    page.locator('text=Submit').click()
    browser.close()
```

### with_server.py 用法

**單 server**：
```bash
python scripts/with_server.py \
  --server "npm run dev" --port 5173 \
  -- python my_test.py
```

**多 server**（前後端同時跑）：
```bash
python scripts/with_server.py \
  --server "cd backend && python server.py" --port 3000 \
  --server "cd frontend && npm run dev" --port 5173 \
  -- python my_test.py
```

腳本邏輯：
1. 平行啟動所有 server
2. 輪詢 port 直到 ready（30s timeout）
3. 跑 `--` 之後的命令
4. 結束時清理所有 server process

## 精華 Script 與可提取資源

### 🌟 `scripts/with_server.py`（極具重用價值）

**這支 ~50 行的腳本能套用到任何「測試需要 server 先跑起來」的情境**——CI 整合、E2E 測試、資料庫＋API＋前端三層啟動。

直接複製即可，無依賴。

### 📋 黑盒呼叫原則

> **Always run scripts with `--help` first. DO NOT read the source until you try running the script first.**

這是 Anthropic 官方的設計哲學：scripts 是黑盒 CLI 工具，不是要被讀進 context 的程式碼。看 `--help`、用、不要讀源碼。

### 📋 元素定位策略（從 `element_discovery.py`）

```python
page.locator('text=Submit')           # 文字
page.locator('role=button[name="OK"]') # ARIA role
page.locator('.btn-primary')           # CSS class
page.locator('#submit-btn')            # ID
page.locator('xpath=//button[1]')      # XPath（最後手段）
```

優先順序：text > role > css > xpath。

## 可移植到自家專案的模式

1. **`with_server.py` 直接抄**：CI 跑 E2E、本地 dev 多服務啟動，都能用。

2. **Reconnaissance-then-Action 心法**：任何不確定的環境（陌生 API、未知 DOM、新平台），先「看清楚」再「動手」。

3. **`networkidle` 等待**：很多 SPA 一上 load 就 fire 還沒就緒；wait for networkidle 是最簡單的等就緒方式。

4. **Black-box script 哲學**：自家 CLI 工具寫好 `--help`，不要強迫使用者（或 Claude）讀原始碼。

5. **Headless 預設**：自動化測試永遠 headless，省記憶體並可在 CI 跑。

## 常見陷阱（Gotchas）

- ❌ 沒等 `networkidle` 就 inspect → SPA 還沒掛載 component；✅ 一定要等
- ❌ 寫 `xpath=//div[3]/button[1]` → 改版易壞；✅ 用 text/role
- ❌ 忘記 `browser.close()` → process leak
- ❌ 把 server 啟動寫在 test script 內 → 失敗時清不乾淨；✅ 用 `with_server.py`
- ❌ headless=False 跑 CI → 沒有顯示器，crash
- ❌ 把 with_server.py 整檔讀進 context → 純粹浪費 token；✅ `--help` 即可

## 延伸閱讀

- 官方檔：[`skills/webapp-testing/SKILL.md`](../../skills/webapp-testing/SKILL.md)
- 主要腳本：[`skills/webapp-testing/scripts/with_server.py`](../../skills/webapp-testing/scripts/with_server.py)
- 範例集：[`skills/webapp-testing/examples/`](../../skills/webapp-testing/examples/)
