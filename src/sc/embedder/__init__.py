# -*- coding: utf-8 -*-
from collective.dexteritytextindexer.utils import searchable
from plone.app.dexterity.behaviors.metadata import IDublinCore
from zope.i18nmessageid import MessageFactory


MessageFactory = MessageFactory('sc.embedder')

# Set field of DublinCore to be searchable.
searchable(IDublinCore, u'title')
searchable(IDublinCore, u'description')
