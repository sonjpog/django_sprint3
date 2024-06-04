from django.conf import settings
from django.http import HttpResponse, HttpRequest
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import now


from blog.models import Post, Category


def index(request: HttpRequest) -> HttpResponse:
    posts = Post.objects.select_related(
        'author', 'category', 'location',
    ).filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True,
    )[:settings.POSTS_BY_PAGE]
    template = 'blog/index.html'
    context = {'post_list': posts}
    return render(request, template, context)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related('author', 'category', 'location',
                                    ).filter(
            is_published=True,
            pub_date__lt=now(),
            category__is_published=True,
        ),
        id=post_id
    )
    return render(request, 'blog/detail.html', {'post': post})


def category_posts(request, category_slug):
    category = get_object_or_404(
        Category, slug=category_slug, is_published=True)

    posts = Post.objects.select_related('author', 'category', 'location').filter(
        category=category,
        is_published=True,
        pub_date__lt=now(),
    )

    template = 'blog/category.html'
    context = {
        'category': category,
        'post_list': posts,
        'slug': category_slug,
    }
    return render(request, template, context)
