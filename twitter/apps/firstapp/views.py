from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm, User
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.postgres.search import SearchVector
from django.contrib.auth.decorators import login_required
from .forms import PostForm, LoginForm, CommentForm, SearchForm
from .models import Post, Comment
from webhook.base import WebhookBase
import datetime


def index(request):
    post_list = Post.objects.all().order_by('-id')

    # Пагинация
    paginator = Paginator(post_list, 10)
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        # Если страница не целое число - ставим первую страницу
        posts = paginator.page(1)
    except EmptyPage:
        # Если страница больше максимально - ставим последнюю страницу
        posts = paginator.page(paginator.num_pages)
    
    # res = Post.objects.annotate(search=SearchVector('title', 'text'),).filter(search='')
    # print(res)
    
    return render(request, 'firstapp/index.html', {
        'form': PostForm, 
        'page': page, 
        'posts': posts, 
    })

# Войти
def sign_in(request):
    form = LoginForm()
    valid = 'false'
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username = username, password = password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
            else:
                messages.error(request, 'Ваш аккаунт отключен')
        else:
            messages.error(request, 'Неверный логин или пароль')
    return render(request, 'firstapp/sign_in.html', {'form': form, 'valid': valid})

# Зарегистрироваться
def sign_up(request):
    form = UserCreationForm()
    if request.method == 'POST':
        user = UserCreationForm(request.POST)
        user = user.save()
        login(request, user)
        return redirect('index')      
    return render(request, 'firstapp/sign_up.html', {'form': form})

# Выйти
def logout_view(request):
    logout(request)
    return redirect('index')

# Создать пост
def create_post(request):
    if request.method == 'POST':
        # Походу передаю не PostForm
        post = Post()
        post.username = request.user.username
        post.datetime = datetime.datetime.now()
        post.title = request.POST.get('title')
        post.text = request.POST.get('text')
        if 'image' in request.FILES:
            post.image = request.FILES['image']

        print(request.POST)
        if request.POST.get('Редактировать'):
            post.changed = True

        post.save()
    return HttpResponseRedirect('/')

# Открыть пост
@login_required(login_url='/login/')
def post_detail(request, post_id):

    post = get_object_or_404(Post, id=post_id)
    comment = Comment.objects.filter(post_id = post_id)
    comment_form = CommentForm()

    # Проверка на лайк
    user_tags = User.objects.filter(users_post_like = post_id)
    current_user = request.user
    if current_user not in user_tags:
        # Не лайкал
        user_liked_it = None
    else:
        # Лайкал
        user_liked_it = True
    
    # Запись в список пользователей, смотревших пост и счетчик количества просмотров
    post.viewdone.add(current_user)
    post.viewcount += 1
    post.save()    

    return render(request, 'firstapp/post_detail.html', {
        'post': post,
        'comment': comment, 
        'comment_form': comment_form, 
        # Bool проверка на лайк данным пользователем данного поста
        'user_liked_it': user_liked_it,
        # id пользователей, лайкнувших пост
        'user_tags': user_tags,
    })

# Оставить комментарий
def add_comment(request, post_id):
    if request.method == 'POST':
        comment = Comment()
        comment.username = request.user.username
        comment.datetime = datetime.datetime.now()
        comment.post_id = post_id
        comment.text = request.POST.get('text')
        comment.save()
    return redirect('post_detail', post_id)

# Поставить лайк
def like(request, post_id):
    if request.method == 'GET':
        post = Post.objects.get(id = post_id)
        user_tags = User.objects.filter(users_post_like = post_id)
        current_user = request.user
        if current_user not in user_tags:
            post.thumbnumber += 1
            post.likedone.add(current_user)
            post.save()
            return redirect('post_detail', post_id)
        else:
            post.thumbnumber -= 1
            post.likedone.remove(current_user)
            post.save()
            return redirect('post_detail', post_id)
    return redirect('post_detail', post_id)

# Поиск по сайту
def search(request):
    form = SearchForm()
    #if request.method == 'POST':
        
    return render(request, 'firstapp/search.html', {'form': form})

# Результат поиска
def search_result(request):
    if request.method == 'POST':
        form = SearchForm()
        query = request.POST.get('query')
        search_title = request.POST.get('search_title')
        search_text = request.POST.get('search_text')

        title_result = None
        text_result = None

        if search_title:
            title_result = Post.objects.filter(title__icontains=query)
        
        if search_text:
            text_result = Post.objects.filter(text__icontains=query)

        return render(request, 'firstapp/search_result.html', {
                'form': form,
                'query': query,
                'title_result': title_result,
                'text_result': text_result
        })

    return redirect('search')

def edit_post(request, username, post_id):
    post = get_object_or_404(Post, id = post_id)
    if request.user.username == username:
        form = PostForm(instance=post)
        return render(request, 'firstapp/edit_post.html', {'form': form, 'post_id': post_id})
    return redirect('/')

def edit_post_save(request, username):
    if request.method == 'POST' and username == request.user.username:
        post = Post.objects.get(id = request.POST.get('post_id'))
        if username == post.username:
            post.id = request.POST.get('post_id')
            post.title = request.POST.get('title')
            post.text = request.POST.get('text')
            post.changed_datetime = datetime.datetime.now()
            post.username = request.user.username
            post.changed = True
            post.save()
            return redirect('post_detail', post.id)
