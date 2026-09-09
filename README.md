# 在线简历 · 潘灏

**前线部署工程师（FDE）/ 产品负责人（具身智能 · 硬科技）** ｜ 常驻深圳 · 随时到岗

这是一个通过 GitHub Pages 托管的在线简历仓库。简历以网页形式发布，打开链接即可查看，支持一键打印为 PDF，并已适配手机端浏览。

## 一、在线访问

- **在线简历**：https://qq547820639.github.io/resume/
- 打开根链接会自动跳转到 FDE 版简历（`resume-fde.html`）

该链接由 GitHub Pages 提供，长期稳定，可直接用于微信名片、个人主页或邮件签名。

## 二、选择版本

| 版本 | 文件 | 说明 |
| --- | --- | --- |
| **FDE 版（默认）** | `resume-fde.html` | 线上默认展示的版本，篇幅精炼，贴合 FDE / 前线部署 / 具身智能岗位定位 |
| 完整版 | `resume.html` | 内容最详尽，包含完整项目细节，适合需要全面了解履历的场景 |
| 备用版 | `resume-brief.html` | 与 FDE 版内容完全相同，作为备用入口保留 |

## 三、文件说明

```
index.html                  入口页，自动跳转到 FDE 版
resume-fde.html             FDE 版简历（线上默认）
resume.html                 完整版简历
resume-brief.html           备用版简历（同 FDE 版）
resume-delivery-fde.md      FDE 版源文件
resume-delivery-v2.md       完整版源文件
resume-delivery-brief.md    备用版源文件
build_resume_html.py        Markdown → HTML 生成脚本
build_resume_pdf.py         Markdown → A4 PDF 生成脚本
```

> **请只修改 `.md` 源文件，不要直接编辑 `.html`** —— HTML 由脚本生成，重新生成后会被覆盖。

## 四、更新简历

1. **修改内容**：编辑对应的 `.md` 源文件，例如 `resume-delivery-fde.md`。

2. **重新生成 HTML**：

   ```bash
   python build_resume_html.py resume-delivery-fde.md resume-fde.html
   ```

3. **（可选）生成 PDF**：

   ```bash
   python build_resume_pdf.py resume-delivery-fde.md resume-fde.pdf
   ```

4. **推送发布**：

   ```bash
   git add .
   git commit -m "更新简历"
   git push
   ```

推送后 GitHub Pages 会在 **1–2 分钟内**自动更新，无需额外操作。

## 五、环境准备

首次使用需安装依赖：

```bash
pip install markdown-it-py reportlab
```

> `build_resume_pdf.py` 依赖 macOS 系统字体（STHeiti），目前仅支持在 macOS 上生成 PDF。

## 六、打印与导出

在浏览器中打开任一 HTML 版本，按 `⌘ / Ctrl + P` 即可打印或另存为 PDF。页面已内置 A4 打印样式：输出为克制的黑白排版，文字为可选中的文本层，能被招聘系统（ATS）正常解析。

## 七、联系方式

- 邮箱：547820639@qq.com
- GitHub：https://github.com/qq547820639
