import os

from django.conf import settings
from django.template.utils import get_app_template_dirs


def get_available_page_templates():
    """
    Получаем названия доступных шаблонов для Pages во всех приложениях проекта.
    """
    template_files = []
    for template_dir in get_app_template_dirs('templates'):
        pages_template_dir = '%s/%s' % (template_dir,
                                        settings.ARTICLES_TEMPLATE_DIR)
        if os.path.isdir(pages_template_dir):
            for file in os.listdir(pages_template_dir):
                if file.endswith('.html'):
                    template_files.append(file[:-5])
    return list(set(template_files))
