import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
import shutil

# for .env file
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.2/howto/deployment/checklist/


SECRET_KEY = os.environ.get("SECRET_KEY", "your-default-key-for-development")


# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True

DEBUG = os.environ.get("DEBUG", "False").lower() == "True"
ALLOWED_HOSTS = [
    "news-agency-7b6n.onrender.com",
    "127.0.0.1",
    "localhost",
]

# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "debug_toolbar",
    "accounts.apps.AccountsConfig",
    "news.apps.NewsConfig",
    "crispy_forms",
    "crispy_bootstrap5",
    "django_extensions",
]

MIDDLEWARE = [
    "debug_toolbar.middleware.DebugToolbarMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "news_agency.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "news_agency.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.2/ref/settings/#databases


if os.environ.get("DATABASE_URL"):
    DATABASES = {
        "default": dj_database_url.parse(
            os.environ.get("DATABASE_URL"), conn_max_age=600
        )
    }
else:
    # Fallback to SQLite for local development
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }


# Password validation
# https://docs.djangoproject.com/en/5.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.2/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/5.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.Redactor"

LOGIN_URL = "/accounts/login/"
LOGIN_REDIRECT_URL = "/"
LOGOUT_REDIRECT_URL = "/"

CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.2/howto/static-files/
# for media files!!!!🔻
STATIC_URL = "/static/"
STATIC_ROOT = BASE_DIR / "staticfiles"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]
# production WhiteNoise
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

WHITENOISE_USE_FINDERS = True
WHITENOISE_AUTOREFRESH = True

# Django Debug Toolbar(for development only)
if DEBUG:
    INTERNAL_IPS = [
        "127.0.0.1",
        "localhost",
    ]

# Media files (uploads)
if DEBUG:
    # Development settings
    MEDIA_URL = "/media/"
    MEDIA_ROOT = BASE_DIR / "media"
else:
    # Production settings for Render
    MEDIA_URL = "/static/media/"
    MEDIA_ROOT = BASE_DIR / "staticfiles" / "media"
    WHITENOISE_STATIC_PREFIX = "/static/"

# For production - ensure media directory exists
if not DEBUG:
    os.makedirs(MEDIA_ROOT, exist_ok=True)

if not DEBUG:
    try:
        media_source = BASE_DIR / "media"
        media_dest = BASE_DIR / "staticfiles" / "media"

        print(f"🔍 Checking media source: {media_source}")
        print(f"🔍 Media source exists: {media_source.exists()}")

        if media_source.exists():
            # Список файлів у source
            source_files = list(media_source.rglob("*"))
            print(f"📁 Found {len(source_files)} items in media source")

            # Створити destination директорію
            media_dest.mkdir(parents=True, exist_ok=True)

            # Видалити існуючі файли якщо є
            if media_dest.exists() and any(media_dest.iterdir()):
                shutil.rmtree(media_dest)
                media_dest.mkdir(parents=True, exist_ok=True)

            # Копіювати файли
            shutil.copytree(media_source, media_dest, dirs_exist_ok=True)

            # Перевірити результат
            copied_files = list(media_dest.rglob("*"))
            print(f"✅ Successfully copied {len(copied_files)} items to {media_dest}")

        else:
            print(f"❌ Media source directory does not exist: {media_source}")

    except Exception as e:
        print(f"❌ Error copying media files: {e}")
        import traceback

        traceback.print_exc()