# _*_ coding: utf8 _*_
from django.db import models

class Hrdb(models.Model):
    #id
    name                = models.CharField('姓名', max_length=32)
    department          = models.CharField('系級', max_length=32)
    grade               = models.CharField('年級', max_length=10)
    studentid           = models.CharField('學號', max_length=7)
    project             = models.CharField('大學專題題目', max_length=10)
    thesis              = models.TextField('研究所論文題目')
    teacher             = models.CharField('指導教授', max_length=30)
    intern              = models.TextField('實習經驗')
    nsc_project         = models.CharField('是否曾參與國科會計劃', max_length=1)
    language_ability    = models.TextField('曾通過哪些語言能力檢定及成績')
    email               = models.TextField('電子信箱')
    ip                  = models.TextField('填寫者IP')
    create_time         = models.DateTimeField('建立時間', auto_now_add=True)
    update_time         = models.DateTimeField('更新時間', auto_now=True)

    class Meta:
        db_table = 'hrdb'
        ordering = ['-id']
