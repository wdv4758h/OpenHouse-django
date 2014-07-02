# -*- coding: utf-8 -*-

from django import forms
from staff.models import Staff

User = Staff

class StaffCreationForm(forms.ModelForm):

    error_messages = {
        'duplicate_username': ('重複的使用者名稱'),
        'password_mismatch': ('兩次輸入的密碼不一樣'),
    }

    required_css_class = 'required'

    password1 = forms.CharField(label=(u'密碼'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=(u'密碼確認'),
        widget=forms.PasswordInput, help_text=('請輸入和前面一樣的密碼'))

    class Meta:
        model = Staff
        fields = '__all__'
        exclude = ('last_login', 'password')
        widgets = {
            'groups': forms.CheckboxSelectMultiple
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(StaffCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            self.save_m2m() # save many to many field
        return user

class StaffEditForm(forms.ModelForm):

    error_messages = {
        'duplicate_username': ('重複的使用者名稱'),
        'password_mismatch': ('兩次輸入的密碼不一樣'),
    }

    required_css_class = 'required'

    password1 = forms.CharField(required=False, label=(u'密碼'), widget=forms.PasswordInput)
    password2 = forms.CharField(required=False, label=(u'密碼確認'),
        widget=forms.PasswordInput, help_text=('請輸入和前面一樣的密碼'))

    class Meta:
        model = Staff
        fields = '__all__'
        exclude = ('last_login', 'password')
        widgets = {
            'groups': forms.CheckboxSelectMultiple
        }

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def save(self, commit=True):
        user = super(StaffEditForm, self).save(commit=False)
        if self.cleaned_data["password1"]:
            user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            self.save_m2m() # save many to many field
        return user
