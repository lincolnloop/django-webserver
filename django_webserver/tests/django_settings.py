# print("sleeping...")
# import time; time.sleep(5)
from django.core.wsgi import get_wsgi_application
try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url

SECRET_KEY = "s"
WSGI_APPLICATION = "django_webserver.tests.django_settings.application"
INSTALLED_APPS = ["django_webserver"]
ROOT_URLCONF = "django_webserver.tests.django_settings"
STATIC_URL = "/static/"
STATIC_ROOT = "/tmp/static"


def health(request):
    from django.http import HttpResponse

    return HttpResponse("ok")


urlpatterns = [url(r"^-/health/$", health)]


application = get_wsgi_application()
