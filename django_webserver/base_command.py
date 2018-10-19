from django.conf import settings
from django.core.management import BaseCommand
from django.core.servers.basehttp import get_internal_wsgi_application

from django_webserver.utils import wsgi_healthcheck


class WebserverCommand(BaseCommand):
    """
    This bypasses any Django handling of the command and sends all arguments straight
    to the webserver.
    """

    def start_server(self, *args):
        raise NotImplementedError

    def prep_server_args(self, argv):
        return argv

    def run_from_argv(self, argv):
        if getattr(settings, "WEBSERVER_WARMUP", True):
            app = get_internal_wsgi_application()
            if getattr(settings, "WEBSERVER_WARMUP_HEALTHCHECK", None):
                wsgi_healthcheck(app, settings.WEBSERVER_WARMUP_HEALTHCHECK)
        self.start_server(*self.prep_server_args(argv))

    def execute(self, *args, **options):
        raise NotImplementedError
