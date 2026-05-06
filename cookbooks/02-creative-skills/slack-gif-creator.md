# slack-gif-creator — Slack 動畫 GIF 神器

## 一句話定位

製作符合 Slack 規格（emoji 128×128、訊息 480×480、< 3s）的動畫 GIF，內附 production-ready 的 `GIFBuilder` 類別、9+ 緩動函式、8 種動畫概念樣板——本 cookbook 中**最直接可拷貝重用**的 skill。

## 何時觸發

- "make me a GIF for Slack"、"animated GIF"、"emoji GIF"
- 製作部門內 emoji、慶祝動畫、提醒動畫

## 目錄結構速覽

```
skills/slack-gif-creator/
├── SKILL.md                 # 主指引（規格 + 動畫概念）
├── requirements.txt         # pillow, imageio, numpy
└── core/
    ├── gif_builder.py       # 🌟 GIFBuilder 主類別
    ├── validators.py        # Slack 規格驗證
    ├── easing.py            # 🌟 14 種緩動函式（極具重用價值）
    └── frame_composer.py    # 圖元繪製便利函式
```

## 核心觀念與工作流

### Slack 規格

| 類型 | 尺寸 | FPS | 顏色數 | 時長 |
|------|------|-----|--------|------|
| Emoji | 128×128 | 10–30 | 48–128 | < 3s |
| 訊息 | 480×480 | 10–30 | 48–128 | < 3s |

### 基本使用

```python
from core.gif_builder import GIFBuilder
from core.frame_composer import create_blank_frame, draw_circle

builder = GIFBuilder(size=(128, 128), fps=20)
for i in range(20):
    frame = create_blank_frame(128, 128, "white")
    draw_circle(frame, x=64, y=64, radius=10 + i, color="red")
    builder.add_frame(frame)
builder.save("my.gif")
```

### 8 種動畫概念（從 SKILL.md）

| 動畫 | 核心數學 |
|------|----------|
| **Shake／Vibrate** | `x += sin(t) * amplitude`、`y += cos(t) * amplitude` |
| **Pulse／Heartbeat** | `scale = 1 + sin(t) * 0.2`（0.8–1.2 間） |
| **Bounce** | `interpolate(0, h, t, "bounce_out")` |
| **Spin／Rotate** | `image.rotate(angle)` 或 sin 波擺動 |
| **Fade In/Out** | RGBA alpha 通道 |
| **Slide** | `interpolate` + ease_out 從畫布外滑入 |
| **Zoom** | `image.resize(scale)` + 中心裁切 |
| **Particle Burst** | 多粒子放射 + 重力 + alpha 衰減 |

## 精華 Script 與可提取資源

### 🌟 `core/easing.py`（強烈推薦複製到任何動畫專案）

提供 14 種緩動函式 + 高階組合函式：

```python
from core.easing import interpolate, calculate_arc_motion, apply_squash_stretch

# 1) 兩值內插 + 緩動（最常用）
y = interpolate(start=10, end=90, t=0.5, easing="bounce_out")

# 2) 拋物線軌跡（自然投擲動作）
x, y = calculate_arc_motion(start=(0, 100), end=(100, 100), height=50, t=0.5)

# 3) 擠壓拉伸（卡通動畫感）
sx, sy = apply_squash_stretch(base_scale=(1.0, 1.0), intensity=0.4, direction="vertical")
```

完整名單：
```
linear, ease_in_quad, ease_out_quad, ease_in_out_quad,
ease_in_cubic, ease_out_cubic, ease_in_out_cubic,
ease_in_bounce, ease_out_bounce, ease_in_out_bounce,
ease_in_elastic, ease_out_elastic, ease_in_out_elastic,
ease_back_in, ease_back_out, ease_back_in_out
```

> 📍 **直接複製整個 `easing.py` 進你的專案**——無依賴、純 math，對任何動畫場景（CSS-in-JS、p5.js、PIL）都有用。

### 🌟 `core/gif_builder.py`

GIF 組裝核心：
- 自動 frame resize
- 自動色彩量化（quantize to global palette）
- DuplicateFrame 偵測（壓縮）
- Slack-mode 自動最佳化

### 🌟 `core/frame_composer.py`

PIL 之上的便利層：
```python
create_blank_frame(w, h, color)
create_gradient_background(w, h, top_color, bottom_color)
draw_circle(frame, x, y, radius, color, thickness=2)
draw_star(frame, cx, cy, points, outer_r, inner_r, color)
draw_text(frame, text, position, font, color)
```

### 🌟 `core/validators.py`

GIF 出檔前確認 Slack 合規：
- 尺寸正確
- FPS 在 10–30
- 顏色數 ≤ 128
- 檔案 < 64KB（emoji 限制）
- 時長 < 3s

## 可移植到自家專案的模式

1. **`easing.py` 複製**：任何動畫專案的核心。

2. **GIFBuilder pattern**：把「frame 累積 → 一次輸出」邏輯封裝起來，比逐張存檔再合成乾淨：
   ```python
   builder = GIFBuilder(...)
   for t in timeline:
       builder.add_frame(render(t))
   builder.save("out.gif")
   ```

3. **Validator 前置檢查**：任何「會被外部規格約束」的輸出（icon、上傳檔案、社群圖），都該寫驗證器。

4. **`interpolate` 統一介面**：`interpolate(start, end, t, easing)`——一個函式涵蓋所有 lerp 場景。

5. **少色彩、多細節**：GIF 為了壓縮會限制色數，但仍能用：漸層、層次形狀、高光、邊框環、發光圓暈，做出「有質感的低色」效果。

## 常見陷阱（Gotchas）

- ❌ 直接存 RGB 8-bit GIF → 大小爆炸；✅ `quantize` 到 48–128 色 + 全域 palette
- ❌ 線寬 1px → 縮放後消失；✅ `width=2+` 為粗線
- ❌ 純 linear 動畫 → 機械感重；✅ 至少用 `ease_out`
- ❌ 黑邊／白邊 frame 混進序列 → 閃爍；✅ 統一 alpha 與背景色
- ❌ FPS 太高 (> 30) → 檔案過大；Slack 通常給你限制；✅ 20 FPS 是甜蜜點

## 延伸閱讀

- 官方檔：[`skills/slack-gif-creator/SKILL.md`](../../skills/slack-gif-creator/SKILL.md)
- 緩動函式（強烈推薦複製）：[`skills/slack-gif-creator/core/easing.py`](../../skills/slack-gif-creator/core/easing.py)
- Builder 類別：[`skills/slack-gif-creator/core/gif_builder.py`](../../skills/slack-gif-creator/core/gif_builder.py)
- 驗證器：[`skills/slack-gif-creator/core/validators.py`](../../skills/slack-gif-creator/core/validators.py)
