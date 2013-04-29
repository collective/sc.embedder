# -*- coding: utf-8 -*-

from lxml import etree, cssselect, html
from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails
from zope.interface import implements

import json


class JSONDetails(object):
    """Return details of the current object in JSON"""
    implements(IJSONDetails)

    def __init__(self, context):
        """Constructor"""
        self.context = context

    def getDetails(self):
        """Builds a JSON object based on the details
           of this object.
        """

        results = {}
        results['title'] = self.context.title_or_id()
        results['description'] = self.context.Description()
        results['embed_html'] = self.context.embed_html

        tree = etree.HTML(self.context.embed_html)
        sel = cssselect.CSSSelector('body > *')
        el = sel(tree)[0]
        el.attrib['width'] = '188'
        el.attrib['height'] = '141'

        results['thumb_html'] = html.tostring(el)

        results.update(self.additionalDetails())

        return json.dumps(results)

    def additionalDetails(self):
        """Hook to allow subclasses to supplement or
           override the default set of results
        """
        return {}
