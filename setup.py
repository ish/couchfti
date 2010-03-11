from setuptools import setup, find_packages
import sys, os

version = '0.1.2'

setup(name='couchfti',
      version=version,
      description="Xapian base full text indexing for couchdb",
      long_description="""\
""",
      classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
      keywords='',
      author='Tim Parkin & Matt Goodall',
      author_email='info@timparkin.co.uk',
      url='http://ish.io',
      license='',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'pyparsing',
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      """,
      )
