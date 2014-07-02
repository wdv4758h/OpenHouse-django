from django import forms
from hrdb.models import Hrdb

class HrdbForm(forms.ModelForm):
    class Meta:
        model = Hrdb
        fields = '__all__'
        exclude = ('ip',)

    def save(self, commit=True):
        user = super(HrdbForm, self).save(commit=False)
        if commit:
            user.save()
        return user
