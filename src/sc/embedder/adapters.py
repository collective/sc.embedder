# -*- coding: utf-8 -*-
from lxml import cssselect
from lxml import etree
from lxml import html
from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails
from urllib2 import quote
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

        tree = etree.HTML(self.context.embed_html)
        sel = cssselect.CSSSelector('body > *')
        el = sel(tree)[0]
        el.attrib['width'] = '188'
        el.attrib['height'] = '141'

        # The raw html bits don't travel nicely over json alone
        # use javascript's decodeURIComponent on the client side
        # to get these values back:
        results['thumb_html'] = quote(html.tostring(el))
        results['embed_html'] = quote(self.context.embed_html)

        results.update(self.additionalDetails())

        return json.dumps(results)

    def additionalDetails(self):
        """Hook to allow subclasses to supplement or
           override the default set of results
        """
        return {}
