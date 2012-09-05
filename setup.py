from setuptools import setup, find_packages
import os

version = '1.0a2.dev0'
description = "A multimedia content type for Plone"
long_description = open("README.txt").read() + "\n" + \
                   open(os.path.join("docs", "INSTALL.txt")).read() + "\n" + \
                   open(os.path.join("docs", "CREDITS.txt")).read() + "\n" + \
                   open(os.path.join("docs", "HISTORY.txt")).read()


setup(name='sc.content.embedder',
      version=version,
      description=description,
      long_description=long_description,
      classifiers=[
        "Development Status :: 1 - Alpha",
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 4.1",
        "Framework :: Plone :: 4.2",
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
      keywords='multimedia video audio oembed plone web embed embedder',
      author='Simples Consultoria',
      author_email='products@simplesconsultoria.com.br',
      url='http://www.simplesconsultoria.com.br',
      license='GPLv2',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      namespace_packages=['sc', 'sc.content'],
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          'setuptools',
          'Products.CMFPlone>=4.1',
          'plone.behavior',
          'plone.app.dexterity>=1.2.1',
          'plone.app.referenceablebehavior',
          'collective.dexteritytextindexer',
          'collective.oembed',
      ],
      extras_require={
        'test': ['plone.app.testing'],
        },
      entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
        """,
      )
