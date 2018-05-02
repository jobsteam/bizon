from django.urls import path

from articles import views as articles_views


app_name = 'articles'

urlpatterns = [
    path('autocomplete/', articles_views.TagAutocomplete.as_view(),
         name='tag-autocomplete'),
    path('tags/<slug:slug>/', articles_views.ArticleTagView.as_view(),
         name='tag'),
    path('search/', articles_views.ArticleSearchView.as_view(),
         name='search'),
    path('<slug:slug>-<int:pk>/', articles_views.CategoryView.as_view(),
         name='category'),
    path('<slug:category_url>/<slug:slug>-<int:pk>/',
         articles_views.ArticleView.as_view(), name='article'),
]
