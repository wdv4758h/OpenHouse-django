from django.shortcuts import render
from rest_framework import viewsets
from api.models import SalarySerializer
from staff.models import Salary

class SalaryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Salary.objects.all()
    serializer_class = SalarySerializer
