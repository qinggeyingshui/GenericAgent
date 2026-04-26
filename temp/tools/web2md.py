import sys
import os
import requests

def convert(url, timeout=30):
    """
    将 URL 转换为文本内容。
    优先使用jina.ai，失败时直接抓取HTML并提取文本。
    
    Args:
        url: 目标URL
        timeout: 请求超时时间（秒）
    
    Returns:
        str: 文本内容，失败返回空字符串
    """
    
    # 方案1: 尝试jina.ai（更干净的markdown）
    try:
        jina_url = f"https://r.jina.ai/{url}"
        response = requests.get(jina_url, timeout=timeout)
        response.raise_for_status()
        if len(response.text) > 100:
            return response.text
    except:
        pass  # 静默失败，尝试fallback
    
    # 方案2: 直接抓取HTML
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        # 尝试用BeautifulSoup提取文本
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')
            # 移除script和style标签
            for script in soup(["script", "style"]):
                script.decompose()
            text = soup.get_text(separator='\n', strip=True)
            return text
        except ImportError:
            # BeautifulSoup不可用，返回原始HTML
            return response.text
            
    except Exception as e:
        print(f"[web2md错误] {url}: {e}")
        return ""

if __name__ == "__main__":
    if len(sys.argv) > 1:
        print(convert(sys.argv[1]))