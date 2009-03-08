from Acquisition import aq_inner, aq_parent                            
from Products.Five import BrowserView
from Products.CMFCore.utils import getToolByName

class PageCheckView(BrowserView):
    """
    Page check for CSS selection
    """

    def isHomePage(self):
        """Checks if the current object is in the portal root folder"""
        obj = self.context
        portalRoot = getToolByName(obj, 'portal_url').getPortalObject()
        parent = aq_parent(aq_inner(obj))
        isInRoot = (obj == portalRoot) or (parent == portalRoot)
        return isInRoot and  obj.meta_type != 'ATFolder'
