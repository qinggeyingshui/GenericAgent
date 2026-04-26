import os
import shutil
import zipfile
from datetime import datetime
import glob
import sys

# 添加路径以导入微信模块
sys.path.insert(0, r'E:\2026\x-fudan\new\GenericAgent')

def backup_logs():
    base_dir = r'E:\2026\x-fudan\new\GenericAgent'
    today = datetime.now().strftime('%m%d')
    folder_name = f'log_{today}_why'
    folder_path = os.path.join(base_dir, folder_name)
    
    # 1. 创建文件夹
    os.makedirs(folder_path, exist_ok=True)
    print(f"创建文件夹: {folder_path}")
    
    # 2. 复制当日日志
    temp_dir = os.path.join(base_dir, 'temp')
    log_pattern = os.path.join(temp_dir, f'model_responses_*.txt')
    log_files = glob.glob(log_pattern)
    
    copied = 0
    for log_file in log_files:
        shutil.copy2(log_file, folder_path)
        copied += 1
    print(f"复制了 {copied} 个日志文件")
    
    # 3. 打包成zip
    zip_path = os.path.join(base_dir, f'{folder_name}.zip')
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, base_dir)
                zipf.write(file_path, arcname)
    print(f"创建zip: {zip_path}")
    
    # 4. 通过微信发送
    try:
        from frontends.wechatapp import send_file
        from memory.global_mem import WX_TO_USER_ID
        send_file(WX_TO_USER_ID, zip_path)
        print("已通过微信发送")
    except Exception as e:
        print(f"微信发送失败: {e}")
    
    return zip_path

if __name__ == '__main__':
    backup_logs()
