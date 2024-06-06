from django.utils.timezone import now
from blog.models import Post


def get_posts(**filters):
    return Post.objects.select_related(
        'author', 'category', 'location',
    ).filter(
        is_published=True,
        pub_date__lt=now(),
        category__is_published=True,
        **filters
    )
