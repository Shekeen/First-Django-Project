from django.contrib import admin
from Blog.models import BlogPost


class BlogPostAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['title', 'text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    list_display = ('title', 'text_snippet', 'pub_date', 'was_recently_published')
    list_filter = ['pub_date']
    search_fields = ['title']
    date_hierarchy = 'pub_date'


admin.site.register(BlogPost, BlogPostAdmin)
