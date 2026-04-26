# R72 | Canva Connect API 能力评估

## 任务
探测 Canva Connect API，评估 OAuth 流程和可用 API 端点，输出 canva_api_guide.md。

## 核心发现

1. **OAuth 2.0 + PKCE 流程完整可实现**：Authorization Code Flow，Python 标准库（secrets/hashlib）即可生成 PKCE 参数，无需第三方依赖。
2. **Designs API**（无 Enterprise 要求）：可创建 Presentation 类型设计、列出/获取设计元数据（5个端点）。
3. **Exports API**（无 Enterprise 要求）：异步 job 模式，支持导出 PPTX/PDF/PNG/GIF/MP4；**仅 Canva Presentations 类型设计可导出 PPTX**。
4. **Assets API**：可上传图片资产供设计使用。
5. **Brand Templates / Autofill**：需 Enterprise 订阅，当前不可用。

## 接入前置条件
- 需在 canva.dev Developer Portal 注册账号并创建 integration
- 获取 client_id + client_secret
- 首次授权需用户在线点击（无法完全无人值守）

## 产出
- `./autonomous_reports/canva_api_guide.md`：112行/3287字节，含OAuth流程+PKCE Python示例+4个API端点说明+完整接入方案

## 可行性结论
技术上完全可行；障碍在于需要用户注册 Developer Portal 并提供 client_id。建议用户访问 canva.dev 注册后提供凭证，Agent 即可实现完整自动化 PPT 生成+导出。

## 记忆更新建议
- global_mem_insight: Canva Connect API条目补充"需client_id/OAuth/Presentations→PPTX导出/canva_api_guide.md"