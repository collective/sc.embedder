try:
    import json
    assert json  # silence pyflakes
except ImportError:
    import simplejson as json
from lxml import etree, cssselect, html

from zope.interface import implements

from Products.CMFCore.utils import getToolByName

from Products.TinyMCE.adapters.interfaces.JSONDetails import IJSONDetails

from plone.outputfilters.browser.resolveuid import uuidFor


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

        portal_types = ('sc.embedder',)

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

        if self.context.portal_type in portal_types:
            image_url = self._getPloneUrl() + '/resolveuid/' + \
                        uuidFor(self.context)
            field_name = 'image'
            images = self.context.restrictedTraverse('@@images')

            results['thumb'] = '%s/@@images/%s/%s' % (image_url,
                                                      field_name,
                                                      'thumb')
            sizes = images.getAvailableSizes(field_name)
            scales = [{'value': '@@images/%s/%s' % (field_name, key),
                       'size': size,
                       'title': key.capitalize()} for key, size in \
                                                    sizes.items()]
            scales.sort(lambda x, y: cmp(x['size'][0], y['size'][0]))
            original_size = images.getImageSize(field_name)
            if original_size[0] < 0 or original_size[1] < 0:
                original_size = (0, 0)
            scales.insert(0, {'value': '',
                              'title': 'Original',
                              'size': original_size})
            results['scales'] = scales
        else:
            results['thumb'] = ""

        results.update(self.additionalDetails())

        return json.dumps(results)

    def additionalDetails(self):
        """Hook to allow subclasses to supplement or
           override the default set of results
        """
        return {}

    def _getPloneUrl(self):
        """Return the URL corresponding to the root of the Plone site."""
        portal_url = getToolByName(self.context, 'portal_url')
        portal = portal_url.getPortalObject()
        return portal.absolute_url()
