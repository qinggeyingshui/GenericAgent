# PPT母版与主题深度管理

## 产出
- 新增工具: temp/tools/ppt_master_toolkit.py (约350行)
- 更新SOP: ppt_com_sop.md (新增母版模块文档)

## 核心函数 (验收3个母版操作函数 ✓)
1. **母版编辑**: get_master, get_layouts, set_master_background, set_master_gradient, add_master_logo, add_master_text
2. **主题色提取**: extract_theme_colors, extract_slide_colors, save_theme_to_json  
3. **批量应用**: apply_theme_to_master, batch_apply_master, copy_master_elements

## 验证
- demo_master_toolkit() 执行成功
- 提取主题色: background1/text1/accent1-6 共12种
- 母版版式: 11个版式正确识别
- 输出: ppt_lab/demo_master.pptx

## 坑点记录
- 新建PPT无SlideMasters集合，需先添加幻灯片触发母版创建
- 使用prs.SlideMaster(单数)访问默认母版
