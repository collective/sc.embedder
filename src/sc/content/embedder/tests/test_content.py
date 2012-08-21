# -*- coding: utf-8 -*-

import unittest2 as unittest

from zope.interface.verify import verifyClass, verifyObject

from plone.app.testing import TEST_USER_ID
from plone.app.testing import setRoles

from sc.content.embedder.content.multimedia import IMultimedia
from sc.content.embedder.content.multimedia import Multimedia

from sc.content.embedder.testing import INTEGRATION_TESTING


PROVIDERS = {
     'youtube': 'http://www.youtube.com/watch?v=n-zxaVt6acg&feature=g-all-u',
     'vimeo': 'http://vimeo.com/17914974',
     'slideshare': 'http://www.slideshare.net/cgiorgi/secrets-of-a-good-pitch',
     'instagram': 'http://www.flickr.com/photos/jup3nep/6796214503/?f=hp',
     }


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

    def test_addview_oembed_data(self):
        add_view = self.folder.unrestrictedTraverse(
                                        '++add++sc.embedder.multimedia')
        add_form = add_view.form_instance
        add_form.update()
        add_form.actions.update()

        # We check for Vimeo that has a more complete oembed implementation
        add_form.widgets['url'].value = 'http://vimeo.com/17914974'
        action = add_form.actions['load']

        # We check first that the fields are empty
        self.assertEquals(u'',
                        add_form.widgets['IDublinCore.title'].value)
        self.assertEquals(u'',
                        add_form.widgets['IDublinCore.description'].value)
        self.assertEquals(u'',
                        add_form.widgets['html'].value)
        self.assertEquals(u'',
                        add_form.widgets['width'].value)
        self.assertEquals(u'',
                        add_form.widgets['height'].value)

        # Then we request the data
        add_form.handleLoad(add_form, action)
        self.assertNotEquals(u'',
                        add_form.widgets['IDublinCore.title'].value)
        self.assertNotEquals(u'',
                        add_form.widgets['IDublinCore.description'].value)
        self.assertNotEquals(u'',
                        add_form.widgets['html'].value)
        self.assertNotEquals(u'',
                        add_form.widgets['width'].value)
        self.assertNotEquals(u'',
                        add_form.widgets['height'].value)
