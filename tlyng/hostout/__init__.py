import logging, os, shutil, tempfile, urllib2, urlparse
import setuptools.archive_util
import datetime
import zc.buildout
import zc.recipe.egg
from os.path import join
import os
from os.path import dirname, abspath
from pkg_resources import resource_string, resource_filename


def add(list, item):
    return '\n'.join( list.split() + [item] )


class Recipe:
    """tlyng.hostout recipe that bootstrap tlyng servers"""

    def __init__(self, buildout, name, options):
        self.name, self.options, self.buildout = name, options, buildout

    def install(self):
        return []

    def update(self):
        return []
