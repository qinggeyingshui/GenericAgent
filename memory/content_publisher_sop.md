# 内容发布自动化 SOP

## 概述
内容发布工具支持多平台内容发布，包括微信公众号图文和短视频平台（抖音/快手/B站）。

## 工具位置
- 发布工具：`temp/tools/content_publisher.py`
- 相关工具：`platform_adapter.py`, `ai_copywriter.py`

## 基础用法

### 1. 微信公众号图文发布

```python
from tools.content_publisher import WechatMPPublisher

publisher = WechatMPPublisher()
result = publisher.publish(
    title="文章标题",
    content="<p>文章正文HTML</p>",
    author="作者名",
    digest="文章摘要",
    cover_image="./cover.jpg",
    save_only=True  # True=仅保存草稿，False=发布
)
```

### 2. 短视频发布

#### 2.1 单个视频发布

**抖音发布**：
```python
from tools.content_publisher import DouyinPublisher

publisher = DouyinPublisher()
result = publisher.publish_video(
    video_path="./video.mp4",
    title="视频标题",
    description="视频描述",
    cover_image="./cover.jpg",
    tags=["标签1", "标签2"],
    schedule_time="2026-04-21 18:00"  # 定时发布
)
```

**快手发布**：
```python
from tools.content_publisher import KuaishouPublisher

publisher = KuaishouPublisher()
result = publisher.publish_video(
    video_path="./video.mp4",
    title="视频标题",
    description="视频描述"
)
```

**B站发布**：
```python
from tools.content_publisher import BilibiliPublisher

publisher = BilibiliPublisher()
result = publisher.publish_video(
    video_path="./video.mp4",
    title="视频标题",
    description="视频简介",
    tags=["标签1", "标签2"]
)
```

#### 2.2 批量发布到多平台

```python
from tools.content_publisher import batch_publish_videos

# 准备视频列表
videos = [
    {
        "path": "./video1.mp4",
        "title": "视频1标题",
        "description": "视频1描述",
        "tags": ["科技", "教程"]
    },
    {
        "path": "./video2.mp4",
        "title": "视频2标题",
        "description": "视频2描述",
        "tags": ["生活", "分享"]
    },
    {
        "path": "./video3.mp4",
        "title": "视频3标题",
        "description": "视频3描述"
    }
]

# 批量发布到多个平台
results = batch_publish_videos(
    videos=videos,
    platforms=["douyin", "kuaishou", "bilibili"]
)

# 查看结果
for r in results:
    print(f"{r['platform']}: {r['video']} - {r['result']['message']}")
```

#### 2.3 定时发布

```python
# 设置定时发布时间
result = publisher.publish_video(
    video_path="./video.mp4",
    title="定时发布的视频",
    schedule_time="2026-04-21 20:00"  # 格式: YYYY-MM-DD HH:MM
)
```

## 浏览器自动化实现

由于短视频平台需要登录状态和复杂的上传流程，实际发布需要使用浏览器自动化：

### 步骤1：登录平台
```python
# 使用web_scan打开创作者平台
# 抖音: https://creator.douyin.com
# 快手: https://cp.kuaishou.com
# B站: https://member.bilibili.com
```

### 步骤2：上传视频
使用CDP协议上传文件（参考tmwebdriver_sop.md）

### 步骤3：填充信息
```javascript
// 使用web_execute_js填充标题、描述、标签
document.querySelector('#title').value = '视频标题';
document.querySelector('#description').value = '视频描述';
```

### 步骤4：设置定时发布
```javascript
// 选择定时发布选项
document.querySelector('[data-type="schedule"]').click();
// 设置时间
document.querySelector('#schedule-time').value = '2026-04-21 18:00';
```

### 步骤5：提交发布
```javascript
// 点击发布按钮
document.querySelector('.publish-btn').click();
```

## 数据回传

发布后获取视频数据：
```python
# 返回结果包含
{
    "success": True/False,
    "message": "发布状态",
    "platform": "平台名称",
    "video_id": "视频ID",  # 发布成功后返回
    "url": "视频链接",     # 发布成功后返回
    "requires_login": True/False
}
```

## 完整工作流示例

### 场景：批量发布3个视频到抖音/快手/B站

```python
from tools.content_publisher import batch_publish_videos

# 1. 准备视频
videos = [
    {"path": "./video1.mp4", "title": "教程1", "description": "描述1"},
    {"path": "./video2.mp4", "title": "教程2", "description": "描述2"},
    {"path": "./video3.mp4", "title": "教程3", "description": "描述3"}
]

# 2. 批量发布
results = batch_publish_videos(
    videos=videos,
    platforms=["douyin", "kuaishou", "bilibili"],
    tags=["教程", "分享"]  # 所有视频共用的标签
)

# 3. 统计结果
success_count = sum(1 for r in results if r['result'].get('success'))
print(f"成功发布: {success_count}/{len(results)}")
```

## 注意事项

1. **登录状态**：短视频发布需要在浏览器中保持登录状态
2. **文件大小**：注意各平台的视频大小限制（通常<2GB）
3. **审核时间**：发布后需要平台审核，通常1-24小时
4. **频率限制**：避免短时间内大量发布，可能触发限流
5. **版权问题**：确保视频内容符合平台规范

## 故障排查

- **上传失败**：检查网络连接和文件格式
- **登录过期**：重新登录创作者平台
- **审核不通过**：检查内容是否违规

## 权限说明

当前实现为框架版本，实际上传需要：
- 浏览器环境（web_scan + web_execute_js）
- 平台登录状态
- CDP文件上传支持（参考tmwebdriver_sop.md）

[record_on_use]
[skill_mapping]
category: content_creation
skill: content_publishing
tools: content_publisher.py
[/skill_mapping]
