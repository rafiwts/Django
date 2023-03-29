from django.contrib import admin
from .models import Post, Comment


class PostAdmin(admin.ModelAdmin): # changing the visual output using ModelAdmin
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    list_filter = ('status', 'created', 'publish', 'author') # adding a window to filter posts using given categories
    search_fields = ('title', 'body') # searching for posts using given categories
    prepopulated_fields = {'slug': ('title',)} # automatic creation of slug using a title
    raw_id_fields = ('author',) # searching for an author of a post
    date_hierarchy = 'publish'
    ordering = ['status', 'publish'] # ordering posts by status and publish columns

admin.site.register(Post, PostAdmin) # registering Post model to admin site, class as one of the parameters


class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')

admin.site.register(Comment, CommentAdmin)
# Register your models here.
