from Products.Five import BrowserView
from zope.interface import implements
from zope.security.interfaces import Unauthorized
from interfaces import ILogoView

class LogoView(BrowserView):
    """
    Gestion des logos
    """
    implements(ILogoView)

    def safe_getattr(self, obj, attr, default):
        """Attempts to read the attr, returning default if Unauthorized."""
        try:
            return getattr(obj, attr, default)
        except Unauthorized:
            return default

    def getLogo(self):
        """
        return the logo regarding folder
        """
        logo = self.safe_getattr(self.context, 'logo.png', None)
        if logo:
            return logo.tag()
        else:
            return None
