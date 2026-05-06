from django.urls import path
from . import views
from .feeds import LatestPostsFeed

app_name = "blog"

urlpatterns = [
    path("", views.post_list, name="home"),
    path("post/<slug:slug>/", views.post_detail, name="post_detail"),
    path("category/<slug:slug>/", views.category_list, name="category"),
    path("tag/<slug:slug>/", views.tag_list, name="tag"),
    path("about/", views.about, name="about"),
    path("rss/", LatestPostsFeed(), name="rss"),
    path("search/", views.post_list, name="search"),
]
