from __future__ import absolute_import

import pyuwsgi
from django.conf import settings

from ...base_command import WebserverCommand
from ...utils import wsgi_app_name


def get_default_args():
    """Load pyuwsgi args from settings or use our defaults"""
    try:
        return settings.PYUWSGI_ARGS
    except AttributeError:
        defaults = [
            "--strict",
            "--need-app",
            # project.wsgi.application -> project.wsgi:application
            "--module={}".format(wsgi_app_name()),
        ]
        if (settings.STATIC_URL or "").startswith("/"):
            defaults.extend(
                [
                    "--static-map",
                    "{}={}".format(
                        settings.STATIC_URL.rstrip("/"), settings.STATIC_ROOT
                    ),
                ]
            )
        return defaults


class Command(WebserverCommand):

    help = "Start pyuwsgi server"

    def prep_server_args(self, argv):
        return get_default_args() + list(argv[2:])

    def start_server(self, *args):
        pyuwsgi.run(args)
