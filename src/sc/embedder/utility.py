# -*- coding: utf-8 -*-
"""This code was taken from collective.oembed and is included here just
to remove the dependency on that package.

See: https://github.com/simplesconsultoria/sc.embedder/issues/13

TODO: Refactor it to get the list of providers on an alternative way.
      The Iframely project maintains a list of oEmbed providers updated.

See: https://github.com/itteco/iframely/blob/master/lib/plugins/system/oembed/providers.json
"""
from sc.embedder.interfaces import IConsumer
from sc.embedder.logger import logger
from zope.interface import implementer

import oembed


@implementer(IConsumer)
class Consumer(object):

    """oEmbed consumer utility."""

    def __init__(self):
        self.consumer = None

    def get_data(self, url, maxwidth=None, maxheight=None, format='json'):
        """Return the data provided by the endpoint."""

        self.initialize_consumer()
        request = {}
        if maxwidth is not None:
            request['maxwidth'] = maxwidth
        if maxheight is not None:
            request['maxheight'] = maxheight
        request['format'] = format

        try:
            response = self.consumer.embed(url, **request)
            return response.getData()
        except oembed.OEmbedNoEndpoint, e:
            logger.info(e)
        except oembed.OEmbedError, e:
            # often a mimetype error
            logger.info(e)

    def initialize_consumer(self):
        if self.consumer is None:
            consumer = oembed.OEmbedConsumer()
            _enpoints = load_all_endpoints()
            for endpoint in _enpoints:
                consumer.addEndpoint(endpoint)
            self.consumer = consumer


REGEX_PROVIDERS = [
    # http://apiblog.youtube.com/2009/10/oembed-support.html
    {u'regex': [r'regex:.*youtube\.com/watch.*',
                r'regex:.*youtube\.com/playlist.*'],
     u'endpoint': 'https://www.youtube.com/oembed'},

    {u'regex': ['http://*.flickr.com/*'],
     u'endpoint': 'http://www.flickr.com/services/oembed'},

    {u'regex': ['http://qik.com/video/*', 'http://qik.com/*'],
     u'endpoint': 'http://qik.com/api/oembed.{format}'},

    {u'regex': ['http://*revision3.com/*'],
     u'endpoint': 'http://revision3.com/api/oembed/'},

    {u'regex': ['http://www.hulu.com/watch/*'],
     u'endpoint': 'http://www.hulu.com/api/oembed.{format}'},

    {u'regex': ['http://vimeo.com/*'],
     u'endpoint': 'http://vimeo.com/api/oembed.{format}'},

    {u'regex': ['http://www.collegehumor.com/video/*'],
     u'endpoint': 'http://www.collegehumor.com/oembed.{format}'},

    {u'regex': ['http://www.polleverywhere.com/polls/*',
                'http://www.polleverywhere.com/multiple_choice_polls/*',
                'http://www.polleverywhere.com/free_text_polls/*'],
     u'endpoint': 'http://www.polleverywhere.com/services/oembed/'},

    {u'regex': ['http://www.ifixit.com/*'],
     u'endpoint': 'http://www.ifixit.com/Embed'},

    {u'regex': ['http://*.smugmug.com/*'],
     u'endpoint': 'http://api.smugmug.com/services/oembed/'},

    {u'regex': ['http://www.slideshare.net/*/*'],
     u'endpoint': 'http://www.slideshare.net/api/oembed/2'},

    {u'regex': ['http://www.23hq.com/*/photo/*'],
     u'endpoint': 'http://www.23hq.com/23/oembed'},

    # http://www.5min.com/APIDocs/Embed.aspx
    {u'regex': ['http://www.5min.com/Video/*'],
     u'endpoint': 'http://api.5min.com/oembed.{format}'},

    # https://dev.twitter.com/docs/embedded-tweets
    {u'regex': ['https://twitter.com/*/status*/*'],
     u'endpoint': 'https://api.twitter.com/1/statuses/oembed.{format}'},

    # http://pic.pbsrc.com/dev_help/Metadata/Metadata_Discovery.htm
    {u'regex': ['regex:.*photobucket\\.com/(albums|groups)/.+$'],
     u'endpoint': 'http://photobucket.com/oembed'},

    # http://pic.pbsrc.com/dev_help/Metadata/Metadata_Discovery.htm
    {u'regex': ['http://*.kinomap.com/*'],
     u'endpoint': 'http://www.kinomap.com/oembed'},

    # http://www.dailymotion.com/doc/api/oembed.html
    {u'regex': ['http://www.dailymotion.com/video/*'],
     u'endpoint': 'http://www.dailymotion.com/services/oembed'},

    {u'regex': ['http://*.clikthrough.com/theater/video/*'],
     u'endpoint': 'http://clikthrough.com/services/oembed'},

    # http://solutions.dotsub.com/oEmbed
    {u'regex': ['http://dotsub.com/view/*'],
     u'endpoint': 'http://dotsub.com/services/oembed'},

    # blit.tv sends an invalid mime-type back
    {u'regex': ['http://*blip.tv/*'],
     u'endpoint': 'http://blip.tv/oembed/'},

    # http://official.fm/developers/oembed
    {u'regex': ['http://official.fm/tracks/*', 'http://official.fm/playlists/*'],
     u'endpoint': 'http://official.fm/services/oembed.{format}'},

    # http://dev.vhx.tv/oembed.html
    {u'regex': ['http://vhx.tv/*'],
     u'endpoint': 'http://vhx.tv/services/oembed.{format}'},

    {u'regex': ['http://*.nfb.ca/film/*'],
     u'endpoint': 'http://www.nfb.ca/remote/services/oembed/'},

    # http://instagr.am/developer/embedding/
    {u'regex': ['http://instagr.am/p/*', 'http://instagr.am/p/*'],
     u'endpoint': 'http://api.instagram.com/oembed'},

    {u'regex': ['http://wordpress.tv/*'],
     u'endpoint': 'http://wordpress.tv/oembed/'},

    {u'regex': ['http://soundcloud.com/*', 'http://soundcloud.com/*/*',
                'http://soundcloud.com/*/sets/*', 'http://soundcloud.com/groups/*',
                'http://snd.sc/*', 'https://soundcloud.com/*'],
     u'endpoint': 'http://soundcloud.com/oembed'},

    # http://blog.screenr.com/post/2145539209/screenr-now-supports-oembed
    {u'regex': ['http://www.screenr.com/*', 'http://screenr.com/*'],
     u'endpoint': 'http://www.screenr.com/api/oembed.{format}'},

    {u'regex': ['https://itunes.apple.com/*'],
     u'endpoint': 'http://www.screenr.com/api/oembed.{format}'},
]


class WordpressEndPoint(oembed.OEmbedEndpoint):

    """Wordpress wait a for in his query params."""

    def __init__(self):
        url = 'http://public-api.wordpress.com/oembed/1.0/'
        urlSchemes = [r'regex:.*.wordpress\.com/.*']
        super(WordpressEndPoint, self).__init__(url, urlSchemes=urlSchemes)

    def request(self, url, **opt):
        query = opt
        query['for'] = 'plone'
        return super(WordpressEndPoint, self).request(url, **query)


def load_all_endpoints():
    endpoints = []

    endpoint = WordpressEndPoint()
    endpoints.append(endpoint)

    providers = REGEX_PROVIDERS

    for provider in providers:
        endpoint = oembed.OEmbedEndpoint(provider[u'endpoint'], provider[u'regex'])
        endpoints.append(endpoint)

    return endpoints
