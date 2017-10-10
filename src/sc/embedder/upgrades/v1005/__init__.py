# -*- coding: utf-8 -*-
from sc.embedder.logger import logger


BEHAVIOR = 'collective.dexteritytextindexer.behavior.IDexterityTextIndexer'


def remove_dexteritytextindexer_behavior(setup_tool):
    """Remove IDexterityTextIndexer behavior to Embedder content type."""
    from plone.dexterity.interfaces import IDexterityFTI
    from zope.component import getUtility
    fti = getUtility(IDexterityFTI, name='sc.embedder')
    behaviors = list(fti.behaviors)
    if BEHAVIOR in behaviors:
        behaviors.remove(BEHAVIOR)
        fti.behaviors = tuple(behaviors)
        logger.info('IDexterityTextIndexer behavior removed from content type')
