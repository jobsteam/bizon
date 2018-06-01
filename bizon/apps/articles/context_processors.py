from datetime import timedelta

from django.utils import timezone
from django.db.models import Q

from articles.models import Article, Category


def articles(request):
    """
    Добавляем в контекст блоки со статьями.
    """
    category_url = request.resolver_match.kwargs.get('category_url')
    current_article_pk = request.resolver_match.kwargs.get('pk')

    exclude_params = {}
    if category_url and current_article_pk:
        exclude_params = {'pk': current_article_pk}

    return {
        'root_categories': Category.objects.filter(level=0),

        'article_top_list': (
            Article.objects
                   .select_related('category')
                   .filter(Q(created__gte=timezone.now()-timedelta(days=7)) &
                           Q(created__lte=timezone.now()),
                           is_published=True)
                   .order_by('-views'))[:7],

        'article_last_list': (
            Article.objects
                   .select_related('category')
                   .filter(is_published=True, created__lte=timezone.now())
                   .exclude(**exclude_params))[:2],

        'article_marquee_list': (
            Article.objects
                   .filter(is_marquee=True, is_published=True,
                           created__lte=timezone.now()))[:8],
    }
