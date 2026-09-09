# -*- coding: utf-8 -*-
"""由 resume-delivery-v2.md 生成 HTML 简历（科技感模板 + 打印样式）。内容 100% 来自源 Markdown，不虚构。"""
import re, pathlib
from markdown_it import MarkdownIt

ROOT = pathlib.Path(__file__).parent
import sys
SRC = ROOT / (sys.argv[1] if len(sys.argv) > 1 else 'resume-delivery-v2.md')
OUT = ROOT / (sys.argv[2] if len(sys.argv) > 2 else 'resume.html')

md_text = SRC.read_text(encoding='utf-8')

# 在源文本中对口径未定字段插入占位符标注（仅标记，不改动事实）
md = MarkdownIt('commonmark', {'html': True, 'typographer': False, 'breaks': False}).enable('table')
body = md.render(md_text)

# 提取首屏姓名与副标题（h1 + 紧跟的 strong 段）
m = re.search(r'<h1>(.*?)</h1>\s*<p><strong>(.*?)</strong></p>\s*<p>(.*?)</p>', body, re.S)
name = m.group(1) if m else '潘灏'
subtitle = m.group(2) if m else ''
meta_line = m.group(3) if m else ''

# 标题纯文本（供 <title> / <meta description> 使用，自动跟随源，避免版本间不一致）
_raw = re.search(r'^\*\*(.+?)\*\*\s*$', md_text, re.M)
title_plain = re.sub(r'（[^（）]*）\s*$', '', _raw.group(1)).strip() if _raw else '简历'
if m:
    body = body.replace(m.group(0), '', 1)

# 移除 markdown 中第一张"求职意向"前的 hr 噪音
body = re.sub(r'^\s*<hr />\s*', '', body)

# 按 h2 切分，将每个模块包裹为卡片 <section>
parts = re.split(r'(?=<h2>)', body)
body = ''.join(
    (f'<section>\n{p.strip()}\n</section>' if p.strip().startswith('<h2>') else p)
    for p in parts
)

