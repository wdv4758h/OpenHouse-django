from rest_framework.generics import ListAPIView
from api.models import NewsSerializer
from ohcms.models import News, NewsIndex

class NewsViewSet(ListAPIView):
    """
    API endpoint that allows users to be viewed or edited.
    """

    serializer_class = NewsSerializer

    def get_queryset(self):
        # assume root page url is 'home'
        parent = NewsIndex.objects.get(url_path='/home/{}/news/'.format(self.kwargs['year']))
        return News.objects.live().descendant_of(parent)
