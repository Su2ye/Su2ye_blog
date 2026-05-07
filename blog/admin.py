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
        ("设置", {"fields": ["status", "is_top", "views", "created_at"]}),
    ]


@admin.register(FriendLink)
class FriendLinkAdmin(admin.ModelAdmin):
    list_display = ["name", "url", "is_active"]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ["name", "post", "body_preview", "is_approved", "created_at"]
    list_filter = ["is_approved", "created_at", "post"]
    search_fields = ["name", "body"]
    actions = ["approve_comments"]

    def body_preview(self, obj):
        return obj.body[:50] + ("..." if len(obj.body) > 50 else "")
    body_preview.short_description = "评论内容"

    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, f"已审核通过 {queryset.count()} 条评论")
    approve_comments.short_description = "批量审核通过"
