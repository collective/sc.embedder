# -*- coding: utf-8 -*-
from lxml import cssselect
from lxml import etree
from lxml import html
from lxml.html.builder import DIV
from plone import api
from plone.app.textfield import RichText
from plone.app.textfield.interfaces import ITransformer
from plone.autoform import directives as form
from plone.dexterity.browser.add import DefaultAddForm
from plone.dexterity.browser.add import DefaultAddView
from plone.dexterity.browser.base import DexterityExtensibleForm
from plone.dexterity.browser.edit import DefaultEditForm
from plone.dexterity.content import Item
from plone.dexterity.events import AddCancelledEvent
from plone.dexterity.events import EditCancelledEvent
from plone.dexterity.events import EditFinishedEvent
from plone.formwidget.namedfile.widget import NamedImageWidget
from plone.indexer import indexer
from plone.namedfile.field import NamedImage as BaseNamedImage
from plone.namedfile.file import NamedImage as ImageValueType
from plone.supermodel import model
from Products.CMFPlone.utils import safe_unicode
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from sc.embedder import MessageFactory as _
from sc.embedder.interfaces import IConsumer
from sc.embedder.logger import logger
from sc.embedder.utils import sanitize_iframe_tag
from sc.embedder.utils import validate_int_or_percentage
from urllib2 import HTTPError
from urllib2 import URLError
from z3c.form import button
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.widget import FieldWidget
from zope import component
from zope import schema
from zope.component import adapter
from zope.event import notify
from zope.interface import implementer
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

import requests
import urllib2
import urlparse


def has_image(content):
    image = content.image
    return (image and image.getSize())


class EmbedderImageWidget(NamedImageWidget):

    klass = u'embedder-image-widget'

    @property
    def download_url(self):
        if self.field is None:
            return None
        if getattr(self, 'url', None):
            return self.url
        if self.ignoreContext:
            return None
        if self.filename_encoded:
            return '%s/++widget++%s/@@download/%s' % (self.request.getURL(),
                                                      self.name,
                                                      self.filename_encoded)
        else:
            return '%s/++widget++%s/@@download' % (self.request.getURL(),
                                                   self.name)


class NamedImage(BaseNamedImage):
    """
    Do not conflict with plone.formwidget.namedfile widget implementation.
    """


@implementer(IFieldWidget)
@adapter(NamedImage, IFormLayer)
def EmbedderImageFieldWidget(field, request):
    return FieldWidget(field, EmbedderImageWidget(request))


class IEmbedder(model.Schema):
    """ A representation of a content embedder content type
    """

    form.order_before(**{'url': '*'})

    url = schema.ASCIILine(
        title=_(u'Multimedia URL'),
        description=_(
            u'The URL for your multimedia file. Can be a URL '
            + u'from YouTube, Vimeo, SlideShare, SoundCloud or '
            + u'other main multimedia websites.',
        ),
        required=False,
    )

    width = schema.ASCIILine(
        title=_(u'Width'),
        description=_(
            u'Can be expressed as a decimal number or a percentage, e.g., 270 or 50%.'),
        required=True,
        constraint=validate_int_or_percentage,
    )

    height = schema.Int(
        title=_(u'Height'),
        description=_(u'Can be expressed as a decimal number, e.g., 480.'),
        required=True,
        min=1,
        max=9999,
    )

    embed_html = schema.Text(
        title=_(u'Embedded HTML code'),
        description=_(u'HTML code to render the embedded media.'),
        required=True,
    )

    player_position = schema.Choice(
        title=_(u'Player position'),
        description=_(u''),
        default=u'Top',
        required=True,
        vocabulary=SimpleVocabulary([
            SimpleTerm(value=u'Top', title=_(u'Top')),
            SimpleTerm(value=u'Bottom', title=_(u'Bottom')),
            SimpleTerm(value=u'Left', title=_(u'Left')),
            SimpleTerm(value=u'Right', title=_(u'Right')),
        ]),
    )

    form.widget(image=EmbedderImageFieldWidget)
    image = NamedImage(
        title=_(u'Preview image'),
        description=_(u'Image to be used when listing content.'),
        required=False,
    )

    text = RichText(
        title=_(u'Body text'),
        required=False,
    )

    alternate_content = RichText(
        title=_(u'Alternate content'),
        description=_(u'Description or transcription for accessibility (WCAG) users.'),
        required=False,
    )


