# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from zope.interface import implements
from mailer import Mailer
from cesstex.skin.browser.interfaces import IManageIST


class ManageIST(BrowserView):
    implements(IManageIST)

    def sendMailDemande(self, direction, sujet, message):
        """
        envoi de mail à la direction
        """
        #yohannamazzeo@hotmail.com
        direction="alain.meurant@affinitic.be, yohannamazzeo@hotmail.com"
        #mailer = Mailer("localhost", direction)
        mailer = Mailer("relay.skynet.be", direction)
        mailer.setSubject(sujet)
        mailer.setRecipients("alain.meurant@affinitic.be, yohannamazzeo@hotmail.com")
        #mailer.setRecipients("alain.meurant@skynet.be")
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

        #pour MANAGE : direction.ist@istmanage.be   IST MANAGE
        #pour LA LOUVIERE :  christina.papadopoulos@gmail.com  IST LA LOUVIERE
        #pour le CEFA : ist.cefa@skynet.be  CEFA MANAGE

        if implantation=="IST MANAGE":
            direction="direction.ist@istmanage.be"
        elif implantation=="IST LA LOUVIERE":
            direction="christina.papadopoulos@gmail.com"
        elif implantation=="CEFA MANAGE":
            direction="ist.cefa@skynet.be"

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
