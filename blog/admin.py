from django.contrib import admin
from .models import Category, Tag, Post, FriendLink, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "post_count"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ["name", "post_count"]
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["title", "category", "status", "views", "is_top", "created_at"]
    list_filter = ["status", "category", "created_at"]
    search_fields = ["title", "body"]
    prepopulated_fields = {"slug": ("title",)}
    fieldsets = [
        (None, {"fields": ["title", "slug", "author"]}),
        ("内容", {"fields": ["image", "summary", "body"]}),
        ("分类", {"fields": ["category", "tags"]}),
        ("设置", {"fields": ["status", "is_top", "views"]}),
    ]


@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "is_active"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "post", "body_preview", "created_at"]
    list_filter = ["created_at", "post"]
    search_fields = ["name", "body"]

    def body_preview(self, obj):
        return obj.body[:50] + ("..." if len(obj.body) > 50 else "")
    body_preview.short_description = "评论内容"
