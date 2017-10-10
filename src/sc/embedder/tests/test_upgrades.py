# -*- coding: utf-8 -*-
from plone import api
from plone.dexterity.interfaces import IDexterityFTI
from sc.embedder.config import PROFILE
from sc.embedder.testing import INTEGRATION_TESTING
from sc.embedder.testing import IS_PLONE_5
from sc.embedder.upgrades.v1003 import REMOVE_CSS
from sc.embedder.upgrades.v1003 import REMOVE_JS
from zope.component import getUtility

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
        self.assertEqual(self._how_many_upgrades_to_do(), 4)

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

    def test_sanitize_iframe_tags(self):
        # check if the upgrade step is registered
        title = u'Sanitize iframe tags'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        iframe = '<iframe src="http://plone.org" frameborder="0"></iframe>'
        with api.env.adopt_roles(['Manager']):
            e1 = api.content.create(
                self.portal, 'sc.embedder', 'e1', embed_html=iframe)

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        expected = '<iframe src="http://plone.org"></iframe>'
        self.assertEqual(e1.embed_html, expected)


class Upgrade1003to1004TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1003', u'1004')

    def test_registrations(self):
        version = self.setup.getLastVersionForProfile(PROFILE)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self._how_many_upgrades_to_do(), 2)

    # FIXME: https://community.plone.org/t/making-content-type-linkable-in-tinymce-under-plone-5/4822
    @unittest.skipIf(IS_PLONE_5, 'Not supported under Plone 5')
    def test_add_as_tinymce_linkable(self):
        # check if the upgrade step is registered
        title = u'Add as TinyMCE linkable'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        tinymce_tool = api.portal.get_tool('portal_tinymce')
        linkable = tinymce_tool.linkable.split('\n')
        linkable.remove('sc.embedder')
        tinymce_tool.linkable = '\n'.join(linkable)
        self.assertNotIn('sc.embedder', tinymce_tool.linkable.split('\n'))

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        self.assertIn('sc.embedder', tinymce_tool.linkable.split('\n'))

    def test_add_relateditems_behavior(self):
        # check if the upgrade step is registered
        title = u'Add Related Items behavior'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        from plone.app.relationfield.behavior import IRelatedItems
        fti = getUtility(IDexterityFTI, name='sc.embedder')
        behaviors = list(fti.behaviors)
        behaviors.remove(IRelatedItems.__identifier__)
        fti.behaviors = tuple(behaviors)
        self.assertNotIn(IRelatedItems.__identifier__, fti.behaviors)

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        self.assertIn(IRelatedItems.__identifier__, fti.behaviors)


class UpgradeTo1005TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1004', u'1005')

    def test_registrations(self):
        version = self.setup.getLastVersionForProfile(PROFILE)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self._how_many_upgrades_to_do(), 1)

    def test_remove_dexteritytextindexer_behavior(self):
        # check if the upgrade step is registered
        title = u'Remove IDexterityTextIndexer behavior'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        # simulate state on previous version
        from sc.embedder.upgrades.v1005 import BEHAVIOR
        fti = getUtility(IDexterityFTI, name='sc.embedder')
        fti.behaviors += (BEHAVIOR,)
        self.assertIn(BEHAVIOR, fti.behaviors)

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        self.assertNotIn(BEHAVIOR, fti.behaviors)


class UpgradeTo1006TestCase(UpgradeTestCaseBase):

    def setUp(self):
        UpgradeTestCaseBase.setUp(self, u'1005', u'1006')

    def test_registrations(self):
        version = self.setup.getLastVersionForProfile(PROFILE)[0]
        self.assertGreaterEqual(int(version), int(self.to_version))
        self.assertEqual(self._how_many_upgrades_to_do(), 1)

    def test_reindex_news_articles(self):
        # check if the upgrade step is registered
        title = u'Reindex SearchableText'
        step = self._get_upgrade_step(title)
        self.assertIsNotNone(step)

        with api.env.adopt_roles(['Manager']):
            for i in xrange(0, 10):
                api.content.create(self.portal, 'sc.embedder', str(i))

        # update metadata without notifying
        self.portal['0'].subject = ('foo', 'bar')
        results = api.content.find(SearchableText='foo')
        self.assertEqual(len(results), 0)

        # run the upgrade step to validate the update
        self._do_upgrade_step(step)
        results = api.content.find(SearchableText='foo')
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0].getURL(), self.portal['0'].absolute_url())
