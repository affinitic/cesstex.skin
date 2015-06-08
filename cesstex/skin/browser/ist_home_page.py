# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from zope.interface import implements
from cesstex.skin.browser.interfaces import IIstHomePageView
from plone.memoize.instance import memoize


class IstHomePageView(BrowserView):
    """
    gestion de la folderview du dossier IST (homePage)
    page divisée en trois blocs horizontaux
    """
    implements(IIstHomePageView)

    @memoize
    def getPageText(self, pageId):
        page = getattr(self.context, pageId, None)
        if page is None:
            return
        return page.getText()

    def getIstHomePageTopSection(self):
        """
        recupère le bloc sup de la page
        """
        return self.getPageText('ist_home_page_top_section')

    def getIstHomePageMiddleSection(self):
        """
        recupère le bloc central de la page
        """
        return self.getPageText('ist_home_page_middle_section')

    def getIstHomePageBottomSection(self):
        """
        recupère le bloc inf de la page
        """
        return self.getPageText('ist_home_page_bottom_section')
