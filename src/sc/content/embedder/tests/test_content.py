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
        self.request = self.layer['request']

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

        # Then we request the data and check again to see that isn't empty.
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

    def test_custom_player_size_addform(self):
        """ Check if the custom size applies to the embed code in the
            add form.
        """
        add_view = self.folder.unrestrictedTraverse(
                                        '++add++sc.embedder.multimedia')
        dummy_data = {}
        dummy_data['html'] = '<object width="512" height="296"><param ' + \
                        'name="flashvars" value="ap=1"></param></object>'
        dummy_data['width'] = 300
        dummy_data['height'] = 200
        add_form = add_view.form_instance
        add_form.set_custom_embed_code(dummy_data)
        self.assertTrue('width="300"' in dummy_data['html'])
        self.assertTrue('height="200"' in dummy_data['html'])

    def test_custom_player_size_editform(self):
        """ Check if the custom size applies to the embed code in the
            edit form.
        """
        edit_view = self.multimedia.unrestrictedTraverse('edit')
        edit_form = edit_view.form_instance
        dummy_data = {}
        dummy_data['html'] = '<object width="512" height="296"><param ' + \
                        'name="flashvars" value="ap=1"></param></object>'
        dummy_data['width'] = 300
        dummy_data['height'] = 200
        edit_form.set_custom_embed_code(dummy_data)
        self.assertTrue('width="300"' in dummy_data['html'])
        self.assertTrue('height="200"' in dummy_data['html'])

    def test_player_position_class(self):
        """ Tests the return of the css class based on the position
            selected in the form.
        """
        view = self.multimedia.unrestrictedTraverse('view')

        # Classes
        self.multimedia.player_pos = u'Top'
        pos_class = view.get_player_pos_class()
        self.assertEquals(pos_class, 'top_embedded')

        self.multimedia.player_pos = u'Bottom'
        pos_class = view.get_player_pos_class()
        self.assertEquals(pos_class, 'bottom_embedded')

        self.multimedia.player_pos = u'Left'
        pos_class = view.get_player_pos_class()
        self.assertEquals(pos_class, 'left_embedded')

        self.multimedia.player_pos = u'Right'
        pos_class = view.get_player_pos_class()
        self.assertEquals(pos_class, 'right_embedded')

    def test_get_url_widget(self):
        from z3c.form.browser.text import TextWidget
        edit_view = self.multimedia.unrestrictedTraverse('edit')
        edit_form = edit_view.form_instance
        edit_form.update()
        url_wid = edit_view.get_url_widget()
        self.assertTrue(TextWidget, url_wid)
        self.assertEquals(url_wid.id, 'form-widgets-url')

    def test_get_load_action(self):
        from z3c.form.button import ButtonAction
        edit_view = self.multimedia.unrestrictedTraverse('edit')
        edit_form = edit_view.form_instance
        edit_form.update()
        load_act = edit_view.get_load_action()
        self.assertTrue(ButtonAction, load_act)
        self.assertEquals(load_act.id, 'form-buttons-load')
