# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.Five import BrowserView
from zope.interface import implements
from cesstex.skin.browser.interfaces import IIstSalleDesProfsView
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize


class IstSalleDesProfsView(BrowserView):
    implements(IIstSalleDesProfsView)

    @memoize
    def getNews(self, nombre):
        """
        récupère les actualités (news)
        """
        catalog = getToolByName(aq_inner(self.context), 'portal_catalog')
        listMonToitNews = catalog(portal_type='News Item',
                                  review_state=('published',),
                                  sort_on='Date',
                                  sort_order='reverse',
                                  sort_limit=nombre)
        return listMonToitNews

    def getNewsIconURL(self, newsBrain):
        """
        récupère l'icône d'une news (ou celle par défaut)
        """
        news = newsBrain.getObject()
        if news.getImage():
            return 'image_tile'
        else:
            # image par défaut
            return 'news.png'

    @memoize
    def getEvents(self, nombre):
        """
        reécupère les événements-calendriers (events)
        """
        catalog = getToolByName(aq_inner(self.context), 'portal_catalog')
        listMonToitevents = catalog(portal_type='Event',
                                    review_state=('published',),
                                    sort_on='Date',
                                    sort_order='reverse',
                                    sort_limit=nombre)
        return [event.getObject() for event in listMonToitevents]

    @memoize
    def getPageText(self, pageId):
        page = getattr(self.context, pageId, None)
        if page is None:
            return
        return page.getText()

    def getIstManageNews(self):
        return self.getPageText('ist-manage-news')

    def getIstLaLouviereNews(self):
        return self.getPageText('ist-la-louviere-news')

    def getIstCefaManageNews(self):
        return self.getPageText('ist-cefa-manage-news')

    def getActualiteDuMoment(self):
        return self.getPageText('actualite-du-moment')
