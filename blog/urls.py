from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home_page, name='home_page'), 
    path('blog/', views.blog_page, name='blog_page'),
    path('aslam/', views.posts_page, name='posts_page'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:id>/', views.post, name='post_detail'),

]

