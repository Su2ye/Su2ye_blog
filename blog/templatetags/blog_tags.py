import markdown
from django import template
from django.conf import settings
from django.utils.safestring import mark_safe
from ..models import Category, Tag, Post, FriendLink

register = template.Library()


@register.filter(name="markdown")
def markdown_filter(text):
    """将 Markdown 文本渲染为 HTML，并添加代码高亮"""
    return mark_safe(
        markdown.markdown(
            text,
            extensions=settings.MARKDOWN_EXTENSIONS,
            extension_configs={
                "markdown.extensions.codehilite": {
                    "css_class": "highlight",
                    "guess_lang": True,
                },
            },
        )
    )


@register.simple_tag
def get_categories():
    return Category.objects.all()


@register.simple_tag
def get_tags():
    return Tag.objects.all()


@register.simple_tag
def get_recent_posts(count=5):
    return Post.objects.filter(status="published").order_by("-created_at")[:count]


@register.simple_tag
def get_popular_posts(count=5):
    return Post.objects.filter(status="published").order_by("-views")[:count]


@register.simple_tag
def get_friend_links():
    return FriendLink.objects.filter(is_active=True)


@register.simple_tag
def get_post_count():
    return Post.objects.filter(status="published").count()


@register.inclusion_tag("blog/_sidebar.html")
def render_sidebar():
    return {
        "categories": Category.objects.all(),
        "tags": Tag.objects.all(),
        "recent_posts": Post.objects.filter(status="published").order_by("-created_at")[:5],
        "popular_posts": Post.objects.filter(status="published").order_by("-views")[:5],
        "friend_links": FriendLink.objects.filter(is_active=True),
    }