@implementer(IEmbedder)
class Embedder(Item):

    """A content embedder."""

    def image_thumb(self):
        """Return a thumbnail."""

        if not has_image(self):
            return None
        view = self.unrestrictedTraverse('@@images')
        return view.scale(fieldname='image',
                          scale='thumb').index_html()

    def tag(self, scale='thumb', css_class='tileImage', **kw):
        """Return a tag to the image."""

        if not (has_image(self)):
            return ''
        view = self.unrestrictedTraverse('@@images')
        return view.tag(fieldname='image',
                        scale=scale,
                        css_class=css_class,
                        **kw)


class BaseForm(DexterityExtensibleForm):

    """Methods and attributes shared by Add and Edit form."""

    tr_fields = {'width': 'width',
                 'height': 'height',
                 'description': 'IDublinCore.description',
                 'title': 'IDublinCore.title',
                 'html': 'embed_html'}

    def set_image(self, url):
        opener = urllib2.build_opener()
        try:
            response = opener.open(url)
            self.widgets['image'].url = url
            self.widgets['image'].value = ImageValueType(data=response.read(),
                                                         filename=url.split('/')[-1])
            self.request['form.widgets.image.action'] = u'load'
        except (IOError, URLError, HTTPError):
            pass

    def get_data(self, url, maxwidth=None, maxheight=None, format='json'):
        """Return the data provided by the endpoint."""

        consumer = component.getUtility(IConsumer)
        json_data = None
        try:
            json_data = consumer.get_data(
                url, maxwidth=None, maxheight=None, format='json')
        except HTTPError, e:
            if e.code == 401:
                api.portal.show_message(
                    _(u'Unauthorized request'), request=self.request, type='error')
            elif e.code == 404:
                api.portal.show_message(
                    _(u'URL not found'), request=self.request, type='error')
            else:
                logger.warn(e)
        except URLError, e:
            # support offline mode
            logger.warn('offline mode')

        return json_data

    def handle_image(self, data):
        url = self.widgets['url'].value
        action = self.request.get('form.widgets.image.action', None)
        if action == 'load':
            json_data = self.get_data(
                url, maxwidth=None, maxheight=None, format='json')
            if json_data.get('thumbnail_url'):
                opener = urllib2.build_opener()
                try:
                    response = opener.open(json_data.get('thumbnail_url'))
                    data['image'] = ImageValueType(data=response.read(),
                                                   filename=json_data.get('thumbnail_url').split('/')[-1])
                except (IOError, URLError, HTTPError):
                    pass

    def get_fallback(self, url):
        supported_mime_types = ('video/mp4', 'video/ogg', 'video/webm')
        embedder_code = """
<iframe src="%(context_url)s/@@embedder_videojs?src=%(url)s&type=%(type)s"
        class="vjs-iframe"
        allowfullscreen>
</iframe>
"""
        r = requests.head(url)
        if r.headers.get('content-type') in supported_mime_types:
            return {'html': embedder_code % {'context_url': self.context.absolute_url(),
                                             'url': urllib2.quote(url, ''),
                                             'type': urllib2.quote(r.headers.get('content-type'), '')}}

    def _validate_url(self, url):
        """Validate if is a valid URL for site.

        :param url: [required] URL to validate.
        :type url: unicode
        :returns: True if valid site URL
        :rtype: bool
        """
        pieces = urlparse.urlparse(url)
        # Must have a net location (ex: www.youtube.com)
        if pieces.netloc == '':
            return False
        if pieces.scheme not in ('http', 'https'):
            return False
        return True

    def load_oembed(self, action):
        url = self.widgets['url'].value

        if not self._validate_url(url):
            api.portal.show_message(
                _(u'Invalid URL'), request=self.request, type='error')
            return

        json_data = self.get_data(
            url, maxwidth=None, maxheight=None, format='json')

        if json_data is None:
            json_data = self.get_fallback(url)
            if json_data is None:
                return
        # html parameter not always required:
        # https://github.com/abarmat/python-oembed/blob/master/oembed/__init__.py#L157-L167
        # https://github.com/abarmat/python-oembed/blob/master/oembed/__init__.py#L181-L187
        if 'html' in json_data:
            json_data['html'] = sanitize_iframe_tag(json_data['html'])
        for k, v in self.tr_fields.iteritems():
            if json_data.get(k):
                self.widgets[v].value = unicode(json_data[k])
        if json_data.get('thumbnail_url'):
            self.set_image(json_data.get('thumbnail_url'))

    def set_custom_embed_code(self, data):
        """Return the code that embed the code.

        Could be with the original size or the custom chosen.
        """
        if 'embed_html' not in data:
            return
        tree = etree.HTML(data['embed_html'])
        sel = cssselect.CSSSelector('body > *')
        el = sel(tree)
        # add a div around if there is more than one element into code
        if len(el) > 1:
            el = DIV(*el)
        else:
            el = el[0]

        # width and height attributes should not be set in a div tag
        if el.tag in ['iframe', 'object']:
            if data.get('width', None):
                el.attrib['width'] = data['width'] and str(data['width']) or el.attrib['width']
            if data.get('height', None):
                el.attrib['height'] = data['height'] and str(data['height']) or el.attrib['height']

        data['embed_html'] = sanitize_iframe_tag(html.tostring(el))


