from bizon.settings.common import *  # NOQA

DEBUG = True
DEBUG404 = not DEBUG

TEMPLATES[0]['OPTIONS']['debug'] = DEBUG  # NOQA

if not TEST:  # NOQA
    INSTALLED_APPS += ['debug_toolbar']  # NOQA
    MIDDLEWARE += [  # NOQA
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    ]


def custom_show_toolbar(request):
    return DEBUG

DEBUG_TOOLBAR_CONFIG = {  # NOQA
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TOOLBAR_CALLBACK': 'settings.dev.custom_show_toolbar',
}

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'simple': {
            'format': '%(module)s: %(message)s'
        },
    },
    'require_debug_true': {
        '()': 'django.utils.log.RequireDebugTrue',
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'bizon': {
            'handlers': ['console'],
            'level': 'DEBUG',
        },
    }
}

if TEST:  # NOQA
    # Радикально ускоряет фабрики пользователей.
    PASSWORD_HASHERS = (
        'django.contrib.auth.hashers.MD5PasswordHasher',
    )

    TEST_RUNNER = 'django_nose.NoseTestSuiteRunner'

    INSTALLED_APPS += (
        'django_nose',
    )
