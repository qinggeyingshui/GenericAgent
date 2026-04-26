"""
使用浏览器抓取网页内容，绕过反爬机制
"""
import sys
sys.path.insert(0, "../")

def convert_with_browser(url, timeout=30):
    """使用浏览器抓取网页内容"""
    try:
        from kiro_tools import web_execute_js, web_scan
        import time
        
        # 在新tab打开
        js_code = f"window.open(\"{url}\", \"_blank\"); \"opened\";"
        web_execute_js(js_code)
        time.sleep(3)
        
        # 获取内容
        content = web_scan(text_only=True)
        return content
    except Exception as e:
        print(f"[web2md_browser错误] {url}: {e}")
        return ""

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        print(convert_with_browser(sys.argv[1]))