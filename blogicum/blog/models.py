from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model

User = get_user_model()


class InheritableOrderingMeta(models.base.ModelBase):
    def __new__(cls, name, bases, attrs):
        new_class = super().__new__(cls, name, bases, attrs)
        if 'Meta' in attrs:
            meta = attrs['Meta']
            if hasattr(meta, 'ordering'):
                if not getattr(new_class._meta, 'abstract', False):
                    if not hasattr(new_class._meta, 'ordering'):
                        new_class._meta.ordering = meta.ordering
        return new_class


class PublishedModel(models.Model, metaclass=InheritableOrderingMeta):
    is_published = models.BooleanField(
        'Опубликовано',
        default=True,
        help_text='Снимите галочку, чтобы скрыть публикацию.'
    )
    created_at = models.DateTimeField('Добавлено', auto_now_add=True)

    class Meta:
        abstract = True
        ordering = ('created_at', )


class Location(PublishedModel):
    name = models.CharField(
        'Название места', max_length=settings.MAX_FIELD_LENGTH)

    class Meta:
        verbose_name = 'местоположение'
        verbose_name_plural = 'Местоположения'

    def __str__(self) -> str:
        return self.name[:settings.REPRESENTATION_LENGTH]


class Category(PublishedModel):
    title = models.CharField('Заголовок', max_length=settings.MAX_FIELD_LENGTH)
    description = models.TextField('Описание')
    slug = models.SlugField(
        'Идентификатор',
        max_length=settings.MAX_FIELD_LENGTH,
        unique=True,
        help_text=(
            'Идентификатор страницы для URL; '
            'разрешены символы латиницы, цифры, '
            'дефис и подчёркивание.'
        )
    )

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return self.title[:settings.REPRESENTATION_LENGTH]


class Post(PublishedModel):
    title = models.CharField('Заголовок', max_length=settings.MAX_FIELD_LENGTH)
    text = models.TextField('Текст')
    pub_date = models.DateTimeField(
        'Дата и время публикации',
        help_text=(
            'Если установить дату и время в будущем — можно '
            'делать отложенные публикации.'
        )
    )
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name='Автор публикации'
    )
    location = models.ForeignKey(
        Location, on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name='Местоположение'
    )
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True,
        verbose_name='Категория'
    )

    class Meta:
        default_related_name = 'posts'
        verbose_name = 'публикация'
        verbose_name_plural = 'Публикации'
        ordering = ('-pub_date', 'created_at')

    def __str__(self):
        return self.title[:settings.REPRESENTATION_LENGTH]
