"""
Cron表达式和任务依赖扩展模块
为scheduled_task系统提供高级调度能力

新增功能:
1. Cron表达式支持 (格式: "分 时 日 月 周")
2. 任务依赖管理 (depends_on字段)

使用方法:
  from cron_scheduler import should_run_cron, check_dependencies
  
  # 检查cron时间
  if should_run_cron(cron_expr, last_run_time):
      ...
  
  # 检查依赖
  if check_dependencies(task_id, depends_on_list, done_dir):
      ...
"""

from datetime import datetime, timedelta
import os

def parse_cron(cron_expr):
    """
    解析cron表达式 (简化版，不依赖外部库)
    格式: "分 时 日 月 周"
    支持: 数字, *, */N, 逗号分隔
    
    返回: (minute, hour, day, month, weekday) 的匹配函数
    """
    parts = cron_expr.strip().split()
    if len(parts) != 5:
        raise ValueError(f"Invalid cron format: {cron_expr}, expected 5 fields")
    
    def make_matcher(field, min_val, max_val):
        """创建字段匹配函数"""
        if field == "*":
            return lambda x: True
        if field.startswith("*/"):
            step = int(field[2:])
            return lambda x: x % step == 0
        if "," in field:
            values = [int(v) for v in field.split(",")]
            return lambda x: x in values
        if "-" in field:
            start, end = map(int, field.split("-"))
            return lambda x: start <= x <= end
        # 单个数字
        val = int(field)
        return lambda x: x == val
    
    matchers = [
        make_matcher(parts[0], 0, 59),   # minute
        make_matcher(parts[1], 0, 23),   # hour
        make_matcher(parts[2], 1, 31),   # day
        make_matcher(parts[3], 1, 12),   # month
        make_matcher(parts[4], 0, 6),    # weekday (0=周日)
    ]
    return matchers

def should_run_cron(cron_expr, last_run_time=None, now=None):
    """
    检查cron表达式是否应该触发
    
    Args:
        cron_expr: cron表达式字符串
        last_run_time: 上次执行时间 (datetime对象)
        now: 当前时间 (datetime对象，默认为当前)
    
    Returns:
        bool: 是否应该执行
    """
    if now is None:
        now = datetime.now()
    
    try:
        matchers = parse_cron(cron_expr)
    except Exception as e:
        print(f"[cron_scheduler] 解析失败: {cron_expr} - {e}")
        return False
    
    # 检查当前时间是否匹配cron表达式
    if not matchers[0](now.minute):  # 分钟
        return False
    if not matchers[1](now.hour):    # 小时
        return False
    if not matchers[2](now.day):     # 日
        return False
    if not matchers[3](now.month):   # 月
        return False
    if not matchers[4](now.weekday()):  # 周 (Python: 0=周一, cron: 0=周日)
        # 转换: Python周一=0 -> cron周一=1
        cron_weekday = (now.weekday() + 1) % 7
        if not matchers[4](cron_weekday):
            return False
    
    # 如果有上次执行时间，检查是否在同一分钟内（防止重复触发）
    if last_run_time:
        if (now.year == last_run_time.year and
            now.month == last_run_time.month and
            now.day == last_run_time.day and
            now.hour == last_run_time.hour and
            now.minute == last_run_time.minute):
            return False
    
    return True


def check_dependencies(task_id, depends_on, done_dir, today=None):
    """
    检查任务依赖是否满足
    
    Args:
        task_id: 当前任务ID
        depends_on: 依赖的任务ID列表
        done_dir: done目录路径
        today: 今天的日期 (datetime对象，默认为今天)
    
    Returns:
        (bool, List[str]): (是否满足, 未满足的任务列表)
    """
    if not depends_on:
        return True, []
    
    if today is None:
        today = datetime.now()
    
    today_str = today.strftime("%Y-%m-%d")
    
    if not os.path.exists(done_dir):
        return False, depends_on
    
    done_files = os.listdir(done_dir)
    missing = []
    
    for dep_task_id in depends_on:
        # 查找今天的依赖任务报告
        found = False
        for df in done_files:
            if df.startswith(today_str) and df.endswith(f"_{dep_task_id}.md"):
                found = True
                break
        
        if not found:
            missing.append(dep_task_id)
    
    return len(missing) == 0, missing

# ============================================================
# 测试和示例
# ============================================================

if __name__ == "__main__":
    print("=== Cron Scheduler 测试 ===\n")
    
    # 测试1: Cron表达式解析
    print("【测试1: Cron表达式】\n")
    
    test_cases = [
        ("0 9 * * *", "每天9:00"),
        ("*/5 * * * *", "每5分钟"),
        ("0 9-17 * * 1-5", "工作日9:00-17:00整点"),
        ("30 8 1 * *", "每月1号8:30"),
    ]
    
    for cron, desc in test_cases:
        try:
            matchers = parse_cron(cron)
            print(f"[OK] {cron:20s} - {desc}")
        except Exception as e:
            print(f"[FAIL] {cron:20s} - 解析失败: {e}")
    
    # 测试2: 时间匹配
    print("\n【测试2: 时间匹配】\n")
    
    # 模拟当前时间为 9:00
    test_time = datetime(2026, 4, 13, 9, 0)
    
    test_exprs = [
        ("0 9 * * *", True, "应该触发"),
        ("0 10 * * *", False, "还没到10点"),
        ("*/5 * * * *", True, "0分钟是5的倍数"),
    ]
    
    for cron, expected, reason in test_exprs:
        result = should_run_cron(cron, now=test_time)
        status = "[OK]" if result == expected else "[FAIL]"
        print(f"{status} {cron:20s} -> {result:5} ({reason})")
    
    # 测试3: 依赖检查
    print("\n【测试3: 任务依赖】\n")
    
    # 模拟done目录
    import tempfile
    with tempfile.TemporaryDirectory() as tmpdir:
        # 创建一些done文件
        today = datetime.now().strftime("%Y-%m-%d")
        
        # 任务A已完成
        open(os.path.join(tmpdir, f"{today}_0900_taskA.md"), "w").close()
        
        # 测试依赖
        satisfied, missing = check_dependencies("taskB", ["taskA"], tmpdir)
        print(f"依赖 taskA: {satisfied} (缺失: {missing})")
        
        satisfied, missing = check_dependencies("taskC", ["taskA", "taskX"], tmpdir)
        print(f"依赖 taskA+taskX: {satisfied} (缺失: {missing})")
    
    print("\n=== 测试完成 ===")
