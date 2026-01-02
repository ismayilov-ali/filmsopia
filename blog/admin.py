from django.contrib import admin
from .models import Post, Like, Favorite, Hometext


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ('title', 'content')

@admin.register(Like)
class PostLike(admin.ModelAdmin):
    list_display = ['user', 'post']
    list_filter = ['user', 'post']
    search_fields = ['user__username', 'post__title']

@admin.register(Favorite)
class PostFavorite(admin.ModelAdmin):
    list_display = ['user', 'post']

@admin.register(Hometext)
class home_pageAdmin(admin.ModelAdmin):
    search_fields = ('title', 'content')
    list_display = ('title', 'content')
    list_filter = ('title',)
    ordering = ('title',)