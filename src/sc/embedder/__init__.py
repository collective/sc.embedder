# -*- coding:utf-8 -*-
from zope.i18nmessageid import MessageFactory

from plone.app.dexterity.behaviors.metadata import IDublinCore

from collective.dexteritytextindexer.utils import searchable


# Set up the i18n message factory for our package
MessageFactory = MessageFactory('sc.content.embedder')

# Set field of DublinCore to be searchable.
searchable(IDublinCore, u'title')
searchable(IDublinCore, u'description')
