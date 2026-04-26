"""
ppt_animation.py - PPT动画效果增强模块
依赖: ppt_com_toolkit.py
功能: 入场/强调/退出动画预设、时间轴控制、动画组合
"""
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))
from ppt_com_toolkit import *

# ══════════════════════════════════════════════════════════════
# 动画效果ID常量 (MsoAnimEffect)
# ══════════════════════════════════════════════════════════════
ANIM = {
    # 入场动画
    "appear": 1, "fly_in": 2, "blinds": 3, "box": 4, "checkerboard": 5,
    "diamond": 6, "dissolve": 7, "fade": 10, "flash_once": 11,
    "peek_in": 12, "random_bars": 13, "spiral": 15, "split": 16,
    "stretch": 17, "strips": 18, "swivel": 19, "wipe": 22,
    "zoom": 23, "float_up": 42, "float_down": 43,
    # 强调动画
    "pulse": 26, "color_pulse": 27, "teeter": 28, "spin": 31,
    "grow_shrink": 32, "desaturate": 33, "darken": 34, "lighten": 35,
    "transparency": 36, "bold_flash": 37, "wave": 44,
    # 退出动画 (用entrance ID + exit type)
    "disappear": 1, "fly_out": 2, "fade_out": 10, "zoom_out": 23,
}

TRIGGER = {"on_click": 1, "with_prev": 2, "after_prev": 3}
ANIM_TYPE = {"entrance": 1, "exit": 2, "emphasis": 3, "motion": 4}

# ══════════════════════════════════════════════════════════════
# 核心动画函数
# ══════════════════════════════════════════════════════════════
def add_entrance(slide, shape, effect="fade", trigger="after_prev", 
                 delay=0.0, duration=0.5):
    """入场动画"""
    eid = ANIM.get(effect, 10)
    seq = slide.TimeLine.MainSequence
    eff = seq.AddEffect(Shape=shape, effectId=eid, trigger=TRIGGER.get(trigger, 3))
    eff.Timing.TriggerDelayTime = delay
    eff.Timing.Duration = duration
    return eff

def add_emphasis(slide, shape, effect="pulse", trigger="with_prev",
                 delay=0.0, duration=0.5, repeat=1):
    """强调动画"""
    eid = ANIM.get(effect, 26)
    seq = slide.TimeLine.MainSequence
    eff = seq.AddEffect(Shape=shape, effectId=eid, trigger=TRIGGER.get(trigger, 2))
    eff.EffectType = 3  # emphasis
    eff.Timing.TriggerDelayTime = delay
    eff.Timing.Duration = duration
    if repeat > 1:
        eff.Timing.RepeatCount = repeat
    return eff

def add_exit(slide, shape, effect="fade_out", trigger="after_prev",
             delay=0.0, duration=0.5):
    """退出动画"""
    eid = ANIM.get(effect, 10)
    seq = slide.TimeLine.MainSequence
    eff = seq.AddEffect(Shape=shape, effectId=eid, trigger=TRIGGER.get(trigger, 3))
    eff.EffectType = 2  # exit
    eff.Timing.TriggerDelayTime = delay
    eff.Timing.Duration = duration
    return eff

def add_motion_path(slide, shape, path_type="right", trigger="after_prev",
                    delay=0.0, duration=1.0):
    """路径动画 (path_type: right/left/up/down/circle)"""
    path_ids = {"right": 63, "left": 62, "up": 64, "down": 65, "circle": 54}
    eid = path_ids.get(path_type, 63)
    seq = slide.TimeLine.MainSequence
    eff = seq.AddEffect(Shape=shape, effectId=eid, trigger=TRIGGER.get(trigger, 3))
    eff.EffectType = 4  # motion
    eff.Timing.TriggerDelayTime = delay
    eff.Timing.Duration = duration
    return eff

# ══════════════════════════════════════════════════════════════
# 组合动画
# ══════════════════════════════════════════════════════════════
def add_combo(slide, shape, entrance="fade", emphasis="pulse", exit_effect=None,
              entrance_delay=0, emphasis_delay=0.5, exit_delay=1.0):
    """组合动画：入场+强调+退出"""
    effs = []
    effs.append(add_entrance(slide, shape, entrance, "after_prev", entrance_delay))
    effs.append(add_emphasis(slide, shape, emphasis, "after_prev", emphasis_delay))
    if exit_effect:
        effs.append(add_exit(slide, shape, exit_effect, "after_prev", exit_delay))
    return effs

def stagger_entrance(slide, shapes, effect="fade", interval=0.3, duration=0.5):
    """交错入场：多个形状依次入场"""
    effs = []
    for i, shp in enumerate(shapes):
        eff = add_entrance(slide, shp, effect, "after_prev", i * interval, duration)
        effs.append(eff)
    return effs

# ══════════════════════════════════════════════════════════════
# 演示生成
# ══════════════════════════════════════════════════════════════
def demo_animations(output_path="./ppt_animation_demo.pptx"):
    """生成动画演示PPT"""
    app = open_ppt(visible=False)
    prs = new_prs(app)
    
    # Slide 1: 入场动画
    s1 = add_slide(prs)
    set_bg_solid(s1, 20, 30, 50)
    t1 = add_text(s1, "入场动画演示", 1, 1, 8, 1.5, sz=36, bold=True)
    add_entrance(s1, t1, "fly_in", "on_click", duration=0.8)
    
    box1 = add_rect(s1, 2, 4, 3, 2, fill=(0, 150, 200))
    shape_text(box1, "淡入", sz=20)
    add_entrance(s1, box1, "fade", "after_prev", delay=0.3)
    
    box2 = add_rect(s1, 6, 4, 3, 2, fill=(200, 100, 50))
    shape_text(box2, "缩放", sz=20)
    add_entrance(s1, box2, "zoom", "after_prev", delay=0.3)
    
    # Slide 2: 强调动画
    s2 = add_slide(prs)
    set_bg_solid(s2, 30, 20, 50)
    t2 = add_text(s2, "强调动画演示", 1, 1, 8, 1.5, sz=36, bold=True)
    add_entrance(s2, t2, "appear", "on_click")
    
    box3 = add_rect(s2, 4, 4, 4, 2.5, fill=(100, 50, 150))
    shape_text(box3, "脉冲+旋转", sz=20)
    add_entrance(s2, box3, "fade", "after_prev")
    add_emphasis(s2, box3, "pulse", "after_prev", delay=0.5, repeat=2)
    add_emphasis(s2, box3, "spin", "after_prev", delay=0.3)
    
    # Slide 3: 退出动画
    s3 = add_slide(prs)
    set_bg_solid(s3, 50, 30, 20)
    t3 = add_text(s3, "退出动画演示", 1, 1, 8, 1.5, sz=36, bold=True)
    add_entrance(s3, t3, "appear", "on_click")
    
    box4 = add_rect(s3, 4, 4, 4, 2.5, fill=(200, 80, 80))
    shape_text(box4, "淡出", sz=20)
    add_entrance(s3, box4, "fade", "after_prev")
    add_exit(s3, box4, "fade_out", "after_prev", delay=1.0)
    
    save_and_quit(app, prs, output_path)
    return output_path

if __name__ == "__main__":
    demo_animations()
