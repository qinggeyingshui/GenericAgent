"""
image_search.py — 关键词图片搜索与本地缓存 (R108, 2026-03-26)

使用 loremflickr.com 无需 API Key，按关键词下载图片到本地缓存。
接口:
  search(keyword, width=800, height=600, count=1, cache_dir=None)
  search_one(keyword, width, height) -> 路径字符串或None
注: source.unsplash.com 已停服(503)，改用 loremflickr.com
"""

import os, hashlib, time
import urllib.request, urllib.parse

DEFAULT_CACHE = os.path.normpath(os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "..","temp","image_cache"))


def _cache_path(cache_dir, keyword, width, height, idx):
    safe = urllib.parse.quote(keyword, safe="")
    h = hashlib.md5(f"{safe}_{width}x{height}_{idx}".encode()).hexdigest()[:8]
    return os.path.join(cache_dir, f"img_{h}.jpg")


def search(keyword, width=800, height=600, count=1, cache_dir=None,
           timeout=20, use_cache=True):
    """
    按关键词搜索图片并缓存到本地。
    keyword: 搜索关键词(英文)，多关键词用逗号: "graph,network"
    width, height: 图片尺寸(像素)
    count: 下载数量(1-5)
    cache_dir: 缓存目录，默认 temp/image_cache/
    use_cache: True=有缓存直接返回
    返回: [本地路径, ...] 列表
    """
    if cache_dir is None:
        cache_dir = DEFAULT_CACHE
    os.makedirs(cache_dir, exist_ok=True)
    count = max(1, min(count, 5))
    results = []
    # loremflickr: /宽/高/关键词[,关键词2]?lock=N 返回固定图片
    kw_enc = urllib.parse.quote(keyword.replace(" ", ","))
    for i in range(count):
        fpath = _cache_path(cache_dir, keyword, width, height, i)
        if use_cache and os.path.exists(fpath) and os.path.getsize(fpath) > 5000:
            results.append(fpath)
            print(f"[image_search] 缓存命中: {os.path.basename(fpath)}")
            continue
        url = f"https://loremflickr.com/{width}/{height}/{kw_enc}?lock={i+1}"
        try:
            req = urllib.request.Request(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
            })
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                data = resp.read()
            if len(data) < 5000:
                print(f"[image_search] 警告: 图片{i+1}数据异常({len(data)}B)")
                continue
            with open(fpath, "wb") as f:
                f.write(data)
            results.append(fpath)
            print(f"[image_search] OK: {os.path.basename(fpath)} ({len(data)//1024}KB)")
        except Exception as e:
            print(f"[image_search] 失败 idx={i}: {e}")
        if i < count - 1:
            time.sleep(0.3)
    return results


def search_one(keyword, width=800, height=600, cache_dir=None):
    """便捷函数：下载1张，返回路径或None"""
    r = search(keyword, width=width, height=height, count=1, cache_dir=cache_dir)
    return r[0] if r else None


if __name__ == "__main__":
    import sys
    kw = sys.argv[1] if len(sys.argv) > 1 else "graph,neural,network"
    paths = search(kw, count=2)
    print("结果:", paths)
