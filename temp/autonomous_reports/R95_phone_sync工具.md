# R95 | ADB手机文件同步CLI工具

日期: 2026-03-26
类型: 产出
验收: PASS

## 产出
- 文件: temp/phone_sync.py（174行）
- 文档: temp/phone_sync_README.md
- 基于: memory/adb_ui.py（adb封装经验）

## 功能
- list: 列出手机指定目录文件，支持--ext过滤
- pull: 批量从手机pull文件到本地目录
- push: 批量从本地push文件到手机目录
- --dry预览模式，--device多设备支持
- 自动检测adb可用性和设备连接状态

## 验收
- phone_sync.py语法检查: PASS
- 三操作CLI结构完整: PASS
- README已写: PASS
- git已commit: PASS
