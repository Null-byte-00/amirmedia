from django.contrib import admin
from .models import Post
# Register your models here.


@admin.register(Post)
class Postadmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ['title']}
    list_display = ['user', 'title', 'text', 'date_published', 'tags', 'slug']
    list_filter = ['date_published']
    search_fields = ['title', 'tags']
