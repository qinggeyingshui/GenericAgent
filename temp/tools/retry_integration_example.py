"""
retry_manager 与 scheduled_task 集成示例
演示如何在定时任务中使用失败重试功能
"""

from retry_manager import RetryManager
from cron_scheduler import should_run_cron, check_dependencies
import json
from datetime import datetime

# 初始化重试管理器
retry_mgr = RetryManager("./sche_tasks/retry_state.json")

# 任务配置示例
task_config = {
    "task_id": "daily_report",
    "cron": "0 9 * * *",  # 每天9点
    "retry_config": {
        "max_retries": 3,
        "retry_delay": 300,  # 5分钟
        "backoff_type": "exponential",
        "backoff_factor": 2
    }
}

def run_task_with_retry(task_id, task_func, retry_config):
    """
    带重试的任务执行器
    
    Args:
        task_id: 任务ID
        task_func: 任务函数
        retry_config: 重试配置
    
    Returns:
        bool: 是否执行成功
    """
    # 1. 检查是否应该重试
    should_retry, delay = retry_mgr.should_retry(task_id, retry_config)
    
    if not should_retry:
        if delay > 0:
            print(f"[{task_id}] 等待重试，剩余 {delay}秒")
            return False
        else:
            print(f"[{task_id}] 已达最大重试次数，跳过")
            return False
    
    # 2. 执行任务
    try:
        print(f"[{task_id}] 开始执行...")
        task_func()
        
        # 3. 成功：清除重试状态
        retry_mgr.record_success(task_id)
        print(f"[{task_id}] 执行成功")
        return True
        
    except Exception as e:
        # 4. 失败：记录重试状态
        retry_mgr.record_failure(task_id, str(e), retry_config)
        print(f"[{task_id}] 执行失败: {e}")
        return False

# 使用示例
def my_task():
    """示例任务"""
    # 模拟可能失败的操作
    import random
    if random.random() < 0.3:  # 30%失败率
        raise Exception("网络超时")
    print("任务执行成功！")

# 在调度循环中使用
if __name__ == "__main__":
    task_id = task_config["task_id"]
    retry_config = task_config["retry_config"]
    
    # 执行任务
    run_task_with_retry(task_id, my_task, retry_config)
