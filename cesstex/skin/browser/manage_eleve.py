# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from zope.interface import implements
# from mailer import Mailer
from Products.CMFCore.utils import getToolByName
from z3c.sqlalchemy import getSAWrapper
from cesstex.db.pgsql.baseTypes import EleveIsm
from interfaces import IManageISM


class ManageEleve(BrowserView):
    implements(IManageISM)

### GESTION DES PROFS ###
    def addLoginEleve(self, login, passw, role):
        """
        ajoute le login et le pass d'un élève
        le role est EleveISM
        """
        uf = getToolByName(self.context, 'acl_users')
        uf.userFolderAddUser(login, passw, [role], [])

    def addInfoEleve(self, userId, userEmail, userName):
        """
        ajoute l'email de l'élève
        """
        membership = getToolByName(self.context, 'portal_membership')
        member = membership.getMemberById(userId)
        properties = {}
        properties['email'] = userEmail
        properties['fullname'] = userName
        getToolByName(self, 'plone_utils').setMemberProperties(member, **properties)

    def delLoginEleve(self, login):
        """
        supprime le login et le pass d'un élève
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

    def getAllEleves(self):
        """
        recuperation de tous les élèves
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EleveIsm)
        query = query.order_by(EleveIsm.eleveism_classe_fk)
        allEleves = query.all()
        return allEleves

    def getEleveByPk(self, elevePk):
        """
        recuperation d'un eleve selon sa pk
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EleveIsm)
        query = query.filter(EleveIsm.eleveism_pk == elevePk)
        eleve = query.one()
        return eleve

    def insertEleve(self):
        """
        insère un nouvel eleve
        """
        fields = self.context.REQUEST

        eleveNom = getattr(fields, 'eleveNom')
        elevePrenom = getattr(fields, 'elevePrenom', None)
        eleveLogin = getattr(fields, 'eleveLogin', None)
        elevePass = getattr(fields, 'elevePass', None)
        eleveEmail = getattr(fields, 'eleveEmail', None)
        eleveClasseFk = getattr(fields, 'eleveClasseFk', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = EleveIsm(eleveism_nom=eleveNom,
                            eleveism_prenom=elevePrenom,
                            eleveism_login=eleveLogin,
                            eleveism_pass=elevePass,
                            eleveism_email=eleveEmail,
                            eleveism_classe_fk=eleveClasseFk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)

        userEleve = ('%s %s') % (elevePrenom, eleveNom)
        userRole = 'EleveISM'
        self.addLoginEleve(eleveLogin, elevePass, userRole)
        self.addInfoEleve(eleveLogin, eleveEmail, userEleve)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le nouvel élève a bien été ajouté !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/ajouter-un-eleve-ism" % (portalUrl)
        self.request.response.redirect(url)
        return ''

    def updateEleve(self):
        """
        Updates un événement acté lié à un dossier
        """

        fields = self.context.REQUEST

        elevePk = getattr(fields, 'elevePk')
        eleveNom = getattr(fields, 'eleveNom')
        elevePrenom = getattr(fields, 'elevePrenom', None)
        eleveEmail = getattr(fields, 'eleveEmail', None)
        eleveLogin = getattr(fields, 'eleveLogin', None)
        elevePass = getattr(fields, 'elevePass', None)
        eleveClasseFk = getattr(fields, 'eleveClasseFk', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EleveIsm)
        query = query.filter(EleveIsm.eleveism_pk == elevePk)
        eleve = query.one()
        eleve.eleveism_nom = unicode(eleveNom, 'utf-8')
        eleve.eleveism_prenom = unicode(elevePrenom, 'utf-8')
        eleve.eleveism_email = unicode(eleveEmail, 'utf-8')
        eleve.eleveism_login = unicode(eleveLogin, 'utf-8')
        eleve.eleveism_pass = unicode(elevePass, 'utf-8')
        eleve.eleveism_classe_fk = eleveClasseFk

        session.flush()

        userEleve = ('%s %s') % (elevePrenom, eleveNom)
        userRole = 'EleveISM'
        self.addLoginEleve(eleveLogin, elevePass, userRole)
        self.addInfoEleve(eleveLogin, eleveEmail, userEleve)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"L'élève a bien été modifié !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/ajouter-un-eleve-ism?elevePk=%s" % (portalUrl, elevePk)
        self.request.response.redirect(url)
        return ''

    def deleteEleve(self):
        """
        Supprimer un élève
        """
        fields = self.context.REQUEST

        elevePk = getattr(fields, 'elevePk', None)
        eleveLogin = getattr(fields, 'eleveLogin', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(EleveIsm)
        query = query.filter(EleveIsm.eleveism_pk == elevePk)
        eleve = query.one()
        session.delete(eleve)
        session.flush()

        self.delLoginEleve(eleveLogin)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"L'élève' a bien été supprimé !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/ajouter-un-eleve-ism?elevefPk=%s" % (portalUrl, elevePk)
        self.request.response.redirect(url)
        return ''
