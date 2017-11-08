import os

# Django settings for dt project.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_ROOT = BASE_DIR
DEBUG = True
TEMPLATE_DEBUG = True

ADMINS = (
    ('Tim Stumbaugh', 'stum@mit.edu'),
    ('Bruno Faviero', 'bfaviero@mit.edu'),
    ('Rachel Wang', 'rswang@mit.edu'),
    ('Michele Miao', 'mqm@mit.edu')
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'dt.db',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': ''
    }
}

EMAIL_HOST = 'outgoing.mit.edu'
EMAIL_PORT = 25
SERVER_EMAIL = 'dt-web@MIT.EDU'

# Local time zone for this installation. Choices can be found here:
# http://www.postgresql.org/docs/8.1/static/datetime-keywords.html#DATETIME-TIMEZONE-SET-TABLE
# although not all variations may be possible on all operating systems.
# If running in a Windows environment this must be set to the same as your
# system time zone.
TIME_ZONE = 'America/New_York'

# Language code for this installation. All choices can be found here:
# http://www.w3.org/TR/REC-html40/struct/dirlang.html#langcodes
# http://blogs.law.harvard.edu/tech/stories/storyReader$15
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# Absolute path to the directory that holds media.
# Example: "/home/media/media.lawrence.com/"
MEDIA_ROOT =  '/var/www/media'

# URL that handles the media served from MEDIA_ROOT.
# Example: "http://media.lawrence.com"
MEDIA_URL = '/media/'

STATIC_URL = '/static/'

# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'

STATICFILES_DIRS = (
    PROJECT_ROOT + '/static',
)

# STATIC_ROOT = PROJECT_ROOT + '/sitestatic'
STATIC_ROOT = PROJECT_ROOT + '/sitestatic'

# Make this unique, and don't share it with anybody.
SECRET_KEY = 's'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader'
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'utils.auth.SSLRemoteUserMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'maintenancemode.middleware.MaintenanceModeMiddleware',
    'django.middleware.doc.XViewMiddleware',
    'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.i18n',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.contrib.messages.context_processors.messages',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'utils.auth.SSLRemoteUserBackend',
)



ROOT_URLCONF = 'dt.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    PROJECT_ROOT + '/templates',
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.flatpages',
    'django.contrib.markup',
    'django.contrib.databrowse',
    'django.contrib.staticfiles',

    'honeypot',
    'tinymce',

    'dt.utils',
    'dt.accounts',
    'dt.blog',
    'dt.shows',
    'dt.auditions',
    'dt.costumes',
    'dt.officers',
    'south',
    'widget_tweaks',
)

DANCER_IMAGE_DIR = 'photos/dancers'
COSTUME_IMAGE_DIR = 'photos/costumes'

# Normalize all incoming URLs by appending a slash if necessary
APPEND_SLASH = True

MAINTENANCE_MODE = False  # Change to True in settings_local to take site offline

# User profiles
AUTH_PROFILE_MODULE = 'accounts.userprofile'

HONEYPOT_FIELD_NAME = 'position'

TINYMCE_DEFAULT_CONFIG = {
    'theme': 'advanced',
    'theme_advanced_toolbar_location': 'top',
    'theme_advanced_toolbar_align': 'left',
    'plugins': 'autolink,style,advlink,advlist,autolink,contextmenu,inlinepopups,paste',
    'paste_auto_cleanup_on_paste': 'true',
    'theme_advanced_buttons1_add' : 'fontselect,fontsizeselect',
    'theme_advanced_buttons2': "cut,copy,paste,pastetext,pasteword,|,bullist,numlist,|,outdent,indent,blockquote,|,undo,redo,|,link,unlink,anchor,image,cleanup,help,code,|,forecolor,backcolor",
    'theme_advanced_buttons3_add': 'styleprops'
}
try:
    from settings_local import *
except:
    pass
