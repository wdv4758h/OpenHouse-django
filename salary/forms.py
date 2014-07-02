# -*- coding: utf-8 -*-

from django import forms
from salary.models import Salary

class SalaryForm(forms.ModelForm):

    class Meta:
        model = Salary
        fields = '__all__'
        exclude = ('status',)
