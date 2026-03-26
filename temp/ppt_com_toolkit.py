"""
ppt_com_toolkit.py — PowerPoint COM 驱动工具库
覆盖：纯色/渐变背景、文本框、形状、图片、表格、过渡动画、进入动画
"""
import os
import win32com.client as win32

def rgb(r, g, b):
    """Python (R,G,B) → COM BGR int"""
    return r + (g << 8) + (b << 16)

PT = 72 / 2.54  # 1cm → points
def cm(v): return v * PT

PP_BLANK         = 12
PP_TITLE_SLIDE   = 1
PP_SAVE_PPTX     = 24
MSO_HORIZONTAL   = 1
ALIGN   = {"left":1,"center":2,"right":3,"justify":4}
ANCHOR  = {"top":1,"middle":3,"bottom":4}

# ── 生命周期 ──────────────────────────────────────────
def open_ppt(visible=False):
    """visible=False 时不设置 Visible（COM 不允许隐藏窗口），True 时显示"""
    app = win32.Dispatch("PowerPoint.Application")
    if visible:
        app.Visible = True
    return app

def new_prs(app):
    return app.Presentations.Add(WithWindow=False)

def save_and_quit(app, prs, path):
    abs_path = os.path.abspath(path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    prs.SaveAs(abs_path, PP_SAVE_PPTX)
    print(f"[COM] 已保存: {abs_path}")
    prs.Saved = True
    try: prs.Close()
    except: pass
    app.Quit()
    print("[COM] 已退出")

# ── 幻灯片 ────────────────────────────────────────────
def add_slide(prs, layout=PP_BLANK):
    return prs.Slides.Add(prs.Slides.Count + 1, layout)

def set_bg_solid(slide, r, g, b):
    bg = slide.Background
    bg.Fill.Solid()
    bg.Fill.ForeColor.RGB = rgb(r, g, b)

def set_bg_gradient(slide, r1,g1,b1, r2,g2,b2, style=3, variant=1):
    """
    style: 1=水平, 2=垂直, 3=对角线向下, 4=对角线向上, 5=从角落, 7=从中心
    variant: 1-4 控制渐变变体
    """
    bg = slide.Background
    bg.Fill.TwoColorGradient(style, variant)
    bg.Fill.ForeColor.RGB = rgb(r1,g1,b1)
    bg.Fill.BackColor.RGB = rgb(r2,g2,b2)

def set_transition(slide, effect=3845, speed=2):
    """
    有效 EntryEffect 枚举值（实测 PowerPoint 16）：
      0    = 无
      257  = 切换 (Cut)
      258  = 随机
      3845 = 淡入淡出 (Fade)
      3846 = 推进 (Push)
      3847 = 擦除 (Wipe)
      3848 = 分割 (Split)
      3849 = 显现 (Reveal)
      3850 = 随机线条
      3851 = 形状 (Shape)
      3852 = 展开 (Uncover)
      3853 = 覆盖 (Cover)
      3854 = 闪光 (Flash)
      3855 = 条纹
      3856 = 蜂巢
      3857 = 闪烁
      3858 = 涡流 (Vortex)
      3859 = 碎片 (Shred)
    speed: 1=慢,2=中,3=快
    """
    slide.SlideShowTransition.EntryEffect = effect
    slide.SlideShowTransition.Speed = speed
    slide.SlideShowTransition.AdvanceOnTime = False

# ── 文本框 ────────────────────────────────────────────
def add_text(slide, text, l, t, w, h,
             sz=20, bold=False, italic=False,
             color=(255,255,255), align="left",
             font="微软雅黑", v_anchor="top", wrap=True):
    tb = slide.Shapes.AddTextbox(MSO_HORIZONTAL, cm(l), cm(t), cm(w), cm(h))
    tf = tb.TextFrame
    tf.WordWrap = -1 if wrap else 0
    tf.AutoSize = 0
    tr = tf.TextRange
    tr.Text = text
    tr.Font.Size = sz; tr.Font.Bold = bold; tr.Font.Italic = italic
    tr.Font.Name = font
    r,g,b = color; tr.Font.Color.RGB = rgb(r,g,b)
    tr.ParagraphFormat.Alignment = ALIGN.get(align, 1)
    tf.VerticalAnchor = ANCHOR.get(v_anchor, 1)
    return tb

def add_text_lines(slide, lines, l, t, w, h,
                   sizes=None, bolds=None, colors=None,
                   align="left", font="微软雅黑", spacing=8):
    """多段落多样式文本框"""
    tb = slide.Shapes.AddTextbox(MSO_HORIZONTAL, cm(l), cm(t), cm(w), cm(h))
    tf = tb.TextFrame; tf.WordWrap = -1; tf.AutoSize = 0
    for i, line in enumerate(lines):
        if i == 0:
            para = tf.TextRange.Paragraphs(1)
        else:
            tf.TextRange.InsertAfter("\r")
            para = tf.TextRange.Paragraphs(i+1)
        para.Text = line
        para.Font.Size = sizes[i] if sizes and i<len(sizes) else 18
        para.Font.Bold = bolds[i] if bolds and i<len(bolds) else False
        para.Font.Name = font
        clr = colors[i] if colors and i<len(colors) else (255,255,255)
        r,g,b = clr; para.Font.Color.RGB = rgb(r,g,b)
        para.ParagraphFormat.SpaceAfter = spacing
        para.ParagraphFormat.Alignment  = ALIGN.get(align,1)
    return tb

# ── 形状 ──────────────────────────────────────────────
def add_rect(slide, l, t, w, h, fill=(0,180,216), line=None, lw=0):
    shp = slide.Shapes.AddShape(1, cm(l), cm(t), cm(w), cm(h))
    r,g,b = fill; shp.Fill.Solid(); shp.Fill.ForeColor.RGB = rgb(r,g,b)
    if line: lr,lg,lb=line; shp.Line.ForeColor.RGB=rgb(lr,lg,lb); shp.Line.Weight=lw
    else: shp.Line.Visible = False
    return shp

def add_rrect(slide, l, t, w, h, fill=(0,119,150), corner=0.1):
    shp = slide.Shapes.AddShape(5, cm(l), cm(t), cm(w), cm(h))
    r,g,b = fill; shp.Fill.Solid(); shp.Fill.ForeColor.RGB = rgb(r,g,b)
    shp.Line.Visible = False
    try: shp.Adjustments(1).Value = corner
    except: pass
    return shp

def add_oval(slide, l, t, w, h, fill=(0,180,216)):
    shp = slide.Shapes.AddShape(9, cm(l), cm(t), cm(w), cm(h))
    r,g,b = fill; shp.Fill.Solid(); shp.Fill.ForeColor.RGB = rgb(r,g,b)
    shp.Line.Visible = False
    return shp

def add_line_shape(slide, x1,y1, x2,y2, color=(0,180,216), weight=1.5):
    ln = slide.Shapes.AddLine(cm(x1),cm(y1),cm(x2),cm(y2))
    r,g,b = color; ln.Line.ForeColor.RGB = rgb(r,g,b); ln.Line.Weight = weight
    return ln

def shape_text(shp, text, sz=16, bold=False,
               color=(255,255,255), align="center", font="微软雅黑"):
    tf = shp.TextFrame; tf.WordWrap = -1
    tr = tf.TextRange; tr.Text = text
    tr.Font.Size=sz; tr.Font.Bold=bold; tr.Font.Name=font
    r,g,b = color; tr.Font.Color.RGB = rgb(r,g,b)
    tr.ParagraphFormat.Alignment = ALIGN.get(align,2)
    tf.VerticalAnchor = 3

# ── 图片 ──────────────────────────────────────────────
def add_picture(slide, path, l, t, w=None, h=None):
    abs_p = os.path.abspath(path)
    if w and h:
        return slide.Shapes.AddPicture(abs_p, False, True, cm(l), cm(t), cm(w), cm(h))
    return slide.Shapes.AddPicture(abs_p, False, True, cm(l), cm(t))

# ── 表格 ──────────────────────────────────────────────
def add_table(slide, data, l, t, w, h,
              head_fill=(0,119,150), cell_fill=(17,39,61),
              text_color=(255,255,255), sz=14, font="微软雅黑"):
    rows = len(data); cols = max(len(row) for row in data)
    tbl = slide.Shapes.AddTable(rows, cols, cm(l), cm(t), cm(w), cm(h)).Table
    for ri in range(1, rows+1):
        for ci in range(1, cols+1):
            cell = tbl.Cell(ri, ci)
            fr,fg,fb = head_fill if ri==1 else cell_fill
            cell.Shape.Fill.Solid()
            cell.Shape.Fill.ForeColor.RGB = rgb(fr,fg,fb)
            val = str(data[ri-1][ci-1]) if ci-1 < len(data[ri-1]) else ""
            cell.Shape.TextFrame.TextRange.Text = val
            cell.Shape.TextFrame.TextRange.Font.Size = sz
            cell.Shape.TextFrame.TextRange.Font.Name = font
            cell.Shape.TextFrame.TextRange.Font.Bold = (ri==1)
            tr2,tg2,tb2 = text_color
            cell.Shape.TextFrame.TextRange.Font.Color.RGB = rgb(tr2,tg2,tb2)
    return tbl

# ── 动画 ──────────────────────────────────────────────
def add_anim_appear(slide, shape, trigger="after_prev", delay=0.3):
    """
    trigger: 'on_click'=1, 'with_prev'=2, 'after_prev'=3
    effectId 1 = msoAnimEffectAppear
    """
    trig_map = {"on_click":1, "with_prev":2, "after_prev":3}
    seq = slide.TimeLine.MainSequence
    eff = seq.AddEffect(
        Shape=shape,
        effectId=1,
        trigger=trig_map.get(trigger, 3)
    )
    eff.Timing.TriggerDelayTime = delay
    return eff

def add_animation(slide, shape, anim_type="entrance", effect_id=None,
                  trigger="on_click", delay=0.0):
    """
    统一动画封装函数
    anim_type: "entrance"(进入) | "exit"(退出) | "path"(路径)
    effect_id: 不传时按类型自动选默认效果ID
      entrance 默认: 1(Appear) | exit 默认: 11(Fly) | path 默认: 64(Down)
    trigger: "on_click"=1 | "with_prev"=2 | "after_prev"=3
    delay: 触发延迟秒数
    返回 Effect COM对象
    """
    trig_map = {"on_click": 1, "with_prev": 2, "after_prev": 3}
    type_map = {"entrance": 1, "exit": 2, "emphasis": 3, "path": 4}

    # 默认effectId
    default_ids = {
        "entrance": 1,   # msoAnimEffectAppear
        "exit":     11,  # msoAnimEffectFly (Exit方向)
        "path":     64,  # msoAnimEffectPathDown
    }
    eid = effect_id if effect_id is not None else default_ids.get(anim_type, 1)

    seq = slide.TimeLine.MainSequence
    eff = seq.AddEffect(
        Shape=shape,
        effectId=eid,
        trigger=trig_map.get(trigger, 1)
    )
    # 强制设置动画类型（exit/path需要覆盖COM默认值）
    eff.EffectType = type_map.get(anim_type, 1)
    eff.Timing.TriggerDelayTime = delay
    return eff

# ============================================================
# R90 新增高级函数 (2026-03-26)
# ============================================================

def batch_replace_text(prs, replacements):
    """
    批量替换整个演示文稿中的文本占位符。
    replacements: dict，如 {"{{标题}}": "实际标题", "{{日期}}": "2026-03-26"}
    返回替换总次数
    """
    count = 0
    for slide in prs.Slides:
        for shape in slide.Shapes:
            if shape.HasTextFrame:
                for para in shape.TextFrame.TextRange.Paragraphs():
                    for run in para.Runs():
                        for old, new in replacements.items():
                            if old in run.Text:
                                run.Text = run.Text.replace(old, new)
                                count += 1
    return count


def set_master_logo(prs, logo_path, l=0.1, t=0.05, w=1.2, h=0.4):
    """
    在母版中统一插入LOGO图片，所有幻灯片自动继承。
    logo_path: 图片绝对路径
    l, t, w, h: 位置和尺寸（英寸，会转为pt）
    """
    PT = 72.0
    master = prs.SlideMasters[1]
    master.Shapes.AddPicture(
        FileName=logo_path,
        LinkToFile=False,
        SaveWithDocument=True,
        Left=l * PT,
        Top=t * PT,
        Width=w * PT,
        Height=h * PT
    )


def add_anim_sequence(slide, shapes, effect_id=1, base_delay=0.3, interval=0.4):
    """
    为shapes列表中的形状批量添加顺序进入动画。
    effect_id: 1=Appear, 2=Fly, 27=Float
    base_delay: 第一个形状的延迟（秒）
    interval: 每个形状之间的间隔（秒）
    返回 effects 列表
    """
    seq = slide.TimeLine.MainSequence
    effects = []
    for i, shape in enumerate(shapes):
        eff = seq.AddEffect(
            Shape=shape,
            effectId=effect_id,
            trigger=3  # after_prev
        )
        eff.Timing.TriggerDelayTime = base_delay + i * interval
        effects.append(eff)
    return effects


def apply_theme_colors(slide, theme="tech_blue"):
    """
    对幻灯片应用预设配色主题（修改背景+统一文本色）。
    theme: "tech_blue" | "academic_green" | "warm_orange" | "dark_pro"
    """
    themes = {
        "tech_blue":      {"bg": (15, 30, 60),   "accent": (0, 180, 216)},
        "academic_green": {"bg": (20, 50, 30),   "accent": (80, 200, 120)},
        "warm_orange":    {"bg": (60, 30, 10),   "accent": (255, 140, 0)},
        "dark_pro":       {"bg": (20, 20, 20),   "accent": (200, 200, 200)},
    }
    t = themes.get(theme, themes["tech_blue"])
    r, g, b = t["bg"]
    set_bg_solid(slide, r, g, b)
    return t["accent"]
