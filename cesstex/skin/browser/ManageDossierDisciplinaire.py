# -*- coding: utf-8 -*-

#import datetime
#import time
#import random
from sqlalchemy import desc
from mailer import Mailer
#from LocalFS import LocalFS
from Products.Five import BrowserView
from zope.interface import implements
from zope.component import getMultiAdapter
from z3c.sqlalchemy import getSAWrapper
#from plone.app.form.widgets.wysiwygwidget import WYSIWYGWidget
#from Products.CMFPlone.utils import normalizeString
from Products.CMFCore.utils import getToolByName
#from Products.CMFPlone import PloneMessageFactory as _
#from Products.AddRemoveWidget.AddRemoveWidget import AddRemoveWidget
#from Products.Archetypes.atapi import LinesField
#from Products.Archetypes.Renderer import renderer
#from Products.Archetypes.atapi import BaseContent
from interfaces import IManageDossierDisciplinaire
#from collective.captcha.browser.captcha import Captcha
from cesstex.db.pgsql.baseTypes import Etudiant, Professeur, DossierDisciplinaire, EvenementActe, EtatPublication, EvenementActeLogModification


class ManageDossierDisciplinaire(BrowserView):
    implements(IManageDossierDisciplinaire)

#### ENVOI DES MAILS ####
    def sendMail(self, sujet, message):
        """
        envoi de mail à clpsbw admin
        """
        mailer = Mailer("localhost", "alain.meurant@affinitic.be")
        #mailer = Mailer("relay.skynet.be", "alain.meurant@affinitic.be, houtain@clps-bw.be" )
        mailer.setSubject(sujet)
        mailer.setRecipients("alain.meurant@affinitic.be")
        mail = message
        mailer.sendAllMail(mail)

    def sendMailForNewDossier(self, elevePk):
        """
        envoi d'un mail lors de la création d'un nouveau dossier disciplinaire
        """
        eleve = self.getElevesByPk(elevePk)
        portalUrl = getToolByName(self.context, 'portal_url')()
        urlDossier = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
        sujet = "[ISM  :: dossier disciplinaire]"
        message = u"""<font color='#FF0000'><b>:: Ajout d'un nouveau dossier disciplinaire ::</b></font><br /><br />
                      Bonjour, <br />
                      Un nouveau dossier disciplinaire vient d'être créé.<br />
                      Il s'agit de l'étudiant:<br />
                      <ul>
                        <li>Nom : <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Prénom : <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Classe :  <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Titutlaire 1 : <font color='#ff9c1b'><b>%s %s</b></font></li>
                        <li>Titutlaire 2 : <font color='#ff9c1b'><b>%s %s</b></font></li>
                        <li>Edicateur : <font color='#ff9c1b'><b>%s %s</b></font></li>
                      </ul>
                      <hr />
                      Le dossier est accessible en cliquant <a href="%s">ici</a>
                   """ % (eleve.eleve_nom, \
                          eleve.eleve_prenom, \
                          eleve.eleve_classe, \
                          eleve.titulaire01.prof_prenom, \
                          eleve.titulaire01.prof_nom, \
                          eleve.titulaire02.prof_prenom, \
                          eleve.titulaire02.prof_nom, \
                          eleve.educateurReferent.prof_prenom, \
                          eleve.educateurReferent.prof_nom, \
                          urlDossier)
        self.sendMail(sujet, message.encode('utf-8'))

    def sendMailForNewEvenementActe(self, elevePk):
        """
        envoi d'un mail lors de la création d'un nouvel événement acté
        """
        eleve = self.getElevesByPk(elevePk)
        portalUrl = getToolByName(self.context, 'portal_url')()
        urlDossier = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
        sujet = "[ISM  :: dossier disciplinaire]"
        message = u"""<font color='#FF0000'><b>:: Ajout d'un nouvel événement acté ::</b></font><br /><br />
                      Bonjour, <br />
                      Un nouvel événement acté vient d'être créé.<br />
                      Il s'agit de l'étudiant:<br />
                      <ul>
                        <li>Nom : <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Prénom : <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Classe :  <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Titutlaire 1 : <font color='#ff9c1b'><b>%s %s</b></font></li>
                        <li>Titutlaire 2 : <font color='#ff9c1b'><b>%s %s</b></font></li>
                        <li>Edicateur : <font color='#ff9c1b'><b>%s %s</b></font></li>
                      </ul>
                      <hr />
                      Le dossier est accessible en cliquant <a href="%s">ici</a>
                   """ % (eleve.eleve_nom, \
                          eleve.eleve_prenom, \
                          eleve.eleve_classe, \
                          eleve.titulaire01.prof_prenom, \
                          eleve.titulaire01.prof_nom, \
                          eleve.titulaire02.prof_prenom, \
                          eleve.titulaire02.prof_nom, \
                          eleve.educateurReferent.prof_prenom, \
                          eleve.educateurReferent.prof_nom, \
                          urlDossier)
        self.sendMail(sujet, message.encode('utf-8'))

    def sendMailForModyfingEvenementActe(self, elevePk):
        """
        envoi d'un mail lors de la création d'un nouvel événement acté
        """
        eleve = self.getElevesByPk(elevePk)
        portalUrl = getToolByName(self.context, 'portal_url')()
        urlDossier = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
        sujet = "[ISM  :: dossier disciplinaire]"
        message = u"""<font color='#FF0000'><b>:: Modification d'un événement acté ::</b></font><br /><br />
                      Bonjour, <br />
                      Un événement acté vient d'être modifié.<br />
                      Il s'agit de l'étudiant:<br />
                      <ul>
                        <li>Nom : <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Prénom : <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Classe :  <font color='#ff9c1b'><b>%s</b></font></li>
                        <li>Titutlaire 1 : <font color='#ff9c1b'><b>%s %s</b></font></li>
                        <li>Titutlaire 2 : <font color='#ff9c1b'><b>%s %s</b></font></li>
                        <li>Edicateur : <font color='#ff9c1b'><b>%s %s</b></font></li>
                      </ul>
                      <hr />
                      Le dossier est accessible en cliquant <a href="%s">ici</a>
                   """ % (eleve.eleve_nom, \
                          eleve.eleve_prenom, \
                          eleve.eleve_classe, \
                          eleve.titulaire01.prof_prenom, \
                          eleve.titulaire01.prof_nom, \
                          eleve.titulaire02.prof_prenom, \
                          eleve.titulaire02.prof_nom, \
                          eleve.educateurReferent.prof_prenom, \
                          eleve.educateurReferent.prof_nom, \
                          urlDossier)
        self.sendMail(sujet, message.encode('utf-8'))


