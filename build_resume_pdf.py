# -*- coding: utf-8 -*-
"""由 resume-delivery-v2.md 生成 A4 投递版 PDF（reportlab，中文正确嵌入，文本层可被 ATS 解析）。"""
import re, pathlib
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer, ListFlowable,
                                ListItem, Table, TableStyle, KeepTogether, PageBreak)

ROOT = pathlib.Path(__file__).parent
import sys
SRC = ROOT / (sys.argv[1] if len(sys.argv) > 1 else 'resume-delivery-v2.md')
OUT = ROOT / (sys.argv[2] if len(sys.argv) > 2 else 'resume.pdf')

FONT_PATH = '/System/Library/Fonts/STHeiti Medium.ttc'
pdfmetrics.registerFont(TTFont('STHeiti', FONT_PATH, subfontIndex=0))
FONT = 'STHeiti'

INK = colors.HexColor('#1a1a1a')
GREY = colors.HexColor('#555555')
ACCENT = colors.HexColor('#b45309')
LINE = colors.HexColor('#c9cdd4')
HEADBG = colors.HexColor('#f4f5f7')

S_NAME = ParagraphStyle('name', fontName=FONT, fontSize=17, leading=21, textColor=INK, spaceAfter=2)
S_SUB = ParagraphStyle('sub', fontName=FONT, fontSize=10, leading=13, textColor=ACCENT, spaceAfter=4)
S_META = ParagraphStyle('meta', fontName=FONT, fontSize=8.2, leading=11.5, textColor=GREY, spaceAfter=1)
S_H2 = ParagraphStyle('h2', fontName=FONT, fontSize=11.5, leading=16, textColor=INK, spaceBefore=12, spaceAfter=4.5)
S_H3 = ParagraphStyle('h3', fontName=FONT, fontSize=10.2, leading=14.5, textColor=INK, spaceBefore=10, spaceAfter=4)
S_H4 = ParagraphStyle('h4', fontName=FONT, fontSize=9.8, leading=13.8, textColor=ACCENT, spaceBefore=8, spaceAfter=3.4)
S_BODY = ParagraphStyle('body', fontName=FONT, fontSize=9.4, leading=14.2, textColor=INK, spaceAfter=3.6, alignment=TA_LEFT)
S_LI = ParagraphStyle('li', fontName=FONT, fontSize=9.4, leading=14, textColor=INK, spaceAfter=2.8, leftIndent=11, firstLineIndent=-11)
S_QUOTE = ParagraphStyle('quote', fontName=FONT, fontSize=8.8, leading=12.8, textColor=GREY, spaceAfter=3)
S_CELL = ParagraphStyle('cell', fontName=FONT, fontSize=8.9, leading=12.8, textColor=INK)
S_CELLH = ParagraphStyle('cellh', fontName=FONT, fontSize=8.9, leading=12.8, textColor=INK)


def inline(t: str) -> str:
    """Markdown 内联：**粗体** → <b>；转义 XML。"""
    t = t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    t = re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', t)
    t = re.sub(r'`(.+?)`', r'<font face="%s">\1</font>' % FONT, t)
    return t


