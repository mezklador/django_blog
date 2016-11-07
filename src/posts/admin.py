from django.contrib import admin
from .models import Post

class PostModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Post

    list_display = ['title', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['title', 'content']

admin.site.register(Post, PostModelAdmin)
