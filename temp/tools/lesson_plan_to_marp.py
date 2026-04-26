#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
lesson_plan_to_marp.py
教案Markdown转Marp演示文稿自动化工具

功能：
1. 解析lesson_plan.md结构
2. 自动添加Marp frontmatter
3. 智能分页（按章节/小节）
4. 插入图片/代码块
5. 调用Marp CLI生成PPTX
"""

import os
import re
import subprocess
from pathlib import Path

class LessonPlanToMarp:
    def __init__(self, npx_path=r'E:\nvm\v20.12.2\npx.cmd'):
        self.npx_path = npx_path
        
    def parse_lesson_plan(self, md_file):
        """解析教案Markdown文件"""
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        return content
    
    def convert_to_marp(self, content, theme='default', paginate=True):
        """转换为Marp格式"""
        # 添加Marp frontmatter
        frontmatter = f"""---
marp: true
theme: {theme}
paginate: {str(paginate).lower()}
backgroundColor: #fff
style: |
  section {{
    font-size: 28px;
  }}
  h1 {{
    color: #0066cc;
    font-size: 48px;
  }}
  h2 {{
    color: #0088cc;
    font-size: 40px;
  }}
---

"""
        
        # 在一级标题前添加分页符
        content = re.sub(r'\n(# [^\n]+)', r'\n---\n\n\1', content)
        
        # 在二级标题前添加分页符（可选）
        content = re.sub(r'\n(## [^\n]+)', r'\n---\n\n\1', content)
        
        # 移除开头多余的分页符
        content = re.sub(r'^---\n+', '', content)
        
        return frontmatter + content
    
    def generate_pptx(self, marp_md, output_pptx):
        """调用Marp CLI生成PPTX"""
        cmd = [
            self.npx_path,
            '@marp-team/marp-cli',
            marp_md,
            '-o', output_pptx,
            '--allow-local-files'
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            return True, f"成功生成: {output_pptx}"
        else:
            return False, result.stderr
    
    def process(self, lesson_plan_file, output_dir='./'):
        """完整处理流程"""
        # 读取教案
        content = self.parse_lesson_plan(lesson_plan_file)
        
        # 转换为Marp格式
        marp_content = self.convert_to_marp(content)
        
        # 保存Marp文件
        base_name = Path(lesson_plan_file).stem
        marp_file = os.path.join(output_dir, f"{base_name}_marp.md")
        
        with open(marp_file, 'w', encoding='utf-8') as f:
            f.write(marp_content)
        
        print(f"[OK] Marp文件已生成: {marp_file}")
        
        # 生成PPTX
        pptx_file = os.path.join(output_dir, f"{base_name}.pptx")
        success, msg = self.generate_pptx(marp_file, pptx_file)
        
        if success:
            print(f"[OK] {msg}")
            print(f"  文件大小: {os.path.getsize(pptx_file)} bytes")
        else:
            print(f"[ERROR] 生成失败: {msg}")
        
        return success, marp_file, pptx_file if success else None


if __name__ == '__main__':
    import sys
    
    if len(sys.argv) < 2:
        print("用法: python lesson_plan_to_marp.py <lesson_plan.md> [output_dir]")
        sys.exit(1)
    
    lesson_file = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else './'
    
    converter = LessonPlanToMarp()
    success, marp_file, pptx_file = converter.process(lesson_file, output_dir)
    
    if success:
        print("\n转换完成！")
    else:
        print("\n转换失败，请检查错误信息")
        sys.exit(1)
