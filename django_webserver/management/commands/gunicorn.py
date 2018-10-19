from __future__ import absolute_import

from gunicorn.app.wsgiapp import WSGIApplication

from ...base_command import WebserverCommand
from ...utils import wsgi_app_name


class DjangoApplication(WSGIApplication):
    def init(self, parser, opts, args):
        # strip mgmt command name from args and insert WSGI module
        args = [wsgi_app_name()] + args[2:]
        super(DjangoApplication, self).init(parser, opts, args)


class Command(WebserverCommand):
    """
    This bypasses any Django handling of the command and sends all arguments straight
    to gunicorn.
    """

    help = "Start gunicorn server"

    def start_server(self, *args):
        DjangoApplication("%(prog)s [OPTIONS]").run()

    def execute(self, *args, **options):
        raise NotImplementedError("gunicorn must receive args from sys.argv")
