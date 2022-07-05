from django.shortcuts import render, get_object_or_404
from .models import Group, Post


POSTS_PER_PAGE = 10


def index(request):
    template = 'posts/index.html'
    title = 'Главная страница'
    text = 'Это главная страница проекта Yatube'
    posts = Post.objects.select_related('author')[:POSTS_PER_PAGE]
    context = {
        'title': title,
        'text': text,
        'posts': posts,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    title = 'Список сообществ'
    text = 'Здесь будет информация о группах проекта Yatube'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:POSTS_PER_PAGE]
    context = {
        'title': title,
        'text': text,
        'group': group,
        'posts': posts,
    }
    return render(request, template, context)
