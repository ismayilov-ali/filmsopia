from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'), 
    path('blog/', views.blog_page, name='blog_page'),
    path('posts/', views.posts_page, name='posts_page'),
    path('post/<slug>/', views.post, name='post'),
    path('posts/', views.post_list, name='post_list'),
]