from __future__ import absolute_import

import uvicorn.main

from ...base_command import WebserverCommand
from ...utils import wsgi_app_name


class Command(WebserverCommand):
    """
    This bypasses any Django handling of the command and sends all arguments straight
    to uvicorn.
    """

    help = "Start uvicorn server"

    def prep_server_args(self, argv):
        return argv[2:] + [wsgi_app_name(), "--wsgi"]

    def start_server(self, *args):
        uvicorn.main.main(args)
