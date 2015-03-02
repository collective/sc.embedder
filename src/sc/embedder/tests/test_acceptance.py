import unittest

import robotsuite

from plone.testing import layered

from sc.embedder.testing import FUNCTIONAL_TESTING


class Keywords(object):
    """ Robot Framework keyword library """

    def get_path_to_tests(self):
        from os.path import dirname
        return dirname(__file__)


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite('test_embedder.txt'),
                layer=FUNCTIONAL_TESTING),
    ])
    return suite
