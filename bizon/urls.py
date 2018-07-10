from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import path
from django.views.generic import RedirectView, TemplateView

from articles.views import IndexView


urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('favicon.ico', RedirectView.as_view(
        url=staticfiles_storage.url('favicon.ico'), permanent=True)),
    path('robots.txt', TemplateView.as_view(
        template_name='robots.txt', content_type='text/plain')),
    path('sdkfjvvr237rufhklsd.txt', TemplateView.as_view(
        template_name='sdkfjvvr237rufhklsd.txt', content_type='text/plain')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path('rss/', include('rss.urls')),
    path('', include('articles.urls')),
]


# DEBUG TOOLBAR
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


# Тестировать 404 страницу
if settings.DEBUG404:
    from django.views.static import serve

    urlpatterns += [
        path('media/<path:path>/',
             serve, {'document_root': settings.MEDIA_ROOT}),
        path('static/<path:path>/',
             serve, {'document_root': settings.STATIC_ROOT})
    ]
