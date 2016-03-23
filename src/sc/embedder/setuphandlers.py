# -*- coding: utf-8 -*-
from plone import api
from Products.CMFPlone.interfaces import INonInstallable
from Products.PortalTransforms.Transform import make_config_persistent
from sc.embedder.logger import logger
from zope.interface import implements


@implementer(INonInstallable)
class HiddenProfiles(object):

    def getNonInstallableProfiles(self):
        """Do not show on Plone's list of installable profiles."""
        return [
            u'sc.embedder:uninstall',
        ]


def setup_portal_transforms(context):
    if not context.readDataFile('sc.embedder-default.txt'):
        return

    logger.info('Updating portal_transform safe_html settings')

    tid = 'safe_html'

    pt = api.portal.get_tool('portal_transforms')
    if tid not in pt.objectIds():
        return

    trans = pt[tid]

    tconfig = trans._config

    tconfig['valid_tags']['iframe'] = '1'

    make_config_persistent(tconfig)
    trans._p_changed = True
    trans.reload()
