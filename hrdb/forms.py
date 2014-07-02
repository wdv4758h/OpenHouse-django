from django import forms
from hrdb.models import Hrdb

class HrdbForm(forms.ModelForm):
    class Meta:
        model = Hrdb
        fields = '__all__'
        exclude = ('ip',)

    def save(self, ip=None, commit=True):
        user = super(HrdbForm, self).save(commit=False)
        if not user.ip: # pass for the first time
            user.ip = ip
        if commit:
            user.save()
        return user
