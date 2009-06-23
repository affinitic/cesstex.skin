from plone.app.portlets.portlets.events import Renderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class MyEventRenderer(Renderer):

    _template = ViewPageTemplateFile('templates/events.pt')
