# _*_ coding: utf8 _*_
from django.db import models

class Hrdb(models.Model):
    name                = models.CharField('姓名', max_length=32)
    department          = models.CharField('系所', max_length=32)
    grade               = models.CharField('年級', max_length=10)
    studentid           = models.CharField('學號', max_length=10)
    project             = models.TextField('大學專題題目', max_length=100, blank=True)
    thesis              = models.TextField('研究所論文題目', max_length=100, blank=True)
    teacher             = models.CharField('指導教授', blank=True, max_length=30)
    intern              = models.TextField('實習經驗', blank=True, max_length=200)
    nsc_project         = models.BooleanField('是否曾參與國科會計劃', max_length=1)
    language_ability    = models.TextField('曾通過哪些語言能力檢定及成績', blank=True, max_length=200)
    email               = models.EmailField('電子信箱')
    ip                  = models.GenericIPAddressField('填寫者IP')
    create_time         = models.DateTimeField('建立時間', auto_now_add=True)
    update_time         = models.DateTimeField('更新時間', auto_now=True)

    class Meta:
        verbose_name = '人才庫'
        verbose_name_plural = '人才庫'
        db_table = 'hrdb'
        ordering = ['-id']

    def __unicode__(self):
        return self.name

    def __str__(self):
        return self.name
