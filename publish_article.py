import requests, re

s = requests.Session()
login_url = 'http://122.51.135.14/admin/login/'

r = s.get(login_url)
csrf = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text).group(1)

r = s.post(login_url, data={
    'csrfmiddlewaretoken': csrf,
    'username': 'su2ye',
    'password': 'cik62222',
    'next': '/admin/'
}, headers={'Referer': login_url})

print('Login:', 'OK' if 'logout' in r.text.lower() else 'FAIL')

add_url = 'http://122.51.135.14/admin/blog/post/add/'
r = s.get(add_url)
csrf2 = re.search(r'name="csrfmiddlewaretoken" value="([^"]+)"', r.text).group(1)

body = """## 起因

博客上线后，我发现文章里的代码块全是灰色，没有任何语法高亮。Python 关键字、字符串、函数名都是一个颜色——这跟纯文本没区别。

作为一个技术博客，代码高亮是基本要求。开始排查。

## 第一回合：CDN 被墙

最初以为是 Pygments 的 CSS 没加载。用了 jsDelivr CDN 的 github.css，国内访问不稳定。于是改成本地生成：

```python
from pygments.formatters import HtmlFormatter
with open("static/css/pygments.css", "w") as f:
    f.write(HtmlFormatter(style="github-dark").get_style_defs(".highlight"))
```

CSS 生成了，模板引用了。刷新——还是不行。

## 第二回合：排查 HTML 输出

用 curl 拉取页面 HTML，发现代码块反引号原样输出，没有被 `<pre><code>` 包裹。问题在渲染环节。

## 第三回合：发现 nl2br 元凶

Django 模板和 CSS 都没问题。真正元凶在 Markdown 扩展配置：

```python
MARKDOWN_EXTENSIONS = [
    "markdown.extensions.fenced_code",
    "markdown.extensions.codehilite",
    "markdown.extensions.nl2br",   # ← 这个破坏了代码块
]
```

nl2br 把换行转成 `<br>`，但它在 fenced_code 之前执行，把代码块里的换行也转了。fenced_code 看到的是被破坏的内容，无法识别。

删掉 nl2br 就修好了。一行配置，一个小时。

## 第四回合：旧文章的后遗症

修好配置后新文章没问题，但之前通过 Django shell 创建的旧文章，由于粘贴时的转义问题，反引号本身就损坏了。需要全部重建。

## 教训

1. nl2br 和 fenced_code 不能共存——Python markdown 的已知陷阱
2. 调试顺序：HTML 输出 → 渲染链路 → 配置源头，比从 CSS 开始猜高效
3. Django shell 粘贴多层 Markdown 会丢反引号——用脚本文件
4. CDN 在国内不可靠——静态资源本地化

整个过程近一个小时。一个配置项，一行代码。但找到它之前绕的弯路，就是调试的本质。

*Su2ye · 2026 年 5 月 6 日*"""

post_data = {
    'csrfmiddlewaretoken': csrf2,
    'title': '调试日志：代码高亮消失的一个小时',
    'slug': 'debug-code-highlight',
    'author': 'Su2ye',
    'body': body,
    'category': '7',  # 杂谈
    'tags': '13',     # 部署
    'summary': '排查博客代码高亮失败的全过程——从 CDN 到 HTML 再到一行配置，记录每个判断和转折。',
    'status': 'published',
    'is_top': '0',
    '_save': '保存',
}

r = s.post(add_url, data=post_data, headers={'Referer': add_url})
if r.status_code == 302 or '/admin/blog/post/' in r.url:
    print('ARTICLE PUBLISHED OK')
    print('View at: http://122.51.135.14/debug-code-highlight/')
else:
    print('Status:', r.status_code)
    # Check for errors
    errs = re.findall(r'<ul class="errorlist[^"]*">(.*?)</ul>', r.text, re.S)
    if errs:
        print('Errors:', errs)
    else:
        print('No errors found - maybe success?')
        if 'successfully' in r.text.lower() or 'was added' in r.text.lower():
            print('Article was added!')
