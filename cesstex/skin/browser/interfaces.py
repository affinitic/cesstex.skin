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


class IManageIST(Interface):
    """
    Gestion de Institut Sainte Thérèse
    """

    def sendMailDemande():
        """
        Envoie une demande faite par le site
        """