class AddForm(BaseForm, DefaultAddForm):
    template = ViewPageTemplateFile('templates/sc.embedder.pt')

    @button.buttonAndHandler(_('Save'), name='save')
    def handleAdd(self, action):
        if self.request.get('form.widgets.url') and \
           not self.request.get('form.widgets.embed_html'):
            fields = {'width': 'form.widgets.width',
                      'height': 'form.widgets.height',
                      'description': 'form.widgets.IDublinCore.description',
                      'title': 'form.widgets.IDublinCore.title',
                      'html': 'form.widgets.embed_html'}
            consumer = component.getUtility(IConsumer)
            json_data = consumer.get_data(self.request['form.widgets.url'],
                                          maxwidth=None,
                                          maxheight=None,
                                          format='json')
            for k, v in fields.iteritems():
                if json_data.get(k):
                    self.request[v] = unicode(json_data[k])
        data, errors = self.extractData()
        self.handle_image(data)
        self.set_custom_embed_code(data)
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True
            api.portal.show_message(
                _(u'Item created'), self.request, type='info')

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        api.portal.show_message(
            _(u'Add New Item operation cancelled.'), self.request, type='info')
        self.request.response.redirect(self.nextURL())
        notify(AddCancelledEvent(self.context))

    @button.buttonAndHandler(_('Load'), name='load')
    def handleLoad(self, action):
        self.load_oembed(action)

    def get_url_widget(self):
        widget = [key for key in self.widgets.values()
                  if key.id == 'form-widgets-url']
        if widget != []:
            url_w = widget[0]
            return url_w

    def get_load_action(self):
        action = [key for key in self.actions.values()
                  if key.id == 'form-buttons-load']
        if action != []:
            load = action[0]
            return load


class AddView(DefaultAddView):
    form = AddForm


class EditForm(DefaultEditForm, BaseForm):
    template = ViewPageTemplateFile('templates/edit.pt')

    @button.buttonAndHandler(_('Load'), name='load')
    def handleLoad(self, action):
        self.load_oembed(action)

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):
        data, errors = self.extractData()
        self.handle_image(data)
        self.set_custom_embed_code(data)
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        api.portal.show_message(
            _(u'Changes saved.'), self.request, type='info')
        self.request.response.redirect(self.nextURL())
        notify(EditFinishedEvent(self.context))

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        api.portal.show_message(
            _(u'Edit cancelled.'), self.request, type='info')
        self.request.response.redirect(self.nextURL())
        notify(EditCancelledEvent(self.context))

    def get_url_widget(self):
        widget = [key for key in self.widgets.values()
                  if key.id == 'form-widgets-url']
        if widget != []:
            url_w = widget[0]
            return url_w

    def get_load_action(self):
        action = [key for key in self.actions.values()
                  if key.id == 'form-buttons-load']
        if action != []:
            load = action[0]
            return load


class View(BrowserView):
    index = ViewPageTemplateFile('templates/view.pt')

    def get_player_pos_class(self):
        """ Returns the css class based on the position of the embed item.
        """
        pos = self.context.player_position
        css_class = '%s_embedded' % pos.lower()
        return css_class

    def __call__(self):
        return self.index()


class EmbedderVideoJS(BrowserView):
    index = ViewPageTemplateFile('templates/embeddervideojs.pt')

    def __call__(self):
        return self.index()


@indexer(IEmbedder)
def searchable_text_indexer(obj):
    """SearchableText should contain id, title, description, body text,
    alternate text and keywords.
    """
    transformer = ITransformer(obj)

    try:
        text = transformer(obj.text, 'text/plain')
    except AttributeError:
        text = ''

    try:
        alternate_text = transformer(obj.alternate_content, 'text/plain')
    except AttributeError:
        alternate_text = ''

    keywords = u' '.join(safe_unicode(s) for s in obj.Subject())

    return u' '.join((
        safe_unicode(obj.id),
        safe_unicode(obj.title) or u'',
        safe_unicode(obj.description) or u'',
        safe_unicode(text),
        safe_unicode(alternate_text),
        safe_unicode(keywords),
    ))
