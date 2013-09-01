#!/usr/bin/env python
import sys

requires = ['requests', 'requests_oauthlib']

console_script = """[console_scripts]
trovebox = trovebox.main:main
"""

# from trovebox._version import __version__
exec(open("trovebox/_version.py").read())

# Check the Python version
(major, minor) = sys.version_info[:2]
if (major, minor) < (2, 6):
    raise SystemExit("Sorry, Python 2.6 or newer required")

try:
    from setuptools import setup
    kw = {'entry_points': console_script,
          'zip_safe': True,
          'install_requires': requires
          }
except ImportError:
    from distutils.core import setup
    kw = {'scripts': ['bin/trovebox'],
          'requires': requires}

setup(name='trovebox',
      version=__version__,
      description='The official Python client library for the Trovebox photo service',
      long_description=open("README.rst").read(),
      author='Pete Burgers, James Walker',
      url='https://github.com/photo/openphoto-python',
      packages=['trovebox', 'trovebox.objects', 'trovebox.api'],
      keywords=['openphoto', 'pyopenphoto', 'openphoto-python',
                'trovebox', 'pytrovebox', 'trovebox-python'],
      classifiers=['Development Status :: 4 - Beta',
                   'Intended Audience :: Developers',
                   'License :: OSI Approved :: Apache Software License',
                   'Operating System :: OS Independent',
                   'Programming Language :: Python',
                   'Topic :: Multimedia :: Graphics',
                   'Topic :: Software Development :: Libraries :: Python Modules',
                   ],
      license='Apache 2.0',
      test_suite='tests.unit',
      **kw
      )
