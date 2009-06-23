from plone.app.portlets.portlets.news import Renderer
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class MyNewsRenderer(Renderer):
    
     _template = ViewPageTemplateFile('templates/news.pt')