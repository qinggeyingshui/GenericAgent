"""
word_toolkit.py — Word COM 驱动工具库
覆盖：新建/打开/保存文档、标题/正文/列表/表格/图片插入、段落格式
接口风格与 ppt_com_toolkit.py 一致
"""
import os
import win32com.client as win32

# Word 常量
WD_SAVE_DOCX       = 16   # wdFormatXMLDocument
WD_ALIGN_LEFT      = 0
WD_ALIGN_CENTER    = 1
WD_ALIGN_RIGHT     = 2
WD_ALIGN_JUSTIFY   = 3
WD_STYLE_HEADING1  = -2   # wdStyleHeading1
WD_STYLE_HEADING2  = -3   # wdStyleHeading2
WD_STYLE_HEADING3  = -4   # wdStyleHeading3
WD_STYLE_NORMAL    = -1   # wdStyleNormal
WD_COLOR_AUTO      = -16777216


# ── 生命周期 ──────────────────────────────────────────
def open_word(visible=False):
    """启动 Word COM 应用。visible=False 时后台静默运行"""
    app = win32.Dispatch("Word.Application")
    app.Visible = visible
    return app


def new_doc(app):
    """新建空白文档，返回 Document 对象"""
    return app.Documents.Add()


def open_doc(app, path):
    """打开已有 .docx 文件"""
    return app.Documents.Open(os.path.abspath(path))


def save_and_quit(app, doc, path):
    """保存为 .docx 并退出 Word"""
    abs_path = os.path.abspath(path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    doc.SaveAs2(abs_path, WD_SAVE_DOCX)
    print(f"[WORD] 已保存: {abs_path}")
    doc.Close(SaveChanges=False)
    app.Quit()
    print("[WORD] 已退出")


def save_doc(doc, path):
    """仅保存，不退出（用于批量操作中间保存）"""
    abs_path = os.path.abspath(path)
    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    doc.SaveAs2(abs_path, WD_SAVE_DOCX)
    print(f"[WORD] 已保存: {abs_path}")


# ── 段落与文本 ──────────────────────────────────────
def add_heading(doc, text, level=1):
    """
    插入标题段落。
    level: 1=一级标题, 2=二级标题, 3=三级标题
    """
    style_map = {1: WD_STYLE_HEADING1, 2: WD_STYLE_HEADING2, 3: WD_STYLE_HEADING3}
    para = doc.Content.Paragraphs.Add()
    para.Range.Text = text
    para.Style = doc.Styles(style_map.get(level, WD_STYLE_HEADING1))
    return para


def add_paragraph(doc, text, bold=False, italic=False, sz=12,
                  align=WD_ALIGN_LEFT, color=None):
    """
    插入正文段落。
    sz: 字号(pt) | color: (r,g,b) 元组或 None
    """
    para = doc.Content.Paragraphs.Add()
    rng = para.Range
    rng.Text = text
    rng.Font.Size = sz
    rng.Font.Bold = bold
    rng.Font.Italic = italic
    para.Alignment = align
    if color:
        r, g, b = color
        rng.Font.Color = r + (g << 8) + (b << 16)
    return para


def add_bullet_list(doc, items, sz=11, indent_cm=1.0):
    """
    插入无序列表（项目符号）。
    items: str 列表
    """
    paras = []
    for item in items:
        para = doc.Content.Paragraphs.Add()
        para.Range.Text = item
        para.Style = doc.Styles("List Bullet")
        para.Range.Font.Size = sz
        paras.append(para)
    return paras


def add_page_break(doc):
    """插入分页符"""
    doc.Content.InsertParagraphAfter()
    rng = doc.Content
    rng.Collapse(0)  # wdCollapseEnd
    rng.InsertBreak(7)  # wdPageBreak


# ── 表格 ──────────────────────────────────────────
def add_table(doc, data, header_bold=True, border=True):
    """
    插入表格。
    data: 二维列表，第一行自动加粗作表头
    header_bold: 首行是否加粗
    border: 是否显示边框
    返回 Table COM 对象
    """
    if not data:
        return None
    rows = len(data)
    cols = max(len(row) for row in data)
    rng = doc.Content
    rng.Collapse(0)
    tbl = doc.Tables.Add(rng, rows, cols)
    if border:
        tbl.Borders.Enable = True
    for r, row in enumerate(data):
        for c, cell_text in enumerate(row):
            cell = tbl.Cell(r + 1, c + 1)
            cell.Range.Text = str(cell_text)
            if header_bold and r == 0:
                cell.Range.Font.Bold = True
    return tbl


# ── 图片 ──────────────────────────────────────────
def add_picture(doc, path, width_cm=None, height_cm=None):
    """
    在文档末尾插入图片。
    width_cm/height_cm: 宽高（厘米），None 则保持原始比例
    返回 InlineShape 对象
    """
    CM_TO_PT = 28.3465  # 1cm = 28.35pt
    rng = doc.Content
    rng.Collapse(0)
    pic = doc.InlineShapes.AddPicture(
        FileName=os.path.abspath(path),
        LinkToFile=False,
        SaveWithDocument=True,
        Range=rng
    )
    if width_cm:
        pic.Width = width_cm * CM_TO_PT
    if height_cm:
        pic.Height = height_cm * CM_TO_PT
    return pic


# ── 页面设置 ──────────────────────────────────────
def set_page_margin(doc, top=2.54, bottom=2.54, left=3.17, right=3.17):
    """
    设置页边距（厘米）。默认 Word 标准页边距
    """
    CM = 28.3465
    ps = doc.PageSetup
    ps.TopMargin    = top    * CM
    ps.BottomMargin = bottom * CM
    ps.LeftMargin   = left   * CM
    ps.RightMargin  = right  * CM


# ── 快捷组合 ──────────────────────────────────────
def build_report(output_path, title, sections, table_data=None):
    """
    一键生成报告型文档。
    title: 文档标题字符串
    sections: [(heading, body_text), ...] 的列表
    table_data: 可选二维列表，插入在最后
    返回 (app, doc) 元组，调用方自行 save_and_quit
    """
    app = open_word(visible=False)
    doc = new_doc(app)
    set_page_margin(doc)
    add_heading(doc, title, level=1)
    for heading, body in sections:
        if heading:
            add_heading(doc, heading, level=2)
        if body:
            add_paragraph(doc, body)
    if table_data:
        add_heading(doc, "数据表格", level=2)
        add_table(doc, table_data)
    return app, doc
