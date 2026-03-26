# phone_sync.py — PC↔手机文件批量同步工具

基于 adb 命令封装，支持 list / pull / push 三种操作。

## 前置条件
- 已安装 adb（Android Debug Bridge）并在PATH中
- 手机开启USB调试，已授权本机

## 用法

### 列出手机目录
    python phone_sync.py list /sdcard/DCIM/Camera
    python phone_sync.py list /sdcard/Download --ext jpg,png

### 手机→本地 (pull)
    python phone_sync.py pull /sdcard/DCIM/Camera ./local_photos
    python phone_sync.py pull /sdcard/Download ./local_dl --ext mp4 --dry

### 本地→手机 (push)
    python phone_sync.py push ./local_files /sdcard/Upload
    python phone_sync.py push ./docs /sdcard/Documents --ext pdf --dry

## 选项
| 选项 | 说明 |
|------|------|
| --ext jpg,mp4 | 仅同步指定扩展名（逗号分隔，无需加点） |
| --dry | 预览模式，列出操作但不实际传输 |
| --device SERIAL | 多设备时指定序列号 |

## 依赖
- 仅标准库 + adb（无需额外pip安装）
- Python 3.8+
