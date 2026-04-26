"""
进程管理器
提供进程启动、停止、重启、监控和自动重启功能

功能:
1. 启动进程 - start_process()
2. 停止进程 - stop_process()
3. 重启进程 - restart_process()
4. 监控资源 - monitor_process()
5. 自动重启守护 - auto_restart_daemon()

依赖: psutil (pip install psutil)
"""

import os
import sys
import time
import subprocess
import psutil
from datetime import datetime
from typing import Optional, Dict, List


class ProcessManager:
    """进程管理器类"""
    
    def __init__(self):
        self.processes = {}  # {name: {"pid": int, "cmd": str, "start_time": float}}
    
    def start_process(self, name: str, command: str, cwd: str = None, 
                     env: dict = None, shell: bool = True) -> Dict:
        """
        启动进程
        
        Args:
            name: 进程名称（用于管理）
            command: 启动命令
            cwd: 工作目录
            env: 环境变量
            shell: 是否使用shell
        
        Returns:
            {"success": bool, "pid": int, "message": str}
        """
        try:
            # 检查是否已存在
            if name in self.processes:
                pid = self.processes[name]["pid"]
                if psutil.pid_exists(pid):
                    return {
                        "success": False,
                        "message": f"进程 {name} 已在运行 (PID: {pid})"
                    }
            
            # 启动进程
            proc = subprocess.Popen(
                command,
                shell=shell,
                cwd=cwd,
                env=env,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # 记录进程信息
            self.processes[name] = {
                "pid": proc.pid,
                "cmd": command,
                "start_time": time.time(),
                "cwd": cwd
            }
            
            return {
                "success": True,
                "pid": proc.pid,
                "message": f"进程 {name} 启动成功"
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"启动失败: {e}"
            }
    def stop_process(self, name: str, timeout: int = 5, force: bool = False) -> Dict:
        """
        停止进程
        
        Args:
            name: 进程名称
            timeout: 等待超时（秒）
            force: 是否强制终止
        
        Returns:
            {"success": bool, "message": str}
        """
        if name not in self.processes:
            return {"success": False, "message": f"进程 {name} 不存在"}
        
        pid = self.processes[name]["pid"]
        
        try:
            if not psutil.pid_exists(pid):
                del self.processes[name]
                return {"success": True, "message": f"进程 {name} 已停止"}
            
            proc = psutil.Process(pid)
            
            if force:
                proc.kill()  # SIGKILL
            else:
                proc.terminate()  # SIGTERM
                try:
                    proc.wait(timeout=timeout)
                except psutil.TimeoutExpired:
                    proc.kill()  # 超时强制终止
            
            del self.processes[name]
            return {"success": True, "message": f"进程 {name} 已停止"}
            
        except Exception as e:
            return {"success": False, "message": f"停止失败: {e}"}
    
    def restart_process(self, name: str) -> Dict:
        """
        重启进程
        
        Args:
            name: 进程名称
        
        Returns:
            {"success": bool, "message": str, "pid": int}
        """
        if name not in self.processes:
            return {"success": False, "message": f"进程 {name} 不存在"}
        
        # 保存启动参数
        cmd = self.processes[name]["cmd"]
        cwd = self.processes[name].get("cwd")
        
        # 停止进程
        stop_result = self.stop_process(name)
        if not stop_result["success"]:
            return stop_result
        
        # 等待一下
        time.sleep(0.5)
        
        # 重新启动
        return self.start_process(name, cmd, cwd=cwd)
    
    def monitor_process(self, name: str) -> Dict:
        """
        监控进程资源使用
        
        Args:
            name: 进程名称
        
        Returns:
            {"success": bool, "pid": int, "cpu": float, "memory": float, "status": str}
        """
        if name not in self.processes:
            return {"success": False, "message": f"进程 {name} 不存在"}
        
        pid = self.processes[name]["pid"]
        
        try:
            if not psutil.pid_exists(pid):
                return {
                    "success": False,
                    "message": f"进程 {name} 已停止",
                    "status": "stopped"
                }
            
            proc = psutil.Process(pid)
            
            return {
                "success": True,
                "pid": pid,
                "cpu_percent": proc.cpu_percent(interval=0.1),
                "memory_mb": proc.memory_info().rss / 1024 / 1024,
                "status": proc.status(),
                "num_threads": proc.num_threads(),
                "create_time": proc.create_time()
            }
            
        except Exception as e:
            return {"success": False, "message": f"监控失败: {e}"}
    def auto_restart_daemon(self, name: str, max_restarts: int = 3, 
                           check_interval: int = 5) -> Dict:
        """
        自动重启守护（阻塞式）
        
        Args:
            name: 进程名称
            max_restarts: 最大重启次数
            check_interval: 检查间隔（秒）
        
        Returns:
            {"success": bool, "restarts": int, "message": str}
        """
        if name not in self.processes:
            return {"success": False, "message": f"进程 {name} 不存在"}
        
        restart_count = 0
        
        print(f"[守护] 开始监控进程 {name}")
        
        try:
            while restart_count < max_restarts:
                time.sleep(check_interval)
                
                # 检查进程状态
                monitor_result = self.monitor_process(name)
                
                if not monitor_result["success"] or monitor_result.get("status") == "stopped":
                    print(f"[守护] 检测到进程 {name} 停止，尝试重启...")
                    
                    restart_result = self.restart_process(name)
                    
                    if restart_result["success"]:
                        restart_count += 1
                        print(f"[守护] 重启成功 ({restart_count}/{max_restarts})")
                    else:
                        print(f"[守护] 重启失败: {restart_result['message']}")
                        break
                else:
                    # 进程正常运行
                    cpu = monitor_result.get("cpu_percent", 0)
                    mem = monitor_result.get("memory_mb", 0)
                    print(f"[守护] 进程 {name} 运行正常 (CPU: {cpu:.1f}%, MEM: {mem:.1f}MB)")
            
            return {
                "success": True,
                "restarts": restart_count,
                "message": f"守护结束，共重启 {restart_count} 次"
            }
            
        except KeyboardInterrupt:
            print(f"[守护] 用户中断")
            return {
                "success": True,
                "restarts": restart_count,
                "message": "用户中断守护"
            }
    
    def list_processes(self) -> List[Dict]:
        """列出所有管理的进程"""
        result = []
        for name, info in self.processes.items():
            pid = info["pid"]
            status = "running" if psutil.pid_exists(pid) else "stopped"
            result.append({
                "name": name,
                "pid": pid,
                "status": status,
                "cmd": info["cmd"]
            })
        return result


# ============================================================
# 测试和示例
# ============================================================

if __name__ == "__main__":
    print("=== Process Manager 测试 ===\n")
    
    pm = ProcessManager()
    
    # 测试1: 启动进程
    print("【测试1: 启动进程】\n")
    
    # 启动一个简单的Python进程
    result = pm.start_process(
        name="test_sleep",
        command=f"{sys.executable} -c \"import time; time.sleep(10)\""
    )
    print(f"启动结果: {result}")
    
    if result["success"]:
        time.sleep(1)
        
        # 测试2: 监控进程
        print("\n【测试2: 监控进程】\n")
        monitor = pm.monitor_process("test_sleep")
        print(f"监控结果: {monitor}")
        
        # 测试3: 列出进程
        print("\n【测试3: 列出进程】\n")
        processes = pm.list_processes()
        for p in processes:
            print(f"  {p['name']:15s} PID:{p['pid']:6d} {p['status']}")
        
        # 测试4: 停止进程
        print("\n【测试4: 停止进程】\n")
        stop = pm.stop_process("test_sleep")
        print(f"停止结果: {stop}")
        
        # 验证停止
        time.sleep(0.5)
        monitor2 = pm.monitor_process("test_sleep")
        print(f"停止后状态: {monitor2}")
    
    print("\n=== 测试完成 ===")
