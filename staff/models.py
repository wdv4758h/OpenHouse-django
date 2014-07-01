# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager, Group

class Staff(AbstractBaseUser):
    """
    A class for OpenHouse staffs

    Look the Default Django User Model for more information :
    https://github.com/django/django/blob/master/django/contrib/auth/models.py
    """

    GENDER = (('M', '男生'), ('F', '女生'))
    studentid = models.CharField('學號', max_length=30, unique=True)
    name      = models.CharField('姓名', max_length=30)
    gender    = models.CharField('性別', choices=GENDER, max_length=1)
    birthday  = models.DateField('出生年月日')
    role      = models.ManyToManyField(Group, verbose_name=u'職稱', blank=True,
        related_name='staff_set', related_query_name='staff')
    mobile    = models.CharField('手機號碼', max_length=16)
    email     = models.EmailField('E-mail')
    fb_url    = models.URLField('FB個人首頁連結')
    bs2id     = models.CharField('BS2帳號', max_length=12)
    ohbbsid   = models.CharField('OH BBS帳號', max_length=12)
    postacct  = models.CharField('郵局帳號', max_length=15)

    is_active = models.BooleanField('是否啟用', default=False)
    update    = models.DateTimeField('最後更新時間', auto_now=True)
    date_join = models.DateTimeField('date joined', auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'studentid'
    #REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'OpenHouse 工作人員'
        verbose_name_plural = 'OpenHouse 工作人員'
        #db_table = 'staff'

    def __unicode__(self):
        return self.get_full_name()

    def __str__(self):
        return self.get_full_name()

    def username(self):
        """
        for someone finding the username field
        """
        return self.name

    def get_full_name(self):
        return self.studentid + ' - ' + self.name

    def get_short_name(self):
        return self.studentid

    @property
    def is_staff(self):
        return True

    @property
    def is_superuser(self):
        return True

    def has_perm(self, perm, obj=None):
        """
        Returns True if the user has the specified permission. This method
        queries all available auth backends, but returns immediately if any
        backend returns True. Thus, a user who has permission from a single
        auth backend is assumed to have permission in general. If an object is
        provided, permissions for this specific object are checked.
        """

        # Active staff have all permissions.
        if self.is_active:
            return True

        # Otherwise we need to check the backends.
        return _user_has_perm(self, perm, obj)
