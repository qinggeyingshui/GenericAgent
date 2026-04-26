"""
工具检测与技能类别自动映射
用于在用户交互时自动识别新领域并扩展技能树
"""
import sys
import re
from typing import List, Dict, Optional, Tuple
sys.path.insert(0, "./")

from skill_tree_api import SkillTree


class ToolCategoryMapper:
    """工具到技能类别的自动映射器"""
    
    def __init__(self):
        self.skill_tree = SkillTree()
        
        # 工具到类别的映射表
        self.tool_map = {
            # 视频处理
            "ffmpeg": ("video_editing", "视频剪辑"),
            "moviepy": ("video_editing", "视频剪辑"),
            "opencv": ("computer_vision", "计算机视觉"),
            
            # 图像处理
            "pillow": ("image_processing", "图像处理"),
            "pil": ("image_processing", "图像处理"),
            "imagemagick": ("image_processing", "图像处理"),
            
            # Web自动化
            "selenium": ("web_automation", "Web自动化"),
            "playwright": ("web_automation", "Web自动化"),
            "puppeteer": ("web_automation", "Web自动化"),
            
            # 音频处理
            "pydub": ("audio_processing", "音频处理"),
            "librosa": ("audio_processing", "音频处理"),
            "soundfile": ("audio_processing", "音频处理"),
            
            # 数据分析
            "pandas": ("data_analysis", "数据分析"),
            "numpy": ("data_analysis", "数据分析"),
            "scipy": ("data_analysis", "数据分析"),
            
            # 机器学习
            "sklearn": ("machine_learning", "机器学习"),
            "tensorflow": ("machine_learning", "机器学习"),
            "pytorch": ("machine_learning", "机器学习"),
            "torch": ("machine_learning", "机器学习"),
            
            # 3D建模
            "blender": ("3d_modeling", "3D建模"),
            "trimesh": ("3d_modeling", "3D建模"),
            
            # 游戏开发
            "pygame": ("game_development", "游戏开发"),
            "unity": ("game_development", "游戏开发"),
            
            # 网络安全
            "scapy": ("network_security", "网络安全"),
            "nmap": ("network_security", "网络安全"),
            
            # 区块链
            "web3": ("blockchain", "区块链"),
            "ethers": ("blockchain", "区块链"),
        }
        
        # 关键词到类别的映射（用于任务描述分析）
        self.keyword_map = {
            "视频": ("video_editing", "视频剪辑"),
            "剪辑": ("video_editing", "视频剪辑"),
            "图片": ("image_processing", "图像处理"),
            "图像": ("image_processing", "图像处理"),
            "音频": ("audio_processing", "音频处理"),
            "声音": ("audio_processing", "音频处理"),
            "3D": ("3d_modeling", "3D建模"),
            "建模": ("3d_modeling", "3D建模"),
            "游戏": ("game_development", "游戏开发"),
            "区块链": ("blockchain", "区块链"),
            "加密": ("blockchain", "区块链"),
            "安全": ("network_security", "网络安全"),
            "渗透": ("network_security", "网络安全"),
        }
    
    def detect_tools_from_code(self, code: str) -> List[str]:
        """从代码中检测使用的工具"""
        tools = []
        
        # 检测import语句
        import_pattern = r"import\s+(\w+)|from\s+(\w+)\s+import"
        matches = re.findall(import_pattern, code)
        for match in matches:
            tool = match[0] or match[1]
            if tool.lower() in self.tool_map:
                tools.append(tool.lower())
        
        # 检测命令行工具（如ffmpeg）
        cmd_pattern = r"subprocess\.(?:run|call|Popen)\(['\"]([\w-]+)"
        cmd_matches = re.findall(cmd_pattern, code)
        for cmd in cmd_matches:
            if cmd.lower() in self.tool_map:
                tools.append(cmd.lower())
        
        return list(set(tools))
    
    def detect_category_from_description(self, description: str) -> Optional[Tuple[str, str]]:
        """从任务描述中检测类别"""
        for keyword, (cat_id, cat_name) in self.keyword_map.items():
            if keyword in description:
                return (cat_id, cat_name)
        return None
    
    def auto_expand_skill_tree(self, 
                               task_description: str,
                               code_used: str = "",
                               tools_used: List[str] = None,
                               report_id: str = "") -> Dict:
        """
        自动扩展技能树
        
        Args:
            task_description: 任务描述
            code_used: 使用的代码
            tools_used: 手动指定的工具列表
            report_id: 报告ID
        
        Returns:
            {"expanded": bool, "category": str, "skills_added": [str]}
        """
        result = {
            "expanded": False,
            "category": None,
            "category_name": None,
            "skills_added": []
        }
        
        # 1. 从代码检测工具
        detected_tools = []
        if code_used:
            detected_tools = self.detect_tools_from_code(code_used)
        
        # 2. 合并手动指定的工具
        if tools_used:
            detected_tools.extend([t.lower() for t in tools_used])
        detected_tools = list(set(detected_tools))
        
        # 3. 从工具映射到类别
        category_candidates = {}
        for tool in detected_tools:
            if tool in self.tool_map:
                cat_id, cat_name = self.tool_map[tool]
                if cat_id not in category_candidates:
                    category_candidates[cat_id] = {
                        "name": cat_name,
                        "tools": [],
                        "count": 0
                    }
                category_candidates[cat_id]["tools"].append(tool)
                category_candidates[cat_id]["count"] += 1
        
        # 4. 从任务描述检测类别
        desc_category = self.detect_category_from_description(task_description)
        if desc_category:
            cat_id, cat_name = desc_category
            if cat_id not in category_candidates:
                category_candidates[cat_id] = {
                    "name": cat_name,
                    "tools": [],
                    "count": 1
                }
            else:
                category_candidates[cat_id]["count"] += 1
        
        # 5. 选择最可能的类别（工具数量最多）
        if not category_candidates:
            return result
        
        best_category = max(category_candidates.items(), 
                           key=lambda x: x[1]["count"])
        cat_id, cat_info = best_category
        
        # 6. 检查类别是否已存在
        existing_categories = self.skill_tree.tree["skill_categories"]
        if cat_id in existing_categories:
            result["category"] = cat_id
            result["category_name"] = cat_info["name"]
            return result  # 类别已存在，无需扩展
        
        # 7. 创建新类别
        success = self.skill_tree.add_category(cat_id, cat_info["name"])
        if not success:
            return result
        
        result["expanded"] = True
        result["category"] = cat_id
        result["category_name"] = cat_info["name"]
        
        # 8. 添加基础技能
        if cat_info["tools"]:
            # 为每个工具创建一个技能
            for tool in cat_info["tools"][:3]:  # 最多添加3个技能
                skill_id = f"{tool}_usage"
                skill_name = f"{tool.upper()}使用"
                
                self.skill_tree.add_skill(
                    category=cat_id,
                    skill_id=skill_id,
                    skill_name=skill_name,
                    level="beginner",
                    tools=[tool],
                    gaps=[f"{tool}高级功能", f"{tool}性能优化"]
                )
                result["skills_added"].append(skill_id)
        
        # 9. 更新使用记录
        if report_id and result["skills_added"]:
            self.skill_tree.update_skill_usage(
                cat_id, 
                result["skills_added"][0], 
                report_id
            )
        
        return result


if __name__ == "__main__":
    # 测试用例
    mapper = ToolCategoryMapper()
    
    # 测试1: 从代码检测工具
    code = """
    import ffmpeg
    import moviepy.editor as mp
    
    video = mp.VideoFileClip("input.mp4")
    """
    
    result = mapper.auto_expand_skill_tree(
        task_description="帮我剪辑视频",
        code_used=code,
        report_id="R99"
    )
    
    print("测试1: 视频剪辑任务")
    print(f"  扩展: {result['expanded']}")
    print(f"  类别: {result['category']} - {result['category_name']}")
    print(f"  技能: {result['skills_added']}")