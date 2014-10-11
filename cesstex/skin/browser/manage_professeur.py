# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from zope.interface import implements
#from mailer import Mailer
from Products.CMFCore.utils import getToolByName
from z3c.sqlalchemy import getSAWrapper
from cesstex.db.pgsql.baseTypes import Professeur, StatutMembre
from interfaces import IManageISM

LIMIT = 10

from cesstex.db.pgsql.baseTypes import Ecole, \
                                       Implantation, \
                                       Professeur, \
                                       StatutMembre



class ManageProfesseur(BrowserView):
    implements(IManageISM)

### GESTION DES PROFS ###
    def addLoginProfesseur(self, login, passw, role):
        """
        ajoute le login et le pass d'un professeur
        le role est ProfISM ou ProfIST
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

    def getEcoleDuProfesseur(self, ecolePK):
        """
        recuperation de l'école d'un prof
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Ecole)
        query = query.filter(Ecole.ecole_pk == ecolePK)
        ecoleDuProfesseur = query.one()
        return ecoleDuProfesseur

    def getAllProfesseurs(self, ecole):
        """
        recuperation de tous les professseurs selon ecole
        table ecole ism=1 ist=2 po=3
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Professeur)
        query = query.order_by(Professeur.prof_nom)
        query = query.filter(Professeur.prof_ecole_fk == ecole)
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
        fields = self.context.REQUEST

        profNom = getattr(fields, 'profNom')
        profPrenom = getattr(fields, 'profPrenom', None)
        profEmail = getattr(fields, 'profEmail', None)
        profEmailCesstex = getattr(fields, 'profEmailCesstex', None)
        profLogin = getattr(fields, 'profLogin', None)
        profPass = getattr(fields, 'profPass', None)
        profStatutFk = getattr(fields, 'profStatutFk', None)
        profEcoleFk = getattr(fields, 'profEcoleFk', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = Professeur(prof_nom=profNom,
                              prof_prenom=profPrenom,
                              prof_email=profEmail,
                              prof_email_id=profEmailCesstex,
                              prof_login=profLogin,
                              prof_pass=profPass,
                              prof_statut_fk=profStatutFk,
                              prof_ecole_fk=profEcoleFk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)

        userProf = ('%s %s') % (profPrenom, profNom)
        userRole = 'ProfISM'
        self.addLoginProfesseur(profLogin, profPass, userRole)
        self.addInfoProfesseur(profLogin, profEmail, userProf)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le nouveau membre a bien été ajouté !"
        ploneUtils.addPortalMessage(message, 'info')
        if profEcoleFk == '1':
            url = "%s/institut-sainte-marie/ajouter-un-professeur-ism" % (portalUrl)
        if profEcoleFk == '2':
            url = "%s/institut-sainte-therese/ajouter-un-professeur-ist" % (portalUrl)
        self.request.response.redirect(url)
        return ''

    def updateProfesseur(self):
        """
        Updates un événement acté lié à un dossier
        """

        fields = self.context.REQUEST

        profPk = getattr(fields, 'profPk')
        profNom = getattr(fields, 'profNom')
        profPrenom = getattr(fields, 'profPrenom', None)
        profEmail = getattr(fields, 'profEmail', None)
        profEmailCesstex = getattr(fields, 'profEmailCesstex', None)
        profLogin = getattr(fields, 'profLogin', None)
        profPass = getattr(fields, 'profPass', None)
        profStatusFk = getattr(fields, 'profStatusFk', None)
        profEcoleFk = getattr(fields, 'profEcoleFk', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(Professeur)
        query = query.filter(Professeur.prof_pk == profPk)
        professeur = query.one()
        professeur.prof_nom = unicode(profNom, 'utf-8')
        professeur.prof_prenom = unicode(profPrenom, 'utf-8')
        professeur.prof_email = unicode(profEmail, 'utf-8')
        professeur.prof_email_id = unicode(profEmailCesstex, 'utf-8')
        professeur.prof_login = unicode(profLogin, 'utf-8')
        professeur.prof_pass = unicode(profPass, 'utf-8')
        professeur.prof_status_fk = profStatusFk
        session.flush()

        userProf = ('%s %s') % (profPrenom, profNom)
        userRole = 'ProfISM'
        self.addLoginProfesseur(profLogin, profPass, userRole)
        self.addInfoProfesseur(profLogin, profEmail, userProf)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"Le professeur a bien été modifié !"
        ploneUtils.addPortalMessage(message, 'info')
        if profEcoleFk == '1':
            url = "%s/institut-sainte-marie/ajouter-un-professeur-ism?profPk=%s" % (portalUrl, profPk)
        if profEcoleFk == '2':
            url = "%s/institut-sainte-therese/ajouter-un-professeur-ist" % (portalUrl)
        self.request.response.redirect(url)
        return ''

    def deleteProfesseur(self):
        """
        Supprimer un événement acté lié à un dossier
        """
        fields = self.context.REQUEST

        profPk = getattr(fields, 'profPk', None)
        profLogin = getattr(fields, 'profLogin', None)
        profEcoleFk = getattr(fields, 'profEcoleFk', None)

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
        if profEcoleFk == '1':
            url = "%s/institut-sainte-marie/ajouter-un-professeur-ism?profPk=%s" % (portalUrl, profPk)
        if profEcoleFk == '2':
            url = "%s/institut-sainte-therese/ajouter-un-professeur-ist" % (portalUrl)
        self.request.response.redirect(url)
        return ''
