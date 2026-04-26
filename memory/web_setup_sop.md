# Web 工具链初始化执行 SOP

若 web_scan 和 web_execute_js 已测试可用，无需执行此 SOP。
仅供初始安装时，code_run 可用但 web 工具尚未配置的场景。

## 目标
在仅具备系统级权限（code_run）时，建立 Web 交互能力（web_scan / web_execute_js）。

## 前置：检测浏览器

## 安装 tmwd_cdp_bridge 扩展
扩展路径: `../assets/tmwd_cdp_bridge/`（MV3 Chrome 扩展，含 CDP debugger + scripting + cookie 能力）

### 自动打开扩展管理页
`chrome://extensions` 无法通过命令行或 JS 打开，需用剪贴板+地址栏方案

### 安装步骤（chrome扩展页难以自动化）
1. 打开扩展管理页，开启「开发者模式」
2. 点击「加载已解压的扩展程序」，选择 `assets/tmwd_cdp_bridge/` 目录，或让用户直接拖入
3. 显示“错误”不用管，一般只是因为还没连上GA

## 阶段 1.6：配置 Tampermonkey CSP 设置
**目的**：移除网站 CSP 头，使 web_execute_js 能在所有页面正常注入执行。
**路径**：TM 管理面板 → 设置 → 配置模式选「高级」→ 修改内容安全策略（CSP）头信息 → 选「全部移除」→ **点保存按钮**
- ⚠️ 高级设置不会自动保存，必须手动点页面底部的「保存」按钮，否则配置不生效

## 阶段二：安装 ljq_web_driver.user.js
**脚本路径**: `../assets/ljq_web_driver.user.js`

### 方案A（自动化，优先）
本地 HTTP 服务器 + TM 中间页，用 `start` 命令打开：
1. Python 启动 `http.server` 托管脚本（Content-Type: text/javascript）
   - ⚠️ 必须用 `Popen(..., stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)` 丢弃输出
   - ❌ 禁用 `stdout=PIPE` 或 `stderr=PIPE`，会导致缓冲区满后服务器阻塞返回空响应
   - Windows 可加 `creationflags=subprocess.CREATE_NO_WINDOW` 避免弹窗
2. `start "" "https://www.tampermonkey.net/script_installation.php#url=http://127.0.0.1:{port}/ljq_web_driver.user.js"`
   - ⚠️ 以上步骤均须用 `Popen` 非阻塞执行，禁止 `subprocess.run`（会等待进程结束）
   - 服务器需持续运行直到用户完成安装，用 `Popen` 启动后立即返回继续执行
3. TM 秒弹安装确认，用户点"安装"即可

### 方案B（手动 fallback）
若方案A失败，用剪贴板：
1. 读取脚本内容 → `pyperclip.copy()`
2. 通知用户在 TM 中【新建脚本 → 全选 → 粘贴 → 保存】

## 阶段三：验证
调用 `web_scan` 或注入 JS 心跳检测，确认脚本已生效。

## 避坑 (Chromium untrusted 拦截)
- ❌ 直接导航到 `localhost/.user.js` → Chromium 弹 untrusted 拦截 + "另存为"，延迟约1分钟
- ✅ 必须用 `start` 命令（系统级）打开 TM 中间页 URL → 秒弹安装，无拦截
- 此问题 Chrome 和 Edge 均存在（Chromium 内核通病）

---
web_automation.browser_control
