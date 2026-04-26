"""
Android 应用管理器
提供应用安装、卸载、列表管理、性能监控、日志抓取等功能

功能:
1. 应用安装/卸载 - install_app(), uninstall_app()
2. 应用列表管理 - list_apps(), get_app_info()
3. 性能监控 - monitor_performance()
4. 日志抓取 - capture_logs()
5. 应用启动/停止 - start_app(), stop_app()

依赖: adb (Android Debug Bridge)
"""

import subprocess
import re
import shutil
from typing import Dict, List, Optional
from datetime import datetime

ADB = shutil.which("adb") or "adb"


class AndroidAppManager:
    """Android 应用管理器"""
    
    def __init__(self, device_id: Optional[str] = None):
        """
        初始化
        
        Args:
            device_id: 设备ID，None表示使用默认设备
        """
        self.device_id = device_id
        self.adb_prefix = [ADB]
        if device_id:
            self.adb_prefix.extend(["-s", device_id])
    
    def _run_adb(self, *args, timeout=30) -> subprocess.CompletedProcess:
        """执行 adb 命令"""
        cmd = self.adb_prefix + list(args)
        return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    
    def install_app(self, apk_path: str, replace: bool = True) -> Dict:
        """
        安装应用
        
        Args:
            apk_path: APK文件路径
            replace: 是否替换已存在的应用
        """
        try:
            args = ["install"]
            if replace:
                args.append("-r")
            args.append(apk_path)
            
            result = self._run_adb(*args, timeout=120)
            
            if "Success" in result.stdout or "Success" in result.stderr:
                return {"success": True, "message": "应用安装成功"}
            else:
                error = result.stdout + result.stderr
                return {"success": False, "message": f"安装失败: {error}"}
        except Exception as e:
            return {"success": False, "message": f"安装异常: {e}"}
    
    def uninstall_app(self, package_name: str, keep_data: bool = False) -> Dict:
        """
        卸载应用
        
        Args:
            package_name: 应用包名
            keep_data: 是否保留数据
        """
        try:
            args = ["uninstall"]
            if keep_data:
                args.append("-k")
            args.append(package_name)
            
            result = self._run_adb(*args)
            
            if "Success" in result.stdout or "Success" in result.stderr:
                return {"success": True, "message": "应用卸载成功"}
            else:
                error = result.stdout + result.stderr
                return {"success": False, "message": f"卸载失败: {error}"}
        except Exception as e:
            return {"success": False, "message": f"卸载异常: {e}"}
    def list_apps(self, filter_type: str = "all") -> Dict:
        """
        列出应用
        
        Args:
            filter_type: 过滤类型 ("all", "system", "third_party", "enabled", "disabled")
        """
        try:
            args = ["shell", "pm", "list", "packages"]
            
            if filter_type == "system":
                args.append("-s")
            elif filter_type == "third_party":
                args.append("-3")
            elif filter_type == "enabled":
                args.append("-e")
            elif filter_type == "disabled":
                args.append("-d")
            
            result = self._run_adb(*args)
            
            if result.returncode == 0:
                packages = []
                for line in result.stdout.strip().split("\n"):
                    if line.startswith("package:"):
                        packages.append(line.replace("package:", ""))
                
                return {
                    "success": True,
                    "packages": packages,
                    "count": len(packages)
                }
            else:
                return {"success": False, "message": "获取应用列表失败"}
        except Exception as e:
            return {"success": False, "message": f"异常: {e}"}
    
    def get_app_info(self, package_name: str) -> Dict:
        """获取应用详细信息"""
        try:
            result = self._run_adb("shell", "dumpsys", "package", package_name)
            
            if result.returncode == 0:
                output = result.stdout
                
                # 提取版本信息
                version_match = re.search(r"versionName=([^\s]+)", output)
                version = version_match.group(1) if version_match else "unknown"
                
                # 提取安装路径
                path_match = re.search(r"codePath=([^\s]+)", output)
                path = path_match.group(1) if path_match else "unknown"
                
                return {
                    "success": True,
                    "package": package_name,
                    "version": version,
                    "path": path
                }
            else:
                return {"success": False, "message": "应用不存在"}
        except Exception as e:
            return {"success": False, "message": f"异常: {e}"}
    
    def start_app(self, package_name: str, activity: Optional[str] = None) -> Dict:
        """
        启动应用
        
        Args:
            package_name: 应用包名
            activity: 启动Activity，None表示启动主Activity
        """
        try:
            if activity:
                component = f"{package_name}/{activity}"
            else:
                # 获取主Activity
                result = self._run_adb("shell", "cmd", "package", "resolve-activity",
                                       "--brief", package_name)
                if result.returncode != 0:
                    return {"success": False, "message": "无法获取主Activity"}
                
                lines = result.stdout.strip().split("\n")
                component = lines[-1] if lines else None
                if not component or "/" not in component:
                    return {"success": False, "message": "无法解析主Activity"}
            
            result = self._run_adb("shell", "am", "start", "-n", component)
            
            if "Error" not in result.stdout and "Error" not in result.stderr:
                return {"success": True, "message": "应用启动成功"}
            else:
                error = result.stdout + result.stderr
                return {"success": False, "message": f"启动失败: {error}"}
        except Exception as e:
            return {"success": False, "message": f"异常: {e}"}
    
    def stop_app(self, package_name: str) -> Dict:
        """停止应用"""
        try:
            result = self._run_adb("shell", "am", "force-stop", package_name)
            
            if result.returncode == 0:
                return {"success": True, "message": "应用已停止"}
            else:
                return {"success": False, "message": "停止失败"}
        except Exception as e:
            return {"success": False, "message": f"异常: {e}"}
    def monitor_performance(self, package_name: Optional[str] = None) -> Dict:
        """
        监控性能
        
        Args:
            package_name: 应用包名，None表示监控整体性能
        """
        try:
            result = {}
            
            # CPU 使用率
            if package_name:
                cpu_result = self._run_adb("shell", "dumpsys", "cpuinfo", "|", "grep", package_name)
            else:
                cpu_result = self._run_adb("shell", "dumpsys", "cpuinfo")
            result["cpu"] = cpu_result.stdout.strip() if cpu_result.returncode == 0 else "N/A"
            
            # 内存使用
            if package_name:
                mem_result = self._run_adb("shell", "dumpsys", "meminfo", package_name)
                if mem_result.returncode == 0:
                    # 提取关键内存信息
                    match = re.search(r"TOTAL\s+(\d+)", mem_result.stdout)
                    if match:
                        total_kb = int(match.group(1))
                        result["memory_mb"] = round(total_kb / 1024, 2)
                    else:
                        result["memory"] = "N/A"
            
            # 电池信息
            battery_result = self._run_adb("shell", "dumpsys", "battery")
            if battery_result.returncode == 0:
                level_match = re.search(r"level: (\d+)", battery_result.stdout)
                temp_match = re.search(r"temperature: (\d+)", battery_result.stdout)
                result["battery_level"] = int(level_match.group(1)) if level_match else "N/A"
                result["battery_temp"] = int(temp_match.group(1)) / 10 if temp_match else "N/A"
            
            return {"success": True, "performance": result}
        except Exception as e:
            return {"success": False, "message": f"异常: {e}"}
    
    def capture_logs(self, package_name: Optional[str] = None, 
                    lines: int = 100, clear: bool = False) -> Dict:
        """
        抓取日志
        
        Args:
            package_name: 应用包名，None表示抓取所有日志
            lines: 抓取行数
            clear: 是否先清空日志
        """
        try:
            if clear:
                self._run_adb("logcat", "-c")
            
            args = ["logcat", "-d", "-t", str(lines)]
            result = self._run_adb(*args)
            
            if result.returncode == 0:
                logs = result.stdout
                
                # 如果指定包名，过滤日志
                if package_name:
                    filtered_logs = []
                    for line in logs.split("\n"):
                        if package_name in line:
                            filtered_logs.append(line)
                    logs = "\n".join(filtered_logs)
                
                return {
                    "success": True,
                    "logs": logs,
                    "lines_count": len(logs.split("\n"))
                }
            else:
                return {"success": False, "message": "日志抓取失败"}
        except Exception as e:
            return {"success": False, "message": f"异常: {e}"}


