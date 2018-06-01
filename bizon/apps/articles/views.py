from django.db.models import Case, IntegerField, F, Sum, Q, When
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.utils import timezone
from django.views.generic import ListView, DetailView

from articles.models import Article, Category

from dal import autocomplete

from taggit.models import Tag


class IndexView(ListView):
    """
    Главная страница сайта.
    """
    model = Article
    paginate_by = 13
    template_name = 'index.html'

    def get_queryset(self):
        qs = super().get_queryset()
        return (qs.select_related('category')
                  .filter(is_published=True, created__lte=timezone.now()))


class CategoryView(ListView):
    """
    Просмотр страницы категории.
    """
    template_name = 'articles/category.html'
    paginate_by = 30
    context_object_name = 'article_list'

    def get_queryset(self):
        """
        Получаем список статей этой категории.
        """
        self.category = get_object_or_404(Category, **self.kwargs)
        return Article.objects.filter(
            is_published=True, created__lte=timezone.now(),
            category__in=self.category.get_descendants(include_self=True))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'category': self.category,
        })
        return context


class ArticleView(DetailView):
    """
    Просмотр страницы статьи.
    """
    context_object_name = 'article'
    related_article_limit = 3
    template_name = 'articles/articles_template/default.html'

    def dispatch(self, request, *args, **kwargs):
        """
        Редирект на правильную категорию статьи, если открывается неправильная.
        """
        article = self.get_object()
        url = article.get_absolute_url()
        if url.split('/')[1] == self.kwargs['category_url']:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(url, permanent=True)

    def get_object(self):
        """
        Получаем статью по её pk и slug, либо возвращаем 404.
        """
        if not getattr(self, '_object', None):
            self._object = get_object_or_404(
                Article, slug=self.kwargs['slug'], pk=self.kwargs['pk'],
                is_published=True, created__lte=timezone.now())
        return self._object

    def get_template_names(self):
        template_name = self.template_name
        article = self.get_object()
        if article.template_name:
            template_name = article.template_name
        return template_name

    def get_context_data(self, **kwargs):
        article = self.get_object()
        Article.objects.filter(pk=article.pk).update(views=F('views') + 1)
        context = super().get_context_data(**kwargs)

        limit = self.related_article_limit
        obj = self.get_object()
        tags = obj.tags.values_list('pk', flat=True)
        related_article_list = (
            Article.objects.select_related('category')
                           .annotate(tags_count=Sum(Case(
                                When(tags__in=tags, then=1),
                                default=0,
                                output_field=IntegerField())))
                           .filter(tags_count__gt=0, is_published=True)
                           .exclude(pk=obj.pk)
                           .order_by('-tags_count')[:limit])
        context.update({
            'related_article_list': related_article_list,
        })
        return context


class TagAutocomplete(autocomplete.Select2QuerySetView):
    """
    Поиск тэгов для автокомплита.
    """
    def get_queryset(self):
        # Don't forget to filter out results depending on the visitor !
        if not self.request.user.is_authenticated:
            return Tag.objects.none()

        qs = Tag.objects.all()

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs


class ArticleTagView(ListView):
    """
    Список статей по тэгу.
    """
    model = Article
    template_name = 'articles/article_tag.html'

    def get_queryset(self):
        """
        Фильтруем статьи по тэгу.
        """
        qs = super().get_queryset()
        tag_slug = self.kwargs['slug']
        return qs.select_related('category').filter(
            tags__slug=tag_slug, is_published=True,
            created__lte=timezone.now())

    def get_context_data(self, *args, **kwargs):
        """
        Добавляем тэг в контекст.
        """
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'tag': Tag.objects.get(slug=self.kwargs['slug']),
        })
        return context


class ArticleSearchView(ListView):
    """
    Результаты поиска статей.
    """
    model = Article
    template_name = 'articles/article_search.html'

    def get_queryset(self):
        """
        Фильтруем статьи по запросу поиска.
        """
        qs = super().get_queryset()
        q = self.request.GET.get('q')
        return (qs.select_related('category')
                  .filter(Q(title__icontains=q) | Q(text__icontains=q),
                          is_published=True, created__lte=timezone.now()))

    def get_context_data(self, *args, **kwargs):
        """
        Добавляем запрос поиска в контекст.
        """
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'search': self.request.GET.get('q'),
        })
        return context
