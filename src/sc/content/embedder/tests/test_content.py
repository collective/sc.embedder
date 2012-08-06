# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.interface.verify import verifyClass, verifyObject

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from sc.content.embedder.content.multimedia import Multimedia
from sc.content.embedder.content.multimedia import IMultimedia
from sc.content.embedder.testing import INTEGRATION_TESTING


class MultimediaTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        setRoles(self.portal, TEST_USER_ID, ['Manager'])
        self.portal.invokeFactory('Folder', 'test-folder')
        self.folder = self.portal['test-folder']

        self.folder.invokeFactory('sc.embedder.multimedia', 'multimedia')
        self.multimedia = self.folder['multimedia']

    def test_adding(self):
        self.assertTrue(IMultimedia.providedBy(self.multimedia))
        self.assertTrue(verifyClass(IMultimedia, Multimedia))

    def test_interface(self):
        self.assertTrue(IMultimedia.providedBy(self.multimedia))
        self.assertTrue(verifyObject(IMultimedia, self.multimedia))
