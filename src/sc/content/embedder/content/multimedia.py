# -*- coding:utf-8 -*-

from five import grok

from zope import schema, component
from zope.event import notify

from z3c.form import button

from Products.statusmessages.interfaces import IStatusMessage

from plone.app.textfield import RichText

from plone.directives import dexterity
from plone.directives import form

from plone.namedfile.field import NamedImage

from plone.dexterity.events import AddCancelledEvent
from plone.dexterity.events import EditFinishedEvent
from plone.dexterity.events import EditCancelledEvent

from collective import dexteritytextindexer

from collective.oembed.interfaces import IConsumer

from sc.content.embedder import MessageFactory as _

from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


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

    html = schema.TextLine(
        title=_(u"Embed html code"),
        description=_(u"This code take care of render the embed" + \
                        " multimedia item"),
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
        required=False,
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


class AddForm(dexterity.AddForm):
    grok.name('sc.embedder.multimedia')

    template = ViewPageTemplateFile('multimedia_templates/' + \
                                    'sc.embedder.multimedia.pt')

    @button.buttonAndHandler(_('Save'), name='save')
    def handleAdd(self, action):
        data, errors = self.extractData()
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
                            _(u"Add New Item operation cancelled"), "info")
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
                    self.widgets[field].value = value

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
    grok.context(IMultimedia)
    template = ViewPageTemplateFile('multimedia_templates/' + \
                                    'edit.pt')

    @button.buttonAndHandler(_(u'Save'), name='save')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return
        self.applyChanges(data)
        IStatusMessage(self.request).addStatusMessage(
                                            _(u"Changes saved"), "info")
        self.request.response.redirect(self.nextURL())
        notify(EditFinishedEvent(self.context))

    @button.buttonAndHandler(_(u'Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(
                                            _(u"Edit cancelled"), "info")
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
                    self.widgets[field].value = value

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
    grok.context(IMultimedia)
    grok.require('zope2.View')
    grok.name('view')

    def get_player_pos_class(self):
        """ Returns the css class based on the position of the embed item.
        """
        pos = self.context.player_pos
        css_class = "%s_embedded" % pos.lower()
        return css_class
