# -*- coding: utf-8 -*-

#import datetime
#import time
#import random
#from sqlalchemy import select, func, distinct
#from mailer import Mailer
#from LocalFS import LocalFS
from Products.Five import BrowserView
from zope.interface import implements
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


class ManageDossierDisciplinaire(BrowserView):
    implements(IManageDossierDisciplinaire)

    def getAllStatutMembre(self):
        """
        recuperation de tous les status des membres (prof, direction, educateur)
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        statutMembreTable = wrapper.getMapper('statut_membre')
        query = session.query(statutMembreTable)
        query = query.order_by(statutMembreTable.statmembre_statut)
        allStatutMembre = query.all()
        return allStatutMembre

    def getAllEtatPublication(self):
        """
        recuperation de tous les états de publication (privé, visible membre)
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        etatPublicationTable = wrapper.getMapper('etat_publication')
        query = session.query(etatPublicationTable)
        query = query.order_by(etatPublicationTable.etat_titre)
        allEtatPublication = query.all()
        return allEtatPublication

    def getAllProfesseurs(self):
        """
        recuperation de tous les professseurs
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        professeurTable = wrapper.getMapper('professeur')
        query = session.query(professeurTable)
        query = query.order_by(professeurTable.prof_nom)
        allProfesseurs = query.all()
        return allProfesseurs

    def getAllEleves(self):
        """
        recuperation de tous les professseurs
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        etudiantTable = wrapper.getMapper('etudiant')
        query = session.query(etudiantTable)
        query = query.order_by(etudiantTable.eleve_nom)
        allEleves = query.all()
        return allEleves

    def getAllDossiers(self):
        """
        recuperation de tous les dossiers disciplinaires
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        dossierTable = wrapper.getMapper('dossier_disciplinaire')
        query = session.query(dossierTable)
        allDossiers = query
        return allDossiers

    def insertEleve(self):
        """
        insère un nouveau dossier disciplinaire
        """
        fields = self.request.form

        nomEleve = fields.get('nomEleve', None)
        prenomEleve = fields.get('prenomEleve', None)
        classeEleve = fields.get('classeEleve', None)
        titulaire01Pk = fields.get('titulaire01Pk', None)
        titulaire02Pk = fields.get('titulaire02Pk', None)
        
        if not titulaire02Pk:
            titulaire02Pk = None
        
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        insertEtudiant = wrapper.getMapper('etudiant')
        newEntry = insertEtudiant(eleve_nom=nomEleve,
                                  eleve_prenom=prenomEleve,
                                  eleve_classe=classeEleve,
                                  eleve_prof_titulaire_01_fk=titulaire01Pk,
                                  eleve_prof_titulaire_02_fk=titulaire02Pk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        #elevePk = newEntry.form_pk

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le nouveau dossier concernant l'élève %s  a bien été créé !" % (nomEleve)
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/espace-interactif/ajouter-un-dossier-disciplinaire" % (portalUrl)
        self.request.response.redirect(url)
        return ''
