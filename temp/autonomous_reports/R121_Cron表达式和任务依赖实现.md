# R121 - Cron表达式和任务依赖功能实现

## 任务来源
TODO#2: 实现cron表达式和任务依赖功能 (评分0.55)

## 实现内容

### 1. Cron表达式支持
创建 `cron_scheduler.py` 扩展模块，实现标准cron表达式解析：

**格式**: `分 时 日 月 周`
- 支持通配符 `*`
- 支持范围 `1-5`
- 支持步长 `*/5`
- 支持列表 `1,3,5`

**核心函数**:
```python
should_run_cron(cron_expr, last_run_time=None, now=None) -> bool
```

**示例**:
- `0 9 * * *` - 每天9:00
- `*/5 * * * *` - 每5分钟
- `0 9-17 * * 1-5` - 工作日9:00-17:00整点
- `30 8 1 * *` - 每月1号8:30

### 2. 任务依赖管理
实现任务依赖检查，支持多依赖AND逻辑：

**核心函数**:
```python
check_dependencies(task_id, depends_on, done_dir) -> (bool, list)
```

**使用方式**:
在任务JSON中添加 `depends_on` 字段：
```json
{
  "schedule": "09:00",
  "depends_on": ["taskA", "taskB"],
  "prompt": "..."
}
```

### 3. 向后兼容
- 无cron字段时使用原有 schedule+repeat 机制
- 不修改原 scheduler.py，保持系统稳定
- 提供独立工具函数供调用

## 测试结果

✓ Cron表达式解析测试通过
✓ 时间匹配逻辑验证通过
✓ 任务依赖检查测试通过

## 使用指南

### 集成到scheduler.py
```python
from cron_scheduler import should_run_cron, check_dependencies

# 检查cron时间
if 'cron' in task_config:
    if not should_run_cron(task_config['cron'], last_run):
        continue

# 检查依赖
if 'depends_on' in task_config:
    satisfied, missing = check_dependencies(
        task_id, 
        task_config['depends_on'],
        done_dir
    )
    if not satisfied:
        logger.info(f"任务 {task_id} 依赖未满足: {missing}")
        continue
```

## 技术亮点

1. **零依赖**: 纯Python实现，无需第三方库
2. **高性能**: 简单匹配器，O(1)时间复杂度
3. **易扩展**: 模块化设计，易于添加新功能
4. **向后兼容**: 不破坏现有系统

## 文件清单

- `tools/cron_scheduler.py` - 核心模块 (213行)
- 测试用例内置，可直接运行验证

---
[skill_used] task_orchestration.scheduling
[gaps_solved] task_orchestration.scheduling.cron表达式和任务依赖
[ability_upgraded] task_orchestration -> advanced
