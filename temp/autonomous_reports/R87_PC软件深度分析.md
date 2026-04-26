# R87 | PC已安装软件深度分析与工具推荐

日期: 2026-03-26
类型: 探测+产出
验收: PASS

## 数据来源
注册表枚举（HKLM+HKCU Uninstall），共357个已安装软件（UTF-8重新导出，旧software_raw.txt编码损坏）。

## 软件类别统计

| 类别 | 数量 |
|------|------|
| 开发工具 | 68 |
| CAD/工程 | 12 |
| Office/文档 | 11 |
| 浏览器/网络 | 6 |
| 数据处理 | 5 |
| 媒体/创意 | 1 |
| 通信 | 1 |
| 未分类 | 251 |
| **合计** | **357** |

## Agent可利用工具发现（>=5条）

### 1. Docker Desktop（已安装）
**可利用方式**: 可在容器内运行隔离环境，部署本地LLM服务（如Ollama容器）、数据库服务。
**当前利用状态**: 未使用。建议：重型依赖任务可用Docker隔离，避免污染主环境。

### 2. Git（已安装）
**可利用方式**: 版本控制local_skills/、autonomous_reports/；diff追踪自己代码修改历史。
**当前利用状态**: 项目内未见.git初始化。建议：对GenericAgent项目初始化git，便于回滚实验。

### 3. Anaconda3 2024.10-1 / Python 3.12.7（已安装）
**可利用方式**: conda创建隔离虚拟环境安装重型包（如torch、transformers）不影响主venv。
**当前利用状态**: 已在用主venv。建议：GPU/ML任务用conda env，日常脚本用主venv。

### 4. Postman x64 11.81.4（已安装）
**可利用方式**: 手动调试API接口（LLM API、arXiv API、微信API等），辅助排查agent网络请求问题。
**当前利用状态**: 未使用。建议：调试新API端点时先用Postman验证参数格式。

### 5. MySQL Server 8.0 + MySQL Installer（已安装）
**可利用方式**: 本地关系数据库，可替代JSON文件存储论文库/教案库，支持复杂查询。
**当前利用状态**: 未使用（当前用PAPERS.md平铺存储）。建议：论文库扩充至50+条后迁移MySQL。

### 6. IBM SPSS Statistics 27（已安装）
**可利用方式**: 统计分析软件，用户可能有统计分析需求，agent可辅助生成SPSS语法脚本。
**当前利用状态**: 未使用。建议：研究方向相关的统计分析任务可调用SPSS命令行接口。

### 7. Wireshark 4.4.5（已安装）
**可利用方式**: 网络抓包，辅助排查浏览器自动化的网络请求失败问题（配合tmwebdriver_sop）。
**当前利用状态**: 未使用。备用调试工具。

### 8. Microsoft Office 2021（已安装，含PowerPoint/Word）
**可利用方式**: win32com直接操控，已有ppt_com_toolkit.py。Word同样可用python-docx或win32com操作。
**当前利用状态**: PPT已集成，**Word尚未封装**。建议：封装word_toolkit.py（用户已询问过Word格式调整）。

### 9. AutoCAD 2021（已安装）
**可利用方式**: 通过AutoCAD脚本语言(.scr)或COM接口批量操作图纸。
**当前利用状态**: 未使用。若用户有建筑/工程图纸需求可支持。

### 10. Audacity 3.6.3（已安装）
**可利用方式**: 命令行调用Audacity处理音频（降噪/格式转换），配合课程录音处理。
**当前利用状态**: 未使用。

## 优先行动建议

| 优先级 | 工具 | 建议行动 |
|--------|------|----------|
| 高 | Word/Office 2021 | 封装word_toolkit.py（用户已有需求） |
| 高 | Git | 对GenericAgent项目git init，建立版本控制 |
| 中 | MySQL 8.0 | 论文库/教案库扩大后迁移数据库存储 |
| 中 | Anaconda3 | GPU/ML任务用conda隔离环境 |
| 低 | Docker | 重型服务部署备用 |

## 记忆更新建议
建议在global_mem_insight.txt补充:
- Word操控: word_toolkit.py(待建，win32com，用户已询问Word格式调整)
- 本地数据库: MySQL 8.0已安装，可替代JSON文件库
- Git: 项目未初始化，建议git init
