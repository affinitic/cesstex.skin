from plone.theme.interfaces import IDefaultPloneLayer
from zope.interface import Interface


class IProfFolder(Interface):
    """
    Marker interface for shareable Prof Folders
    """


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


class IManageProfesseur(Interface):
    """
    Gestion des professeurs
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


class IManageISM(Interface):
    """
    Gestion de Institut Sainte Marie
    """

    def getIsmgInfoLaUne():
        """
        recupere le texte de ism-info-a-la-une
        """
