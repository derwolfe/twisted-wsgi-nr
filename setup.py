import codecs
import sys
import os

from setuptools import setup


version = "0.0.1"

# thanks hynek
def read(*parts):
    """
    Build an absolute path from *parts* and and return the contents of the
    resulting file.  Assume UTF-8 encoding.
    """
    here = os.path.abspath(os.path.dirname(__file__))
    with codecs.open(os.path.join(here, *parts), "rb", "utf-8") as f:
        return f.read()


setup(
    name="twisted_wsgi_nr",
    version=version,
    description="test of new relic with falcon wsgi and twisted server",
    long_description=read("README.md"),
    author="Chris Wolfe",
    author_email="chriswwolfe@gmail.com",
    url="https://github.com/derwolfe/twisted-wsgi-nr",
    # entry_points={
    #     "console_scripts": [
    #         "pleasework = twisted_wsgi_nr:run"
    #     ],
    # },
    license="MIT",
    py_modules=["twisted_wsgi_nr"],
    install_requires=[
        "falcon",
        "twisted",
        "newrelic",
        "structlog"
    ],
)
