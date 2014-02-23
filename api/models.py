from rest_framework import serializers
from staff.models import Salary

class SalarySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Salary
        fields = ('staff_id', 'description', 'start_time', 'end_time')
