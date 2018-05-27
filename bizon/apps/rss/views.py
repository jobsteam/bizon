from datetime import timedelta

from django.utils import timezone

from django.views.generic import ListView

from articles.models import Article


class ZenRSSView(ListView):
    """
    RSS для yandex zen.
    """
    content_type = 'text/xml'
    model = Article
    template_name = 'rss/zen.xml'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created__gte=timezone.now()-timedelta(days=3),
                         is_published=True)


class NovaRSSView(ListView):
    """
    RSS для yandex zen.
    """
    content_type = 'text/xml'
    model = Article
    template_name = 'rss/nova.xml'

    def get_queryset(self):
        qs = super().get_queryset()
        return qs.filter(created__gte=timezone.now()-timedelta(days=3),
                         is_published=True)
