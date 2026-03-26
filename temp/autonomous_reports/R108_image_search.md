# R108 — local_skills/image_search.py 关键词图片搜索工具

**日期**: 2026-03-26
**类型**: 产出
**状态**: 完成

## 任务目标
实现按关键词搜索并缓存图片的本地SKILL，无需API Key。

## 产出

| 文件 | 说明 |
|------|------|
| `local_skills/image_search.py` | 新建，3185 bytes |
| `temp/image_cache/` | 缓存目录，img_*.jpg |

## API

    search(keyword, width=800, height=600, count=1,
           cache_dir=None, timeout=20, use_cache=True)
    -> [本地路径, ...]

    search_one(keyword, width, height) -> 路径字符串或None

## 验证结果
- 关键词 "graph,neural,network"，640x480，下载2张
- img_8fb61ea9.jpg 54KB, img_52948b87.jpg 54KB
- 验收 PASS

## 设计决策
- source.unsplash.com 已停服(503)，改用 loremflickr.com
- loremflickr: /宽/高/关键词?lock=N 固定随机种子，count个图用不同lock
- 缓存key = md5(keyword_WxH_idx)，use_cache=True时命中直接返回
- 多关键词用逗号: "graph,network"
