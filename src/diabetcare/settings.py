from django.contrib import messages
from pathlib import Path
import environ
import os

from django.utils.translation import gettext_lazy as _

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()

environ.Env.read_env(env_file=str(BASE_DIR / "diabetcare" / ".env"))

SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = env.bool("DEBUG", False)

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

AUTHENTICATION_BACKENDS = [
    # Needed to login by username in Django admin, regardless of `allauth`
    'django.contrib.auth.backends.ModelBackend',

    # `allauth` specific authentication methods, such as login by email
    'allauth.account.auth_backends.AuthenticationBackend',
]

# En production, utilisez des variables d'environnement
SOCIALACCOUNT_PROVIDERS = {
    'google': {
        'APP': {
            'client_id': env('GOOGLE_CLIENT_ID'),     # Récupéré depuis .env
            'secret': env('GOOGLE_CLIENT_SECRET'),    # Jamais en dur dans le code
            'key': ''
        }
    }
}

ACCOUNT_FORMS = {
    'signup': 'users.forms.MyCustomSignupForm',
}

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    "django_extensions",
    'crispy_forms',
    'crispy_bootstrap5',
    'compressor',
    'widget_tweaks',
    'users',
    'patients',
    'nutritions',
    'translations',
    'activities',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.google',  # Provider Google
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware', # Activation de la gestion des langues
    # Add the account middleware:
    "allauth.account.middleware.AccountMiddleware",
]

ROOT_URLCONF = 'diabetcare.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ["templates"],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',

                # `allauth` needs this from django
                "django.template.context_processors.request",
            ],
        },
    },
]

WSGI_APPLICATION = 'diabetcare.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST"),
        "PORT": env("PORT"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

LANGUAGES = [
    ('fr', _('Français')),
    ('en', _('English')),
]

LANGUAGE_CODE = 'fr'  # Langue par défaut
USE_I18N = True  # Active la traduction
USE_L10N = True  # Active le formatage régional
USE_TZ = True

LOCALE_PATHS = [BASE_DIR / 'locale']  # Dossier contenant les fichiers de traduction


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"
STATICFILES_DIRS = [os.path.join(BASE_DIR, "diabetcare/static")]
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")
STATICFILES_FINDERS = ('compressor.finders.CompressorFinder',)

STATICFILES_FINDERS = [
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
]

MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "mediafiles")

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

MESSAGE_TAGS = {messages.ERROR: "danger"}

# django-crispy-forms
PACKS_TEMPLAIRES_AUTORISÉS_CRISPY = "bootstrap5"
PACK_TEMPLAIRES_CRISPY = "bootstrap5"
CRISPY_TEMPLATE_PACK = 'bootstrap5'  # or 'bootstrap5' depending on what you use

EMAIL_HOST = "smtp.zoho.com"
EMAIL_HOST_USER = "guydon@zohomail.com"
EMAIL_USE_TLS = False
EMAIL_USE_SSL = True
DEFAULT_FROM_EMAIL = "guydon@zohomail.com"
EMAIL_PORT = 465
EMAIL_HOST_PASSWORD = "WCT9KMBd1XwC"
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"


SESSION_ENGINE = 'django.contrib.sessions.backends.signed_cookies'
SESSION_COOKIE_NAME = 'app_session_uuid'
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SECURE = False  # Uniquement en HTTPS

SECURE_SSL_REDIRECT = False
SECURE_HSTS_SECONDS = 0 # 31536000  # Force HTTPS pour 1 an
SECURE_REFERRER_POLICY = None # "strict-origin-when-cross-origin"

# Authentification
SESSION_COOKIE_AGE = 1800  # 30 minutes
SESSION_SAVE_EVERY_REQUEST = True  # Rafraîchit le timeout
ACCOUNT_MAX_EMAIL_ADDRESSES = 1  # Limite à un seul email par compte

# Sécurité avancée
SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False
SECURE_BROWSER_XSS_FILTER = True

SITE_ID = 1

AUTH_USER_MODEL = 'users.CustomUser'  # Définir le modèle utilisateur personnalisé
ACCOUNT_LOGIN_METHODS = {"email"}  # Authentification uniquement par email

ACCOUNT_SIGNUP_FIELDS = [
    "email*",  # Email obligatoire (* signifie que le champ est requis)
    "password1*",
    "password2*",
]
ACCOUNT_EMAIL_VERIFICATION = "optional"
LOGIN_REDIRECT_URL = '/dashboard'
LOGOUT_REDIRECT_URL = '/'
ACCOUNT_UNIQUE_EMAIL = True
ACCOUNT_SESSION_REMEMBER = True
ACCOUNT_SIGNUP_EMAIL_ENTER_TWICE = False