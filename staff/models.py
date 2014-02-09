# _*_ coding: utf8 _*_

from django.db import models
from django.forms import ModelForm
from django import forms
import datetime

class Staff(models.Model):
    #id
    #studentid = models.PositiveIntegerField(default=0)
    studentid = models.CharField(max_length=100)
    #password
    name      = models.CharField(max_length=100)
    gender    = models.BooleanField()
    birthday  = models.DateField()
    role      = models.CharField(max_length=300)
    mobile    = models.PositiveIntegerField(default=0)
    email     = models.EmailField()
    fb_url    = models.URLField()
    bs2id     = models.CharField(max_length=12)
    ohbbsid   = models.CharField(max_length=12)
    postacct  = models.CharField(max_length=15)
    verify    = models.BooleanField()
    timestamp = models.DateField()

class Resume(models.Model):
    #id
    uid          = models.CharField(max_length=7)
    name         = models.CharField(max_length=100)
    gender       = models.BooleanField()
    birthday     = models.DateField()
    department   = models.CharField(max_length=16)     #extra
    mobile       = models.PositiveIntegerField(default=0)
    email        = models.EmailField()
    msn          = models.CharField(max_length=64)     #extra
    bs2id        = models.CharField(max_length=12)
    facebook     = models.CharField(max_length=64)     #extra
    highschool   = models.CharField(max_length=32)     #extra
    credits      = models.IntegerField()               #extra
    interests    = models.CharField(max_length=100)    #extra
    skills       = models.CharField(max_length=100)    #extra
    experience   = models.CharField(max_length=250)    #extra
    date         = models.IntegerField()               #extra
    group_forum  = models.BooleanField()               #extra
    group_show   = models.BooleanField()               #extra
    group_design = models.BooleanField()               #extra
    impression   = models.CharField(max_length=250)    #extra
    note         = models.CharField(max_length=250)    #extra
    timestamp    = models.DateField()

    def __unicode__(self):
        return self.name

class Salary(models.Model):

    #user order_by to insure the order
    tmp1 = Staff.objects.values('name').order_by('studentid')
    tmp2 = Staff.objects.values('studentid').order_by('studentid')

    STAFFS = []
    for i,j in zip(tmp1,tmp2):
        STAFFS.append((j['studentid'], j['studentid'] + ' - ' + i['name']))    #(value, display_text)

    #id
    staff_id    = models.CharField('工作人員', max_length=100, choices=STAFFS)
    description = models.CharField('工作內容', max_length=100, help_text='工作內容')
    start_time  = models.DateTimeField('開始時間', help_text='開始時間')
    end_time    = models.DateTimeField('結束時間', help_text='結束時間')
    verify      = models.CharField(max_length=100, editable=False)  #need to modify
    deny_reason = models.CharField(max_length=64, editable=False)
    timestamp   = models.DateTimeField(editable=False)

    def __unicode__(self):
        return self.staff_id

class SalaryForm(ModelForm):
    class Meta:
        model = Salary

    description = forms.CharField(label='工作內容', widget=forms.Textarea, help_text='工作內容')

    # On Python 3: def __str__(self):
    def __unicode__(self):
        return self.username

    def save(self, commit=True):
        salary = Salary()

        #looking for better solution
        salary.staff_id = self.cleaned_data['staff_id']
        salary.description = self.cleaned_data['description']
        salary.start_time = self.cleaned_data['start_time']
        salary.end_time = self.cleaned_data['end_time']
        salary.verify = '待審核'
        salary.deny_reason = ''
        salary.timestamp = str(datetime.datetime.now()).split('.')[0]

        if commit:
            salary.save()
        return salary
