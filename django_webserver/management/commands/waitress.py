from __future__ import absolute_import

from waitress.runner import run

from ...base_command import WebserverCommand
from ...utils import wsgi_app_name


class Command(WebserverCommand):
    """
    This bypasses any Django handling of the command and sends all arguments straight
    to waitress.
    """

    help = "Start waitress server"

    def start_server(self, *args):
        run(argv=args[1:] + (wsgi_app_name(),))
