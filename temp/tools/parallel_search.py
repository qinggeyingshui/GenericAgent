#!/usr/bin/env python3
"""
并行多引擎搜索工具
支持GitHub、DuckDuckGo、Brave、Serper等搜索引擎
From: GenericAgent/temp/parallel_search.py
Version: 1.0.0 (2026-04-16)
"""
import requests
import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import List, Dict, Any, Optional
from datetime import datetime
import time

class ParallelSearch:
    def __init__(self, brave_key: Optional[str] = None, serper_key: Optional[str] = None, github_token: Optional[str] = None):
        self.brave_key = brave_key
        self.serper_key = serper_key
        self.github_token = github_token
        self.timeout = 15
        self.max_retries = 2
        
    def search_github(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """搜索GitHub仓库"""
        try:
            headers = {"Accept": "application/vnd.github.v3+json"}
            if self.github_token:
                headers["Authorization"] = f"token {self.github_token}"
            
            url = "https://api.github.com/search/repositories"
            params = {"q": query, "sort": "stars", "order": "desc", "per_page": max_results}
            
            resp = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            
            results = []
            for item in data.get("items", [])[:max_results]:
                results.append({
                    "title": item["full_name"],
                    "url": item["html_url"],
                    "description": item.get("description", ""),
                    "stars": item["stargazers_count"],
                    "updated": item["updated_at"]
                })
            
            return {"engine": "github", "success": True, "results": results, "count": len(results)}
        except Exception as e:
            return {"engine": "github", "success": False, "error": str(e), "results": []}
    
    def search_duckduckgo(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """搜索DuckDuckGo (使用HTML解析)"""
        try:
            url = "https://html.duckduckgo.com/html/"
            data = {"q": query}
            headers = {"User-Agent": "Mozilla/5.0"}
            
            resp = requests.post(url, data=data, headers=headers, timeout=self.timeout)
            resp.raise_for_status()
            
            # 简单HTML解析提取结果
            from html.parser import HTMLParser
            
            class DDGParser(HTMLParser):
                def __init__(self):
                    super().__init__()
                    self.results = []
                    self.current_result = {}
                    self.in_result = False
                    self.in_title = False
                    
                def handle_starttag(self, tag, attrs):
                    attrs_dict = dict(attrs)
                    if tag == "a" and attrs_dict.get("class") == "result__a":
                        self.in_title = True
                        self.current_result["url"] = attrs_dict.get("href", "")
                        
                def handle_data(self, data):
                    if self.in_title:
                        self.current_result["title"] = data.strip()
                        
                def handle_endtag(self, tag):
                    if tag == "a" and self.in_title:
                        self.in_title = False
                        if self.current_result.get("title"):
                            self.results.append(self.current_result.copy())
                        self.current_result = {}
            
            parser = DDGParser()
            parser.feed(resp.text)
            
            return {"engine": "duckduckgo", "success": True, "results": parser.results[:max_results], "count": len(parser.results[:max_results])}
        except Exception as e:
            return {"engine": "duckduckgo", "success": False, "error": str(e), "results": []}
    
    def search_brave(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """搜索Brave (需要API key)"""
        if not self.brave_key:
            return {"engine": "brave", "success": False, "error": "API key not provided", "results": []}
        
        try:
            url = "https://api.search.brave.com/res/v1/web/search"
            headers = {"Accept": "application/json", "X-Subscription-Token": self.brave_key}
            params = {"q": query, "count": max_results}
            
            resp = requests.get(url, headers=headers, params=params, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            
            results = []
            for item in data.get("web", {}).get("results", [])[:max_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("url", ""),
                    "description": item.get("description", "")
                })
            
            return {"engine": "brave", "success": True, "results": results, "count": len(results)}
        except Exception as e:
            return {"engine": "brave", "success": False, "error": str(e), "results": []}
    
    def search_serper(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        """搜索Serper/Google (需要API key)"""
        if not self.serper_key:
            return {"engine": "serper", "success": False, "error": "API key not provided", "results": []}
        
        try:
            url = "https://google.serper.dev/search"
            headers = {"X-API-KEY": self.serper_key, "Content-Type": "application/json"}
            payload = {"q": query, "num": max_results}
            
            resp = requests.post(url, headers=headers, json=payload, timeout=self.timeout)
            resp.raise_for_status()
            data = resp.json()
            
            results = []
            for item in data.get("organic", [])[:max_results]:
                results.append({
                    "title": item.get("title", ""),
                    "url": item.get("link", ""),
                    "description": item.get("snippet", "")
                })
            
            return {"engine": "serper", "success": True, "results": results, "count": len(results)}
        except Exception as e:
            return {"engine": "serper", "success": False, "error": str(e), "results": []}
    
    def parallel_search(self, query: str, engines: List[str] = None, max_results: int = 5) -> Dict[str, Any]:
        """并行搜索多个引擎"""
        if engines is None:
            engines = ["github", "duckduckgo"]
            if self.brave_key:
                engines.append("brave")
            if self.serper_key:
                engines.append("serper")
        
        engine_map = {
            "github": self.search_github,
            "duckduckgo": self.search_duckduckgo,
            "brave": self.search_brave,
            "serper": self.search_serper
        }
        
        start_time = time.time()
        all_results = {}
        
        with ThreadPoolExecutor(max_workers=len(engines)) as executor:
            future_to_engine = {
                executor.submit(engine_map[eng], query, max_results): eng 
                for eng in engines if eng in engine_map
            }
            
            for future in as_completed(future_to_engine):
                engine = future_to_engine[future]
                try:
                    result = future.result()
                    all_results[engine] = result
                except Exception as e:
                    all_results[engine] = {"engine": engine, "success": False, "error": str(e), "results": []}
        
        elapsed = time.time() - start_time
        
        # 聚合结果
        aggregated = self._aggregate_results(all_results)
        
        return {
            "query": query,
            "engines": engines,
            "elapsed_seconds": round(elapsed, 2),
            "timestamp": datetime.now().isoformat(),
            "raw_results": all_results,
            "aggregated": aggregated
        }
    
    def _aggregate_results(self, raw_results: Dict[str, Any]) -> Dict[str, Any]:
        """聚合和去重结果"""
        all_items = []
        seen_urls = set()
        
        for engine, data in raw_results.items():
            if data.get("success"):
                for item in data.get("results", []):
                    url = item.get("url", "")
                    if url and url not in seen_urls:
                        seen_urls.add(url)
                        item["source_engine"] = engine
                        all_items.append(item)
        
        # 按来源引擎优先级排序 (GitHub > Serper > Brave > DuckDuckGo)
        priority = {"github": 0, "serper": 1, "brave": 2, "duckduckgo": 3}
        all_items.sort(key=lambda x: priority.get(x.get("source_engine", ""), 99))
        
        success_count = sum(1 for d in raw_results.values() if d.get("success"))
        
        return {
            "total_results": len(all_items),
            "engines_succeeded": success_count,
            "engines_failed": len(raw_results) - success_count,
            "results": all_items
        }

def search(query: str, engines: List[str] = None, max_results: int = 5, 
           brave_key: str = None, serper_key: str = None, github_token: str = None) -> Dict[str, Any]:
    """便捷搜索函数"""
    searcher = ParallelSearch(brave_key=brave_key, serper_key=serper_key, github_token=github_token)
    return searcher.parallel_search(query, engines=engines, max_results=max_results)

if __name__ == "__main__":
    # 测试
    result = search("python async web scraping", engines=["github", "duckduckgo"], max_results=3)
    print(json.dumps(result, indent=2, ensure_ascii=False))
