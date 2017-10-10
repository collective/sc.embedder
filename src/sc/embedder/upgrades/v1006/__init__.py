# -*- coding: utf-8 -*-
from plone import api
from sc.embedder.logger import logger
from sc.embedder.upgrades import get_valid_objects

import transaction


def reindex_searchable_text(setup_tool):
    """Reindex embedders to fix SearchableText."""
    logger.info('Reindexing the catalog')
    catalog = api.portal.get_tool('portal_catalog')
    results = catalog(portal_type='sc.embedder')
    logger.info(u'Found {0} embedders'.format(len(results)))
    for n, obj in enumerate(get_valid_objects(results), start=1):
        catalog.catalog_object(obj, idxs=['SearchableText'])
        if n % 1000 == 0:
            transaction.commit()
            logger.info('{0} items processed.'.format(n))

    transaction.commit()
    logger.info('Done.')
