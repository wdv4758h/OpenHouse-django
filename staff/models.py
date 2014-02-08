from django.db import models

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
    #id
    staff_id    = models.PositiveIntegerField(default=0)
    start_time  = models.DateTimeField()
    end_time    = models.DateTimeField()
    description = models.CharField(max_length=100)
    verify      = models.CharField(max_length=100)  #need to modify
    deny_reason = models.CharField(max_length=64)
    timestamp   = models.DateField()

    def __unicode__(self):
        return self.staffid
