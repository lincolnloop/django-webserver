import os

UWSGI_VERSION = "2.0.17.1"
UWSGI_LIB = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "libuwsgi-{}.so".format(UWSGI_VERSION))
)
