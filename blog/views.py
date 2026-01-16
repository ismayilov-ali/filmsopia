from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Like, Favorite, Hometext, Comment
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegisterForm
from django.contrib import messages
from django.contrib.auth.models import User

def blog_page(request):
    return render(request, 'blog_page.html')

def posts_page(request):
    return render(request, 'posts_page.html')

def home_page(request):
    hometext = Hometext.objects.all()

    context = {
        'hometext': hometext
    }
    return render(request, 'home_page.html', context)

def post(request, id):
    post = get_object_or_404(Post, id=id)
    # Like vəziyyətini yoxla
    user_has_liked = False
    user_has_favorited = False

    if request.user.is_authenticated:
        user_has_liked = post.likes.filter(user=request.user).exists()
        user_has_favorited = post.favorites.filter(user=request.user).exists()

    context = {
        'post': post,
        'user_has_liked': user_has_liked,
        'user_has_favorited': user_has_favorited
    }
    return render(request, 'post_detail.html', context)

def post_list(request):
    posts = Post.objects.all()
    return render(request, 'post_list.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    
    # Like vəziyyətini yoxla
    user_has_liked = False
    if request.user.is_authenticated:
        user_has_liked = post.likes.filter(user=request.user).exists()
    
    context = {
        'post': post,
        'user_has_liked': user_has_liked,
    }
    return render(request, 'post_detail.html', context)

@login_required
def comment_post(request, post_id):
    if request.method == 'POST':
        post = get_object_or_404(Post, id=post_id)
        content = request.POST.get('content')
        
        if content and content.strip():
            Comment.objects.create(
                post=post,
                user=request.user,
                content=content.strip()
            )
    
    return redirect('blog:post_detail', id=post_id)

@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    
    if not created:
        like.delete()
        liked = False
    else:
        liked = True
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': post.likes.count()
        })
    
    return redirect('blog:post_detail', id=post_id)

@login_required
def favorite_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    favorite, created = Favorite.objects.get_or_create(user=request.user, post=post)

    if not created:
        favorite.delete()
        favorited = False
    else:
        favorited = True

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'favorited': favorited,
            'total_favorites': post.favorites.count()
        })
    
    return redirect('blog:post_detail', id=post_id)

def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Qeydiyyat uğurla tamamlandı!')
            return redirect('blog:home_page')
    else:
        form = UserRegisterForm()
    
    context = {'form': form}
    return render(request, 'register.html', context)

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Xoş gəldiniz, {username}!')
                next_url = request.GET.get('next', 'blog:home_page')
                return redirect(next_url)
        else:
            messages.error(request, 'bele bir istifadeci yoxdu!')
    else:
        form = AuthenticationForm()
    
    context = {'form': form}
    return render(request, 'login.html', context)

def logout_view(request):
    logout(request)
    messages.info(request, 'Çıxış etdiniz.')
    return redirect('blog:home_page')

def user_profile(request, username):
    """İstifadəçi profil səhifəsi"""
    profile_user = get_object_or_404(User, username=username)
    
    # İstifadəçinin şərhləri
    user_comments = Comment.objects.filter(user=profile_user).select_related('post')
    
    # İstifadəçinin like etdiyi postlar
    liked_posts = Post.objects.filter(likes__user=profile_user).distinct()
    
    # İstifadəçinin favorite etdiyi postlar
    favorited_posts = Post.objects.filter(favorites__user=profile_user).distinct()
    
    # Statistika
    stats = {
        'total_comments': user_comments.count(),
        'total_likes': liked_posts.count(),
        'total_favorites': favorited_posts.count(),
    }
    
    context = {
        'profile_user': profile_user,
        'user_comments': user_comments[:10],  # Son 10 şərh
        'liked_posts': liked_posts[:6],  # Son 6 like
        'favorited_posts': favorited_posts[:6],  # Son 6 favorite
        'stats': stats,
    }
    
    return render(request, 'user_profile.html', context)