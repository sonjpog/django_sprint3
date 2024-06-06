from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404

from blog.models import Category
from .utils import get_posts


def index(request: HttpRequest) -> HttpResponse:
    posts = get_posts()[:settings.POSTS_BY_PAGE]
    template = 'blog/index.html'
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(
        get_posts(),
        id=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True)

    posts = get_posts(category=category)
    template = 'blog/category.html'
    context = {
        'category': category,
        'post_list': posts,
        'slug': category_slug,
    }
    return render(request, template, context)
