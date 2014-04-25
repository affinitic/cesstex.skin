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

class IIsmInfoSemaine(Interface):
    """
    Gestion des news infos semaine sur la folder view ism
    """

    def getNews():
        """
        liste les news
        """

    def getNewsIconURL(newsBrain):
        """
        recupere l'icone d'une news (ou celle par defaut)
        """

class IIsmEventAgenda(Interface):
    """
    Gestion des events agenda sur la folder view ism
    """

    def getEvents():
        """
        liste les events
        """


class IManageISM(Interface):
    """
    Gestion de Institut Sainte Marie
    """
    def getAllProfesseurs():
        """
        recupere tous les professeurs ISM
        """

    def insertProfesseur():
        """
        insere un nouveau prof dans dbPg et dans aclUser
        """

    def updateProfesseur():
        """
        update un professeur dans dbPg et dans aclUser
        """

    def deleteProfesseur():
        """
        delete un professeur dans dbPg et dans aclUser
        """


class IManageDossierDisciplinaire(Interface):
    """
    Gestion des dossiers disciplinaires
    """
    def insertEvenementActe():
        """
        insere un nouvel evenement acte dans un dossier disciplinaire
        """

    def updateEvenementActe():
        """
        update un evenement acte dans un dossier disciplinaire
        """


class IManageIST(Interface):
    """
    Gestion de Institut Sainte Therese
    """

    def sendMailDemande():
        """
        Envoie une demande faite par le site
        """

    def traiterDemandeIst():
        """
        gere la demande et envoie mail selon implantation
        """

    def getNewsIst():
        """
        liste les news
        """

    def getNewsIconURL(newsBrain):
        """
        recupere l'icone d'une news (ou celle par defaut)
        """
