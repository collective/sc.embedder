# -*- coding: utf-8 -*-
from plone import api
from sc.embedder.config import PROFILE
from sc.embedder.testing import INTEGRATION_TESTING
from sc.embedder.upgrades.v1003 import REMOVE_CSS
from sc.embedder.upgrades.v1003 import REMOVE_JS

import unittest


class UpgradeTestCaseBase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self, from_version, to_version):
        self.portal = self.layer['portal']
        self.setup = self.portal['portal_setup']
        self.from_version = from_version
        self.to_version = to_version

    def _get_upgrade_step(self, title):
        """Get one of the upgrade steps.

        :param title: [required] the title used to register the upgrade step
        :type obj: str
        """
        self.setup.setLastVersionForProfile(PROFILE, self.from_version)
        upgrades = self.setup.listUpgrades(PROFILE)
        steps = [s for s in upgrades[0] if s['title'] == title]
        return steps[0] if steps else None

    def _do_upgrade_step(self, step):
        """Execute an upgrade step.

        :param step: [required] the step we want to run
        :type step: str
        """
        request = self.layer['request']
        request.form['profile_id'] = PROFILE
        request.form['upgrades'] = [step['id']]
        self.setup.manage_doUpgrades(request=request)

    def _how_many_upgrades_to_do(self):
        self.setup.setLastVersionForProfile(PROFILE, self.from_version)
        upgrades = self.setup.listUpgrades(PROFILE)
        assert len(upgrades) > 0
        return len(upgrades[0])


class Upgrade1000to1001TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1000', u'1001')

    def test_upgrade_to_1001_registrations(self):
        version = self.setup.getLastVersionForProfile(PROFILE)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self._how_many_upgrades_to_do(), 1)

    def test_add_embedder_tile(self):
        # check if the upgrade step is registered
        title = u'Add embedder tile'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        from sc.embedder.Extensions.Install import remove_tile
        remove_tile(api.portal.get())
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertNotIn(u'sc.embedder', tiles)

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        tiles = api.portal.get_registry_record('plone.app.tiles')
        self.assertIn(u'sc.embedder', tiles)


class Upgrade1001to1002TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1001', u'1002')

    def test_upgrade_to_1002_registrations(self):
        version = self.setup.getLastVersionForProfile(PROFILE)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self._how_many_upgrades_to_do(), 1)


class Upgrade1002to1003TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1002', u'1003')

    def test_upgrade_to_1003_registrations(self):
        version = self.setup.getLastVersionForProfile(PROFILE)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self._how_many_upgrades_to_do(), 3)

    def test_remove_videojs_resources(self):
        # check if the upgrade step is registered
        title = u'Remove Video.js from resource registries'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        css_tool = api.portal.get_tool('portal_css')
        css_tool.registerResource(REMOVE_CSS)
        self.assertIn(REMOVE_CSS, css_tool.getResourceIds())
        js_tool = api.portal.get_tool('portal_javascripts')
        js_tool.registerResource(REMOVE_JS)
        self.assertIn(REMOVE_JS, js_tool.getResourceIds())

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        self.assertNotIn(REMOVE_CSS, css_tool.getResourceIds())
        self.assertNotIn(REMOVE_JS, js_tool.getResourceIds())
