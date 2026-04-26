# R41 — PATH 异常自动修复脚本

**日期**: 2026-03-25
**类型**: 产出
**编号**: R41

## 摘要

编写 `path_cleaner.py`，实时扫描系统/用户 PATH 环境变量，识别不存在路径和重复条目，生成分析报告及 PowerShell 修复脚本（不自动写注册表，需用户手动审阅执行）。

## 产出

- **主脚本**: `./path_cleaner.py`
- **分析报告**: `./path_report.txt`（含 66 条目详细分析）
- **修复脚本**: `./fix_path.ps1`（需管理员权限执行）

## 扫描结果

| 指标 | 数值 |
|------|------|
| PATH 总条目 | **66 条** |
| 发现异常 | **22 条** |
| 不存在路径 | 16 条 |
| 重复条目 | 6 条 |
| 正常条目 | 44 条 |

**验收**: 识别 ≥5 条异常 ✔（22条）、生成修复脚本 ✔

## 主要异常摘要

### 不存在路径（16条）

| 范围 | 路径 | 原因推测 |
|------|------|---------|
| SYSTEM | `C:\P` + `ogram Files\MATLAB\R2023a\bin` | 分号截断导致路径碎片 |
| SYSTEM | `node_global` | 相对路径，无效 |
| SYSTEM | `D:\微信web开发者工具\dll` | 微信开发工具已卸载 |
| SYSTEM | `C:\Pro` + `ram Files (x86)\...` | 同上，截断碎片 |
| SYSTEM | `VS2022 MSVC 14.40` bin 路径 | VS 版本已更新 |
| SYSTEM | `E:\Tesseract-OCR` | Tesseract 未安装/已移除 |
| USER | `Python37` × 2 | Python 3.7 已卸载 |
| USER | `.cargo\bin` | Rust 工具链已卸载 |
| USER | `Python37-32` × 2 | 同上 |
| USER | QQGameTempest Hall 路径 | 游戏已卸载 |
| USER | IDEA 2024.3.4 bin 路径 | IDEA 移动或卸载 |
| USER | `.dotnet\tools` | .NET 工具链缺失 |

### 重复条目（6条）

- `%NVM_HOME%` 在 SYSTEM 和 USER 各出现一次（已有 `E:\nvm` 实体条目）
- `%NVM_SYMLINK%` 在 SYSTEM 和 USER 各出现一次
- `%USERPROFILE%\AppData\Local\Microsoft\WindowsApps` 与实体路径重复
- `E:\Nmap` 在 SYSTEM 和 USER 各出现一次

## 安全策略

- `fix_path.ps1` **不自动执行**，需用户以管理员权限手动运行
- 执行前自动备份当前 PATH 到 `%TEMP%\PATH_*_BACKUP_*.txt`
- 修复后需重启终端验证

## 特别注意

MATLAB 路径因分号截断变为碎片（`C:\P` + `ogram Files\MATLAB\...`），修复后如需 MATLAB 可手动重新添加完整路径。