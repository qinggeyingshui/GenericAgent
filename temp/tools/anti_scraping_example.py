"""
反爬虫工具包实际使用示例

演示如何与 web_execute_js 工具集成
"""

import sys
sys.path.insert(0, "./")

from anti_scraping_toolkit import AntiScrapingStrategy


def mock_web_execute_js(script: str, **kwargs):
    """模拟 web_execute_js 工具（实际使用时替换为真实工具）"""
    print(f"[Mock] 执行 JS: {script[:80]}...")
    
    # 模拟返回
    if "Network.setUserAgentOverride" in script:
        return {"ok": True}
    elif "Network.getCookies" in script:
        return {
            "ok": True,
            "result": {
                "cookies": [
                    {"name": "session_id", "value": "abc123", "domain": ".example.com"}
                ]
            }
        }
    elif "Network.clearBrowserCookies" in script:
        return {"ok": True}
    elif "document.querySelector" in script:
        return {"ok": True, "result": True}
    else:
        return {"ok": True}


def example_scraping_task():
    """示例：抓取任务"""
    print("="*60)
    print("反爬虫策略实战示例")
    print("="*60 + "\n")
    
    # 初始化策略
    strategy = AntiScrapingStrategy(mock_web_execute_js)
    
    print("[1] 安全导航到目标页面（自动UA轮换+延迟）")
    strategy.safe_navigate("https://example.com", wait_for_idle=False)
    
    print("\n[2] 等待动态内容加载")
    strategy.waiter.wait_for_element(".product-list", mock_web_execute_js, timeout=2)
    
    print("\n[3] 获取当前 Cookies")
    cookies = strategy.cookie_manager.get_cookies(mock_web_execute_js)
    print(f"  获取到 {len(cookies)} 个 Cookie")
    
    print("\n[4] 批量抓取多个页面")
    urls = [
        "https://example.com/page1",
        "https://example.com/page2",
        "https://example.com/page3",
    ]
    
    def process_page(url):
        print(f"  处理: {url}")
        return {"url": url, "status": "ok"}
    
    results = strategy.batch_scrape(urls, process_page)
    print(f"\n  完成 {len(results)} 个页面抓取")
    
    print("\n" + "="*60)
    print("[OK] 示例完成")
    print("="*60)


if __name__ == "__main__":
    example_scraping_task()