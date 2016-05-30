from django.contrib import admin
from blogpost.models import Blogpost

# Register your models here.
class BlogpostAdmin(admin.ModelAdmin):
    """docstring for BlogpostAdmin"""
    exclude = ['posted']
    prepopulated_fields = {'slug': ('title', )}

admin.site.register(Blogpost, BlogpostAdmin)
