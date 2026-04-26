"""
PPT模板批量下载脚本
配合浏览器自动化批量下载模板
"""
import os
import json
import time
import urllib.request
from pathlib import Path

def download_template(url, save_path, timeout=30):
    """下载单个模板文件"""
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as response:
            with open(save_path, "wb") as f:
                f.write(response.read())
        return True
    except Exception as e:
        print(f"下载失败: {e}")
        return False

def batch_download(templates_data, save_dir="./ppt_templates/files"):
    """批量下载模板"""
    os.makedirs(save_dir, exist_ok=True)
    success_count = 0
    
    for i, template in enumerate(templates_data, 1):
        template_id = template.get("id", i)
        download_url = template.get("download_url")
        
        if not download_url:
            print(f"[{i}] 跳过: 无下载链接")
            continue
        
        filename = f"template_{template_id}.pptx"
        save_path = os.path.join(save_dir, filename)
        
        if os.path.exists(save_path):
            print(f"[{i}] 已存在: {filename}")
            success_count += 1
            continue
        
        print(f"[{i}/{len(templates_data)}] 下载: {filename}")
        if download_template(download_url, save_path):
            success_count += 1
            print(f"  ✓ 成功")
        else:
            print(f"  ✗ 失败")
        
        time.sleep(1)  # 避免请求过快
    
    print(f"\n下载完成: {success_count}/{len(templates_data)}")
    return success_count

if __name__ == "__main__":
    print("批量下载工具已加载")