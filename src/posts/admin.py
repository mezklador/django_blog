from django.contrib import admin
from .models import Post, Category

class PostModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Post

    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'content']

class CategoryModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Category

admin.site.register(Post, PostModelAdmin)
admin.site.register(Category, CategoryModelAdmin)
