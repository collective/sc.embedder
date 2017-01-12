# -*- coding: utf-8 -*-
from plone import api
from sc.embedder.content.embedder import IEmbedder
from sc.embedder.logger import logger
from sc.embedder.utils import sanitize_iframe_tag


REMOVE_CSS = '++resource++sc.embedder/video-js/video-js.css'
REMOVE_JS = '++resource++sc.embedder/video-js/video.js'


def remove_videojs_resources(setup_tool):
    """Remove Video.js from resource registries."""
    css_tool = api.portal.get_tool('portal_css')
    css_tool.unregisterResource(REMOVE_CSS)
    logger.info('Video.js was removed from portal_css.')

    js_tool = api.portal.get_tool('portal_javascripts')
    js_tool.unregisterResource(REMOVE_JS)
    logger.info('Video.js was removed from portal_javascripts.')


def sanitize_iframe_tags(setup_tool):
    """Remove invalid attributes from iframes."""
    logger.info('Sanitizing iframes from embedded code')
    catalog = api.portal.get_tool('portal_catalog')
    query = dict(object_provides=IEmbedder.__identifier__)
    results = catalog.unrestrictedSearchResults(**query)
    for brain in results:
        obj = brain.getObject()
        try:
            obj.embed_html = sanitize_iframe_tag(obj.embed_html)
        except TypeError:  # pragma: no cover
            msg = 'An error ocurred sanitizing object: {0}; skipping'
            logger.error(msg.format(obj.absolute_url()))

    logger.info('{0} objects were processed'.format(len(results)))