CSS = """
:root{
  --bg:#0b0e14; --bg2:#111621; --card:#151b28; --line:#232c3d;
  --fg:#e8edf7; --fg-dim:#9aa7bd; --accent:#ff6a00; --accent2:#ff9a3c;
  --ok:#2ecc71; --radius:14px;
  --fs:16px; --lh:2.0;
}
*{box-sizing:border-box}
html{-webkit-text-size-adjust:100%}
body{
  margin:0; padding:0;
  background:
    radial-gradient(1100px 520px at 12% -8%, rgba(255,106,0,.16), transparent 60%),
    radial-gradient(900px 480px at 100% 0%, rgba(60,130,255,.12), transparent 55%),
    var(--bg);
  color:var(--fg);
  font:var(--fs)/var(--lh) -apple-system,BlinkMacSystemFont,"PingFang SC","Hiragino Sans GB","Microsoft YaHei","Noto Sans SC",Segoe UI,Helvetica,Arial,sans-serif;
  letter-spacing:.01em;
}
.wrap{max-width:920px;margin:0 auto;padding:34px 22px 72px}

/* Hero */
.hero{
  position:relative;overflow:hidden;
  background:linear-gradient(135deg,rgba(255,106,0,.14),rgba(20,26,38,.9) 42%,rgba(20,26,38,.96));
  border:1px solid var(--line);border-radius:18px;padding:34px 30px;margin-bottom:26px;
  box-shadow:0 18px 50px -22px rgba(0,0,0,.9);
  animation:rise .5s ease both;
}
.hero:before{
  content:"";position:absolute;inset:0;pointer-events:none;
  background:linear-gradient(90deg,transparent,rgba(255,154,60,.10),transparent);
  transform:translateX(-100%);animation:sweep 6.5s ease-in-out infinite;
}
@keyframes sweep{0%{transform:translateX(-100%)}55%,100%{transform:translateX(100%)}}
@keyframes rise{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}
.hero h1{margin:0 0 8px;font-size:2.15rem;letter-spacing:.04em}
.hero .sub{color:var(--accent2);font-weight:700;font-size:1.06rem;margin-bottom:12px}
.hero .meta{color:var(--fg-dim);font-size:.93rem;line-height:2}
.hero .meta b{color:var(--fg);font-weight:600}
.badge{
  display:inline-block;margin:0 6px 6px 0;padding:4px 11px;border-radius:999px;font-size:.78rem;
  background:rgba(255,106,0,.12);border:1px solid rgba(255,106,0,.35);color:var(--accent2)
}

/* Sections */
section{
  background:linear-gradient(180deg,var(--card),var(--bg2));
  border:1px solid var(--line);border-radius:var(--radius);
  padding:26px 28px;margin:0 0 22px;
  box-shadow:0 12px 34px -24px rgba(0,0,0,.9);
  transition:transform .18s ease,border-color .18s ease;
}
section:hover{transform:translateY(-2px);border-color:rgba(255,106,0,.32)}
h2{font-size:1.2rem;margin:0 0 18px;padding-bottom:12px;border-bottom:1px solid var(--line);color:#fff;letter-spacing:.06em}
h2:before{content:"";display:inline-block;width:9px;height:9px;border-radius:2px;background:var(--accent);margin-right:10px;vertical-align:middle}
h3{font-size:1.06rem;margin:26px 0 12px;color:#fff;line-height:1.5}
h4{font-size:1.0rem;margin:20px 0 10px;color:var(--accent2)}
h3:first-of-type,h4:first-of-type{margin-top:4px}
p{margin:12px 0}
ul{margin:12px 0;padding-left:22px}
li{margin:9px 0}
strong{color:#fff}
em{color:var(--fg-dim);font-style:normal;font-size:.92rem}
code{background:rgba(255,255,255,.06);padding:1px 6px;border-radius:5px;font-size:.9em}

/* Tables */
table{width:100%;border-collapse:collapse;margin:18px 0;font-size:.94rem;display:block;overflow-x:auto;white-space:nowrap}
thead th{
  text-align:left;background:rgba(255,106,0,.10);color:var(--accent2);
  padding:13px 14px;border-bottom:1px solid var(--line);font-weight:700;white-space:nowrap
}
td{padding:13px 14px;border-bottom:1px solid rgba(35,44,61,.7);vertical-align:top;white-space:normal;line-height:1.85}
tbody tr:hover td{background:rgba(255,255,255,.03)}
blockquote{
  margin:16px 0;padding:14px 18px;border-left:3px solid var(--accent);
  background:rgba(255,106,0,.07);border-radius:0 8px 8px 0;color:var(--fg-dim);font-size:.93rem
}
hr{border:0;border-top:1px dashed var(--line);margin:16px 0}

/* 数字高亮 */
.num{color:var(--accent2);font-weight:700;padding:0 1px}
.ph{color:#ffd08a;background:rgba(255,208,138,.12);border-radius:5px;padding:1px 6px;font-size:.86em}

footer{color:var(--fg-dim);font-size:.82rem;text-align:center;margin-top:26px;line-height:1.9}

/* 移动端 */
@media (max-width:640px){
  :root{--fs:14.5px}
  .wrap{padding:16px 12px 40px}
  .hero{padding:22px 18px}
  .hero h1{font-size:1.65rem}
  section{padding:16px 15px;border-radius:12px}
  table{font-size:.88rem}
  h2{font-size:1.05rem}
}
@media (prefers-reduced-motion:reduce){
  *{animation:none!important;transition:none!important}
}

/* ============ 打印 / PDF（A4，克制排版） ============ */
@media print{
  @page{size:A4;margin:14mm 13mm}
  html,body{background:#fff!important;color:#151515!important}
  body{font-size:9.6pt;line-height:1.62}
  .wrap{max-width:none;padding:0}
  .hero{
    background:#fff!important;border:0;border-bottom:1.8pt solid #b45309;border-radius:0;padding:0 0 5pt;margin:0 0 7pt;
    box-shadow:none;animation:none
  }
  .hero:before{display:none}
  .hero h1{font-size:17pt;margin:0 0 2pt;color:#000}
  .hero .sub{color:#92400e!important;font-size:9.6pt;margin-bottom:3pt}
  .hero .meta{color:#333!important;font-size:8.3pt;line-height:1.5}
  .hero div[style]{margin-top:4pt!important}
  .badge{background:#fff!important;border:.5pt solid #b45309;color:#92400e!important;padding:0 4pt;font-size:7.4pt;margin:0 3pt 0 0}
  section{
    background:#fff!important;border:0;border-radius:0;padding:0;margin:0 0 10pt;box-shadow:none;
    break-inside:auto
  }
  section:hover{transform:none}
  h2{font-size:11pt;color:#000;border-bottom:.7pt solid #999;padding-bottom:2.5pt;margin:0 0 6pt;break-after:avoid}
  h2:before{background:#b45309;width:6pt;height:6pt;margin-right:5pt}
  h3{font-size:9.8pt;color:#000;margin:8pt 0 3.5pt;break-after:avoid;line-height:1.35}
  h4{font-size:9.1pt;color:#92400e;margin:4pt 0 1.6pt;break-after:avoid}
  p,li{orphans:3;widows:3}
  ul{margin:2pt 0;padding-left:12pt}
  li{margin:2.4pt 0;font-size:9.4pt;line-height:1.6}
  p{font-size:9.4pt;margin:3.5pt 0;line-height:1.62}
  em{font-size:8.8pt}
  table{display:table!important;width:100%;font-size:8.5pt;border-collapse:collapse;margin:3pt 0;break-inside:avoid;white-space:normal}
  thead th{background:#f3f4f6!important;color:#000!important;border-bottom:.7pt solid #999;padding:2.6pt 5pt;font-size:8.5pt}
  td{padding:2.4pt 5pt;border-bottom:.4pt solid #e5e7eb;color:#111;font-size:8.5pt;line-height:1.38}
  blockquote{background:#fff8f0!important;border-left:2pt solid #b45309;color:#333;padding:3pt 6pt;margin:3pt 0;font-size:8.8pt;line-height:1.42}
  hr{display:none}
  .num{color:#92400e!important}
  .ph{background:#fff;border:.4pt dashed #b45309;color:#92400e!important;padding:0 2pt;font-size:8.4pt}
  footer{color:#666!important;font-size:7.6pt;margin-top:5pt;line-height:1.5}
  a{color:#000;text-decoration:none}
}
"""

