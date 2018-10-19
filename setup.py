import os
import sys

from setuptools import find_packages, setup


README = open(os.path.join(os.path.dirname(__file__), "README.md")).read()

TESTS_REQUIRE = ["pytest"]

if sys.version_info < (3, 3):
    TESTS_REQUIRE.append("mock")

setup(
    name="django-webserver",
    version="1.2.0",
    description="Django management commands for production webservers",
    author="Peter Baumgartner",
    author_email="pete@lincolnloop.com",
    url="https://github.com/lincolnloop/django-webserver",
    long_description=README,
    long_description_content_type="text/markdown",
    keywords=["django", "pyuwsgi", "uwsgi", "gunicorn"],
    packages=find_packages(),
    license="MIT",
    install_requires=["Django"],
    extras_require={
        "test": TESTS_REQUIRE,
        "pyuwsgi": ["pyuwsgi>=2.0.17.2b3"],
        "gunicorn": ["gunicorn"],
        "waitress": ["waitress"],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Framework :: Django",
    ],
)
