from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = 'blog'

urlpatterns = [
    path('', views.home_page, name='home_page'),
    path('blog/', views.blog_page, name='blog_page'),
    path('posts/', views.post_list, name='post_list'),
    path('post/<int:id>/', views.post, name='post_detail'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('post/<int:post_id>/favorite/', views.favorite_post, name='favorite_post'),
    path('post/<int:post_id>/comment/', views.comment_post, name='comment'),

    # Auth URLs
    path('signup/', views.sign_up, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
