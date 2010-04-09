import os

from setuptools import setup, find_packages


VERSION = "0.7.13" # N.B.: duplicate of tiddlywebplugins.instancer.__init__


setup(
    name = "tiddlywebplugins.instancer",
    version = VERSION,
    url = "http://pypi.python.org/pypi/tiddlywebplugins.instancer",
    description = "utilities to simplify instance management for TiddlyWeb verticals",
    long_description = file(os.path.join(os.path.dirname(__file__), "README")).read(),
    platforms = "Posix; MacOS X; Windows",
    author = "FND",
    author_email = "FNDo@gmx.net",
    namespace_packages = ["tiddlywebplugins"],
    packages = find_packages(exclude=["test"]),
    install_requires = ["setuptools",
        "tiddlyweb>=1.0.0",
        "tiddlywebplugins.utils>=1.0",
        "tiddlywebplugins.twimport>=0.9.4"],
    zip_safe = False
)
