"""
自媒体脚本生成器
基于主题生成视频脚本，支持多种风格
"""
from typing import Dict, List
from enum import Enum

class ScriptStyle(Enum):
    """脚本风格"""
    KNOWLEDGE = "knowledge"  # 知识科普
    ENTERTAINMENT = "entertainment"  # 娱乐搞笑
    EMOTION = "emotion"  # 情感故事

class ScriptGenerator:
    """视频脚本生成器"""
    
    def __init__(self):
        self.templates = self._init_templates()
    
    def _init_templates(self) -> Dict:
        """初始化脚本模板"""
        return {
            ScriptStyle.KNOWLEDGE: {
                "opening": [
                    "大家好，今天我们来聊聊{topic}",
                    "你知道{topic}吗？今天就来深入了解一下",
                    "关于{topic}，很多人都有误解，今天我们来揭秘"
                ],
                "body_intro": "首先，我们需要了解",
                "body_points": ["第一点", "第二点", "第三点", "最后"],
                "closing": [
                    "以上就是关于{topic}的全部内容，希望对你有帮助",
                    "如果你觉得有用，记得点赞关注",
                    "我们下期再见"
                ]
            },
            ScriptStyle.ENTERTAINMENT: {
                "opening": [
                    "兄弟们！今天整个活儿，聊聊{topic}",
                    "哈喽大家好，今天给大家带来{topic}的搞笑解读",
                    "笑死我了，{topic}居然还能这么玩"
                ],
                "body_intro": "话不多说，直接开整",
                "body_points": ["先说第一个笑点", "接着来第二个", "还有更离谱的", "最后压轴"],
                "closing": [
                    "好了，今天的{topic}就到这里",
                    "笑了的扣1，没笑的扣2",
                    "咱们下期见，拜拜"
                ]
            },
            ScriptStyle.EMOTION: {
                "opening": [
                    "有人说，{topic}是人生中最重要的事",
                    "当我们谈论{topic}时，我们在谈论什么",
                    "关于{topic}，我想和你分享一个故事"
                ],
                "body_intro": "让我慢慢讲给你听",
                "body_points": ["故事的开始", "转折来了", "最触动的部分", "结局"],
                "closing": [
                    "这就是{topic}教会我的道理",
                    "希望这个故事能给你一些启发",
                    "如果你也有类似经历，欢迎评论区分享"
                ]
            }
        }
    
    def generate(self, topic: str, style: ScriptStyle, key_points: List[str] = None) -> Dict[str, str]:
        """生成视频脚本
        
        Args:
            topic: 主题
            style: 脚本风格
            key_points: 关键要点列表（可选，默认生成3-4个）
        
        Returns:
            包含opening/body/closing的脚本字典
        """
        template = self.templates[style]
        
        # 生成开头
        opening = template["opening"][0].format(topic=topic)
        
        # 生成正文
        body_parts = []
        body_parts.append(template["body_intro"])
        
        if key_points:
            for i, point in enumerate(key_points):
                label = template["body_points"][min(i, len(template["body_points"])-1)]
                body_parts.append(f"{label}：{point}")
        else:
            # 默认生成占位符
            for label in template["body_points"][:3]:
                body_parts.append(f"{label}：[在此填写具体内容]")
        
        body = "\n\n".join(body_parts)
        
        # 生成结尾
        closing = "\n".join([s.format(topic=topic) for s in template["closing"]])
        
        return {
            "opening": opening,
            "body": body,
            "closing": closing,
            "full_script": f"{opening}\n\n{body}\n\n{closing}"
        }
    
    def generate_multi_style(self, topic: str, key_points: List[str] = None) -> Dict[str, Dict]:
        """生成所有风格的脚本供对比选择"""
        return {
            style.value: self.generate(topic, style, key_points)
            for style in ScriptStyle
        }

def create_script_generator() -> ScriptGenerator:
    """工厂函数"""
    return ScriptGenerator()