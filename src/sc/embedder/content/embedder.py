# -*- coding: utf-8 -*-
from collective import dexteritytextindexer
from five import grok
from lxml import cssselect
from lxml import etree
from lxml import html
from plone import api
from plone.app.textfield import RichText
from plone.dexterity.browser.base import DexterityExtensibleForm
from plone.dexterity.events import AddCancelledEvent
from plone.dexterity.events import EditCancelledEvent
from plone.dexterity.events import EditFinishedEvent
from plone.directives import dexterity
from plone.directives import form
from plone.formwidget.namedfile.widget import NamedImageWidget
from plone.namedfile.field import NamedImage as BaseNamedImage
from plone.namedfile.file import NamedImage as ImageValueType
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from Products.validation import validation
from sc.embedder import MessageFactory as _
from sc.embedder.interfaces import IConsumer
from sc.embedder.logger import logger
from urllib2 import HTTPError
from urllib2 import URLError
from z3c.form import button
from z3c.form.interfaces import IFieldWidget
from z3c.form.interfaces import IFormLayer
from z3c.form.widget import FieldWidget
from zope import schema, component
from zope.component import adapter
from zope.event import notify
from zope.interface import implementer
from zope.interface import Interface

import urllib2


grok.templatedir('templates')


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


class IEmbedder(form.Schema):
    """ A representation of a content embedder content type
    """

    dexteritytextindexer.searchable('text', 'alternate_content')

    form.order_before(**{'url': '*'})

    url = schema.TextLine(
        title=_(u'Multimedia URL'),
        description=_(u'The URL for your multimedia file. Can be a URL ' +
                      u'from YouTube, Vimeo, SlideShare, SoundCloud or ' +
                      u'other main multimedia websites.'),
        required=False,
    )

    width = schema.Int(
        title=_(u'Width'),
        description=_(u''),
        required=True,
    )

    height = schema.Int(
        title=_(u'Height'),
        description=_(u''),
        required=True,
    )

    embed_html = schema.Text(
        title=_(u'Embedded HTML code'),
        description=_(u'HTML code to render the embedded media'),
        required=True,
    )

    player_position = schema.Choice(
        title=_(u'Player position'),
        description=_(u''),
        default=u'Top',
        required=True,
        values=[u'Top', u'Bottom', u'Left', u'Right'],
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


class Embedder(dexterity.Item):
    """ A content embedder
    """
    grok.implements(IEmbedder)

    def image_thumb(self):
        ''' Return a thumbnail '''
        if not has_image(self):
            return None
        view = self.unrestrictedTraverse('@@images')
        return view.scale(fieldname='image',
                          scale='thumb').index_html()

    def tag(self, scale='thumb', css_class='tileImage', **kw):
        ''' Return a tag to the image '''
        if not (has_image(self)):
            return ''
        view = self.unrestrictedTraverse('@@images')
        return view.tag(fieldname='image',
                        scale=scale,
                        css_class=css_class,
                        **kw)


class BaseForm(DexterityExtensibleForm):
    """
    """

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
        except:
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
                logger.info(e)
        except URLError, e:
            # support offline mode
            logger.info('offline mode')

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
                except:
                    pass

    def get_fallback(self, url):
        supported_mime_types = ('video/mp4', 'video/ogg', 'video/webm')
        embedder_code = """
<iframe src="%(context_url)s/@@embedder_videojs?src=%(url)s&type=%(type)s"
        class="vjs-iframe"
        allowfullscreen="1" mozallowfullscreen="1" webkitallowfullscreen="1"
        frameborder="0">
</iframe>
"""
        request = urllib2.Request(url)
        request.get_method = lambda: 'HEAD'
        opener = urllib2.build_opener()
        response = opener.open(request)
        if response.headers.get('content-type') in supported_mime_types:
            return {'html': embedder_code % {'context_url': self.context.absolute_url(),
                                             'url': urllib2.quote(url, ''),
                                             'type': urllib2.quote(response.headers.get('content-type'), '')}}

    def load_oembed(self, action):
        url = self.widgets['url'].value

        v = validation.validatorFor('isURL')
        if v(url) != 1:
            api.portal.show_message(
                _(u'Invalid URL'), request=self.request, type='error')
            return

        json_data = self.get_data(
            url, maxwidth=None, maxheight=None, format='json')

        if json_data is None:
            json_data = self.get_fallback(url)
            if json_data is None:
                return
        for k, v in self.tr_fields.iteritems():
            if json_data.get(k):
                self.widgets[v].value = unicode(json_data[k])
        if json_data.get('thumbnail_url'):
            self.set_image(json_data.get('thumbnail_url'))

    def set_custom_embed_code(self, data):
        """ Return the code that embed the code. Could be with the
            original size or the custom chosen.
        """
        if 'embed_html' not in data:
            return
        tree = etree.HTML(data['embed_html'])
        sel = cssselect.CSSSelector('body > *')
        el = sel(tree)[0]

        if data.get('width', None):
            el.attrib['width'] = data['width'] and str(data['width']) or el.attrib['width']
        if data.get('height', None):
            el.attrib['height'] = data['height'] and str(data['height']) or el.attrib['height']

        data['embed_html'] = html.tostring(el)


class AddForm(BaseForm, dexterity.AddForm):
    grok.name('sc.embedder')
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


class EditForm(dexterity.EditForm, BaseForm):
    grok.context(IEmbedder)
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


class View(dexterity.DisplayForm):
    grok.context(IEmbedder)
    grok.require('zope2.View')
    grok.name('view')

    def get_player_pos_class(self):
        """ Returns the css class based on the position of the embed item.
        """
        pos = self.context.player_position
        css_class = '%s_embedded' % pos.lower()
        return css_class


class EmbedderVideoJS(grok.View):
    grok.context(Interface)
    grok.require('zope2.View')
    grok.name('embedder_videojs')
