"""
多平台学习资源搜索引擎
支持知乎、B站、CSDN、GitHub等平台
"""
import sys
import json
import time
import re
from typing import List, Dict, Optional
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor, as_completed
sys.path.insert(0, "../")

try:
    from local_skills.web2md import convert as web2md_convert
except:
    from tools.web2md import convert as web2md_convert

# B站专用内容提取器
try:
    from temp.bilibili_content import extract_from_url as _bilibili_extract
    _BILIBILI_EXTRACTOR_AVAILABLE = True
except ImportError:
    try:
        sys.path.insert(0, "./")
        from bilibili_content import extract_from_url as _bilibili_extract
        _BILIBILI_EXTRACTOR_AVAILABLE = True
    except ImportError:
        _BILIBILI_EXTRACTOR_AVAILABLE = False


class MultiPlatformSearch:
    """多平台学习资源搜索"""
    
    def __init__(self):
        self.platforms = {
            "zhihu": {
                "name": "知乎",
                "search_url": "https://www.zhihu.com/search?type=content&q={query}",
                "priority": 1
            },
            "bilibili": {
                "name": "B站",
                "search_url": "https://search.bilibili.com/all?keyword={query}",
                "priority": 2
            },
            "csdn": {
                "name": "CSDN",
                "search_url": "https://so.csdn.net/so/search?q={query}",
                "priority": 3
            },
            "github": {
                "name": "GitHub",
                "search_url": "https://github.com/search?q={query}&type=repositories",
                "priority": 4
            }
        }
    
    def search(self, 
               query: str, 
               platforms: List[str] = None,
               max_results: int = 5) -> Dict[str, List[Dict]]:
        """
        多平台搜索
        
        Args:
            query: 搜索关键词
            platforms: 平台列表，默认全部
            max_results: 每个平台最多返回结果数
        
        Returns:
            {
                "zhihu": [{"title": str, "url": str, "snippet": str}],
                "bilibili": [...],
                ...
            }
        """
        if platforms is None:
            platforms = list(self.platforms.keys())
        
        results = {}
        
        # 并行搜索所有平台
        with ThreadPoolExecutor(max_workers=len(platforms)) as executor:
            future_to_platform = {
                executor.submit(self._search_platform, platform, query, max_results): platform
                for platform in platforms if platform in self.platforms
            }
            
            for future in as_completed(future_to_platform):
                platform = future_to_platform[future]
                try:
                    results[platform] = future.result()
                except Exception as e:
                    print(f"[警告] {platform}搜索失败: {e}")
                    results[platform] = []
        
        return results
    
    def _search_platform(self, 
                        platform: str, 
                        query: str,
                        max_results: int) -> List[Dict]:
        """单平台搜索（使用Google搜索特定站点）"""
        
        # 构建站点限定搜索
        site_map = {
            "zhihu": "site:zhihu.com",
            "bilibili": "site:bilibili.com",
            "csdn": "site:csdn.net",
            "github": "site:github.com"
        }
        
        site_query = f"{query} {site_map.get(platform, '')}"
        google_url = f"https://www.google.com/search?q={quote(site_query)}&num={max_results}"
        
        # 使用web2md获取搜索结果
        try:
            md_content = web2md_convert(google_url)
            results = self._parse_google_results(md_content, platform)
            return results[:max_results]
        except Exception as e:
            print(f"[错误] 搜索{platform}失败: {e}")
            return []
    
    def _parse_google_results(self, md_content: str, platform: str) -> List[Dict]:
        """解析Google搜索结果的markdown"""
        results = []
        
        # 简单解析：查找链接和标题
        lines = md_content.split("\n")
        current_item = {}
        
        for line in lines:
            # 检测标题（通常是链接）
            if line.startswith("[") and "](" in line:
                if current_item:
                    results.append(current_item)
                
                # 提取标题和URL
                try:
                    title_end = line.index("](")
                    url_end = line.index(")", title_end)
                    title = line[1:title_end]
                    url = line[title_end+2:url_end]
                    
                    current_item = {
                        "title": title,
                        "url": url,
                        "snippet": "",
                        "platform": platform
                    }
                except:
                    pass
            
            # 收集描述片段
            elif current_item and line.strip() and not line.startswith("#"):
                current_item["snippet"] += line.strip() + " "
        
        if current_item:
            results.append(current_item)
        
        return results
    
    def fetch_content(self, url: str) -> str:
        """获取页面完整内容（markdown格式）"""
        try:
            return web2md_convert(url)
        except Exception as e:
            return f"[错误] 无法获取内容: {e}"

    def fetch_bilibili_content(self, url: str) -> Dict:
        """
        B站专用内容提取（优于通用web2md）
        返回结构化内容: title/desc/comments/danmaku/text_summary/source_level
        """
        if not _BILIBILI_EXTRACTOR_AVAILABLE:
            return {"text_summary": self.fetch_content(url), "source_level": "web2md_fallback"}
        # 提取bvid
        m = re.search(r"BV[a-zA-Z0-9]+", url)
        if not m:
            return {"text_summary": self.fetch_content(url), "source_level": "web2md_fallback"}
        try:
            result = _bilibili_extract(url)
            return result
        except Exception as e:
            print(f"[B站] 专用提取失败，降级web2md: {e}")
            return {"text_summary": self.fetch_content(url), "source_level": "web2md_fallback"}
    
    def search_and_fetch(self,
                        query: str,
                        platforms: List[str] = None,
                        fetch_top_n: int = 3) -> Dict:
        """
        搜索并获取前N个结果的完整内容
        
        Returns:
            {
                "query": str,
                "results": [
                    {
                        "platform": str,
                        "title": str,
                        "url": str,
                        "content": str  # markdown格式
                    }
                ]
            }
        """
        # 1. 搜索
        search_results = self.search(query, platforms, max_results=5)
        
        # 2. 收集所有结果并按优先级排序
        all_results = []
        for platform, items in search_results.items():
            priority = self.platforms[platform]["priority"]
            for item in items:
                item["priority"] = priority
                all_results.append(item)
        
        all_results.sort(key=lambda x: x["priority"])
        
        # 3. 获取前N个的完整内容
        fetched_results = []
        for item in all_results[:fetch_top_n]:
            print(f"[获取] {item['title'][:50]}...")
            content = self.fetch_content(item["url"])
            
            fetched_results.append({
                "platform": item["platform"],
                "title": item["title"],
                "url": item["url"],
                "snippet": item["snippet"],
                "content": content
            })
            
            time.sleep(2)  # 避免请求过快
        
        return {
            "query": query,
            "total_found": len(all_results),
            "fetched": len(fetched_results),
            "results": fetched_results
        }


if __name__ == "__main__":
    # 测试
    searcher = MultiPlatformSearch()
    
    # 测试1: 基础搜索
    print("=== 测试1: 搜索Python异步编程 ===\n")
    results = searcher.search("Python异步编程教程", platforms=["zhihu"], max_results=3)
    
    for platform, items in results.items():
        print(f"\n{platform}:")
        for i, item in enumerate(items, 1):
            print(f"  {i}. {item['title'][:50]}")
            print(f"     {item['url']}")