# -*- coding: utf-8 -*-
from sc.embedder.config import PROJECTNAME
from sc.embedder.logger import logger


def add_tile(setup_tool):
    """Update control panel options."""
    profile = 'profile-{0}:default'.format(PROJECTNAME)
    setup_tool.runImportStepFromProfile(profile, 'plone.app.registry')
    logger.info('Added collective.cover tile for sc.embedder content type.')
