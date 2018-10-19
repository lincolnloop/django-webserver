SECRET_KEY = "s"
ALLOWED_HOSTS = ["testserver"]
WSGI_APPLICATION = "django_webserver.tests.app.application"
INSTALLED_APPS = ["django_webserver"]
ROOT_URLCONF = "django_webserver.tests.app"
STATIC_URL = "/static/"
STATIC_ROOT = "/tmp/static"
