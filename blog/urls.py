from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.home_page, name='home_page'), 
    path('blog/', views.blog_page, name='blog_page'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:id>/', views.post, name='post_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/favorite/', views.favorite_post, name='favorite_post'),
    path('post/<int:post_id>/comment/', views.comment_post, name='comment'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'), 
    path('user/<str:username>/', views.user_profile, name='user_profile'),
]