def parse(md: str):
    """返回 (name, subtitle, meta, blocks)。blocks 为 (type, content) 列表。"""
    lines = md.split('\n')
    name = subtitle = meta = ''
    blocks = []
    i = 0
    # 头部：# 名 → 空 → **副标题** → 空 → 元信息行
    while i < len(lines):
        l = lines[i].strip()
        if l.startswith('# '):
            name = l[2:].strip(); i += 1; break
        i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and lines[i].strip().startswith('**'):
        subtitle = lines[i].strip().strip('*'); i += 1
    while i < len(lines) and not lines[i].strip():
        i += 1
    if i < len(lines) and not lines[i].startswith('#') and not lines[i].startswith('---'):
        meta = lines[i].strip(); i += 1

    buf_table = []
    while i < len(lines):
        raw = lines[i]
        l = raw.strip()
        if l == '<!--pagebreak-->':
            if buf_table:
                blocks.append(('table', buf_table)); buf_table = []
            blocks.append(('pagebreak', None))
            i += 1; continue
        if not l or l == '---':
            if buf_table:
                blocks.append(('table', buf_table)); buf_table = []
            i += 1; continue
        if l.startswith('|'):
            cells = [c.strip() for c in l.strip('|').split('|')]
            if not all(re.fullmatch(r':?-{2,}:?', c) for c in cells):
                buf_table.append(cells)
            i += 1; continue
        if buf_table:
            blocks.append(('table', buf_table)); buf_table = []
        if l.startswith('#### '):
            blocks.append(('h4', l[5:].strip()))
        elif l.startswith('### '):
            blocks.append(('h3', l[4:].strip()))
        elif l.startswith('## '):
            blocks.append(('h2', l[3:].strip()))
        elif l.startswith('> '):
            blocks.append(('quote', l[2:].strip()))
        elif l.startswith('- '):
            blocks.append(('li', l[2:].strip()))
        elif l.startswith('**') and '：' in l:
            blocks.append(('body', l))
        elif not l.startswith('#'):
            blocks.append(('body', l))
        i += 1
    if buf_table:
        blocks.append(('table', buf_table))
    return name, subtitle, meta, blocks