#### ETAT PUBLICATION ####
    def getAllEtatPublication(self):
        """
        recuperation de tous les états de publication (privé, visible membre)
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EtatPublication)
        query = query.order_by(EtatPublication.etat_titre)
        allEtatPublication = query.all()
        return allEtatPublication


#### PROFESSEURS ####
    def getAllProfesseurs(self, statutProf):
        """
        recuperation de tous les professseurs
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Professeur)
        query = query.filter(Professeur.prof_statut_fk == statutProf)
        query = query.order_by(Professeur.prof_nom)
        allProfesseurs = query.all()
        return allProfesseurs


#### ELEVES ####
    def getAllEleves(self):
        """
        recuperation de tous les élèves qui ont un dossier disciplinaire
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Etudiant)
        query = query.order_by(Etudiant.eleve_nom)
        allEleves = query.all()
        return allEleves

    def getElevesByPk(self, elevePk=None):
        """
        recuperation d'un élève selon sa pk
        """
        if not elevePk:
            fields = self.request.form
            elevePk = fields.get('elevePk', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Etudiant)
        query = query.filter(Etudiant.eleve_pk == elevePk)
        eleveByPk = query.one()
        return eleveByPk

    def insertEleve(self):
        """
        insère un nouvel élève dans la table etudaint
        insère un nouveau dossier dans la table dossier liè à cet élève
        """
        fields = self.request.form

        eleveNom = fields.get('nomEleve', None)
        elevePrenom = fields.get('prenomEleve', None)
        eleveClasse = fields.get('classeEleve', None)
        titulaire01Pk = fields.get('titulaire01Pk', None)
        titulaire02Pk = fields.get('titulaire02Pk', None)
        educateurReferent = fields.get('educateurReferent', None)

        if not titulaire02Pk:
            titulaire02Pk = None

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = Etudiant(eleve_nom=eleveNom,
                            eleve_prenom=elevePrenom,
                            eleve_classe=eleveClasse,
                            eleve_prof_titulaire_01_fk=titulaire01Pk,
                            eleve_prof_titulaire_02_fk=titulaire02Pk,
                            eleve_educateur_referent_fk=educateurReferent)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        elevePk = newEntry.eleve_pk

        self.insertDossier(elevePk, eleveNom, eleveClasse)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le nouveau dossier concernant l'élève %s  a bien été créé !" % (eleveNom)
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-dossier-disciplinaire" % (portalUrl)
        self.request.response.redirect(url)
        return ''

    def updateEleve(self):
        """
        mise à jour des données d'un élève dans la table etudaint
        """
        fields = self.request.form

        elevePk = fields.get('elevePk', None)
        eleveNom = fields.get('nomEleve', None)
        elevePrenom = fields.get('prenomEleve', None)
        eleveClasse = fields.get('classeEleve', None)
        titulaire01Pk = fields.get('titulaire01Pk', None)
        titulaire02Pk = fields.get('titulaire02Pk', None)
        educateurReferent = fields.get('educateurReferent', None)

        if not titulaire02Pk:
            titulaire02Pk = None

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Etudiant)
        query = query.filter(Etudiant.eleve_pk == elevePk)
        eleve = query.one()
        eleve.eleve_nom = unicode(eleveNom, 'utf-8')
        eleve.eleve_prenom = unicode(elevePrenom, 'utf-8')
        eleve.eleve_classe = unicode(eleveClasse, 'utf-8')
        eleve.eleve_prof_titulaire_01_fk = titulaire01Pk
        eleve.eleve_prof_titulaire_02_fk = titulaire02Pk
        eleve.eleve_educateur_referent_fk = educateurReferent

        session.flush()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le dossier concernant l'élève %s  a bien été modifié !" % (eleveNom)
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-dossier-disciplinaire" % (portalUrl)
        self.request.response.redirect(url)
        return ''

    def deleteEleve(self, elevePk=None):
        """
        suppression d'un eleve dans la table etudiant
        """
        if not elevePk:
            fields = self.request.form
            elevePk = fields.get('elevePk')

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Etudiant)
        query = query.filter(Etudiant.eleve_pk == elevePk)
        eleve = query.one()
        session.delete(eleve)
        session.flush()
        return ''



#### DOSSIERS DISCIPLINAIRES ####
    def getDossierId(self, elevePk, eleveNom, eleveClasse):
        """
        genere une id de dossier
        """
        ismTools = getMultiAdapter((self.context, self.request), name="manageISM")
        num = ismTools.getTimeStamp()
        dossierId = "ISM-%s-%s-%s-%s" % (elevePk, eleveNom, eleveClasse, num)
        return dossierId


    def getAllDossiers(self):
        """
        recuperation de tous les dossiers disciplinaires
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(DossierDisciplinaire)
        allDossiers = query.one()
        return allDossiers

    def getDossierByEleve(self, elevePk):
        """
        recuperation du dossier disciplinaire d'un student
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(DossierDisciplinaire)
        query = query.filter(DossierDisciplinaire.dosdis_pk == elevePk)
        dossierEleve = query.one()
        return dossierEleve

    def insertDossier(self, elevePk, eleveNom, eleveClasse):
        """
        insère un nouveau dossier disciplinaire
        """

        ismTools = getMultiAdapter((self.context, self.request), name="manageISM")
        #auteurConnecte = ismTools.getUserAuthenticated()

        dossierDisciplianireID = self.getDossierId(elevePk, eleveNom, eleveClasse)
        dossierDisciplianireAnneeScolaire = ismTools.getAnneeCourante()
        dossierDisciplianireElevePk = elevePk
# XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
        dossierDisciplianireAuteurPk = 2

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = DossierDisciplinaire(dosdis_id=dossierDisciplianireID,
                                        dosdis_annee_scolaire=dossierDisciplianireAnneeScolaire,
                                        dosdis_actif=True,
                                        dosdis_eleve_fk=dossierDisciplianireElevePk,
                                        dosdis_auteur_fk=dossierDisciplianireAuteurPk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)

        self.sendMailForNewDossier(elevePk)

        return ''

    def deleteDossierDisciplinaire(self):
        """
        Supprimer un dossier disciplinaire et ses event actés
        """
        fields = self.request.form

        dossierDisciplinairePk = fields.get('dossierDisciplinairePk')
        elevePk = fields.get('elevePk')
        #evenementActePk = fields.get('evenementActePk', None)
        self.deleteEvenementActeByDossierDisciplinaire(dossierDisciplinairePk)
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(DossierDisciplinaire)
        query = query.filter(DossierDisciplinaire.dosdis_pk == dossierDisciplinairePk)
        dossierDisciplinaire = query.one()
        session.delete(dossierDisciplinaire)
        session.flush()
        self.deleteEleve(elevePk)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le dossier disciplinaire et les événements qui lui sont liés ont bien été supprimés !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-dossier-disciplinaire" % (portalUrl)
        self.request.response.redirect(url)
        return ''

#### EVENEMENTS ACTES POUR UN DOSSIER ####

    def getAllEvenementByDossier(self, dossierDisciplinairePk):
        """
        recuperation de tous événements actés pour un dossier disciplinaire
        d'un élève
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_dossier_diciplinaire_fk == dossierDisciplinairePk)
        query = query.order_by(desc(EvenementActe.eventact_date_creation))
        AllEvenements = query.all()
        return AllEvenements

    def getEvenementByPk(self, evenementActePk):
        """
        recuperation d'un événement acté szlon sa pk
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_pk == evenementActePk)
        evenementActe = query.one()
        return evenementActe

    def getNombreEvenementActeByDossier(self, dossierDisciplinairePk):
        """
        Somme de tous les evenements actes pour un dossier
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_dossier_diciplinaire_fk == dossierDisciplinairePk)
        evenementActe = query.all()
        nombreEvenementActe = len(evenementActe)
        return nombreEvenementActe

    def getNombreEvenementActeByEleve(self, eleveDossierPk):
        """
        Somme de tous les evenements actes pour un élève
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_dossier_diciplinaire_fk == eleveDossierPk)
        evenementActe = query.all()
        nombreEvenementActe = len(evenementActe)
        return nombreEvenementActe


    def insertEvenementActe(self):
        """
        insère un nouveau dossier disciplinaire
        """

        ismTools = getMultiAdapter((self.context, self.request), name="manageISM")
        auteurConnecte = ismTools.getUserAuthenticated()

        fields = self.request.form

        elevePk = fields.get('elevePk')
        evenement = fields.get('evenement', None)
        sanction = fields.get('sanction', None)
        intervenant = fields.get('intervenant', None)
        etatPublication = fields.get('etatPublication', None)
        dossierDisciplinairePk = fields.get('dossierDisciplinairePk', None)

        nombreEvenementActeDossier = self.getNombreEvenementActeByDossier(dossierDisciplinairePk)
        evenementNumeroOrdre = nombreEvenementActeDossier + 1

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = EvenementActe(eventact_auteur_creation=auteurConnecte,
                                 eventact_evenement=evenement,
                                 eventact_sanction=sanction,
                                 eventact_intervenant=intervenant,
                                 eventact_etat_publication_fk=etatPublication,
                                 eventact_numero_ordre=evenementNumeroOrdre,
                                 eventact_dossier_diciplinaire_fk=dossierDisciplinairePk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        
        self.sendMailForNewEvenementActe(elevePk)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le nouvel événement a bien été ajouté !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
        self.request.response.redirect(url)
        return ''

    def updateEvenementActe(self):
        """
        Updates un événement acté lié à un dossier
        """
        fields = self.request.form

        elevePk = fields.get('elevePk')
        evenementActePk = fields.get('evenementActePk', None)
        evenement = fields.get('evenement', None)
        sanction = fields.get('sanction', None)
        intervenant = fields.get('intervenant', None)
        etatPublication = fields.get('etatPublication', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_pk == evenementActePk)
        evenementActe = query.one()
        evenementActe.eventact_evenement = unicode(evenement, 'utf-8')
        evenementActe.eventact_sanction = unicode(sanction, 'utf-8')
        evenementActe.eventact_intervenant = unicode(intervenant, 'utf-8')
        evenementActe.eventact_etat_publication_fk = etatPublication
        session.flush()

        self.insertLogModificationEvenementActe(evenementActePk)
        self.sendMailForModyfingEvenementActe(elevePk)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"L'événement a bien été modifié !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
        self.request.response.redirect(url)
        return ''

    def deleteEvenementActe(self):
        """
        Supprimer un événement acté lié à un dossier
        """
        fields = self.request.form

        elevePk = fields.get('elevePk')
        evenementActePk = fields.get('evenementActePk', None)

        self.deleteLogModificationEvenementActe()

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_pk == evenementActePk)
        evenementActe = query.one()
        session.delete(evenementActe)
        session.flush()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"L'événement a bien été supprimé !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/la-salle-des-profs/gestion-des-dossiers-disciplinaires/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
        self.request.response.redirect(url)
        return ''

    def deleteEvenementActeByDossierDisciplinaire(self, dossierDisciplinairePk):
        """
        Supprimer les événements actés lié à un dossier
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActe)
        query = query.filter(EvenementActe.eventact_dossier_diciplinaire_fk == dossierDisciplinairePk)
        allEvenementsActes = query.all()
        for evenementActe in allEvenementsActes:
            evenementActePk = evenementActe.eventact_pk
            self.deleteLogModificationEvenementActe(evenementActePk)
            session.delete(evenementActe)
        session.flush()
        return ''


 #### LOG MODIFICATION EVENEMENTS ACTES POUR UN DOSSIER ####
    def getAllLogModificationForEvenementActe(self, evenementActePk):
        """
        recuperation de tous les logs de modifications pour une événement acté
        pour un dossier disciplinaire d'un élève
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActeLogModification)
        query = query.filter(EvenementActeLogModification.eventactlogmodif_evenement_acte_fk == evenementActePk)
        query = query.order_by(EvenementActeLogModification.eventactlogmodif_date_modification)
        AllLogForEvenement = query.all()
        return AllLogForEvenement

    def insertLogModificationEvenementActe(self, evenementActePk):
        """
        insère un nouveau log pour une modification d'un événement acté
        """

        ismTools = getMultiAdapter((self.context, self.request), name="manageISM")
        auteurConnecte = ismTools.getUserAuthenticated()

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = EvenementActeLogModification(eventactlogmodif_auteur_modification=auteurConnecte,
                                                eventactlogmodif_evenement_acte_fk=evenementActePk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)

        return ''

    def deleteLogModificationEvenementActe(self, evenementActePk=None):
        """
        Supprimer les log de modifications d'un événement acté lors
        de la suppression de cet événement.
        """
        #elevePk = fields.get('elevePk') 
        if not evenementActePk:
            fields = self.request.form
            evenementActePk = fields.get('evenementActePk', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EvenementActeLogModification)
        query = query.filter(EvenementActeLogModification.eventactlogmodif_evenement_acte_fk == evenementActePk)
        evenementActeLog = query.all()
        for pk in evenementActeLog:
            session.delete(pk)
        session.flush()

        return ''
