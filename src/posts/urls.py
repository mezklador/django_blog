from django.conf.urls import url
from django.contrib import admin
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

#app_name = "posts"

urlpatterns = [
    url(r'^$',
        BlogListView.as_view(),
        name="blog_list"),
    url(r'^(?P<pk>\d+)$',
        BlogDetailView.as_view(),
        name='post_detail'),
    url(r'^new/$',
        BlogCreateView.as_view(),
        name="new_post"),
    url(r'^(?P<pk>\d+)/edit$',
        BlogUpdateView.as_view(),
        name="update_post"),
    url(r'^(?P<pk>\d+)/destroy$',
        BlogDeleteView.as_view(),
        name="delete_post"),
]
