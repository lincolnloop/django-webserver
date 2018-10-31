# django-webserver

Run production webservers such as [pyuwsgi](https://pypi.org/project/pyuwsgi/) (aka uWSGI) or [gunicorn](https://pypi.org/project/gunicorn/) as a Django management command.

----

[![build status](https://travis-ci.org/lincolnloop/django-webserver.svg?branch=master)](https://travis-ci.org/lincolnloop/django-pyuwsgi) [![pypi](https://img.shields.io/pypi/v/django-webserver.svg)](https://pypi.org/pypi/django-webserver) [![pyversions](https://img.shields.io/pypi/pyversions/django-webserver.svg)](https://pypi.org/pypi/django-webserver)

## Usage

1. Install a variant:

    ```
    pip install django-webserver[pyuwsgi]
    ```

    or

    ```
    pip install django-webserver[gunicorn]
    ```

    or

    ```
    pip install django-webserver[uvicorn]  # Python 3.5+ only
    ```

    or

    ```
    pip install django-webserver[waitress]
    ```

2. Add to `INSTALLED_APPS`:

    ```python
    INSTALLED_APPS = [
       # ...
       "django_webserver",
       # ...
    ]
    ```
3. Run:

    ```
    manage.py pyuwsgi --http=:8000 ...
    ```

    or

    ```
    manage.py gunicorn
    ```

    or

    ```
    manage.py uvicorn
    ```

    or

    ```
    manage.py waitress --port=8000
    ```

## Configuration

### With pyuwsgi

![uwsgi logo](https://cldup.com/uiFb8Sn4Ea.png)

[(py)uWSGI docs](https://uwsgi-docs.readthedocs.io/en/latest/)

Pyuwsgi already knows the Python interpreter and virtualenv (if applicable) to use from the Django management command environment. By default, it will run with the following flags (using `settings.WSGI_APPLICATION` to determine the module):

```
--strict --need-app --module={derived}
```

If you have `STATIC_URL` defined with a local URL, it will also add `--static-map`, derived from `STATIC_URL` and `STATIC_ROOT`.

You can pass any additional arguments uWSGI accepts in from the command line.

But uWSGI has a lot of flags, and many of them, you want every time you run the project. For that scenario, you can configure your own defaults using the optional setting, `PYUWSGI_ARGS`. Here's an example you might find helpful:

```python
PYUWSGI_ARGS = [
    "--master",
    "--strict",
    "--need-app",
    "--module".
    ":".join(WSGI_APPLICATION.rsplit(".", 1)),
    "--no-orphans",
    "--vacuum",
    "--auto-procname",
    "--enable-threads",
    "--offload-threads=4",
    "--thunder-lock",
    "--static-map",
    "=".join([STATIC_URL.rstrip("/"), STATIC_ROOT]),
    "--static-expires",
    "/* 7776000",
]
```

Don't forget to also set something like `--socket=:8000` or `--http=:8000` so your app listens on a port. Depending on your setup, it may make more sense to pass this in via the command line than hard-coding it in your settings.

### With gunicorn

![gunicorn logo](https://cldup.com/TObFsJSacv.png)

[gunicorn docs](https://docs.gunicorn.org/en/stable/)

Same as the standard gunicorn configuration, but the application will be set for you from `settings.WSGI_APPLICATION`.

_Note: Unlike the other servers, you have to configure gunicorn with environment variables or via `sys.argv`. If you use it with Django's `call_command`, keep in mind any additional arguments you pass will not be applied._

### With uvicorn

![uvicorn logo](https://cldup.com/By389I7ZHd.png)

[uvicorn docs](https://www.uvicorn.org/)

Same as the standard uvicorn configuration, but the application will be set for you from `settings.WSGI_APPLICATION` as well as `--wsgi`.

### With waitress

![waitress logo](https://cldup.com/3m18XSyzuM.png)

[waitress docs](https://docs.pylonsproject.org/projects/waitress/en/latest/index.html)

Same as the standard [`waitress-serve`](https://docs.pylonsproject.org/projects/waitress/en/latest/runner.html) arguments, but the application will be set for you from `settings.WSGI_APPLICATION`.

Unlike the other servers, waitress is supported on Windows.

### Pre-warming Your App

Default:

```python
WEBSERVER_WARMUP = True
```

Typically, when a WSGI server starts, it will bind to the necessary ports _then_ import/setup your application. On larger projects, it's normal for startup to take multiple seconds. During that time, it is unable to respond to incoming requests.

To avoid that downtime, this app imports your WSGI module _before_ starting the relevant server. If, for some reason this behavior is undesirable, you can set `WEBSERVER_WARMUP = False` in your settings.

### Running a Healthcheck at Startup

This is not enabled by default. It requires `WEBSERVER_WARMUP = True`.

```python
WEBSERVER_WARMUP_HEALTHCHECK = "/-/health/"
```

Internally calls the provided URL prior to starting the server and exits with a failure if it does not return a `200`.

It can be helpful to have your app exit immediately if it is unable to successfully respond to a healthcheck. Your process or container manager should immediately show the service failed instead of waiting for a load balancer or some other monitoring tool to notify catch the problem.


## Motivation

In some scenarios, it is beneficial to distribute a Django project with a single entrypoint for command-line interaction. This can come in handy when building Docker containers or self-contained Python apps with something like [shiv](https://github.com/linkedin/shiv).

Pre-warming the application and running a healthcheck can also open the door for some zero-downtime deployment scenarios that previously weren't possible due to the issues described in "Pre-warming your app". For example, you could use the `--reuse-port` option in uWSGI or gunicorn to bring up a new version of your app on the same port, knowing it is already warmed-up and healthy. After a successful startup, the old version can safely be torn down without dropping any traffic.
