# -*- coding:utf-8 -*-

from five import grok
from zope import schema

from plone.directives import dexterity

from plone.directives import form

from plone.namedfile.field import NamedImage

from plone.app.textfield import RichText

from collective import dexteritytextindexer

from sc.content.embedder import MessageFactory as _


player_options = {'top': u'Top',
                  'bottom': u'Bottom',
                  'left': u'Left',
                  'right': u'Right',
                  }


class IMultimedia(form.Schema):
    """ A representation of a Multimedia content type
    """

    dexteritytextindexer.searchable('body_txt', 'alt_cont')
    form.order_before(**{'url': '*'})
    url = schema.TextLine(
        title=_(u"Multimedia URL"),
        description=_(u"The URL for your multimedia file. Can be a URL " + \
                      u"from Youtube, Vimeo, Slideshare, SounCloud or " + \
                      u"other main multimedia websites."),
        required=True,
        )

    width = schema.Int(
        title=_(u"Width"),
        description=_(u""),
        required=False,
        )

    height = schema.Int(
        title=_(u"Height"),
        description=_(u""),
        required=False,
        )

    player_pos = schema.Choice(
        title=_(u"Player position"),
        description=_(u""),
        default=u'Top',
        required=True,
        values=[u'Top', u'Bottom', u'Left', u'Right'],
        )

    body_txt = RichText(
        title=_(u"Body text"),
        required=False,
        )

    alt_cont = RichText(
        title=_(u"Alternative content"),
        description=_(u"Description or transcription to an individual" + \
                      u"that is no able to see or hear."),
        required=True,
        )

    image = NamedImage(
        title=_(u"Image"),
        description=_(u"A image to be used when listing content."),
        required=False,
        )


class Multimedia(dexterity.Item):
    """ A Multimedia
    """
    grok.implements(IMultimedia)


class View(dexterity.DisplayForm):
    grok.context(IMultimedia)
    grok.require('zope2.View')
    grok.name('view')
