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


class IManageISM(Interface):
    """
    Gestion de Institut Sainte Marie
    """
    def getNewsIsm():
        """
        liste les news
        """

    def getNewsIconURL(newsBrain):
        """
        récupère l'icône d'une news (ou celle par défaut)
        """


class IManageDossierDisciplinaire(Interface):
    """
    Gestion des dossiers disciplinaires
    """
    def getAllDossier():
        """
        recuperation de tous les dossiers disciplinaires
        """

    def insertDossierDisciplinaire():
        """
        insère un nouveau dossier disciplinaire
        """


class IManageIST(Interface):
    """
    Gestion de Institut Sainte Thérèse
    """

    def sendMailDemande():
        """
        Envoie une demande faite par le site
        """

    def traiterDemandeIst():
        """
        gère la demande et envoie mail selon implantation
        """

    def getNewsIst():
        """
        liste les news
        """

    def getNewsIconURL(newsBrain):
        """
        récupère l'icône d'une news (ou celle par défaut)
        """
