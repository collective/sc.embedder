# -*- coding: utf-8 -*-
from plone import api
from sc.embedder.config import PROJECTNAME


def remove_tile(portal):
    tiles = api.portal.get_registry_record('plone.app.tiles')
    if u'sc.embedder' in tiles:
        tiles.remove(u'sc.embedder')


def uninstall(portal):
    remove_tile(portal)
    profile = 'profile-%s:uninstall' % PROJECTNAME
    setup_tool = api.portal.get_tool(name='portal_setup')
    setup_tool.runAllImportStepsFromProfile(profile)
    return 'Ran all uninstall steps.'
