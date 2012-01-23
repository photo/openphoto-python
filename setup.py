from setuptools import setup

setup(name='openphoto',
      version='0.1',
      description='Client library for the openphoto project',
      author='James Walker',
      author_email='walkah@walkah.net',
      url='https://github.com/openphoto/openphoto-python',
      packages=['openphoto'],
      install_requires=['oauth2'],
      scripts=['scripts/openphoto'],
      )
