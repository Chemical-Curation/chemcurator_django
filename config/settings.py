import os

import environ

ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path("chemreg")

env = environ.Env(
    CACHE_URL=(str, "locmemcache://"),
    DATABASE_URL=(str, "sqlite:///.sqlite3"),
    DEBUG=(bool, True),
    SESSION_COOKIE_AGE=(int, 900),
    SECRET_KEY=(str, "secret"),
    URL_CONF=(str, "api"),
    WHITELIST_HOST=(str, ""),
    WHITELIST_LOCAL=(bool, True),
    WEB_CONCURRENCY=(int, 1),
)
if os.path.exists(ROOT_DIR(".env")):
    env.read_env(ROOT_DIR(".env"))

#################
# Core Settings #
#    django     #
#################
# https://docs.djangoproject.com/en/3.0/ref/settings/#core-settings

ALLOWED_HOSTS = []
if env.bool("WHITELIST_LOCAL"):
    ALLOWED_HOSTS += [
        "0.0.0.0",
        "127.0.0.1",
        "localhost",
    ]
if env("WHITELIST_HOST"):
    ALLOWED_HOSTS += [env("WHITELIST_HOST")]
CACHES = {"default": env.cache_url("CACHE_URL", env("CACHE_URL"))}
DATABASES = {"default": env.db_url("DATABASE_URL", env("DATABASE_URL"))}
DEBUG = env("DEBUG")
INSTALLED_APPS = [
    # Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.messages",
    "django.contrib.sessions",
    "django.contrib.staticfiles",
    # Third party apps
    "polymorphic",
    "rest_framework",
    # Local apps
    "chemreg.common.apps.CommonConfig",
    "chemreg.compound.apps.CompoundConfig",
    "chemreg.users.apps.UsersConfig",
    "chemreg.utils.apps.UtilsConfig",
]
MEDIA_ROOT = APPS_DIR("media")
MEDIA_URL = "/media/"
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]
ROOT_URLCONF = "config.urls." + env("URL_CONF")
SECRET_KEY = env("SECRET_KEY")
TEMPLATES = [
    {
        "APP_DIRS": True,
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "OPTIONS": {
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    }
]
TIME_ZONE = "UTC"
USE_I18N = False
WSGI_APPLICATION = "config.wsgi.application"

#######################
#    Auth Settings    #
# django.contrib.auth #
#######################
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
AUTH_USER_MODEL = "users.User"
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "login/"
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]

###########################
#    Session Settings     #
# django.contrib.sessions #
###########################
# https://docs.djangoproject.com/en/3.0/ref/settings/#sessions

SESSION_COOKIE_AGE = env("SESSION_COOKIE_AGE")
SESSION_COOKIE_SAMESITE = "Strict"
SESSION_ENGINE = "django.contrib.sessions.backends.cache"
SESSION_SAVE_EVERY_REQUEST = True

##############################
#    Static Files Settings   #
# django.contrib.staticfiles #
##############################
# https://docs.djangoproject.com/en/3.0/ref/settings/#static-files

STATIC_ROOT = ROOT_DIR("collected_static")
STATIC_URL = "/static/"

#######################
#  Gunicorn Settings  #
#      gunicorn       #
#######################
# https://docs.gunicorn.org/en/latest/settings.html

WEB_CONCURRENCY = env("WEB_CONCURRENCY")

#########################
#  WhiteNoise Settings  #
#      whitenoise       #
#########################
# http://whitenoise.evans.io/en/stable/django.html

WHITENOISE_AUTOREFRESH = DEBUG
WHITENOISE_USE_FINDERS = DEBUG