def build():
    md = SRC.read_text(encoding='utf-8')

    # 页眉标题：取源首个加粗标题行，去掉末尾方向括号（如"（具身智能 · 硬科技）"）
    _m = re.search(r'^\*\*(.+?)\*\*\s*$', md, re.M)
    global HEADER_TITLE
    HEADER_TITLE = ('潘灏 · ' + re.sub(r'（[^（）]*）\s*$', '', _m.group(1)).strip()) if _m else '潘灏 · 简历'
    name, subtitle, meta, blocks = parse(md)
    story = []
    pending = []

    # 头部
    story.append(Paragraph(inline(name), S_NAME))
    if subtitle:
        story.append(Paragraph(inline(subtitle), S_SUB))
    if meta:
        story.append(Paragraph(inline(meta), S_META))
    story.append(Spacer(1, 3))
    story.append(Table([['']], colWidths=[176 * mm], rowHeights=[1.4],
                       style=TableStyle([('LINEBELOW', (0, 0), (-1, -1), 1.4, ACCENT),
                                         ('TOPPADDING', (0, 0), (-1, -1), 0),
                                         ('BOTTOMPADDING', (0, 0), (-1, -1), 0)])))
    story.append(Spacer(1, 4))

    W = 176 * mm
    for kind, content in blocks:
        if kind == 'pagebreak':
            story.extend(pending); pending = []
            story.append(PageBreak())
        elif kind == 'h2':
            story.extend(pending); pending = []
            story.append(Spacer(1, 2))
            story.append(Paragraph(inline(content), S_H2))
            story.append(Table([['']], colWidths=[W], rowHeights=[0.8],
                               style=TableStyle([('LINEBELOW', (0, 0), (-1, -1), 0.8, LINE),
                                                 ('TOPPADDING', (0, 0), (-1, -1), 0),
                                                 ('BOTTOMPADDING', (0, 0), (-1, -1), 0)])))
            story.append(Spacer(1, 3))
        elif kind == 'h3':
            pending.append(Paragraph(inline(content), S_H3))
        elif kind == 'h4':
            pending.append(Paragraph(inline(content), S_H4))
        elif kind == 'body':
            f = Paragraph(inline(content), S_BODY)
            if pending:
                story.append(KeepTogether(pending + [f])); pending = []
            else:
                story.append(f)
        elif kind == 'li':
            f = Paragraph('<font color="#b45309">▪</font>&nbsp;&nbsp;' + inline(content), S_LI)
            if pending:
                story.append(KeepTogether(pending + [f])); pending = []
            else:
                story.append(f)
        elif kind == 'quote':
            t = Table([[Paragraph(inline(content), S_QUOTE)]], colWidths=[W])
            t.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor('#fff8f0')),
                ('LINEBEFORE', (0, 0), (0, -1), 1.6, ACCENT),
                ('LEFTPADDING', (0, 0), (-1, -1), 8), ('RIGHTPADDING', (0, 0), (-1, -1), 8),
                ('TOPPADDING', (0, 0), (-1, -1), 5.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 5.5),
            ]))
            if pending:
                story.append(KeepTogether(pending + [t])); pending = []
            else:
                story.append(t)
            story.append(Spacer(1, 2.5))
        elif kind == 'table':
            rows = content
            if not rows:
                continue
            ncols = max(len(r) for r in rows)
            data = []
            for ri, r in enumerate(rows):
                cells = [Paragraph(inline(c), S_CELLH if ri == 0 else S_CELL) for c in r]
                while len(cells) < ncols:
                    cells.append(Paragraph('', S_CELL))
                data.append(cells)
            # 列宽：首列略窄，其余均分
            if ncols == 2:
                cw = [W * 0.24, W * 0.76]
            elif ncols == 3:
                cw = [W * 0.22, W * 0.56, W * 0.22]
            elif ncols >= 4:
                cw = [W * 0.26] + [W * 0.74 / (ncols - 1)] * (ncols - 1)
            else:
                cw = [W]
            tb = Table(data, colWidths=cw, repeatRows=1)
            tb.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), HEADBG),
                ('TEXTCOLOR', (0, 0), (-1, 0), INK),
                ('GRID', (0, 0), (-1, -1), 0.35, colors.HexColor('#e3e6ea')),
                ('VALIGN', (0, 0), (-1, -1), 'TOP'),
                ('LEFTPADDING', (0, 0), (-1, -1), 6), ('RIGHTPADDING', (0, 0), (-1, -1), 6),
                ('TOPPADDING', (0, 0), (-1, -1), 6.5), ('BOTTOMPADDING', (0, 0), (-1, -1), 6.5),
            ]))
            # 大表格（>9 行）允许跨页（repeatRows 保持表头），避免整体下推造成页面空白
            if pending:
                if len(rows) <= 9:
                    story.append(KeepTogether(pending + [tb, Spacer(1, 3)]))
                else:
                    story.extend(pending)
                    story.append(tb)
                    story.append(Spacer(1, 3))
                pending = []
            elif len(rows) <= 9:
                story.append(KeepTogether([tb, Spacer(1, 3)]))
            else:
                story.append(tb)
                story.append(Spacer(1, 3))

    if pending:
        story.extend(pending); pending = []

    # 文档
    def on_page(canv, doc):
        canv.saveState()
        if doc.page > 1:
            canv.setFont(FONT, 7.4)
            canv.setFillColor(colors.HexColor('#9aa0aa'))
            canv.drawString(18 * mm, A4[1] - 11 * mm, HEADER_TITLE)
            canv.drawRightString(A4[0] - 18 * mm, A4[1] - 11 * mm, '深圳 · 随时到岗')
            canv.setStrokeColor(colors.HexColor('#e3e6ea'))
            canv.setLineWidth(0.5)
            canv.line(18 * mm, A4[1] - 12.5 * mm, A4[0] - 18 * mm, A4[1] - 12.5 * mm)
        canv.setFont(FONT, 7.4)
        canv.setFillColor(colors.HexColor('#9aa0aa'))
        canv.drawCentredString(A4[0] / 2, 9 * mm, str(doc.page))
        canv.restoreState()

    doc = BaseDocTemplate(str(OUT), pagesize=A4,
                          leftMargin=19 * mm, rightMargin=19 * mm,
                          topMargin=17 * mm, bottomMargin=17 * mm,
                          title='潘灏 · AI 产品经理 / 产品负责人 · 简历', author='潘灏')
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id='f')
    doc.addPageTemplates([PageTemplate(id='main', frames=[frame], onPage=on_page)])
    doc.build(story)
    print(f"生成: {OUT}")


if __name__ == '__main__':
    build()
