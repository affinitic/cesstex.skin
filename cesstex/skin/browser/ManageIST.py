# -*- coding: utf-8 -*-

from Acquisition import aq_inner
from Products.Five import BrowserView
from zope.interface import implements
from mailer import Mailer
from cesstex.skin.browser.interfaces import IManageIST
from Products.CMFCore.utils import getToolByName
from plone.memoize.instance import memoize

LIMIT = 10


class ManageIST(BrowserView):
    implements(IManageIST)

    @memoize
    def getEventsIst(self):
        catalog = getToolByName(aq_inner(self.context), 'portal_catalog') 
        events = catalog(portal_type='Event',
                         review_state=('external', 'internal', 'publish'), 
                         path={'query': 'plone/institut-sainte-therese', 'depth': 1},
                         sort_on='Date',
                         sort_order='reverse',
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

    def sendMailDemande(self, direction, sujet, message):
        """
        envoi de mail à la direction
        """
        #yohannamazzeo@hotmail.com
        #direction="alain.meurant@affinitic.be, yohannamazzeo@hotmail.com"
        mailer = Mailer("localhost", direction)
        #mailer = Mailer("relay.skynet.be", direction)
        mailer.setSubject(sujet)
        #mailer.setRecipients("alain.meurant@affinitic.be, yohannamazzeo@hotmail.com")
        mailer.setRecipients(direction)
        mail = message
        mailer.sendAllMail(mail)

    def traiterDemandeIst(self):
        """
        gère la demande et envoie mail selon implantation
        """
        fields = self.context.REQUEST
        civilite=fields.get('civilite')
        prenom=fields.get('prenom')
        nom=fields.get('nom')
        rue=fields.get('rue')
        numero=fields.get('numero')
        cp=fields.get('cp')
        localite=fields.get('localite')
        telephone=fields.get('telephone')
        email=fields.get('email')
        option=fields.get('option')
        implantation=fields.get('implantation')
        demande=fields.get('demande')
        direction=''

        #pour MANAGE : Marie-Christine DELMOITIEZ, coordination@istmanage.be   IST MANAGE
        #pour LA LOUVIERE :  christina.papadopoulos@gmail.com  IST LA LOUVIERE
        #pour le CEFA : Dominique BERTRAND, dominiquewillaerts@hotmail.com  CEFA MANAGE

        if implantation=="IST MANAGE":
            direction="coordination@istmanage.be"
        elif implantation=="IST LA LOUVIERE":
            direction="christina.papadopoulos@gmail.com"
        elif implantation=="CEFA MANAGE":
            direction="dominiquewillaerts@hotmail.com"

        sujet="testmail %s"%(implantation)

        message="""DEMANDE D'INFORMATION VIA LE SITE<br>
        <hr>
        %s %s %s<br>
        %s, %s<br>
        %s, %s<br>
        %s<br>
        %s<br>
        <hr>
        Option : %s<br>
        Implantation : %s<br>
        <hr>
        Demande :<br>
        %s
        <hr>
        pour : %s
        """%(civilite,prenom,nom,rue,numero,cp,localite,telephone,email,option,implantation,demande,direction)

        self.sendMailDemande(direction, sujet, message)
