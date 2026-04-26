"""
内容发布自动化工具
支持多平台内容发布，当前实现：微信公众号
"""
from abc import ABC, abstractmethod
from typing import Dict, Optional
import json

class ContentPublisher(ABC):
    """内容发布器基类"""
    
    @abstractmethod
    def publish(self, title: str, content: str, cover_image: Optional[str] = None, **kwargs) -> Dict:
        """发布内容
        
        Args:
            title: 文章标题
            content: 文章正文（HTML格式）
            cover_image: 封面图片路径
            **kwargs: 平台特定参数
            
        Returns:
            {"success": bool, "message": str, "url": str}
        """
        pass

class WechatMPPublisher(ContentPublisher):
    """微信公众号发布器
    
    使用web_execute_js操作微信公众平台
    需要用户已在浏览器登录 https://mp.weixin.qq.com
    """
    
    def __init__(self):
        self.base_url = "https://mp.weixin.qq.com"
        
    def publish(self, title: str, content: str, cover_image: Optional[str] = None, 
                author: str = "", digest: str = "", **kwargs) -> Dict:
        """发布微信公众号图文
        
        Args:
            title: 文章标题
            content: 文章正文（HTML格式）
            cover_image: 封面图片本地路径
            author: 作者
            digest: 摘要
            **kwargs: 其他参数
                - save_only: bool, 仅保存草稿不发布
                
        Returns:
            {"success": bool, "message": str, "article_id": str}
        """
        save_only = kwargs.get('save_only', True)  # 默认仅保存草稿
        
        steps = {
            "navigate": f"导航到 {self.base_url}",
            "new_article": "点击新建图文消息",
            "fill_title": f"填充标题: {title}",
            "fill_author": f"填充作者: {author}",
            "fill_content": "填充正文内容",
            "upload_cover": "上传封面图片" if cover_image else "跳过封面",
            "fill_digest": f"填充摘要: {digest}" if digest else "跳过摘要",
            "save": "保存草稿" if save_only else "发布文章"
        }
        
        return {
            "success": False,
            "message": "需要实际浏览器环境测试，请使用 execute_publish() 方法",
            "steps": steps,
            "requires_login": True,
            "platform": "微信公众号"
        }
    
    def get_publish_script(self, title: str, content: str, cover_image: Optional[str] = None,
                          author: str = "", digest: str = "", save_only: bool = True) -> str:
        """生成发布脚本供web_execute_js调用
        
        Returns:
            JavaScript代码字符串
        """
        # 转义特殊字符
        title_escaped = title.replace("'", "\\'").replace("\n", "\\n")
        content_escaped = content.replace("'", "\\'").replace("\n", "\\n")
        author_escaped = author.replace("'", "\\'")
        digest_escaped = digest.replace("'", "\\'")
        
        script = f"""
// 微信公众号图文发布脚本
(async function() {{
    const result = {{success: false, message: '', steps: []}};
    
    try {{
        // 1. 检查是否在公众平台
        if (!location.href.includes('mp.weixin.qq.com')) {{
            result.message = '请先导航到微信公众平台';
            return result;
        }}
        
        // 2. 点击新建图文消息（如果在首页）
        const newBtn = document.querySelector('[data-name="新建图文消息"], .new-msg__link');
        if (newBtn) {{
            newBtn.click();
            result.steps.push('点击新建图文消息');
            await new Promise(r => setTimeout(r, 2000));
        }}
        
        // 3. 填充标题
        const titleInput = document.querySelector('#title, [placeholder*="标题"]');
        if (titleInput) {{
            titleInput.value = '{title_escaped}';
            titleInput.dispatchEvent(new Event('input', {{bubbles: true}}));
            result.steps.push('填充标题');
        }}
        
        // 4. 填充作者
        if ('{author_escaped}') {{
            const authorInput = document.querySelector('#author, [placeholder*="作者"]');
            if (authorInput) {{
                authorInput.value = '{author_escaped}';
                authorInput.dispatchEvent(new Event('input', {{bubbles: true}}));
                result.steps.push('填充作者');
            }}
        }}
        
        // 5. 填充正文（富文本编辑器）
        const editor = document.querySelector('#edui1_iframeholder iframe');
        if (editor && editor.contentWindow) {{
            const doc = editor.contentWindow.document;
            doc.body.innerHTML = '{content_escaped}';
            result.steps.push('填充正文');
        }}
        
        // 6. 填充摘要
        if ('{digest_escaped}') {{
            const digestInput = document.querySelector('#digest, [placeholder*="摘要"]');
            if (digestInput) {{
                digestInput.value = '{digest_escaped}';
                digestInput.dispatchEvent(new Event('input', {{bubbles: true}}));
                result.steps.push('填充摘要');
            }}
        }}
        
        // 7. 保存或发布
        const saveBtn = document.querySelector('.js_send, [data-name="保存"]');
        if (saveBtn && !{str(save_only).lower()}) {{
            // 仅在非save_only模式下点击发布
            result.steps.push('准备发布（需手动确认）');
        }} else {{
            result.steps.push('内容已填充，请手动保存');
        }}
        
        result.success = true;
        result.message = '内容填充完成';
        
    }} catch(e) {{
        result.message = '执行出错: ' + e.message;
    }}
    
    return result;
}})();
"""
        return script
    
    def get_upload_cover_cdp_commands(self, cover_image_path: str, tab_id: Optional[int] = None) -> Dict:
        """生成上传封面的CDP批量命令
        
        Args:
            cover_image_path: 封面图片绝对路径
            tab_id: 标签页ID（可选）
            
        Returns:
            CDP batch命令字典
        """
        commands = [
            {"cmd": "cdp", "method": "DOM.getDocument", "params": {"depth": 1}},
            {"cmd": "cdp", "method": "DOM.querySelector", "params": {
                "nodeId": "$0.root.nodeId",
                "selector": "input[type=file][accept*=image]"
            }},
            {"cmd": "cdp", "method": "DOM.setFileInputFiles", "params": {
                "nodeId": "$1.nodeId",
                "files": [cover_image_path]
            }}
        ]
        
        batch_cmd = {"cmd": "batch", "commands": commands}
        if tab_id:
            batch_cmd["tabId"] = tab_id
            
        return batch_cmd

