# -*- coding: utf-8 -*-
from plone import api
from sc.embedder.logger import logger


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
