#-*- coding: utf-8 -*-

import unittest2 as unittest
import doctest

from plone.testing import layered

from sc.embedder.testing import FUNCTIONAL_TESTING


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(doctest.DocFileSuite('tests/test_buttons.txt',
                                     package='sc.embedder'),
                layer=FUNCTIONAL_TESTING),
    ])
    return suite
