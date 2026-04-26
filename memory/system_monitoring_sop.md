# system_monitoring_sop.md - System Monitoring SOP (R172, 2026-04-20)

Tool: tools/system_monitor.py | System resource monitoring & alerting

## Core Functions

```python
from system_monitor import SystemMonitor, monitor_once, get_dashboard

# Basic monitoring
monitor = SystemMonitor()
metrics = monitor.collect_metrics()
# Returns: {timestamp, cpu, memory, disk, alerts?}

# Save history
monitor.save_history(metrics)

# Get history
history = monitor.get_history(limit=100)

# Set thresholds
monitor.set_threshold('cpu', 80)
monitor.set_threshold('memory', 85)
monitor.set_threshold('disk', 90)

# Get alerts
alerts = monitor.get_alerts(limit=50)

# Clear alerts
monitor.clear_alerts()

# Quick monitoring
metrics = monitor_once()

# Dashboard
dashboard = get_dashboard()
# Returns: {current, recent_history, alerts}
```

## Use Cases

1. **Real-time Monitoring**: Collect current system metrics
2. **Threshold Alerting**: Auto-alert when exceeding thresholds
3. **Historical Analysis**: Track resource usage trends
4. **Dashboard**: Get comprehensive system status

## Dependencies

- psutil: System metrics collection

## Notes

- Default thresholds: CPU 80%, Memory 85%, Disk 90%
- History limited to 1000 records
- Alerts stored in memory (cleared on restart)

[skill_mapping]
category: system_monitoring
skill: 系统资源监控与告警
tools: system_monitor.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('system_monitoring_sop.md')
```
