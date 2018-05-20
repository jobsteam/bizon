from django.contrib import admin
from django.forms import ModelForm

from dal import autocomplete

from mptt.admin import DraggableMPTTAdmin

from sorl.thumbnail.admin import AdminImageMixin

from articles import models as articles_models


@admin.register(articles_models.Category)
class CategoryAdmin(DraggableMPTTAdmin):
    prepopulated_fields = {
        'slug': (
            'title',
        )
    }


@admin.register(articles_models.Author)
class AuthorAdmin(admin.ModelAdmin):
    pass


class GalleryAdmin(AdminImageMixin, admin.StackedInline):
    classes = ['collapse']
    extra = 1
    model = articles_models.Photo


class BaseArticleAdminForm(ModelForm):
    class Meta:
        widgets = {
            'tags': autocomplete.TaggitSelect2('articles:tag-autocomplete'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        model_name = self.Meta.model._meta.model_name
        category_queryset = self.fields['category'].queryset
        self.fields['category'].queryset = category_queryset.filter(
            article_type=model_name, parent__isnull=False)


class BaseArticleAdmin(AdminImageMixin, admin.ModelAdmin):
    form = BaseArticleAdminForm

    search_fields = ['title']

    inlines = [
        GalleryAdmin,
    ]

    list_display = [
        'title',
        'created',
    ]

    list_filter = [
        'created',
        'authors',
    ]

    prepopulated_fields = {
        'slug': (
            'title',
        )
    }


@admin.register(articles_models.News)
class NewsAdmin(BaseArticleAdmin):
    pass


@admin.register(articles_models.Reading)
class ReadingAdmin(BaseArticleAdmin):
    pass


@admin.register(articles_models.Future)
class FutureAdmin(BaseArticleAdmin):
    pass


@admin.register(articles_models.Globe)
class GlobeAdmin(BaseArticleAdmin):
    pass


@admin.register(articles_models.Fun)
class FunAdmin(BaseArticleAdmin):
    pass


@admin.register(articles_models.Media)
class MediaAdmin(BaseArticleAdmin):
    pass
