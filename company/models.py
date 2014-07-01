# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager

class Company(AbstractBaseUser):
    """
    A class for OpenHouse company

    Look the Default Django User Model for more information :
    https://github.com/django/django/blob/master/django/contrib/auth/models.py
    """

    CATEGORYS = (
        (u'半導體', u'半導體'),
        (u'消費電子', u'消費電子'),
        (u'網路通訊', u'網路通訊'),
        (u'光電光學', u'光電光學'),
        (u'資訊軟體', u'資訊軟體'),
        (u'集團', u'集團'),
        (u'綜合', u'綜合'),
        (u'人力銀行', u'人力銀行'),
        (u'機構', u'機構')
    )

    cid          = models.CharField('統編', max_length=8)
    name         = models.CharField('公司名稱', max_length=64)
    shortname    = models.CharField('公司簡稱', max_length=16)
    category     = models.CharField('類別', max_length=10, choices=CATEGORYS)
    phone        = models.CharField('公司電話', max_length=32)
    postal_code  = models.CharField('郵遞區號', max_length=5)
    address      = models.CharField('公司地址', max_length=128)
    website      = models.URLField('公司網站', max_length=64, help_text='請輸入網址')
    logo         = models.ImageField('LOGO', upload_to='{}/company/'.format(settings.MEDIA_ROOT))
    brief        = models.TextField('公司簡介', max_length=110)
    introduction = models.TextField('公司介紹', max_length=260)
    hr_name      = models.CharField('人資姓名', max_length=32)
    hr_phone     = models.CharField('人資電話', max_length=32)
    hr_fax       = models.CharField('人資傳真', max_length=32)
    hr_mobile    = models.CharField('人資手機', max_length=32)
    hr_email     = models.EmailField('人資信箱', max_length=64)

    is_active    = models.BooleanField('是否啟用', default=False)
    update       = models.DateTimeField('最後更新時間', auto_now=True)
    date_join    = models.DateTimeField('date joined', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'cid'
    #REQUIRED_FIELDS = []

    class Meta:
        verbose_name = '廠商'
        verbose_name_plural = '廠商'

    def __unicode__(self):
        return self.get_full_name()

    def __str__(self):
        return self.get_full_name()

    def username(self):
        """
        for someone finding the username field
        """
        return self.shortname

    def get_full_name(self):
        return self.cid + ' - ' + self.shortname

    def get_short_name(self):
        return self.cid

    @property
    def is_staff(self):
        return False

    @property
    def is_superuser(self):
        return False

    def has_perm(self, perm, obj=None):
        return False
