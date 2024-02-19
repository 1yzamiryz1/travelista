from django.urls import path

from blog.feeds import LatestEntriesFeed
from blog.views import *

app_name = "blog"

urlpatterns = [
    path("", blog_view, name="blog_view"),
    path("<int:pid>", blog_single, name="single"),
    path("category/<str:cat_name>", blog_view, name="category"),
    path("tag/<str:tag_name>", blog_view, name="tag"),
    path("author/<str:author_username>", blog_view, name="author"),
    path("search/", blog_search, name="search"),
    path('rss/feed/', LatestEntriesFeed())
]