# -*- coding: utf-8 -*-

from Products.Five import BrowserView
from zope.interface import implements
from mailer import Mailer
from cesstex.skin.browser.interfaces import IManageIST


class ManageIST(BrowserView):
    implements(IManageIST)

    def sendMailDemande(self):
        """
        envoi de mail à la direction
        """
        sujet="testmail"
        message="envoi mail"
        #mailer = Mailer("localhost", "alain.meurant@skynet.be)
        mailer = Mailer("relay.skynet.be", "alain.meurant@affinitic.be")
        mailer.setSubject(sujet)
        mailer.setRecipients("alain.meurant@affinitic.be")
        #mailer.setRecipients("alain.meurant@skynet.be")
        mail = message
        mailer.sendAllMail(mail)

    def sendMailOperateur(self, sujetOperateur, messageOperateur, adresseOperateur):
        """
        envoi de mail à l'operateur dont les donnees change d'état
        """
        mailer = Mailer("localhost", adresseOperateur)
        #mailer = Mailer("relay.skynet.be", adresseOperateur)
        #mailer = Mailer("smtp.scarlet.be", adresse)
        mailer.setSubject(sujetOperateur)
        recipients="%s, %s"%('alain.meurant@affinitic.be', adresseOperateur)
        mailer.setRecipients(recipients)
        mail = messageOperateur
        mailer.sendAllMail(mail)
