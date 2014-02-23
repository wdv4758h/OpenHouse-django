from rest_framework import serializers
#from staff.models import Salary
from announce.models import Announce

#class SalarySerializer(serializers.HyperlinkedModelSerializer):
#    class Meta:
#        model = Salary
#        fields = ('staff_id', 'description', 'start_time', 'end_time')

class AnnounceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Announce
        fields = ('id', 'title', 'content', 'author_id', 'create_time', 'update_time')
