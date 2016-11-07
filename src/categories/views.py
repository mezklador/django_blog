from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import (ListView,
                                  DetailView)
from django.views.generic.edit import (CreateView,
                                       UpdateView,
                                       DeleteView)
from .models import Category


class CategoryListView(ListView):
    model = Category
    context_object_name = 'all_categories'

    def get_queryset(self):
        querylist = Category.objects.all()
        # Maybe I have to plan a GET method for searching category?
        return querylist

class CategoryDetailView(DetailView):
    model = Category


class CategoryCreateView(CreateView):
    model = Category
    fields = ['label', 'description']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CategoryCreateView, self).dispatch(*args, **kwargs)

class CategoryUpdateView(UpdateView):
    model = Category
    fields = ['label', 'description']

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CategoryUpdateView, self).dispatch(*args, **kwargs)


class CategoryDeleteView(DeleteView):
    model = Category

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(CategoryDeleteView, self).dispatch(*args, **kwargs)

