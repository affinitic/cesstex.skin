from Products.Five import BrowserView


class GalleryView(BrowserView):

    def countElements(self):
        """
        Count elements in folder or topic for atct_album_view
        """
        context = self.context.getObject()
        is_topic = context.portal_type == 'Topic'
        results = []
        if is_topic:
            results = context.queryCatalog()
        else:
            results = context.getFolderContents()
        return len(results)
