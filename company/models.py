# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.validators import MinLengthValidator

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

    cid          = models.CharField(u'統編', unique=True, max_length=8, validators=[MinLengthValidator(8)])
    name         = models.CharField(u'公司名稱', max_length=64)
    shortname    = models.CharField(u'公司簡稱', max_length=16)
    category     = models.CharField(u'類別', max_length=10, choices=CATEGORYS)
    phone        = models.CharField(u'公司電話', max_length=32, help_text='格式: 區碼-號碼#分機')
    postal_code  = models.CharField(u'郵遞區號', max_length=5)
    address      = models.CharField(u'公司地址', max_length=128)
    website      = models.URLField(u'公司網站', max_length=64, help_text='請輸入網址')
    logo         = models.ImageField(u'LOGO', upload_to='{}/company/'.format(settings.MEDIA_ROOT),
                    help_text='''網站展示、筆記本內頁公司介紹使用，僅接受 jpg, png, gif 格式。
                    建議解析度為 300 dpi 以上，以達到最佳效果。''')
    brief        = models.TextField(u'公司簡介', max_length=110, help_text='字數限制為110字')
    introduction = models.TextField(u'公司介紹', max_length=260, help_text='字數限制為260字')
    hr_name      = models.CharField(u'人資姓名', max_length=32)
    hr_phone     = models.CharField(u'人資電話', max_length=32, help_text='格式: 區碼-號碼#分機')
    hr_fax       = models.CharField(u'人資傳真', max_length=32, help_text='格式: 區碼-號碼#分機')
    hr_mobile    = models.CharField(u'人資手機', max_length=32, help_text='格式: 0912-345678')
    hr_email     = models.EmailField(u'人資信箱', max_length=64)

    is_active    = models.BooleanField(u'是否啟用', default=False)
    last_update  = models.DateTimeField(u'最後更新時間', auto_now=True)
    date_join    = models.DateTimeField(u'date joined', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'cid'
    #REQUIRED_FIELDS = []

    class Meta:
        verbose_name = u'廠商'
        verbose_name_plural = u'廠商'
        db_table = 'company'

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
        return u'{} - {}'.format(self.cid, self.shortname)

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
