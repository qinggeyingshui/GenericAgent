"""
反爬虫处理工具包

功能:
1. User-Agent 轮换
2. 请求延迟随机化
3. Cookie/Session 管理
4. 动态内容等待（基于 CDP）
5. 批量抓取限流器

依赖: web_execute_js 工具（通过 tmwebdriver CDP 桥）
"""

import random
import time
import json
from typing import List, Dict, Optional, Callable
from datetime import datetime, timedelta


class UserAgentRotator:
    """User-Agent 轮换器"""
    
    # 常见浏览器 UA 池
    USER_AGENTS = [
        # Chrome on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
        # Chrome on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        # Firefox on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
        # Firefox on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:121.0) Gecko/20100101 Firefox/121.0",
        # Edge on Windows
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edg/120.0.0.0",
        # Safari on macOS
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15",
    ]
    
    def __init__(self, custom_agents: Optional[List[str]] = None):
        """
        初始化
        
        Args:
            custom_agents: 自定义 UA 列表（可选）
        """
        self.agents = custom_agents if custom_agents else self.USER_AGENTS
        self.current_index = 0
    
    def get_random(self) -> str:
        """随机获取一个 UA"""
        return random.choice(self.agents)
    
    def get_next(self) -> str:
        """轮询获取下一个 UA"""
        ua = self.agents[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.agents)
        return ua
    
    def set_ua_via_cdp(self, ua: str, web_execute_js_func: Callable) -> Dict:
        """
        通过 CDP 设置 User-Agent
        
        Args:
            ua: User-Agent 字符串
            web_execute_js_func: web_execute_js 工具函数
        
        Returns:
            CDP 执行结果
        """
        cdp_cmd = {
            "cmd": "cdp",
            "method": "Network.setUserAgentOverride",
            "params": {"userAgent": ua}
        }
        return web_execute_js_func(script=json.dumps(cdp_cmd))

class RequestDelayManager:
    """请求延迟管理器（模拟人类行为）"""
    
    def __init__(self, min_delay: float = 1.0, max_delay: float = 3.0):
        """
        初始化
        
        Args:
            min_delay: 最小延迟（秒）
            max_delay: 最大延迟（秒）
        """
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.last_request_time = None
    
    def wait(self):
        """执行随机延迟"""
        if self.last_request_time:
            elapsed = time.time() - self.last_request_time
            delay = random.uniform(self.min_delay, self.max_delay)
            if elapsed < delay:
                time.sleep(delay - elapsed)
        self.last_request_time = time.time()
    
    def random_delay(self, min_sec: Optional[float] = None, max_sec: Optional[float] = None):
        """
        执行一次性随机延迟
        
        Args:
            min_sec: 最小延迟（覆盖默认值）
            max_sec: 最大延迟（覆盖默认值）
        """
        min_d = min_sec if min_sec is not None else self.min_delay
        max_d = max_sec if max_sec is not None else self.max_delay
        delay = random.uniform(min_d, max_d)
        time.sleep(delay)


class RateLimiter:
    """批量抓取限流器"""
    
    def __init__(self, max_requests: int = 10, time_window: int = 60):
        """
        初始化
        
        Args:
            max_requests: 时间窗口内最大请求数
            time_window: 时间窗口（秒）
        """
        self.max_requests = max_requests
        self.time_window = time_window
        self.requests = []  # [(timestamp, ...)]
    
    def acquire(self) -> bool:
        """
        尝试获取请求许可
        
        Returns:
            True: 允许请求
            False: 超过限流，需等待
        """
        now = time.time()
        # 清理过期记录
        self.requests = [t for t in self.requests if now - t < self.time_window]
        
        if len(self.requests) < self.max_requests:
            self.requests.append(now)
            return True
        return False
    
    def wait_if_needed(self):
        """如果超限则等待"""
        while not self.acquire():
            # 计算需要等待的时间
            if self.requests:
                oldest = self.requests[0]
                wait_time = self.time_window - (time.time() - oldest) + 0.1
                if wait_time > 0:
                    print(f"[RateLimiter] 达到限流，等待 {wait_time:.1f}秒...")
                    time.sleep(wait_time)
            else:
                break

