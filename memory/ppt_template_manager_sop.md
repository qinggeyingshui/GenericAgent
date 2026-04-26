# PPT模板管理 SOP

## 概述
PPT模板管理工具提供模板配置管理和模板市场功能，支持自定义模板样式和批量下载在线模板。

## 工具位置
- 配置管理：`temp/tools/ppt_template_manager.py`
- 模板市场：`temp/ppt_file_manager.py`
- 爬虫工具：`temp/ppt_template_crawler.py`

## 基础用法

### 1. 模板配置管理
```python
from tools.ppt_template_manager import *

# 加载预定义模板
template = load_template("business_blue")

# 保存自定义模板
save_template("my_template", {
    "name": "我的模板",
    "colors": {"primary": [0, 51, 102]},
    "fonts": {"title": {"name": "微软雅黑", "size": 44}}
})

# 应用模板到PPT
from tools.ppt_com_toolkit import PPTToolkit
toolkit = PPTToolkit()
prs = toolkit.create_presentation()
apply_template_to_ppt(prs, template, toolkit)
```

### 2. 模板市场

#### 2.1 爬取模板
使用浏览器自动化从pptsupermarket.com批量下载模板：

**步骤1：打开模板列表页**
```javascript
// 访问网站并进入模板列表
window.location.href = 'https://www.pptsupermarket.com/ppts';
```

**步骤2：提取模板元数据**
```javascript
// 提取所有模板的信息
const cards = document.querySelectorAll('#_ljq1 > div.col-lg-3');
const templates = [];
cards.forEach((card, index) => {
  const link = card.querySelector('a');
  const img = card.querySelector('img');
  if (link && img) {
    templates.push({
      id: index + 1,
      detailUrl: link.href,
      imageUrl: img.src,
      title: img.alt || `模板${index + 1}`
    });
  }
});
// 保存到文件
JSON.stringify({count: templates.length, templates: templates}, null, 2);
```

**步骤3：批量下载PPTX文件**
```python
import json
import urllib.request
import os

# 读取模板数据
with open('./ppt_templates/templates_raw.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# 下载模板（从图片URL推断下载URL）
for i, template in enumerate(data['templates'][:50], 1):
    # 提取图片路径
    image_url = template['imageUrl']
    if 'path=' in image_url:
        image_path = image_url.split('path=')[1]
        # 转换为下载URL：/PIC/ -> /PPT/, .jpg -> .pptx
        download_url = image_path.replace('/PIC/', '/PPT/').replace('.jpg', '.pptx')
        
        # 下载文件
        save_path = f'./ppt_templates/files/template_{i:03d}.pptx'
        urllib.request.urlretrieve(download_url, save_path)
        print(f"[{i}/50] 已下载: {save_path}")
```

**实际案例（2026-04-21）**：
- 网站：pptsupermarket.com
- 爬取数量：60个模板元数据
- 下载数量：50个PPTX文件
- 总大小：248.77 MB
- 耗时：约15分钟（分4批下载避免超时）

#### 2.2 分类管理
```python
from ppt_file_manager import PPTFileManager

manager = PPTFileManager()

# 扫描本地模板
manager.scan_templates()

# 分类模板
manager.categorize_template('template_001', '商务')
manager.categorize_template('template_002', '教育')

# 添加标签
manager.add_tags('template_001', ['蓝色', '简约', '科技'])

# 添加描述
manager.update_description('template_001', '适合商务汇报的简约蓝色模板')
```

#### 2.3 预览和搜索
```python
# 按分类搜索
business_templates = manager.search_templates(category='商务')

# 按关键词搜索
results = manager.search_templates(keyword='科技')

# 按标签搜索
blue_templates = manager.search_templates(tags=['蓝色'])

# 获取统计信息
stats = manager.get_statistics()
print(f"总模板数: {stats['total_templates']}")
print(f"分类分布: {stats['categories']}")
```

#### 2.4 导出使用
```python
# 导出模板到指定位置
manager.export_template('template_001', './my_presentation.pptx')

# 批量导出
for template_id in ['template_001', 'template_002']:
    manager.export_template(template_id, f'./{template_id}.pptx')
```

## 完整工作流示例

### 场景：为商务汇报准备模板
```python
from ppt_file_manager import PPTFileManager

# 1. 初始化管理器
manager = PPTFileManager()
manager.scan_templates()

# 2. 搜索合适的模板
templates = manager.search_templates(
    category='商务',
    keyword='科技'
)

# 3. 查看候选模板
for tid, info in templates.items():
    print(f"{tid}: {info['size_mb']} MB, 标签: {info.get('tags', [])}")

# 4. 选择并导出
manager.export_template('template_005', './商务汇报.pptx')
```

## 模板市场数据结构

### 元数据格式
```json
{
  "templates": {
    "template_001": {
      "file_name": "template_001.pptx",
      "size_mb": 2.5,
      "category": "商务",
      "tags": ["蓝色", "简约"],
      "description": "商务汇报模板",
      "created_at": "2026-04-21"
    }
  }
}
```

## 注意事项
1. 模板文件存储在 `temp/ppt_templates/files/`
2. 元数据保存在 `temp/ppt_templates/metadata.json`
3. 下载模板时注意版权和使用许可
4. 大文件下载可能需要较长时间

## 故障排查
- **下载失败**：检查网络连接，尝试更换下载地址
- **文件损坏**：重新下载或使用备用地址
- **分类错误**：手动调用 `categorize_template()` 修正

[record_on_use]
[skill_mapping]
category: document_generation
skill: ppt_template_management
tools: ppt_template_manager.py, ppt_file_manager.py
[/skill_mapping]