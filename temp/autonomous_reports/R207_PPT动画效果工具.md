# R207 PPT动画效果工具

## 产出
- `temp/tools/ppt_animation.py` (约150行)
- 更新 `memory/ppt_com_sop.md`

## 功能
| 函数 | 说明 |
|------|------|
| add_entrance | 入场动画(fade/fly_in/zoom等) |
| add_emphasis | 强调动画(pulse/spin/teeter等) |
| add_exit | 退出动画(fade_out/fly_out等) |
| add_motion_path | 路径动画(right/left/up/down/circle) |
| add_combo | 组合动画(入场+强调+退出) |
| stagger_entrance | 交错入场(多形状依次) |

## 验收
✅ 生成 `temp/ppt_animation_demo.pptx` (3页)
- Slide 1: 入场动画(fly_in + fade + zoom)
- Slide 2: 强调动画(pulse + spin)
- Slide 3: 退出动画(fade_out)
