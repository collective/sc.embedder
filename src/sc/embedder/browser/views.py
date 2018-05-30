# -*- coding: utf-8 -*-
from Products.Five.browser import BrowserView
from Products.TinyMCE.adapters.interfaces.JSONFolderListing import IJSONFolderListing
from Products.TinyMCE.adapters.interfaces.JSONSearch import IJSONSearch
from Products.TinyMCE.browser.interfaces.browser import ITinyMCEBrowserView
from Products.TinyMCE.interfaces.utility import ITinyMCE
from zope.component import getUtility
from zope.interface import implementer


@implementer(ITinyMCEBrowserView)
class TinyMCEBrowserView(BrowserView):
    """TinyMCE Browser View"""

    def jsonSCEmbedderFolderListing(self, rooted, document_base_url):
        """Returns the folderlisting of sc.embedder objects in JSON"""

        utility = getUtility(ITinyMCE)
        portal_types = ['sc.embedder']
        portal_types.extend(utility.containsobjects.split('\n'))

        object = IJSONFolderListing(self.context, None)
        if object is None:
            return ''
        results = object.getListing(portal_types, rooted,
                                    document_base_url)
        return results

    def jsonSCEmbedderSearch(self, searchtext):
        """Returns the search results of sc.embedder objects in JSON"""

        utility = getUtility(ITinyMCE)
        portal_types = ['sc.embedder']
        portal_types.extend(utility.containsobjects.split('\n'))

        object = IJSONSearch(self.context, None)
        if object is None:
            return ''
        results = object.getSearchResults(portal_types, searchtext)
        return results
