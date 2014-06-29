from rest_framework import serializers
from ohcms.models import News

class NewsSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = News
        fields = ('id', 'title', 'body', 'create_time', 'update_time')
