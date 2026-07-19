from pathlib import Path
import os
from corsheaders.defaults import default_headers
from datetime import timedelta
from dotenv import load_dotenv
load_dotenv()


BASE_DIR = Path(__file__).resolve().parent.parent

DEV = True if os.getenv("DEV") == 'true' else False

SECRET_KEY = os.getenv("SECRET_KEY")

DEBUG = True

ALLOWED_HOSTS = ['backend', 'backend:8000', 'frontend', 'nurstart.com']

CORS_ALLOWED_ORIGINS = [
    os.getenv("CORS_ORIGINS"),
    'https://nurstart.com',
    'https://www.nurstart.com',
]

CSRF_TRUSTED_ORIGINS = [
    os.getenv("CORS_ORIGINS"),
    'https://nurstart.com',
    'https://www.nurstart.com',
]
# 2. Безопасные cookies (так как теперь работает HTTPS)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# 3. Дополнительные заголовки, чтобы Django понимал, что запрос пришел через HTTPS-прокси Nginx
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


CORS_ALLOW_CREDENTIALS = True
SESSION_COOKIE_SAMESITE = 'Lax'
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7

if DEV:
    # Dev
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv("POSTGRES_DB"),
            'USER': os.getenv("POSTGRES_USER"),
            'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
            'HOST': os.getenv("POSTGRES_HOST_DEV"),
            'PORT': os.getenv("POSTGRES_PORT"),
            'TEST': {
                'NAME': os.getenv("POSTGRES_HOST_DEV"),
            },
        }
    }

    SIMPLE_JWT = {
        'UPDATE_LAST_LOGIN': True,
        'ROTATE_REFRESH_TOKENS': True,
        'ACCESS_TOKEN_LIFETIME': timedelta(days=1),  # minutes=2
        'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    }


else:
    # Prod
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql_psycopg2',
            'NAME': os.getenv("POSTGRES_DB"),
            'USER': os.getenv("POSTGRES_USER"),
            'PASSWORD': os.getenv("POSTGRES_PASSWORD"),
            'HOST': os.getenv("POSTGRES_HOST"),
            'PORT': os.getenv("POSTGRES_PORT"),
            'TEST': {
                'NAME': os.getenv("POSTGRES_HOST"),
            },
        }
    }

    SIMPLE_JWT = {
        'UPDATE_LAST_LOGIN': True,
        'ROTATE_REFRESH_TOKENS': True,
        'ACCESS_TOKEN_LIFETIME': timedelta(minutes=1),
        'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    }



INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',
    'rest_framework.authtoken',
    'rest_framework_simplejwt',

    'ninja_jwt',
    'ninja_extra',
    'celery',
    'corsheaders',
    'db_logger',
    # 'livereload', # автоматическая перезагрузка страницы при изменении кода, замедляет работу, на проде выключать livereload.middleware.LiveReloadScript

    'user',
    'truck'
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'ninja.compatibility.files.fix_request_files_middleware'
    # 'livereload.middleware.LiveReloadScript',
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_THROTTLE_CLASSES': [
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle'
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '10/second',
        'user': '20/second'
    },
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.LimitOffsetPagination',
    'PAGE_SIZE': 100,
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
}

CORS_ORIGIN_ALLOW_ALL = True

CORS_ALLOW_HEADERS = (
    *default_headers,
    "device",
    "jwtToken",
    "JWToken",
)

ASGI_APPLICATION = 'project.asgi.application'

CELERY_BROKER_URL = "redis://redis:6379"
CELERY_RESULT_BACKEND = "redis://redis:6379"
CELERY_TASK_TIME_LIMIT = 3600

ROOT_URLCONF = 'project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR,'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'


AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 6,
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


LANGUAGE_CODE = 'ru'

USE_I18N = True

USE_L10N = False

USE_TZ = False

DATE_FORMAT = 'd.m.Y'
TIME_FORMAT = 'H:i'
DATETIME_FORMAT = 'd.m.Y, H:i'

DATETIME_INPUT_FORMATS = [
    '%d.%m.%Y, %H:%M:%S',
    '%d.%m.%Y, %H:%M',
]


STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')

# А вот папки, где лежат ваши исходные файлы (файлы разработки),
# нужны только если мы не в продакшене или если они физически существуют в проекте
STATICFILES_DIRS = [
    # Убедитесь, что этот путь НЕ совпадает со STATIC_ROOT!
    os.path.join(BASE_DIR, "static_src"),
]

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, '..', 'media')

if not os.path.exists(MEDIA_ROOT):
    os.makedirs(MEDIA_ROOT)


DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


AUTH_USER_MODEL = 'user.CustomUser'


LOGS_DIR = os.path.join(BASE_DIR, '../logs/')

if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'console': {
            'format': '%(name)-12s %(levelname)-8s %(message)s'
        },
        'file': {
            'format': '%(asctime)s %(name)-12s %(levelname)-8s %(message)s'
        },
        'db_log': {
            'format': '%(name)-12s %(message)s'
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'console'
        },
        'file_django': {
            'class': 'logging.FileHandler',  # logging.handlers.RotatingFileHandler - если нужно пересоздавать
            'formatter': 'file',
            'filename': LOGS_DIR + 'django.log',
        },
        'db_log': {
            'level': 'DEBUG',
            'formatter': 'db_log',
            'class': 'db_logger.db_log_handler.DatabaseLogHandler'
        },
        'file_api': {
            'class': 'logging.FileHandler',
            'formatter': 'file',
            'filename': LOGS_DIR + 'api.log',
        },
    },
    'loggers': {
        'django': {
            'level': 'WARNING',
            'handlers': ['console', 'file_django']
        },
        'API': {
            'level': 'INFO',
            'handlers': ['console', 'db_log', 'file_api'],
        },
    },
}

DJANGO_DB_LOGGER_ENABLE_FORMATTER = True


SEND_BOT = os.getenv('SEND_BOT')
BOT_ID = os.getenv('TELEGRAM_BOT_ID')
CHAT_ID = os.getenv('TELEGRAM_BOT_CHAT_ID')