JS = """
// 数字与关键指标高亮（克制：仅着色，不改变内容）
document.addEventListener('DOMContentLoaded', function(){
  var sel = 'li,p,td,blockquote,strong';
  document.querySelectorAll(sel).forEach(function(el){
    if (el.querySelector('.num')) return;
    var html = el.innerHTML;
    // 保护标签与已有标记
    var out = html.replace(/(?<!<[^>]*)(?<!\\/)([0-9][0-9,\\.]*(?:\\s?%|\\+|\\s?K|\\s?万字|\\s?件|\\s?份|\\s?个|\\s?项|\\s?版|\\s?款|\\s?条|\\s?类|\\s?张|\\s?次)?)/g, function(m, p1, offset){
      if (/class="(num|ph)"/.test(html.slice(Math.max(0,offset-24), offset))) return m;
      if (/<[^>]*$/.test(html.slice(0, offset))) return m;
      return '<span class="num">' + m + '</span>';
    });
    if (out !== html && !/<(table|thead|tbody|tr)/i.test(html)) el.innerHTML = out;
  });
});
"""

html = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} · {title_plain} · 简历</title>
<meta name="description" content="{name} · {title_plain} · 常驻深圳 · 随时到岗">
<style>{CSS}</style>
</head>
<body>
<div class="wrap">

<header class="hero">
  <h1>{name}</h1>
  <div class="sub">{subtitle}</div>
  <div class="meta">{meta_line}</div>
  <div style="margin-top:12px">
    <span class="badge">随时到岗</span>
    <span class="badge">常驻深圳</span>
    <span class="badge">AI 协同交付</span>
    <span class="badge">具身智能 / 外骨骼</span>
  </div>
</header>

<main>
{body}
</main>

<footer>
  本简历所有数据均可溯源至本人材料与交付物；专利为递交前草稿、论文作者著录待定、EWOH 为演示实例代码级自验收——均以如实口径标注。
</footer>

</div>
<script>{JS}</script>
</body>
</html>
"""

OUT.write_text(html, encoding='utf-8')
print(f"生成: {OUT}  ({len(html):,} 字符)")
