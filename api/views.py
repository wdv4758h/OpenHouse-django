from django.shortcuts import render
from rest_framework import viewsets
#from api.models import SalarySerializer
#from staff.models import Salary
from api.models import AnnounceSerializer
from announce.models import Announce

#class SalaryViewSet(viewsets.ModelViewSet):
#    """
#    API endpoint that allows users to be viewed or edited.
#    """
#    queryset = Salary.objects.all()
#    serializer_class = SalarySerializer

class AnnounceViewSet(viewsets.ReadOnlyModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Announce.objects.all()
    serializer_class = AnnounceSerializer
