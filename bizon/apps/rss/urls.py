from django.urls import path

from rss import views as rss_views


app_name = 'rss'

urlpatterns = [
    path('zen/', rss_views.ZenRSSView.as_view(), name='zen'),
    path('nova/', rss_views.NovaRSSView.as_view(), name='nova'),
]
