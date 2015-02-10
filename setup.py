# -*- coding: utf-8 -*-

from setuptools import find_packages
from setuptools import setup

import os

version = '1.0b4.dev0'
description = "This packages contains a Dexterity-based content type that "
"allows you to embedded content (such as photos or videos) from third "
"parties into your Plone site."
long_description = (
    open("README.rst").read() + "\n" +
    open(os.path.join("docs", "CREDITS.rst")).read() + "\n" +
    open(os.path.join("docs", "CHANGES.rst")).read()
)

setup(name='sc.embedder',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Web Environment",
          "Framework :: Plone",
          "Framework :: Plone :: 4.2",
          "Framework :: Plone :: 4.3",
          "Intended Audience :: End Users/Desktop",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
          "Operating System :: OS Independent",
          "Programming Language :: JavaScript",
          "Programming Language :: Python",
          "Programming Language :: Python :: 2.6",
          "Programming Language :: Python :: 2.7",
          "Topic :: Internet :: WWW/HTTP",
          "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
          "Topic :: Multimedia",
          "Topic :: Office/Business",
          "Topic :: Software Development :: Libraries :: Python Modules",
      ],
      keywords='multimedia video audio oembed plone embed embedder',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='http://www.simplesconsultoria.com.br',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['sc'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'collective.dexteritytextindexer',
          'collective.oembed<2.0a1',
          'five.grok',
          'lxml',
          'Pillow',
          'plone.app.dexterity',
          'plone.app.referenceablebehavior',
          'plone.dexterity',
          'plone.directives.dexterity',
          'plone.namedfile[blobs]',
          'Products.CMFCore',
          'Products.CMFPlone >=4.2',
          'Products.GenericSetup',
          'Products.TinyMCE',
          'setuptools',
          'zope.component',
          'zope.event',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'plone.app.testing',
              'plone.browserlayer',
              'plone.testing',
              'robotframework-selenium2library',
              'robotsuite',
              'unittest2',
          ],
      },
      entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
        """,
      )
