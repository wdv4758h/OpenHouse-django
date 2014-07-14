# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, Group
from datetime import datetime

class StaffManager(BaseUserManager):

    def _create_user(self, studentid, email, password, is_superuser, **extra_fields):
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(studentid=studentid, email=email, is_active=True,
                is_superuser=is_superuser, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, studentid, mail, password=None, **extra_fields):
        return self._create_user(studentid, email, password, False, **extra_fields)

    def create_superuser(self, studentid, email, password, **extra_fields):
        return self._create_user(studentid, email, password, True, **extra_fields)

    def create_nonregistered_user(self, studentid, email, password):
        user = self.model(studentid=studentid, email=email, password=password, is_active=False, is_superuser=False)
        user.save(using=self._db)
        return user

class Staff(AbstractBaseUser):
    """
    A class for OpenHouse staffs

    Look the Default Django User Model for more information :
    https://github.com/django/django/blob/master/django/contrib/auth/models.py
    """

    GENDER = (('M', '男生'), ('F', '女生'))
    studentid = models.CharField(u'學號', max_length=30, unique=True)
    name      = models.CharField(u'姓名', max_length=30)
    gender    = models.CharField(u'性別', choices=GENDER, max_length=1)
    birthday  = models.DateField(u'出生年月日', default=datetime.today())
    groups      = models.ManyToManyField(Group, verbose_name=u'職位', blank=True,
        related_name='staff_set', related_query_name='staff')
    mobile    = models.CharField(u'手機號碼', max_length=16)
    email     = models.EmailField(u'E-mail')
    fb_url    = models.URLField(u'FB個人首頁連結', default='https://www.facebook.com/')
    bs2id     = models.CharField(u'BS2帳號', max_length=12)
    ohbbsid   = models.CharField(u'OH BBS帳號', max_length=12)
    postacct  = models.CharField(u'郵局帳號', max_length=15)

    is_active = models.BooleanField(u'是否啟用', default=False)
    update    = models.DateTimeField(u'最後更新時間', auto_now=True)
    date_join = models.DateTimeField(u'date joined', auto_now_add=True)

    objects = StaffManager()

    USERNAME_FIELD = 'studentid'
    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name = u'OpenHouse 工作人員'
        verbose_name_plural = u'OpenHouse 工作人員'
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
        return u'{} - {}'.format(self.studentid, self.name)

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

    def has_module_perms(self, app_label):
        """
        Returns True if the user has any permissions in the given app label.
        Uses pretty much the same logic as has_perm, above.
        """
        # Active superusers have all permissions.
        if self.is_active and self.is_superuser:
            return True
        return _user_has_module_perms(self, app_label)
