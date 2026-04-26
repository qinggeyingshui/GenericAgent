# R81 win32com PPT动画效果API

**日期**: 2026-03-26
**任务类型**: 探测+产出
**状态**: 验收通过

## 任务目标
实现进入/退出/路径动画3类效果，封装add_animation()；输出demo_animation.pptx

## 成果

### 新增函数
`ppt_com_toolkit.py` 追加 `add_animation(slide, shape, anim_type, effect_id, trigger, delay)`

| 参数 | 说明 |
|------|------|
| anim_type | "entrance"(进入)/"exit"(退出)/"path"(路径) |
| effect_id | 不传自动选默认: entrance=1/exit=1/path=64 |
| trigger | "on_click"=1/"with_prev"=2/"after_prev"=3 |
| delay | 触发延迟秒数 |

### 输出文件
- `demo_animation.pptx` (3页)
  - Slide1: 进入动画(Appear) x2，on_click+after_prev
  - Slide2: 退出动画(Exit) x1，on_click
  - Slide3: 路径动画(Path Down) x1，on_click

### effectId参考
| 效果 | effectId |
|------|----------|
| Appear(出现) | 1 |
| Fly In(飞入) | 10 |
| Path Down(向下路径) | 64 |

## 验收结果
| 验收项 | 结果 |
|--------|------|
| demo_animation.pptx存在 | PASS |
| ppt_com_toolkit.py含add_animation | PASS |
| 进入/退出/路径3类动画 | PASS |

## 经验
- app.Quit()在某些环境会抛com_error(-2147352567)，但文件已成功SaveAs，可忽略
- EffectType设置需在AddEffect之后，COM才接受覆盖
- 路径动画effectId=64为PathDown，需PowerPoint支持