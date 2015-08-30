# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from zope.interface import implements
# from mailer import Mailer
from Products.CMFCore.utils import getToolByName
from z3c.sqlalchemy import getSAWrapper
from cesstex.db.pgsql.baseTypes import ClasseIsm
from interfaces import IManageISM


class ManageClasse(BrowserView):
    implements(IManageISM)

### GESTION DES CLASSESS ###
    def getAllClasses(self):
        """
        recuperation de toutes les classes
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(ClasseIsm)
        query = query.order_by(ClasseIsm.classeism_nom)
        allClasses = query.all()
        return allClasses

    def getClasseByPk(self, classePk):
        """
        recuperation d'un classe selon sa pk
        """
        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(ClasseIsm)
        query = query.filter(ClasseIsm.classeism_pk == classePk)
        classe = query.one()
        return classe

    def insertClasse(self):
        """
        insère un nouvel classe
        """
        fields = self.context.REQUEST

        classeNom = getattr(fields, 'classeNom')
        classeTitulaire01Pk = fields.get('classeTitulaire01Pk', None)
        classeTitulaire02Pk = fields.get('classeTitulaire02Pk', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        newEntry = ClasseIsm(classeism_nom=classeNom,
                             classeism_titulaire_01_fk=classeTitulaire01Pk,
                             classeism_titulaire_02_fk=classeTitulaire02Pk)
        session.add(newEntry)
        session.flush()
        session.refresh(newEntry)

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"La nouvelle classe a bien été ajoutée !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/ajouter-une-classe-ism" % (portalUrl)
        self.request.response.redirect(url)
        return ''

    def updateClasse(self):
        """
        Updates un événement acté lié à un dossier
        """

        fields = self.context.REQUEST

        classePk = getattr(fields, 'classePk')
        classeNom = getattr(fields, 'classeNom')
        classeTitulaire01Pk = fields.get('classeTitulaire01Pk', None)
        classeTitulaire02Pk = fields.get('classeTitulaire02Pk', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(ClasseIsm)
        query = query.filter(ClasseIsm.classeism_pk == classePk)
        classe = query.one()
        classe.classeism_nom = unicode(classeNom, 'utf-8')
        classe.classeism_titulaire_01_fk = classeTitulaire01Pk
        classe.classeism_titulaire_02_fk = classeTitulaire02Pk
        session.flush()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"La classe a bien été modifiée !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/ajouter-une-classe-ism?classePk=%s" % (portalUrl, classePk)
        self.request.response.redirect(url)
        return ''

    def deleteClasse(self):
        """
        Supprimer un élève
        """
        fields = self.context.REQUEST

        classePk = getattr(fields, 'classePk', None)

        wrapper = getSAWrapper('cesstex')
        session = wrapper.session
        query = session.query(ClasseIsm)
        query = query.filter(ClasseIsm.classeism_pk == classePk)
        classe = query.one()
        session.delete(classe)
        session.flush()

        portalUrl = getToolByName(self.context, 'portal_url')()
        ploneUtils = getToolByName(self.context, 'plone_utils')
        message = u"La classe a bien été supprimée !"
        ploneUtils.addPortalMessage(message, 'info')
        url = "%s/institut-sainte-marie/ajouter-une-classe-ism?classefPk=%s" % (portalUrl, classePk)
        self.request.response.redirect(url)
        return ''
