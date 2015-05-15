# -*- coding: utf-8 -*-

from zope.component import getUtility
from zope.component import getMultiAdapter
#from zope.interface import alsoProvides
from plone.portlets.constants import CONTEXT_CATEGORY
from plone.portlets.interfaces import IPortletManager, \
                                      IPortletAssignmentMapping, \
                                      ILocalPortletAssignmentManager
from plone.app.portlets.portlets import navigation
from Products.CMFCore.utils import getToolByName
import logging
from plone import api

logger = logging.getLogger('cestex.skin')


def setupcesstex(context):
    if context.readDataFile('cesstex.skin_various.txt') is None:
        return
    portal = context.getSite()
    clearPortlets(portal)
    deleteFolder(portal, 'Members')
    setupNavigationPortlet(portal)
    updateSecurity(portal)

    logger.info('Installing cesstex.skin')
    portal = context.getSite()

    existingIds = portal.objectIds()

    # Create 3 Documents for top boxes
    # setTitle needed because of https://github.com/plone/plone.api/issues/99
    if not 'ist-manage-news' in existingIds:
        page = api.content.create(container=portal, type='Document',
                                  id='ist-manage-news',
                                  title="Manage News")
        page.setTitle("Manage News")
        page.setExcludeFromNav(True)
        api.content.transition(obj=portal['ist-manage-news'],
                               transition='internal-publish')
    if not 'ist-la-louviere-news' in existingIds:
        page = api.content.create(container=portal, type='Document',
                                  id='ist-la-louviere-news',
                                  title="La Louviere News")
        page.setTitle("La Louvière News")
        page.setExcludeFromNav(True)
        api.content.transition(obj=portal['ist-la-louviere-news'],
                               transition='internal-publish')
    if not 'ist-cefa-manage-news' in existingIds:
        page = api.content.create(container=portal, type='Document',
                                  id='ist-cefa-manage-news',
                                  title="CEFA Manage News")
        page.setTitle("CEFA Manage News")
        page.setExcludeFromNav(True)
        api.content.transition(obj=portal['ist-cefa-manage-news'],
                               transition='internal-publish')

    portal.setLayout('istSalleDesProfs')


def setupNewFolder(portal, folder, idFolder, titleFolder, descriptionFolder, indexFolder):
    newFolder = createFolder(folder, idFolder, titleFolder, descriptionFolder)
    changeFolderView(portal, newFolder, indexFolder)
    return newFolder


def createFolder(parentFolder, folderId, folderTitle, folderDescription=''):
    if folderId not in parentFolder.objectIds():
        parentFolder.invokeFactory('Folder', folderId, title=folderTitle,
                                   description=folderDescription)
    createdFolder = getattr(parentFolder, folderId)
    publishObject(createdFolder)
    createdFolder.reindexObject()
    return createdFolder


def deleteFolder(portal, folderId):
    folder = getattr(portal, folderId, None)
    if folder is not None:
        portal.manage_delObjects(folderId)


def changeFolderView(portal, newFolder, viewname):
    addViewToType(portal, 'Folder', viewname)
    if newFolder.getLayout() != viewname:
        newFolder.setLayout(viewname)


def addViewToType(portal, typename, templatename):
    pt = getToolByName(portal, 'portal_types')
    foldertype = getattr(pt, typename)
    available_views = list(foldertype.getAvailableViewMethods(portal))
    if not templatename in available_views:
        available_views.append(templatename)
        foldertype.manage_changeProperties(view_methods=available_views)


def publishObject(obj):
    portal_workflow = getToolByName(obj, 'portal_workflow')
    if portal_workflow.getInfoFor(obj, 'review_state') in ['visible', 'private']:
        portal_workflow.doActionFor(obj, 'publish')
    return


def clearPortlets(folder):
    clearColumnPortlets(folder, 'left')
    clearColumnPortlets(folder, 'right')


def clearColumnPortlets(folder, column):
    manager = getManager(folder, column)
    assignments = getMultiAdapter((folder, manager), IPortletAssignmentMapping)
    for portlet in assignments:
        del assignments[portlet]
    assignable = getMultiAdapter((folder, manager), ILocalPortletAssignmentManager)
    assignable.setBlacklistStatus(CONTEXT_CATEGORY, True)


def setupNavigationPortlet(folder):
    manager = getManager(folder, 'left')
    assignments = getMultiAdapter((folder, manager, ), IPortletAssignmentMapping)

    assignment = navigation.Assignment(name=u"Navigation",
                                       root=None,
                                       currentFolderOnly=False,
                                       includeTop=False,
                                       topLevel=0,
                                       bottomLevel=0)
    assignments['navtree'] = assignment


def getManager(folder, column):
    if column == 'left':
        manager = getUtility(IPortletManager, name=u'plone.leftcolumn', context=folder)
    else:
        manager = getUtility(IPortletManager, name=u'plone.rightcolumn', context=folder)
    return manager


def updateSecurity(portal):
    wfTool = getToolByName(portal, 'portal_workflow')
    wfTool.updateRoleMappings()
