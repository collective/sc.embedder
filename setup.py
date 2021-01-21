# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup


version = '1.5.1'
description = 'This packages contains a Dexterity-based content type that '
'allows you to embedded content (such as photos or videos) from third '
'parties into your Plone site.'
long_description = (
    open('README.rst').read() + '\n' +
    open('CONTRIBUTORS.rst').read() + '\n' +
    open('CHANGES.rst').read()
)

setup(name='sc.embedder',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Web Environment',
          'Framework :: Plone',
          'Framework :: Plone :: 4.3',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
          'Operating System :: OS Independent',
          'Programming Language :: JavaScript',
          'Programming Language :: Python',
          'Programming Language :: Python :: 2.7',
          'Topic :: Internet :: WWW/HTTP',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
          'Topic :: Multimedia',
          'Topic :: Office/Business',
          'Topic :: Software Development :: Libraries :: Python Modules',
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
          'lxml',
          'cssselect',
          'plone.api',
          'plone.app.content',
          'plone.app.dexterity',
          'plone.app.relationfield',
          'plone.app.textfield',
          'plone.autoform',
          'plone.dexterity',
          'plone.formwidget.namedfile',
          'plone.namedfile',
          'plone.supermodel',
          'plone.uuid',
          'Products.CMFPlone >=4.3',
          'Products.GenericSetup',
          'Products.PortalTransforms >=2.1.10',
          'python-oembed',
          'requests',
          'setuptools',
          'z3c.form',
          'zope.component',
          'zope.event',
          'zope.i18nmessageid',
          'zope.interface',
          'zope.publisher',
          'zope.schema',
      ],
      extras_require={
          'test': [
              'httmock',
              'plone.app.robotframework',
              'plone.app.testing [robot]',
              'plone.browserlayer',
              'plone.testing',
              'Products.statusmessages',
              'robotsuite',
          ],
      },
      entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
        """,
      )
