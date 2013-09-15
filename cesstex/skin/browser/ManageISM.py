# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.Five import BrowserView
from zope.interface import implements
#from mailer import Mailer
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize
from datetime import date, datetime
from z3c.sqlalchemy import getSAWrapper
from cesstex.db.pgsql.baseTypes import Professeur, StatutMembre
from interfaces import IManageISM

LIMIT = 10


class ManageISM(BrowserView):
    implements(IManageISM)

    @memoize
    def getEventsIsm(self):
        catalog = getToolByName(aq_inner(self.context), 'portal_catalog')
        events = catalog(portal_type='Event',
                         review_state=('external', 'internal', 'publish'),
                         path={'query': 'plone/institut-sainte-marie', 'depth': 1},
                         sort_on='start',
                         sort_order='ascending',
                         sort_limit=LIMIT)[:LIMIT]
        return events

    def getEventsIconURL(self, eventsBrain):
        """
        récupère l'icône d'une news (ou celle par défaut)
        """
        events = eventsBrain.getObject()
        if events.getImage():
            return 'image_tile'
        else:
            # image par défaut
            return 'events.gif'

    def getAnneeCourante(self):
        """
        recupere l'annee courante
        """
        today = date.today()
        return today.year

    def getTimeStamp(self):
        timeStamp = datetime.now()
        return timeStamp


### GESTION DES PROFS ###
    def addLoginProfesseur(self, login, passw, role):
        """
        ajoute le login et le pass d'un professeur
        le role est ProfISM
        """
        uf = getToolByName(self.context, 'acl_users')
        uf.userFolderAddUser(login, passw, [role], [])

    def addInfoProfesseur(self, userId, userEmail, userName):
        """
        ajoute l'email du professeur
        """
        membership = getToolByName(self.context, 'portal_membership')
        member = membership.getMemberById(userId)
        properties = {}
        properties['email'] = userEmail
        properties['fullname'] = userName
        getToolByName(self, 'plone_utils').setMemberProperties(member, **properties)

    def delLoginProfesseur(self, login):
        """
        supprime le login et le pass d'un professeur
        le role est ProfISM
        """
        uf = getToolByName(self.context, 'acl_users')
        uf.userFolderDelUsers([login])

    def getUserAuthenticated(self):
        """
        retourne le nom du user loggué
        """
        pm = getToolByName(self.context, 'portal_membership')
        user = pm.getAuthenticatedMember()
        user = user.getUserName()
        return user

    def getRoleUserAuthenticated(self):
        """
        retourne le nom du user loggué
        """
        pm = getToolByName(self.context, 'portal_membership')
        user = pm.getAuthenticatedMember()
        userRole = user.getRoles()
        return userRole

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

    def getProfesseurByPk(self, profPk):
        """
        recuperation d'un professseur selon sa pk
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Professeur)
        query = query.filter(Professeur.prof_pk == profPk)
        professeur = query.one()
        return professeur

    def insertProfesseur(self):
        """
        insère un nouveau dossier disciplinaire
        """
        fields = self.request.form

        profNom = fields.get('profNom')
        profPrenom = fields.get('profPrenom', None)
        profEmail = fields.get('profEmail', None)
        profLogin = fields.get('profLogin', None)
        profPass = fields.get('profPass', None)
        profStatutFk = fields.get('profStatutFk', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = Professeur(prof_nom=profNom,
                              prof_prenom=profPrenom,
                              prof_email=profEmail,
                              prof_login=profLogin,
                              prof_pass=profPass,
                              prof_statut_fk=profStatutFk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)
        profPk = newEntry.prof_pk

        userProf = ('%s %s')%(profPrenom, profNom)
        userRole = 'ProfISM'
        self.addLoginProfesseur(profLogin, profPass, userRole)
        self.addInfoProfesseur(profLogin, profEmail, userProf)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le nouveau membre a bien été ajouté !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/ajouter-un-professeur" % (portalUrl)
        self.request.response.redirect(url)
        return ''

    def updateProfesseur(self):
        """
        Updates un événement acté lié à un dossier
        """
        fields = self.request.form

        profPk = fields.get('profPk')
        profNom = fields.get('profNom')
        profPrenom = fields.get('profPrenom', None)
        profEmail = fields.get('profEmail', None)
        profLogin = fields.get('profLogin', None)
        profPass = fields.get('profPass', None)
        profStatusFk = fields.get('profStatusFk', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Professeur)
        query = query.filter(Professeur.prof_pk == profPk)
        professeur = query.one()
        professeur.prof_nom = unicode(profNom, 'utf-8')
        professeur.prof_prenom = unicode(profPrenom, 'utf-8')
        professeur.prof_email = unicode(profEmail, 'utf-8')
        professeur.prof_login = unicode(profLogin, 'utf-8')
        professeur.prof_pass = unicode(profPass, 'utf-8')
        professeur.prof_status_fk = profStatusFk
        session.flush()

        userProf = ('%s %s')%(profPrenom, profNom)
        userRole = 'ProfISM'
        self.addLoginProfesseur(profLogin, profPass, userRole)
        self.addInfoProfesseur(profLogin, profEmail, userProf)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le professeur a bien été modifié !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/ajouter-un-professeur?profPk=%s" % (portalUrl, profPk)
        self.request.response.redirect(url)
        return ''

    def deleteProfesseur(self):
        """
        Supprimer un événement acté lié à un dossier
        """
        fields = self.request.form

        profPk = fields.get('profPk', None)
        profLogin = fields.get('profLogin', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Professeur)
        query = query.filter(Professeur.prof_pk == profPk)
        professeur = query.one()
        session.delete(professeur)
        session.flush()

        self.delLoginProfesseur(profLogin)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le professeur a bien été supprimé !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/ajouter-un-professeur?profPk=%s" % (portalUrl, profPk)
        self.request.response.redirect(url)
        return ''

