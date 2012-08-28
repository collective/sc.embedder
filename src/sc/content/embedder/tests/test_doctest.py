#-*- coding: utf-8 -*-

import unittest2 as unittest
import doctest

from plone.testing import layered

from sc.content.embedder.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('tests/test_buttons.txt',
                                     package='sc.content.embedder'),
                layer=FUNCTIONAL_TESTING),
        ])
    return suite
