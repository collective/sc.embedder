# -*- coding: utf-8 -*-
from plone import api
from plone.browserlayer.utils import registered_layers
from sc.embedder.config import PROJECTNAME
from sc.embedder.testing import INTEGRATION_TESTING
from sc.embedder.testing import IS_PLONE_5

import unittest


class InstallTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']

    def test_installed(self):
        self.assertTrue(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer(self):
        layers = [layer.getName() for layer in registered_layers()]
        self.assertIn('IEmbedderLayer', layers)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_css_registry(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertIn('embedder.css', resource_ids)

    def test_add_permissions(self):
        permission = 'sc.embedder: Add Embedder'
        roles = self.portal.rolesOfPermission(permission)
        roles = [r['name'] for r in roles if r['selected']]
        expected = ['Contributor', 'Manager', 'Owner', 'Site Administrator']
        self.assertListEqual(roles, expected)

    # FIXME: https://community.plone.org/t/making-content-type-linkable-in-tinymce-under-plone-5/4822
    @unittest.skipIf(IS_PLONE_5, 'Not supported under Plone 5')
    def test_tinymce_linkables(self):
        linkables = self.portal.portal_tinymce.linkable.split('\n')
        self.assertIn('sc.embedder', linkables)

    def test_tile(self):
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertIn(u'sc.embedder', tiles)


class UninstallTest(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']
        self.qi = self.portal['portal_quickinstaller']
        self.qi.uninstallProducts(products=[PROJECTNAME])

    def test_uninstalled(self):
        self.assertFalse(self.qi.isProductInstalled(PROJECTNAME))

    def test_browserlayer_removed(self):
        layers = [layer.getName() for layer in registered_layers()]
        self.assertNotIn('IEmbedderLayer', layers)

    @unittest.skipIf(IS_PLONE_5, 'No easy way to test this under Plone 5')
    def test_css_removed(self):
        resource_ids = self.portal.portal_css.getResourceIds()
        self.assertNotIn('embedder.css', resource_ids)

    # FIXME: https://community.plone.org/t/making-content-type-linkable-in-tinymce-under-plone-5/4822
    @unittest.skipIf(IS_PLONE_5, 'Not supported under Plone 5')
    def test_tinymce_linkables(self):
        linkables = self.portal.portal_tinymce.linkable.split('\n')
        self.assertNotIn('sc.embedder', linkables)

    def test_tile_removed(self):
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertNotIn(u'sc.embedder', tiles)
