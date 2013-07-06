#!/usr/bin/env python
import openphoto

requires = ['requests', 'requests_oauthlib']

try:
    from setuptools import setup
    kw = {'entry_points':
          """[console_scripts]\nopenphoto = openphoto.main:main\n""",
          'zip_safe': False,
          'install_requires': requires
          }
except ImportError:
    from distutils.core import setup
    kw = {'scripts': ['bin/openphoto'],
          'requires': requires}

setup(name='openphoto',
      version=openphoto.__version__,
      description='Python client library for Trovebox/Openphoto',
      author='Pete Burgers, James Walker',
      url='https://github.com/openphoto/openphoto-python',
      packages=['openphoto'],
      **kw
      )
