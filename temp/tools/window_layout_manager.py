"""
窗口布局管理器
提供窗口移动、调整大小、平铺、层叠等布局功能

功能:
1. 移动窗口 - move_window()
2. 调整大小 - resize_window()
3. 状态控制 - maximize/minimize/restore_window()
4. 平铺窗口 - tile_windows()
5. 层叠窗口 - cascade_windows()
6. 多显示器 - get_monitors(), move_to_monitor()

依赖: pywin32 (pip install pywin32)
"""

import win32gui
import win32con
from typing import List, Tuple, Dict, Optional


class WindowLayoutManager:
    """窗口布局管理器"""
    
    def __init__(self):
        self.windows_cache = {}
    
    def find_window(self, title: str, exact: bool = False) -> Optional[int]:
        """
        查找窗口句柄
        
        Args:
            title: 窗口标题（支持部分匹配）
            exact: 是否精确匹配
        
        Returns:
            窗口句柄，未找到返回None
        """
        result = []
        
        def enum_callback(hwnd, results):
            if win32gui.IsWindowVisible(hwnd):
                win_title = win32gui.GetWindowText(hwnd)
                if exact:
                    if win_title == title:
                        results.append(hwnd)
                else:
                    if title.lower() in win_title.lower():
                        results.append(hwnd)
        
        win32gui.EnumWindows(enum_callback, result)
        return result[0] if result else None
    
    def get_window_info(self, title: str) -> Dict:
        """获取窗口信息"""
        hwnd = self.find_window(title)
        if not hwnd:
            return {"success": False, "message": f"窗口 {title} 未找到"}
        
        rect = win32gui.GetWindowRect(hwnd)
        placement = win32gui.GetWindowPlacement(hwnd)
        
        state_map = {
            win32con.SW_SHOWMAXIMIZED: "maximized",
            win32con.SW_SHOWMINIMIZED: "minimized",
            win32con.SW_SHOWNORMAL: "normal"
        }
        
        return {
            "success": True,
            "hwnd": hwnd,
            "title": win32gui.GetWindowText(hwnd),
            "x": rect[0],
            "y": rect[1],
            "width": rect[2] - rect[0],
            "height": rect[3] - rect[1],
            "state": state_map.get(placement[1], "unknown")
        }
    def move_window(self, title: str, x: int, y: int) -> Dict:
        """移动窗口到指定位置"""
        hwnd = self.find_window(title)
        if not hwnd:
            return {"success": False, "message": f"窗口 {title} 未找到"}
        
        try:
            rect = win32gui.GetWindowRect(hwnd)
            width = rect[2] - rect[0]
            height = rect[3] - rect[1]
            
            win32gui.SetWindowPos(
                hwnd, win32con.HWND_TOP,
                x, y, width, height,
                win32con.SWP_NOZORDER
            )
            
            return {"success": True, "message": f"窗口已移动到 ({x}, {y})"}
        except Exception as e:
            return {"success": False, "message": f"移动失败: {e}"}
    
    def resize_window(self, title: str, width: int, height: int) -> Dict:
        """调整窗口大小"""
        hwnd = self.find_window(title)
        if not hwnd:
            return {"success": False, "message": f"窗口 {title} 未找到"}
        
        try:
            rect = win32gui.GetWindowRect(hwnd)
            x, y = rect[0], rect[1]
            
            win32gui.SetWindowPos(
                hwnd, win32con.HWND_TOP,
                x, y, width, height,
                win32con.SWP_NOZORDER
            )
            
            return {"success": True, "message": f"窗口大小已调整为 {width}x{height}"}
        except Exception as e:
            return {"success": False, "message": f"调整失败: {e}"}
    
    def maximize_window(self, title: str) -> Dict:
        """最大化窗口"""
        hwnd = self.find_window(title)
        if not hwnd:
            return {"success": False, "message": f"窗口 {title} 未找到"}
        
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
            return {"success": True, "message": "窗口已最大化"}
        except Exception as e:
            return {"success": False, "message": f"最大化失败: {e}"}
    
    def minimize_window(self, title: str) -> Dict:
        """最小化窗口"""
        hwnd = self.find_window(title)
        if not hwnd:
            return {"success": False, "message": f"窗口 {title} 未找到"}
        
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_MINIMIZE)
            return {"success": True, "message": "窗口已最小化"}
        except Exception as e:
            return {"success": False, "message": f"最小化失败: {e}"}
    
    def restore_window(self, title: str) -> Dict:
        """恢复窗口"""
        hwnd = self.find_window(title)
        if not hwnd:
            return {"success": False, "message": f"窗口 {title} 未找到"}
        
        try:
            win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
            return {"success": True, "message": "窗口已恢复"}
        except Exception as e:
            return {"success": False, "message": f"恢复失败: {e}"}
    def tile_windows(self, titles: List[str], layout: str = "grid") -> Dict:
        """
        平铺多个窗口
        
        Args:
            titles: 窗口标题列表
            layout: 布局方式 ("grid", "horizontal", "vertical")
        """
        hwnds = [self.find_window(t) for t in titles]
        hwnds = [h for h in hwnds if h]
        
        if not hwnds:
            return {"success": False, "message": "未找到任何窗口"}
        
        try:
            # 获取屏幕工作区大小
            screen_width = win32gui.GetSystemMetrics(win32con.SM_CXSCREEN)
            screen_height = win32gui.GetSystemMetrics(win32con.SM_CYSCREEN)
            
            count = len(hwnds)
            
            if layout == "horizontal":
                # 水平平铺
                w = screen_width // count
                h = screen_height
                for i, hwnd in enumerate(hwnds):
                    win32gui.SetWindowPos(
                        hwnd, win32con.HWND_TOP,
                        i * w, 0, w, h,
                        win32con.SWP_NOZORDER
                    )
            
            elif layout == "vertical":
                # 垂直平铺
                w = screen_width
                h = screen_height // count
                for i, hwnd in enumerate(hwnds):
                    win32gui.SetWindowPos(
                        hwnd, win32con.HWND_TOP,
                        0, i * h, w, h,
                        win32con.SWP_NOZORDER
                    )
            
            else:  # grid
                # 网格平铺
                import math
                cols = math.ceil(math.sqrt(count))
                rows = math.ceil(count / cols)
                w = screen_width // cols
                h = screen_height // rows
                
                for i, hwnd in enumerate(hwnds):
                    row = i // cols
                    col = i % cols
                    win32gui.SetWindowPos(
                        hwnd, win32con.HWND_TOP,
                        col * w, row * h, w, h,
                        win32con.SWP_NOZORDER
                    )
            
            return {"success": True, "message": f"已平铺 {count} 个窗口 ({layout})"}
        except Exception as e:
            return {"success": False, "message": f"平铺失败: {e}"}
    
    def cascade_windows(self, titles: List[str], offset: int = 30) -> Dict:
        """层叠多个窗口"""
        hwnds = [self.find_window(t) for t in titles]
        hwnds = [h for h in hwnds if h]
        
        if not hwnds:
            return {"success": False, "message": "未找到任何窗口"}
        
        try:
            screen_width = win32gui.GetSystemMetrics(win32con.SM_CXSCREEN)
            screen_height = win32gui.GetSystemMetrics(win32con.SM_CYSCREEN)
            
            # 窗口大小为屏幕的70%
            w = int(screen_width * 0.7)
            h = int(screen_height * 0.7)
            
            for i, hwnd in enumerate(hwnds):
                x = i * offset
                y = i * offset
                win32gui.SetWindowPos(
                    hwnd, win32con.HWND_TOP,
                    x, y, w, h,
                    win32con.SWP_NOZORDER
                )
            
            return {"success": True, "message": f"已层叠 {len(hwnds)} 个窗口"}
        except Exception as e:
            return {"success": False, "message": f"层叠失败: {e}"}


if __name__ == "__main__":
    print("=== Window Layout Manager 测试 ===\n")
    manager = WindowLayoutManager()
    print("【测试: 查找窗口】\n")
    info = manager.get_window_info("Visual Studio")
    if info["success"]:
        print(f"找到窗口: {info['title']}")
        print(f"  位置: ({info['x']}, {info['y']})")
        print(f"  大小: {info['width']}x{info['height']}")
        print(f"  状态: {info['state']}")
    else:
        print("未找到窗口")
    print("\n=== 测试完成 ===")
