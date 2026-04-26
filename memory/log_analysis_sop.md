# log_analysis_sop.md - Log Analysis SOP (R174, 2026-04-20)

Tool: tools/log_analyzer.py | Log analysis & visualization

## Core Functions

```python
from log_analyzer import LogAnalyzer, analyze_log

# Create analyzer
analyzer = LogAnalyzer()

# Parse log file
count = analyzer.parse_log_file('app.log')

# Get error statistics
stats = analyzer.get_error_stats()
# Returns: {'ERROR': 10, 'WARNING': 5, 'INFO': 100}

# Get error messages
errors = analyzer.get_error_messages(limit=10)

# Get hourly statistics
hourly = analyzer.get_hourly_stats()

# Detect common patterns
patterns = analyzer.detect_patterns()

# Generate report
report = analyzer.generate_report()

# Export to JSON
analyzer.export_json('report.json')

# Get visualization data
viz_data = analyzer.get_visualization_data()
# Returns: {pie_chart: {labels, values}, line_chart: {hours, errors}}

# Quick analysis
report = analyze_log('app.log')
```

## Use Cases

1. **Log Parsing**: Parse multiple log formats
2. **Error Analysis**: Statistics and pattern detection
3. **Trend Visualization**: Hourly/daily trends
4. **Troubleshooting**: Identify common errors

## Supported Patterns

- ERROR/Error/error
- WARNING/Warning/warning
- INFO/Info/info
- Timestamp: YYYY-MM-DD HH:MM:SS

## Notes

- Auto-detects log levels
- Handles multiple timestamp formats
- Pattern detection for common errors

[skill_mapping]
category: system_monitoring
skill: 日志分析与可视化
tools: log_analyzer.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('log_analysis_sop.md')
```
