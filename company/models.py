# _*_ coding: utf8 _*_

from django.db import models
from django.forms import ModelForm
from django import forms

class Company(models.Model):

    CATEGORYS = (
        ('半導體', '半導體'),
        ('消費電子', '消費電子'),
        ('網路通訊', '網路通訊'),
        ('光電光學', '光電光學'),
        ('資訊軟體', '資訊軟體'),
        ('集團', '集團'),
        ('綜合', '綜合'),
        ('人力銀行', '人力銀行'),
        ('機構', '機構')
    )

    #id
    cid          = models.CharField('統編', max_length=8)
    name         = models.CharField('公司名稱', max_length=64)
    shortname    = models.CharField('公司簡稱', max_length=16)
    #password
    category     = models.CharField('類別', max_length=10, choices=CATEGORYS)  #need to be fixed
    phone        = models.CharField('公司電話', max_length=32)
    postal_code  = models.CharField('郵遞區號', max_length=5)
    address      = models.CharField('公司地址', max_length=128)
    website      = models.CharField('公司網站', max_length=64)
    logo_webpath = models.TextField('LOGO')
    brief        = models.CharField('公司簡介', max_length=110)
    introduction = models.CharField('公司介紹', max_length=260)
    hr_name      = models.CharField('人資姓名', max_length=32)
    hr_phone     = models.CharField('人資電話', max_length=32)
    hr_fax       = models.CharField('人資傳真', max_length=32)
    hr_mobile    = models.CharField('人資手機', max_length=32)
    hr_email     = models.CharField('人資信箱', max_length=64)
    timestamp    = models.DateField(editable=False)

class CompanyForm(ModelForm):
    class Meta:
        model = Company

    brief = forms.CharField(label='公司簡介', widget=forms.Textarea)
    introduction = forms.CharField(label='公司介紹', widget=forms.Textarea)
    hr_email     = forms.CharField(label='人資信箱', widget=forms.EmailInput, max_length=64)

    def __unicode__(self):
        return self.shortname

    def save(self, commit=True):
        company = Company()

        company.cid = self.cleaned_data['cid']
        company.name = self.cleaned_data['name']
        company.shortname = self.cleaned_data['shortname']
        #password
        #check password
        company.password = self.cleaned_data['password']

        company.category = self.cleaned_data['category']
        company.phone = self.cleaned_data['phone']
        company.postal_code = self.cleaned_data['postal_code']
        company.address = self.cleaned_data['address']
        company.website = self.cleaned_data['website']
        company.logo_webpath = self.cleaned_data['logo_webpath']
        company.brief = self.cleaned_data['brief']
        company.introduction = self.cleaned_data['introduction']
        company.hr_name = self.cleaned_data['hr_name']
        company.hr_phone = self.cleaned_data['hr_phone']
        company.hr_fax = self.cleaned_data['hr_fax']
        company.hr_email = self.cleaned_data['hr_email']
        company.hr_mobile = self.cleaned_data['hr_mobile']
        company.timestamp = str(datetime.datetime.now()).split('.')[0]

        if commit:
            company.save()
        return company
