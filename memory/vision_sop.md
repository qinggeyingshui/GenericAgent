# Vision API SOP

## ⚠️ 前置规则（必须遵守）

1. **先枚举窗口**：调用 vision 前必须先用 `pygetwindow` 枚举窗口标题，确认目标窗口存在且已激活到前台。窗口不存在就不要截图。
2. **🚫 禁止全屏截图**：必须先利用ljqCtrl截取窗口区域。能截局部（如标题栏）就不截整窗口，能截窗口就绝不全屏。全屏截图在任何场景下都不允许。
3. **能不用 vision 就不用**：如果窗口标题/本地 OCR（`ocr_utils.py`）能获取所需信息，就不要调用 vision API，省 token 且更可靠。Vision 是最后手段。

## 快速用法

```python
from vision_api import ask_vision
result = ask_vision(image, prompt="描述图片内容", backend="claude", timeout=60, max_pixels=1_440_000)
# image: 文件路径(str/Path) 或 PIL Image
# backend: 'claude'(默认) | 'openai' | 'modelscope'
# 返回 str：成功为模型回复，失败为 'Error: ...'
```

## 如果没有 `vision_api.py`，初次构建vision能力

## 故障排除
| 问题 | 解决方案 |
|------|--------|
| 导入失败 | 可检查 `../../mykey.py` 文件是否存在（仅检查存在性，不读取内容） |
| 超时 | 提高 timeout 或降低 max_pixels |
| 格式错误 | 确保使用 PIL 支持的格式（PNG/JPG/GIF等） |

## 关键风险与坑点 (L3 Caveats)
- **无重试机制**: `vision_api.py` 内部未实现 API 错误重试（如 503、超时）。在自动化流程中使用时，**必须在上层代码手动实现重试逻辑**（建议指数退避），否则偶发网络波动会导致任务直接崩溃中断。
- **API Config**: 当前使用 `claude_config141`(ncode.vkm2.com, 已验证)。备选可用: `native_claude_config2/84/5535`。失效时直接改 `vision_api.py` 中的 `cfg = mk.claude_configXXX`。

---
更新: 2025-07-18 | 修复oai_config导入+返回值统一str
更新: 2026-02-18 | 默认后端改为Claude原生API | SOP精简(删废话/水段/合并示例)
更新: 2026-07 | 修复config(原claude_config8不存在)→改为claude_config141

---
 media_processing.image
