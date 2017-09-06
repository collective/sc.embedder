# -*- coding: utf-8 -*-
from plone import api
from sc.embedder.logger import logger


def add_as_tinymce_linkable(setup_tool):
    """Add Embedder to TinyMCE's list of linkable content types."""
    tinymce_tool = api.portal.get_tool('portal_tinymce')
    linkable = tinymce_tool.linkable.split('\n')
    linkable.append('sc.embedder')
    tinymce_tool.linkable = '\n'.join(linkable)
    assert 'sc.embedder' in tinymce_tool.linkable.split('\n')
    logger.info("sc.embedder added to TinyMCE's list of linkable content types.")