class DynamicContentWaiter:
    """动态内容等待器（基于 CDP）"""
    
    @staticmethod
    def wait_for_element(selector: str, web_execute_js_func: Callable, 
                         timeout: int = 10, interval: float = 0.5) -> bool:
        """
        等待元素出现
        
        Args:
            selector: CSS 选择器
            web_execute_js_func: web_execute_js 工具函数
            timeout: 超时时间（秒）
            interval: 轮询间隔（秒）
        
        Returns:
            True: 元素出现
            False: 超时
        """
        start_time = time.time()
        
        while time.time() - start_time < timeout:
            # 使用 CDP DOM.performSearch 轻量级检测
            cdp_cmd = {
                "cmd": "batch",
                "commands": [
                    {"cmd": "cdp", "method": "DOM.getDocument", "params": {"depth": 1}},
                    {"cmd": "cdp", "method": "DOM.performSearch", 
                     "params": {"query": selector}}
                ]
            }
            
            result = web_execute_js_func(script=json.dumps(cdp_cmd))
            
            if result.get("ok") and len(result.get("results", [])) >= 2:
                search_result = result["results"][1]
                if search_result.get("ok") and search_result.get("resultCount", 0) > 0:
                    return True
            
            time.sleep(interval)
        
        return False
    
    @staticmethod
    def wait_for_network_idle(web_execute_js_func: Callable, 
                               idle_time: float = 0.5, timeout: int = 10) -> bool:
        """
        等待网络空闲（所有请求完成）
        
        Args:
            web_execute_js_func: web_execute_js 工具函数
            idle_time: 空闲判定时间（秒）
            timeout: 超时时间（秒）
        
        Returns:
            True: 网络空闲
            False: 超时
        """
        # 启用网络监控
        enable_cmd = {"cmd": "cdp", "method": "Network.enable", "params": {}}
        web_execute_js_func(script=json.dumps(enable_cmd))
        
        start_time = time.time()
        last_activity = time.time()
        
        # 简化实现：等待固定时间后检查 document.readyState
        while time.time() - start_time < timeout:
            check_js = """
            return {
                readyState: document.readyState,
                activeRequests: performance.getEntriesByType("resource")
                    .filter(r => !r.responseEnd).length
            };
            """
            
            result = web_execute_js_func(script=check_js)
            
            if (result.get("readyState") == "complete" and 
                result.get("activeRequests", 0) == 0):
                if time.time() - last_activity >= idle_time:
                    return True
            else:
                last_activity = time.time()
            
            time.sleep(0.2)
        
        return False


class CookieManager:
    """Cookie 管理器（基于 CDP）"""
    
    @staticmethod
    def get_cookies(web_execute_js_func: Callable, url: Optional[str] = None) -> List[Dict]:
        """
        获取 Cookies
        
        Args:
            web_execute_js_func: web_execute_js 工具函数
            url: 指定 URL（可选，不指定则返回所有）
        
        Returns:
            Cookie 列表
        """
        cdp_cmd = {"cmd": "cookies"}
        result = web_execute_js_func(script=json.dumps(cdp_cmd))
        
        cookies = result.get("cookies", [])
        
        if url:
            # 过滤匹配 URL 的 cookies
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            cookies = [c for c in cookies if domain.endswith(c.get("domain", "").lstrip("."))]
        
        return cookies
    
    @staticmethod
    def set_cookie(web_execute_js_func: Callable, cookie: Dict) -> bool:
        """
        设置 Cookie
        
        Args:
            web_execute_js_func: web_execute_js 工具函数
            cookie: Cookie 字典（需包含 name, value, domain 等）
        
        Returns:
            是否成功
        """
        cdp_cmd = {
            "cmd": "cdp",
            "method": "Network.setCookie",
            "params": cookie
        }
        result = web_execute_js_func(script=json.dumps(cdp_cmd))
        return result.get("ok", False)
    
    @staticmethod
    def clear_cookies(web_execute_js_func: Callable, url: Optional[str] = None) -> bool:
        """
        清除 Cookies
        
        Args:
            web_execute_js_func: web_execute_js 工具函数
            url: 指定 URL（可选）
        
        Returns:
            是否成功
        """
        if url:
            cdp_cmd = {
                "cmd": "cdp",
                "method": "Network.clearBrowserCookies",
                "params": {}
            }
        else:
            cdp_cmd = {
                "cmd": "cdp",
                "method": "Network.clearBrowserCookies",
                "params": {}
            }
        
        result = web_execute_js_func(script=json.dumps(cdp_cmd))
        return result.get("ok", False)

