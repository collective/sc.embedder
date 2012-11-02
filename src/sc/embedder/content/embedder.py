# -*- coding:utf-8 -*-

from lxml import etree, cssselect

from five import grok

from zope import schema, component
from zope.event import notify

from Products.statusmessages.interfaces import IStatusMessage

from plone.app.textfield import RichText

from plone.directives import dexterity
from plone.directives import form

from plone.namedfile.field import NamedImage

from plone.dexterity.events import AddCancelledEvent
from plone.dexterity.events import EditFinishedEvent
from plone.dexterity.events import EditCancelledEvent

from z3c.form import button

from collective import dexteritytextindexer

from collective.oembed.interfaces import IConsumer

from sc.embedder import MessageFactory as _

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

grok.templatedir('templates')


class IEmbedder(form.Schema):
    """ A representation of a content embedder content type
    """

    dexteritytextindexer.searchable('text', 'alternate_content')

    form.order_before(**{'url': '*'})

    url = schema.TextLine(
        title=_(u"Multimedia URL"),
        description=_(u"The URL for your multimedia file. Can be a URL " + \
                      u"from YouTube, Vimeo, SlideShare, SoundCloud or " + \
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

    embed_html = schema.Text(
        title=_(u"Embed html code"),
        description=_(u"This code take care of render the embed " + \
                      u"multimedia item"),
        required=True,
        )

    player_position = schema.Choice(
        title=_(u"Player position"),
        description=_(u""),
        default=u'Top',
        required=True,
        values=[u'Top', u'Bottom', u'Left', u'Right'],
        )

    text = RichText(
        title=_(u"Body text"),
        required=False,
        )

    alternate_content = RichText(
        title=_(u"Alternate content"),
        description=_(u"Description or transcription to an individual " + \
                      u"that is no able to see or hear."),
        required=False,
        )

    image = NamedImage(
        title=_(u"Image"),
        description=_(u"A image to be used when listing content."),
        required=False,
        )


class Embedder(dexterity.Item):
    """ A content embedder
    """
    grok.implements(IEmbedder)


class AddForm(dexterity.AddForm):
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
        self.set_custom_embed_code(data)
        if errors:
            self.status = self.formErrorsMessage
            return
        obj = self.createAndAdd(data)
        if obj is not None:
            # mark only as finished if we get the new object
            self._finishedAdd = True
            IStatusMessage(self.request).addStatusMessage(
                                                _(u"Item created"), "info")

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
                    _(u"Operation cancelled."), "info")
        self.request.response.redirect(self.nextURL())
        notify(AddCancelledEvent(self.context))

    @button.buttonAndHandler(_('Load'), name='load')
    def handleLoad(self, action):
        fields = ['width', 'height', 'description', 'title', 'html']
        url = self.widgets['url'].value
        if url != '':
            consumer = component.getUtility(IConsumer)
            data = consumer.get_data(url, maxwidth=None, maxheight=None,
                                    format='json')
            if data is None:
                return
            for field in fields:
                if field in data.keys():
                    value = data[field]
                    if field == 'description':
                        field = 'IDublinCore.description'
                    elif field == 'title':
                        field = 'IDublinCore.title'
                    elif field == 'html':
                        field = 'embed_html'
                    self.widgets[field].value = value

    def set_custom_embed_code(self, data):
        """ Return the code that embed the code. Could be with the
            original size or the custom chosen.
        """
        tree = etree.HTML(data['embed_html'])
        sel = cssselect.CSSSelector('body > *')
        el = sel(tree)[0]

        if 'width' in data.keys():
            el.attrib['width'] = data['width'] and str(data['width']) or el.attrib['width']
        if 'height' in data.keys():
            el.attrib['height'] = data['height'] and str(data['height']) or el.attrib['height']

        data['embed_html'] = etree.tostring(el)

    def get_url_widget(self):
        widget = [key for key in self.widgets.values() \
                 if key.id == 'form-widgets-url']
        if widget != []:
            url_w = widget[0]
            return url_w

    def get_load_action(self):
        action = [key for key in self.actions.values() \
                 if key.id == 'form-buttons-load']
        if action != []:
            load = action[0]
            return load


class EditForm(dexterity.EditForm):
    grok.context(IEmbedder)
    template = ViewPageTemplateFile('templates/edit.pt')

    @button.buttonAndHandler(_(u'Apply'), name='save')
    def handleApply(self, action):
        data, errors = self.extractData()
        self.set_custom_embed_code(data)
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(
                                            _(u"Changes saved."), "info")
        self.request.response.redirect(self.nextURL())
        notify(EditFinishedEvent(self.context))

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
                                            _(u"Edit cancelled."), "info")
        self.request.response.redirect(self.nextURL())
        notify(EditCancelledEvent(self.context))

    @button.buttonAndHandler(_('Load'), name='load')
    def handleLoad(self, action):
        fields = ['width', 'height', 'description', 'title', 'html']
        url = self.widgets['url'].value
        if url != '':
            consumer = component.getUtility(IConsumer)
            data = consumer.get_data(url, maxwidth=None, maxheight=None,
                                    format='json')
            if data is None:
                return
            for field in fields:
                if field in data.keys():
                    value = data[field]
                    if field == 'description':
                        field = 'IDublinCore.description'
                    elif field == 'title':
                        field = 'IDublinCore.title'
                    elif field == 'html':
                        field = 'embed_html'
                    self.widgets[field].value = value

    def set_custom_embed_code(self, data):
        """ Return the code that embed the code. Could be with the
            original size or the custom chosen.
        """
        tree = etree.HTML(data['embed_html'])
        sel = cssselect.CSSSelector('body > *')
        el = sel(tree)[0]

        if 'width' in data.keys():
            el.attrib['width'] = data['width'] and str(data['width']) or el.attrib['width']
        if 'height' in data.keys():
            el.attrib['height'] = data['height'] and str(data['height']) or el.attrib['height']

        data['embed_html'] = etree.tostring(el)

    def get_url_widget(self):
        widget = [key for key in self.widgets.values() \
                 if key.id == 'form-widgets-url']
        if widget != []:
            url_w = widget[0]
            return url_w

    def get_load_action(self):
        action = [key for key in self.actions.values() \
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
        css_class = "%s_embedded" % pos.lower()
        return css_class