# ============ 使用示例 ============

if __name__ == "__main__":
    print("=== Android App Manager 使用指南 ===\n")
    
    manager = AndroidAppManager()
    
    print("【功能列表】\n")
    print("1. 应用安装")
    print("   manager.install_app('/path/to/app.apk')")
    print("   manager.install_app('/path/to/app.apk', replace=True)  # 替换安装\n")
    
    print("2. 应用卸载")
    print("   manager.uninstall_app('com.example.app')")
    print("   manager.uninstall_app('com.example.app', keep_data=True)  # 保留数据\n")
    
    print("3. 应用列表")
    print("   manager.list_apps()  # 所有应用")
    print("   manager.list_apps('third_party')  # 第三方应用")
    print("   manager.list_apps('system')  # 系统应用\n")
    
    print("4. 应用信息")
    print("   manager.get_app_info('com.example.app')\n")
    
    print("5. 启动/停止应用")
    print("   manager.start_app('com.example.app')")
    print("   manager.stop_app('com.example.app')\n")
    
    print("6. 性能监控")
    print("   manager.monitor_performance()  # 整体性能")
    print("   manager.monitor_performance('com.example.app')  # 应用性能\n")
    
    print("7. 日志抓取")
    print("   manager.capture_logs(lines=100)")
    print("   manager.capture_logs('com.example.app', lines=50)\n")
    
    print("=== 使用指南完成 ===")