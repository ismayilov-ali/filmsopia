from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Post, Like, Favorite, Hometext


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