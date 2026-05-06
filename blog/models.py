from django.db import models
from django.urls import reverse
from django.utils import timezone


class Category(models.Model):
    """文章分类"""
    name = models.CharField("分类名称", max_length=50, unique=True)
    slug = models.SlugField("URL标识", max_length=50, unique=True)
    description = models.TextField("分类描述", blank=True, default="")

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = "分类"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"slug": self.slug})

    @property
    def post_count(self):
        return self.posts.filter(status="published").count()


class Tag(models.Model):
    """文章标签"""
    name = models.CharField("标签名称", max_length=50, unique=True)
    slug = models.SlugField("URL标识", max_length=50, unique=True)

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = "标签"
        ordering = ["name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:tag", kwargs={"slug": self.slug})

    @property
    def post_count(self):
        return self.posts.filter(status="published").count()


class Post(models.Model):
    """博客文章"""
    STATUS_CHOICES = [
        ("draft", "草稿"),
        ("published", "已发布"),
    ]

    title = models.CharField("标题", max_length=200)
    slug = models.SlugField("URL标识", max_length=200, unique=True)
    author = models.CharField("作者", max_length=50, default="Su2ye")
    category = models.ForeignKey(
        Category,
        verbose_name="分类",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="posts",
    )
    tags = models.ManyToManyField(Tag, verbose_name="标签", blank=True, related_name="posts")
    image = models.ImageField("封面图", upload_to="post_images/%Y/%m/", blank=True)
    summary = models.TextField("摘要", max_length=500, blank=True, default="")
    body = models.TextField("正文")
    status = models.CharField("状态", max_length=10, choices=STATUS_CHOICES, default="draft")
    views = models.PositiveIntegerField("阅读量", default=0)
    is_top = models.BooleanField("置顶", default=False)
    created_at = models.DateTimeField("创建时间", default=timezone.now)
    updated_at = models.DateTimeField("更新时间", auto_now=True)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = "文章"
        ordering = ["-is_top", "-created_at"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", kwargs={"slug": self.slug})

    def increase_views(self):
        self.views += 1
        self.save(update_fields=["views"])

    @property
    def prev_post(self):
        return (
            Post.objects.filter(status="published", created_at__lt=self.created_at)
            .order_by("-created_at")
            .first()
        )

    @property
    def next_post(self):
        return (
            Post.objects.filter(status="published", created_at__gt=self.created_at)
            .order_by("created_at")
            .first()
        )


class FriendLink(models.Model):
    """友情链接"""
    name = models.CharField("网站名称", max_length=100)
    url = models.URLField("网站地址")
    description = models.CharField("描述", max_length=200, blank=True, default="")
    is_active = models.BooleanField("启用", default=True)

    class Meta:
        verbose_name = "友情链接"
        verbose_name_plural = "友情链接"
        ordering = ["-is_active", "id"]

    def __str__(self):
        return self.name


class Comment(models.Model):
    """文章评论"""
    post = models.ForeignKey(
        Post, verbose_name="文章", on_delete=models.CASCADE, related_name="comments"
    )
    name = models.CharField("昵称", max_length=50)
    email = models.EmailField("邮箱", blank=True, default="")
    body = models.TextField("评论内容", max_length=2000)
    created_at = models.DateTimeField("评论时间", auto_now_add=True)

    class Meta:
        verbose_name = "评论"
        verbose_name_plural = "评论"
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.name}: {self.body[:30]}"
