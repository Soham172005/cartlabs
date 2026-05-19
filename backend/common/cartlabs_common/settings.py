import os
from urllib.parse import urlparse


def database_from_url(url):
    parsed = urlparse(url)
    return {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": parsed.path.lstrip("/"),
        "USER": parsed.username,
        "PASSWORD": parsed.password,
        "HOST": parsed.hostname,
        "PORT": parsed.port or 5432,
    }


def build_settings(service_label, apps=None, middleware=None):
    return {
        "SECRET_KEY": os.getenv("DJANGO_SECRET_KEY", "cartlabs-dev-secret"),
        "DEBUG": os.getenv("DEBUG", "true").lower() == "true",
        "ALLOWED_HOSTS": os.getenv("ALLOWED_HOSTS", "*").split(","),
        "INSTALLED_APPS": [
            "django.contrib.contenttypes",
            "django.contrib.auth",
            *(apps or []),
        ],
        "MIDDLEWARE": [
            "django.middleware.security.SecurityMiddleware",
            "django.middleware.common.CommonMiddleware",
            *(middleware or []),
        ],
        "ROOT_URLCONF": "config.urls",
        "TEMPLATES": [],
        "WSGI_APPLICATION": "config.wsgi.application",
        "DATABASES": {
            "default": database_from_url(
                os.getenv("DATABASE_URL", "postgres://cartlabs:cartlabs@localhost:5432/cartlabs")
            )
        },
        "DEFAULT_AUTO_FIELD": "django.db.models.BigAutoField",
        "USE_TZ": True,
        "TIME_ZONE": "UTC",
        "SERVICE_LABEL": service_label,
        "APPEND_SLASH": False,
    }
