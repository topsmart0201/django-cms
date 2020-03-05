INSTALLED_ADDONS = [
    # <INSTALLED_ADDONS>  # Warning: text inside the INSTALLED_ADDONS tags is auto-generated. Manual changes will be overwritten.
    'aldryn-addons',
    'aldryn-django',
    'aldryn-sso',
    'aldryn-django-cms',
    'django-filer',
    # </INSTALLED_ADDONS>
]


import aldryn_addons.settings
aldryn_addons.settings.load(locals())


import os
import logging
from typing import List
from enum import Enum

import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
from sentry_sdk.integrations.logging import LoggingIntegration
from env_settings import env


# fix idea errors for divio imported settings
INSTALLED_APPS: List[str] = locals()['INSTALLED_APPS']
MIDDLEWARE: List[str] = locals()['MIDDLEWARE']
BASE_DIR: str = locals()['BASE_DIR']
STATIC_URL: str = locals()['STATIC_URL']
HTTP_PROTOCOL: str = locals()['STATIC_URL']
TEMPLATES: List[dict] = locals()['TEMPLATES']


################################################################################
## === project custom === ##
################################################################################


DATE_FORMAT = 'F j, Y'


class DivioEnv(Enum):
    LOCAL = 'local'
    TEST = 'test'
    LIVE = 'live'


DIVIO_ENV_ENUM = DivioEnv
DIVIO_ENV = DivioEnv(env.get('STAGE', 'local'))


################################################################################
## === django core === ##
################################################################################


INSTALLED_APPS.insert(0, 'backend.auth')  # for USERNAME_FIELD = 'email', before `cms` since it has a User model

INSTALLED_APPS.extend([
    # django packages
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'cuser', # for USERNAME_FIELD = 'email' in backend.auth
    'gtm',
    'solo',
    'rest_framework',
    'import_export',
    'adminsortable2',
    'admin_reorder',
    'django_extensions',
    'django_countries',
    'logentry_admin',

    # django cms packages

    'aldryn_apphooks_config',
    'djangocms_icon',
    'djangocms_text_ckeditor',
    'djangocms_link',
    'djangocms_googlemap',
    'djangocms_video',
    'djangocms_history',
    'djangocms_picture',
    'djangocms_snippet',
    'djangocms_helpers',
    'djangocms_page_meta',
        'meta',

    'djangocms_modules',
    'aldryn_forms_bs4_templates',
    'djangocms_redirect',

    'djangocms_bootstrap4',
    'djangocms_bootstrap4.contrib.bootstrap4_alerts',
    'djangocms_bootstrap4.contrib.bootstrap4_badge',
    'djangocms_bootstrap4.contrib.bootstrap4_card',
    'djangocms_bootstrap4.contrib.bootstrap4_carousel',
    'djangocms_bootstrap4.contrib.bootstrap4_collapse',
    'djangocms_bootstrap4.contrib.bootstrap4_content',
    'djangocms_bootstrap4.contrib.bootstrap4_grid',
    'djangocms_bootstrap4.contrib.bootstrap4_jumbotron',
    'djangocms_bootstrap4.contrib.bootstrap4_link',
    'djangocms_bootstrap4.contrib.bootstrap4_listgroup',
    'djangocms_bootstrap4.contrib.bootstrap4_media',
    'djangocms_bootstrap4.contrib.bootstrap4_picture',
    'djangocms_bootstrap4.contrib.bootstrap4_tabs',
    'djangocms_bootstrap4.contrib.bootstrap4_utilities',


    # project

    'backend.plugins.default.bs4_float',
    'backend.plugins.default.bs4_hiding',
    'backend.plugins.default.bs4_inline_alignment',
    'backend.plugins.default.bs4_spacer',
    'backend.plugins.default.bs4_lightbox_gallery',
    'backend.plugins.default.bs4_card_columns',
    'backend.plugins.default.heading_element',
    'backend.plugins.default.hero_image_element',
    'backend.plugins.default.section_element',

    'backend.error_handler',
])


MIDDLEWARE.extend([
    # django packages
    'admin_reorder.middleware.ModelAdminReorder',

    # django cms optional
    'djangocms_redirect.middleware.RedirectMiddleware',
])


AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
]


AUTH_USER_MODEL = 'backend_auth.User'


STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'frontend/'),
]

default_template_engine: dict = TEMPLATES[0]
default_template_engine['DIRS'].extend([
    os.path.join(BASE_DIR, 'backend/templates/'),
])
default_template_engine['OPTIONS']['context_processors'].extend([
    'django_settings_export.settings_export',
])


EMAIL_BACKEND = env.get(
    'EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend',
)


################################################################################
## === django packages === ##
################################################################################


# allauth
AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = HTTP_PROTOCOL
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_USERNAME_REQUIRED = False
ACCOUNT_USER_MODEL_USERNAME_FIELD = None
ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = False
AUTHENTICATED_LOGIN_REDIRECTS = False  # otherwise admins can't access the login view
LOGIN_REDIRECT_URL = '/'
CONFIRM_EMAIL_ON_GET = True


