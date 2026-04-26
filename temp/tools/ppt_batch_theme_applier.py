#!/usr/bin/env python3
"""
ppt_batch_theme_applier.py - PPT批量主题应用工具

功能:
1. 批量读取PPT文件
2. 应用指定主题的配色方案
3. 修改标题/正文字体
4. 支持单文件和目录批量处理

依赖: win32com, ppt_theme_manager.py
"""
import os
import sys
import win32com.client
from pathlib import Path
from typing import List, Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(SCRIPT_DIR)
from ppt_theme_manager import ThemeManager

class PPTBatchThemeApplier:
    def __init__(self):
        self.theme_manager = ThemeManager()
        self.ppt_app = None
    
    def _init_ppt_app(self):
        """初始化PowerPoint应用"""
        if self.ppt_app is None:
            self.ppt_app = win32com.client.Dispatch("PowerPoint.Application")
            self.ppt_app.Visible = 1
    
    def _close_ppt_app(self):
        """关闭PowerPoint应用"""
        if self.ppt_app:
            self.ppt_app.Quit()
            self.ppt_app = None
    
    def _hex_to_rgb(self, hex_color: str) -> int:
        """将十六进制颜色转换为RGB整数"""
        hex_color = hex_color.lstrip("#")
        r, g, b = int(hex_color[0:2], 16), int(hex_color[2:4], 16), int(hex_color[4:6], 16)
        return r + (g << 8) + (b << 16)
    
    def apply_theme_to_file(self, ppt_path: str, theme_id: str, output_path: Optional[str] = None) -> bool:
        """应用主题到单个PPT文件"""
        try:
            self._init_ppt_app()
                        # 获取主题配置
            theme = self.theme_manager.get_theme(theme_id)
            if not theme:
                print(f"错误: 主题 {theme_id} 不存在")
                return False
            
            # 打开PPT文件
            ppt_path = os.path.abspath(ppt_path)
            if not os.path.exists(ppt_path):
                print(f"错误: 文件不存在 {ppt_path}")
                return False
            
            print(f"正在处理: {os.path.basename(ppt_path)}")
            presentation = self.ppt_app.Presentations.Open(ppt_path)
            
            # 应用主题配色
            colors = theme["colors"]
            primary_rgb = self._hex_to_rgb(colors["primary"])
            secondary_rgb = self._hex_to_rgb(colors["secondary"])
            accent_rgb = self._hex_to_rgb(colors["accent"])
            text_rgb = self._hex_to_rgb(colors["text"])
            bg_rgb = self._hex_to_rgb(colors["background"])
            
            # 遍历所有幻灯片
            for slide in presentation.Slides:
                # 设置背景颜色
                slide.FollowMasterBackground = 0
                slide.Background.Fill.Solid()
                slide.Background.Fill.ForeColor.RGB = bg_rgb
                
                # 遍历所有形状
                for shape in slide.Shapes:
                    # 处理文本框
                    if shape.HasTextFrame:
                        text_frame = shape.TextFrame
                        if text_frame.HasText:
                            # 设置字体
                            for para in text_frame.TextRange.Paragraphs():
                                para.Font.Name = theme["fonts"]["body"]
                                para.Font.Color.RGB = text_rgb
                                
                                # 标题使用主色
                                if shape.Name.startswith("Title") or "标题" in shape.Name:
                                    para.Font.Color.RGB = primary_rgb
                    
                    # 处理形状填充
                    if shape.Fill.Visible:
                        if shape.Fill.Type == 1:  # msoFillSolid
                            # 根据形状类型应用不同颜色
                            if "Title" in shape.Name or "标题" in shape.Name:
                                shape.Fill.ForeColor.RGB = primary_rgb
                            else:
                                shape.Fill.ForeColor.RGB = accent_rgb
            
            # 保存文件
            if output_path:
                output_path = os.path.abspath(output_path)
                presentation.SaveAs(output_path)
                print(f"已保存到: {output_path}")
            else:
                presentation.Save()
                print(f"已更新原文件")
            
            presentation.Close()
            return True
            
        except Exception as e:
            print(f"处理失败: {e}")
            return False
    
    def batch_apply_theme(self, input_dir: str, theme_id: str, output_dir: Optional[str] = None) -> dict:
        """批量应用主题到目录下所有PPT文件"""
        results = {"success": [], "failed": []}
        
        input_path = Path(input_dir)
        if not input_path.exists():
            print(f"错误: 目录不存在 {input_dir}")
            return results
        
        # 查找所有PPT文件
        ppt_files = list(input_path.glob("*.pptx")) + list(input_path.glob("*.ppt"))
        
        if not ppt_files:
            print(f"警告: 目录下没有找到PPT文件")
            return results
        
        print(f"找到 {len(ppt_files)} 个PPT文件\n")
        
        # 创建输出目录
        if output_dir:
            output_path = Path(output_dir)
            output_path.mkdir(parents=True, exist_ok=True)
        
        # 批量处理
        for ppt_file in ppt_files:
            if output_dir:
                out_file = str(Path(output_dir) / ppt_file.name)
            else:
                out_file = None
            
            success = self.apply_theme_to_file(str(ppt_file), theme_id, out_file)
            
            if success:
                results["success"].append(ppt_file.name)
            else:
                results["failed"].append(ppt_file.name)
        
        return results
    
    def __del__(self):
        """析构函数：确保关闭PowerPoint"""
        self._close_ppt_app()

def main():
    """命令行工具"""
    import argparse
    
    parser = argparse.ArgumentParser(description="PPT批量主题应用工具")
    parser.add_argument("input", help="输入PPT文件或目录")
    parser.add_argument("--theme", "-t", default="academic_blue", help="主题ID（默认: academic_blue）")
    parser.add_argument("--output", "-o", help="输出文件或目录（不指定则覆盖原文件）")
    parser.add_argument("--list-themes", "-l", action="store_true", help="列出所有可用主题")
    
    args = parser.parse_args()
    
    applier = PPTBatchThemeApplier()
    
    # 列出主题
    if args.list_themes:
        print("\n可用主题列表:\n")
        for theme in applier.theme_manager.list_themes():
            print(f"  [{theme[\"id\"]}] {theme[\"name\"]}")
            print(f"      {theme[\"description\"]}\n")
        return
    
    # 处理文件或目录
    input_path = Path(args.input)
    
    if input_path.is_file():
        # 单文件处理
        success = applier.apply_theme_to_file(str(input_path), args.theme, args.output)
        if success:
            print("\n✓ 处理完成")
        else:
            print("\n✗ 处理失败")
    elif input_path.is_dir():
        # 批量处理
        results = applier.batch_apply_theme(str(input_path), args.theme, args.output)
        print(f"\n=== 处理结果 ===")
        print(f"成功: {len(results[\"success\"])} 个")
        print(f"失败: {len(results[\"failed\"])} 个")
        
        if results["failed"]:
            print("\n失败文件:")
            for f in results["failed"]:
                print(f"  - {f}")
    else:
        print(f"错误: 路径不存在 {args.input}")
    
    applier._close_ppt_app()

if __name__ == "__main__":
    main()