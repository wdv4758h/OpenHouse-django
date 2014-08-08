# -*- coding: utf-8 -*-

from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, UserManager
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from company.storage import OverwriteStorage

def validate_all_num(string):
    if not string.isdigit():
        raise ValidationError(u'必須都是數字')

def validate_phone(string):
    RegexValidator(r'^(\d+-)?\d+(#\d+)?$', message=u'格式: 區碼-號碼#分機')(string)

def validate_mobile(string):
    RegexValidator(r'^\d{4}-\d{6}$', message=u'格式: 0912-345678')(string)

def get_logo_path(instance, filename):
    return '{}company_logo/{}-{}.{}'.format(
                settings.MEDIA_ROOT,
                instance.cid,
                instance.shortname,
                filename.rpartition('.')[2])


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

    cid          = models.CharField(u'統編', unique=True, max_length=8,
                    validators=[MinLengthValidator(8), validate_all_num])
    name         = models.CharField(u'公司名稱', max_length=64)
    shortname    = models.CharField(u'公司簡稱', max_length=16)
    category     = models.CharField(u'類別', max_length=10, choices=CATEGORYS)
    phone        = models.CharField(u'公司電話', max_length=32,
                    help_text='格式: 區碼-號碼#分機',
                    validators=[validate_phone])
    postal_code  = models.CharField(u'郵遞區號', max_length=5, validators=[validate_all_num])
    address      = models.CharField(u'公司地址', max_length=128)
    website      = models.URLField(u'公司網站', max_length=64, help_text='請輸入網址')
    logo         = models.ImageField(u'LOGO', upload_to=get_logo_path,
                    storage=OverwriteStorage(),
                    help_text='''網站展示、筆記本內頁公司介紹使用，僅接受 jpg, png, gif 格式。
                    建議解析度為 300 dpi 以上，以達到最佳效果。''')
    brief        = models.TextField(u'公司簡介', max_length=110, help_text='字數限制為110字')
    introduction = models.TextField(u'公司介紹', max_length=260, help_text='字數限制為260字')
    hr_name      = models.CharField(u'人資姓名', max_length=32)
    hr_phone     = models.CharField(u'人資電話', max_length=32,
                    help_text='格式: 區碼-號碼#分機',
                    validators=[validate_phone])
    hr_fax       = models.CharField(u'人資傳真', max_length=32,
                    help_text='格式: 區碼-號碼#分機',
                    validators=[validate_phone])
    hr_mobile    = models.CharField(u'人資手機', max_length=32,
                    help_text='格式: 0912-345678',
                    validators=[validate_mobile])
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

class Requirement(models.Model):
    requirement = models.TextField(u'徵才需求', max_length=260, help_text=u'字數限制為260字')
    resume_to   = models.TextField(u'投履歷至', max_length=100, help_text=u'字數限制為100字')

    class Meta:
        abstract = True

class RdssCompanyRequirement(Requirement):
    company = models.OneToOneField(Company, primary_key=True, related_name='rdss_requirement')

    class Meta:
        db_table = 'company_rdss_requirement'

class RecruitCompanyRequirement(Requirement):
    company = models.OneToOneField(Company, primary_key=True, related_name='recruit_requirement')

    class Meta:
        db_table = 'company_recruit_requirement'
