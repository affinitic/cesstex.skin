# -*- coding: UTF-8 -*-

from zope.component import adapts
from zope.interface import implements
from archetypes.schemaextender.interfaces import ISchemaExtender
from archetypes.schemaextender.field import ExtensionField
from Products.ATContentTypes.content.event import ATEvent
from Products.Archetypes.public import TextField, StringField, TextAreaWidget, StringWidget


class ProfResponsableField(ExtensionField, StringField):
    """
    """
    StringField(
        name='profResponsable',
        required=False,
        searchable=True,
        widget=StringWidget(
            description='',
            label=u'Professeur responsable',
            size=40))


class ProfsAccompagnateursField(ExtensionField, TextField):
    """
    """
    TextField(
        name='profsAccompagnateurs',
        required=False,
        searchable=True,
        widget=TextAreaWidget(description='',
                              label=u'Professeurs accompagnateurs',
                              cols=40))


class ContentExtender(object):
    adapts(ATEvent)
    implements(ISchemaExtender)

    fields = [
        ProfResponsableField(
            name='profResponsable',
            required=False,
            searchable=True,
            widget=StringWidget(description='',
                                label=u'Professeur responsable',
                                size=40)),
        ProfsAccompagnateursField(
            name='profsAccompagnateurs',
            required=False,
            searchabl=True,
            widget=TextAreaWidget(description='',
                                  label=u'Professeurs accompagnateurs',
                                  cols=40))]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
