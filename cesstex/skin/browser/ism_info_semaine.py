# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

class IsmInfoSemaine(BrowserView):

    @memoize
    def getNews(self, nombre):
        catalog = getToolByName(aq_inner(self.context), 'portal_catalog')
        return catalog(portal_type='News Item',
                       review_state=('external', 'internal'),
                       isGlobal=1,
                       sort_on='Date',
                       sort_order='reverse',
                       sort_limit=nombre)

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
