# Canva Connect API 接入指南
> 基于官方文档 canva.dev/docs/connect | 评估时间: 2026-03-26

## 一、总体评估

Canva Connect API 是 REST API，支持 OAuth 2.0 授权，可程序化创建/管理设计、导出为 PPTX 等格式。
**关键约束**: 需在 Canva Developer Portal 注册 integration，获取 client_id + client_secret。
**Enterprise 限制**: 部分 API（Brand Templates/Autofill）需要 Enterprise 账号。

## 二、OAuth 2.0 接入流程（Authorization Code + PKCE）

### 步骤概览
1. 在 Developer Portal 创建 integration，配置 scopes 和 redirect_uri
2. 生成 code_verifier（43-128位随机串）和 code_challenge（SHA-256 hash → base64url）
3. 引导用户访问授权 URL，获取 authorization_code
4. 用 authorization_code 换取 access_token + refresh_token
5. 用 access_token 调用 API，token 过期后用 refresh_token 刷新

### 授权 URL 格式
```
https://www.canva.com/api/oauth/authorize
  ?code_challenge=<SHA256(code_verifier) base64url>
  &code_challenge_method=s256
  &scope=<space separated scopes>
  &response_type=code
  &client_id=<client_id>
  &state=<random string>
  &redirect_uri=<registered redirect uri>
```

### Python 示例：生成 PKCE 参数
```python
import secrets, hashlib, base64

code_verifier = secrets.token_urlsafe(96)
digest = hashlib.sha256(code_verifier.encode()).digest()
code_challenge = base64.urlsafe_b64encode(digest).rstrip(b"=").decode()
state = secrets.token_urlsafe(32)
```

### 常用 Scopes
| Scope | 用途 |
|-------|------|
| asset:read | 读取资产 |
| asset:write | 上传资产 |
| design:meta:read | 读取设计元数据 |
| design:content:read | 读取设计内容 |
| design:content:write | 修改设计内容 |
| folder:read | 读取文件夹 |

## 三、核心 API 端点

### API 1: Designs（设计管理）
**文档**: canva.dev/docs/connect/api-reference/designs/

| 接口 | 方法 | 说明 |
|------|------|------|
| POST /v1/designs | POST | 创建新设计（指定类型：presentation/doc等）|
| GET /v1/designs | GET | 列出用户所有设计 |
| GET /v1/designs/{designId} | GET | 获取单个设计元数据 |
| GET /v1/designs/{designId}/pages | GET | 获取设计页面元数据 |
| GET /v1/designs/{designId}/export-formats | GET | 查询可导出格式 |

### API 2: Exports（导出为文件）
**文档**: canva.dev/docs/connect/api-reference/exports/
**关键能力**: 支持导出为 PPTX（PowerPoint格式）

| 接口 | 方法 | 说明 |
|------|------|------|
| POST /v1/exports | POST | 创建异步导出任务（指定 format: pptx/pdf/png等）|
| GET /v1/exports/{exportId} | GET | 轮询导出状态，完成后获取下载链接 |

**支持的导出格式**: pdf / jpg / png / gif / pptx / mp4
**限制**: 仅 Canva Presentations 类型设计可导出为 PPTX

### API 3: Assets（资产管理）
**文档**: canva.dev/docs/connect/api-reference/assets/
可上传图片等资产供设计使用，scope: asset:read + asset:write

### API 4: Brand Templates（品牌模板，需 Enterprise）
可读取企业品牌模板列表，用于 Autofill 自动填充内容。

## 四、PPT 制作场景接入方案

### 场景：程序化生成 Canva 演示文稿并导出 PPTX

```
流程:
1. OAuth 授权 → 获取 access_token
2. POST /v1/designs (type=presentation) → 获取 designId
3. (可选) 上传图片资产: POST /v1/assets
4. POST /v1/exports (designId, format=pptx) → 获取 exportId
5. 轮询 GET /v1/exports/{exportId} 直到 status=success
6. 下载 export.urls[0] 即得 .pptx 文件
```

## 五、接入前置条件与限制

| 条件 | 说明 |
|------|------|
| Developer Portal 账号 | 需注册并创建 integration |
| client_id + client_secret | 从 Developer Portal 获取 |
| redirect_uri | 必须预先在 Portal 注册 |
| 用户在线授权 | 首次需用户点击授权，无法完全无人值守 |
| Enterprise（部分功能）| Brand Templates/Autofill 需 Enterprise 订阅 |
| PPTX 导出 | 仅 Presentation 类型设计可导出为 PPTX |

## 六、可行性评估

- **可行**: OAuth 流程标准，Python 可直接实现；Designs+Exports API 无 Enterprise 要求
- **障碍**: 首次授权需用户交互；需要在 Canva 官网注册 Developer 账号并创建 integration
- **建议下步**: 用户注册 canva.dev Developer Portal → 创建 integration → 提供 client_id 给 Agent 实现完整自动化
