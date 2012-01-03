from setuptools import setup, find_packages
import os

version = '1.0'

setup(name='tlyng.hostout',
      version=version,
      description="",
      long_description=open("README.txt").read() + "\n" +
                       open(os.path.join("docs", "HISTORY.txt")).read(),
      # Get more strings from
      # http://pypi.python.org/pypi?:action=list_classifiers
      classifiers=[
        "Programming Language :: Python",
        ],
      keywords='',
      author='',
      author_email='',
      url='http://svn.plone.org/svn/collective/',
      license='GPL',
      packages=find_packages(exclude=['ez_setup']),
      namespace_packages=['tlyng'],
      include_package_data=True,
      zip_safe=False,
      install_requires = [
        'zc.recipe.egg',
        'setuptools',
        'collective.hostout>=1.0a5',
        'paramiko',
      ],
      entry_points = {
        'zc.buildout':['default = tlyng.hostout:Recipe'],
        'fabric': ['fabfile = tlyng.hostout.fabfile']
      },
    )
