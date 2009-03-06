# aller declarer le setuphandlers dans le ƣmport_steps.xml


# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.component import getMultiAdapter
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import IPortletManager
from plone.portlets.interfaces import IPortletAssignmentMapping
from plone.portlets.interfaces import ILocalPortletAssignmentManager
from plone.app.portlets.portlets import classic
from plone.app.portlets.portlets import navigation
from Products.CMFCore.utils import getToolByName
from Products.Five.component import enableSite
from zope.app.component.interfaces import ISite

import logging
logger = logging.getLogger('Cesstex.skin')

LANGUAGES = ['fr']

def setupcesstex(context):
    logger.debug('Setup cesstex skin')
    portal = context.getSite()
    if not ISite.providedBy(portal):
        enableSite(portal)
    setupHomePortlets(portal)
    createContent(portal)

def publishObject(obj):
    portal_workflow = getToolByName(obj, 'portal_workflow')
    if portal_workflow.getInfoFor(obj, 'review_state') in ['visible','private']:
        portal_workflow.doActionFor(obj, 'publish')
    return

def getManager(folder, column):
    if column == 'left':
        manager = getUtility(IPortletManager, name=u'plone.leftcolumn', context=folder)
    else:
        manager = getUtility(IPortletManager, name=u'plone.rightcolumn', context=folder)
    return manager

def addViewToType(portal, typename, templatename):
    pt = getToolByName(portal, 'portal_types')
    foldertype = getattr(pt, typename)
    available_views = list(foldertype.getAvailableViewMethods(portal))
    if not templatename in available_views:
        available_views.append(templatename)
        foldertype.manage_changeProperties(view_methods=available_views)

def changeFolderView(portal, folder, viewname):
    addViewToType(portal, 'Folder', viewname)
    if folder.getLayout() != viewname:
        folder.setLayout(viewname)

def clearColumnPortlets(folder, column):
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager,), IPortletAssignmentMapping)
    for portlet in assignments:
        del assignments[portlet]

def clearPortlets(folder):
    clearColumnPortlets(folder, 'left')
    clearColumnPortlets(folder, 'right')

def blockParentPortlets(folder):
    manager = getManager(folder, 'left')
    assignable = getMultiAdapter((folder, manager,), ILocalPortletAssignmentManager)
    assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)

    manager = getManager(folder, 'right')
    assignable = getMultiAdapter((folder, manager,), ILocalPortletAssignmentManager)
    assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)

def setupSubNavigationPortlet(folder):
    manager = getManager(folder, 'left')
    assignments = getMultiAdapter((folder, manager,), IPortletAssignmentMapping)

    assignment = navigation.Assignment(name=u"Navigation",
                                       root=None,
                                       currentFolderOnly=False,
                                       includeTop=False,
                                       topLevel=1,
                                       bottomLevel=0)
    assignments['navtree'] = assignment
    setupClassicPortlet(folder, 'portlet_sub_menus', 'left')

def setupSimpleNavigationPortlet(folder, column):
    #Add simple navigation portlet to folder
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager,), IPortletAssignmentMapping)
    assignment = navigation.Assignment()
    assignments['navigation'] = assignment

def setupClassicPortlet(folder, template, column):
    #Add classic portlet (using template) to folder
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager,), IPortletAssignmentMapping)

    assignment = classic.Assignment(template=template, macro='portlet')
    if assignments.has_key(template):
        del assignments[template]
    assignments[template] = assignment

def movePortlet(folder, name, column, position):
    #Change position order of portlet
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager,), IPortletAssignmentMapping)

    keys = list(assignments.keys())
    idx = keys.index(name)
    keys.remove(name)
    keys.insert(position, name)
    assignments.updateOrder(keys)

def createPage(parentFolder, documentId, documentTitle):
    if documentId not in parentFolder.objectIds():
        parentFolder.invokeFactory('Document', documentId, title=documentTitle)
    document = getattr(parentFolder, documentId)
    #By default, created page are written in English
    #XXX bug here : document.setLanguage('en')
    publishObject(document)
    return document

def createFolder(parentFolder, folderId, folderTitle):
    if folderId not in parentFolder.objectIds():
        parentFolder.invokeFactory('Folder', folderId, title=folderTitle)
    createdFolder = getattr(parentFolder, folderId)
    createdFolder.reindexObject()
    publishObject(createdFolder)
    createdFolder.reindexObject()
    return createdFolder

def setupHomePortlets(folder):
    #Creates portlets columns for root pages
    clearPortlets(folder)
    blockParentPortlets(folder)

def createContent(portal):
    #Create empty documents and folders
    cesstexFolder = createFolder(portal, "centre-scolaire-saint-exupery", "Centre scolaire Saint-Exupéry")
    createPage(cesstexFolder, "centre-scolaire-saint-exupery", "Centre scolaire Saint-Exupéry ?")

    lalouviereFolder = createFolder(portal, "site-de-la-louviere", "Site de La Louvière")
    createPage(cesstexFolder, "site-de-la-louviere", "Site de La Louvière")

    manageFolder = createFolder(portal, "site-de-manage", "Site de Manage")
    createPage(cesstexFolder, "site-de-manage", "Site de Manage")

    maternelleFolder = createFolder(portal, "maternelle", "Maternelle")
    createPage(cesstexFolder, "maternelle", "Maternelle")

    primaireFolder = createFolder(portal, "primaire", "Primaire")
    createPage(cesstexFolder, "primaire", "Primaire")

    secondaireFolder = createFolder(portal, "secondaire", "Secondaire")
    createPage(cesstexFolder, "secondaire", "Secondaire")

    ecoleFondamentaleStMarieFolder = createFolder(portal, "ecole-fondamentale-sainte-marie", "Ecole fondamentale Sainte-Marie")
    createPage(cesstexFolder, "ecole-fondamentale-sainte-marie", "Ecole fondamentale Sainte-Marie")

    sectionFondamentaleStAntoineFolder = createFolder(portal, "section-fondamentale-saint-antoine", "Section fondamentale Saint-Antoine")
    createPage(cesstexFolder, "section-fondamentale-saint-antoine", "Section fondamentale Saint-Antoine")

    ecolePrimaireStMarieFolder = createFolder(portal, "ecole-primaire-sainte-marie", "Ecole primaire Sainte-Marie")
    createPage(cesstexFolder, "ecole-primaire-sainte-marie", "Ecole primaire Sainte Marie")

    institutStMarieFolder = createFolder(portal, "institut-sainte-marie", "Institut Sainte Marie")
    createPage(cesstexFolder, "institut-sainte-marie", "Institut Sainte-Marie")

    institutStThereseFolder = createFolder(portal, "institut-sainte-therese", "Institut Sainte-Thérèse")
    createPage(cesstexFolder, "institut-sainte-therese", "Institut Sainte-Thérèse")




























