from django.db.models import Q
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import Post, Category, Tag


def post_list(request):
    """首页：文章列表 + 搜索"""
    posts = Post.objects.filter(status="published")
    search_query = ""

    query = request.GET.get("q", "").strip()
    if query:
        search_query = query
        posts = posts.filter(
            Q(title__icontains=query) | Q(body__icontains=query) | Q(summary__icontains=query)
        )

    page = request.GET.get("page", 1)
    paginator = Paginator(posts, 10)
    try:
        page_obj = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(request, "blog/post_list.html", {
        "page_obj": page_obj,
        "search_query": search_query,
        "page_title": "首页",
    })


def post_detail(request, slug):
    """文章详情页"""
    post = get_object_or_404(Post, slug=slug, status="published")
    post.increase_views()
    return render(request, "blog/post_detail.html", {
        "post": post,
        "page_title": post.title,
    })


def category_list(request, slug):
    """分类文章列表"""
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status="published")
    paginator = Paginator(posts, 10)
    page = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(request, "blog/post_list.html", {
        "page_obj": page_obj,
        "search_query": "",
        "page_title": f"分类：{category.name}",
        "category": category,
    })


def tag_list(request, slug):
    """标签文章列表"""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status="published")
    paginator = Paginator(posts, 10)
    page = request.GET.get("page", 1)
    try:
        page_obj = paginator.page(page)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)

    return render(request, "blog/post_list.html", {
        "page_obj": page_obj,
        "search_query": "",
        "page_title": f"标签：{tag.name}",
        "tag": tag,
    })


def about(request):
    """关于页面"""
    return render(request, "blog/about.html", {"page_title": "关于"})
