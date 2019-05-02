# -*- coding: utf-8 -*-
from lxml import cssselect
from lxml import etree
from lxml import html
from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails
from Products.TinyMCE.adapters.JSONDetails import JSONDetails as JSONDetailsBase
from urllib2 import quote
from zope.interface import implementer

import json


@implementer(IJSONDetails)
class JSONDetails(JSONDetailsBase):
    """Return details of the current object in JSON"""

    def getDetails(self):
        """Builds a JSON object based on the details
           of this object.
        """

        results = json.loads(super(JSONDetails, self).getDetails())

        results['description'] = self.context.description

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

        return json.dumps(results)
