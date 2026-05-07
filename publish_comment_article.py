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

body = """## 问题

博客上线初期用的是 Giscus 评论系统——基于 GitHub Discussions，免费无广告，当时觉得是完美的选择。

用了一段时间后发现问题：国内访问太慢了。加载评论列表要等好几秒，发表评论时经常卡在"加载中"然后失败。原因很简单——Giscus 走的是 GitHub API，国内到 GitHub 的网络不稳定。

对技术博客来说，评论是重要的交流渠道。如果读者想说句话都要卡半天，体验太差。

## 方案对比

我考虑了三个替代方案：

| 方案 | 加载速度 | 部署难度 | 费用 |
|------|---------|---------|------|
| Waline + LeanCloud | 快 | 中 | 免费 |
| Waline + Supabase + Vercel | 快 | 中 | 免费 |
| Django 内置评论 | 最快 | 低 | 无 |

前两个都需要额外部署后端服务。对一个小博客来说，多一个服务就等于多一个可能的故障点。Django 自带的能力完全够用——评论数据直接存在 SQLite 里，零外部依赖。

## 实现

改动很小，核心就三步：

**1. 新增 Comment 模型（20 行）**

```python
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments")
    name = models.CharField("昵称", max_length=50)
    email = models.EmailField("邮箱", blank=True)
    body = models.TextField("评论内容", max_length=2000)
    is_approved = models.BooleanField("审核通过", default=False)
    created_at = models.DateTimeField("评论时间", auto_now_add=True)
```

**2. 文章详情视图增加 POST 处理（10 行）**

```python
if request.method == "POST":
    name = request.POST.get("name", "").strip()
    body = request.POST.get("body", "").strip()
    if name and body and len(body) >= 2:
        Comment.objects.create(post=post, name=name, body=body)
    return redirect(post.get_absolute_url())
```

**3. 模板替换（Giscus 脚本 → 评论列表 + 表单）**

```html
{% for c in comments %}
<div>{{ c.name }} · {{ c.created_at|date:"Y-m-d H:i" }}</div>
<p>{{ c.body }}</p>
{% endfor %}

<form method="post">
  {% csrf_token %}
  <input name="name" placeholder="昵称" required>
  <textarea name="body" placeholder="写下你的想法..." required></textarea>
  <button type="submit">发表评论</button>
</form>
```

评论默认隐藏，需要在后台审核通过后才公开显示。防止垃圾和违规内容。

## 前后对比

| | Giscus | Django 评论 |
|------|------|------|
| 加载速度 | 2-5 秒 | 瞬间 |
| 发表评论 | 偶发失败 | 秒发 |
| 外部依赖 | GitHub API | 无 |
| 数据归属 | GitHub 仓库 | 自己的数据库 |
| 评论审核 | 不支持 | 后台审核 |
| 账号 | 需 GitHub | 填昵称即可 |

## 总结

选择技术方案时，简单 > 炫酷。Giscus 的理念很好——用 GitHub Issues 存储评论——但对国内用户来说，网络延迟让这个方案不成立。

不如回归最简单的方式：一个模型、一个表单、一个模板。快，稳，可控。

有想法欢迎在下方评论区交流。

*Su2ye · 2026 年 5 月 6 日*"""

post_data = {
    'csrfmiddlewaretoken': csrf2,
    'title': '告别 Giscus：将评论系统迁移到 Django 内置方案',
    'slug': 'migrate-comments-to-django',
    'author': 'Su2ye',
    'body': body,
    'category': '6',  # 部署
    'tags': '9',      # 博客
    'summary': 'Giscus 国内访问太慢，于是花 5 分钟用 50 行代码在 Django 里实现了一整套评论系统——包括审核机制。',
    'status': 'published',
    'is_top': '0',
    '_save': '保存',
}

r = s.post(add_url, data=post_data, headers={'Referer': add_url})
if r.status_code == 302 or '/admin/blog/post/' in r.url:
    print('ARTICLE PUBLISHED OK')
else:
    print('Status:', r.status_code)
    errs = re.findall(r'<ul class="errorlist[^"]*">(.*?)</ul>', r.text, re.S)
    if errs:
        print('Errors:', errs)
    else:
        print('Check manually')
