# R04｜浏览器链路修复与 GNN 检索边界小结（自主行动）

日期：2026-03-24  
模式：自主行动（autonomous_operation_sop）

## 1. 任务目标

在不改动系统级环境（仅使用项目下 uv 环境）的前提下：

1. 修复 TMWebDriver 相关依赖，使 `web_scan` / `web_execute_js` 能正常控制用户 Chrome + Tampermonkey。
2. 基于修复后的链路，在学术站点上做一次 “GNN 相关论文检索” 的最小自动化示范。
3. 识别外部站点的反自动化边界，并为后续 GNN 论文长期跟踪提供经验。

## 2. 环境与依赖修复

- 约束：
  - 必须使用项目内 uv 管理的环境；
  - 禁止动 C 盘或使用系统 Python 全局安装；
  - 依赖安装方式限定为 `uv pip` / `uv run`。

- 关键操作：
  1. 在项目根执行：
     - `uv pip install simple_websocket_server`
     - `uv pip install beautifulsoup4`
  2. 在 `E:/2026/x-fudan/new/GenericAgent` 下验证：
     - `import TMWebDriver` 成功（之前缺 `simple_websocket_server`、`bs4` 现已解决）。
  3. 在 `./temp` 下，由于 cwd 变化导致找不到 TMWebDriver：
     - 在脚本中显式 `sys.path.append('E:/2026/x-fudan/new/GenericAgent')`；
     - 然后 `from TMWebDriver import TMWebDriver; TMWebDriver()` 成功启动后台服务。

- 结果：
  - TMWebDriver 后台（基于 `simple_websocket_server`）已可在当前 uv/venv 环境正常运行。
  - Chrome + Tampermonkey + TMWebDriver 的物理链路打通。

## 3. 浏览器链路验证

- 使用 `web_scan`：
  - 初始只看到 `https://www.baidu.com/`，说明连接成功但尚无其他标签页。
- 在 `temp` 环境中启动 TMWebDriver 后台后再次 `web_scan`：
  - 成功识别当前 Chrome 标签页，并抓取百度首页主体文本。
- 证明：
  - Python → TMWebDriver → Tampermonkey → Chrome 整条控制链路已恢复可用，可用来驱动后续的学术站点访问与页面采集。

## 4. GNN 论文检索最小示范 & 外部边界

### 4.1 自动导航与检索动作

1. 从百度页，通过 `web_execute_js` 执行：
   - `window.location.href = 'https://scholar.google.com/';`
   - 成功跳转到 Google Scholar 首页。
2. 在 Scholar 首页通过 JS 自动填写并提交检索表单：
   - 找到 `input[name="q"]`，填入关键词：
     - `graph neural networks survey 2024`
   - 通过 `form.submit()` 提交搜索。
   - 返回状态 `SUBMITTED`，说明前端动作已执行。

### 4.2 触发反自动化（reCAPTCHA）

- 搜索提交后，使用 `web_scan` 抓取页面内容，发现已跳转至 Google 的 “人机身份验证” 页面：
  - URL 类似 `https://www.google.com/sorry/index?...continue=https://scholar.google.com/scholar?...`
  - 页面主体为 reCAPTCHA 说明：
    - 系统检测到来自当前网络的异常流量；
    - 要求完成人机验证以继续访问。
- 这是 Google Scholar 一侧的明确风控边界：
  - 我不会、也不能尝试绕过或自动破解 reCAPTCHA。
  - 在当前网络/访问模式下，继续对 Scholar 执行自动化访问风险较大，收益有限。

## 5. 对后续 GNN 论文长期跟踪的启示

1. **基础设施层面**
   - 依赖（`simple_websocket_server`, `beautifulsoup4`）已通过 uv 环境正确安装；
   - TMWebDriver + Chrome + Tampermonkey 链路已成功验证；
   - 之后可以稳定使用 `web_scan` / `web_execute_js` 驱动浏览器做各种学术站点操作。

2. **站点选择与访问策略**
   - Google Scholar：
     - 能被自动导航与提交搜索，但稍复杂的检索就触发了 reCAPTCHA。
     - 建议：
       - 将 Scholar 主要用于 **低频、人机协作式查询**（由你来点选验证码和浏览结果，我只做轻量辅助，如解析当前页）。
       - 避免高频自动抓取，以免加重风控。
   - 推荐作为自动化主力的数据源：
     - **arXiv**（特别是 cs.LG, cs.LG + stat.ML, cs.AI 下的 graph / GNN 相关）；
     - **OpenReview**（例如 ICLR / NeurIPS / ICML / ICLR workshops 中的 GNN、graph learning track）；
     - **DBLP / Semantic Scholar** 等较少主动触发强验证码的站点。
   - 后续可以在这些站点上为你定制：
     - 关键词/主题过滤（Graph neural networks, graph foundation models, geometric deep learning, topological deep learning 等）；
     - 年份过滤（例如 2023–2026）；
     - 周期性更新逻辑（每日/每周扫描新条目）。

3. **总体评价**
   - 本轮任务达成了预期的“最小可行示范”：
     - 修好浏览器自动化基础设施；
     - 在真实学术站点上验证了自动检索动作；
     - 识别并尊重了 Google Scholar 的反自动化边界。
   - 后续长程任务应重点围绕：
     - 在 arXiv / OpenReview 等更友好的站点上构建稳定的 GNN 论文收集与更新流程；
     - 在你在线时，再结合 Scholar 做人工辅助的交叉验证和 citation 追踪。

## 6. 建议的下一步（供后续轮次或你在线时参考）

1. 在你在线时：
   - 共同选择首批 arXiv 搜索式（如 “\"graph neural network\" OR \"GNN\" foundation model” + 时间过滤）；
   - 决定优先级最高的两个子方向：
     - 表征学习 & Graph Foundation Models；
     - 图上的几何/拓扑深度学习。
2. 在后续自主轮次：
   - 绕开 Scholar，优先在 arXiv / OpenReview 上实现：
     - 自动访问 / 搜索；
     - 抓取标题、作者、年份、链接、简短摘要；
     - 存成本地 markdown/JSON 以便你阅读。
3. 保留当前 TMWebDriver 启动方式的脚本片段，用于后续复用：
   - 在 `temp` 环境下启动时记得：
     - `sys.path.append('E:/2026/x-fudan/new/GenericAgent')`
     - `from TMWebDriver import TMWebDriver; TMWebDriver()`