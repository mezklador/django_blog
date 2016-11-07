from django.contrib import admin
from .models import Category

class CategoryModelAdmin(admin.ModelAdmin):
    class Meta:
        model = Category

    list_display = ['label', 'slug', 'created_at', 'updated_at']
    list_filter = ['created_at', 'updated_at']
    search_fields = ['label', 'description']


admin.site.register(Category, CategoryModelAdmin)
