"""
B站视频内容提取器
三层降级策略: 字幕(需登录) → 视频简介 → 评论+弹幕
无需登录即可获取: 视频信息、评论、弹幕
"""
import re
import sys
import json
import requests
from typing import Dict, List, Optional

# Windows GBK终端兼容
if sys.stdout.encoding and sys.stdout.encoding.lower() != 'utf-8':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

BASE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.bilibili.com",
    "Accept-Language": "zh-CN,zh;q=0.9"
}


def get_video_info(bvid: str) -> Optional[Dict]:
    """获取视频基本信息: title/desc/aid/cid/owner/duration/tags"""
    url = f"https://api.bilibili.com/x/web-interface/view?bvid={bvid}"
    try:
        r = requests.get(url, headers=BASE_HEADERS, timeout=10)
        d = r.json()
        if d.get("code") != 0:
            print(f"[B站] 视频信息获取失败: {d.get('message')}")
            return None
        data = d["data"]
        return {
            "bvid": bvid,
            "aid": data["aid"],
            "cid": data["cid"],
            "title": data["title"],
            "desc": data.get("desc", "").strip(),
            "owner": data["owner"]["name"],
            "duration": data.get("duration", 0),
            "view": data.get("stat", {}).get("view", 0),
            "like": data.get("stat", {}).get("like", 0),
            "tags": [t["tag_name"] for t in data.get("tags", [])] if data.get("tags") else [],
        }
    except Exception as e:
        print(f"[B站] 视频信息异常: {e}")
        return None


def get_subtitles(bvid: str, cid: int) -> Optional[str]:
    """尝试获取CC字幕文本（无登录通常返回空）"""
    url = f"https://api.bilibili.com/x/player/v2?bvid={bvid}&cid={cid}"
    try:
        r = requests.get(url, headers=BASE_HEADERS, timeout=10)
        d = r.json()
        subtitles = d.get("data", {}).get("subtitle", {}).get("subtitles", [])
        if not subtitles:
            return None
        # 取第一条字幕（优先中文）
        sub = next((s for s in subtitles if "zh" in s.get("lan", "")), subtitles[0])
        sub_url = sub.get("subtitle_url", "")
        if not sub_url:
            return None
        if sub_url.startswith("//"):
            sub_url = "https:" + sub_url
        r2 = requests.get(sub_url, headers=BASE_HEADERS, timeout=10)
        body = r2.json()
        texts = [item["content"] for item in body.get("body", [])]
        return " ".join(texts)
    except Exception as e:
        print(f"[B站] 字幕获取异常: {e}")
        return None


def get_comments(aid: int, max_n: int = 20) -> List[str]:
    """获取热门评论文本列表"""
    url = f"https://api.bilibili.com/x/v2/reply/main?type=1&oid={aid}&mode=3&next=0&ps={min(max_n,20)}"
    try:
        r = requests.get(url, headers=BASE_HEADERS, timeout=10)
        d = r.json()
        replies = d.get("data", {}).get("replies", []) or []
        return [rep["content"]["message"] for rep in replies[:max_n]]
    except Exception as e:
        print(f"[B站] 评论获取异常: {e}")
        return []


def get_danmaku(cid: int, max_n: int = 200) -> List[str]:
    """获取弹幕文本列表"""
    url = f"https://comment.bilibili.com/{cid}.xml"
    try:
        r = requests.get(url, headers=BASE_HEADERS, timeout=10)
        r.encoding = "utf-8"
        texts = re.findall(r"<d [^>]+>([^<]+)</d>", r.text)
        return texts[:max_n]
    except Exception as e:
        print(f"[B站] 弹幕获取异常: {e}")
        return []


def extract_content(bvid: str, max_comments: int = 20, max_danmaku: int = 100) -> Dict:
    """
    主接口：提取B站视频全部可用文本内容
    返回结构:
    {
        "bvid": str,
        "title": str,
        "owner": str,
        "duration": int,
        "desc": str,          # 视频简介
        "subtitles": str,     # 字幕全文（可能为None）
        "comments": [str],    # 热门评论
        "danmaku": [str],     # 弹幕样本
        "text_summary": str,  # 综合文本摘要（用于调研）
        "source_level": str,  # 内容来源级别
    }
    """
    print(f"[B站] 提取视频内容: {bvid}")

    # Step1: 视频基本信息
    info = get_video_info(bvid)
    if not info:
        return {"bvid": bvid, "error": "视频信息获取失败"}

    result = {**info, "subtitles": None, "comments": [], "danmaku": [], "text_summary": "", "source_level": ""}

    # Step2: 尝试获取字幕（最高质量）
    subs = get_subtitles(bvid, info["cid"])
    if subs:
        result["subtitles"] = subs
        result["source_level"] = "subtitle"
        print(f"[B站] [OK] 字幕获取成功 ({len(subs)} chars)")
    else:
        print("[B站] [!] 无字幕，降级到简介+评论")

    # Step3: 获取评论
    comments = get_comments(info["aid"], max_comments)
    result["comments"] = comments

    # Step4: 获取弹幕
    danmaku = get_danmaku(info["cid"], max_danmaku)
    result["danmaku"] = danmaku

    # Step5: 组合文本摘要
    parts = []
    parts.append(f"【标题】{info['title']}")
    parts.append(f"【UP主】{info['owner']}")

    if subs:
        parts.append(f"【字幕全文】\n{subs[:3000]}")
        result["source_level"] = "subtitle"
    elif info["desc"]:
        parts.append(f"【视频简介】\n{info['desc'][:1000]}")
        result["source_level"] = "desc"

    if comments:
        top_comments = "\n".join(f"- {c[:100]}" for c in comments[:10])
        parts.append(f"【热门评论】\n{top_comments}")
        if not result["source_level"]:
            result["source_level"] = "comments"

    if danmaku:
        dm_sample = " / ".join(danmaku[:30])
        parts.append(f"【弹幕样本】{dm_sample[:500]}")

    result["text_summary"] = "\n\n".join(parts)
    return result


def extract_from_url(url: str) -> Dict:
    """从B站视频URL提取内容，自动解析bvid"""
    m = re.search(r"BV[a-zA-Z0-9]+", url)
    if not m:
        return {"error": f"无法从URL解析bvid: {url}"}
    return extract_content(m.group())


if __name__ == "__main__":
    import sys
    bvid = sys.argv[1] if len(sys.argv) > 1 else "BV14rzQB9EJj"
    result = extract_content(bvid)
    print("\n" + "="*60)
    print(result.get("text_summary", "无内容")[:2000])
    print(f"\n来源级别: {result.get('source_level')}")
    print(f"评论数: {len(result.get('comments',[]))}, 弹幕数: {len(result.get('danmaku',[]))}")