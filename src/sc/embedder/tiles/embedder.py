# -*- coding: utf-8 -*-
from collective.cover.tiles.base import IPersistentCoverTile
from collective.cover.tiles.base import PersistentCoverTile
from plone.tiles.interfaces import ITileDataManager
from plone.uuid.interfaces import IUUID
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.embedder import MessageFactory as _
from zope import schema


class IEmbedderTile(IPersistentCoverTile):
    """
    """

    title = schema.TextLine(
        title=_(u'Title'),
        required=False,
    )

    embed_code = schema.TextLine(
        title=_(u'Videos'),
        required=False,
        readonly=True,
    )

    url = schema.TextLine(
        title=_(u'Videos'),
        required=False,
        readonly=True,
    )

    uuids = schema.List(
        title=_(u'Videos'),
        value_type=schema.TextLine(),
        required=False,
        readonly=True,
    )


class EmbedderTile(PersistentCoverTile):
    index = ViewPageTemplateFile('embedder.pt')
    is_configurable = False
    is_editable = True
    limit = 1

    def populate_with_object(self, obj):
        super(EmbedderTile, self).populate_with_object(obj)  # check permission

        # here we should check if the embeded item has its a video
        # XXX
        if obj.portal_type in self.accepted_ct():

            title = obj.Title()
            url = obj.absolute_url()
            uuid = IUUID(obj)
            embed = obj.embed_html
            data_mgr = ITileDataManager(self)
            data_mgr.set({'title': title,
                          'url': url,
                          'uuid': uuid,
                          'embed_code': embed,
                          })

    def get_uid(self, obj):
        return IUUID(obj)

    def accepted_ct(self):
        """ Return a list of content types accepted by the tile.
        """
        return ['sc.embedder']
