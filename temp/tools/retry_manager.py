"""
任务失败重试管理模块
为scheduled_task系统提供失败重试能力

功能:
1. 重试策略配置 (最大次数、延迟、退避算法)
2. 重试状态持久化
3. 多种退避算法 (固定、线性、指数)

使用方法:
  from retry_manager import RetryManager
  
  rm = RetryManager(state_file="retry_state.json")
  
  # 检查是否应该重试
  should_retry, delay = rm.should_retry("task1", config)
  
  # 记录失败
  rm.record_failure("task1", "Connection timeout", config)
  
  # 记录成功
  rm.record_success("task1")
"""

from datetime import datetime, timedelta
import json
import os
from pathlib import Path

class RetryManager:
    """任务重试管理器"""
    
    def __init__(self, state_file="retry_state.json"):
        """
        初始化重试管理器
        
        Args:
            state_file: 状态文件路径
        """
        self.state_file = Path(state_file)
        self.state = self._load_state()
    
    def _load_state(self):
        """加载重试状态"""
        if self.state_file.exists():
            try:
                with open(self.state_file, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[retry_manager] 加载状态失败: {e}")
                return {}
        return {}
    
    def _save_state(self):
        """保存重试状态"""
        try:
            self.state_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.state_file, "w", encoding="utf-8") as f:
                json.dump(self.state, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"[retry_manager] 保存状态失败: {e}")    
    def _calculate_delay(self, retry_count, config):
        """
        计算重试延迟
        
        Args:
            retry_count: 当前重试次数
            config: 重试配置
        
        Returns:
            延迟秒数
        """
        base_delay = config.get("retry_delay", 60)
        backoff_type = config.get("backoff_type", "exponential")
        backoff_factor = config.get("backoff_factor", 2)
        
        if backoff_type == "fixed":
            return base_delay
        elif backoff_type == "linear":
            return base_delay * retry_count
        elif backoff_type == "exponential":
            return base_delay * (backoff_factor ** (retry_count - 1))
        else:
            return base_delay
    
    def should_retry(self, task_id, config):
        """
        检查任务是否应该重试
        
        Args:
            task_id: 任务ID
            config: 重试配置 {
                "max_retries": 3,
                "retry_delay": 60,
                "backoff_type": "exponential",
                "backoff_factor": 2
            }
        
        Returns:
            (should_retry: bool, delay: int)
        """
        if task_id not in self.state:
            return True, 0  # 首次执行
        
        task_state = self.state[task_id]
        retry_count = task_state.get("retry_count", 0)
        max_retries = config.get("max_retries", 3)
        
        # 检查是否超过最大重试次数
        if retry_count >= max_retries:
            return False, 0
        
        # 检查是否到达重试时间
        next_retry_str = task_state.get("next_retry")
        if next_retry_str:
            next_retry = datetime.fromisoformat(next_retry_str)
            now = datetime.now()
            if now < next_retry:
                delay = int((next_retry - now).total_seconds())
                return False, delay  # 还未到重试时间
        
        return True, 0
    
    def record_failure(self, task_id, error_message, config):
        """
        记录任务失败
        
        Args:
            task_id: 任务ID
            error_message: 错误信息
            config: 重试配置
        """
        now = datetime.now()
        
        if task_id not in self.state:
            self.state[task_id] = {
                "retry_count": 0,
                "last_failure": None,
                "next_retry": None,
                "error_message": None
            }
        
        task_state = self.state[task_id]
        task_state["retry_count"] += 1
        task_state["last_failure"] = now.isoformat()
        task_state["error_message"] = error_message
        
        # 计算下次重试时间
        delay = self._calculate_delay(task_state["retry_count"], config)
        next_retry = now + timedelta(seconds=delay)
        task_state["next_retry"] = next_retry.isoformat()
        
        self._save_state()
        
        retry_time_str = next_retry.strftime("%Y-%m-%d %H:%M:%S")
        print(f"[retry_manager] {task_id} 失败 (第{task_state['retry_count']}次), "
              f"下次重试: {retry_time_str}")
    
    def record_success(self, task_id):
        """
        记录任务成功，清除重试状态
        
        Args:
            task_id: 任务ID
        """
        if task_id in self.state:
            del self.state[task_id]
            self._save_state()
            print(f"[retry_manager] {task_id} 成功，清除重试状态")
    
    def get_retry_status(self, task_id):
        """
        获取任务重试状态
        
        Args:
            task_id: 任务ID
        
        Returns:
            重试状态字典，如果任务不存在返回None
        """
        return self.state.get(task_id)
    
    def get_all_retrying_tasks(self):
        """获取所有正在重试的任务"""
        return list(self.state.keys())
    
    def clear_task(self, task_id):
        """
        清除任务重试状态
        
        Args:
            task_id: 任务ID
        """
        if task_id in self.state:
            del self.state[task_id]
            self._save_state()


# ============ 测试代码 ============
if __name__ == "__main__":
    print("=== RetryManager 测试 ===\n")
    
    # 创建测试管理器
    rm = RetryManager("test_retry_state.json")
    
    # 测试配置
    config = {
        "max_retries": 3,
        "retry_delay": 5,  # 5秒用于测试
        "backoff_type": "exponential",
        "backoff_factor": 2
    }
    
    print("【测试1: 首次执行】")
    should, delay = rm.should_retry("task1", config)
    print(f"  should_retry: {should}, delay: {delay}s")
    print()
    
    print("【测试2: 记录失败】")
    rm.record_failure("task1", "Connection timeout", config)
    status = rm.get_retry_status("task1")
    print(f"  状态: {status}")
    print()
    
    print("【测试3: 检查重试（立即）】")
    should, delay = rm.should_retry("task1", config)
    print(f"  should_retry: {should}, delay: {delay}s")
    print()
    
    print("【测试4: 多次失败】")
    for i in range(2, 4):
        rm.record_failure("task1", f"Error {i}", config)
        status = rm.get_retry_status("task1")
        retry_count = status['retry_count']
        print(f"  第{i}次失败: retry_count={retry_count}")
    print()
    
    print("【测试5: 超过最大重试次数】")
    should, delay = rm.should_retry("task1", config)
    print(f"  should_retry: {should}, delay: {delay}s")
    print()
    
    print("【测试6: 记录成功】")
    rm.record_success("task1")
    status = rm.get_retry_status("task1")
    print(f"  状态: {status}")
    print()
    
    print("【测试7: 不同退避算法】")
    for backoff_type in ["fixed", "linear", "exponential"]:
        test_config = config.copy()
        test_config["backoff_type"] = backoff_type
        print(f"  {backoff_type}:")
        for retry in range(1, 4):
            delay = rm._calculate_delay(retry, test_config)
            print(f"    第{retry}次重试延迟: {delay}s")
    print()
    
    # 清理测试文件
    import os
    if os.path.exists("test_retry_state.json"):
        os.remove("test_retry_state.json")
    
    print("[OK] 测试完成")
