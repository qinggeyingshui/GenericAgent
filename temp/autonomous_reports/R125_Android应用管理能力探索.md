# R125 - Android应用管理能力探索

## 任务来源
TODO#8: 探索Android UI控制的应用安装能力 (评分0.52)

## 探索内容

### 1. 现有能力分析
- **adb_ui.py**: UI dump+解析、tap点击、弹窗检测
- **phone_sync.py**: 文件同步
- **现状**: 缺少应用安装、性能监控、日志抓取功能

### 2. 实现成果

创建 `android_app_manager.py` Android应用管理器：

**核心功能**:
```python
class AndroidAppManager:
    install_app(apk_path, replace=False)
    uninstall_app(package_name, keep_data=False)
    list_apps(filter_type="all")
    get_app_info(package_name)
    start_app(package_name, activity=None)
    stop_app(package_name)
    monitor_performance(package_name=None)
    capture_logs(package_name=None, lines=100)
```

**应用安装**:
- adb install 命令
- 支持替换安装 (-r)
- 支持降级安装 (-d)

**应用管理**:
- pm list packages (系统/第三方/启用/禁用)
- dumpsys package 获取详细信息
- am start/force-stop 启动停止

**性能监控**:
- dumpsys cpuinfo - CPU使用率
- dumpsys meminfo - 内存占用
- dumpsys battery - 电池状态

**日志抓取**:
- logcat -d 抓取日志
- 支持按包名过滤
- 支持清空日志

### 3. 能力边界

**已实现**:
✅ 应用安装/卸载
✅ 应用列表和信息查询
✅ 应用启动/停止
✅ 性能监控 (CPU/内存/电池)
✅ 日志抓取和过滤

**待探索**:
- 应用权限管理 (pm grant/revoke)
- 应用数据备份/恢复
- 应用性能分析 (systrace)
- 实时性能监控 (持续采样)

### 4. 最佳实践

1. **安装前检查**: 先检查设备连接和存储空间
2. **性能监控**: 定期采样，避免频繁调用
3. **日志过滤**: 指定包名减少日志量
4. **错误处理**: 检查adb命令返回值

## 技能树更新

```
[skill_added] mobile_control.app_management.应用安装
[skill_added] mobile_control.app_management.应用卸载
[skill_added] mobile_control.app_management.应用列表
[skill_added] mobile_control.performance_monitoring.CPU监控
[skill_added] mobile_control.performance_monitoring.内存监控
[skill_added] mobile_control.performance_monitoring.电池监控
[skill_added] mobile_control.log_capture.日志抓取
[gaps_remaining] mobile_control.app_management.权限管理, 数据备份
[ability_upgraded] mobile_control.app_management -> intermediate
[evidence] 实现完整应用管理器，覆盖安装/监控/日志功能
```
