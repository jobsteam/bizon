import re

from django.conf import settings
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from ckeditor_uploader.fields import RichTextUploadingField

from mptt.models import MPTTModel, TreeForeignKey

from polymorphic.models import PolymorphicModel

from sorl.thumbnail import ImageField

from transliterate import translit

from taggit.managers import TaggableManager
from taggit.models import Tag

from articles.utils import get_available_page_templates


class Author(models.Model):
    """
    Модель `Автор`.
    """
    last_name = models.CharField(
        'фамилия',
        max_length=254)
    name = models.CharField(
        'имя',
        max_length=254)
    patronymic = models.CharField(
        'отчество',
        max_length=254)

    class Meta:
        ordering = ['last_name', 'name']
        verbose_name = 'автор'
        verbose_name_plural = 'авторы'

    def __str__(self):
        return '%s %s' % (self.last_name, self.name)


class Article(PolymorphicModel):
    """
    Модель `Статья`.
    """
    TEMPLATE_CHOICES = [
        ('%s/%s.html' % (settings.ARTICLES_TEMPLATE_DIR, template), template)
        for template in get_available_page_templates()]

    title = models.CharField(
        'название',
        max_length=254, db_index=True)
    slug = models.SlugField(
        'slug',
        allow_unicode=False, blank=True)
    category = models.ForeignKey(
        'articles.Category',
        on_delete=models.CASCADE,
        verbose_name='категория',
        related_name='articles')
    cover = ImageField(
        'обложка',
        upload_to='cover', blank=True, null=True)
    background = ImageField(
        'задник',
        upload_to='background', blank=True, null=True)
    intro = models.TextField(
        'анонс',
        blank=True)
    text = RichTextUploadingField(
        'текст',
        blank=True)
    created = models.DateTimeField(
        'дата создания',
        default=timezone.now)
    updated = models.DateTimeField(
        'дата изменения',
        editable=False, auto_now=True)
    views = models.PositiveIntegerField(
        'кол-во просмотров',
        default=0)
    authors = models.ManyToManyField(
        'articles.Author',
        verbose_name='авторы',
        related_name='articles',
        blank=True)
    is_published = models.BooleanField(
        'опубликовано',
        default=True)
    is_marquee = models.BooleanField(
        'бегущая строка',
        default=False)
    template_name = models.CharField(
        'шаблон',
        choices=TEMPLATE_CHOICES,
        default='%s/default.html' % settings.ARTICLES_TEMPLATE_DIR,
        max_length=254)

    tags = TaggableManager()

    class Meta:
        ordering = ['-created']
        verbose_name = 'статья'
        verbose_name_plural = 'статьи'

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('articles:article', kwargs={
            'slug': self.slug,
            'pk': self.pk,
            'category_url': '%s-%s' % (self.category.slug, self.category.pk),
        })

    @property
    def text_images(self):
        pattern = r'img.*src\=[\"\'](\S*)[\"\']'
        return re.findall(pattern, self.text)


class News(Article):
    """
    Модель `Новость`.
    """
    class Meta:
        verbose_name = 'новость'
        verbose_name_plural = 'новости'


class Reading(Article):
    """
    Модель `Чтиво`.
    """
    class Meta:
        verbose_name = 'чтиво'
        verbose_name_plural = 'чтиво'


class Future(Article):
    """
    Модель `Будущее`.
    """
    class Meta:
        verbose_name = 'будущее'
        verbose_name_plural = 'будущее'


class Globe(Article):
    """
    Модель `Глобус`.
    """
    class Meta:
        verbose_name = 'глобус'
        verbose_name_plural = 'глобусы'


class Fun(Article):
    """
    Модель `Каламбур`.
    """
    class Meta:
        verbose_name = 'каламбур'
        verbose_name_plural = 'каламбуры'


class Media(Article):
    """
    Модель `Медиа`.
    """
    class Meta:
        verbose_name = 'медиа'
        verbose_name_plural = 'медиа'


class Category(MPTTModel):
    ARTICLE_TYPE_CHOICES = (
        ('news', 'Новость'),
        ('reading', 'Чтиво'),
        ('future', 'Будущее'),
        ('globe', 'Глобус'),
        ('fun', 'Каламбур'),
        ('media', 'Медиа'),
    )

    title = models.CharField(
        'название',
        max_length=254, db_index=True)
    slug = models.SlugField(
        'slug',
        allow_unicode=False)
    parent = TreeForeignKey(
        'self',
        verbose_name='родительская категория',
        related_name='children',
        on_delete=models.CASCADE,
        null=True, blank=True, db_index=True)
    article_type = models.CharField(
        'тип статьи',
        choices=ARTICLE_TYPE_CHOICES, default='News', max_length=254,
        db_index=True)

    class MPTTMeta:
        order_insertion_by = ['title']

    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('articles:category', kwargs={'slug': self.slug,
                                                    'pk': self.pk})


class Photo(models.Model):
    """
    Модель для галереи новостей.
    """
    article = models.ForeignKey(
        'articles.Article',
        on_delete=models.CASCADE,
        verbose_name='статья',
        related_name='gallery')
    title = models.CharField(
        'название',
        max_length=254, blank=True)
    pic = ImageField(
        'изображение',
        upload_to='gallery')
    description = models.TextField(
        'описание',
        blank=True)
    author = models.CharField(
        'автор',
        max_length=254, blank=True)

    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'

    def __str__(self):
        return str(self.pk)


@receiver(post_save, sender=Tag)
def update_tag_slug(sender, instance, created, **kwargs):
    """
    Исправляем slug при создании нового тэга.
    """
    if created is True:
        sender.objects.filter(pk=instance.pk).update(
            slug=slugify(translit(instance.name, 'ru', reversed=True)))
