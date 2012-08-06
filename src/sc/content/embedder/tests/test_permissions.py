# -*- coding: utf-8 -*-

import unittest2 as unittest

from sc.content.embedder.testing import INTEGRATION_TESTING


class PermissionsTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

    def test_add_permissions(self):
        permission = 'sc.content.embedder: Add Multimedia'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Contributor', 'Manager', 'Owner', 'Site Administrator']
        self.assertListEqual(roles, expected)
