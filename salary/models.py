# -*- coding: utf-8 -*-

from django.db import models

class Salary(models.Model):

    staff  = models.ForeignKey('staff.Staff', limit_choices_to={'is_active': True}, verbose_name='工作人員')
    desc   = models.TextField('工作內容')
    start  = models.DateTimeField('開始時間')
    end    = models.DateTimeField('結束時間')
    status = models.CharField('審核狀態', default='未審核', max_length=10)

    class Meta:
        verbose_name = '報帳'
        verbose_name_plural = '報帳'
        db_table = 'salary'
