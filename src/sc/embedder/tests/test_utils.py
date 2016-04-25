# -*- coding: utf-8 -*-
from sc.embedder.utils import sanitize_iframe_tag

import unittest


class UtilsTestCase(unittest.TestCase):

    def test_sanitize_iframe_tag_slideshare(self):
        iframe = '<iframe src="//www.slideshare.net/slideshow/embed_code/key/JTepPmXR1Pgccr" width="595" height="485" frameborder="0" marginwidth="0" marginheight="0" scrolling="no" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/Pjoie/how-to-embed-powerpoint-presentation-using-slideshare" title="How to Embed PowerPoint Presentation Using Slideshare" target="_blank">How to Embed PowerPoint Presentation Using Slideshare</a> </strong> from <strong><a href="//www.slideshare.net/Pjoie" target="_blank">Joie Ocon</a></strong> </div>'
        expected = '<iframe src="//www.slideshare.net/slideshow/embed_code/key/JTepPmXR1Pgccr" width="595" height="485" style="border:1px solid #CCC; border-width:1px; margin-bottom:5px; max-width: 100%;" allowfullscreen> </iframe> <div style="margin-bottom:5px"> <strong> <a href="//www.slideshare.net/Pjoie/how-to-embed-powerpoint-presentation-using-slideshare" title="How to Embed PowerPoint Presentation Using Slideshare" target="_blank">How to Embed PowerPoint Presentation Using Slideshare</a> </strong> from <strong><a href="//www.slideshare.net/Pjoie" target="_blank">Joie Ocon</a></strong> </div>'
        self.assertIn(expected, sanitize_iframe_tag(iframe))

    def test_sanitize_iframe_tag_soundcloud(self):
        iframe = '<iframe width="100%" height="166" scrolling="no" frameborder="no" src="https://w.soundcloud.com/player/?visual=true&amp;url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F260347735&amp;show_artwork=true"></iframe>'
        expected = '<iframe width="100%" height="166" src="https://w.soundcloud.com/player/?visual=true&amp;url=http%3A%2F%2Fapi.soundcloud.com%2Ftracks%2F260347735&amp;show_artwork=true"></iframe>'
        self.assertIn(expected, sanitize_iframe_tag(iframe))

    def test_sanitize_iframe_tag_vimeo(self):
        iframe = '<iframe src="https://player.vimeo.com/video/85804536" width="640" height="360" frameborder="0" webkitallowfullscreen mozallowfullscreen allowfullscreen></iframe><p><a href="https://vimeo.com/85804536">Plone Community (italian subtitles)</a> from <a href="https://vimeo.com/abstractsrl">Abstract</a> on <a href="https://vimeo.com">Vimeo</a>.</p>'
        expected = '<iframe src="https://player.vimeo.com/video/85804536" width="640" height="360" allowfullscreen></iframe><p><a href="https://vimeo.com/85804536">Plone Community (italian subtitles)</a> from <a href="https://vimeo.com/abstractsrl">Abstract</a> on <a href="https://vimeo.com">Vimeo</a>.</p>'
        self.assertIn(expected, sanitize_iframe_tag(iframe))

    def test_sanitize_iframe_tag_youtube(self):
        iframe = '<iframe allowfullscreen="" frameborder="0" height="315" src="http://www.youtube.com/embed/UkWd0azv3fQ#t=2m30s" width="420"></iframe>'
        expected = '<iframe allowfullscreen="" height="315" src="http://www.youtube.com/embed/UkWd0azv3fQ#t=2m30s" width="420"></iframe>'
        self.assertIn(expected, sanitize_iframe_tag(iframe))