class AntiScrapingStrategy:
    """反爬虫综合策略"""
    
    def __init__(self, web_execute_js_func: Callable):
        """
        初始化
        
        Args:
            web_execute_js_func: web_execute_js 工具函数
        """
        self.web_execute_js = web_execute_js_func
        self.ua_rotator = UserAgentRotator()
        self.delay_manager = RequestDelayManager()
        self.rate_limiter = RateLimiter()
        self.cookie_manager = CookieManager()
        self.waiter = DynamicContentWaiter()
    
    def prepare_request(self, rotate_ua: bool = True):
        """
        请求前准备（UA轮换 + 延迟）
        
        Args:
            rotate_ua: 是否轮换 UA
        """
        # 限流检查
        self.rate_limiter.wait_if_needed()
        
        # UA 轮换
        if rotate_ua:
            ua = self.ua_rotator.get_random()
            self.ua_rotator.set_ua_via_cdp(ua, self.web_execute_js)
            print(f"[AntiScraping] 已设置 UA: {ua[:50]}...")
        
        # 随机延迟
        self.delay_manager.wait()
    
    def safe_navigate(self, url: str, wait_for_idle: bool = True) -> bool:
        """
        安全导航（带反爬虫保护）
        
        Args:
            url: 目标 URL
            wait_for_idle: 是否等待网络空闲
        
        Returns:
            是否成功
        """
        self.prepare_request()
        
        # 导航
        nav_js = "location.href = " + json.dumps(url) + ";"
        self.web_execute_js(script=nav_js)
        
        # 等待加载
        if wait_for_idle:
            success = self.waiter.wait_for_network_idle(self.web_execute_js)
            if not success:
                print("[AntiScraping] 警告: 网络未完全空闲")
        
        return True
    
    def batch_scrape(self, urls: List[str], 
                     process_func: Callable[[str], Dict],
                     max_workers: int = 1) -> List[Dict]:
        """
        批量抓取（带限流和延迟）
        
        Args:
            urls: URL 列表
            process_func: 处理函数（接收 URL，返回结果字典）
            max_workers: 并发数（当前仅支持1）
        
        Returns:
            结果列表
        """
        results = []
        
        for i, url in enumerate(urls, 1):
            print(f"[AntiScraping] 处理 {i}/{len(urls)}: {url}")
            
            self.prepare_request()
            
            try:
                result = process_func(url)
                results.append({"url": url, "success": True, "data": result})
            except Exception as e:
                print(f"[AntiScraping] 错误: {e}")
                results.append({"url": url, "success": False, "error": str(e)})
        
        return results


if __name__ == "__main__":
    # 使用示例
    print("="*60)
    print("反爬虫工具包使用示例")
    print("="*60)
    
    # 示例1: UA 轮换
    print("\n【示例1】User-Agent 轮换")
    ua_rotator = UserAgentRotator()
    print(f"  随机 UA: {ua_rotator.get_random()[:60]}...")
    print(f"  下一个 UA: {ua_rotator.get_next()[:60]}...")
    
    # 示例2: 延迟管理
    print("\n【示例2】请求延迟")
    delay_mgr = RequestDelayManager(min_delay=0.5, max_delay=1.0)
    print("  执行延迟...")
    delay_mgr.wait()
    print("  [OK] 延迟完成")
    
    # 示例3: 限流器
    print("\n【示例3】限流器")
    limiter = RateLimiter(max_requests=5, time_window=10)
    for i in range(7):
        if limiter.acquire():
            print(f"  请求 {i+1}: [OK] 允许")
        else:
            print(f"  请求 {i+1}: [X] 超限")
    
    print("\n" + "="*60)