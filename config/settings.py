import os

import environ

ROOT_DIR = environ.Path(__file__) - 2
APPS_DIR = ROOT_DIR.path("chemreg")

env = environ.Env()
if os.path.exists(ROOT_DIR(".env")):
    env.read_env(ROOT_DIR(".env"))

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")
AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]
AUTH_USER_MODEL = "users.User"
CACHES = {"default": env.cache_url("CACHE_URL")}
DATABASES = {"default": env.db_url("DATABASE_URL")}
DEBUG = env.bool("DEBUG")
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
LOGIN_REDIRECT_URL = "/"
LOGIN_URL = "/login/"
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
PASSWORD_HASHERS = [
    "django.contrib.auth.hashers.Argon2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2PasswordHasher",
    "django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher",
    "django.contrib.auth.hashers.BCryptSHA256PasswordHasher",
]
ROOT_URLCONF = "config.urls." + env.str("URL_CONF")
SECRET_KEY = env.str("SECRET_KEY")
STATIC_ROOT = ROOT_DIR("collected_static")
STATIC_URL = "/static/"
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