def create_wechat_publisher() -> WechatMPPublisher:
    """创建微信公众号发布器实例"""
    return WechatMPPublisher()

# 使用示例

class VideoPublisher(ContentPublisher):
    """短视频发布器基类"""
    
    def publish_video(self, video_path: str, title: str, description: str = "", 
                     cover_image: Optional[str] = None, tags: list = None, 
                     schedule_time: Optional[str] = None, **kwargs) -> Dict:
        """发布短视频"""
        pass

class DouyinPublisher(VideoPublisher):
    """抖音短视频发布器"""
    
    def __init__(self):
        self.base_url = "https://creator.douyin.com"
        
    def publish(self, title: str, content: str, **kwargs) -> Dict:
        return {"success": False, "message": "请使用 publish_video() 方法"}
    
    def publish_video(self, video_path: str, title: str, description: str = "",
                     cover_image: Optional[str] = None, tags: list = None,
                     schedule_time: Optional[str] = None, **kwargs) -> Dict:
        return {
            "success": False,
            "message": "抖音发布需要浏览器环境和登录状态",
            "platform": "抖音",
            "requires_login": True
        }

class KuaishouPublisher(VideoPublisher):
    """快手短视频发布器"""
    
    def __init__(self):
        self.base_url = "https://cp.kuaishou.com"
        
    def publish(self, title: str, content: str, **kwargs) -> Dict:
        return {"success": False, "message": "请使用 publish_video() 方法"}
    
    def publish_video(self, video_path: str, title: str, description: str = "",
                     cover_image: Optional[str] = None, tags: list = None,
                     schedule_time: Optional[str] = None, **kwargs) -> Dict:
        return {
            "success": False,
            "message": "快手发布需要浏览器环境和登录状态",
            "platform": "快手",
            "requires_login": True
        }

class BilibiliPublisher(VideoPublisher):
    """B站视频发布器"""
    
    def __init__(self):
        self.base_url = "https://member.bilibili.com/platform/upload/video/frame"
        
    def publish(self, title: str, content: str, **kwargs) -> Dict:
        return {"success": False, "message": "请使用 publish_video() 方法"}
    
    def publish_video(self, video_path: str, title: str, description: str = "",
                     cover_image: Optional[str] = None, tags: list = None,
                     schedule_time: Optional[str] = None, **kwargs) -> Dict:
        return {
            "success": False,
            "message": "B站发布需要浏览器环境和登录状态",
            "platform": "B站",
            "requires_login": True
        }

def batch_publish_videos(videos: list, platforms: list, **common_kwargs) -> list:
    """批量发布视频到多个平台"""
    publishers = {
        "douyin": DouyinPublisher(),
        "kuaishou": KuaishouPublisher(),
        "bilibili": BilibiliPublisher()
    }
    
    results = []
    for video in videos:
        for platform in platforms:
            if platform not in publishers:
                continue
            publisher = publishers[platform]
            kwargs = {**common_kwargs, **video}
            result = publisher.publish_video(
                video_path=kwargs.get("path"),
                title=kwargs.get("title"),
                description=kwargs.get("description", ""),
                cover_image=kwargs.get("cover_image"),
                tags=kwargs.get("tags"),
                schedule_time=kwargs.get("schedule_time")
            )
            results.append({
                "platform": platform,
                "video": video.get("title"),
                "result": result
            })
    return results

if __name__ == "__main__":
    publisher = create_wechat_publisher()
    
    # 示例1: 获取发布信息
    result = publisher.publish(
        title="测试文章标题",
        content="<p>这是文章正文</p>",
        author="作者名",
        digest="文章摘要",
        save_only=True
    )
    print("发布信息:", json.dumps(result, ensure_ascii=False, indent=2))
    
    # 示例2: 生成JS脚本
    script = publisher.get_publish_script(
        title="测试文章",
        content="<p>正文内容</p>",
        author="作者",
        save_only=True
    )
    print("\n生成的JS脚本长度:", len(script))
    
    # 示例3: 生成封面上传CDP命令
    cdp_cmd = publisher.get_upload_cover_cdp_commands("/path/to/cover.jpg")
    print("\nCDP命令:", json.dumps(cdp_cmd, ensure_ascii=False, indent=2))
