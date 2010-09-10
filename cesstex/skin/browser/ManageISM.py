# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.Five import BrowserView
from zope.interface import implements
#from mailer import Mailer
from cesstex.skin.browser.interfaces import IManageISM
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

LIMIT = 10


class ManageISM(BrowserView):
    implements(IManageISM)

    @memoize
    def getEventsIsm(self):
        catalog = getToolByName(aq_inner(self.context), 'portal_catalog') 
        events = catalog(portal_type='Event',
                         review_state=('external', 'internal', 'publish'), 
                         path={'query': 'plone/institut-sainte-marie', 'depth': 1},
                         sort_on='start',
                         sort_order='reverse',
                         sort_limit=LIMIT)[:LIMIT]
        return events

    def getEventsIconURL(self, eventsBrain):
        """
        récupère l'icône d'une news (ou celle par défaut)
        """
        events = eventsBrain.getObject()
        if events.getImage():
            return 'image_tile'
        else:
            # image par défaut
            return 'events.gif'
