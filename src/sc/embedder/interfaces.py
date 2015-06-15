# -*- coding: utf-8 -*-
from zope.interface import Interface


class IEmbedderLayer(Interface):
    """ Browser layer
    """


class IConsumer(Interface):

    """oEmbed consumer utility."""

    def get_data(url, maxwidth=None, maxheight=None, format='json'):
        """Return the data provided by the endpoint."""
