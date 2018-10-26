from __future__ import absolute_import

import waitress.runner

from ...base_command import WebserverCommand
from ...utils import wsgi_app_name


class Command(WebserverCommand):
    """
    This bypasses any Django handling of the command and sends all arguments straight
    to waitress.
    """

    help = "Start waitress server"

    def prep_server_args(self, argv):
        return argv[1:] + [wsgi_app_name()]

    def start_server(self, *args):
        waitress.runner.run(argv=args)
