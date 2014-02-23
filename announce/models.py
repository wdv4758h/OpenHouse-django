# _*_ coding: utf8 _*_

from django.db import models

class Announce(models.Model):
    #id
    title       = models.CharField('標題', max_length=100)
    content     = models.TextField('內容')
    author_id   = models.CharField('發佈者 ID', max_length=10)
    create_time = models.DateTimeField('發佈時間', auto_now_add=True)
    update_time = models.DateTimeField('更新時間', auto_now=True)

    class Meta:
        db_table = 'announce'
        ordering = ['-id', '-update_time']
