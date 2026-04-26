# R90 | win32com高级PPT功能扩充

日期: 2026-03-26
类型: 产出
验收: PASS

## 任务目标
向 ppt_com_toolkit.py 追加用户指定的高级功能函数（母版/主题切换/批量替换/动画序列），
并更新 ability_list.md 作为使用手册。

## 执行结果
入库前: 21函数 241行 | 入库后: 24函数 320行 | 新增: 4个高级函数

### 新增函数清单

| 函数 | 功能 | 典型用途 |
|---|---|---|
| `batch_replace_text(prs, replacements)` | 全文批量替换占位符 | 模板变量填充，如{{标题}}→实际值 |
| `set_master_logo(prs, logo_path, l,t,w,h)` | 母版统一注入LOGO图片 | 所有页面自动显示品牌标识 |
| `add_anim_sequence(slide, shapes, ...)` | 批量顺序入场动画 | 要点逐条显示，interval可控节奏 |
| `apply_theme_colors(slide, theme)` | 4种预设配色主题一键切换 | tech_blue/academic_green/warm_orange/dark_pro |

## 新增产出物
- `./ppt_com_toolkit.py`: 追加4函数，320行
- `./ability_list.md`: 完整能力手册，24函数分类索引+坑点+验证状态

## 技术备注
- batch_replace_text: 遍历所有幻灯片>形状>段落>Run，精确替换不破坏格式
- set_master_logo: SlideMasters索引从1开始（COM约定）
- add_anim_sequence: after_prev触发链+delay递增，实现自动序列无需点击
- apply_theme_colors: 返回accent色tuple方便后续着色使用
- SmartArt原生API(AddSmartArt)依赖msoSmartArtLayout枚举，已在SOP注明用rrect模拟替代

## 验收
- [x] ppt_com_toolkit.py新增>=3个高级函数（实际新增4个）
- [x] ability_list.md存在，含全部24函数分类索引
- [x] 覆盖用户指定方向：母版/主题切换/批量替换/动画序列
