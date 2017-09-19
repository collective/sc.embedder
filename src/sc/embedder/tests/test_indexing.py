# -*- coding: utf-8 -*-
from plone import api
from plone.app.textfield.value import RichTextValue
from sc.embedder.content.embedder import IEmbedder
from sc.embedder.testing import INTEGRATION_TESTING

import unittest


class IndexingTestCase(unittest.TestCase):

    layer = INTEGRATION_TESTING

    def setUp(self):
        self.portal = self.layer['portal']

        with api.env.adopt_roles(['Manager']):
            self.foo = api.content.create(self.portal, 'sc.embedder', 'foo')
            self.bar = api.content.create(self.portal, 'sc.embedder', 'bar')

    def test_interface_indexed(self):
        results = api.content.find(object_provides=IEmbedder.__identifier__)
        self.assertEqual(2, len(results))
        results = [r.getURL() for r in results]
        self.assertIn(self.foo.absolute_url(), results)
        self.assertIn(self.bar.absolute_url(), results)

    def test_portal_type_indexed(self):
        results = api.content.find(portal_type='sc.embedder')
        self.assertEqual(2, len(results))
        self.assertEqual(results[0].getURL(), self.foo.absolute_url())
        self.assertEqual(results[1].getURL(), self.bar.absolute_url())

    def test_id_indexed(self):
        results = api.content.find(id=u'foo')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.foo.absolute_url())

    def test_title_indexed(self):
        self.foo.title = u'título'
        self.foo.reindexObject()
        results = api.content.find(Title=u'título')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.foo.absolute_url())

    def test_description_indexed(self):
        self.foo.description = u'descrição'
        self.foo.reindexObject()
        results = api.content.find(Description=u'descrição')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.foo.absolute_url())

    def test_keywords_indexed(self):
        self.foo.subject = ('foo', 'baz')
        self.foo.reindexObject()
        self.bar.subject = ('bar', 'baz')
        self.bar.reindexObject()
        results = api.content.find(Subject=('foo'))
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.foo.absolute_url())
        results = api.content.find(Subject=('bar'))
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.bar.absolute_url())
        results = api.content.find(Subject=('baz'))
        self.assertEqual(2, len(results))
        self.assertEqual(results[0].getURL(), self.foo.absolute_url())
        self.assertEqual(results[1].getURL(), self.bar.absolute_url())

    def test_id_in_searchable_text(self):
        results = api.content.find(SearchableText='foo')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.foo.absolute_url())

    def test_title_in_searchable_text(self):
        self.foo.title = u'título'
        self.foo.reindexObject()
        results = api.content.find(SearchableText=u'título')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.foo.absolute_url())

    def test_description_in_searchable_text(self):
        self.foo.description = u'descrição'
        self.foo.reindexObject()
        results = api.content.find(SearchableText=u'descrição')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.foo.absolute_url())

    def test_text_in_searchable_text(self):
        self.foo.text = RichTextValue(u'texto rico', 'text/plain', 'text/html')
        self.foo.reindexObject()
        results = api.content.find(SearchableText=u'texto rico')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.foo.absolute_url())

    def test_alternate_content_in_searchable_text(self):
        self.foo.alternate_content = RichTextValue(
            u'texto rico', 'text/plain', 'text/html')
        self.foo.reindexObject()
        results = api.content.find(SearchableText=u'texto rico')
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.foo.absolute_url())

    def test_keywords_in_searchable_text(self):
        self.foo.subject = ('foo', 'baz')
        self.foo.reindexObject()
        self.bar.subject = ('bar', 'baz')
        self.bar.reindexObject()
        results = api.content.find(SearchableText=('foo'))
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.foo.absolute_url())
        results = api.content.find(SearchableText=('bar'))
        self.assertEqual(1, len(results))
        self.assertEqual(results[0].getURL(), self.bar.absolute_url())
        results = api.content.find(SearchableText=('baz'))
        self.assertEqual(2, len(results))
        results = [r.getURL() for r in results]
        self.assertIn(self.foo.absolute_url(), results)
        self.assertIn(self.bar.absolute_url(), results)
