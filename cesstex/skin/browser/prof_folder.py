# -*- coding: utf-8 -*-

from zope.interface import alsoProvides
from plone import api
from Products.Five import BrowserView
from Products.CMFCore.interfaces import IFolderish
from Products.CMFPlacefulWorkflow.PlacefulWorkflowTool import WorkflowPolicyConfig_id

from cesstex.skin.browser.interfaces import IProfFolder


class ProfFolderView(BrowserView):

    def can_configure(self):
        """
        """
        context = self.context
        if not IFolderish.providedBy(context):
            return False
        alreadyActivated = self.isFolderProfActivated()
        return (not alreadyActivated)

    def isFolderProfActivated(self):
        """
        """
        context = self.context
        return(IProfFolder.providedBy(context))

    def configure(self):
        """
        """
        context = self.context
        self.configure_prof_folder(context)
        api.portal.show_message(message=u"Configuration terminée du dossier privé pour profs. N'oubliez pas de configurer les partages.",
                                request=self.request,
                                type='info')
        self.request.response.redirect(context.absolute_url())
        return ''

    def configure_prof_folder(self, context):
        """
        """
        policy = getattr(context, WorkflowPolicyConfig_id, None)
        if policy is None:
            context.manage_addProduct['CMFPlacefulWorkflow'].manage_addWorkflowPolicyConfig()
            policy = getattr(context, WorkflowPolicyConfig_id)
            policy.setPolicyBelow('prof_folder')
            policy.setPolicyIn('prof_folder')
        context.reindexObjectSecurity()
        alsoProvides(context, IProfFolder)
