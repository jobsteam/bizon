import os
import sys


TEST = 'test' in sys.argv
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def path(*a):
    return os.path.join(BASE_DIR, *a)


# This trick allows to import apps without that prefixes
sys.path.insert(0, path('apps'))
sys.path.insert(0, path('libs'))
sys.path.insert(1, path('.'))


ROOT_URLCONF = 'bizon.urls'
WSGI_APPLICATION = 'bizon.wsgi.application'

ALLOWED_HOSTS = ['bizon.news']


INSTALLED_APPS = [
    'dal',
    'dal_select2',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.gis',
    'django.contrib.staticfiles',
    'polymorphic',
    'mptt',
    'django_extensions',
    'djangoyarn',
    'pipeline',
    'ckeditor',
    'ckeditor_uploader',
    'taggit',
    'sorl.thumbnail',
    'libs',
    'articles',
    'rss',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
# -----------------------------------------------------------------------------


# TEMPLATES -------------------------------------------------------------------
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'APP_DIRS': True,
        'DIRS': [path('templates')],
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'articles.context_processors.articles',
            ],
        },
    },
]

ARTICLES_TEMPLATE_DIR = 'articles/articles_template'
# -----------------------------------------------------------------------------


# INTERNATIONALIZATION --------------------------------------------------------
TIME_ZONE = 'Europe/Moscow'
LANGUAGE_CODE = 'ru-ru'
USE_I18N = True
USE_L10N = True
USE_TZ = True
# -----------------------------------------------------------------------------


# STATIC AND MEDIA FILES ------------------------------------------------------
STATICFILES_DIRS = [
    path('static'),
]

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

STATICFILES_STORAGE = 'pipeline.storage.PipelineStorage'

STATIC_URL = '/static/'
STATIC_ROOT = path('../../static')

MEDIA_URL = '/media/'
MEDIA_ROOT = path('../media')
# -----------------------------------------------------------------------------


# YARN SETTINGS ---------------------------------------------------------------
YARN_MODULES_ROOT = path('static')

YARN_INSTALLED_APPS = (
    '@fancyapps/fancybox@3.3',
    'include-media-export@1.0',
    'include-media@1.4',
    'jquery-match-height@0.7',
    'jquery.marquee@1.5',
    'jquery@3.3',
    'normalize.css@8.0',
)
# -----------------------------------------------------------------------------


# PIPELINE SETTINGS -----------------------------------------------------------
STATICFILES_FINDERS += (
    'pipeline.finders.PipelineFinder',
)

PIPELINE = {
    'CSS_COMPRESSOR': None,
    'DISABLE_WRAPPER': True,
    'JS_COMPRESSOR': None,
    'SASS_ARGUMENTS': '--include-path %s' % path('static'),
    'SASS_BINARY': 'sassc',
    'COFFEE_SCRIPT_ARGUMENTS': '-b',
    'STYLESHEETS': {
        'styles': {
            'source_filenames': (
                'node_modules/@fancyapps/fancybox/dist/jquery.fancybox.min.css',  # NOQA
                'frontend/css/style.css',
                'frontend/css/responsive.css',
            ),
            'output_filename': 'frontend/css/styles.css',
        },
    },
    'JAVASCRIPT': {
        'libs': {
            'source_filenames': (
                'node_modules/jquery/dist/jquery.min.js',
                'node_modules/jquery-match-height/dist/jquery.matchHeight-min.js',  # NOQA
                'node_modules/@fancyapps/fancybox/dist/jquery.fancybox.min.js',
                'libs/js/jquery.simplemarquee/jquery.simplemarquee.js',
            ),
            'output_filename': 'frontend/js/libs.js',
        },
        'settings': {
            'source_filenames': (
                'frontend/js/settings.js',
            ),
            'output_filename': 'frontend/js/settings.js',
        },
    },
    'COMPILERS': (
        'pipeline.compilers.coffee.CoffeeScriptCompiler',
        'pipeline.compilers.sass.SASSCompiler',
    ),
}
# -----------------------------------------------------------------------------


# CKEDITOR SETTINGS -----------------------------------------------------------
CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = 'pillow'
CKEDITOR_RESTRICT_BY_DATE = True

CKEDITOR_CONFIGS = {
    'default': {
        'toolbar': 'full',
    },
}
# -----------------------------------------------------------------------------


# DJANGO TAGGIT ---------------------------------------------------------------
TAGGIT_CASE_INSENSITIVE = True
# -----------------------------------------------------------------------------


# IPYTHON NOTEBOOK ------------------------------------------------------------
IPYTHON_ARGUMENTS = [
    '--ext', 'django_extensions.management.notebook_extension',
]

NOTEBOOK_ARGUMENTS = [
    '--ip=0.0.0.0',
    '--no-browser',
]
# -----------------------------------------------------------------------------
