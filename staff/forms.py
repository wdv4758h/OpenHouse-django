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

    GENDER = (('M', '男生'), ('F', '女生'))

    # Fields
    studentid = forms.CharField(required=True, label=(u'學號'))
    name      = forms.CharField(required=True, label=(u'姓名'))
    gender    = forms.ChoiceField(choices=GENDER, label=(u'性別'))
    birthday  = forms.DateField(label=(u'出生年月日'))
    mobile    = forms.CharField(label=(u'手機號碼'), max_length=16)
    email     = forms.EmailField()
    fb_url    = forms.URLField(initial='https://www.facebook.com/', label=(u'FB個人首頁連結'))
    bs2id     = forms.CharField(label=(u'BS2帳號'), max_length=12)
    ohbbsid   = forms.CharField(label=(u'OH BBS帳號'), max_length=12)
    postacct  = forms.CharField(label=(u'郵局帳號'), max_length=15)

    password1 = forms.CharField(label=(u'密碼'), widget=forms.PasswordInput)
    password2 = forms.CharField(label=(u'密碼確認'),
        widget=forms.PasswordInput, help_text=('請輸入和前面一樣的密碼'))

    class Meta:
        model = Staff
        fields = '__all__'
        exclude = ('last_login', 'password')
        widgets = {
            'role': forms.CheckboxSelectMultiple
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
        print(self.cleaned_data)
        user = super(StaffCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user

class StaffEditForm(forms.ModelForm):

    error_messages = {
        'duplicate_username': ('重複的使用者名稱'),
        'password_mismatch': ('兩次輸入的密碼不一樣'),
    }

    required_css_class = 'required'

    GENDER = (('M', '男生'), ('F', '女生'))

    # Fields
    studentid = forms.CharField(required=True, label=(u'學號'))
    name      = forms.CharField(required=True, label=(u'姓名'))
    gender    = forms.ChoiceField(choices=GENDER, label=(u'性別'))
    birthday  = forms.DateField(label=(u'出生年月日'))
    mobile    = forms.CharField(label=(u'手機號碼'), max_length=16)
    email     = forms.EmailField()
    fb_url    = forms.URLField(initial='https://www.facebook.com/', label=(u'FB個人首頁連結'))
    bs2id     = forms.CharField(label=(u'BS2帳號'), max_length=12)
    ohbbsid   = forms.CharField(label=(u'OH BBS帳號'), max_length=12)
    postacct  = forms.CharField(label=(u'郵局帳號'), max_length=15)

    password1 = forms.CharField(required=False, label=(u'密碼'), widget=forms.PasswordInput)
    password2 = forms.CharField(required=False, label=(u'密碼確認'),
        widget=forms.PasswordInput, help_text=('請輸入和前面一樣的密碼'))

    is_active = forms.BooleanField(required=False, label=(u'啟用'))

    class Meta:
        model = Staff
        fields = '__all__'
        exclude = ('last_login', 'password')
        widgets = {
            'role': forms.CheckboxSelectMultiple
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
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        return user
