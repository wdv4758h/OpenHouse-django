from rest_framework.generics import ListAPIView
from api.models import NewsSerializer
from ohcms.models import News, NewsIndex

class NewsList(ListAPIView):
    """
    API for News
    """

    serializer_class = NewsSerializer

    def get_queryset(self):
        # assume root page url is 'home'
        year = self.request.get_full_path().split('/')[2]
        #year = self.kwargs['year']
        parent = NewsIndex.objects.get(url_path='/home/{}/news/'.format(year))
        return News.objects.live().descendant_of(parent)
