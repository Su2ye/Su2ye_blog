from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Q
from .models import Post, Category, Tag, Comment


def post_list(request):
    posts = Post.objects.filter(status="published")
    category = None
    tag = None
    query = request.GET.get("q", "")

    if query:
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
        "page_obj": page_obj, "category": category, "tag": tag,
        "query": query, "search_query": query,
    })


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status="published")
    post.increase_views()

    if request.method == "POST":
        name = request.POST.get("name", "").strip()
        body = request.POST.get("body", "").strip()
        if name and body and len(body) >= 2:
            Comment.objects.create(
                post=post, name=name,
                email=request.POST.get("email", "").strip(),
                body=body
            )
        return redirect(post.get_absolute_url())

    comments = post.comments.filter(is_approved=True)
    return render(request, "blog/post_detail.html", {"post": post, "comments": comments})


def category_list(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(status="published", category=category)
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page", 1))
    return render(request, "blog/post_list.html", {"page_obj": page_obj, "category": category})


def tag_list(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(status="published", tags=tag)
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page", 1))
    return render(request, "blog/post_list.html", {"page_obj": page_obj, "tag": tag})


def search(request):
    q = request.GET.get("q", "")
    posts = Post.objects.filter(status="published").filter(
        Q(title__icontains=q) | Q(body__icontains=q) | Q(summary__icontains=q)
    ) if q else Post.objects.none()
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(request.GET.get("page", 1))
    return render(request, "blog/post_list.html", {"page_obj": page_obj, "query": q, "search_query": q})


def about(request):
    return render(request, "blog/about.html")
