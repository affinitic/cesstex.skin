# -*- coding: UTF-8 -*-

from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField
from Products.ATContentTypes.content.newsitem import ATNewsItem
from Products.Archetypes.public import BooleanField, BooleanWidget


class ALaUneField(ExtensionField, BooleanField):
    """
    """


class ValveProfField(ExtensionField, BooleanField):
    """
    """


class NewsExtender(object):
    adapts(ATNewsItem)
    implements(ISchemaExtender)

    fields = [
        ALaUneField(
            name='isALaUneNews',
            required=False,
            languageIndependent=True,
            default=False,
            widget=BooleanWidget(description=u"""Cochez cette case si l'actualite doit
                                                 apparaitre dans la rubrique 'A la une sur
                                                 la page' d'accueil.""",
                                 label=u"Actualité 'A la Une'")),

        ValveProfField(
            name='isValveProfNews',
            required=False,
            languageIndependent=True,
            default=False,
            widget=BooleanWidget(description=u"""Cochez cette case s'il s'agit
                                                 d'une actualite pour la valve prof.""",
                                 label=u"Actualite 'Valve Prof'"))]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
