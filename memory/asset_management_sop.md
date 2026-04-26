# 素材库管理 SOP

工具：`temp/tools/asset_manager.py`  
数据库：`temp/assets.db`（SQLite）

## 功能概览
- 素材元数据管理（路径/分类/标签/描述/时间）
- 分类和标签体系
- 多维度检索（关键词/分类/标签）
- 批量导入

## 使用方法

### 1. 初始化数据库
```python
from temp.tools.asset_manager import init_db
init_db()  # 首次使用必须调用
```

### 2. 添加素材
```python
from temp.tools.asset_manager import add_asset

# 基础添加
asset_id = add_asset("path/to/file.jpg")

# 完整信息
asset_id = add_asset(
    path="path/to/file.jpg",
    category="图片",
    description="产品宣传图",
    tags=["营销", "2026Q1"]
)
```

### 3. 更新素材
```python
from temp.tools.asset_manager import update_asset

update_asset(
    asset_id=1,
    category="视频",
    description="更新后的描述",
    tags=["新标签1", "新标签2"]
)
```

### 4. 检索素材
```python
from temp.tools.asset_manager import search_assets

# 关键词检索
results = search_assets(keyword="宣传")

# 按分类检索
results = search_assets(category="图片")

# 按标签检索
results = search_assets(tags=["营销", "2026Q1"])

# 组合检索
results = search_assets(
    keyword="产品",
    category="图片",
    tags=["营销"]
)
```

### 5. 批量导入
```python
from temp.tools.asset_manager import batch_import

# 导入目录下所有文件
imported = batch_import(
    directory="path/to/assets",
    category="图片",
    default_tags=["批量导入", "2026"]
)
print(f"导入 {len(imported)} 个文件")
```

### 6. 查看分类和标签
```python
from temp.tools.asset_manager import list_categories, list_tags

categories = list_categories()  # 所有分类
tags = list_tags()              # 所有标签
```

### 7. 删除素材
```python
from temp.tools.asset_manager import delete_asset

delete_asset(asset_id=1)
```

## 数据结构

### 素材表 (assets)
- id: 主键
- path: 文件路径（唯一）
- category: 分类
- description: 描述
- created_at: 创建时间
- updated_at: 更新时间

### 标签表 (tags)
- id: 主键
- name: 标签名（唯一）

### 关联表 (asset_tags)
- asset_id: 素材ID
- tag_id: 标签ID

## 使用场景

### 场景1：管理教学素材
```python
# 导入课件图片
batch_import("./teaching_materials/images", category="教学图片", default_tags=["课件"])

# 检索特定课程素材
results = search_assets(category="教学图片", tags=["数学", "初中"])
```

### 场景2：自媒体素材库
```python
# 添加视频素材
add_asset("videos/intro.mp4", category="视频", tags=["片头", "通用"])

# 检索可用素材
results = search_assets(keyword="片头", category="视频")
```

### 场景3：项目资源管理
```python
# 按项目分类
add_asset("project_a/logo.png", category="设计", tags=["项目A", "Logo"])

# 检索项目资源
results = search_assets(tags=["项目A"])
```

## 注意事项
1. 首次使用必须调用 `init_db()` 初始化数据库
2. 路径必须唯一，重复添加返回 -1
3. 标签自动去重，不区分大小写建议统一命名规范
4. 批量导入会递归扫描子目录
5. 删除素材会同时删除关联的标签关系

## 扩展建议
- 支持文件类型自动识别（图片/视频/音频/文档）
- 添加文件大小和MD5校验
- 支持缩略图生成
- 添加使用频率统计
- 支持素材评分和收藏

[skill_mapping]
category: knowledge_management
skill: asset_management
tools: asset_manager.py
[/skill_mapping]

## [record_on_use]
执行完本SOP后，调用以下命令记录使用情况：
```python
import sys
sys.path.append('../memory')
from autonomous_operation_sop.helper import record_skill_usage
record_skill_usage('asset_management_sop.md')
```
