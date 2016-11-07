from django.conf.urls import url
from .views import (CategoryListView,
                    CategoryDetailView,
                    CategoryCreateView,
                    CategoryUpdateView,
                    CategoryDeleteView)

urlpatterns = [
    url(r'^$',
        CategoryListView.as_view(),
        name="categories"),
    url(r'^new/$',
        CategoryCreateView.as_view(),
        name="create_category"),
    url(r'^(?P<slug>[\w-]+)/$',
        CategoryDetailView.as_view(),
        name="category_detail"),
    url(r'^(?P<slug>[\w-]+)/edit$',
        CategoryUpdateView.as_view(),
        name="category_update"),
    url(r'^(?P<slug>[\w-]+)/delete$',
        CategoryDeleteView.as_view(),
        name="category_delete"),
]
