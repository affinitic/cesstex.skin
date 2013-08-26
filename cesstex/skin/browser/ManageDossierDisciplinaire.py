# -*- coding: utf-8 -*-

#import datetime
#import time
#import random
#from sqlalchemy import select, func, distinct
#from mailer import Mailer
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
from cesstex.db.pgsql.baseTypes import Etudiant, Professeur, DossierDisciplinaire, EvenementActe, StatutMembre, EtatPublication, EvenementActeLogModification


class ManageDossierDisciplinaire(BrowserView):
    implements(IManageDossierDisciplinaire)

    def getAllStatutMembre(self):
        """
        recuperation de tous les status des membres (prof, direction, educateur)
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(StatutMembre)
        query = query.order_by(StatutMembre.statmembre_statut)
        allStatutMembre = query.all()
        return allStatutMembre

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
    def getAllProfesseurs(self):
        """
        recuperation de tous les professseurs
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Professeur)
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

        if not titulaire02Pk:
            titulaire02Pk = None

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = Etudiant(eleve_nom=eleveNom,
                            eleve_prenom=elevePrenom,
                            eleve_classe=eleveClasse,
                            eleve_prof_titulaire_01_fk=titulaire01Pk,
                            eleve_prof_titulaire_02_fk=titulaire02Pk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        elevePk = newEntry.eleve_pk

        self.insertDossier(elevePk, eleveNom, eleveClasse)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le nouveau dossier concernant l'élève %s  a bien été créé !" % (eleveNom)
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/espace-interactif/ajouter-un-dossier-disciplinaire" % (portalUrl)
        self.request.response.redirect(url)
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
        auteurConnecte = ismTools.getUserAuthenticated()

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
        query = query.order_by(EvenementActe.eventact_date_creation)
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

        
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = EvenementActe(eventact_auteur_creation=auteurConnecte,
                                 eventact_evenement=evenement,
                                 eventact_sanction=sanction,
                                 eventact_intervenant=intervenant,
                                 eventact_etat_publication_fk=etatPublication,
                                 eventact_dossier_diciplinaire_fk=dossierDisciplinairePk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        
        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le nouvel événement a bien été ajouté !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/espace-interactif/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
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

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"L'événement a bien été modifié !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/espace-interactif/ajouter-un-evenement-au-dossier?elevePk=%s" % (portalUrl, elevePk)
        self.request.response.redirect(url)
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
        
        import pdb; pdb.set_trace()
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = EvenementActeLogModification(eventactlogmodif_auteur_modification=auteurConnecte,
                                                eventactlogmodif_evenement_acte_fk=evenementActePk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        
        return ''