GTM_CONTAINER_ID = env.get('GTM_CONTAINER_ID', 'GTM-1234')


WEBPACK_DEV_URL = env.get('WEBPACK_DEV_URL', default='http://localhost:8090/assets/')


SETTINGS_EXPORT = [
    'WEBPACK_DEV_URL',
    'DIVIO_ENV',
    'DIVIO_ENV_ENUM',
    'SENTRY_IS_ENABLED',
    'SENTRY_DSN',
]


SENTRY_IS_ENABLED = env.get_bool('SENTRY_IS_ENABLED', False)
SENTRY_DSN = env.get('SENTRY_DSN')
if SENTRY_IS_ENABLED:
    # noinspection PyTypeChecker
    sentry_sdk.init(
        dsn=SENTRY_DSN,
        integrations=[
            DjangoIntegration(),
            LoggingIntegration(
                level=logging.INFO,  # Capture info and above as breadcrumbs
                event_level=None,  # Send no events from log messages
            )
        ],
        environment=DIVIO_ENV.value,
    )


ADMIN_REORDER = [
    {
        'label': 'CMS Pages',
        'app': 'cms',
        'models': [
            'cms.Page',
            'djangocms_redirect.Redirect',
        ],
    },
    {
        'label': 'CMS Plugins',
        'app': 'cms',
        'models': [
            {'model': 'aldryn_forms.FormSubmission', 'label': 'Dynamic forms submissions'},
            {'model': 'djangocms_modules.Category', 'label': 'Plugin modules categories'},
            {'model': 'djangocms_snippet.Snippet', 'label': 'HTML snippets'},
        ],
    },
    {
        'label': 'Articles',
        'app': 'articles',
        'models': [
            'articles.Article',
            'articles.Category',
            'articles.ArticlesConfig',
        ],
    },
    {
        'label': 'Files',
        'app': 'filer',
        'models': [
            'filer.Folder',
            {'model': 'filer.ThumbnailOption', 'label': 'Images thumbnail options'},
        ],
    },
    {
        'label': 'Users',
        'app': 'auth',
        'models': [
            'backend_auth.User',
            {'model': 'auth.Group', 'label': 'User groups for everything'},
            {'model': 'cms.PageUserGroup', 'label': 'User groups for pages'},
            'cms.GlobalPagePermission',
            {'model': 'aldryn_sso.AldrynCloudUser', 'label': 'Admin users from Divio'},
        ],
    },
    {
        'label': 'robots.txt',
        'app': 'robots',
        'models': [
            {'model': 'robots.Rule', 'label': 'Access rules'},
            'robots.Url',
        ],
    },
    {
        'label': 'Sites',
        'app': 'sites',
        'models': [
            'sites.Site',
        ],
    },
]


################################################################################
## === django-cms core === ##
################################################################################


CMS_TEMPLATES = [
    ('content-full-width.html', 'full width'),
]


################################################################################
## === django-cms packages === ##
################################################################################


DJANGOCMS_BOOTSTRAP4_GRID_SIZE = 24
DJANGOCMS_BOOTSTRAP4_GRID_COLUMN_CHOICES = [
    ('col', 'Column'),
    # for full width columns that have no left/right padding
    ('col p-0', 'Full-width Column'),
    ('w-100', 'Break'),
    ('', 'Empty'),
]


DJANGOCMS_GOOGLEMAP_API_KEY = env.get('DJANGOCMS_GOOGLEMAP_API_KEY', '123')


CKEDITOR_SETTINGS = {
    'language': '{{ language }}',
    'toolbar': 'CUSTOM',
    'toolbar_CUSTOM': [
        ['Undo', 'Redo'],
        ['cmsplugins', '-', 'ShowBlocks'],
        ['Format', 'Styles', 'FontSize'],
        ['TextColor', 'BGColor', '-', 'PasteText', 'PasteFromWord', 'RemoveFormat'],
        ['Maximize', ''],
        '/',
        ['Bold', 'Italic', 'Underline', '-', 'Subscript', 'Superscript', '-', ],
        ['JustifyLeft', 'JustifyCenter', 'JustifyRight'],
        # we dont want 'Link', this is done by the bootstrap4 link/button plugin which covers all kind of links
        ['Unlink'],
        ['NumberedList', 'BulletedList', '-', 'Outdent', 'Indent', '-', 'Table'],
        ['Source']
    ],
    'stylesSet': [
        {'name': 'Float Left', 'element': 'span', 'attributes': {'class': 'float-left'}},
        {'name': 'H1', 'element': 'h1'},
    ],
    'contentsCss': [
        f'{WEBPACK_DEV_URL}global.css' if env.is_dev() else f'{STATIC_URL}/dist/global.css',
        f'{WEBPACK_DEV_URL}vendor.css' if env.is_dev() else f'{STATIC_URL}/dist/vendor.css',
        f'{STATIC_URL}/djangocms_text_ckeditor/ckeditor/contents.css',  # default required styles
    ],
    'config': {
        'allowedContent': True,
    }
}

META_SITE_PROTOCOL = 'http' if DIVIO_ENV == DivioEnv.LOCAL else 'https'
