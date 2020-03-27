from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, User
from django.contrib.auth.models import Group
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from firstapp.models import Post, Comment
from user_profile_app.forms import UserForm

def profile(request, username):
    user = get_object_or_404(User, username=username)
    user_group = user.groups.get(user__username__contains=username)
    user_posts = Post.objects.filter(username=username)
    user_comments = Comment.objects.filter(username=username).order_by('-id')
    form = UserForm(instance=user)
    # Пагинация
    paginator = Paginator(user_comments, 2)
    page = request.GET.get('page')
    try:
        user_comments = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не целое число - ставим первую страницу
        user_comments = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимально - ставим последнюю страницу
        user_comments = paginator.page(paginator.num_pages)

    if request.method == 'GET' and request.GET.get('edit'):
            # Права на редактирование профиля, если владелец
            if username == request.user.username:
                return render(request, 'user_profile_app/profile.html', {
                    'user_posts': user_posts, 
                    'form': form,
                    'user': user,
                    'user_group': user_group.name,
                    'user_comments': user_comments,
                    'page': page, 
                })
    
    if request.method == 'POST':
        #user.id = request.user.id
        user.username = request.POST.get('username')
        user.email = request.POST.get('email')
        user.last_name = request.POST.get('last_name')
        user.first_name = request.POST.get('first_name')
        user.save()
        return redirect('profile', username)

    return render(request, 'user_profile_app/profile.html', {
        'user_posts': user_posts, 
        'user': user,
        'user_group': user_group.name,
        'user_comments': user_comments,
        'page': page, 
    })
