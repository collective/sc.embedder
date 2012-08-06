# -*- coding: utf-8 -*-

from Products.CMFCore.utils import getToolByName

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

class Fixture(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import sc.content.embedder
        self.loadZCML(package=sc.content.embedder)
        z2.installProduct(app, 'sc.content.embedder')

    def setUpPloneSite(self, portal):
        # Install into Plone site using portal_setup
        self.applyProfile(portal, 'sc.content.embedder:default')

    def tearDownZope(self, app):
        # Uninstall product
        z2.uninstallProduct(app, 'sc.content.embedder')


FIXTURE = Fixture()
INTEGRATION_TESTING = IntegrationTesting(
    bases=(FIXTURE,),
    name='sc.content.embedder:Integration',
    )
FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(FIXTURE,),
    name='sc.content.embedder:Functional',
    )