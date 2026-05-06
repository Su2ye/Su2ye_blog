from django.contrib.syndication.views import Feed
from django.urls import reverse
from .models import Post


class LatestPostsFeed(Feed):
    title = "Su2ye 的博客"
    link = "/"
    description = "最新文章更新"

    def items(self):
        return Post.objects.filter(status="published").order_by("-created_at")[:20]

    def item_title(self, item):
        return item.title

    def item_description(self, item):
        return item.summary

    def item_link(self, item):
        return reverse("blog:post_detail", kwargs={"slug": item.slug})

    def item_pubdate(self, item):
        return item.created_at
