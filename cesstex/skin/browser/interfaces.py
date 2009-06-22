from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface

class ICesstexTheme(IDefaultPloneLayer):
    """
    Theme for cesstex
    """
class ILogoView(Interface):
    """
    Gestion des logo selon les sous-sites
    """
    def getLogo():
        """
        return the logo regarding folder
        """