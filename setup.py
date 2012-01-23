requires = ['oauth2', 'httplib2']
try:
    import json
except ImportError:
    requires.append('simplejson')

try:
    from setuptools import setup
    kw = {'entry_points':
          """[console_scripts]\nopenphoto = openphoto.main:main\n""",
          'zip_safe': False,
          'install_requires': requires
          }
except ImportError:
    from distutils.core import setup
    kw = {'scripts': ['scripts/openphoto'],
          'requires': requires}

setup(name='openphoto',
      version='0.1',
      description='Client library for the openphoto project',
      author='James Walker',
      author_email='walkah@walkah.net',
      url='https://github.com/openphoto/openphoto-python',
      packages=['openphoto'],
      **kw
      )
