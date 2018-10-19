try:
    from django.urls import re_path as url
except ImportError:
    from django.conf.urls import url

from django.core.wsgi import get_wsgi_application

application = get_wsgi_application()


def health(request):
    from django.http import HttpResponse

    return HttpResponse("ok")


urlpatterns = [url(r"^-/health/$", health)]
